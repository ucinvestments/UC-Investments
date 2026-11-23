from io import BytesIO
from pathlib import Path
import unittest

from openpyxl import Workbook

from Finance.scrapers.etf_holdings import read_ssga_xlsx
from Finance.scrapers.sec_13f_parser import fetch_latest_filing


class ExampleResponse:
    def __init__(self, data=None, content=b""):
        self.data = data
        self.content = content

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


class ExampleEdgar:
    def get(self, url, **_):
        latest = "0001234567-26-000002"
        if url.endswith(".json") and "/submissions/" in url:
            return ExampleResponse({"filings": {"recent": {
                "form": ["13F-HR/A", "13F-HR"],
                "reportDate": ["2026-03-31", "2026-06-30"],
                "filingDate": ["2026-09-10", "2026-08-14"],
                "accessionNumber": ["0001234567-26-000003", latest],
                "primaryDocument": ["primary.xml", "primary.xml"],
            }}})
        if latest.replace("-", "") not in url:
            raise AssertionError(f"Fetched the older report period: {url}")
        match Path(url).name:
            case "primary.xml":
                return ExampleResponse(content=b"""
                    <edgarSubmission><periodOfReport>06-30-2026</periodOfReport>
                      <tableEntryTotal>1</tableEntryTotal><tableValueTotal>12345</tableValueTotal>
                    </edgarSubmission>
                """)
            case "index.json":
                return ExampleResponse({"directory": {"item": [{"name": "table.xml"}]}})
            case "table.xml":
                return ExampleResponse(content=b"""
                    <informationTable><infoTable><nameOfIssuer>Example Inc</nameOfIssuer>
                      <titleOfClass>COM</titleOfClass><cusip>123456789</cusip><value>12345</value>
                    </infoTable></informationTable>
                """)
        raise AssertionError(url)


class DisclosureSourcesTest(unittest.TestCase):
    def test_latest_reporting_period_wins_over_newer_amendment_to_older_quarter(self):
        filing, positions = fetch_latest_filing(ExampleEdgar(), "1234567")
        self.assertEqual(filing["date"], "2026-06-30")
        self.assertEqual(positions[0]["value"], 12_345)

    def test_spdr_exports_use_percentage_points_both_above_and_below_one(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(("Holdings:", "As of 15-Jun-2026"))
        sheet.append(("Name", "Ticker", "Identifier", "Weight"))
        sheet.append(("Example One", "ONE", "123456789", 2))
        sheet.append(("Example Two", "TWO", "123456700", 0.5))
        sheet.append(("INDEX FUT JUN26", "FUT", "123456701", -0.001))
        content = BytesIO()
        workbook.save(content)
        workbook.close()

        date, positions = read_ssga_xlsx(content.getvalue())
        self.assertEqual(date, "2026-06-15")
        self.assertEqual([row["weight"] for row in positions], [0.02, 0.005])
