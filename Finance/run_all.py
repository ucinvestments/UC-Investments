"""Refresh the public explorer snapshot or run an individual research scraper."""

import argparse
from pathlib import Path
import subprocess
import sys

from snapshot import DEFAULT_OUTPUT, FINANCE_DIR, refresh

SCRAPERS = {
    "pdf": "uc_pdf_parser.py",
    "13f": "sec_13f_parser.py",
    "etf": "etf_holdings.py",
    "edgar": "edgar_13f_scraper.py",
    "funds": "fund_scrapers.py",
    "aggregate": "aggregator.py",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="*", metavar="TARGET",
                        help=f"Optional research steps (no publication): {', '.join(SCRAPERS)}")
    parser.add_argument("--output", type=Path, help="Write the explorer snapshot to this path")
    args = parser.parse_args()

    for target in args.targets:
        if target not in SCRAPERS:
            parser.error(f"unknown target {target}")
    if args.targets and args.output:
        parser.error("--output applies to the full explorer refresh")

    if args.targets:
        for target in args.targets:
            subprocess.run(
                [sys.executable, FINANCE_DIR / "scrapers" / SCRAPERS[target]],
                cwd=FINANCE_DIR.parent, check=True,
            )
    else:
        refresh(args.output or DEFAULT_OUTPUT)


if __name__ == "__main__":
    main()
