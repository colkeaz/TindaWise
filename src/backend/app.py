"""
TindaWise FastAPI Application Server
Provides REST APIs informed by Sari-Sari Store Owner Field Interviews (Kuya Ronny Bautista & Ate Mina):
- Owner-editable price list (`GET /api/prices`, `POST /api/prices`)
- Ephemeral STT + AI extraction preview supporting SKU catalog & direct peso utang (`POST /api/extract-utang`)
- Human-in-the-loop owner confirmation, Suki/Kakilala trust tags & deterministic ledger update (`POST /api/ledger/confirm`)
- 1-Tap Simple Kwaderno & Quick Peso fallback entry (`POST /api/ledger/confirm` with `source_mode="tap_fallback"`)
- Debtor balances, walk-by itemized history & face-to-face / SMS reminder drafting (`GET /api/ledger/debtors`, `GET /api/ledger/debtors/{debtor_id}`, `GET /api/ledger/reminder/{debtor_id}`)
- Full or partial debt repayment (`POST /api/ledger/pay`, `POST /api/ledger/payment`)
- RA 10173 Data Privacy compliance summary (`GET /api/privacy`)
"""

from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

from ledger_engine import DEFAULT_DB_PATH, TindaWiseEngine

app = FastAPI(
    title="TindaWise Counter Utang Copilot",
    description="Spoken Taglish Utang Extraction + Owner Confirmation + Deterministic Price List & Ledger",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = TindaWiseEngine(db_path=os.environ.get("TINDAWISE_DB_PATH", DEFAULT_DB_PATH))
FRONTEND_HTML = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "frontend",
    "index.html",
)


class PriceItemUpsertRequest(BaseModel):
    sku_id: str
    canonical_name: str
    unit: str = "pc"
    unit_price: str
    aliases: List[str] = Field(default_factory=list)


class ExtractUtangRequest(BaseModel):
    transcript_text: str
    prefer_cloud_api: bool = True


class ConfirmLineItem(BaseModel):
    sku_id: Optional[str] = None
    item_name: str
    quantity: str
    unit: str = "pc"
    owner_override_unit_price: Optional[str] = None


class ConfirmUtangRequest(BaseModel):
    debtor_name: str
    items: List[ConfirmLineItem]
    owner_confirmed: bool
    source_mode: str = "voice_confirmed"
    raw_transcript: str = ""
    due_date_raw: str = ""
    due_date_iso: str = ""
    was_corrected: bool = False
    contact_note: str = ""
    trust_tag: str = "Suki"


class PaymentRequest(BaseModel):
    debtor_id: int
    amount_paid: str
    note: str = ""


@app.get("/", response_class=HTMLResponse)
def serve_frontend() -> Any:
    if os.path.exists(FRONTEND_HTML):
        return FileResponse(FRONTEND_HTML)
    return HTMLResponse("<h1>TindaWise Backend Running</h1>")


@app.get("/api/prices")
def list_prices() -> Dict[str, Any]:
    return {"items": engine.get_price_list()}


@app.post("/api/prices")
def save_price_item(req: PriceItemUpsertRequest) -> Dict[str, Any]:
    try:
        updated = engine.upsert_price_item(
            sku_id=req.sku_id,
            canonical_name=req.canonical_name,
            unit=req.unit,
            unit_price=req.unit_price,
            aliases=req.aliases,
        )
        return {"status": "ok", "item": updated}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/extract-utang")
def extract_utang(req: ExtractUtangRequest) -> Dict[str, Any]:
    preview = engine.extract_utang_preview(
        transcript_text=req.transcript_text,
        prefer_cloud_api=req.prefer_cloud_api,
    )
    return asdict(preview)


@app.post("/api/ledger/confirm")
def confirm_utang(req: ConfirmUtangRequest) -> Dict[str, Any]:
    try:
        result = engine.confirm_and_record_utang(
            debtor_name=req.debtor_name,
            items=[item.model_dump() for item in req.items],
            owner_confirmed=req.owner_confirmed,
            source_mode=req.source_mode,
            raw_transcript=req.raw_transcript,
            due_date_raw=req.due_date_raw,
            due_date_iso=req.due_date_iso,
            was_corrected=req.was_corrected,
            contact_note=req.contact_note,
            trust_tag=req.trust_tag,
        )
        return {"status": "confirmed", "entry": result}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/ledger/debtors")
def list_debtors() -> Dict[str, Any]:
    return {"debtors": engine.get_debtors_summary()}


@app.get("/api/ledger/debtors/{debtor_id}")
def get_debtor_history(debtor_id: int) -> Dict[str, Any]:
    try:
        return engine.get_debtor_history(debtor_id=debtor_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/ledger/pay")
@app.post("/api/ledger/payment")
def pay_utang(req: PaymentRequest) -> Dict[str, Any]:
    try:
        res = engine.record_payment(
            debtor_id=req.debtor_id,
            amount_paid=req.amount_paid,
            note=req.note,
        )
        return {"status": "paid", "payment": res}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/ledger/reminder/{debtor_id}")
def get_manual_reminder(debtor_id: int, store_name: str = "Tindahan ni Nanay") -> Dict[str, Any]:
    try:
        return engine.draft_manual_reminder(debtor_id=debtor_id, store_name=store_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/privacy")
def get_privacy_policy() -> Dict[str, Any]:
    return {
        "framework": "Philippine Data Privacy Act of 2012 (RA 10173)",
        "audio_policy": "Push-to-talk only. Ephemeral processing in memory (0-day audio retention; audio deleted immediately after STT).",
        "ledger_storage": "Stored locally on the store owner's device (SQLite / local storage). Uses customer nicknames; no government IDs required.",
        "reminder_policy": "Drafted locally on device. Supports face-to-face counter reminders or manual sending via native SMS/Messenger (no automated third-party SMS blasting).",
    }

