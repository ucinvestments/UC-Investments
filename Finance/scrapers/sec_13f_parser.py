"""
SEC 13F Filing Parser
Parses the UC Regents 13F-HR filing (XML format) from SEC EDGAR.
Extracts all publicly traded equity positions with values and share counts.

Usage:
    python Finance/scrapers/sec_13f_parser.py

Output:
    Finance/outputs/sec_13f_holdings.csv
    Finance/outputs/sec_13f_holdings.json
"""

import csv
import json
import os
import sys
import xml.etree.ElementTree as ET

import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_PATH = os.path.join(BASE_DIR, "sources.json")
SOURCES_DIR = os.path.join(BASE_DIR, "sources")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

# 13F XML namespaces
NS = {"ns": "http://www.sec.gov/edgar/document/thirteenf/informationtable"}


def download_xml(url, filename):
    """Download 13F XML to sources directory."""
    path = os.path.join(SOURCES_DIR, filename)
    if os.path.exists(path):
        print(f"  Already downloaded: {filename}")
        return path
    print(f"  Downloading: {filename}")
    headers = {"User-Agent": "UC-Investments-Research research@example.com"}
    resp = requests.get(url, headers=headers, timeout=60)
    resp.raise_for_status()
    with open(path, "wb") as f:
        f.write(resp.content)
    return path


def parse_13f_xml(xml_path):
    """
    Parse 13F information table XML.
    Returns list of holdings with name, cusip, value, shares, etc.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    holdings = []

    # Try with namespace first, then without
    info_tables = root.findall(".//ns:infoTable", NS)
    if not info_tables:
        # Try without namespace
        info_tables = root.findall(".//{*}infoTable")
    if not info_tables:
        # Try as direct children or any tag containing the data
        info_tables = root.iter()

    for entry in root.findall(".//ns:infoTable", NS) or root.findall(".//{*}infoTable"):
        holding = {}

        # Extract fields - try with and without namespace
        for tag, key in [
            ("nameOfIssuer", "name"),
            ("titleOfClass", "title_of_class"),
            ("cusip", "cusip"),
            ("value", "value_thousands"),
            ("investmentDiscretion", "discretion"),
            ("votingAuthority", None),
        ]:
            el = entry.find(f"ns:{tag}", NS)
            if el is None:
                el = entry.find(f"{{*}}{tag}")
            if el is not None and key:
                holding[key] = el.text

        # Parse shrsOrPrnAmt
        shares_el = entry.find("ns:shrsOrPrnAmt", NS)
        if shares_el is None:
            shares_el = entry.find("{*}shrsOrPrnAmt")
        if shares_el is not None:
            amt = shares_el.find("ns:sshPrnamt", NS)
            if amt is None:
                amt = shares_el.find("{*}sshPrnamt")
            if amt is not None:
                holding["shares"] = amt.text

            amt_type = shares_el.find("ns:sshPrnamtType", NS)
            if amt_type is None:
                amt_type = shares_el.find("{*}sshPrnamtType")
            if amt_type is not None:
                holding["share_type"] = amt_type.text

        # Parse voting authority
        vote_el = entry.find("ns:votingAuthority", NS)
        if vote_el is None:
            vote_el = entry.find("{*}votingAuthority")
        if vote_el is not None:
            for vtype in ["Sole", "Shared", "None"]:
                vel = vote_el.find(f"ns:{vtype}", NS)
                if vel is None:
                    vel = vote_el.find(f"{{*}}{vtype}")
                if vel is not None:
                    holding[f"voting_{vtype.lower()}"] = vel.text

        # Convert value from thousands to actual
        if "value_thousands" in holding:
            try:
                holding["value"] = int(holding["value_thousands"]) * 1000
            except (ValueError, TypeError):
                holding["value"] = 0

        if holding.get("name"):
            holdings.append(holding)

    return holdings


def write_outputs(holdings, csv_path, json_path):
    """Write holdings to CSV and JSON."""
    # CSV
    fieldnames = [
        "name",
        "title_of_class",
        "cusip",
        "value",
        "shares",
        "share_type",
        "discretion",
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        # Sort by value descending
        sorted_holdings = sorted(holdings, key=lambda x: x.get("value", 0), reverse=True)
        writer.writerows(sorted_holdings)

    # JSON
    sorted_holdings = sorted(holdings, key=lambda x: x.get("value", 0), reverse=True)
    with open(json_path, "w") as f:
        json.dump(
            {
                "filing": "13F-HR",
                "filer": "THE REGENTS OF THE UNIVERSITY OF CALIFORNIA",
                "total_holdings": len(holdings),
                "total_value": sum(h.get("value", 0) for h in holdings),
                "holdings": sorted_holdings,
            },
            f,
            indent=2,
        )

    print(f"  Wrote {len(holdings)} holdings to CSV and JSON")
    total_val = sum(h.get("value", 0) for h in holdings)
    print(f"  Total 13F value: ${total_val:,.0f}")


def main():
    os.makedirs(SOURCES_DIR, exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    with open(SOURCES_PATH) as f:
        sources = json.load(f)

    print("=== SEC 13F Parser ===\n")

    # Download XML
    print("Downloading 13F filing...")
    xml_path = download_xml(
        sources["sec_13f"]["uc_regents"], "uc_regents_13f.xml"
    )

    # Parse
    print("\nParsing 13F XML...")
    holdings = parse_13f_xml(xml_path)
    print(f"  Found {len(holdings)} positions")

    # Write outputs
    print("\nWriting outputs...")
    write_outputs(
        holdings,
        os.path.join(OUTPUTS_DIR, "sec_13f_holdings.csv"),
        os.path.join(OUTPUTS_DIR, "sec_13f_holdings.json"),
    )

    # Top 10 preview
    print("\nTop 10 holdings by value:")
    sorted_h = sorted(holdings, key=lambda x: x.get("value", 0), reverse=True)
    for h in sorted_h[:10]:
        print(f"  {h['name']:40s} ${h.get('value', 0):>15,.0f}")

    print("\nDone!")


if __name__ == "__main__":
    main()
