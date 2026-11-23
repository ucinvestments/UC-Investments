"""Read dated holdings exports from iShares and State Street."""

import csv
from datetime import datetime
from io import BytesIO, StringIO
import json
import re
from pathlib import Path

import openpyxl
import requests

BASE_DIR = Path(__file__).resolve().parents[1]


def read_ishares_csv(content):
    stream = StringIO(content.decode("utf-8-sig"))
    rows = csv.reader(stream)
    for row in rows:
        if row and row[0] == "Fund Holdings as of":
            date = datetime.strptime(row[1], "%b %d, %Y").date().isoformat()
            break
    else:
        raise ValueError("iShares export is missing its holdings date")

    for header in rows:
        if header and header[0] == "Ticker":
            break
    else:
        raise ValueError("iShares export is missing its holdings table")

    positions = [
        {
            "name": row["Name"], "ticker": row["Ticker"],
            "exchange": row["Exchange"], "weight": float(row["Weight (%)"]) / 100,
        }
        for row in csv.DictReader(stream, fieldnames=header)
        if row.get("Asset Class") == "Equity" and row.get("Name")
    ]
    return date, positions


def read_ssga_xlsx(content, expected_ticker=None):
    workbook = openpyxl.load_workbook(BytesIO(content), read_only=True, data_only=True)
    try:
        rows = workbook.active.values
        if expected_ticker:
            ticker_row = next((row for row in rows if row[0] == "Ticker Symbol:"), None)
            if not ticker_row or ticker_row[1] != expected_ticker:
                raise ValueError(f"Expected a State Street export for {expected_ticker}")
        date_row = next((row for row in rows if row[0] == "Holdings:"), None)
        if not date_row:
            raise ValueError("State Street export is missing its holdings date")
        date = datetime.strptime(date_row[1], "As of %d-%b-%Y").date().isoformat()
        header = next((row for row in rows if row[0] == "Name"), None)
        if not header:
            raise ValueError("State Street export is missing its holdings table")
        name, ticker, identifier, weight = (
            header.index(column) for column in ("Name", "Ticker", "Identifier", "Weight")
        )
        maturity = header.index("Maturity") if "Maturity" in header else None
        positions = [
            {
                "name": row[name], "ticker": str(row[ticker]),
                "cusip": str(row[identifier]), "weight": float(row[weight]) / 100,
            }
            for row in rows
            if row[name] and row[ticker] not in (None, "", "-")
            and row[identifier] not in (None, "", "-") and row[weight] is not None
            and (maturity is None or row[maturity] in (None, "", "-"))
            and not re.search(r"\b(?:FUT|FUTURE|FUTURES)\b", row[name], re.I)
        ]
        return date, positions
    finally:
        workbook.close()


def fetch_etf(session, url):
    response = session.get(url, timeout=45)
    response.raise_for_status()
    reader = read_ssga_xlsx if url.endswith(".xlsx") else read_ishares_csv
    date, positions = reader(response.content)
    if not positions:
        raise ValueError(f"No equity holdings found in {url}")
    return date, positions


def main():
    sources = json.loads((BASE_DIR / "sources.json").read_text())
    output = BASE_DIR / "outputs"
    output.mkdir(exist_ok=True)
    with requests.Session() as session:
        for name, url in sources["etf_holdings"].items():
            date, holdings = fetch_etf(session, url)
            with (output / f"etf_{name}.csv").open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=["name", "ticker", "weight"], extrasaction="ignore")
                writer.writeheader()
                writer.writerows(sorted(holdings, key=lambda row: row["weight"], reverse=True))
            print(f"{name}: {len(holdings)} positions as of {date}")


if __name__ == "__main__":
    main()
