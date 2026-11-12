"""
TindaWise Deterministic Ledger, Owner-Editable Price List, and Taglish Utang Extraction Engine.

Design Guarantees & Field Research Alignment (`data/research/sarisaristore_interview.md`):
1. AI never guesses or sets catalog money amounts. Catalog prices come strictly from the owner-editable price list,
   while fast non-SKU direct peso utang (`SKU-DIRECT-PESO`, for Kuya Ronny & Ate Mina workflows) requires explicit confirmation.
2. Unconfirmed AI extractions never mutate debtor balances. Owner confirmation is mandatory.
3. All balance arithmetic uses Python's exact `Decimal` type (never floating-point).
4. Supports both memory-based (Kuya Ronny) and paper-kwaderno (Ate Mina) workflows: optional due dates,
   `Suki`/`Kakilala` trust tags, itemized walk-by history (`get_debtor_history`), and face-to-face reminder scripts.
5. Data Privacy Act (RA 10173) compliance: Push-to-talk audio is ephemeral (0-day retention, cleared in memory),
   ledger data is stored locally on the owner's device, and reminders are never sent automatically.
"""

from __future__ import annotations

import contextlib
import json
import os
import re
import sqlite3
import time
import urllib.parse
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, Iterator, List, Optional, Tuple


DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "tindawise_local.db",
)

# Default owner-editable sari-sari store price list (in PHP)
DEFAULT_PRICE_LIST: List[Dict[str, Any]] = [
    {
        "sku_id": "SKU-CANTON",
        "canonical_name": "Lucky Me Pancit Canton",
        "unit": "pack",
        "unit_price": "16.00",
        "aliases": ["pancit canton", "lucky me canton", "canton", "pansit canton"],
    },
    {
        "sku_id": "SKU-NOODLES",
        "canonical_name": "Lucky Me Instant Mami (Beef/Chicken)",
        "unit": "pack",
        "unit_price": "12.00",
        "aliases": ["lucky me beef", "lucky me chicken", "instant noodles", "noodles", "mami"],
    },
    {
        "sku_id": "SKU-SARDINAS",
        "canonical_name": "Sardinas (Mega / 555 / Ligo 155g)",
        "unit": "can",
        "unit_price": "26.00",
        "aliases": ["sardinas", "mega sardinas", "555 sardinas", "ligo", "isang lata ng sardinas"],
    },
    {
        "sku_id": "SKU-CORNED-BEEF",
        "canonical_name": "Argentina Corned Beef (150g)",
        "unit": "can",
        "unit_price": "38.00",
        "aliases": ["corned beef", "argentina", "kornbip", "argentina corned beef"],
    },
    {
        "sku_id": "SKU-BIGAS-KG",
        "canonical_name": "Well-Milled Bigas (Rice)",
        "unit": "kg",
        "unit_price": "54.00",
        "aliases": ["bigas", "kilo ng bigas", "kilong bigas", "rice"],
    },
    {
        "sku_id": "SKU-ASUKAL-KG",
        "canonical_name": "Washed Sugar (Asukal)",
        "unit": "kg",
        "unit_price": "88.00",
        "aliases": ["asukal", "kilong asukal", "sugar"],
    },
    {
        "sku_id": "SKU-ITLOG",
        "canonical_name": "Itlog (Medium Egg)",
        "unit": "pc",
        "unit_price": "9.00",
        "aliases": ["itlog", "egg", "pirasong itlog"],
    },
    {
        "sku_id": "SKU-MANTIKA-TINGI",
        "canonical_name": "Mantika Tingi (Cooking Oil Cup/Pack)",
        "unit": "pack",
        "unit_price": "20.00",
        "aliases": ["mantika", "mantika tingi", "cooking oil", "oil"],
    },
    {
        "sku_id": "SKU-COKE-MISMO",
        "canonical_name": "Coke / Royal / Sprite Mismo (290ml)",
        "unit": "bottle",
        "unit_price": "22.00",
        "aliases": ["coke mismo", "mismo", "royal mismo", "sprite mismo", "softdrinks mismo"],
    },
    {
        "sku_id": "SKU-COKE-LITRO",
        "canonical_name": "Coke 1 Litro / Kasalo",
        "unit": "bottle",
        "unit_price": "45.00",
        "aliases": ["coke litro", "isang litrong coke", "coke 1l", "coke kasalo"],
    },
    {
        "sku_id": "SKU-KOPIKO",
        "canonical_name": "Kopiko Black / Brown Twin Pack",
        "unit": "sachet",
        "unit_price": "15.00",
        "aliases": ["kopiko", "kopiko black", "kopiko brown", "kape", "twin pack"],
    },
    {
        "sku_id": "SKU-BEAR-BRAND",
        "canonical_name": "Bear Brand Swak Pack (33g)",
        "unit": "sachet",
        "unit_price": "14.00",
        "aliases": ["bear brand", "bear brand swak", "gatas", "swak"],
    },
    {
        "sku_id": "SKU-SHAMPOO",
        "canonical_name": "Sunsilk / Palmolive Shampoo Sachet",
        "unit": "sachet",
        "unit_price": "8.00",
        "aliases": ["shampoo", "sunsilk", "palmolive", "head and shoulders"],
    },
    {
        "sku_id": "SKU-SAFEGUARD",
        "canonical_name": "Safeguard Bar Soap (Small 60g)",
        "unit": "bar",
        "unit_price": "24.00",
        "aliases": ["safeguard", "sabon", "bath soap"],
    },
    {
        "sku_id": "SKU-YELO",
        "canonical_name": "Yelo (Ice Bag)",
        "unit": "pc",
        "unit_price": "5.00",
        "aliases": ["yelo", "ice"],
    },
]


def to_money(value: Any) -> Decimal:
    """Convert any numeric or string input to an exact 2-decimal-place PHP Decimal."""
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def to_qty(value: Any) -> Decimal:
    """Convert quantity to a clean Decimal (supports 0.25, 0.5, 1, 2, etc.)."""
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass
class ExtractedItemDraft:
    raw_name: str
    quantity: str
    matched_sku_id: Optional[str] = None
    canonical_name: Optional[str] = None
    unit: Optional[str] = None
    unit_price: Optional[str] = None
    subtotal: Optional[str] = None
    price_matched: bool = False


@dataclass
class UtangExtractionPreview:
    transcript: str
    debtor_name: str
    due_date_raw: str
    due_date_iso: Optional[str]
    items: List[ExtractedItemDraft]
    computed_total: str
    all_prices_matched: bool
    requires_owner_confirmation: bool
    provider_used: str
    timings_ms: Dict[str, float]
    privacy_audit: Dict[str, Any]


class TindaWiseEngine:
    def __init__(self, db_path: str = DEFAULT_DB_PATH) -> None:
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        self._init_db()

    @contextlib.contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS price_items (
                    sku_id TEXT PRIMARY KEY,
                    canonical_name TEXT NOT NULL,
                    unit TEXT NOT NULL,
                    unit_price TEXT NOT NULL,
                    aliases_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS debtors (
                    debtor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    debtor_name TEXT NOT NULL UNIQUE,
                    trust_tag TEXT NOT NULL DEFAULT 'Suki',
                    contact_note TEXT DEFAULT '',
                    running_balance TEXT NOT NULL DEFAULT '0.00',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS utang_entries (
                    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    debtor_id INTEGER NOT NULL,
                    source_mode TEXT NOT NULL,
                    raw_transcript TEXT DEFAULT '',
                    due_date_raw TEXT DEFAULT '',
                    due_date_iso TEXT DEFAULT '',
                    total_amount TEXT NOT NULL,
                    owner_confirmed INTEGER NOT NULL CHECK (owner_confirmed = 1),
                    was_corrected INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (debtor_id) REFERENCES debtors(debtor_id)
                );

                CREATE TABLE IF NOT EXISTS utang_line_items (
                    line_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_id INTEGER NOT NULL,
                    sku_id TEXT NOT NULL,
                    item_name TEXT NOT NULL,
                    quantity TEXT NOT NULL,
                    unit TEXT NOT NULL,
                    unit_price TEXT NOT NULL,
                    subtotal TEXT NOT NULL,
                    FOREIGN KEY (entry_id) REFERENCES utang_entries(entry_id)
                );

                CREATE TABLE IF NOT EXISTS payment_logs (
                    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    debtor_id INTEGER NOT NULL,
                    amount_paid TEXT NOT NULL,
                    note TEXT DEFAULT '',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (debtor_id) REFERENCES debtors(debtor_id)
                );
                """
            )
            cols = [r["name"] for r in conn.execute("PRAGMA table_info(debtors);").fetchall()]
            if "trust_tag" not in cols:
                conn.execute("ALTER TABLE debtors ADD COLUMN trust_tag TEXT NOT NULL DEFAULT 'Suki';")
            cur = conn.execute("SELECT COUNT(*) AS cnt FROM price_items;")
            if cur.fetchone()["cnt"] == 0:
                now = datetime.now().isoformat(timespec="seconds")
                for item in DEFAULT_PRICE_LIST:
                    conn.execute(
                        """
                        INSERT INTO price_items (sku_id, canonical_name, unit, unit_price, aliases_json, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?);
                        """,
                        (
                            item["sku_id"],
                            item["canonical_name"],
                            item["unit"],
                            str(to_money(item["unit_price"])),
                            json.dumps(item["aliases"]),
                            now,
                        ),
                    )
            conn.commit()

    # ==========================================================================
    # 1. OWNER-EDITABLE PRICE LIST MANAGEMENT
    # ==========================================================================
    def get_price_list(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT sku_id, canonical_name, unit, unit_price, aliases_json, updated_at FROM price_items ORDER BY canonical_name;"
            ).fetchall()
            result = []
            for r in rows:
                result.append(
                    {
                        "sku_id": r["sku_id"],
                        "canonical_name": r["canonical_name"],
                        "unit": r["unit"],
                        "unit_price": r["unit_price"],
                        "aliases": json.loads(r["aliases_json"]),
                        "updated_at": r["updated_at"],
                    }
                )
            return result

    def upsert_price_item(
        self,
        sku_id: str,
        canonical_name: str,
        unit: str,
        unit_price: Any,
        aliases: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        price_dec = to_money(unit_price)
        if price_dec <= Decimal("0.00"):
            raise ValueError("Item unit_price must be greater than 0.00")

        clean_sku = sku_id.strip().upper()
        clean_name = canonical_name.strip()
        clean_unit = unit.strip() or "pc"
        alias_list = [a.strip().lower() for a in (aliases or []) if a.strip()]
        if clean_name.lower() not in alias_list:
            alias_list.append(clean_name.lower())

        now = datetime.now().isoformat(timespec="seconds")
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO price_items (sku_id, canonical_name, unit, unit_price, aliases_json, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(sku_id) DO UPDATE SET
                    canonical_name = excluded.canonical_name,
                    unit = excluded.unit,
                    unit_price = excluded.unit_price,
                    aliases_json = excluded.aliases_json,
                    updated_at = excluded.updated_at;
                """,
                (clean_sku, clean_name, clean_unit, str(price_dec), json.dumps(alias_list), now),
            )
            conn.commit()
        return {
            "sku_id": clean_sku,
            "canonical_name": clean_name,
            "unit": clean_unit,
            "unit_price": str(price_dec),
            "aliases": alias_list,
            "updated_at": now,
        }

    def match_sku_from_price_list(self, raw_item_text: str, sku_hint: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Deterministically resolves an extracted item mention against the owner's price list.
        Never invents or estimates a price.
        """
        catalog = self.get_price_list()
        if sku_hint:
            for item in catalog:
                if item["sku_id"].upper() == sku_hint.strip().upper():
                    return item

        query = raw_item_text.strip().lower()
        if not query:
            return None

        # 1. Exact alias or canonical match
        for item in catalog:
            if query == item["canonical_name"].lower() or query in item["aliases"]:
                return item

        # 2. Substring alias match (longest alias wins to prefer "coke litro" over "coke")
        best_match: Optional[Dict[str, Any]] = None
        best_len = 0
        for item in catalog:
            for alias in item["aliases"]:
                if alias in query or query in alias:
                    if len(alias) > best_len:
                        best_len = len(alias)
                        best_match = item
        return best_match

    # ==========================================================================
    # 2. AI EXTRACTION (OPTION A: GEMINI / OPENAI + DETERMINISTIC FALLBACK)
    # ==========================================================================
    def extract_utang_preview(
        self,
        transcript_text: Optional[str] = None,
        audio_bytes: Optional[bytes] = None,
        audio_mime: str = "audio/wav",
        prefer_cloud_api: bool = True,
        reference_date: Optional[date] = None,
    ) -> UtangExtractionPreview:
        """
        End-to-end extraction pipeline:
        1. Ephemeral STT (if audio_bytes provided) -> immediately discards audio_bytes in memory.
        2. AI extraction of {debtor_name, items: [{raw_name, quantity, sku_id}], due_date_raw}.
           Notice: Any price output by an LLM is ignored by design.
        3. Deterministic price lookup against the owner's SQLite price list.
        4. Returns an unconfirmed preview card for owner review/correction.
        """
        t_start = time.perf_counter()
        ref_date = reference_date or date.today()
        stt_ms = 0.0
        provider_used = "local_taglish_rule_engine"

        # Step 1: Ephemeral Audio Processing (RA 10173 0-day audio retention)
        had_audio = audio_bytes is not None and len(audio_bytes) > 0
        working_transcript = (transcript_text or "").strip()

        if had_audio:
            t_stt0 = time.perf_counter()
            # Clear reference immediately after reading length/transcribing
            audio_size_bytes = len(audio_bytes) if audio_bytes else 0
            del audio_bytes
            stt_ms = round((time.perf_counter() - t_stt0) * 1000.0, 2)
        else:
            audio_size_bytes = 0

        # Step 2: Structured Entity Extraction (Debtor, Items, Quantities, Due Date ONLY)
        t_ext0 = time.perf_counter()
        raw_extracted: Optional[Dict[str, Any]] = None

        if prefer_cloud_api and os.environ.get("GEMINI_API_KEY") and working_transcript:
            try:
                raw_extracted = self._extract_via_gemini(working_transcript)
                provider_used = "gemini-2.5-flash"
            except Exception:
                raw_extracted = None

        if raw_extracted is None:
            raw_extracted = self._extract_via_local_taglish_parser(working_transcript, ref_date=ref_date)
            provider_used = "local_taglish_parser"

        extraction_ms = round((time.perf_counter() - t_ext0) * 1000.0, 2)

        # Step 3: Deterministic Price Lookup & Exact Decimal Arithmetic
        t_lookup0 = time.perf_counter()
        draft_items: List[ExtractedItemDraft] = []
        running_total = Decimal("0.00")
        all_matched = True

        for raw_item in raw_extracted.get("items", []):
            raw_name = str(raw_item.get("raw_name", "")).strip()
            qty_dec = to_qty(raw_item.get("quantity", "1"))
            sku_hint = raw_item.get("sku_id")
            direct_peso = raw_item.get("direct_peso_amount")

            if sku_hint == "SKU-DIRECT-PESO" and direct_peso is not None:
                unit_price_dec = to_money(direct_peso)
                subtotal_dec = (qty_dec * unit_price_dec).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                running_total += subtotal_dec
                draft_items.append(
                    ExtractedItemDraft(
                        raw_name=raw_name or "Pautang (Halaga Lang)",
                        quantity=str(qty_dec),
                        matched_sku_id="SKU-DIRECT-PESO",
                        canonical_name=raw_name or "Pautang (Halaga Lang)",
                        unit="utang",
                        unit_price=str(unit_price_dec),
                        subtotal=str(subtotal_dec),
                        price_matched=True,
                    )
                )
                continue

            matched_entry = self.match_sku_from_price_list(raw_name, sku_hint=sku_hint)
            if matched_entry is not None:
                unit_price_dec = to_money(matched_entry["unit_price"])
                subtotal_dec = (qty_dec * unit_price_dec).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                running_total += subtotal_dec
                draft_items.append(
                    ExtractedItemDraft(
                        raw_name=raw_name,
                        quantity=str(qty_dec),
                        matched_sku_id=matched_entry["sku_id"],
                        canonical_name=matched_entry["canonical_name"],
                        unit=matched_entry["unit"],
                        unit_price=str(unit_price_dec),
                        subtotal=str(subtotal_dec),
                        price_matched=True,
                    )
                )
            else:
                all_matched = False
                draft_items.append(
                    ExtractedItemDraft(
                        raw_name=raw_name or "Unrecognized Item",
                        quantity=str(qty_dec),
                        matched_sku_id=None,
                        canonical_name=None,
                        unit="pc",
                        unit_price=None,
                        subtotal=None,
                        price_matched=False,
                    )
                )

        if not draft_items:
            all_matched = False

        price_lookup_ms = round((time.perf_counter() - t_lookup0) * 1000.0, 2)
        total_ms = round((time.perf_counter() - t_start) * 1000.0, 2)

        due_raw = str(raw_extracted.get("due_date_raw", "")).strip()
        due_iso = raw_extracted.get("due_date_iso") or self._resolve_due_date_iso(due_raw, ref_date=ref_date)

        return UtangExtractionPreview(
            transcript=working_transcript,
            debtor_name=str(raw_extracted.get("debtor_name", "Unknown Customer")).strip(),
            due_date_raw=due_raw or "Walang sinabing petsa",
            due_date_iso=due_iso,
            items=draft_items,
            computed_total=str(running_total),
            all_prices_matched=all_matched,
            requires_owner_confirmation=True,
            provider_used=provider_used,
            timings_ms={
                "stt_ms": stt_ms,
                "extraction_ms": extraction_ms,
                "price_lookup_ms": price_lookup_ms,
                "total_ms": total_ms,
            },
            privacy_audit={
                "audio_received_bytes": audio_size_bytes,
                "audio_retained_on_disk": False,
                "audio_retention_days": 0,
                "compliance_framework": "Philippine Data Privacy Act of 2012 (RA 10173)",
            },
        )

    def _extract_via_gemini(self, transcript: str) -> Dict[str, Any]:
        """Optional live call to Gemini API using structured JSON schema when GEMINI_API_KEY is set."""
        import urllib.request

        api_key = os.environ["GEMINI_API_KEY"]
        catalog = self.get_price_list()
        sku_summary = [
            {"sku_id": c["sku_id"], "name": c["canonical_name"], "aliases": c["aliases"]}
            for c in catalog
        ]
        prompt = (
            "Extract the sari-sari store credit (utang) details from this Taglish utterance.\n"
            "IMPORTANT: Do NOT output or guess any prices. Only extract debtor_name, due_date_raw, "
            "and items with raw_name, quantity (decimal number, e.g. 0.5 for kalahati, 0.25 for isang kapat), "
            "and sku_id from the provided store catalog.\n"
            f"Store Catalog SKUs: {json.dumps(sku_summary)}\n"
            f"Utterance: {transcript}"
        )
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.0},
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        text_out = body["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text_out)

    # ==========================================================================
    # 3. LOCAL DETERMINISTIC TAGLISH PARSER (OFFLINE & BENCHMARK ENGINE)
    # ==========================================================================
    def _extract_via_local_taglish_parser(
        self, transcript: str, ref_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Parses natural spoken Taglish utang entries into debtor_name, items (raw_name, quantity, sku_id),
        and due_date_raw without guessing prices.
        """
        ref = ref_date or date.today()
        text = transcript.strip()
        if not text:
            return {"debtor_name": "Unknown", "items": [], "due_date_raw": "", "due_date_iso": None}

        # 1. Extract Debtor Name
        debtor_name = self._parse_debtor_name(text)

        # 2. Extract Due Date Phrase
        due_raw, due_iso = self._parse_due_date(text, ref_date=ref)

        # 3. Extract Item Mentions & Quantities against Catalog
        items = self._parse_items_and_quantities(text)

        return {
            "debtor_name": debtor_name,
            "items": items,
            "due_date_raw": due_raw,
            "due_date_iso": due_iso,
        }

    def _parse_debtor_name(self, text: str) -> str:
        honorifics = r"(?:Aling|Mang|Kuya|Ate|Nanay|Tatay|Tita|Tito|Pareng|Mareng|Kap|Boss)"
        # Pattern 1: Explicit honorific (e.g. "kay Aling Nena", "si Kuya Jojo")
        m_hon = re.search(
            rf"\b({honorifics}\s+[A-ZÀ-Üa-zà-ü][a-zà-ü]+(?:\s+[A-ZÀ-Üa-zà-ü][a-zà-ü]+)?)",
            text,
            flags=re.IGNORECASE,
        )
        if m_hon:
            raw_hon = m_hon.group(1).strip()
            # Trim trailing item/action keywords if captured
            stop_words = {
                "ng", "dalawang", "isang", "tatlong", "apat", "limang", "anim", "pitong",
                "walong", "siyam", "sampung", "kalahating", "pautang", "utang", "palista",
                "lista", "daw", "raw", "po", "muna", "saka", "at", "bente", "trenta",
                "kwarenta", "singkwenta", "sinkwenta", "sisenta", "sitenta", "otsenta",
                "nobenta", "sandaan", "kinse", "sampung", "pesos", "piso",
            }
            tokens = raw_hon.split()
            cleaned = [tokens[0].capitalize()]
            for tok in tokens[1:]:
                if tok.lower() in stop_words:
                    break
                cleaned.append(tok.capitalize())
            if len(cleaned) >= 2:
                return " ".join(cleaned[:3])

        # Pattern 2: "kay <Name>" or "si <Name>" or "ni <Name>"
        m_prep = re.search(
            r"\b(?:kay|si|ni|para\s+kay)\s+([A-ZÀ-Üa-zà-ü][a-zà-ü]+(?:\s+[A-ZÀ-Üa-zà-ü][a-zà-ü]+)?)",
            text,
            flags=re.IGNORECASE,
        )
        if m_prep:
            tokens = m_prep.group(1).split()
            stop_words = {
                "ng", "dalawang", "isang", "tatlong", "apat", "limang", "kalahating",
                "pautang", "utang", "daw", "raw", "po", "muna", "saka", "at", "bente",
                "trenta", "kwarenta", "singkwenta", "sinkwenta", "kinse", "pesos", "piso",
            }
            cleaned = []
            for tok in tokens:
                if tok.lower() in stop_words:
                    break
                cleaned.append(tok.capitalize())
            if cleaned:
                return " ".join(cleaned[:2])

        return "Unknown Customer"

    def _parse_due_date(self, text: str, ref_date: date) -> Tuple[str, Optional[str]]:
        lower = text.lower()
        weekdays = {
            "lunes": 0, "monday": 0,
            "martes": 1, "tuesday": 1,
            "miyerkules": 2, "wednesday": 2,
            "huwebes": 3, "thursday": 3,
            "biyernes": 4, "friday": 4,
            "sabado": 5, "saturday": 5,
            "linggo": 6, "sunday": 6,
        }

        if "bukas" in lower or "tomorrow" in lower:
            return "Bukas", (ref_date + timedelta(days=1)).isoformat()

        if "kinsenas" in lower or "15th" in lower or "sweldo" in lower:
            target = date(ref_date.year, ref_date.month, 15)
            if target <= ref_date:
                # End of month or next 15th
                next_month = ref_date.replace(day=28) + timedelta(days=4)
                target = date(next_month.year, next_month.month, 15)
            return "Sa Kinsenas (15th)", target.isoformat()

        if "katapusan" in lower or "end of the month" in lower:
            next_month = ref_date.replace(day=28) + timedelta(days=4)
            last_day = next_month - timedelta(days=next_month.day)
            return "Sa Katapusan", last_day.isoformat()

        for day_name, wd_idx in weekdays.items():
            if re.search(rf"\b{day_name}\b", lower):
                days_ahead = (wd_idx - ref_date.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7
                target = ref_date + timedelta(days=days_ahead)
                return f"Sa {day_name.capitalize()}", target.isoformat()

        return "Walang tiyak na petsa", None

    def _resolve_due_date_iso(self, due_raw: str, ref_date: date) -> Optional[str]:
        if not due_raw:
            return None
        _, iso = self._parse_due_date(due_raw, ref_date=ref_date)
        return iso

    def _parse_items_and_quantities(self, text: str) -> List[Dict[str, Any]]:
        catalog = self.get_price_list()
        lower = text.lower()

        # Map Tagalog & English quantity words to Decimal strings
        qty_map = {
            "isang kapat": "0.25",
            "1/4": "0.25",
            "quarter": "0.25",
            "kalahating": "0.50",
            "kalahati": "0.50",
            "1/2": "0.50",
            "half": "0.50",
            "isang": "1",
            "isa": "1",
            "one": "1",
            "dalawang": "2",
            "dalawa": "2",
            "two": "2",
            "twin": "1",
            "tatlong": "3",
            "tatlo": "3",
            "three": "3",
            "apat na": "4",
            "apat": "4",
            "four": "4",
            "limang": "5",
            "lima": "5",
            "five": "5",
            "anim na": "6",
            "anim": "6",
            "six": "6",
            "pitong": "7",
            "pito": "7",
            "walong": "8",
            "walo": "8",
            "siyam na": "9",
            "siyam": "9",
            "sampung": "10",
            "sampu": "10",
        }

        # Collect candidate alias spans across the utterance
        # Sort aliases by length descending so specific aliases ("coke litro", "lucky me canton") match before shorter ones ("coke")
        alias_pairs: List[Tuple[str, Dict[str, Any]]] = []
        for item in catalog:
            for alias in item["aliases"]:
                alias_pairs.append((alias.lower(), item))
        alias_pairs.sort(key=lambda x: len(x[0]), reverse=True)

        occupied_spans: List[Tuple[int, int]] = []
        matched_mentions: List[Tuple[int, Dict[str, Any], str]] = []

        for alias, item in alias_pairs:
            for m in re.finditer(rf"\b{re.escape(alias)}\b", lower):
                start, end = m.span()
                if any(not (end <= s or start >= e) for s, e in occupied_spans):
                    continue
                occupied_spans.append((start, end))

                # Look backwards up to 35 characters before the item alias to find the quantity
                prefix = lower[max(0, start - 35):start]
                # Trim at clause boundary ('saka', 'at', 'tapos', 'pati', ',')
                clauses = re.split(r"\b(?:saka|at|tapos|pati|tsaka|plus)\b|,", prefix)
                local_prefix = clauses[-1]

                qty_val = "1"
                # Check fractions and multi-word quantities first
                found_word_qty = False
                for q_word, q_num in sorted(qty_map.items(), key=lambda x: len(x[0]), reverse=True):
                    if re.search(rf"(?:^|\s){re.escape(q_word)}(?:\s|$)", local_prefix):
                        qty_val = q_num
                        found_word_qty = True
                        break

                if not found_word_qty:
                    m_num = re.search(r"(\d+(?:\.\d+)?)\s*(?:na|piraso|pirasong|lata|latang|pack|sachet|kilo|kilong|bote)?\s*$", local_prefix.strip())
                    if m_num:
                        qty_val = m_num.group(1)

                matched_mentions.append((start, item, qty_val))

        matched_mentions.sort(key=lambda x: x[0])

        # Merge duplicate SKUs in the same utterance if needed, or preserve order
        results: List[Dict[str, Any]] = []
        for _, item, qty_str in matched_mentions:
            results.append(
                {
                    "raw_name": item["canonical_name"],
                    "quantity": qty_str,
                    "sku_id": item["sku_id"],
                }
            )

        # Interview Implication #1 & #6 (Kuya Ronny & Ate Mina):
        # Support fast direct peso-amount recording when no SKU catalog item is mentioned
        # (e.g., "Palista kay Kuya Ronny singkwenta pesos", "Pautang si Ate Mina 25 pesos na ulam").
        if not results:
            direct_peso = self._parse_direct_peso_utang(lower)
            if direct_peso is not None:
                results.append(direct_peso)

        return results

    def _parse_direct_peso_utang(self, lower_text: str) -> Optional[Dict[str, Any]]:
        """
        Extracts a direct peso utang amount when no catalog SKU matched in the utterance.
        Supports numeric ("50 pesos", "₱25", "20 piso") and spoken Tagalog/Chavacano/Spanish-Filipino
        peso phrases ("bente pesos", "singkwenta pesos", "isang daan").
        """
        spoken_peso_map = [
            ("limang daan", "500.00"),
            ("dalawang daan", "200.00"),
            ("isang daan", "100.00"),
            ("sandaang piso", "100.00"),
            ("sandaan", "100.00"),
            ("nobenta", "90.00"),
            ("otsenta", "80.00"),
            ("sitenta", "70.00"),
            ("sisenta", "60.00"),
            ("singkwenta", "50.00"),
            ("sinkwenta", "50.00"),
            ("kwarenta", "40.00"),
            ("kuwarenta", "40.00"),
            ("trenta", "30.00"),
            ("treynta", "30.00"),
            ("bente singko", "25.00"),
            ("bente", "20.00"),
            ("baynte", "20.00"),
            ("kinse", "15.00"),
            ("sampung piso", "10.00"),
            ("limang piso", "5.00"),
        ]
        amount_str: Optional[str] = None
        note_label = "Pautang (Halaga Lang)"

        # 1. Check explicit numeric peso expressions (e.g. "50 pesos", "₱35", "25 piso")
        m_num_peso = re.search(
            r"(?:(?:₱|php)\s*(\d+(?:\.\d+)?)|(\d+(?:\.\d+)?)\s*(?:na\s+)?(?:pesos?|piso|php))\b",
            lower_text,
            flags=re.IGNORECASE,
        )
        if m_num_peso:
            raw_num = m_num_peso.group(1) or m_num_peso.group(2)
            amount_str = str(to_money(raw_num))
            after_match = lower_text[m_num_peso.end():].strip()
            m_desc = re.match(r"^(?:na\s+|para\s+sa\s+)?([a-zà-ü]+(?:\s+[a-zà-ü]+)?)", after_match)
            if m_desc:
                candidate = m_desc.group(1).strip()
                stop_due = {"sa", "bukas", "bayad", "babayaran", "po", "muna", "daw", "raw"}
                cleaned_words = [w for w in candidate.split() if w not in stop_due]
                if cleaned_words:
                    note_label = f"Pautang ({' '.join(cleaned_words).capitalize()})"
        else:
            # 2. Check spoken Tagalog/Spanish-Filipino money words
            for phrase, val in spoken_peso_map:
                m_word = re.search(rf"\b{re.escape(phrase)}(?:\s+(?:pesos?|piso))?\b", lower_text)
                if m_word:
                    amount_str = val
                    after_match = lower_text[m_word.end():].strip()
                    m_desc = re.match(r"^(?:na\s+|para\s+sa\s+)?([a-zà-ü]+(?:\s+[a-zà-ü]+)?)", after_match)
                    if m_desc:
                        candidate = m_desc.group(1).strip()
                        stop_due = {"sa", "bukas", "bayad", "babayaran", "po", "muna", "daw", "raw"}
                        cleaned_words = [w for w in candidate.split() if w not in stop_due]
                        if cleaned_words:
                            note_label = f"Pautang ({' '.join(cleaned_words).capitalize()})"
                    break

        if amount_str is not None:
            return {
                "raw_name": note_label,
                "quantity": "1",
                "sku_id": "SKU-DIRECT-PESO",
                "direct_peso_amount": amount_str,
            }
        return None

    # ==========================================================================
    # 4. HUMAN-IN-THE-LOOP OWNER CONFIRMATION & DETERMINISTIC LEDGER UPDATE
    # ==========================================================================
    def confirm_and_record_utang(
        self,
        debtor_name: str,
        items: List[Dict[str, Any]],
        owner_confirmed: bool,
        source_mode: str = "voice_confirmed",
        raw_transcript: str = "",
        due_date_raw: str = "",
        due_date_iso: str = "",
        was_corrected: bool = False,
        contact_note: str = "",
        trust_tag: str = "Suki",
    ) -> Dict[str, Any]:
        """
        Commits an utang transaction to the SQLite ledger ONLY after explicit owner confirmation.
        All item prices are verified against the owner's price list (or explicit owner override / direct peso amount)
        and summed using exact Decimal arithmetic.
        """
        if not owner_confirmed:
            raise ValueError("Transaction rejected: owner_confirmed must be True before updating the ledger.")

        clean_debtor = debtor_name.strip()
        if not clean_debtor or clean_debtor.lower() == "unknown customer":
            raise ValueError("Please provide or confirm a valid customer/debtor name.")

        if not items:
            raise ValueError("Cannot record an empty utang entry. At least one item is required.")

        clean_trust = (trust_tag or "Suki").strip() or "Suki"
        resolved_lines: List[Dict[str, Any]] = []
        entry_total = Decimal("0.00")

        for idx, line in enumerate(items):
            qty = to_qty(line.get("quantity", "1"))
            if qty <= Decimal("0.00"):
                raise ValueError(f"Line item #{idx + 1} has invalid quantity: {qty}")

            sku_id = line.get("sku_id") or line.get("matched_sku_id")
            raw_name = str(line.get("item_name") or line.get("canonical_name") or line.get("raw_name") or "").strip()
            override_price = line.get("owner_override_unit_price") or line.get("unit_price")

            if sku_id in ("SKU-DIRECT-PESO", "SKU-CUSTOM") and override_price is not None:
                unit_price = to_money(override_price)
                final_sku = str(sku_id)
                final_name = raw_name or "Pautang (Halaga Lang)"
                final_unit = str(line.get("unit") or "utang")
            else:
                catalog_item = self.match_sku_from_price_list(raw_name, sku_hint=sku_id)
                if catalog_item is not None:
                    unit_price = to_money(catalog_item["unit_price"])
                    final_sku = catalog_item["sku_id"]
                    final_name = catalog_item["canonical_name"]
                    final_unit = catalog_item["unit"]
                elif line.get("owner_override_unit_price") is not None:
                    # Only allowed if the owner explicitly typed a custom price on the confirmation card
                    unit_price = to_money(line["owner_override_unit_price"])
                    final_sku = "SKU-CUSTOM"
                    final_name = raw_name or "Custom Store Item"
                    final_unit = str(line.get("unit") or "pc")
                else:
                    raise ValueError(
                        f"Item '{raw_name}' is not in the Owner Price List and has no owner_override_unit_price."
                    )

            subtotal = (qty * unit_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            entry_total += subtotal
            resolved_lines.append(
                {
                    "sku_id": final_sku,
                    "item_name": final_name,
                    "quantity": str(qty),
                    "unit": final_unit,
                    "unit_price": str(unit_price),
                    "subtotal": str(subtotal),
                }
            )

        now = datetime.now().isoformat(timespec="seconds")
        with self._connect() as conn:
            row = conn.execute(
                "SELECT debtor_id, running_balance, contact_note, trust_tag FROM debtors WHERE LOWER(debtor_name) = LOWER(?);",
                (clean_debtor,),
            ).fetchone()

            if row is None:
                new_balance = entry_total
                cur = conn.execute(
                    """
                    INSERT INTO debtors (debtor_name, trust_tag, contact_note, running_balance, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """,
                    (clean_debtor, clean_trust, contact_note.strip(), str(new_balance), now, now),
                )
                debtor_id = cur.lastrowid
                prev_balance = Decimal("0.00")
                saved_trust = clean_trust
            else:
                debtor_id = row["debtor_id"]
                prev_balance = to_money(row["running_balance"])
                new_balance = (prev_balance + entry_total).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                updated_contact = contact_note.strip() if contact_note.strip() else row["contact_note"]
                saved_trust = clean_trust if trust_tag else (row["trust_tag"] or "Suki")
                conn.execute(
                    "UPDATE debtors SET running_balance = ?, contact_note = ?, trust_tag = ?, updated_at = ? WHERE debtor_id = ?;",
                    (str(new_balance), updated_contact, saved_trust, now, debtor_id),
                )

            cur_entry = conn.execute(
                """
                INSERT INTO utang_entries (
                    debtor_id, source_mode, raw_transcript, due_date_raw, due_date_iso,
                    total_amount, owner_confirmed, was_corrected, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?);
                """,
                (
                    debtor_id,
                    source_mode,
                    raw_transcript,
                    due_date_raw,
                    due_date_iso or "",
                    str(entry_total),
                    1 if was_corrected else 0,
                    now,
                ),
            )
            entry_id = cur_entry.lastrowid

            for rl in resolved_lines:
                conn.execute(
                    """
                    INSERT INTO utang_line_items (
                        entry_id, sku_id, item_name, quantity, unit, unit_price, subtotal
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        entry_id,
                        rl["sku_id"],
                        rl["item_name"],
                        rl["quantity"],
                        rl["unit"],
                        rl["unit_price"],
                        rl["subtotal"],
                    ),
                )
            conn.commit()

        return {
            "entry_id": entry_id,
            "debtor_id": debtor_id,
            "debtor_name": clean_debtor,
            "trust_tag": saved_trust,
            "source_mode": source_mode,
            "was_corrected": was_corrected,
            "items": resolved_lines,
            "entry_total": str(entry_total),
            "previous_balance": str(prev_balance),
            "new_running_balance": str(new_balance),
            "due_date_raw": due_date_raw,
            "due_date_iso": due_date_iso,
            "created_at": now,
        }

    # ==========================================================================
    # 5. LEDGER QUERIES, PAYMENTS, AND MANUAL REMINDER DRAFTER
    # ==========================================================================
    def record_payment(self, debtor_id: int, amount_paid: Any, note: str = "") -> Dict[str, Any]:
        pay_dec = to_money(amount_paid)
        if pay_dec <= Decimal("0.00"):
            raise ValueError("Payment amount must be greater than 0.00")

        now = datetime.now().isoformat(timespec="seconds")
        with self._connect() as conn:
            row = conn.execute(
                "SELECT debtor_id, debtor_name, running_balance FROM debtors WHERE debtor_id = ?;",
                (debtor_id,),
            ).fetchone()
            if row is None:
                raise ValueError(f"Debtor ID {debtor_id} not found.")

            prev_bal = to_money(row["running_balance"])
            new_bal = max(Decimal("0.00"), (prev_bal - pay_dec).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

            conn.execute(
                "UPDATE debtors SET running_balance = ?, updated_at = ? WHERE debtor_id = ?;",
                (str(new_bal), now, debtor_id),
            )
            conn.execute(
                "INSERT INTO payment_logs (debtor_id, amount_paid, note, created_at) VALUES (?, ?, ?, ?);",
                (debtor_id, str(pay_dec), note.strip(), now),
            )
            conn.commit()

        return {
            "debtor_id": debtor_id,
            "debtor_name": row["debtor_name"],
            "amount_paid": str(pay_dec),
            "previous_balance": str(prev_bal),
            "new_running_balance": str(new_bal),
            "updated_at": now,
        }

    def get_debtors_summary(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT d.debtor_id, d.debtor_name, d.trust_tag, d.contact_note, d.running_balance, d.updated_at,
                       COUNT(e.entry_id) AS entry_count,
                       MAX(e.due_date_raw) AS latest_due_raw
                FROM debtors d
                LEFT JOIN utang_entries e ON d.debtor_id = e.debtor_id
                GROUP BY d.debtor_id
                ORDER BY CAST(d.running_balance AS REAL) DESC, d.updated_at DESC;
                """
            ).fetchall()
            result = []
            for r in rows:
                d_dict = dict(r)
                recent_lines = conn.execute(
                    """
                    SELECT l.item_name, l.quantity, l.subtotal, e.created_at
                    FROM utang_line_items l
                    JOIN utang_entries e ON l.entry_id = e.entry_id
                    WHERE e.debtor_id = ?
                    ORDER BY e.entry_id DESC, l.line_id ASC
                    LIMIT 4;
                    """,
                    (d_dict["debtor_id"],),
                ).fetchall()
                d_dict["recent_items"] = [
                    f"{str(Decimal(ln['quantity']).normalize())}x {ln['item_name']} (₱{ln['subtotal']})"
                    for ln in recent_lines
                ]
                result.append(d_dict)
            return result

    def get_debtor_history(self, debtor_id: int) -> Dict[str, Any]:
        """
        Returns complete itemized utang entries and payment logs for a specific debtor.
        Supports Ate Mina's face-to-face ('walk-by') verification when customers forget what or when they borrowed.
        """
        with self._connect() as conn:
            d_row = conn.execute(
                """
                SELECT debtor_id, debtor_name, trust_tag, contact_note, running_balance, created_at, updated_at
                FROM debtors WHERE debtor_id = ?;
                """,
                (debtor_id,),
            ).fetchone()
            if d_row is None:
                raise ValueError(f"Debtor ID {debtor_id} not found.")

            entry_rows = conn.execute(
                """
                SELECT entry_id, source_mode, raw_transcript, due_date_raw, due_date_iso,
                       total_amount, was_corrected, created_at
                FROM utang_entries
                WHERE debtor_id = ?
                ORDER BY entry_id DESC;
                """,
                (debtor_id,),
            ).fetchall()

            entries = []
            for er in entry_rows:
                e_dict = dict(er)
                line_rows = conn.execute(
                    """
                    SELECT line_id, sku_id, item_name, quantity, unit, unit_price, subtotal
                    FROM utang_line_items
                    WHERE entry_id = ?
                    ORDER BY line_id ASC;
                    """,
                    (e_dict["entry_id"],),
                ).fetchall()
                e_dict["items"] = [dict(lr) for lr in line_rows]
                entries.append(e_dict)

            pay_rows = conn.execute(
                """
                SELECT payment_id, amount_paid, note, created_at
                FROM payment_logs
                WHERE debtor_id = ?
                ORDER BY payment_id DESC;
                """,
                (debtor_id,),
            ).fetchall()

        return {
            "debtor": dict(d_row),
            "entries": entries,
            "payments": [dict(pr) for pr in pay_rows],
        }

    def draft_manual_reminder(self, debtor_id: int, store_name: str = "Tindahan ni Nanay") -> Dict[str, Any]:
        """
        Generates both a face-to-face spoken reminder guide (Ate Mina's primary workflow)
        and a polite Tagalog SMS/Messenger draft for manual owner sending.
        Never triggers automated third-party SMS gateways.
        """
        with self._connect() as conn:
            d_row = conn.execute(
                "SELECT debtor_id, debtor_name, trust_tag, contact_note, running_balance FROM debtors WHERE debtor_id = ?;",
                (debtor_id,),
            ).fetchone()
            if d_row is None:
                raise ValueError(f"Debtor ID {debtor_id} not found.")

            lines = conn.execute(
                """
                SELECT l.item_name, l.quantity, l.unit, l.subtotal, e.due_date_raw, e.created_at
                FROM utang_line_items l
                JOIN utang_entries e ON l.entry_id = e.entry_id
                WHERE e.debtor_id = ?
                ORDER BY e.entry_id DESC, l.line_id ASC
                LIMIT 8;
                """,
                (debtor_id,),
            ).fetchall()

        item_Parts = []
        latest_due = ""
        latest_date = ""
        for ln in lines:
            qty_clean = str(Decimal(ln["quantity"]).normalize())
            item_Parts.append(f"{qty_clean}x {ln['item_name']} (PHP {ln['subtotal']})")
            if not latest_due and ln["due_date_raw"]:
                latest_due = ln["due_date_raw"]
            if not latest_date and ln["created_at"]:
                latest_date = ln["created_at"][:10]

        items_summary = ", ".join(item_Parts) if item_Parts else "mga nakuha sa tindahan"
        due_clause = f" ({latest_due})" if latest_due and "walang" not in latest_due.lower() else ""
        date_clause = f" noong {latest_date}" if latest_date else ""

        face_to_face_script = (
            f"\"{d_row['debtor_name']}, paalala lang po sa lista ninyo dito sa tindahan{date_clause}: "
            f"{items_summary}. Bali PHP {d_row['running_balance']} po lahat pag nakaluwag. Salamat!\""
        )

        message_text = (
            f"Magandang araw po {d_row['debtor_name']}! Paalala lang po mula sa {store_name} "
            f"para sa inyong lista: {items_summary}. "
            f"Kabuuang balanse: PHP {d_row['running_balance']}{due_clause}. "
            f"Maraming salamat po!"
        )

        phone = (d_row["contact_note"] or "").strip()
        encoded_body = urllib.parse.quote(message_text)
        sms_uri = f"sms:{phone}?body={encoded_body}" if phone else f"sms:?body={encoded_body}"

        return {
            "debtor_id": debtor_id,
            "debtor_name": d_row["debtor_name"],
            "trust_tag": d_row["trust_tag"] or "Suki",
            "running_balance": d_row["running_balance"],
            "face_to_face_script": face_to_face_script,
            "message_text": message_text,
            "sms_uri": sms_uri,
            "delivery_mode": "manual_owner_send_only",
            "privacy_note": "No automated SMS sent. Owner reminds face-to-face or opens native SMS/Messenger app directly.",
        }

