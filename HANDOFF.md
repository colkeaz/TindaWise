# TindaWise — Project Handoff, Field Research Synthesis & Architecture Guide

**Tech Connect: SYNC AIdeathon (2026) | BatStateU The NEU – Alangilan**  
_Hosted by the Center for Technopreneurship and Innovation (CTI) & Center for Artificial Intelligence and Smart Technologies (CAIST)_

---

## 1. Project Context & Field Research Foundation

**TindaWise** is a human-in-the-loop, Taglish voice-and-tap *kwaderno* copilot engineered specifically for Philippine neighborhood *sari-sari* store micro-retailers.

### Why Existing Digital Ledger Apps Fail at the Counter

Our field interviews with *sari-sari* store owners ([`data/research/sarisaristore_interview.md`](data/research/sarisaristore_interview.md)) revealed that store owners operate under two distinct workflows and face adoption barriers that conventional digital bookkeeping apps (e.g., Lista PH, Peddlr) fail to address:

1. **Interview 1 — Kuya Ronny Bautista (Memory & Trust-Based Workflow):**
   - **Practice:** Allows both regular buyers (*suki*) and non-regular neighbors to borrow on credit based on personal judgment and trust. He does not maintain a formal written record of debts and waits for customers to pay voluntarily.
   - **Problem:** Without written records, transactions can be forgotten or difficult to verify.
   - **Reaction to App:** Conditionally receptive—especially because it helps keep records when someone forgets a transaction—provided recording is effortless and supports rather than replaces personal trust.
2. **Interview 2 — Ate Mina (Paper *Kwaderno* & Selective *Suki* Workflow):**
   - **Practice:** Selectively lends to trusted, regular customers (*suki*) who are likely to repay. She writes down debts in a paper notebook (*kwaderno*) and reminds customers **face-to-face** when they visit or pass by the store:
     > *"Uy, may utang ka pa dito. Bakit 'di mo ako binabayaran?"*
   - **Problem:** Customers genuinely forget they still have an outstanding debt, and checking old paper records for long-overdue balances is inconvenient.
   - **Reaction to Conventional App Pitch:** Hesitant when pitched a standard mobile app requiring manual typing of items, payment deadlines, and automated notifications. She explicitly noted that she is unfamiliar with complex cellphone applications and prefers her established written *kwaderno*.

### How TindaWise Solves Both Workflows

$$\text{Spoken Taglish or 1-Tap Peso/Item} \longrightarrow \text{Entity / Peso Extraction} \longrightarrow \text{Deterministic Math} \longrightarrow \text{Owner Confirmation} \longrightarrow \text{Local Kwaderno Ledger}$$

- **For Kuya Ronny:** A **3-second Push-to-Talk Taglish voice button** and **Direct Peso-Amount Logging (`SKU-DIRECT-PESO`)** allow him to say *"Palista kay Kuya Ronny singkwenta pesos na ulam"* (or tap `+₱50`) so transactions are never forgotten—without writing in a notebook or setting up complex SKUs.
- **For Ate Mina:** **Simple Kwaderno Mode** strips away technical menus in favor of oversized Filipino-first buttons, optional due dates (*"Kapag nakaluwag"*), `Suki` trust badges, an instant **Walk-By Counter Search**, an **Itemized History Modal** (to show customers who forgot *what* and *when* they borrowed), and an on-screen **Face-to-Face Reminder Script (*Harapang Paalala*)**.

---

## 2. Repository Architecture & Codebase Map

```text
.
├── .gitignore                         # Standard Python, SQLite, environment & handoff ignores
├── requirements.txt                   # FastAPI, Uvicorn, Pydantic runtime dependencies
├── README.md                          # Primary repository documentation, research summary & quickstart
├── HANDOFF.md                         # This architecture, field research & competition defense guide
├── data/
│   ├── eval/
│   │   ├── sample_manifest.csv        # 36-utterance Taglish evaluation dataset across 6 speakers & 4 noise conditions
│   │   └── Evaluation_Benchmark_Report.md  # Detailed benchmark & interview scenario report
│   └── research/
│       └── sarisaristore_interview.md # Field interview findings & engineering traceability (Kuya Ronny & Ate Mina)
├── src/
│   ├── backend/
│   │   ├── app.py                     # FastAPI REST API server (CORS, endpoints, HTML serving)
│   │   └── ledger_engine.py           # SQLite database schema, price list, direct peso parser & Decimal math
│   ├── eval/
│   │   └── evaluate_voice_utang.py    # Automated accuracy, latency & field-scenario benchmark suite
│   └── frontend/
│       └── index.html                 # Filipino-first Simple Kwaderno Mode, Voice Capture & Offline Sync
└── tests/
    └── test_ledger_engine.py          # 7 unit tests verifying pricing safety, direct peso utang, history & privacy
```

---

## 3. Core Architectural Guardrails & Interview Traceability Matrix

| Research Theme / Implication | Guardrail / Feature | Implementation in Codebase | Why It Matters |
| :--- | :--- | :--- | :--- |
| **Implication #1 & #6:** Fast debt recording & optional item details | **Direct Peso-Amount Utang (`SKU-DIRECT-PESO`) + Catalog Matching** | `_parse_direct_peso_utang()` in `ledger_engine.py` + `+₱5` to `+₱100` quick chips in `index.html`. Catalog items strictly use `price_items` via `Decimal("0.01")`. | Store owners can record quick peso amounts (*"singkwenta pesos"*) without configuring a full SKU catalog first, while catalog items never hallucinate prices. |
| **Theme 4 & Implication #5:** Tech unfamiliarity & accessible interface | **Filipino-First Simple Kwaderno Mode + Judge Demo Toggle** | `toggleUiMode()` in `index.html` defaults to large Tagalog buttons (*"1. Maglista ng Utang"*, *"2. Listahan ng May Utang"*), hiding developer metrics unless toggled. | Directly addresses Ate Mina's hesitation toward complex English/typing-heavy mobile apps. |
| **Theme 1:** Central role of trust in lending decisions | **Relationship Trust Badges (`Suki` vs. `Kakilala`)** | `trust_tag` column in SQLite `debtors` table (`ledger_engine.py`) and selector in `index.html`. | Reflects Ate Mina's selective *suki* lending and Kuya Ronny's flexible neighbor lending without requiring invasive personal IDs. |
| **Theme 3 & Implication #2 & #3:** Informal face-to-face collection & forgotten debts | **Walk-By Counter Search, Itemized History & *Harapang Paalala* Script** | `GET /api/ledger/debtors/{id}` (`get_debtor_history`) and `face_to_face_script` in `draft_manual_reminder()`, plus optional due dates (*"Walang tiyak na petsa"*). | Supports Ate Mina's face-to-face reminders when customers walk by the store and resolves disputes when customers forget old debts. |
| **Implication #4:** Offline functionality | **Local SQLite + Automatic Browser `localStorage` Sync** | `TindaWiseEngine` runs 100% locally in SQLite; `index.html` caches prices, debtors, and history in `localStorage` for zero-internet fallback. | Guarantees 100% availability even when mobile data is unavailable at the store counter. |
| **Safety & Privacy Guardrails** | **Human-in-the-Loop Confirmation & RA 10173 0-Day Audio Privacy** | `POST /api/extract-utang` never mutates SQLite; `POST /api/ledger/confirm` requires `owner_confirmed=True`. Audio bytes are deleted immediately after STT. | Store owners retain 100% control over balances and reminders; zero automated debt harassment. |

---

## 4. Competition Pitch & Judge Q&A Defense Guide

When presenting the interview findings from [`data/research/sarisaristore_interview.md`](data/research/sarisaristore_interview.md) to judges, use the following evidence-backed framing:

1. **How to Frame Ate Mina's Hesitation (Turning a Research Hurdle into Your Strongest Design Proof):**
   - *Judge Question:* *"In your second interview, Ate Mina said she was hesitant to use a mobile app and preferred her paper records. Doesn't that invalidate your app?"*
   - *Defense Answer:* *"Ate Mina's reaction is our most important finding. During the interview, she was pitched a conventional app: manual tap entry of items, strict payment deadlines, and automatic notifications. She rejected that because typing on a phone is intimidating for her and she collects debts face-to-face when her suki walk by. That exact insight is why we engineered TindaWise differently: (1) zero-typing Taglish voice capture and 1-tap peso buttons in a familiar Filipino 'Simple Kwaderno Mode', (2) optional due dates instead of rigid deadlines, and (3) instant walk-by itemized history so when a suki passes her window and forgets they owe money, she can show the exact date and items in one tap."*
2. **How to Frame Kuya Ronny Bautista's Workflow:**
   - *Defense Answer:* *"Kuya Ronny represents store owners who lend on trust and memory without writing anything down because paper logging is tedious during store hours. He saw value in an app specifically for remembering transactions when someone forgets. Our 3-second Push-to-Talk and direct peso logging ('Palista kay Kuya Ronny singkwenta pesos') give him a written record with zero writing friction."*
3. **Transparency on Research Limitations (*Ate Josefina.aac*):**
   - As documented in `data/research/sarisaristore_interview.md`, two full interviews (*Kuya Ronny Bautista* and *Ate Mina*) were analyzed in depth, while a third recording (*Ate Josefina.aac*) had unrecoverable spoken audio and was excluded to maintain strict research integrity rather than fabricating responses.

---

## 5. Verification & Testing Playbook

### Running Unit Tests (7 / 7 Passing)

Verifies that extraction previews never alter balances, catalog prices are strictly enforced, direct peso utang (`SKU-DIRECT-PESO`) and itemized debtor history work accurately, and partial payments calculate with exact `Decimal` precision:

```powershell
python -m unittest tests/test_ledger_engine.py -v
```

### Running the Empirical Benchmark & Field Scenario Suite

Evaluates 36 multi-speaker Taglish utterances under 4 counter noise conditions (`quiet_counter`, `electric_fan`, `street_tricycle`, `radio_chatter`) plus the field interview scenarios:

```powershell
python src/eval/evaluate_voice_utang.py
```

**Measured Benchmark Results:**

- Debtor Name Accuracy: **94.4%** (34/36)
- Item & Quantity Extraction: **94.4%** (34/36)
- Deterministic Total Match: **94.4%** (34/36)
- Due Date Extraction: **100.0%** (36/36)
- Direct Peso-Amount Extraction (Kuya Ronny / Ate Mina scenarios): **100.0%**
- Median Extraction Latency (`p50`): **~1.5 ms**
- Time Saved vs Paper Notebook: **73.4%** faster (6.76s vs 25.46s)

### Running the Live Counter Server

```powershell
uvicorn app:app --app-dir src/backend --reload --port 8000
```

Then navigate to `http://localhost:8000` in any web or mobile browser.
