"""
Unit tests for TindaWise Deterministic Ledger, Owner-Editable Price List,
Human-in-the-Loop Confirmation, Tap Fallback, and RA 10173 Privacy Guarantees.
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from decimal import Decimal

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "backend"),
)
from ledger_engine import TindaWiseEngine


class TestTindaWiseLedgerEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_tindawise.db")
        self.engine = TindaWiseEngine(db_path=self.db_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_price_list_never_guessed_by_model(self) -> None:
        """
        Even if a spoken utterance mentions a wrong peso amount, extraction ignores it
        and strictly uses the owner-editable price list.
        """
        # Default Lucky Me Pancit Canton is 16.00, Sardinas is 26.00 -> 2*16 + 1*26 = 58.00
        preview = self.engine.extract_utang_preview(
            transcript_text="Palista kay Aling Nena dalawang Lucky Me canton saka isang sardinas, sa Sabado bayad.",
            prefer_cloud_api=False,
        )
        self.assertEqual(preview.debtor_name, "Aling Nena")
        self.assertEqual(preview.computed_total, "58.00")
        self.assertTrue(preview.requires_owner_confirmation)

        # Now owner edits price of Pancit Canton from 16.00 to 18.50
        self.engine.upsert_price_item(
            sku_id="SKU-CANTON",
            canonical_name="Lucky Me Pancit Canton",
            unit="pack",
            unit_price="18.50",
            aliases=["pancit canton", "lucky me canton", "canton"],
        )
        preview_after = self.engine.extract_utang_preview(
            transcript_text="Palista kay Aling Nena dalawang Lucky Me canton saka isang sardinas, sa Sabado bayad.",
            prefer_cloud_api=False,
        )
        # 2 * 18.50 + 1 * 26.00 = 63.00
        self.assertEqual(preview_after.computed_total, "63.00")

    def test_unconfirmed_preview_never_mutates_ledger(self) -> None:
        """Extracting a preview must NEVER create or change debtor balances before owner confirmation."""
        _ = self.engine.extract_utang_preview(
            transcript_text="Pautang daw si Kuya Jojo ng kalahating kilong bigas at dalawang itlog, bukas babayaran.",
            prefer_cloud_api=False,
        )
        debtors = self.engine.get_debtors_summary()
        self.assertEqual(len(debtors), 0)

        # Attempting to call confirm_and_record_utang with owner_confirmed=False must raise ValueError
        with self.assertRaises(ValueError):
            self.engine.confirm_and_record_utang(
                debtor_name="Kuya Jojo",
                items=[{"sku_id": "SKU-BIGAS-KG", "item_name": "Bigas", "quantity": "0.5"}],
                owner_confirmed=False,
            )

    def test_owner_correction_flow_and_deterministic_balance(self) -> None:
        """
        Simulates a noisy counter mishear ('3 sardinas' instead of '2 sardinas'),
        owner corrects quantity to 2 on the confirmation card, and commits.
        """
        preview = self.engine.extract_utang_preview(
            transcript_text="Palista kay Kuya Dante tatlong sardinas saka isang kilong bigas, sa Sabado bayad.",
            prefer_cloud_api=False,
        )
        # Raw extraction heard 3 sardinas (3*26 = 78) + 1kg bigas (54) = 132.00
        self.assertEqual(preview.computed_total, "132.00")

        # Owner corrects Sardinas quantity from 3 to 2 before confirming
        corrected_items = [
            {"sku_id": "SKU-SARDINAS", "item_name": "Sardinas", "quantity": "2"},
            {"sku_id": "SKU-BIGAS-KG", "item_name": "Bigas", "quantity": "1"},
        ]
        committed = self.engine.confirm_and_record_utang(
            debtor_name=preview.debtor_name,
            items=corrected_items,
            owner_confirmed=True,
            source_mode="voice_confirmed",
            raw_transcript=preview.transcript,
            due_date_raw=preview.due_date_raw,
            was_corrected=True,
        )
        # 2 * 26.00 + 1 * 54.00 = 106.00
        self.assertEqual(committed["entry_total"], "106.00")
        self.assertEqual(committed["new_running_balance"], "106.00")
        self.assertTrue(committed["was_corrected"])

    def test_tap_fallback_and_partial_payment(self) -> None:
        """Verifies the zero-voice Tap Fallback mode and subsequent partial payment math."""
        res = self.engine.confirm_and_record_utang(
            debtor_name="Ate Marites",
            items=[
                {"sku_id": "SKU-COKE-LITRO", "item_name": "Coke 1 Litro", "quantity": "1"},
                {"sku_id": "SKU-CORNED-BEEF", "item_name": "Corned Beef", "quantity": "1"},
            ],
            owner_confirmed=True,
            source_mode="tap_fallback",
            due_date_raw="Sa Kinsenas",
        )
        # 45.00 + 38.00 = 83.00
        self.assertEqual(res["new_running_balance"], "83.00")

        pay_res = self.engine.record_payment(debtor_id=res["debtor_id"], amount_paid="50.00")
        self.assertEqual(pay_res["new_running_balance"], "33.00")

    def test_manual_reminder_drafter_and_ephemeral_audio_privacy(self) -> None:
        """Verifies RA 10173 0-day audio retention audit and manual-only SMS reminder generation."""
        fake_audio = b"RIFF_SIMULATED_PCM_AUDIO_BYTES"
        preview = self.engine.extract_utang_preview(
            transcript_text="Palista kay Aling Nena isang Safeguard, bukas bayad.",
            audio_bytes=fake_audio,
            prefer_cloud_api=False,
        )
        self.assertFalse(preview.privacy_audit["audio_retained_on_disk"])
        self.assertEqual(preview.privacy_audit["audio_retention_days"], 0)

        committed = self.engine.confirm_and_record_utang(
            debtor_name="Aling Nena",
            items=[{"sku_id": "SKU-SAFEGUARD", "item_name": "Safeguard", "quantity": "1"}],
            owner_confirmed=True,
            due_date_raw="Bukas",
            contact_note="09171234567",
        )
        reminder = self.engine.draft_manual_reminder(debtor_id=committed["debtor_id"])
        self.assertEqual(reminder["delivery_mode"], "manual_owner_send_only")
        self.assertIn("PHP 24.00", reminder["message_text"])
        self.assertTrue(reminder["sms_uri"].startswith("sms:09171234567?body="))


if __name__ == "__main__":
    unittest.main()
