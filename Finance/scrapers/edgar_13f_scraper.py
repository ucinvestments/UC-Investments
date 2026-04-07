"""
SEC EDGAR 13F Scraper
Fetches the latest 13F-HR filings for hedge funds (Adage Capital, Himalaya Capital, etc.)
from SEC EDGAR and extracts their portfolio holdings.

Usage:
    python Finance/scrapers/edgar_13f_scraper.py

Output:
    Finance/outputs/13f_<fund_name>.csv
"""

import csv
import json
import os
import sys
import time
import xml.etree.ElementTree as ET

import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_PATH = os.path.join(BASE_DIR, "sources.json")
SOURCES_DIR = os.path.join(BASE_DIR, "sources")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

EDGAR_BASE = "https://efts.sec.gov/LATEST/search-index?q=%2213F-HR%22&dateRange=custom&startdt=2024-01-01&forms=13F-HR"
EDGAR_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik}.json"
EDGAR_FILING_BASE = "https://www.sec.gov/Archives/edgar/data"

HEADERS = {
    "User-Agent": "UC-Investments-Research research@example.com",
    "Accept-Encoding": "gzip, deflate",
}

NS_13F = {"ns": "http://www.sec.gov/edgar/document/thirteenf/informationtable"}


def get_latest_13f_url(cik):
    """
    Find the latest 13F-HR filing URL for a given CIK.
    Uses the EDGAR submissions API.
    """
    # Pad CIK to 10 digits
    cik_padded = cik.lstrip("0").zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"

    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])
    dates = recent.get("filingDate", [])

    # Find the most recent 13F-HR or 13F-HR/A
    for i, form in enumerate(forms):
        if form in ("13F-HR", "13F-HR/A"):
            accession = accessions[i].replace("-", "")
            filing_date = dates[i]
            return cik.lstrip("0"), accession, filing_date

    return None, None, None


def get_13f_xml_url(cik_num, accession):
    """Find the information table XML within a 13F filing."""
    index_url = f"{EDGAR_FILING_BASE}/{cik_num}/{accession}/index.json"
    resp = requests.get(index_url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    index_data = resp.json()

    for item in index_data.get("directory", {}).get("item", []):
        name = item.get("name", "").lower()
        if "infotable" in name or "information" in name:
            return f"{EDGAR_FILING_BASE}/{cik_num}/{accession}/{item['name']}"

    # Fallback: look for any XML file
    for item in index_data.get("directory", {}).get("item", []):
        name = item.get("name", "").lower()
        if name.endswith(".xml") and "primary" not in name:
            return f"{EDGAR_FILING_BASE}/{cik_num}/{accession}/{item['name']}"

    return None


def parse_13f_info_table(xml_content):
    """Parse 13F information table XML content into holdings list."""
    root = ET.fromstring(xml_content)
    holdings = []

    # Try multiple namespace patterns
    entries = root.findall(".//ns:infoTable", NS_13F)
    if not entries:
        entries = root.findall(".//{*}infoTable")

    for entry in entries:
        holding = {}
        for tag, key in [
            ("nameOfIssuer", "name"),
            ("titleOfClass", "title_of_class"),
            ("cusip", "cusip"),
            ("value", "value_thousands"),
        ]:
            el = entry.find(f"ns:{tag}", NS_13F)
            if el is None:
                el = entry.find(f"{{*}}{tag}")
            if el is not None:
                holding[key] = el.text

        # Parse shares
        shares_el = entry.find("ns:shrsOrPrnAmt", NS_13F)
        if shares_el is None:
            shares_el = entry.find("{*}shrsOrPrnAmt")
        if shares_el is not None:
            amt = shares_el.find("ns:sshPrnamt", NS_13F)
            if amt is None:
                amt = shares_el.find("{*}sshPrnamt")
            if amt is not None:
                holding["shares"] = amt.text

        if "value_thousands" in holding:
            try:
                holding["value"] = int(holding["value_thousands"]) * 1000
            except (ValueError, TypeError):
                holding["value"] = 0

        if holding.get("name"):
            holdings.append(holding)

    return holdings


def holdings_to_weights(holdings):
    """Convert absolute holdings to portfolio weights."""
    total_value = sum(h.get("value", 0) for h in holdings)
    if total_value == 0:
        return holdings

    for h in holdings:
        h["weight"] = h.get("value", 0) / total_value

    return holdings


def write_fund_csv(holdings, output_path, fund_name, filing_date):
    """Write fund holdings in the project's standard CSV format."""
    total_value = sum(h.get("value", 0) for h in holdings)
    sorted_h = sorted(holdings, key=lambda x: x.get("value", 0), reverse=True)

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        # Metadata header (matching existing format)
        writer.writerow(["Fund Name (AS CITED)", fund_name])
        writer.writerow(["Internal Name", fund_name])
        writer.writerow(["Restricted y/n", "n"])
        writer.writerow(["Ammount of companies in fund (restricted)", str(len(holdings))])
        writer.writerow(["Filing Date (restricted)", filing_date])
        writer.writerow(["Source", f"SEC EDGAR 13F-HR"])
        writer.writerow(["Note:", ""])
        writer.writerow(["Restricted Data:", ""])
        writer.writerow(["Company", "Index Weight"])

        for h in sorted_h:
            writer.writerow([h["name"], f"{h.get('weight', 0):.7f}"])

    print(f"  Wrote {len(holdings)} holdings to {output_path}")


def main():
    os.makedirs(SOURCES_DIR, exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    with open(SOURCES_PATH) as f:
        sources = json.load(f)

    print("=== EDGAR 13F Scraper ===\n")

    funds = sources.get("whale_wisdom_13f", {})

    for fund_key, fund_info in funds.items():
        cik = fund_info["cik"]
        name = fund_info["name"]
        print(f"\nProcessing: {name} (CIK: {cik})")

        # Find latest 13F
        print("  Finding latest 13F-HR filing...")
        cik_num, accession, filing_date = get_latest_13f_url(cik)

        if not accession:
            print(f"  Error: No 13F-HR found for {name}")
            continue

        print(f"  Filing date: {filing_date}")

        # Get XML URL
        time.sleep(0.2)  # Be polite to EDGAR
        xml_url = get_13f_xml_url(cik_num, accession)
        if not xml_url:
            print(f"  Error: Could not find info table XML")
            continue

        print(f"  Downloading info table...")
        time.sleep(0.2)
        resp = requests.get(xml_url, headers=HEADERS, timeout=30)
        resp.raise_for_status()

        # Save raw XML
        xml_path = os.path.join(SOURCES_DIR, f"13f_{fund_key}.xml")
        with open(xml_path, "wb") as f:
            f.write(resp.content)

        # Parse
        holdings = parse_13f_info_table(resp.content)
        holdings = holdings_to_weights(holdings)
        print(f"  Found {len(holdings)} positions")

        # Write output
        output_path = os.path.join(OUTPUTS_DIR, f"13f_{fund_key}.csv")
        write_fund_csv(holdings, output_path, name, filing_date)

        total_val = sum(h.get("value", 0) for h in holdings)
        print(f"  Total portfolio value: ${total_val:,.0f}")

        # Top 5 preview
        sorted_h = sorted(holdings, key=lambda x: x.get("value", 0), reverse=True)
        for h in sorted_h[:5]:
            print(f"    {h['name']:35s} {h.get('weight', 0):8.4%}  ${h.get('value', 0):>13,.0f}")

        time.sleep(0.5)  # Rate limit between filers

    print("\nDone!")


if __name__ == "__main__":
    main()
