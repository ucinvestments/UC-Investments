"""Publish UC's campus foundation endowment tables as a separate dataset."""

import argparse
from datetime import datetime
from html.parser import HTMLParser
from io import BytesIO
import json
import math
from pathlib import Path
import re
from tempfile import NamedTemporaryFile
from urllib.parse import urljoin, urlsplit

import pdfplumber
import requests


INDEX_URL = "https://www.ucop.edu/investment-office/investment-reports/annual-reports/index.html"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[2] / "Webapp/static/data/campus-endowments.json"
CAMPUSES = (
    "Berkeley", "Davis", "Irvine", "Los Angeles", "Merced", "Riverside",
    "San Diego", "San Francisco", "Santa Barbara", "Santa Cruz",
)
VALUE_FIELDS = ("regents", "foundation_gep", "foundation_bgp", "foundation_stip", "foundation_other", "total")
ALLOCATION_FIELDS = (
    "us_equity", "non_us_equity", "global_equity", "us_fixed_income",
    "non_us_fixed_income", "absolute_return", "real_assets", "real_estate",
    "private_equity", "private_credit", "other", "cash_equivalents",
)
MONEY = re.compile(r"(?:\$[\d,]+|-)")
PERCENT = re.compile(r"-?\d+(?:\.\d+)?%")


class EndowmentReportLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchor = None
        self.reports = {}

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.anchor = (dict(attrs).get("href") or "", [])

    def handle_data(self, data):
        if self.anchor:
            self.anchor[1].append(data)

    def handle_endtag(self, tag):
        if tag != "a" or not self.anchor:
            return
        href, text = self.anchor
        self.anchor = None
        label = " ".join("".join(text).split())
        match = re.search(r"Annual Endowment Report\s+(20\d{2})\s*[-–]\s*(\d{2,4})", label, re.I)
        url = urljoin(INDEX_URL, href)
        address = urlsplit(url)
        if match and address.scheme == "https" and address.hostname == "www.ucop.edu" and address.path.endswith(".pdf"):
            start, end = (int(part) for part in match.groups())
            if end < 100:
                end += 2000
            if end == start + 1:
                self.reports[end] = url


def campus_table(text, cell_pattern, count):
    rows = {}
    for campus in CAMPUSES:
        prefix = re.compile(rf"^{re.escape(campus)}(?:\d+(?:,\s*\d+)*)?\s+")
        matches = []
        for line in text.splitlines():
            match = prefix.match(line)
            if match:
                cells = line[match.end():].split()
                if len(cells) == count and all(cell_pattern.fullmatch(cell) for cell in cells):
                    matches.append(cells)
        if len(matches) != 1:
            raise ValueError(f"Expected one {count}-column row for {campus}, found {len(matches)}")
        rows[campus] = matches[0]
    return rows


def parse_report(content, year):
    tables = {}
    headings = ("3.2 Total University Endowed Assets", "3.5 Asset Allocation of Managed Endowment Funds")
    with pdfplumber.open(BytesIO(content)) as report:
        for page in report.pages:
            text = page.extract_text()
            if not text:
                continue
            for heading in headings:
                if heading in text.splitlines():
                    if heading in tables:
                        raise ValueError(f"Duplicate report section: {heading}")
                    tables[heading] = (page.page_number, text)

    values_page, values = tables[headings[0]]
    allocation_page, allocations = tables[headings[1]]
    current = f"June 30, {year}"
    previous = f"June 30, {year - 1}"
    periods = [datetime.strptime(date, "%B %d, %Y").date().isoformat() for date in (current, previous)]
    if any(f"{date} Market Value ($Thousands)" not in values for date in (current, previous)):
        raise ValueError("Market value table dates or units have changed")
    if f"as of {current}" not in allocations or f"Fiscal Year {year}" not in allocations:
        raise ValueError("Asset allocation table date has changed")

    market_rows = campus_table(values, MONEY, 2 * len(VALUE_FIELDS))
    allocation_rows = campus_table(allocations, PERCENT, len(ALLOCATION_FIELDS) + 3)
    campuses = []
    for name in CAMPUSES:
        amounts = [0 if cell == "-" else int(cell[1:].replace(",", "")) * 1000 for cell in market_rows[name]]
        by_period = {}
        for index, period in enumerate(periods):
            start = index * len(VALUE_FIELDS)
            row = dict(zip(VALUE_FIELDS, amounts[start:start + len(VALUE_FIELDS)], strict=True))
            if abs(sum(row[field] for field in VALUE_FIELDS[:-1]) - row["total"]) > 3000:
                raise ValueError(f"Market values do not reconcile for {name} in {period}")
            by_period[period] = row

        *weights, total, net_return, volatility = [float(cell[:-1]) for cell in allocation_rows[name]]
        if total != 100 or not math.isclose(math.fsum(weights), total, abs_tol=0.65):
            raise ValueError(f"Allocation values do not reconcile for {name}")
        campuses.append({
            "campus": name,
            "market_value_usd": by_period,
            "foundation_allocation_percent": dict(zip(ALLOCATION_FIELDS, weights, strict=True)),
            "foundation_return_percent": net_return,
            "foundation_volatility_percent": volatility,
        })
    return {
        "as_of": periods[0],
        "pdf_pages": {"market_values": values_page, "foundation_allocations": allocation_page},
        "scope": (
            "Campus market values include Regents-designated assets and foundation assets. "
            "Asset allocation, returns and volatility describe only the foundation portfolios. "
            "Foundation assets invested in GEP, BGP and STIP overlap with those pools."
        ),
        "campuses": campuses,
    }


def fetch_campus_endowments(session):
    response = session.get(INDEX_URL, timeout=30)
    response.raise_for_status()
    parser = EndowmentReportLinks()
    parser.feed(response.text)
    if not parser.reports:
        raise ValueError("UC's annual reports page has no dated annual endowment report links")
    year = max(parser.reports)
    url = parser.reports[year]
    response = session.get(url, timeout=45)
    response.raise_for_status()
    return {"source_url": url, **parse_report(response.content, year)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    output = parser.parse_args().output
    with requests.Session() as session:
        data = fetch_campus_endowments(session)
    output.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            json.dump(data, handle, indent=2, ensure_ascii=False, allow_nan=False)
            handle.write("\n")
            handle.close()
            temporary.chmod(0o644)
            temporary.replace(output)
        finally:
            temporary.unlink(missing_ok=True)
    print(f"{len(data['campuses'])} campus endowments as of {data['as_of']} → {output}")


if __name__ == "__main__":
    main()
