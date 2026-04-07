"""
Aggregator: combines scraper outputs into the format expected by the webapp/backend.

Reads fund allocations from listed_investments.csv, multiplies by per-holding weights
from composition files (ETF holdings, EDGAR 13F filings), fuzzy-matches company names
across funds, and outputs:
  - full_investments_false_estimation_true_class_grouping.json  (consolidated voting shares)
  - full_investments_false_estimation_false_class_grouping.json (separate voting shares)
  - asset_classes.json
"""

import csv
import json
import os
import re
import sys

from thefuzz import process, fuzz

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

LISTED_INVESTMENTS_PATH = os.path.join(OUTPUTS_DIR, "listed_investments.csv")

# Fund name substring -> composition CSV filename
FUND_FILE_MAP = {
    "MSCI ACWI IMI": "etf_ishares_acwi.csv",
    "SSGA S&P 500": "etf_spdr_spyx.csv",
    "SPDR MSCI": "etf_spdr_qus.csv",
    "ADAGE CAPITAL": "13f_adage_capital.csv",
    "HIMALAYA CAPITAL": "13f_himalaya_capital.csv",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_listed_investments():
    """Return list of dicts from listed_investments.csv."""
    funds = []
    with open(LISTED_INVESTMENTS_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            funds.append({
                "name": row["Name"].strip(),
                "investment_type": row["Investment_Type"].strip(),
                "total": float(row["Total_investment"]),
                "ucrp": float(row["UCRP_Amount"]),
                "gep": float(row["GEP_Amount"]),
            })
    return funds


def match_fund_to_file(fund_name):
    """Return composition CSV path if fund_name matches a known pattern, else None."""
    upper = fund_name.upper()
    for pattern, filename in FUND_FILE_MAP.items():
        if pattern in upper:
            path = os.path.join(OUTPUTS_DIR, filename)
            if os.path.exists(path):
                return path
    return None


def load_etf_holdings(filepath):
    """Load ETF-style CSV (name,ticker,weight) and return list of (name, weight)."""
    holdings = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"].strip()
            weight = float(row["weight"])
            # Some ETF files express weights as percentages (>1 means percentage)
            # We'll normalize later in the aggregation step
            holdings.append((name, weight))
    return holdings


def load_13f_holdings(filepath):
    """
    Load EDGAR 13F-style CSV with metadata header rows.
    Format: 8 header rows, then 'Company,Index Weight' followed by data.
    Returns list of (company_name, weight).
    """
    holdings = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        data_started = False
        for row in reader:
            if len(row) < 2:
                continue
            if row[0].strip() == "Company" and row[1].strip() == "Index Weight":
                data_started = True
                continue
            if not data_started:
                continue
            company = row[0].strip()
            try:
                weight = float(row[1])
            except (ValueError, IndexError):
                continue
            if company:
                holdings.append((company, weight))
    return holdings


def load_holdings(filepath):
    """Detect file type and load holdings, normalizing weights to fractional form."""
    basename = os.path.basename(filepath)
    if basename.startswith("13f_"):
        holdings = load_13f_holdings(filepath)
    else:
        holdings = load_etf_holdings(filepath)

    # Auto-detect whether weights are fractional (sum ~1) or percentage (sum ~100).
    # If the sum of weights exceeds 5, assume they are percentages and divide by 100.
    weight_sum = sum(w for _, w in holdings)
    if weight_sum > 5:
        holdings = [(name, w / 100.0) for name, w in holdings]

    return holdings


def normalize_name(name, consolidate_voting_shares=False):
    """Normalize a company name for matching."""
    n = name.lower().strip()
    n = n.replace("corporation", "corp").replace("incorporated", "inc")
    if consolidate_voting_shares:
        n = re.sub(r"\bclass\s+\w+", " ", n)
        n = re.sub(r"\bcl\s+\w+", " ", n)
    else:
        n = n.replace("class ", "cl ")
    # Collapse whitespace
    n = re.sub(r"\s+", " ", n).strip()
    return n


def sub_dict_search(investments_list, name):
    """Find an investment dict by asset name, return (dict, index) or (None, None)."""
    for i, item in enumerate(investments_list):
        if item["asset"] == name:
            return item, i
    return None, None


# ---------------------------------------------------------------------------
# Core aggregation
# ---------------------------------------------------------------------------

def aggregate(consolidate_voting_shares=True):
    """
    Aggregate all fund composition data into the standard JSON format.

    Returns the full investments dict:
    {
        "invesmtent names list": [...],
        "summed investments": [{
            "asset": "company name",
            "total investment": dollar_amount,
            "funding sources": [
                {"fund name:": "FUND", "ammount_invested": dollar_amount}
            ]
        }, ...],
        "Private holdings (not analyzed)": dollar_amount
    }
    """
    funds = load_listed_investments()

    total_investments = {
        "invesmtent names list": [],
        "summed investments": [],
    }

    total_sum = 0
    total_upper_sum = 0

    for fund in funds:
        fund_name = fund["name"]
        money_in_fund = fund["total"]
        total_upper_sum += money_in_fund

        comp_file = match_fund_to_file(fund_name)
        if comp_file is None:
            # No composition data available — counts as private/unanalyzed
            continue

        holdings = load_holdings(comp_file)
        if not holdings:
            continue

        fund_sum = 0
        weight_sum = 0

        for company_name, weight in holdings:
            sec_name = normalize_name(company_name, consolidate_voting_shares)
            if not sec_name:
                continue

            # Safety net: if any individual weight > 1 after file-level
            # normalization, treat it as a percentage (matches old aggregator behavior)
            if weight > 1:
                weight = weight * 0.01

            names_list = total_investments["invesmtent names list"]

            if sec_name not in names_list:
                # Fuzzy match against existing names
                if names_list:
                    match = process.extractOne(
                        sec_name, names_list, scorer=fuzz.token_sort_ratio
                    )
                    if match and match[1] >= 95:
                        sec_name = match[0]
                    else:
                        names_list.append(sec_name)
                        total_investments["summed investments"].append({
                            "asset": sec_name,
                            "total investment": 0,
                            "funding sources": [],
                        })
                else:
                    names_list.append(sec_name)
                    total_investments["summed investments"].append({
                        "asset": sec_name,
                        "total investment": 0,
                        "funding sources": [],
                    })

            _, idx = sub_dict_search(total_investments["summed investments"], sec_name)
            if idx is None:
                print(f"  WARNING: could not find '{sec_name}' after insert — skipping")
                continue

            dollar_amount = money_in_fund * weight
            total_investments["summed investments"][idx]["total investment"] += dollar_amount
            total_investments["summed investments"][idx]["funding sources"].append({
                "fund name:": fund_name,
                "ammount_invested": dollar_amount,
            })
            total_sum += dollar_amount
            fund_sum += dollar_amount
            weight_sum += weight

        print(f"  {fund_name}: allocated ${fund_sum:,.0f} of ${money_in_fund:,.0f} "
              f"(weight sum: {weight_sum:.4f})")

    total_investments["Private holdings (not analyzed)"] = total_upper_sum - total_sum

    # Sort by total investment descending
    total_investments["summed investments"].sort(
        key=lambda x: x["total investment"], reverse=True
    )

    return total_investments


def build_asset_classes():
    """
    Group funds from listed_investments.csv by asset class.

    Output format matches the backend /asset-classes endpoint:
    [
        {
            "A.s.set ._Class": "PUBLIC EQUITY",
            "InVesTmeNts": ["FUND1", "FUND2", ...],
            "Total I\u2102nvest\u2208d": dollar_amount
        },
        ...
    ]
    """
    funds = load_listed_investments()
    output = []

    for fund in funds:
        asset_type = fund["investment_type"]
        found = False
        for entry in output:
            if entry["A.s.set ._Class"] == asset_type:
                entry["InVesTmeNts"].append(fund["name"])
                entry["Total I\u2102nvest\u2208d"] += fund["total"]
                found = True
                break
        if not found:
            output.append({
                "A.s.set ._Class": asset_type,
                "InVesTmeNts": [fund["name"]],
                "Total I\u2102nvest\u2208d": fund["total"],
            })

    return output


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not os.path.exists(LISTED_INVESTMENTS_PATH):
        print(f"ERROR: {LISTED_INVESTMENTS_PATH} not found. Run scrapers first.")
        sys.exit(1)

    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    # Generate both class-grouping variants
    for consolidate in [True, False]:
        label = "true" if consolidate else "false"
        print(f"\nAggregating (consolidate_voting_shares={consolidate})...")
        result = aggregate(consolidate_voting_shares=consolidate)

        out_path = os.path.join(
            OUTPUTS_DIR,
            f"full_investments_false_estimation_{label}_class_grouping.json",
        )
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f)
        print(f"  -> {out_path}")
        print(f"     {len(result['summed investments'])} companies, "
              f"${result['Private holdings (not analyzed)']:,.0f} unanalyzed")

    # Asset classes
    print("\nBuilding asset classes...")
    asset_classes = build_asset_classes()
    ac_path = os.path.join(OUTPUTS_DIR, "asset_classes.json")
    with open(ac_path, "w", encoding="utf-8") as f:
        json.dump(asset_classes, f)
    print(f"  -> {ac_path} ({len(asset_classes)} classes)")

    print("\nDone.")


if __name__ == "__main__":
    main()
