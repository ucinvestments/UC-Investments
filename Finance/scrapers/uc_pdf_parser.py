"""Read UC pension and endowment holdings disclosures."""

import csv
from datetime import datetime
from decimal import Decimal
from html.parser import HTMLParser
from io import BytesIO
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit

import pdfplumber
import requests

BASE_DIR = Path(__file__).resolve().parents[1]
SOURCES_PATH = BASE_DIR / "sources.json"
OUTPUTS_DIR = BASE_DIR / "outputs"

ASSET_CLASSES = {
    "PUBLIC EQUITY", "FIXED INCOME", "PRIVATE EQUITY", "PRIVATE CREDIT",
    "REAL ESTATE", "REAL ASSETS", "ABSOLUTE RETURN",
}
REPORTED_TOTAL = "TOTAL PUBLIC & ALTERNATIVE ASSETS"
AMOUNT = re.compile(r"[+-]?\$?\d[\d,]*(?:\.\d{1,2})?")


class HoldingsLinks(HTMLParser):
    """Read PDF links labeled as the pool's holdings on the UC policy page."""

    def __init__(self, pool):
        super().__init__()
        self.pool = pool
        self.href = None
        self.label = ""
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.href = dict(attrs).get("href")
            self.label = ""

    def handle_data(self, data):
        if self.href:
            self.label += data

    def handle_endtag(self, tag):
        if tag == "a" and self.href:
            label = " ".join(self.label.lower().split())
            if re.search(rf"\b{self.pool} holdings\b", label):
                self.links.append(self.href)
            self.href = None


def amount_columns(chars):
    # Inter-column whitespace comes from the PDF coordinates. It is much wider
    # than the gaps between digits or words introduced by the text extractor.
    gaps = ((right["x0"] - left["x1"], index)
            for index, (left, right) in enumerate(zip(chars, chars[1:]), 1))
    gap, index = max(gaps, default=(0, 0))
    if gap < 20:
        return None
    value = "".join(char["text"] for char in chars[index:]).replace(" ", "")
    negative = value.startswith("(") and value.endswith(")")
    value = value[1:-1] if negative else value
    if not AMOUNT.fullmatch(value):
        return None
    amount = Decimal(value.replace(",", "").replace("$", ""))
    name = pdfplumber.utils.extract_text(chars[:index], x_tolerance=2).strip()
    return name, -amount if negative else amount


def read_disclosure(pdf_path):
    """Extract listed holdings and verify them against the printed report total."""
    holdings = []
    asset_class = None
    report_date = reported_total = None
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for line in page.extract_text_lines():
                text = " ".join(line["text"].split())
                if match := re.fullmatch(r"Holdings as of (\w+ \d{1,2}, \d{4})", text, re.I):
                    report_date = datetime.strptime(match[1], "%B %d, %Y").date().isoformat()
                if text.upper() in ASSET_CLASSES:
                    asset_class = text.upper()
                    continue
                columns = amount_columns(line["chars"])
                if not columns:
                    continue
                name, amount = columns
                if name.upper() == REPORTED_TOTAL:
                    reported_total = amount
                elif name.upper().startswith("TOTAL "):
                    asset_class = None
                elif asset_class and not name.replace(",", "").isdigit():
                    holdings.append({
                        "name": "Name not disclosed" if name.upper() == "#N/A" else name,
                        "type": asset_class,
                        "amount": amount,
                    })

    if not report_date or not holdings or reported_total is None or reported_total <= 0:
        raise ValueError("UC disclosure is missing its report date, holdings, or printed total")
    parsed_total = sum(holding["amount"] for holding in holdings)
    # UC displays some rows rounded to whole dollars.
    if abs(parsed_total - reported_total) > Decimal(len(holdings) + 1) / 2:
        raise ValueError(f"UC disclosure {report_date} lists {parsed_total:,}, expected {reported_total:,}")
    return report_date, holdings


def fetch_disclosure(session, pool, policy_url):
    page = session.get(policy_url, timeout=30)
    page.raise_for_status()
    parser = HoldingsLinks(pool.lower())
    parser.feed(page.text)
    reports = []
    for link in dict.fromkeys(parser.links):
        url = urljoin(page.url, link)
        target = urlsplit(url)
        if target.scheme != "https" or target.netloc != urlsplit(policy_url).netloc:
            continue
        if not target.path.lower().endswith(".pdf"):
            continue
        response = session.get(url, timeout=60)
        response.raise_for_status()
        date, holdings = read_disclosure(BytesIO(response.content))
        reports.append((date, url, holdings))
    if not reports:
        raise ValueError(f"No {pool} holdings PDF found on {policy_url}")
    return max(reports, key=lambda report: report[0])


def parse_holdings_pdf(pdf_path):
    return read_disclosure(pdf_path)[1]


def write_holdings_csv(holdings, output_path):
    """Write holdings to CSV."""
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Investment_Type", "Amount"])
        writer.writeheader()
        for h in holdings:
            writer.writerow(
                {"Name": h["name"], "Investment_Type": h["type"], "Amount": h["amount"]}
            )
    print(f"  Wrote {len(holdings)} holdings to {output_path}")


def combine_holdings(ucrp_holdings, gep_holdings, output_path):
    """
    Combine UCRP and GEP holdings into a single listed_investments.csv.
    Matches funds by name and aggregates amounts.
    """
    combined = {}

    for h in ucrp_holdings:
        key = (h["name"].upper(), h["type"])
        if key not in combined:
            combined[key] = {
                "Name": h["name"],
                "Investment_Type": h["type"],
                "Total_investment": 0,
                "UCRP_Amount": 0,
                "GEP_Amount": 0,
            }
        combined[key]["UCRP_Amount"] += h["amount"]
        combined[key]["Total_investment"] += h["amount"]

    for h in gep_holdings:
        key = (h["name"].upper(), h["type"])
        if key not in combined:
            combined[key] = {
                "Name": h["name"],
                "Investment_Type": h["type"],
                "Total_investment": 0,
                "UCRP_Amount": 0,
                "GEP_Amount": 0,
            }
        combined[key]["GEP_Amount"] += h["amount"]
        combined[key]["Total_investment"] += h["amount"]

    # Sort by total investment descending
    sorted_holdings = sorted(combined.values(), key=lambda x: x["Total_investment"], reverse=True)

    with open(output_path, "w", newline="") as f:
        fields = ["Name", "Investment_Type", "Total_investment", "UCRP_Amount", "GEP_Amount"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sorted_holdings)

    print(f"  Wrote {len(sorted_holdings)} combined holdings to {output_path}")


def main():
    sources = json.loads(SOURCES_PATH.read_text())
    with requests.Session() as session:
        _, _, ucrp = fetch_disclosure(session, "UCRP", sources["uc_policy_pages"]["ucrp"])
        _, _, gep = fetch_disclosure(session, "GEP", sources["uc_policy_pages"]["gep"])

    OUTPUTS_DIR.mkdir(exist_ok=True)
    write_holdings_csv(ucrp, OUTPUTS_DIR / "ucrp_holdings.csv")
    write_holdings_csv(gep, OUTPUTS_DIR / "gep_holdings.csv")
    combine_holdings(ucrp, gep, OUTPUTS_DIR / "listed_investments.csv")


if __name__ == "__main__":
    main()
