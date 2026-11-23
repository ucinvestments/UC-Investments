"""Build and publish a validated, dated snapshot for UC Investment Explorer."""

from collections import defaultdict
from datetime import datetime, timezone
import fcntl
import json
import math
import os
from pathlib import Path
import re
import tempfile

import requests

from scrapers.aggregator import normalize_name
from scrapers.etf_holdings import fetch_etf, read_ssga_xlsx
from scrapers.private_markets import enrich_funds
from scrapers.sec_13f_parser import fetch_latest_filing
from scrapers.uc_pdf_parser import fetch_disclosure

FINANCE_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT = FINANCE_DIR.parent / "Webapp/static/data/holdings-snapshot.json"
US_EXCHANGES = {"NASDAQ", "NYSE", "NYSE ARCA", "NYSE AMERICAN", "CBOE BZX"}
PROXIES = {
    "ishares_acwi": {
        "name": "iShares MSCI ACWI ETF",
        "funds": ("MSCI ACWI IMI TF EX-TOB AND FF", "MSCI ACWI IMI EX-TOB AND FF"),
        "method": "ETF proxy",
    },
    "spdr_spyx": {
        "name": "State Street SPDR S&P 500 Fossil Fuel Reserves Free ETF",
        "funds": ("SSGA S&P 500 EX-TOB UCRP", "SSGA S&P 500 EX-TOB AND FF"),
        "method": "ETF proxy",
    },
    "adage_capital": {
        "name": "Adage Capital Partners Form 13F",
        "funds": ("ADAGE CAPITAL",),
        "method": "Manager 13F estimate",
    },
}


def listed_funds(reports):
    categories = {}
    funds = defaultdict(dict)
    for pool, holdings in reports.items():
        for row in holdings:
            key = (row["name"].upper(), row["type"])
            categories[key] = row["name"]
            funds[key][pool] = funds[key].get(pool, 0) + row["amount"]

    result = [
        {
            "name": categories[key], "category": key[1], "amount": float(sum(values.values())),
            "allocations": [{"name": pool, "amount": float(amount)} for pool, amount in values.items()],
        }
        for key, values in funds.items()
    ]
    return sorted(result, key=lambda row: -row["amount"])


def asset_classes(funds):
    groups = defaultdict(list)
    for fund in funds:
        groups[fund["category"]].append(fund)
    return sorted((
        {
            "name": name, "amount": math.fsum(fund["amount"] for fund in group),
            "allocations": [], "funds": [fund["name"] for fund in group],
        }
        for name, group in groups.items()
    ), key=lambda row: -row["amount"])


def proxy_inputs(session, config, used_proxies):
    sources = {}
    weights = {}
    for key in sorted(used_proxies - {"adage_capital"}):
        url = config["etf_holdings"][key]
        date, weights[key] = fetch_etf(session, url)
        sources[key] = {"date": date, "url": url}

    by_ticker = {row["ticker"]: row["name"] for row in weights.get("spdr_spyx", [])}
    by_cusip = {row["cusip"]: row["name"] for row in weights.get("spdr_spyx", [])}
    for row in weights.get("ishares_acwi", []):
        if row["exchange"].upper() in US_EXCHANGES:
            row["name"] = by_ticker.get(row["ticker"], row["name"])

    if "adage_capital" in used_proxies:
        manager = config["whale_wisdom_13f"]["adage_capital"]
        sources["adage_capital"], filing = fetch_latest_filing(session, manager["cik"])
        total = sum(row["value"] for row in filing)
        weights["adage_capital"] = [
            {
                "name": by_cusip.get(row["cusip"], share_class_name(row)),
                "weight": row["value"] / total,
            }
            for row in filing
            if not row.get("option") and row.get("share_type") == "SH"
            and re.search(r"\b(COM|COMMON|ORD|ORDINARY|SHS|SHARES|ADR|ADS|CL|CLASS)\b", row["title_of_class"])
            and not row["title_of_class"].startswith("*W")
        ]

    for key, rows in weights.items():
        share = math.fsum(row["weight"] for row in rows)
        if not 0.5 <= share <= 1.005 or any(row["weight"] < 0 for row in rows):
            raise ValueError(f"{key} returned implausible equity weights ({share:.2%})")
        sources[key].update(name=PROXIES[key]["name"], method=PROXIES[key]["method"])
    return weights, sources


def share_class_name(row):
    name = row["name"]
    share_class = re.search(r"\b(?:CL|CLASS) ([A-Z])\b", row["title_of_class"])
    if share_class and not re.search(r"\b(?:CL|CLASS) [A-Z]\b", name):
        return f"{name} Class {share_class[1]}"
    return name


def company_estimates(funds, weights, consolidate):
    companies = defaultdict(lambda: defaultdict(float))
    for fund, source in funds:
        for row in weights[source]:
            if row["weight"] > 0:
                company = normalize_name(row["name"], consolidate_voting_shares=consolidate)
                companies[company][fund["name"], source] += fund["amount"] * row["weight"]
    return sorted((
        {
            "name": name, "amount": math.fsum(parts.values()), "basis": "estimate",
            "allocations": [
                {"name": fund, "source": source, "amount": amount}
                for (fund, source), amount in sorted(parts.items(), key=lambda item: -item[1])
            ],
        }
        for name, parts in companies.items()
    ), key=lambda row: (-row["amount"], row["name"]))


def regents_positions(session, regents, securities, etfs):
    reported = []
    for security in securities:
        row = {
            "name": security["name"], "amount": security["value"], "basis": "reported",
            "category": " · ".join(filter(None, (
                security["title_of_class"], security.get("option"), security["cusip"],
            ))),
            "allocations": [],
        }
        if security["cusip"] in etfs and not security.get("option"):
            etf = etfs[security["cusip"]]
            response = session.get(etf["url"], timeout=45)
            response.raise_for_status()
            date, holdings = read_ssga_xlsx(response.content, expected_ticker=etf["ticker"])
            row["name"] = f"{etf['ticker']} · {etf['name']}"
            row["lookThrough"] = {**etf, "date": date}
            if date == regents["date"]:
                share = math.fsum(holding["weight"] for holding in holdings)
                if not 0 < share <= 1.005 or any(holding["weight"] < 0 for holding in holdings):
                    raise ValueError(f"{etf['ticker']} returned implausible equity weights ({share:.2%})")
                row["lookThrough"]["estimates"] = [
                    {
                        "name": holding["name"], "ticker": holding["ticker"],
                        "amount": security["value"] * holding["weight"],
                    }
                    for holding in sorted(holdings, key=lambda holding: -holding["weight"])
                    if holding["weight"] > 0
                ]
        reported.append(row)
    return sorted(reported, key=lambda row: (-row["amount"], row["name"]))


def build_snapshot(session, config):
    checked_at = datetime.now(timezone.utc).isoformat(timespec="microseconds")
    reports = {}
    sources = {}
    for pool, url in config["uc_policy_pages"].items():
        date, document, holdings = fetch_disclosure(session, pool, url)
        reports[pool.upper()] = holdings
        sources[pool] = {
            "name": pool.upper(), "date": date, "url": document,
            "amount": float(sum(holding["amount"] for holding in holdings)),
        }

    funds = listed_funds(reports)
    regents, securities = fetch_latest_filing(session, config["regents_cik"])
    reported = regents_positions(session, regents, securities, config["regents_etfs"])
    private_markets = enrich_funds(session, config["private_markets"], funds)
    regents.update(name="UC Regents Form 13F")

    fund_sources = {fund: key for key, proxy in PROXIES.items() for fund in proxy["funds"]}
    matched = [
        (fund, fund_sources[fund["name"].upper()])
        for fund in funds
        if fund["name"].upper() in fund_sources and fund["category"] == "PUBLIC EQUITY" and fund["amount"] > 0
    ]
    weights, proxies = proxy_inputs(session, config, {key for _, key in matched})
    grouped = company_estimates(matched, weights, True)
    separate = company_estimates(matched, weights, False)
    total = math.fsum(fund["amount"] for fund in funds)
    assigned = math.fsum(row["amount"] for row in grouped)
    if not 0 <= assigned <= total or not math.isclose(assigned, math.fsum(row["amount"] for row in separate)):
        raise ValueError("Company estimates do not reconcile across share-class views")

    return {
        "schemaVersion": 1, "checkedAt": checked_at,
        "disclosures": sources, "proxies": proxies, "regents": regents, "privateMarkets": private_markets,
        "coverage": {"total": total, "assigned": assigned},
        "funds": funds, "assetClasses": asset_classes(funds),
        "companies": {"grouped": grouped, "separate": separate}, "reported": reported,
    }


def publish(snapshot, output):
    output.parent.mkdir(parents=True, exist_ok=True)
    directory = os.open(output.parent, os.O_RDONLY)
    try:
        fcntl.flock(directory, fcntl.LOCK_EX)
        if output.exists():
            previous = json.loads(output.read_text())
            if snapshot["checkedAt"] < previous["checkedAt"]:
                raise ValueError("A newer refresh was already published")
            groups = ("disclosures", "proxies", "privateMarkets")
            for group in groups:
                for key, source in snapshot.get(group, {}).items():
                    if key in previous.get(group, {}) and source["date"] < previous[group][key]["date"]:
                        raise ValueError(f"{key} reported an older source date than the current snapshot")
            if snapshot["regents"]["date"] < previous["regents"]["date"]:
                raise ValueError("The Regents filing period went backwards")
            if snapshot["regents"]["filed"] < previous["regents"]["filed"] and (
                snapshot["regents"]["date"] == previous["regents"]["date"]
            ):
                raise ValueError("The Regents filing was superseded")

        # A failed download, parse, or write leaves the prior public snapshot intact.
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent, delete=False) as stream:
                temporary = Path(stream.name)
                json.dump(snapshot, stream, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
                stream.write("\n")
                os.fchmod(stream.fileno(), 0o644)
                stream.flush()
                os.fsync(stream.fileno())
            temporary.replace(output)
        finally:
            if temporary:
                temporary.unlink(missing_ok=True)
    finally:
        os.close(directory)


def refresh(output):
    config = json.loads((FINANCE_DIR / "sources.json").read_text())
    with requests.Session() as session:
        snapshot = build_snapshot(session, config)
    publish(snapshot, output)
    print(f"Published {output} with UCRP and GEP disclosures, Regents 13F and dated proxy sources.")
    for source in (*snapshot["disclosures"].values(), snapshot["regents"], *snapshot["proxies"].values(), *snapshot["privateMarkets"].values()):
        print(f"  {source['name']}: {source['date']}")
