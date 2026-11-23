"""Tests: missing external payment confirmation never becomes 'earnings'."""
import unittest
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location(
    "gate", Path(__file__).resolve().parent / "agent_outcome_guard.py"
)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class GateTests(unittest.TestCase):
    def test_no_bank_proof_means_zero(self):
        r = gate.evaluate([{"id":"sale1","kind":"paid_sale",
                            "payment_reference":"T123","gross_eur":250,
                            "expenses_eur":40}])
        self.assertEqual(r["bank_row_matched_gross_eur"], 0)
        self.assertEqual(r["events"][0]["status"], "UNCONFIRMED_NO_REVENUE_COUNTED")

    def test_exact_unique_bank_match(self):
        e = [{"id":"s1","kind":"paid_sale","payment_reference":"T123",
              "gross_eur":250,"expenses_eur":40}]
        t = [{"reference":"T123","amount_eur":250,"received":True}]
        r=gate.evaluate(e,t)
        self.assertEqual(r["bank_row_matched_net_after_recorded_expenses_eur"],210)

    def test_duplicate_bank_ref_not_accepted(self):
        e = [{"id":"s1","kind":"paid_sale","payment_reference":"T123",
              "gross_eur":250,"expenses_eur":40}]
        t = [{"reference":"T123","amount_eur":250,"received":True}] * 2
        self.assertEqual(gate.evaluate(e,t)["bank_row_matched_gross_eur"],0)

    def test_listing_url_not_assumed_live(self):
        r=gate.evaluate([{"id":"a","kind":"published_listing",
                         "public_url":"https://example.com/ad"}])
        self.assertEqual(r["events"][0]["status"],"EVIDENCE_ONLY_NOT_LIVE_VERIFIED")

    def test_video_missing_rejected(self):
        r=gate.evaluate([{"id":"v","kind":"media_file",
                         "local_path":"/nonexistent/file.mp4"}])
        self.assertEqual(r["events"][0]["status"],"REJECTED")

    def test_duplicate_event_id_rejected(self):
        e=[{"id":"same","kind":"buyer_lead"},{"id":"same","kind":"buyer_lead"}]
        self.assertEqual(gate.evaluate(e)["events"][-1]["reason"],"missing_or_duplicate_id")


if __name__=="__main__":
    unittest.main()
