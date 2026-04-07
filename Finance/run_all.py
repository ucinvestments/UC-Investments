"""
Run all Finance scrapers and processors.

Usage:
    python Finance/run_all.py           # Run everything (scrapers then aggregate)
    python Finance/run_all.py pdf       # Just UC PDF parser
    python Finance/run_all.py 13f       # Just SEC 13F (UC Regents direct)
    python Finance/run_all.py etf       # Just ETF holdings
    python Finance/run_all.py edgar     # Just EDGAR 13F (hedge funds)
    python Finance/run_all.py funds     # Just fund scrapers (Ariel, INDIX, etc.)
    python Finance/run_all.py aggregate # Just aggregation step
"""

import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCRAPERS = {
    "pdf": ("UC PDF Parser", os.path.join(BASE_DIR, "scrapers", "uc_pdf_parser.py")),
    "13f": ("SEC 13F Parser", os.path.join(BASE_DIR, "scrapers", "sec_13f_parser.py")),
    "etf": ("ETF Holdings", os.path.join(BASE_DIR, "scrapers", "etf_holdings.py")),
    "edgar": ("EDGAR 13F Scraper", os.path.join(BASE_DIR, "scrapers", "edgar_13f_scraper.py")),
    "funds": ("Fund Scrapers", os.path.join(BASE_DIR, "scrapers", "fund_scrapers.py")),
    "aggregate": ("Aggregator", os.path.join(BASE_DIR, "scrapers", "aggregator.py")),
}


def run_scraper(key, name, script_path):
    print(f"\n{'='*60}")
    print(f"  Running: {name}")
    print(f"{'='*60}\n")
    result = subprocess.run([sys.executable, script_path], cwd=os.path.dirname(BASE_DIR))
    if result.returncode != 0:
        print(f"\n  !! {name} failed with exit code {result.returncode}")
    return result.returncode


def main():
    # Default order: all scrapers first, then aggregate last
    default_order = ["pdf", "13f", "etf", "edgar", "funds", "aggregate"]
    targets = sys.argv[1:] if len(sys.argv) > 1 else default_order

    print("UC Investment Data Refresh")
    print(f"Running: {', '.join(targets)}\n")

    results = {}
    for key in targets:
        if key not in SCRAPERS:
            print(f"Unknown scraper: {key}")
            print(f"Available: {', '.join(SCRAPERS.keys())}")
            sys.exit(1)
        name, path = SCRAPERS[key]
        results[key] = run_scraper(key, name, path)

    print(f"\n{'='*60}")
    print("  Summary")
    print(f"{'='*60}")
    for key, rc in results.items():
        status = "OK" if rc == 0 else "FAILED"
        print(f"  {SCRAPERS[key][0]:30s} [{status}]")


if __name__ == "__main__":
    main()
