# TindaWise — Agent Continuation Briefing

Updated: 2026-11-12, Asia/Singapore. Workspace: `C:/Users/Lenovo/Documents/AIdeathon`.

## Goal and exact stopping point

Improve the user's edited pitch deck using project documents, implementation evidence, and the newly supplied interview recordings. Deliver an editable nine-slide PowerPoint, matching PDF, and synchronized two-minute speaker notes. The latest nine-slide plan was developed but **has not been implemented**. The immediate user request was to write this continuation briefing, not execute that plan.

The initial deck was created and checked earlier in this conversation. The user subsequently edited it and supplied an extensive critique asking for market potential, competitive positioning, a business model, stronger benchmark presentation, and evidence of the working Android APK. Resume from these edits, not the original generator output.

## User decisions — preserve these

- Nine slides, two minutes total; informative and concise so judges understand the problem, solution, and role of AI.
- Deliver PowerPoint and PDF, with speaker notes. Use English narration with natural Taglish examples, as in the current deck.
- Use **summarized interview findings**, rather than direct quotes, named respondents, or audio clips.
- **Leave team credits off.** Do not invent members, roles, adviser, contact details, or credentials.
- **Free pilot first.** Validate demand and willingness to pay before proposing prices or committed rollout dates. The critique's ₱49/month, ₱499/year, 15-store pilot, Bluetooth printing, and dated rollout were suggestions, not approved commitments.
- User rejected both offered visual-style choices without specifying another. Preserve their clean green design and tagline closing; make content-driven improvements without claiming they approved a full redesign.
- Do not re-ask the above decisions. Do not publish, push, send messages, or make a repository public as part of deck creation.

## Current files and source-of-truth warning

| Path | Status / purpose |
|---|---|
| `deliverables/TindaWise_Pitch_Deck.pptx.pptx` | **Newest discovered deck:** 518,222 bytes, modified Nov 12 at 20:28:44. Seven slides. Treat as the presumptive latest user edit; inspect its visuals first. |
| `deliverables/TindaWise_Pitch_Deck.pptx` | Edited seven-slide deck, 216,778 bytes, modified at 20:03:33. Previously rendered and reviewed. |
| `deliverables/TindaWise_Pitch_Deck.pdf` | **Stale:** original ten-slide export from before user edits. |
| `deliverables/TindaWise_Speaker_Notes.md` | **Stale:** original ten-slide script and notes. |
| `deliverables/previews/` | **Stale:** original ten-slide renders. Do not treat as current PPTX previews. |
| `deliverables/build_deck.py` | Original ten-slide generator. Running it unmodified will overwrite user edits. |
| `deliverables/export_deck.ps1` | Working PowerPoint COM exporter, currently targets the original filename and previews folder. Parameterize for revised outputs. |
| `deliverables/verify_deck.py` | Original verification; hardcodes ten slides. Must be adapted for nine slides and revised filenames. |
| `deliverables/verification.json` | Historical verification only; not valid for edited decks. |
| `HANDOFF.md` | Existing project/research/architecture document. Preserved; this briefing does not replace it. |
| `handoff/competition/AIdeathon_Guidelines.md` | Competition rubric, requirements, dates. Hidden from normal rg enumeration by ignore rules. |
| `handoff/proposals/TindaWise_Project_Proposal.md` | Proposal, some stronger claims than code supports; cross-check rather than copy blindly. |
| `handoff/competition/MASTER_PLAN.md` | Historical strategy and alternate concepts; includes speculative/unsupported numerical claims. |
| `TindaWise_2_Minute_Pixar_Pitch_Plan.docx` | Original story direction; contains dramatizations and overclaims that require correction. |
| `data/research/sarisaristore_interview.md` | Existing summaries of two interviews; explicitly excludes usable findings from Josefina due to extraction uncertainty. |
| `data/eval/Evaluation_Benchmark_Report.md` | Reported benchmark results; use with evaluator and CSV. |
| `data/eval/sample_manifest.csv` | 36 transcript samples and prefilled logging-time columns. |
| `src/eval/evaluate_voice_utang.py` | Demonstrates what is actually measured and the rounding convention. |
| `src/frontend/index.html` | Actual browser UI, local parser, optional Gemini, confirmation, SMS banner, localStorage. |
| `src/backend/ledger_engine.py`, `src/backend/app.py` | Separate FastAPI/SQLite implementation with Decimal arithmetic and local/template reminder generation. |
| `android/app/src/main/java/ph/edu/batstateu/tindawise/MainActivity.java` | Android WebView, device speech recognition, native SMS bridge. |
| `android/app/src/main/assets/index.html` | Packaged frontend copy; compare with source before claiming APK matches current source. |
| `android/build_apk.py` | Existing build/sign/verify pipeline. Avoid rebuilding just to produce deck evidence unless necessary. |
| `dist/tindawise_apk_live.png` | Existing actual Android screenshot. |
| `TindaWise-v1.0.0.apk`, `dist/TindaWise-v1.0.0.apk` | Existing app packages. Verify signature before calling them signed in revised materials. |

Both PPTX files were inspected as OOXML and contain substantially the same seven-slide text. The newer double-extension file was **not visually rendered** during this session; its different file size may reflect image/layout changes. Do not assume identical visuals. Older user-edited deck removes recurring header/footer text, simplifies slide 6, and replaces pilot closing with a large TindaWise tagline. The older file's slide 7 notes still discuss a pilot although the visible slide is only the brand/tagline.

## Interview recordings — still to process

Files exist under `interview records/`:

- `Kuya Ronj.aac` — approximately 4.77 MB.
- `Ate minay.aac` — approximately 6.75 MB.
- `Ate Josefina.aac` — approximately 7.42 MB.

**Recordings have not been listened to or transcribed in this session.** Existing documents call people Kuya Ronny and Ate Mina, which differs from filenames. Since the user selected anonymous summaries, do not guess identities or treat three files as three validated respondents automatically.

Suggested execution: install an isolated local faster-whisper environment, use a multilingual model (large-v3-turbo with CPU int8 is a reasonable starting point), preserve timestamped segments, and review the passages supporting each theme. Use Tagalog/Taglish, do not force English transcription. Separate interviewer-proposed features from spontaneous respondent needs. Mark unintelligible passages; do not fill gaps. Store transcripts and a concise evidence mapping under `data/research/`, keeping recordings untouched. Put only anonymized findings in the deck.

Environment last checked: no `OPENAI_API_KEY` configured; `openai`, `whisper`, and `faster_whisper` were not installed in the default Python. `torch` is installed. No ffmpeg/ffprobe command was found on PATH; faster-whisper uses PyAV and does not require a separate FFmpeg executable. No Whisper model cache was found. Recheck environment before installing anything. Downloads/installations were not performed for transcription during the planning phase.

## Verified facts and important claim boundaries

- Default catalog example: 2 × Canton at ₱16 plus 1 × sardines at ₱26 = **₱58**.
- Source supports direct-peso entries, fractional quantities, editable previews, owner confirmation, history, payments, and owner-controlled SMS handoff.
- Speech recognition is supplied by Android/browser services. Cloud Gemini extraction is optional. The local fallback is a **rule-based parser**, not a local generative LLM. Default web mode is local.
- AI extracts transaction fields; catalog prices come from the owner's catalog. Extraction can still select the wrong customer, SKU, or quantity. Owner confirmation reduces risk but does not make errors architecturally impossible.
- Python backend uses Decimal; browser/Android frontend uses JavaScript calculations rounded to cents and localStorage. Do not imply the shipped WebView sends every transaction through Python/SQLite.
- Reminder text is **template-based** in the current code, not a demonstrated third generative-AI layer. Native SMS opens for owner review/send; no automatic bulk collection.
- Fully offline voice and certified RA 10173 compliance were not established. App-level no-audio-storage intent does not establish third-party speech-service behavior. Avoid blanket compliance or zero-error claims.
- Repository reports **34/36 = 94.4%** item-and-quantity matches and the same name accuracy. Evaluator consumes stored transcript strings, not raw audio. Noise/speaker labels are CSV metadata, not proof of live noise robustness or six-speaker audio testing.
- Logging-time columns average to 25.458333… seconds (paper) and 6.755555… seconds (voice+confirm). Evaluator rounds means first: **25.46 and 6.76**, then computes **73.4%** reduction. Using unrounded means yields 73.5%; preserve the evaluator's convention and state provenance.
- Timing collection protocol was not established. Present 73.4% as a **reported benchmark using supplied timing data**, not newly verified field performance.
- Do not claim 100% post-confirmation accuracy across 36 cases: the evaluator does not establish that result. Catalog arithmetic is a design property distinct from extraction correctness.
- Do not use unverified 5 PM scenes, wet hands, 6–8 competitor taps, lost-capital percentages, 90% credit penetration, or 5,000 local stores as measured research facts.

## Rubric and external research

From `handoff/competition/AIdeathon_Guidelines.md`:

| Preliminary | Points | Final | Points |
|---|---:|---|---:|
| Problem Statement | 30 | Problem and Impact | 20 |
| Innovation & AI Integration | 30 | AI Innovation and MVP | 25 |
| Market Potential | 20 | Market Validation | 20 |
| Impact | 20 | Business Model | 20 |
| | | Pitch Delivery | 15 |

The critique's assertion that business/market account for 40 points in **both** rounds is incorrect; 40 applies to final-round market validation + business model. Guidelines list four students and one adviser as team eligibility requirements, but user explicitly chose to omit credits from slides. Do not invent an official named track; proposal describes MSME Operations as its domain.

Sources already inspected online (verify again if needed, put citations and access dates in notes):

- Market: https://pia.gov.ph/news/dti-ncro-chief-supports-growth-of-sari-sari-store-owners/ — reports DTI recorded **over 1.3 million Philippine sari-sari stores in 2024**. Attribute date/source; not a paying-customer count or validated serviceable market.
- Peddlr: https://www.peddlr.io/en/about — POS, inventory, sales, reports, cash/credit ledger. Do not claim barcode-only input or lack of credit tracking.
- Lista: https://www.lista.com.ph/copy-of-home — sales, expenses, receivables; advertises automatic SMS reminders. Treat this page as its published business offering; don't infer its entire current product from one page.
- Packworks: https://packworks.io/ — connected commerce/mobile ecosystem and store tools. Compare documented focus rather than asserting absence of competitor features.
- Source remote: `https://github.com/colkeaz/TindaWise.git`. Public browsing of https://github.com/colkeaz/TindaWise returned **404**. Could be private; do not label it deleted. Do not add a judge-facing QR until destination works anonymously; don't change visibility or publish a release without authorization.

## Agreed implementation direction: nine slides / 120 seconds

| # | Slide | Content | Time |
|---|---|---|---:|
| 1 | TindaWise | Taglish Voice-to-Lista Copilot; actual app screenshot; MSME positioning, no team credits. | 8s |
| 2 | Counter problem | Anonymous, verified memory/paper workflows and recording/retrieval friction. | 16s |
| 3 | Speak → Review → Save | Real ₱58 confirmation screenshot; compact ₱50 direct-peso example and owner-controlled SMS handoff. | 22s |
| 4 | Where AI adds value | Speech → extraction → catalog calculation → owner approval; optional Gemini and rule-based fallback. | 18s |
| 5 | Prototype and results | APK; 94.4% transcript item/quantity matches; reported 73.4% timing reduction with short methodology labels. | 13s |
| 6 | Market and differentiation | Dated national opportunity, Batangas starting segment, compact sourced competitor positioning. | 16s |
| 7 | Path to a business | Owner as prospective buyer; direct onboarding; free pilot; test demand for future backup/family access. | 13s |
| 8 | Pilot and milestones | Recruit → observe representative tasks → assess repeat use → evaluate willingness to pay and delivery costs. | 8s |
| 9 | Closing | Preserve large TindaWise name/tagline; invite trying Android prototype. QR only if accessible. | 6s |

Target approximately 240–260 narration words. Keep detailed methodology, architecture, competitor sources, and rubric mapping in notes/supporting Markdown. Do not restore the deleted appendix to the main deck. Optional paid features are hypotheses, not implemented capabilities; no committed price, pilot count, revenue, partner, or dated rollout.

## Ordered work for the next implementation agent

1. Read this file, inspect the **newest double-extension PPTX visually**, and preserve both existing PPTX files. Use a new revised filename (e.g. `TindaWise_Pitch_Deck_Revised.pptx`). Do not run the old generator first.
2. Read applicable skills and required references below. Review recordings and create the timestamped transcript/evidence summary. Decide which anonymous themes can actually be used based on evidence, not the older narrative.
3. Reconcile source claims into one evidence ledger. Use the newest code for implemented behavior, artifacts for reported metrics, and dated external citations for market/competition. Historical proposals contain conflicting latency figures and stronger claims than implementation supports.
4. Verify APK signature and launch existing app on emulator. Capture real confirmation/direct-peso/SMS banner screens with fictional data. The critique's `tindawise_voice_computed.png` and `tindawise_sms_banner.png` were **not found**. Capture them rather than pretending they exist. Demonstrate draft SMS without sending a message.
5. Edit from the user's newest deck, preserving its visual choices and native editable text/shapes. Build the nine-slide narrative above. Update the generator so later runs reproduce the revised result without restoring old content. Prefer surgical edits to original package/native shapes over screenshot-only slides.
6. Rewrite notes for every slide, especially the current closing, and generate matching Markdown notes. Include sources, limitations, future-feature labels, and actual timings. Update file arguments and slide-count assumptions in export/verification scripts.
7. Export revised PDF and fresh previews. Inspect every slide, fix overlaps/wrapping/screenshot legibility, then check slide count/text parity, note consistency, ₱58 arithmetic, 120-second schedule, script word count, and any QR link. A timing schedule is not a timed rehearsal; report honestly.
8. Deliver revised PPTX/PDF/notes plus a brief evidence/changes summary. Preserve user originals and source recordings. No application code changes are necessary for the deck task.

## Tools, working commands, and known failures

- Shell is PowerShell; workspace is Windows. Python default is `C:/Python314/python.exe`. `.pitch-deps/` contains python-pptx, Pillow, pypdf and associated dependencies installed for the original deck. Use `sys.path.insert(0, str(ROOT / '.pitch-deps'))` for existing helper scripts. For speech tooling, an isolated compatible Python environment may be needed.
- PowerPoint is installed at `C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE`. Original exporter successfully uses COM: `Presentations.Open(path, $true, $false, $false)`, then `SaveAs(pdfPath, 32)` and `Export(previewFolder, 'PNG', 1600, 900)`. Always close the opened presentation and quit the COM instance in finally.
- `ExportAsFixedFormat($pdfPath, 2)` failed with `Cannot convert the "2" value of type "int" to type "Object".` Use the proven SaveAs route.
- Original managed sandbox caused Python-library read PermissionError and PowerPoint `80070520` logon-session errors. Permissions later changed to unrestricted/no approvals. Recheck current policy; do not blindly reintroduce escalation flags.
- A temporary `.deck-deps/` installation was removed. Do not rely on it. `.pitch-deps/` remains.
- Original verification passed ten-slide PDF/PPTX parity and 241 narration words before user edits. Its shape-bounds assertions do not prove text-fit or absence of overlaps; visual inspection remains necessary.
- UTF-8 DOCX extraction: use `python -X utf8` with zipfile/OOXML. Default cp1252 previously failed on peso characters.
- Inspect ignored material with `rg --files --no-ignore handoff`. Ordinary `rg --files` omitted the important competition/proposal files.
- Android SDK: `C:/Users/Lenovo/AppData/Local/Android/Sdk`. Last read-only `adb devices -l` showed connected `emulator-5554`. Build tools `36.0.0/apksigner.bat` exist. Read Android interaction references before UI actions. Never expose signing secrets or API keys in logs.
- Git status at handoff: `.pitch-deps/`, `deliverables/`, and `interview records/` were untracked. No source code was changed for deck production. Do not assume these files are committed or available on GitHub.
- Review-only PNGs for the older seven-slide edited file exist in `C:/Users/Lenovo/AppData/Local/Temp/TindaWise-edited-deck-review`; these are temporary and not previews of the newest double-extension deck.

## Skills discovered and consulted

Project instruction: at project start read `C:/Users/Lenovo/SKILLS_CATALOG.md`, run `python C:/Users/Lenovo/search_skills.py "<keyword>"`, prefer harness-exposed duplicates, read selected SKILL.md, and cite applied skills in handoff. Catalog/helper were read and searched for pitch deck, presentation, and transcription. GitHub skill search was explicitly requested and performed. No new global skills were installed.

- **Investor materials** — applied for claim consistency and deck structure: `C:/Users/Lenovo/.codex/plugins/cache/ecc/ecc/2.2.3/skills/investor-materials/SKILL.md` (initial session used the equivalent `.gemini/config/plugins/ecc/skills/investor-materials/SKILL.md`).
- **PPTX editing** — read from official GitHub: https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md . Editing guidance favors preserving existing package/layout, native formatting, relationship/schema checks, and full visual QA. Consult current full skill and relevant scripts before implementation; don't assume files were installed locally.
- **Android CLI** — read for screenshot/interaction planning: `C:/Users/Lenovo/.codex/skills/android-cli/SKILL.md`. Required before device UI operations: `references/interact.md`; before journey testing: `references/journeys.md`.
- **Transcribe** — discovered/read: https://github.com/openai/skills/blob/main/skills/.curated/transcribe/SKILL.md . Its OpenAI API path requires a configured key, absent when checked. Do not request secrets in chat. Local alternative documentation: https://github.com/SYSTRAN/faster-whisper . No recording transcription has run yet.
- **Handoff** — applied to this briefing: `C:/Users/Lenovo/.codex/plugins/cache/claude-mem-local/claude-mem/13.35.0/skills/handoff/SKILL.md`. Used `AGENT_HANDOFF.md` to preserve the existing project `HANDOFF.md`.
- **Wowerpoint** — inspected but not selected: NotebookLM single-document generated PDF workflow does not fit preservation of this editable PPTX and multiple evidence sources. No NotebookLM upload or generation was performed.

## Memory and restart

The claude-mem search `TindaWise pitch deck interviews` scoped to `AIdeathon` returned a retrieval failure during this handoff. No observation IDs were obtained; do not assume durable memory contains this context. This Markdown is the concrete continuation source. Re-run memory search if helpful, using the required mem_search index → context → details flow.

Suggested next-session instruction: **Read AGENT_HANDOFF.md, inspect the latest edited PowerPoint, and continue the nine-slide pitch improvement plan.**
