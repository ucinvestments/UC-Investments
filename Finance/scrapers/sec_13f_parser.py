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
from datetime import datetime
from io import BytesIO
import json
import os
from pathlib import Path
import xml.etree.ElementTree as ET

import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_PATH = os.path.join(BASE_DIR, "sources.json")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

# 13F XML namespaces
NS = {"ns": "http://www.sec.gov/edgar/document/thirteenf/informationtable"}


SEC_HEADERS = {
    "User-Agent": os.environ.get("SEC_USER_AGENT", "UC Investment Explorer admin@ucinvestments.info"),
}
EDGAR_ARCHIVES = "https://www.sec.gov/Archives/edgar/data"


def fetch_latest_filing(session, cik):
    def fetch(url):
        response = session.get(url, headers=SEC_HEADERS, timeout=45)
        response.raise_for_status()
        return response

    recent = fetch(f"https://data.sec.gov/submissions/CIK{int(cik):010}.json").json()["filings"]["recent"]
    filings = [
        (period, filed, int(accession.replace("-", "")), accession, primary, form)
        for form, period, filed, accession, primary in zip(
            recent["form"], recent["reportDate"], recent["filingDate"],
            recent["accessionNumber"], recent["primaryDocument"], strict=True,
        )
        if form in {"13F-HR", "13F-HR/A"} and period
    ]
    if not filings:
        raise ValueError(f"No holdings filing found for SEC filer {cik}")

    period, filed, _, accession, primary, form = max(filings)
    base = f"{EDGAR_ARCHIVES}/{int(cik)}/{accession.replace('-', '')}"
    cover = ET.fromstring(fetch(f"{base}/{Path(primary).name}").content)
    cover_period = cover.findtext(".//{*}periodOfReport")
    if not cover_period or datetime.strptime(cover_period, "%m-%d-%Y").date().isoformat() != period:
        raise ValueError(f"SEC cover page date does not match submissions metadata for {accession}")
    if form.endswith("/A") and cover.findtext(".//{*}amendmentType") != "RESTATEMENT":
        raise ValueError(f"SEC amendment {accession} requires combining multiple information tables")

    files = fetch(f"{base}/index.json").json()["directory"]["item"]
    table_files = [
        item["name"] for item in files
        if item["name"].endswith(".xml") and item["name"] != Path(primary).name
    ]
    if len(table_files) != 1:
        raise ValueError(f"Expected one SEC information table for {accession}, got {len(table_files)}")
    positions = parse_13f_xml(BytesIO(fetch(f"{base}/{table_files[0]}").content))
    count = int(cover.findtext(".//{*}tableEntryTotal"))
    total = int(cover.findtext(".//{*}tableValueTotal"))
    if count == 0 or len(positions) != count or sum(row["value"] for row in positions) != total:
        raise ValueError(f"SEC holdings do not reconcile to the cover sheet for {accession}")
    return {
        "date": period,
        "filed": filed,
        "url": f"{base}/{accession}-index.html",
    }, positions


def parse_13f_xml(xml_path):
    """
    Parse 13F information table XML.
    Returns list of holdings with name, cusip, value, shares, etc.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    holdings = []

    for entry in root.findall(".//ns:infoTable", NS) or root.findall(".//{*}infoTable"):
        holding = {}

        # Extract fields - try with and without namespace
        for tag, key in [
            ("nameOfIssuer", "name"),
            ("titleOfClass", "title_of_class"),
            ("cusip", "cusip"),
            ("value", "value"),
            ("investmentDiscretion", "discretion"),
            ("putCall", "option"),
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

        if holding.get("name"):
            holding["value"] = int(holding["value"])
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
    with open(SOURCES_PATH) as f:
        sources = json.load(f)
    with requests.Session() as session:
        filing, holdings = fetch_latest_filing(session, sources["regents_cik"])
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    write_outputs(
        holdings,
        os.path.join(OUTPUTS_DIR, "sec_13f_holdings.csv"),
        os.path.join(OUTPUTS_DIR, "sec_13f_holdings.json"),
    )
    print(f"Regents holdings as of {filing['date']}: {filing['url']}")


if __name__ == "__main__":
    main()
