"""
UC Holdings PDF Parser
Parses UCRP and GEP holdings disclosure PDFs from UCOP.
Downloads PDFs, extracts text, and produces a combined CSV of all fund allocations.

Usage:
    python Finance/scrapers/uc_pdf_parser.py

Output:
    Finance/outputs/ucrp_holdings.csv
    Finance/outputs/gep_holdings.csv
    Finance/outputs/listed_investments.csv  (combined)
"""

import csv
import json
import os
import re
import sys
import requests

try:
    import pdfplumber
except ImportError:
    print("Missing dependency: pip install pdfplumber")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_PATH = os.path.join(BASE_DIR, "sources.json")
SOURCES_DIR = os.path.join(BASE_DIR, "sources")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

# Asset class sections as they appear in UC holdings PDFs (matched case-insensitively)
ASSET_CLASSES = [
    "PUBLIC EQUITY",
    "FIXED INCOME",
    "PRIVATE EQUITY",
    "PRIVATE CREDIT",
    "REAL ESTATE",
    "REAL ASSETS",
    "ABSOLUTE RETURN",
]

# Lines containing these exact phrases (case-insensitive) are skipped entirely.
# Note: "TOTAL" by itself is too aggressive -- it would kill fund names like
# "NOMURA HIGH YIELD TOTAL RETURN".  Instead we match lines that START with
# "TOTAL" or contain specific total-line patterns.
SKIP_PATTERNS = [
    "MARKET VALUE",
    "INVESTMENT NAME",
    "AS OF",
    "ASSET NAME",
    "BASE MARKET VALUE",
    "INDIVIDUAL HOLDINGS",
    "PUBLIC ASSETS",
    "ALTERNATIVE ASSETS",
    "TOTAL PUBLIC",
    "TOTAL ALTERNATIVE",
    "TOTAL NET",
    "TOTAL CASH",
    "RECEIVABLES/PAYABLES",
    "HOLDINGS AS OF",
    "HOLDINGS DISCLOSURE",
]


def download_pdf(url, filename):
    """Download PDF to sources directory."""
    path = os.path.join(SOURCES_DIR, filename)
    if os.path.exists(path):
        print(f"  Already downloaded: {filename}")
        return path
    print(f"  Downloading: {filename}")
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    with open(path, "wb") as f:
        f.write(resp.content)
    return path


def _is_skip_line(upper_line):
    """Return True if this line should be skipped (headers, totals, etc.)."""
    for pat in SKIP_PATTERNS:
        if pat in upper_line:
            return True
    # Lines that are exactly "TOTAL <asset_class>" or start with "TOTAL "
    # but allow fund names that *contain* the word TOTAL mid-name.
    if upper_line.startswith("TOTAL ") or upper_line == "TOTAL":
        return True
    return False


def _is_page_number(stripped):
    """Return True if the line is just a page number (bare integer)."""
    return stripped.isdigit()


def _fix_split_amount(name, amount_str):
    """
    Fix a common pdfplumber extraction artifact where leading digit(s) of a
    right-aligned dollar amount get grouped with the left-aligned fund name.

    Example: pdfplumber extracts the line
        "SEQUOIA CAPITAL CHINA GROWTH VI        122,885,808"
    as text "SEQUOIA CAPITAL CHINA GROWTH VI 1 22,885,808" (the '1' drifts left).

    Two split modes:
      A) Comma-boundary split: "1,791,431,073" -> name gets "1", amount "791,431,073"
         Reconstruction: prefix + "," + amount_str == formatted(prefix + amount)
      B) Within-group split: "122,885,808" -> name gets "1", amount "22,885,808"
         The extracted amount starts with a leading-zero or the leading group is
         incomplete AND the base name (without the digit suffix) doesn't look like
         it naturally has a numeric component.

    Returns (fixed_name, fixed_amount_str).
    """
    # Check if name ends with a short digit suffix (1-3 digits) separated by space
    m = re.match(r"^(.+?)\s+(\d{1,3})$", name)
    if not m:
        return name, amount_str

    base_name = m.group(1)
    digit_prefix = m.group(2)

    # Reconstruct the full amount by prepending the stray digits
    raw_amount = amount_str.replace(",", "")
    candidate = digit_prefix + raw_amount
    candidate_int = int(candidate)
    formatted = f"{candidate_int:,}"

    # Check A: comma-boundary split.
    # "1" + "," + "791,431,073" = "1,791,431,073" == formatted
    literal_concat = digit_prefix + "," + amount_str
    if formatted == literal_concat:
        return base_name, str(candidate_int)

    # Check B: within-group split where amount starts with "0".
    # Real dollar amounts never have a leading zero, so this is definitive.
    # E.g., "80,548,888" split as name+"8" and "0,548,888"
    if raw_amount.startswith("0"):
        return base_name, str(candidate_int)

    # No valid reconstruction; the digit is part of the fund name.
    return name, amount_str


def _is_subtotal_line(name, amount):
    """
    Detect lines that are section subtotals rather than real fund entries.
    Subtotals appear as bare numbers or very short 'names' that are actually
    the leading digits of the subtotal amount that got split off.
    """
    # A 'name' that is purely digits (e.g. "8", "3", "5") is a subtotal fragment
    if name.isdigit():
        return True
    # #N/A entries from the PDF
    if name.upper() in ("#N/A",):
        return True
    return False


def parse_holdings_pdf(pdf_path):
    """
    Extract fund holdings from a UC holdings PDF.
    Returns list of dicts: [{"name": str, "type": str, "amount": int}, ...]
    """
    holdings = []
    current_asset_class = None

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            # Try layout-aware extraction first (pdfplumber >= 0.7.0) which
            # preserves column alignment and prevents right-aligned numbers
            # from merging with left-aligned fund names.
            try:
                text = page.extract_text(layout=True)
            except TypeError:
                text = page.extract_text()
            if text:
                full_text += text + "\n"

    lines = full_text.split("\n")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Skip bare page numbers
        if _is_page_number(stripped):
            continue

        # Collapse runs of whitespace for pattern matching, but first
        # note whether there was a large gap (layout mode inserts spaces
        # to preserve column alignment).
        normalized = re.sub(r"\s+", " ", stripped)

        # Check if this line is an asset class header
        upper = normalized.upper()
        matched_class = None
        for ac in ASSET_CLASSES:
            if upper == ac or upper.startswith(ac + " ") or upper.endswith(ac):
                matched_class = ac
                break

        if matched_class:
            current_asset_class = matched_class
            continue

        if current_asset_class is None:
            continue

        # Skip header/total/meta lines
        if _is_skip_line(upper):
            continue

        # Try to extract: FUND NAME followed by a dollar amount
        # Amount format: digits with commas, optionally followed by decimal cents
        # e.g., "58,248,850,263.68" or "3,523,218,069"
        # Pattern: name (non-greedy), whitespace, then a properly comma-formatted
        # number with 1-3 leading digits followed by comma groups of 3.
        match = re.match(
            r"^(.+?)\s+\$?([\d]{1,3}(?:,\d{3})+(?:\.\d+)?)\s*$", normalized
        )

        if match:
            name = match.group(1).strip()
            amount_str = match.group(2)

            # Strip decimal portion (we store whole dollars)
            if "." in amount_str:
                amount_str = amount_str.split(".")[0]

            # Fix pdfplumber split-amount artifact (leading digits of amount
            # absorbed into fund name)
            name, amount_str = _fix_split_amount(name, amount_str)

            # Parse amount
            amount_clean = amount_str.replace(",", "")
            try:
                amount = int(amount_clean)
            except ValueError:
                continue

            # Skip subtotal lines and zero/negative amounts
            if amount <= 0:
                continue
            if _is_subtotal_line(name, amount):
                continue

            holdings.append(
                {
                    "name": name,
                    "type": current_asset_class,
                    "amount": amount,
                }
            )

    return holdings


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
        key = h["name"].upper()
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
        key = h["name"].upper()
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
    os.makedirs(SOURCES_DIR, exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    with open(SOURCES_PATH) as f:
        sources = json.load(f)

    print("=== UC Holdings PDF Parser ===\n")

    # Download PDFs
    print("Downloading PDFs...")
    ucrp_pdf = download_pdf(sources["uc_holdings"]["ucrp"], "ucrp_holdings.pdf")
    gep_pdf = download_pdf(sources["uc_holdings"]["gep"], "gep_holdings.pdf")

    # Parse
    print("\nParsing UCRP holdings...")
    ucrp_holdings = parse_holdings_pdf(ucrp_pdf)
    print(f"  Found {len(ucrp_holdings)} holdings")

    print("\nParsing GEP holdings...")
    gep_holdings = parse_holdings_pdf(gep_pdf)
    print(f"  Found {len(gep_holdings)} holdings")

    # Write individual CSVs
    print("\nWriting output files...")
    write_holdings_csv(ucrp_holdings, os.path.join(OUTPUTS_DIR, "ucrp_holdings.csv"))
    write_holdings_csv(gep_holdings, os.path.join(OUTPUTS_DIR, "gep_holdings.csv"))

    # Combine
    combine_holdings(ucrp_holdings, gep_holdings, os.path.join(OUTPUTS_DIR, "listed_investments.csv"))

    print("\nDone!")


if __name__ == "__main__":
    main()
