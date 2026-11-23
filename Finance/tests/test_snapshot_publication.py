from io import BytesIO
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

from openpyxl import Workbook

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from snapshot import publish, regents_positions


def snapshot(date="2026-06-30", amount=100):
    return {
        "checkedAt": "2026-10-20T12:00:00+00:00",
        "disclosures": {"ucrp": {"date": date, "amount": amount}},
        "proxies": {},
        "regents": {"date": date, "filed": "2026-08-14"},
    }


class SnapshotPublicationTest(unittest.TestCase):
    def test_rejected_refresh_keeps_last_complete_snapshot(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "holdings.json"
            publish(snapshot(), output)
            prior = output.read_bytes()

            for candidate in (snapshot(date="2025-06-30"), snapshot(amount=float("nan"))):
                with self.subTest(candidate=candidate):
                    with self.assertRaises(ValueError):
                        publish(candidate, output)
                    self.assertEqual(output.read_bytes(), prior)
                    self.assertEqual(list(Path(directory).iterdir()), [output])

            publish(snapshot(amount=125), output)
            self.assertEqual(json.loads(output.read_bytes())["disclosures"]["ucrp"]["amount"], 125)

class RegentsEtfTest(unittest.TestCase):
    def test_enriches_the_exact_position_with_only_period_matched_estimates(self):
        regents = {"date": "2026-09-30"}
        source = {"ticker": "EXMP", "name": "Example ETF", "url": "https://example.test/exmp.xlsx"}
        security = {
            "cusip": "123456789", "name": "ETF", "value": 1200, "title_of_class": "ETF",
        }
        other = {**security, "cusip": "987654321"}

        for workbook_date, estimates in (("19-Nov-2026", []), ("30-Sep-2026", [120])):
            with self.subTest(workbook_date=workbook_date):
                workbook = Workbook()
                sheet = workbook.active
                sheet.append(("Ticker Symbol:", "EXMP"))
                sheet.append(("Holdings:", f"As of {workbook_date}"))
                sheet.append(("Name", "Ticker", "Identifier", "Weight", "Maturity"))
                sheet.append(("Example Stock", "STK", "123412341", 10, "-"))
                sheet.append(("Example Bond", "BND", "343434343", 90, "12/31/2030"))
                content = BytesIO()
                workbook.save(content)
                workbook.close()

                class Session:
                    def get(self, url, **_):
                        if url != source["url"]:
                            raise AssertionError(url)
                        return self

                    def raise_for_status(self):
                        pass

                session = Session()
                session.content = content.getvalue()
                positions = regents_positions(session, regents, [security, other], {security["cusip"]: source})
                target = next(row for row in positions if "lookThrough" in row)
                self.assertEqual(target["amount"], 1200)
                self.assertEqual(sum(row["amount"] for row in positions), 2400)
                self.assertEqual(
                    [row["amount"] for row in target["lookThrough"].get("estimates", [])],
                    estimates,
                )
