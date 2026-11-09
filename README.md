# TindaWise — Taglish Voice-to-Lista Counter Copilot
**Human-in-the-Loop Counter Utang Ledger for Philippine Sari-Sari Stores**  
*Tech Connect: SYNC AIdeathon (2026) — Batangas State University The NEU – Alangilan*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/framework-FastAPI-teal.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Privacy: RA 10173](https://img.shields.io/badge/Compliance-RA%2010173%20(0--Day%20Retention)-success.svg)](#privacy--compliance)
[![Deterministic Math](https://img.shields.io/badge/Ledger-100%25%20Exact%20Decimal-blueviolet.svg)](#core-design--safety-guardrails)

---

## Overview

In the Philippines, neighborhood *sari-sari* stores serve over 90% of households. During counter rush hours, micro-credit transactions (*utang sa listahan*) are hurriedly jotted down in paper notebooks (*kwaderno*), resulting in forgotten entries, lost pages, and uncollected debt. Existing digital ledger apps require 4 to 8 manual screen taps per item, causing store owners to abandon them during peak business hours.

**TindaWise** is a lightweight, mobile-first counter copilot designed to eliminate this friction through a **3-second spoken Taglish workflow** backed by deterministic financial guardrails:

$$\text{Spoken Taglish Utterance} \longrightarrow \text{Ephemeral STT} \longrightarrow \text{Entity Extraction} \longrightarrow \text{Owner Price List Match} \longrightarrow \text{Owner Confirmation} \longrightarrow \text{Deterministic Ledger Update}$$

> **Example:** An owner presses push-to-talk and says:  
> *"Pautang daw si Pareng Boyet dalawang sardinas saka limang instant noodles bayaran daw sa Sabado"*  
> Within **1.5 ms**, TindaWise extracts the debtor (`Pareng Boyet`), matches the items to the store's price list (`2x Sardines @ ₱22.00 = ₱44.00`, `5x Instant Noodles @ ₱15.00 = ₱75.00`), computes the exact total (`₱119.00`), parses the due date, and displays an itemized confirmation card with `+ / -` steppers. With **one tap**, the ledger is recorded.

---

## Core Design & Safety Guardrails

1. **Model Never Guesses Money:**
   - LLMs are prone to arithmetic errors and financial hallucinations. In TindaWise, the AI extracts **only entity tokens**: `{debtor_name, items: [{sku_id, quantity}], due_date_raw}`.
   - All monetary amounts are computed strictly against the store owner's editable price catalog (`price_items` table) using Python `Decimal(quantize="0.01")` arithmetic.
2. **Ephemeral Previews & Human-in-the-Loop Confirmation:**
   - Spoken extraction produces an ephemeral preview. **No database balance is altered until the store owner explicitly taps Confirm**.
   - If ambient noise causes a mishear (e.g., 3 cans instead of 2), the owner adjusts the quantity with a single tap before committing.
3. **1-Tap No-Voice Fallback for Peak Noise:**
   - Philippine street counters frequently experience loud background noise (revving tricycles, street chatter, rain on tin roofs).
   - The UI includes a permanent **1-Tap Quick Fallback Bar** allowing instant logging of common items without voice input.
4. **RA 10173 (Philippine Data Privacy Act) Compliance:**
   - **0-Day Audio Retention:** Spoken audio buffers are processed in memory and discarded immediately after transcription. No audio recordings are stored.
   - **Local Nicknames:** Customers are identified by familiar neighborhood nicknames (e.g., *Aling Nena*, *Kuya Jun*) rather than sensitive national IDs or full legal names.
5. **Owner-Controlled Polite Reminders:**
   - Debt collection is socially sensitive in Filipino barangay culture. TindaWise generates polite, culturally respectful SMS/messenger drafts (e.g., *"Magandang araw po Aling Nena! Paalala lang po..."*) that the owner reviews and sends manually. The system never sends automated or harassing messages.

---

## Repository Structure

```text
.
├── .gitignore                         # Git exclusion rules (pycache, databases, handoff)
├── requirements.txt                   # Production dependencies (FastAPI, Uvicorn, Pydantic)
├── README.md                          # Project documentation & quickstart
├── HANDOFF.md                         # Architecture handoff & competition deliverables guide
├── data/
│   └── eval/
│       ├── sample_manifest.csv        # 36-utterance multi-speaker Taglish benchmark dataset
│       └── Evaluation_Benchmark_Report.md  # Generated evaluation accuracy & latency report
├── src/
│   ├── backend/
│   │   ├── app.py                     # FastAPI REST API server
│   │   └── ledger_engine.py           # SQLite database schema, price list, Decimal ledger math
│   ├── eval/
│   │   └── evaluate_voice_utang.py    # Multi-speaker evaluation benchmark harness
│   └── frontend/
│       └── index.html                 # Mobile-first counter capture, confirmation & tap fallback UI
└── tests/
    └── test_ledger_engine.py          # Unit tests verifying pricing safety, math & privacy rules
```

---

## Quickstart Guide

### 1. Prerequisites
- Python 3.10 or higher
- Modern web browser (Chrome, Edge, Safari, Firefox)

### 2. Installation
```powershell
# Clone the repository
git clone https://github.com/colkeaz/TindaWise.git
cd TindaWise

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Unit Tests
Verifies that extraction previews never alter balances without confirmation, prices are strictly resolved from the owner catalog, and partial payments calculate with exact `Decimal` precision:
```powershell
python -m unittest tests/test_ledger_engine.py -v
```

### 4. Run the 36-Utterance Taglish Benchmark
Evaluates extraction accuracy and execution latency across 36 spoken Taglish utterances with 6 speakers and 4 counter noise conditions (Quiet, Street Chatter, Tricycle/Motorcycle, Rainy Counter):
```powershell
python src/eval/evaluate_voice_utang.py
```

### 5. Launch the Application Server
```powershell
uvicorn app:app --app-dir src/backend --reload --port 8000
```
Open **`http://localhost:8000`** in your browser to interact with the mobile-first Counter UI.

Alternatively, you can open `src/frontend/index.html` directly in any browser for standalone client testing.

---

## REST API Reference

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/prices` | `GET` | Retrieve the store owner's editable price list. |
| `/api/prices` | `POST` | Add or update an item's unit price, canonical name, or aliases. |
| `/api/extract-utang` | `POST` | Ephemeral extraction preview from spoken transcript. Never mutates ledger balances. |
| `/api/ledger/confirm` | `POST` | Commit confirmed line items to debtor balance with exact Decimal math. |
| `/api/ledger/debtors` | `GET` | List all active debtors, current outstanding balances, and last transaction timestamps. |
| `/api/ledger/reminder/{debtor_id}` | `GET` | Generate a respectful, culturally polite SMS reminder draft for manual owner dispatch. |
| `/api/ledger/payment` | `POST` | Record full or partial debt repayments against outstanding balance. |
| `/api/privacy` | `GET` | Verify RA 10173 privacy audit status and 0-day audio retention guarantees. |

---

## Benchmark Performance

Results measured across 36 spoken Taglish test utterances using `src/eval/evaluate_voice_utang.py`:

| Metric | Measured Value | Standard / Baseline |
| :--- | :---: | :---: |
| **Debtor Name Extraction Accuracy** | **94.4%** (34/36) | Target $\ge$ 90% |
| **Item SKU & Quantity Accuracy** | **94.4%** (34/36) | Target $\ge$ 90% |
| **Deterministic Price-List Match** | **94.4%** (34/36) | 100% exact math against price list |
| **Due Date Parsing Accuracy** | **100.0%** (36/36) | Relative dates (*"sa Sabado"*, *"sa kinsenas"*) |
| **Mean Local Extraction Latency** | **1.49 ms** | Sub-50ms counter response |
| **P95 Extraction Latency** | **1.68 ms** | Sub-50ms counter response |
| **End-to-End Time Saved vs Paper** | **73.4% faster** | 6.76s (Voice+Confirm) vs 25.46s (Paper Notebook) |

---

## License

This project is licensed under the MIT License — see the repository for full license details.
