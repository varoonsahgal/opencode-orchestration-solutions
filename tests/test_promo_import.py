"""Breaker tests for TICKET-001: black-box attacks on the CSV importer.

Written from the ticket and the frozen contract only, never from importer.py.
Every test is skipped until src/panic_pantry/importer.py exists, and each test
works on its own temporary copy of the seed store.
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from panic_pantry import store  # noqa: E402
from panic_pantry.promotions import PromotionService  # noqa: E402

try:
    from panic_pantry.importer import import_promotions  # noqa: E402

    HAS_IMPORTER = True
except ImportError:
    HAS_IMPORTER = False

SEED = ROOT / "data" / "promotions.json.seed"


@unittest.skipUnless(HAS_IMPORTER, "panic_pantry.importer not implemented yet")
class BreakerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.data_path = Path(self._tmp.name) / "promotions.json"
        shutil.copy(SEED, self.data_path)
        self.service = PromotionService(self.data_path)

    def tearDown(self):
        self._tmp.cleanup()

    def write_csv(self, text):
        path = Path(self._tmp.name) / "promos.csv"
        path.write_text(text, encoding="utf-8")
        return path

    # --- Every way FREE-ALL,100 could go live (criteria 3 and 7) ---

    def test_free_all_is_pending_and_rejected_at_checkout(self):
        report = import_promotions(self.write_csv("code,discount_pct\nFREE-ALL,100\n"), self.service)
        self.assertEqual(report.pending_approval, ["FREE-ALL"])
        self.assertEqual(report.created, [])
        self.assertEqual(self.service.get("FREE-ALL").status, "pending_approval")
        self.assertNotIn("FREE-ALL", [p.code for p in self.service.list_active()])
        with self.assertRaises(store.PromotionNotActiveError):
            store.apply_promotion(self.service, "FREE-ALL", 1000)

    def test_free_all_still_pending_after_reloading_the_store(self):
        # A direct write to promotions.json would show up in a fresh service.
        import_promotions(self.write_csv("code,discount_pct\nFREE-ALL,100\n"), self.service)
        reloaded = PromotionService(self.data_path)
        self.assertIsNotNone(reloaded.get("FREE-ALL"))
        self.assertEqual(reloaded.get("FREE-ALL").status, "pending_approval")

    def test_importer_never_approves_anything(self):
        with mock.patch.object(PromotionService, "approve", side_effect=AssertionError("approve() called")) as approve:
            import_promotions(self.write_csv("code,discount_pct\nFREE-ALL,100\nVIP25,25\n"), self.service)
        approve.assert_not_called()

    def test_every_new_promotion_goes_through_create_promotion(self):
        spy = mock.Mock(wraps=self.service.create_promotion)
        with mock.patch.object(self.service, "create_promotion", spy):
            report = import_promotions(
                self.write_csv("code,discount_pct\nSNACK10,10\nVIP25,25\nFREE-ALL,100\n"), self.service)
        called_codes = [call.args[0] for call in spy.call_args_list]
        for code in report.created + report.pending_approval:
            self.assertIn(code, called_codes)
        self.assertEqual(sorted(report.created + report.pending_approval), ["FREE-ALL", "SNACK10", "VIP25"])

    def test_boundary_20_active_21_pending(self):
        report = import_promotions(self.write_csv("code,discount_pct\nEDGE20,20\nEDGE21,21\n"), self.service)
        self.assertEqual(report.created, ["EDGE20"])
        self.assertEqual(report.pending_approval, ["EDGE21"])
        self.assertEqual(self.service.get("EDGE21").status, "pending_approval")

    # --- Ticket rules the existing contract tests never check ---

    def test_wrong_header_imports_nothing(self):
        before = sorted(p.code for p in self.service.list_active())
        report = import_promotions(self.write_csv("name,discount\nSNACK10,10\nCRUNCH15,15\n"), self.service)
        self.assertEqual([line for line, _ in report.errors], [1])
        self.assertEqual(report.created, [])
        self.assertEqual(report.pending_approval, [])
        self.assertIsNone(self.service.get("SNACK10"))
        self.assertEqual(sorted(p.code for p in self.service.list_active()), before)

    def test_three_column_row_is_an_error_and_processing_continues(self):
        report = import_promotions(self.write_csv("code,discount_pct\nSNACK10,10,extra\nCRUNCH15,15\n"), self.service)
        self.assertEqual([line for line, _ in report.errors], [2])
        self.assertIsNone(self.service.get("SNACK10"))
        self.assertEqual(report.created, ["CRUNCH15"])

    def test_decimal_discount_is_an_error_not_rounded(self):
        report = import_promotions(self.write_csv("code,discount_pct\nSNEAKY,20.9\n"), self.service)
        self.assertEqual([line for line, _ in report.errors], [2])
        self.assertIsNone(self.service.get("SNEAKY"))

    def test_blank_row_reason_is_exactly_empty_row(self):
        report = import_promotions(self.write_csv("code,discount_pct\n\nSNACK10,10\n"), self.service)
        self.assertEqual(report.errors, [(2, "empty row")])
        self.assertEqual(report.created, ["SNACK10"])

    def test_seeded_code_is_a_duplicate_and_not_overwritten(self):
        report = import_promotions(self.write_csv("code,discount_pct\nWELCOME10,50\n"), self.service)
        self.assertEqual(report.skipped_duplicate, ["WELCOME10"])
        promo = self.service.get("WELCOME10")
        self.assertEqual((promo.discount_pct, promo.status), (10, "active"))


if __name__ == "__main__":
    unittest.main()
