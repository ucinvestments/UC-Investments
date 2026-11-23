"""Read supplemental private-market fund disclosures from UC."""

from collections import Counter
from datetime import datetime
from io import BytesIO
import re

import pdfplumber

PRIVATE_EQUITY = {
    "title": "Private equity performance",
    "date_pattern": r"Private Equity Investments as of (\w+ \d{1,2}, \d{4})",
    "date_format": "%B %d, %Y",
    "formats": {
        "private_equity": (
            (220, 280, 353, 426, 503, 577, 656, 726),
            ("Fund", "Vintage year", "Committed capital", "Paid-in capital", "Market value",
             "Distributions", "Total value", "Value multiple", "Net IRR"),
        ),
    },
}
ALTERNATIVE_FEES = {
    "title": "Alternative investment fees disclosure",
    "date_pattern": r"Alternative Investment Fees and Expenses, Inception to (\d{1,2}/\d{1,2}/\d{2,4})",
    "date_format": "%m/%d/%y",
    "formats": {
        "cash_flows": (
            (169, 385, 433, 490, 550, 610, 665, 721),
            ("Fund", None, "Vintage year", "Commitments", "Contributions", "Distributions",
             "Distributions and remaining value", "Total gain or loss", "Investment multiple"),
        ),
        "fees": (
            (180, 225, 290, 360, 430, 490, 570, 668),
            ("Fund", "Net IRR", "Gross IRR", "Management fees", "Partnership expenses",
             "Profit sharing paid", "Fees paid by portfolio companies",
             "Expenses and carry", "Total fees and expenses"),
        ),
    },
}
PRIVATE_CATEGORIES = {"PRIVATE EQUITY", "PRIVATE CREDIT", "REAL ESTATE", "REAL ASSETS", "ABSOLUTE RETURN"}
DOLLAR = re.compile(r"\(?-?\d[\d,]*(?:\.\d+)?\)?")


def name_key(name):
    return re.sub(r"[^A-Z0-9]+", "", name.upper()).strip()


def columns(chars, boundaries):
    cells = [[] for _ in range(len(boundaries) + 1)]
    for char in chars:
        index = sum(char["x0"] >= boundary for boundary in boundaries)
        cells[index].append(char)
    return [pdfplumber.utils.extract_text(cell, x_tolerance=0.75).strip() if cell else "" for cell in cells]


def metric_value(label, value):
    if label == "Vintage year" or label.endswith(("multiple", "IRR")):
        return value
    if value.startswith("("):
        return f"(${value[1:]}"
    return f"${value}"


def read_report(content, report):
    records = []
    dates = set()
    with pdfplumber.open(BytesIO(content)) as pdf:
        for page in pdf.pages:
            lines = page.extract_text_lines()
            for line in lines:
                if match := re.search(report["date_pattern"], line["text"], re.I):
                    date_format = report["date_format"]
                    if date_format == "%m/%d/%y" and len(match[1].rsplit("/", 1)[1]) == 4:
                        date_format = "%m/%d/%Y"
                    dates.add(datetime.strptime(match[1], date_format).date().isoformat())

            if report is PRIVATE_EQUITY:
                section = "private_equity"
                start = 0
            else:
                heading = next((i for i, line in enumerate(lines) if line["text"].startswith("Investment Name")), None)
                if heading is None:
                    raise ValueError("Investment fees disclosure is missing its column headings")
                section = "cash_flows" if "Vintage Year" in lines[heading]["text"] else "fees"
                start = heading + 1
            bounds, labels = report["formats"][section]
            for line in lines[start:]:
                cells = columns(line["chars"], bounds)
                name, *values = cells
                values = [value.replace(" ", "") for value in values]
                if not name or name.startswith(("(", "§")):
                    continue
                if "Vintage year" in labels:
                    year = values[labels.index("Vintage year") - 1]
                    if not re.fullmatch(r"(?:19|20)\d{2}", year):
                        continue
                    dollar_fields = values[2:7] if section == "cash_flows" else values[1:6]
                else:
                    dollar_fields = values[2:]
                if not any(DOLLAR.fullmatch(value) for value in dollar_fields) or not all(
                    value in {"", "-"} or DOLLAR.fullmatch(value) for value in dollar_fields
                ):
                    continue
                metrics = [
                    {"label": label, "value": metric_value(label, value)}
                    for label, value in zip(labels[1:], values, strict=True) if label and value and value != "-"
                ]
                records.append((section, name, metrics))
    if len(dates) != 1 or {section for section, _, _ in records} != set(report["formats"]):
        raise ValueError(f"Could not read a dated {report['title']} table")
    return dates.pop(), records


def enrich_funds(session, urls, funds):
    sources = {}
    by_name = Counter(name_key(fund["name"]) for fund in funds)
    available = {
        name_key(fund["name"]): fund for fund in funds
        if fund["category"] in PRIVATE_CATEGORIES and by_name[name_key(fund["name"])] == 1
        and fund["name"] != "Name not disclosed"
    }

    for key, report in (("private_equity", PRIVATE_EQUITY), ("alternative_fees", ALTERNATIVE_FEES)):
        url = urls[key]
        response = session.get(url, timeout=60)
        response.raise_for_status()
        date, rows = read_report(response.content, report)
        sources[key] = {"name": report["title"], "date": date, "url": url}
        matches = Counter((section, name_key(name)) for section, name, _ in rows)
        for section, name, metrics in rows:
            normalized = name_key(name)
            if normalized in available and matches[section, normalized] == 1:
                title = {"cash_flows": "Commitments and cash flows", "fees": "Fees and expenses"}.get(section, report["title"])
                available[normalized].setdefault("disclosures", []).append({
                    "source": key, "title": title, "name": name, "metrics": metrics,
                })
    return sources
