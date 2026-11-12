# TindaWise — Taglish Voice-to-Lista & Simple Kwaderno Copilot
**Human-in-the-Loop Counter *Utang* Ledger for Philippine Sari-Sari Stores**  
*Tech Connect: SYNC AIdeathon (2026) — Batangas State University The NEU – Alangilan*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/framework-FastAPI-teal.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Privacy: RA 10173](https://img.shields.io/badge/Compliance-RA%2010173%20(0--Day%20Retention)-success.svg)](#core-design--safety-guardrails)
[![Deterministic Math](https://img.shields.io/badge/Ledger-100%25%20Exact%20Decimal-blueviolet.svg)](#core-design--safety-guardrails)
[![Field Validated](https://img.shields.io/badge/Field%20Research-Sari--Sari%20Owner%20Interviews-orange.svg)](#field-research--user-validation-sarisaristore_interviewmd)

---

## Overview

In the Philippines, neighborhood *sari-sari* stores serve over 90% of households. Our field interviews with neighborhood store owners ([`data/research/sarisaristore_interview.md`](data/research/sarisaristore_interview.md)) revealed that store owners do not all manage customer credit (*utang*) the same way—they fall into two distinct operational workflows, both underserved by conventional mobile apps:

1. **Memory & Trust-Based Lenders (e.g., *Kuya Ronny Bautista*):** Allow both regular (*suki*) and familiar customers to borrow based on personal trust without maintaining formal written records. Without records, transactions can be forgotten or difficult to verify, yet writing every small transaction down takes too much effort.
2. **Paper *Kwaderno* & Selective *Suki* Lenders (e.g., *Ate Mina*):** Lend selectively to trusted regulars, write debts in a paper notebook (*kwaderno*), and remind customers **face-to-face** when they pass by the store (*"Uy, may utang ka pa dito. Bakit 'di mo ako binabayaran?"*). Customers frequently forget what or when they borrowed. Crucially, owners like Ate Mina **reject conventional mobile apps** because they are unfamiliar with complex cellphone menus, dislike typing item details, and prefer personal reminders over rigid automated payment deadlines.

**TindaWise** bridges both workflows by combining a **3-second spoken Taglish voice copilot** (for effortless recording without writing or typing) with a **Filipino-first Simple *Kwaderno* UI** (for paper-like familiarity, 1-tap quick peso logging, and instant face-to-face counter lookup):

$$\text{Spoken Taglish or 1-Tap Peso/Item} \longrightarrow \text{Entity / Peso Extraction} \longrightarrow \text{Deterministic Math} \longrightarrow \text{Owner Confirmation} \longrightarrow \text{Local Kwaderno Ledger}$$

> **Example 1 — Itemized SKU Voice Entry:**  
> *"Palista kay Aling Nena dalawang Lucky Me canton saka isang sardinas, sa Sabado bayad."*  
> Within **~1.5 ms**, TindaWise extracts the debtor (`Aling Nena`), matches the store's price list (`2x Lucky Me Pancit Canton @ ₱16.00 = ₱32.00`, `1x Sardinas @ ₱26.00 = ₱26.00`), computes the exact total (`₱58.00`), and displays an editable confirmation card.
>
> **Example 2 — Fast Direct Peso Entry (No SKU Setup Needed — Kuya Ronny / Ate Mina Workflow):**  
> *"Palista kay Kuya Ronny singkwenta pesos na ulam"* (or tapping **`+ ₱50`** in Simple Kwaderno Mode)  
> Immediately creates a `₱50.00` `Pautang (Ulam)` confirmation line with optional due date (`Walang tiyak na petsa / Kapag nakaluwag`) and a relationship badge (`Suki` or `Kakilala`).

---

## Field Research & User Validation (`data/research/sarisaristore_interview.md`)

 Qualitative interviews conducted with *sari-sari* store owners established four research themes and six design implications that directly govern TindaWise's engineering:

### Comparative Summary of Interviewed Store Owners

| Dimension | Interview 1: Kuya Ronny Bautista | Interview 2: Ate Mina | How TindaWise Accommodates Both |
| :--- | :--- | :--- | :--- |
| **Credit Practice** *(Theme 1)* | Flexible; lends to *suki* and non-regulars based on personal judgment and trust. | Selective; lends only to trusted regular customers (*suki*) likely to repay. | **Relationship Trust Badges (`⭐ Suki` vs. `🤝 Kakilala`):** Supports both selective *suki* tracking and flexible neighbor lending without requiring formal IDs. |
| **Debt Recording** *(Theme 2)* | **Memory-based:** No consistent written record; relies on familiarity. | **Paper-based (*Kwaderno*):** Writes down debts in a notebook to avoid forgetting. | **Dual Capture (Voice + 1-Tap Kwaderno):** 3-second Push-to-Talk eliminates writing friction for Kuya Ronny; Simple Kwaderno Mode mirrors Ate Mina's paper list. |
| **Forgetting & Verification** | Transactions may be forgotten or unverified without written records. | Customers genuinely forget old balances; looking up old paper notes takes time. | **Walk-By Counter Search & Itemized History:** 1-tap lookup (`GET /api/ledger/debtors/{id}`) shows exact dates and items borrowed when a customer walks by. |
| **Payment Collection** *(Theme 3)* | Informal; generally waits for customers to pay voluntarily. | Waits or **personally reminds customers face-to-face** when they visit/pass by. | **Face-to-Face Script (*Harapang Paalala*) & Optional Due Dates:** Generates an on-screen conversational reminder script plus optional manual SMS/Messenger copy. |
| **Tech Adoption Barrier** *(Theme 4)* | Conditionally receptive if it helps remember forgotten transactions easily. | Hesitant; unfamiliar with complex mobile apps and cellphone features; prefers paper. | **Filipino-First "Simple Kwaderno Mode":** Large buttons, conversational Tagalog labels, zero technical clutter, and 1-tap Quick Peso chips (`+₱5` to `+₱100`). |

### Traceability: 6 Research Implications $\longrightarrow$ TindaWise Implementation

1. **Fast debt recording** *(Implication #1)* $\longrightarrow$ **3-Second Taglish Voice Capture + 1-Tap Quick Peso Chips (`+₱5`, `+₱10`, `+₱20`, `+₱50`, `+₱100`)** in [`index.html`](src/frontend/index.html) and `_parse_direct_peso_utang()` in [`ledger_engine.py`](src/backend/ledger_engine.py).
2. **Simple outstanding-balance list** *(Implication #2)* $\longrightarrow$ **Digital Kwaderno Ledger Tab** with instant walk-by customer search and itemized transaction history modal (`GET /api/ledger/debtors/{debtor_id}`).
3. **Optional reminders & deadlines** *(Implication #3)* $\longrightarrow$ Due dates default to *"Walang tiyak na petsa / Kapag nakaluwag"* (never mandatory), and reminders provide both a **Face-to-Face Counter Script** and manual SMS/Messenger copy (`GET /api/ledger/reminder/{debtor_id}`).
4. **Offline functionality** *(Implication #4)* $\longrightarrow$ Local SQLite database (`data/tindawise_local.db`), local deterministic Taglish parser (zero internet required), and automatic browser `localStorage` caching in [`index.html`](src/frontend/index.html).
5. **Accessible interface** *(Implication #5)* $\longrightarrow$ **Simple Kwaderno Mode** defaults to high-contrast, oversized touch buttons and natural Tagalog labels (*"1. Maglista ng Utang"*, *"2. Listahan ng May Utang (Kwaderno)"*, *"3. Presyo ng Paninda"*), with a header toggle for **Judge / Tech Demo View**.
6. **Optional customer & item details** *(Implication #6)* $\longrightarrow$ Requires only a familiar neighborhood nickname (e.g., *Aling Nena*, *Kuya Ronny*) and allows direct peso amounts (`SKU-DIRECT-PESO`) without forcing SKU catalog setup for small miscellaneous transactions.

---

## Core Design & Safety Guardrails

1. **Model Never Guesses Money:**
   - LLMs are prone to arithmetic errors and financial hallucinations. For store catalog items, TindaWise extracts **only entity tokens** (`{debtor_name, items: [{sku_id, quantity}], due_date_raw}`) and resolves unit prices strictly from the owner's editable `price_items` table using Python `Decimal(quantize="0.01")` arithmetic.
   - For non-SKU direct peso transactions (`SKU-DIRECT-PESO`), the exact spoken or tapped peso amount is parsed deterministically and requires explicit owner confirmation.
2. **Ephemeral Previews & Human-in-the-Loop Confirmation:**
   - Spoken extraction (`POST /api/extract-utang`) produces an ephemeral preview. **No database balance is altered until the store owner explicitly taps Confirm (`✅ I-save sa Kwaderno`)**.
   - If ambient noise causes a mishear (e.g., 3 cans instead of 2), the owner adjusts the quantity or price with a single tap before committing.
3. **1-Tap No-Voice Fallback & Quick Peso Mode:**
   - Philippine street counters frequently experience loud background noise (revving tricycles, street chatter, rain on tin roofs), and some store owners prefer tapping over speaking.
   - The UI includes permanent **1-Tap Customer Chips**, **1-Tap Quick Peso Buttons (`+₱5` to `+₱100`)**, and **1-Tap Product Chips**.
4. **RA 10173 (Philippine Data Privacy Act) Compliance:**
   - **0-Day Audio Retention:** Spoken audio buffers are processed ephemerally in memory and discarded immediately after transcription. No audio recordings are stored on disk.
   - **Local Nicknames Only:** Customers are identified by neighborhood nicknames (*Aling Nena*, *Kuya Jun*) with `Suki` / `Kakilala` tags rather than sensitive national IDs or legal names.
5. **Culturally Respectful, Owner-Controlled Reminders:**
   - Supports Ate Mina's preferred **Face-to-Face Reminder (*Harapang Paalala*)** when a customer walks by the counter, as well as polite Tagalog SMS/Messenger drafts that the owner reviews and sends manually. The system never sends automated background messages.

---

## Repository Structure

```text
.
├── .gitignore                         # Git exclusion rules (pycache, databases, handoff)
├── requirements.txt                   # Production dependencies (FastAPI, Uvicorn, Pydantic)
├── README.md                          # Primary project documentation, research alignment & quickstart
├── HANDOFF.md                         # Architecture handoff, interview traceability & defense guide
├── android/                           # Native Android wrapper & APK build pipeline
│   ├── app/src/main/                  # AndroidManifest.xml, MainActivity.java (Speech/SMS bridge)
│   ├── build_apk.py                   # Automated aapt2, javac, d8, zipalign & apksigner build tool
│   └── tindawise-release.jks          # V1/V2/V3 release keystore
├── dist/
│   └── TindaWise-v1.0.0.apk           # Aligned and signed installable Android application
├── TindaWise-v1.0.0.apk               # Root-level release binary ready for direct sideloading
├── data/
│   ├── eval/
│   │   ├── sample_manifest.csv        # 36-utterance multi-speaker Taglish benchmark dataset
│   │   └── Evaluation_Benchmark_Report.md  # Generated evaluation accuracy, latency & validation report
│   └── research/
│       └── sarisaristore_interview.md # Field interview findings & engineering traceability (Kuya Ronny & Ate Mina)
├── src/
│   ├── backend/
│   │   ├── app.py                     # FastAPI REST API server
│   │   └── ledger_engine.py           # SQLite schema, price list, direct peso parser & Decimal ledger math
│   ├── eval/
│   │   └── evaluate_voice_utang.py    # Multi-speaker evaluation & field-scenario benchmark harness
│   └── frontend/
│       └── index.html                 # Filipino-first Simple Kwaderno UI, Voice Capture & Offline Sync
└── tests/
    └── test_ledger_engine.py          # Unit tests verifying pricing safety, direct peso utang, history & privacy
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
Verifies all 7 core guarantees: model never guesses catalog prices, unconfirmed previews never mutate balances, noisy-counter owner corrections, tap fallback & partial payments, RA 10173 0-day audio privacy, direct peso-amount utang (`SKU-DIRECT-PESO`), and itemized debtor history with face-to-face reminder scripts:
```powershell
python -m unittest tests/test_ledger_engine.py -v
```

### 4. Run the 36-Utterance Taglish Benchmark
Evaluates extraction accuracy and execution latency across 36 spoken Taglish utterances with 6 speakers and 4 counter noise conditions (`quiet_counter`, `electric_fan`, `street_tricycle`, `radio_chatter`), plus field interview validation scenarios:
```powershell
python src/eval/evaluate_voice_utang.py
```

### 5. Launch the Application Server
```powershell
uvicorn app:app --app-dir src/backend --reload --port 8000
```
Open **`http://localhost:8000`** in your browser to interact with the **Simple Kwaderno Counter UI** (and toggle **Judge / Tech Demo View** in the top header).

Alternatively, you can open `src/frontend/index.html` directly in any browser (`file://`) for standalone offline operation backed by `localStorage`.

### 6. Install or Rebuild the Native Android APK
The project includes a fully standalone, signed native Android package with on-device speech-to-text, push-to-talk, and native SMS dispatch:
```powershell
# Sideload the release APK directly to an Android phone or emulator:
adb install -r TindaWise-v1.0.0.apk

# Or recompile, package, zipalign, and sign (V2/V3) from source:
python android/build_apk.py
```

---

## REST API Reference

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/prices` | `GET` | Retrieve the store owner's editable price list. |
| `/api/prices` | `POST` | Add or update an item's unit price, canonical name, or spoken Taglish aliases. |
| `/api/extract-utang` | `POST` | Ephemeral extraction preview from spoken transcript (supports both catalog SKUs and direct peso utang). Never mutates ledger balances. |
| `/api/ledger/confirm` | `POST` | Commit owner-confirmed line items and `trust_tag` (`Suki` / `Kakilala`) to debtor balance using exact `Decimal` math. |
| `/api/ledger/debtors` | `GET` | List all active debtors, `trust_tag`, recent borrowed items preview, optional due dates, and running balances. |
| `/api/ledger/debtors/{debtor_id}` | `GET` | Retrieve full itemized transaction entries and payment logs for face-to-face ("walk-by") counter verification. |
| `/api/ledger/reminder/{debtor_id}` | `GET` | Generate both an in-person counter script (`face_to_face_script`) and a polite SMS/Messenger draft (`message_text`, `sms_uri`). |
| `/api/ledger/pay` (`/api/ledger/payment`) | `POST` | Record full or partial debt repayments against a customer's outstanding balance. |
| `/api/privacy` | `GET` | Verify RA 10173 privacy compliance and 0-day audio retention guarantees. |

---

## Benchmark Performance

Results measured across 36 spoken Taglish test utterances using `src/eval/evaluate_voice_utang.py`:

| Metric | Measured Value | Standard / Baseline |
| :--- | :---: | :---: |
| **Debtor Name Extraction Accuracy** | **94.4%** (34/36) | Target $\ge$ 90% |
| **Item SKU & Quantity Accuracy** | **94.4%** (34/36) | Target $\ge$ 90% |
| **Deterministic Price-List Match** | **94.4%** (34/36) | 100% exact math against price list |
| **Due Date Parsing Accuracy** | **100.0%** (36/36) | Relative dates (*"sa Sabado"*, *"sa kinsenas"*) & optional dates |
| **Direct Peso-Amount Extraction** | **100.0%** | Spoken Tagalog/numeric peso amounts (*"singkwenta pesos"*, *"₱25"*) |
| **Median Local Extraction Latency (`p50`)** | **~1.5 ms** | Sub-50ms counter response |
| **End-to-End Time Saved vs Paper** | **73.4% faster** | 6.76s (Voice+Confirm) vs 25.46s (Paper Notebook) |

---

## License

This project is licensed under the MIT License — see the repository for full license details.
