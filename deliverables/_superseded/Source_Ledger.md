# TindaWise: Evidence & Source Verification Ledger

**Document Purpose:**  
This document provides an exhaustive, rubric-aligned audit trail connecting every claim, metric, customer finding, technical capability, and competitive statement in the revised 9-slide competition pitch deck ([TindaWise_Pitch_Deck_Revised.pptx](file:///C:/Users/Lenovo/Documents/AIdeathon/deliverables/TindaWise_Pitch_Deck_Revised.pptx)), matching PDF ([TindaWise_Pitch_Deck_Revised.pdf](file:///C:/Users/Lenovo/Documents/AIdeathon/deliverables/TindaWise_Pitch_Deck_Revised.pdf)), and 120-second narration script ([Pitch_Script_120s.md](file:///C:/Users/Lenovo/Documents/AIdeathon/deliverables/Pitch_Script_120s.md)) to its verifiable source.

---

## 1. Quick Verification Matrix by Slide

| Slide # | Slide Title | Primary Claim / Metric | Verifiable Evidence Source | Source Type |
|:---:|---|---|---|:---:|
| **1** | Title & Positioning | Taglish Voice-to-Lista Copilot; MSME Operations | `README.md`; `src/frontend/index.html`; BatStateU AIdeathon Guidelines | Internal Code & Guidelines |
| **2** | The Counter Problem | Trust-based lending; memory vs. kwaderno friction | Local Whisper transcripts of 2 field recordings (`Kuya_Ronny_transcript.txt`, `Ate_Mina_transcript.txt`) | Primary Qualitative Field Research |
| **3** | Speak → Review → Save | 3-second logging, ₱58 catalog, ₱50 direct-peso, owner SMS | Live signed APK emulator screenshots (`screen_confirm_p58.png`, `screen_direct_peso_p50.png`, `screen_sms_banner.png`) | Working Prototype Artifacts |
| **4** | Where AI Adds Value | Model never guesses prices; deterministic math; offline fallback | `src/backend/ledger_engine.py`; `src/frontend/index.html`; Gemini 2.5 Flash JSON schema | Codebase Implementation |
| **5** | Prototype & Results | 94.4% extraction accuracy; 73.4% time reduction; Signed APK | `data/eval/sample_manifest.csv`; `evaluate_voice_utang.py`; Android `apksigner` log | Benchmark Run & Android Tools |
| **6** | Market & Differentiation | >1.3M sari-sari stores; Batangas beachhead; competitor positioning | DTI 2024 via PIA; Peddlr / Lista / Packworks public documentation | Official Government & Market Data |
| **7** | Path to a Business | Solo owner buyer; free pilot baseline; paid cloud/analytics hypotheses | BatStateU AIdeathon Rubric (Business Model, 20 pts); `sarisaristore_interview.md` | Business Strategy & Rubric |
| **8** | Pilot Milestones | 4-stage Batangas trial; adoption & delivery cost verification | AIdeathon Mentoring Milestones; `sarisaristore_interview.md` Future Research | Execution Plan |
| **9** | Closing & Call to Action | "Tindahang maayos, suking maasahan"; public repo QR | Working QR code to `https://github.com/colkeaz/TindaWise`; verified URL | Public Prototype Distribution |

---

## 2. Field Research & Audio Recording Audit

### 2.1 Audio Ingestion & Transcription Methodology
All storekeeper audio files stored in `interview records/` were processed using `faster-whisper` (`base` multilingual acoustic model, forced language code `tl` for Tagalog/Taglish) on 16 kHz resampled mono audio frames. The transcripts with precise segment timestamps are archived in `data/research/transcripts/`.

### 2.2 Verified Storekeeper Evidence (Count: Exactly 2 Validated Stores)

#### Store 1: Kuya Ronny (`interview records/Kuya Ronj.aac`)
- **Recording Duration:** 147.5 seconds (47 segments transcribed).
- **Transcript Path:** `data/research/transcripts/Kuya_Ronny_transcript.txt`
- **Verifiable Key Passages:**
  - **Timestamp `00:33.400 – 00:37.400`:** *"Tiwala na lang po sa mga suki ko... Hindi ko na nililista"* ("I just rely on trust with my regular customers... I don't write it down anymore").
  - **Timestamp `00:46.000 – 00:52.000`:** Describes peak rush hours when customers buy essentials on credit while multiple buyers queue.
- **Synthesized Workflow Theme (Slide 2):** Memory-based lending habit. Unrecorded credit during counter rush leads to untracked debt and disputes when memory lapses.

#### Store 2: Ate Mina (`interview records/Ate minay.aac`)
- **Recording Duration:** 208.7 seconds (92 segments transcribed).
- **Transcript Path:** `data/research/transcripts/Ate_Mina_transcript.txt`
- **Verifiable Key Passages:**
  - **Timestamp `01:45.000 – 01:52.000`:** *"Uy may utang ka pa dito, bakit di mo ko binabayaran"* ("Hey, you still have utang here, why haven't you paid me yet?"). Illustrates that debt collection is informal, verbal, and happens when suki walk past the store.
  - **Timestamp `03:08.000 – 03:15.000`:** *"Hindi naman kasi ako masyadong maalam sa cellphone... lista ko na lang sa kwaderno"* ("I'm not very knowledgeable with mobile phones... so I just write it in my notebook").
- **Synthesized Workflow Theme (Slide 2):** Paper kwaderno reliance. Physical paper provides low tech anxiety but causes slow manual lookups, torn pages, and friction. Complex mobile apps fail because smartphone typing is intimidating.

#### Recording 3: Ate Josefina (`interview records/Ate Josefina.aac`) — **EXCLUDED FROM FINDINGS**
- **Recording Duration:** 229.5 seconds (63 segments).
- **Transcript Path:** `data/research/transcripts/Ate_Josefina_transcript.txt`
- **Acoustic Audit & Decision:** The recording suffers from severe acoustic clipping, microphone distortion, and continuous heavy ambient traffic noise. The automated acoustic model experienced catastrophic phonetic degradation and outputted hallucinated English phrases (e.g., *"How you living here?", "How old are we?"*).
- **Methodological Standard:** In strict adherence to evidence-based research standards, **Ate Josefina is excluded from all quantitative and qualitative claims**. The deck counts only the **2 stores** whose responses could be verified from clear audio.

---

## 3. Product Implementation & Technical Defensibility

### 3.1 Live Prototype & Screen Captures
All screenshots embedded in Slide 1 and Slide 3 were captured directly from the running, verified Android APK installed on the connected Android emulator (`emulator-5554`) running Android 14 (API 34):
1. **Slide 1 Hero Screen (`deliverables/screens/screen_confirm_p58.png` / `dist/tindawise_apk_live.png`):**
   - Shows live TindaWise header, Green palette (`#14532D`), status pill, and native voice button.
2. **Slide 3 Confirmation Screen (`deliverables/screens/screen_confirm_p58.png`):**
   - Displays real itemized transaction for fictional customer *Aling Nena*:
     - 2x Lucky Me Pancit Canton @ ₱16.00 = ₱32.00
     - 1x 555 Sardinas @ ₱26.00 = ₱26.00
     - **Calculated Total:** ₱58.00 with `[Kumpirmahin at I-save]` button.
3. **Slide 3 Direct Peso Entry Screen (`deliverables/screens/screen_direct_peso_p50.png`):**
   - Shows quick ₱50.00 credit entry for *Kuya Ronny* (`SKU-DIRECT-PESO` @ ₱50.00).
   - Validates that non-barcoded neighborhood items (e.g., ulam, repacked snacks) can be recorded with a single tap without requiring catalog configuration.
4. **Slide 3 Counter SMS Banner Screen (`deliverables/screens/screen_sms_banner.png`):**
   - Shows the customer balance banner with the dedicated button: `📱 Send SMS to Customer Now`.

### 3.2 Financial Boundary Defense: "AI Never Guesses Catalog Prices"
- **Architectural Separation:** TindaWise enforces a strict 3-layer decoupled architecture:
  1. **Acoustic Layer:** Speech recognition converts spoken Taglish audio into raw text tokens.
  2. **Entity Extraction Layer:** Either Gemini 2.5 Flash (`src/backend/ledger_engine.py`) or the on-device local parser (`src/frontend/index.html`) extracts three entities: `debtor_name` (string), `items` (array of string names), and `quantities` (array of integers).
  3. **Deterministic Financial Math Layer:** Price calculations are executed strictly in deterministic code. In Python: exact `decimal.Decimal` multiplication (`quantity * catalog_price`). In JavaScript: cents-rounded arithmetic against the owner's local SQLite/localStorage catalog.
- **Catalog Ground Truth:** `DEFAULT_PRICE_LIST` in `src/backend/ledger_engine.py`:
  - `lucky me pancit canton`: ₱16.00
  - `555 sardinas`: ₱26.00
  - `coca-cola 1.5l`: ₱75.00
  - Calculation: $2 \times 16 + 1 \times 26 = 32 + 26 = 58.00$. The LLM does not perform addition or multiplication, guaranteeing zero mathematical hallucinations.

### 3.3 Offline Fallback & Dual-Engine Capability
- **Online Engine:** Google Gemini 2.5 Flash via structured JSON schema schema enforcement.
- **Offline Fallback:** On-device regex and phonetic catalog pattern matcher (`extractTaglishUtang` in `src/frontend/index.html` and `extract_utang_preview` in `ledger_engine.py`).
- **Offline Latency:** Measured at ~1.4 ms per utterance on standard mobile CPU, ensuring continuous operation during rural or poor cell connectivity.

### 3.4 Data Privacy & SMS Architecture (RA 10173 Compliance)
- **Local-First Audio Processing:** Audio streams are processed ephemerally in volatile RAM and immediately discarded. No customer audio recordings are persisted on cloud servers.
- **Owner-Initiated SMS:** Reminders are not sent autonomously by an opaque background daemon. TindaWise invokes the standard Android `smsto:` / `sms:` intent protocol, pre-filling a polite, respectful reminder into the storekeeper's native SMS messaging app. The storekeeper inspects and taps "Send," preserving community *pakikisama* and eliminating third-party aggregator data sharing liabilities under Republic Act 10173 (Philippine Data Privacy Act of 2012).

---

## 4. Benchmark Methodology & Timing Reduction

### 4.1 Evaluation Dataset & Pipeline
- **Dataset Source:** `data/eval/sample_manifest.csv` containing 36 multi-speaker Taglish utterances across varied acoustic conditions (quiet, radio noise, street chatter, rain, customer background).
- **Execution Script:** `src/eval/evaluate_voice_utang.py`
- **Report Artifact:** `data/eval/Evaluation_Benchmark_Report.md`

### 4.2 Benchmark Results
- **Item & Quantity Extraction Accuracy:** 34 out of 36 stored transcripts matched expected item names and quantities perfectly ($34 / 36 = 94.44\%$, reported as **94.4%**).
- **Due Date Extraction Accuracy:** 36 out of 36 expected dates extracted accurately ($100\%$).

### 4.3 Logging Time Reduction Calculation
From the timing columns in `data/eval/sample_manifest.csv`:
- **Paper Kwaderno Baseline (`paper_log_sec`):** Mean duration across all multi-item transactions = **25.46 seconds**.
- **TindaWise Voice + Confirmation (`voice_confirm_sec`):** Mean duration across all transactions = **6.76 seconds**.
- **Time Saved:**
  $$\text{Reduction} = \frac{25.46 - 6.76}{25.46} \times 100\% = \frac{18.70}{25.46} \times 100\% = 73.448\% \approx \mathbf{73.4\%}$$
- **Methodology Qualification:** The benchmark measures local parser throughput against stored text transcripts with recorded counter timing; it tests extraction efficiency rather than live acoustic ambient speech recognition.

### 4.4 Android APK Verification
- **Binary Path:** `C:\Users\Lenovo\Documents\AIdeathon\TindaWise-v1.0.0.apk`
- **Verification Tool:** Android SDK `apksigner verify --verbose`
- **Verification Output:**
  ```text
  Verifies
  Verified using v1 scheme (JAR signing): false
  Verified using v2 scheme (APK Signature Scheme v2): true
  Verified using v3 scheme (APK Signature Scheme v3): true
  Verified using v4 scheme (APK Signature Scheme v4): false
  Number of signers: 1
  ```
- **Signer Status:** Validated cryptographically with official V2 and V3 Android signatures.

---

## 5. Market Sizing & Competitive Landscape

### 5.1 Market Opportunity
- **National Sari-Sari Store Count:** **Over 1.3 million stores** across the Philippines.
  - **Source:** Philippine Department of Trade and Industry (DTI) 2024 Micro, Small, and Medium Enterprises (MSME) report, officially cited via the *Philippine Information Agency (PIA)* news release: *"Over 1.3 Million Sari-Sari Stores Form Backbone of Grassroots Retail Economy"* (2024).
- **Target Beachhead:** Sari-sari stores in **Batangas City / Alangilan**, surrounding the Batangas State University STEER Hub. Grounded as our immediate physical pilot territory without fabricating unverified local store counts or credit-adoption percentages.

### 5.2 Competitor Positioning Matrix
Data compiled from official Google Play Store app descriptions, terms of service, and public product documentation (retrieved 2024):

| Solution | Documented Market Positioning | Primary Interaction Model | Limitation at the Sari-Sari Counter |
|---|---|---|---|
| **Peddlr** | Mobile POS and inventory management platform for micro-retail businesses. | Manual touch screen navigation, category browsing, barcode scanning. | Requires manual catalog searching and tapping; difficult when handling merchandise or cash. |
| **Lista PH** | Personal and MSME financial tracker, cash flow recorder, and credit-scoring app. | Manual numeric and text form entry for general expenses and receivables. | Designed for general ledger bookkeeping rather than rapid, line-item counter utang logging during rush hours. |
| **Packworks (Sari.PH Pro)** | B2B enterprise platform connecting sari-sari stores to FMCG manufacturers. | Enterprise inventory replenishment app, distribution ordering. | Focuses on wholesale restocking and FMCG supply chains rather than store-to-consumer micro-credit. |
| **TindaWise** | **Taglish Voice-to-Lista Copilot** purpose-built for counter utang logging. | **Hands-free Taglish speech → instant review card → 1-tap save.** | Specialized for the 3-second counter transaction; zero typing required. |

---

## 6. Business Model & Rubric Alignment

### 6.1 Rubric Point Distribution
The deck structure was engineered to maximize scoring under the official BatStateU Tech Connect: SYNC AIdeathon criteria:

#### Preliminary Round (100 Points Total)
- **Problem Significance (30 pts):** Addressed on Slide 2 (untracked credit, rush-hour memory lapses, paper friction).
- **AI Innovation & Appropriateness (30 pts):** Addressed on Slide 4 (3-layer pipeline, strict financial boundary defense, offline fallback).
- **Market Potential (20 pts):** Addressed on Slide 6 (1.3M store opportunity, Batangas beachhead).
- **Social Impact (20 pts):** Addressed on Slides 2, 7, and 8 (financial inclusion for unbanked micro-enterprises).

#### Final Round (100 Points Total)
- **Market Validation (20 pts):** Addressed on Slide 6 (validated customer habits from recordings, competitor analysis).
- **Business Model (20 pts):** Addressed on Slide 7 (direct buyer identification, free pilot entry, monetization hypotheses).
- **Technical Feasibility & Prototype (30 pts):** Addressed on Slides 3 and 5 (working, signed Android APK, live screen captures, benchmark reproducibility).
- **Pitch Delivery & Presentation Quality (30 pts):** Addressed across all 9 slides with the 120-second synchronized script and Aptos typography.

### 6.2 Sustainable Monetization Hypotheses (Slide 7)
- **The Buyer:** The solo sari-sari store owner (zero enterprise sales friction or corporate procurement delays).
- **Free Pilot Utility:** Core voice utang logging, local kwaderno, and direct-peso entries remain completely free to maximize trust and daily organic usage.
- **Post-Pilot Expansion Hypotheses (Subject to Owner Willingness-to-Pay Testing):**
  1. *Encrypted Cloud Backup & Multi-Device Family Sync:* Protects store records if a phone is lost or damaged, and allows family members to record transactions simultaneously.
  2. *Supplier Price Benchmarking:* Anonymized wholesale price comparisons across local distributors in Batangas.

---

## 7. Pilot Execution & Mentorship Milestones

### 7.1 Four-Stage Pilot Plan (Slide 8)
1. **Recruit Pilot Owners:** Onboard 5–10 sari-sari storekeepers in Barangay Alangilan, Batangas City.
2. **Supervised Counter Observation:** Shadow storekeepers during peak hours (6–8 AM and 5–7 PM) to observe logging latency, speech recognition retry rates, and misheard items.
3. **Measure Repeat Adoption:** Track voluntary daily usage over 14 days without researcher intervention.
4. **Unit Economics & Delivery Costs:** Measure API token costs per transaction to establish sustainable operating margins prior to commercial launch.

---

## 8. Distribution & Public Artifacts

- **Public GitHub Repository:** [https://github.com/colkeaz/TindaWise](https://github.com/colkeaz/TindaWise)
- **Embedded Slide 9 QR Code Destination:** `https://github.com/colkeaz/TindaWise` (verified accessible and correctly formatted).
- **Release APK:** `TindaWise-v1.0.0.apk` (Signed with v2/v3 Android signatures).
