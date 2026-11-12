# TindaWise — Speaker Script & Source Notes
Seven main slides · 120 seconds · Three Q&A appendix slides

## Slide 1 — 0:00–0:08 · 8 seconds
TindaWise turns spoken Taglish into a reviewable utang entry, helping sari-sari store owners record credit while keeping control.

**Sources:** README.md; src/frontend/index.html; dist/tindawise_apk_live.png

**Qualifications:** Existing Android screenshot, not a new demonstration of live AI.

## Slide 2 — 0:08–0:28 · 20 seconds
For neighborhood stores, utang depends on trust. Our interviews found two habits: Kuya Ronny relies on memory, while Ate Mina keeps a paper kwaderno. Records can be hard to recall, and complex phone workflows create another barrier.

**Sources:** data/research/sarisaristore_interview.md — Interviews 1 and 2, preliminary findings and limitations.

**Qualifications:** Two qualitative interviews; neither proves adoption, measured financial loss, or market-wide prevalence. The personas are interview respondents, not paying users.

## Slide 3 — 0:28–0:53 · 25 seconds
The owner says, “Palista kay Aling Nena dalawang Lucky Me canton saka isang sardinas.” TindaWise prepares a draft: two Canton packs at sixteen pesos and one sardines can at twenty-six—fifty-eight pesos. The owner checks the details, corrects any misheard items, then confirms to save it in the local kwaderno.

**Sources:** src/backend/ledger_engine.py — DEFAULT_PRICE_LIST, extract_utang_preview, confirmation flow; src/frontend/index.html — confirmation UI.

**Qualifications:** Editable explanatory reconstruction of the documented example, not a captured live response. ₱16 × 2 + ₱26 = ₱58. Prices are store-editable.

## Slide 4 — 0:53–1:18 · 25 seconds
Here is the AI’s role. Speech recognition supplies text. Optional Gemini extracts the customer, products, quantities, and due date. Catalog prices drive the calculation, and the owner approves the entry. A local rule-based parser provides a fallback. Cloud AI needs internet; voice availability depends on the device.

**Sources:** src/frontend/index.html — extractViaGemini, extractTaglishUtang, toggleVoiceCapture; src/backend/ledger_engine.py — _extract_via_gemini; Android MainActivity.java — speech recognition bridge.

**Qualifications:** Gemini is optional, with local mode the default. Rule-based parsing is not an on-device generative model. Speech recognition is a separate service. Cloud requests include transaction text and SKU catalog information. Extraction may be wrong; review remains essential. Python backend uses Decimal; browser implementation uses JavaScript calculations rounded to cents.

## Slide 5 — 1:18–1:35 · 17 seconds
At a noisy counter, owners can tap peso amounts instead. When a suki passes by, they can retrieve the balance and itemized history. Filipino labels, optional due dates, and owner-controlled reminders fit the familiar kwaderno workflow.

**Sources:** src/frontend/index.html — tap controls, debtor history, reminders; src/backend/ledger_engine.py — direct peso, get_debtor_history, reminders; data/research/sarisaristore_interview.md.

**Qualifications:** Feature presence is not evidence that owners find it easier. Reminders remain owner-initiated; no claim of improved repayment or dispute prevention.

## Slide 6 — 1:35–1:50 · 15 seconds
Our evidence is preliminary: two owner interviews, and thirty-four of thirty-six correct item-and-quantity extractions in the repository’s stored-transcript benchmark. That does not establish live speech accuracy or adoption. Real counter testing is next.

**Sources:** data/research/sarisaristore_interview.md; data/eval/Evaluation_Benchmark_Report.md; data/eval/sample_manifest.csv; src/eval/evaluate_voice_utang.py.

**Qualifications:** 34/36 = 94.4% rounded. This is the repository-reported local parser result, not a new evaluation or Gemini benchmark. Speaker/noise fields are metadata in the CSV; evaluator does not process recordings.

## Slide 7 — 1:50–2:00 · 10 seconds
Next, we seek store-owner partners for supervised trials measuring recording time, corrections, and ease of use. TindaWise: Tindahang maayos, suking maasahan.

**Sources:** Proposed next step based on the limitations and future research questions in data/research/sarisaristore_interview.md.

**Qualifications:** A proposed pilot, not an existing partnership or committed deployment. No funding amount, team roster, or commercial traction was established in the source material.

## Slide 8 — Appendix · Q&A only
The shipped web interface and Android wrapper use browser-side logic and local storage. The repository also includes a separate FastAPI and SQLite backend. Both offer local parsing and optional Gemini extraction.

**Sources:** src/frontend/index.html; android/app/src/main/java/ph/edu/batstateu/tindawise/MainActivity.java; src/backend/app.py; src/backend/ledger_engine.py.

**Qualifications:** Do not suggest the current web UI routes all transactions through Python Decimal. App-level audio retention statements do not establish speech-service retention behavior or legal compliance. No credentials appear in this deck.

## Slide 9 — Appendix · Q&A only
The evaluator feeds stored transcript text into the extraction engine. It measures local extraction latency and compares extracted fields with expected values. The logging-time comparison comes from timing columns already present in the manifest.

**Sources:** data/eval/Evaluation_Benchmark_Report.md; data/eval/sample_manifest.csv; src/eval/evaluate_voice_utang.py.

**Qualifications:** 73.4% = (mean paper time − mean voice+confirm time) / mean paper time × 100, rounded. Noise labels and speaker IDs do not make this an audio recognition evaluation. Due-date matching is reported as 36/36; no claim of robust generalization.

## Slide 10 — Appendix · Q&A only
This is a proposed evaluation, not an ongoing deployment. Observe owners completing representative tasks, compare against their current method, and use the results to decide what needs simplifying.

**Sources:** Proposed protocol derived from data/research/sarisaristore_interview.md — Research Limitations and Implications.

**Qualifications:** Use fictional transaction data for initial supervised sessions. Report sample size, conditions, failures, and corrections alongside any future performance claims. No real customer outreach is authorized by deck creation.

## Production handoff
Applied skill: [investor-materials](C:/Users/Lenovo/.gemini/config/plugins/ecc/skills/investor-materials/SKILL.md).
Native slide text and shapes are editable; the app screenshot is an embedded image. Slides 8–10 are Q&A material outside the two-minute script.
