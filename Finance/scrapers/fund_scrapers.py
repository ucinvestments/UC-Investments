"""
Fund Holdings Scrapers
Scrapes holdings for mutual funds and separate accounts that UC invests in.

Handles:
  - Ariel US Small Cap: Scrapes holdings from Ariel Investments website
  - Kotak India Growth (INDIX): Fetches holdings from ALPS website or EDGAR N-PORT
  - Arrowstreet Global 130-30: Manual stub (separate account, no public source)
  - Earnest Partners Small Cap Value: Manual stub (no public source)

Usage:
    python Finance/scrapers/fund_scrapers.py

Output:
    Finance/outputs/fund_<fund_name>.csv
"""

import csv
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET

import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_PATH = os.path.join(BASE_DIR, "sources.json")
SOURCES_DIR = os.path.join(BASE_DIR, "sources")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

EDGAR_HEADERS = {
    "User-Agent": "UC-Investments-Research research@example.com",
    "Accept-Encoding": "gzip, deflate",
}


def write_fund_csv(holdings, output_path, fund_name, internal_name, source_url,
                   filing_date="", note="", restricted="n"):
    """Write fund holdings in the project's standard metadata CSV format."""
    sorted_h = sorted(holdings, key=lambda x: x.get("weight", 0), reverse=True)

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Fund Name (AS CITED)", fund_name])
        writer.writerow(["Internal Name", internal_name])
        writer.writerow(["Restricted y/n", restricted])
        writer.writerow(["Ammount of companies in fund (restricted)", str(len(holdings))])
        writer.writerow(["Filing Date (restricted)", filing_date])
        writer.writerow(["Source", source_url])
        writer.writerow(["Note:", note])
        writer.writerow(["Restricted Data:", ""])
        writer.writerow(["Company", "Index Weight"])

        for h in sorted_h:
            writer.writerow([h["name"], f"{h['weight']:.7f}"])

    print(f"  Wrote {len(holdings)} holdings to {output_path}")


# ---------------------------------------------------------------------------
# Ariel US Small Cap
# ---------------------------------------------------------------------------

def scrape_ariel_small_cap(url):
    """
    Scrape Ariel US Small Cap holdings from arielinvestments.com.

    Ariel publishes holdings on their fund pages. The page typically contains
    a table with company names and weights. We also try to find a direct
    PDF/CSV link for holdings data.
    """
    print(f"  Fetching: {url}")

    if BeautifulSoup is None:
        print("  Warning: beautifulsoup4 not installed, trying regex fallback")
        print("  Install with: pip install beautifulsoup4")

    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    html = resp.text

    # Save raw source
    source_path = os.path.join(SOURCES_DIR, "fund_ariel_small_cap.html")
    with open(source_path, "w", encoding="utf-8") as f:
        f.write(html)

    holdings = []

    # Strategy 1: Parse HTML table with BeautifulSoup
    if BeautifulSoup is not None:
        holdings = _parse_ariel_html(html)

    # Strategy 2: Regex fallback if BS4 unavailable or found nothing
    if not holdings:
        holdings = _parse_ariel_regex(html)

    # Strategy 3: Look for a linked holdings PDF or CSV
    if not holdings:
        print("  Trying to find holdings PDF link...")
        holdings = _try_ariel_pdf_link(html, url)

    return holdings


def _parse_ariel_html(html):
    """Parse holdings from Ariel fund page using BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    holdings = []

    # Look for holdings tables - Ariel uses various table formats
    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) < 2:
                continue

            # Try to find rows with a company name and a percentage weight
            text_vals = [c.get_text(strip=True) for c in cells]

            # Look for a percentage value in the row
            for i, val in enumerate(text_vals):
                pct_match = re.search(r"(\d+\.?\d*)\s*%", val)
                if pct_match and i > 0:
                    name = text_vals[0].strip()
                    if name and not name.lower().startswith(("company", "holding", "name", "total")):
                        weight = float(pct_match.group(1)) / 100.0
                        holdings.append({"name": name, "ticker": "", "weight": weight})
                    break
                elif pct_match and i == 0 and len(text_vals) > 1:
                    # Weight might be in first column, name in second
                    continue

    # Also look for structured holdings sections (div-based layouts)
    if not holdings:
        # Some Ariel pages use div-based card layouts for holdings
        holding_sections = soup.find_all(
            ["div", "section"],
            class_=re.compile(r"(holding|portfolio|position)", re.I)
        )
        for section in holding_sections:
            name_el = section.find(class_=re.compile(r"(name|company|title)", re.I))
            weight_el = section.find(class_=re.compile(r"(weight|percent|pct)", re.I))
            if name_el and weight_el:
                name = name_el.get_text(strip=True)
                weight_text = weight_el.get_text(strip=True)
                pct_match = re.search(r"(\d+\.?\d*)", weight_text)
                if pct_match and name:
                    weight = float(pct_match.group(1)) / 100.0
                    holdings.append({"name": name, "ticker": "", "weight": weight})

    if holdings:
        print(f"  Parsed {len(holdings)} holdings from HTML")
    return holdings


def _parse_ariel_regex(html):
    """Fallback regex parsing for Ariel holdings page."""
    holdings = []

    # Pattern: look for company name followed by percentage
    # Ariel pages often list holdings as "Company Name ... X.XX%"
    pattern = re.compile(
        r'(?:class="[^"]*(?:holding|company|name)[^"]*"[^>]*>)\s*([A-Z][^<]{2,50})<.*?'
        r'(\d{1,3}\.\d{1,4})\s*%',
        re.DOTALL | re.IGNORECASE
    )
    for match in pattern.finditer(html):
        name = match.group(1).strip()
        weight = float(match.group(2)) / 100.0
        if name and weight > 0:
            holdings.append({"name": name, "ticker": "", "weight": weight})

    if holdings:
        print(f"  Parsed {len(holdings)} holdings via regex")
    return holdings


def _try_ariel_pdf_link(html, base_url):
    """Look for a direct holdings PDF link on the Ariel page."""
    # Ariel publishes holdings PDFs with pattern like:
    # /wp-content/uploads/YYYY/MM/SMALL_Holdings-YYYY-MM-DD.pdf
    pdf_pattern = re.compile(
        r'href="([^"]*(?:holdings|HOLDINGS)[^"]*\.(?:pdf|csv|xlsx))"',
        re.IGNORECASE
    )
    matches = pdf_pattern.findall(html)

    for match in matches:
        pdf_url = match
        if not pdf_url.startswith("http"):
            # Make absolute URL
            from urllib.parse import urljoin
            pdf_url = urljoin(base_url, pdf_url)

        print(f"  Found holdings file: {pdf_url}")
        # Download but don't try to parse PDF here -- note the URL for manual use
        try:
            resp = requests.get(pdf_url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            ext = "pdf" if pdf_url.endswith(".pdf") else "csv"
            save_path = os.path.join(SOURCES_DIR, f"fund_ariel_small_cap_holdings.{ext}")
            with open(save_path, "wb") as f:
                f.write(resp.content)
            print(f"  Downloaded holdings file to: {save_path}")

            if ext == "csv":
                return _parse_generic_csv(save_path)
        except Exception as e:
            print(f"  Warning: Could not download {pdf_url}: {e}")

    print("  Could not extract structured holdings from Ariel website")
    print("  MANUAL: Check for updated holdings at https://www.arielinvestments.com/ariel-fund/")
    return []


def _parse_generic_csv(file_path):
    """Try to parse a generic holdings CSV."""
    holdings = []
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = None
            weight = None
            for key, val in row.items():
                k = key.lower().strip()
                if k in ("name", "company", "holding", "security"):
                    name = val.strip()
                if k in ("weight", "weight (%)", "% of fund", "percent", "pct"):
                    try:
                        w = float(val.replace("%", "").replace(",", "").strip())
                        weight = w / 100.0 if w > 1 else w
                    except (ValueError, TypeError):
                        pass
            if name and weight is not None:
                holdings.append({"name": name, "ticker": "", "weight": weight})
    return holdings


# ---------------------------------------------------------------------------
# Kotak India Growth (INDIX) via ALPS or EDGAR N-PORT
# ---------------------------------------------------------------------------

def scrape_kotak_india_growth(url):
    """
    Scrape ALPS/Kotak India Growth (INDIX) holdings.

    Strategy:
    1. Try ALPS website for holdings data
    2. Fall back to SEC EDGAR N-PORT filing
    """
    print(f"  Fetching ALPS page: {url}")

    holdings = []

    # Strategy 1: ALPS website
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        html = resp.text

        source_path = os.path.join(SOURCES_DIR, "fund_kotak_indix.html")
        with open(source_path, "w", encoding="utf-8") as f:
            f.write(html)

        holdings = _parse_alps_holdings(html)
    except Exception as e:
        print(f"  Warning: Could not fetch ALPS page: {e}")

    # Strategy 2: EDGAR N-PORT
    if not holdings:
        print("  ALPS page did not yield holdings, trying EDGAR N-PORT...")
        holdings = _fetch_nport_holdings("INDIX", "811-23724")

    return holdings


def _parse_alps_holdings(html):
    """Parse holdings from ALPS fund page."""
    holdings = []

    if BeautifulSoup is not None:
        soup = BeautifulSoup(html, "html.parser")

        # ALPS typically displays holdings in a table
        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            header_cells = []
            name_col = None
            weight_col = None

            for row in rows:
                cells = row.find_all(["td", "th"])
                texts = [c.get_text(strip=True) for c in cells]

                if not header_cells:
                    # Try to identify header row
                    for i, t in enumerate(texts):
                        tl = t.lower()
                        if any(k in tl for k in ("name", "holding", "security", "company")):
                            name_col = i
                        if any(k in tl for k in ("weight", "percent", "% of", "pct", "net assets")):
                            weight_col = i
                    if name_col is not None and weight_col is not None:
                        header_cells = texts
                        continue

                if header_cells and len(texts) > max(name_col or 0, weight_col or 0):
                    name = texts[name_col].strip()
                    weight_str = texts[weight_col].strip()
                    if not name or name.lower() in ("total", "cash", ""):
                        continue
                    try:
                        w = float(weight_str.replace("%", "").replace(",", "").strip())
                        weight = w / 100.0 if w > 1 else w
                        holdings.append({"name": name, "ticker": "", "weight": weight})
                    except (ValueError, TypeError):
                        continue

        if holdings:
            print(f"  Parsed {len(holdings)} holdings from ALPS HTML")
    else:
        # Regex fallback for ALPS
        # Look for JSON data in page (ALPS sometimes embeds holdings as JSON)
        json_pattern = re.compile(r'"holdings"\s*:\s*(\[.*?\])', re.DOTALL)
        match = json_pattern.search(html)
        if match:
            try:
                data = json.loads(match.group(1))
                for item in data:
                    name = item.get("name", item.get("securityName", ""))
                    weight = item.get("weight", item.get("percentOfNetAssets", 0))
                    if isinstance(weight, str):
                        weight = float(weight.replace("%", "")) / 100.0
                    elif weight > 1:
                        weight = weight / 100.0
                    if name:
                        holdings.append({"name": name, "ticker": "", "weight": weight})
                print(f"  Parsed {len(holdings)} holdings from ALPS JSON")
            except (json.JSONDecodeError, ValueError):
                pass

    return holdings


def _fetch_nport_holdings(ticker, series_id):
    """
    Fetch holdings from SEC EDGAR N-PORT filing for a mutual fund.
    Uses EDGAR full-text search to find the latest N-PORT filing.
    """
    holdings = []

    try:
        # Search for latest N-PORT filing for this fund
        search_url = (
            "https://efts.sec.gov/LATEST/search-index?"
            f"q=%22{ticker}%22&forms=N-PORT&dateRange=custom&startdt=2024-01-01"
        )
        # Use EDGAR EFTS search API
        efts_url = (
            f"https://efts.sec.gov/LATEST/search-index?"
            f"q=%22{ticker}%22&forms=NPORT-P"
        )

        # Alternative: use full-text search
        search_api = (
            f"https://efts.sec.gov/LATEST/search-index?"
            f"q=%22{ticker}%22&dateRange=custom&startdt=2024-01-01&forms=NPORT-P"
        )

        # Try the EDGAR full text search
        ft_url = (
            f"https://efts.sec.gov/LATEST/search-index?"
            f"q=%22ALPS+Kotak%22&forms=NPORT-P&dateRange=custom&startdt=2024-01-01"
        )

        # Use the simpler approach: search EDGAR for NPORT filings
        # ALPS Advisors CIK
        alps_cik = "0001409057"
        cik_padded = alps_cik.lstrip("0").zfill(10)
        submissions_url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"

        print(f"  Fetching EDGAR submissions for ALPS Advisors...")
        resp = requests.get(submissions_url, headers=EDGAR_HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        recent = data.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        accessions = recent.get("accessionNumber", [])
        dates = recent.get("filingDate", [])

        # Find latest N-PORT filing
        nport_accession = None
        nport_date = None
        for i, form in enumerate(forms):
            if form in ("NPORT-P", "NPORT-P/A"):
                nport_accession = accessions[i].replace("-", "")
                nport_date = dates[i]
                break

        if not nport_accession:
            print("  No N-PORT filing found for ALPS Advisors")
            return []

        print(f"  Found N-PORT filing dated {nport_date}")
        cik_num = alps_cik.lstrip("0")

        time.sleep(0.2)

        # Get filing index to find the XML
        index_url = f"https://www.sec.gov/Archives/edgar/data/{cik_num}/{nport_accession}/index.json"
        resp = requests.get(index_url, headers=EDGAR_HEADERS, timeout=30)
        resp.raise_for_status()
        index_data = resp.json()

        xml_url = None
        for item in index_data.get("directory", {}).get("item", []):
            name = item.get("name", "").lower()
            if name.endswith(".xml") and "primary" not in name:
                candidate = f"https://www.sec.gov/Archives/edgar/data/{cik_num}/{nport_accession}/{item['name']}"
                xml_url = candidate
                break

        if not xml_url:
            print("  Could not find N-PORT XML in filing")
            return []

        print(f"  Downloading N-PORT XML...")
        time.sleep(0.2)
        resp = requests.get(xml_url, headers=EDGAR_HEADERS, timeout=60)
        resp.raise_for_status()

        save_path = os.path.join(SOURCES_DIR, "fund_kotak_nport.xml")
        with open(save_path, "wb") as f:
            f.write(resp.content)

        holdings = _parse_nport_xml(resp.content, ticker)

    except Exception as e:
        print(f"  Error fetching N-PORT: {e}")

    return holdings


def _parse_nport_xml(xml_content, target_ticker=""):
    """
    Parse N-PORT XML to extract holdings.
    N-PORT filings can contain multiple series; we filter by ticker if possible.
    """
    holdings = []

    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        print(f"  Error parsing N-PORT XML: {e}")
        return []

    # N-PORT uses various namespaces
    # Find all investment entries
    inv_entries = root.findall(".//{*}invstOrSec")

    if not inv_entries:
        print("  No investment entries found in N-PORT XML")
        return []

    total_value = 0
    raw_holdings = []

    for entry in inv_entries:
        name_el = entry.find("{*}name")
        ticker_el = entry.find("{*}ticker")
        val_el = entry.find("{*}valUSD")
        pct_el = entry.find("{*}pctVal")

        name = name_el.text.strip() if name_el is not None and name_el.text else ""
        ticker = ticker_el.text.strip() if ticker_el is not None and ticker_el.text else ""
        value = 0
        pct = 0

        if val_el is not None and val_el.text:
            try:
                value = float(val_el.text)
            except ValueError:
                pass

        if pct_el is not None and pct_el.text:
            try:
                pct = float(pct_el.text)
            except ValueError:
                pass

        if name:
            raw_holdings.append({
                "name": name,
                "ticker": ticker if ticker != "N/A" else "",
                "value": value,
                "weight": pct / 100.0 if pct else 0,
            })
            total_value += value

    # If weights weren't provided, compute from values
    if raw_holdings and all(h["weight"] == 0 for h in raw_holdings) and total_value > 0:
        for h in raw_holdings:
            h["weight"] = h["value"] / total_value

    holdings = [h for h in raw_holdings if h["weight"] > 0]

    if holdings:
        print(f"  Parsed {len(holdings)} holdings from N-PORT XML")

    return holdings


# ---------------------------------------------------------------------------
# Arrowstreet Global 130-30 (manual stub)
# ---------------------------------------------------------------------------

def stub_arrowstreet():
    """
    Arrowstreet Global 130-30 is a separate account, not a publicly traded fund.
    Holdings data previously came from a Morgan Stanley PDF report.
    No publicly scrapeable source is available.
    """
    print("  MANUAL: Arrowstreet Global 130-30 requires manual data entry")
    print("  Previous source: Morgan Stanley PDF report")
    print("  URL: https://mim.fgsfulfillment.com/download.aspx?sku=PRRP-AGEF-ANZ")
    print("  Skipping -- no automated source available")
    return []


# ---------------------------------------------------------------------------
# Earnest Partners Small Cap Value (manual stub)
# ---------------------------------------------------------------------------

def stub_earnest_partners():
    """
    Earnest Partners Small Cap Value is managed via a separate account.
    Holdings data previously came from a Morgan Stanley PDF report.
    No publicly scrapeable source is available.
    """
    print("  MANUAL: Earnest Partners Small Cap Value requires manual data entry")
    print("  Previous source: Morgan Stanley PDF report")
    print("  URL: https://www.morganstanley.com/content/dam/msdotcom/en/wealth-investmentsolutions/pdfs/uma/epl-s.pdf")
    print("  Skipping -- no automated source available")
    return []


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

FUND_CONFIGS = {
    "ariel_small_cap": {
        "display_name": "ARIEL US SMALL CAP",
        "internal_name": "ARIEL US SMALL CAP",
        "source_key": "ariel_small_cap",
        "scraper": scrape_ariel_small_cap,
        "restricted": "n",
        "note": "",
    },
    "kotak_india_growth": {
        "display_name": "KOTAK INDIA GROWTH",
        "internal_name": "ALPS | Kotak India ESG Fund",
        "source_key": "kotak_india_growth",
        "scraper": scrape_kotak_india_growth,
        "restricted": "n",
        "note": "No specific fund manager is listed, but this is our best guess as to who it is.",
    },
    "arrowstreet_130_30": {
        "display_name": "ARROWSTREET GLOBAL 130-30",
        "internal_name": "Arrowstreet Global Equity Fund",
        "source_key": None,
        "scraper": lambda url: stub_arrowstreet(),
        "restricted": "Y",
        "note": "Separate account -- requires manual data from Morgan Stanley PDF",
    },
    "earnest_partners_scv": {
        "display_name": "EARNEST PARTNERS SMALL CAP VALUE",
        "internal_name": "Earnest Partners SC Value (EPL-S)",
        "source_key": None,
        "scraper": lambda url: stub_earnest_partners(),
        "restricted": "y",
        "note": "Separate account -- requires manual data from Morgan Stanley PDF",
    },
}


def main():
    os.makedirs(SOURCES_DIR, exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    with open(SOURCES_PATH) as f:
        sources = json.load(f)

    fund_urls = sources.get("fund_websites", {})
    manual_sources = sources.get("fund_manual", {})

    print("=== Fund Holdings Scraper ===\n")

    for fund_key, config in FUND_CONFIGS.items():
        print(f"\nProcessing: {config['display_name']}")

        # Get URL from sources.json
        source_key = config["source_key"]
        url = fund_urls.get(source_key, "") if source_key else ""
        manual_url = manual_sources.get(fund_key, "") if not url else ""

        # Run the scraper
        holdings = config["scraper"](url or manual_url)

        if holdings:
            output_path = os.path.join(OUTPUTS_DIR, f"fund_{fund_key}.csv")
            source_url = url or manual_url or "manual"
            write_fund_csv(
                holdings,
                output_path,
                fund_name=config["display_name"],
                internal_name=config["internal_name"],
                source_url=source_url,
                filing_date="",
                note=config["note"],
                restricted=config["restricted"],
            )

            # Preview top 5
            sorted_h = sorted(holdings, key=lambda x: x.get("weight", 0), reverse=True)
            for h in sorted_h[:5]:
                print(f"    {h['name']:40s} {h['weight']:8.4%}")
        else:
            print(f"  No holdings scraped for {config['display_name']}")

    print("\nDone!")


if __name__ == "__main__":
    main()
