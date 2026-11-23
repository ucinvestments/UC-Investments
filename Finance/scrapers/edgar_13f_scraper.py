"""Export SEC 13F holdings for configured fund managers as weight CSVs."""

import csv
import json
from pathlib import Path
import time

import requests

if __package__:
    from .sec_13f_parser import fetch_latest_filing
else:
    from sec_13f_parser import fetch_latest_filing

BASE_DIR = Path(__file__).resolve().parents[1]


def holdings_to_weights(holdings):
    """Convert absolute holdings to portfolio weights."""
    total_value = sum(h.get("value", 0) for h in holdings)
    if total_value == 0:
        return holdings

    for h in holdings:
        h["weight"] = h.get("value", 0) / total_value

    return holdings


def write_fund_csv(holdings, output_path, fund_name, filing):
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
        writer.writerow(["Filing Date (restricted)", filing["filed"]])
        writer.writerow(["Source", filing["url"]])
        writer.writerow(["Note:", f"Reporting period: {filing['date']}"])
        writer.writerow(["Restricted Data:", ""])
        writer.writerow(["Company", "Index Weight"])

        for h in sorted_h:
            writer.writerow([h["name"], f"{h.get('weight', 0):.7f}"])

    print(f"  Wrote {len(holdings)} holdings to {output_path}")


def main():
    sources = json.loads((BASE_DIR / "sources.json").read_text())
    output = BASE_DIR / "outputs"
    output.mkdir(exist_ok=True)
    with requests.Session() as session:
        for key, fund in sources["whale_wisdom_13f"].items():
            filing, holdings = fetch_latest_filing(session, fund["cik"])
            write_fund_csv(
                holdings_to_weights(holdings), output / f"13f_{key}.csv", fund["name"], filing,
            )
            time.sleep(0.2)


if __name__ == "__main__":
    main()
