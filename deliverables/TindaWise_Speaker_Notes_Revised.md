# TindaWise — Speaker Notes (Revised Nine-Slide Deck)

**Runtime:** 120 seconds · **Slides:** 9 · **Language:** English narration with natural Taglish examples
**Deck:** `TindaWise_Pitch_Deck_Revised.pptx` · **PDF:** `TindaWise_Pitch_Deck_Revised.pdf`

These notes are also embedded in each slide's PowerPoint notes pane.
Interview findings are anonymized summaries, not quotes. No names, roles, or
recordings appear in the deck.

## Timing map

| # | Slide | Window | Seconds | Job |
|---|-------|--------|---------|-----|
| 1 | Cover | 0:00–0:08 | 8 | Name the product and the loop |
| 2 | Problem | 0:08–0:24 | 16 | Two owner habits, one weak point |
| 3 | Flow | 0:24–0:46 | 22 | Speak → review → save, with the ₱58 example |
| 4 | AI | 0:46–1:04 | 18 | Where AI helps and where it stops |
| 5 | Evidence | 1:04–1:17 | 13 | Working build and two benchmarks |
| 6 | Market | 1:17–1:33 | 16 | Large count, narrow entry, real competitors |
| 7 | Business | 1:33–1:46 | 13 | Buyer, free pilot, open monetization |
| 8 | Pilot | 1:46–1:54 | 8 | Four decisions, no promises |
| 9 | Closing | 1:54–2:00 | 6 | Tagline and demo invitation |

---

## Slide 1 — Cover (0:00–0:08)

> TindaWise is a Taglish voice-to-lista copilot for sari-sari stores. The owner speaks one sentence, checks the draft, and saves it.

**On screen:** Real confirmation screen from the signed Android build, fictional data.
**Say “prototype,” not “launched product.”**

## Slide 2 — Problem (0:08–0:24)

> Utang runs on trust. One owner keeps balances in memory. Another writes debts in a kwaderno. Different habits, same weak point: both depend on remembering.

**On screen:** Two anonymized habit cards.
**Guardrail:** Two qualitative interviews only. Do not generalize to all stores.

## Slide 3 — Flow (0:24–0:46)

> She speaks naturally: “Palista kay Aling Nena, dalawang Lucky Me canton saka isang sardinas, sa Sabado bayad.” The app drafts two canton at sixteen pesos, one sardinas at twenty-six, fifty-eight total. Nothing saves before she confirms.

**Arithmetic to hold:** 2 × ₱16 = ₱32; 1 × ₱26 = ₱26; total ₱58.
**Add if asked:** an item not on the price list can be logged as a direct amount, e.g. ₱50.

## Slide 4 — AI (0:46–1:04)

> Speech recognition turns Taglish into text. Extraction proposes customer, items, quantities, and due date. Prices come from her catalog, so AI never invents a peso amount. Local rules default; Gemini optional. She corrects, then saves.

**Do not claim:** 100% accuracy or fully offline voice.
**Do say:** extraction can misread a name or quantity; the review tap is the safeguard.

## Slide 5 — Evidence (1:04–1:17)

> This is the signed build. On thirty-six stored transcripts it matched items and quantities in thirty-four—ninety-four point four percent. Supplied timing shows six point eight seconds versus twenty-five point five on paper. Both are benchmarks, not field results.

**Source:** `data/eval/Evaluation_Benchmark_Report.md` (34/36 = 94.4%; 25.46s → 6.76s = 73.4%).
**Limits:** Stored transcripts, not live speech. Timing protocol undocumented. No adoption or repayment data.
**Screenshots:** Fictional data; no SMS was sent. The reminder is a draft the owner sends.

## Slide 6 — Market (1:17–1:33)

> DTI recorded over one point three million sari-sari stores nationally in 2024. A count, not an addressable market. We start in Batangas. Peddlr, Lista, and Packworks assume a POS or typed entries. Our wedge: voice-first Taglish.

**Sources (accessed Nov 2026):**
- Philippine Information Agency / DTI, 2024 sari-sari store count (1.3M+).
- Peddlr product pages: POS, inventory, sales reports, credit ledger.
- Lista product pages: sales, expenses, receivables; SMS reminders advertised.
- Packworks pages: connected store ecosystem and mobile store tools.

**Guardrail:** The 1.3M figure is national, not a serviceable market or a user count.

## Slide 7 — Business (1:33–1:46)

> The buyer is the owner-operator. We begin with a free pilot and hands-on onboarding. Monetization stays open: backup, sync, or staff access are hypotheses, not priced features.

**Do not state:** a subscription price, revenue target, store target, or partner.
**If pressed:** validation comes before pricing; the pilot tests whether owners keep using it and can name a value.

## Slide 8 — Pilot (1:46–1:54)

> The pilot is four decisions: recruit, observe real counter tasks, return after week two, test willingness to pay. No store count, price, or date is committed.

**On screen:** Recruit → Observe → Return → Decide.
**Gate:** Retention and a stated value, not download counts.

## Slide 9 — Closing (1:54–2:00)

> TindaWise: speak one utang, check the draft, save it. Tindahang maayos, suking maasahan. Thank you.

**Demo:** Offer the installed APK on the device.
**Do not show a QR code:** the public repository link returned 404 during preparation.

---

## Claim boundaries

- No claim of 100% extraction accuracy or certified RA 10173 compliance.
- No claim of offline voice recognition; only the rule-based parser is local by default.
- Reminder text is template-based and owner-sent; nothing is collected automatically.
- Interview evidence is two anonymized qualitative summaries; the third recording
  produced no transcript, so no finding is attributed to it.
- The 94.4% and 73.4% figures are benchmark results, not field outcomes.
- Screenshots use fictional customer data and were cropped to exclude the app's
  in-UI “RA 10173” badge.

## Delivery notes

- Total spoken script: **258 words** (target 240–260 for a calm 120-second pace).
- Pause points: after the ₱58 total (slide 3), after “benchmarks, not field results”
  (slide 5), and before the tagline (slide 9).
- If running long, drop the optional ₱50 direct-amount line on slide 3 and the
  “Gemini is optional” clause on slide 4; both are recoverable in Q&A.
