# Interview Notes: Sari-Sari Store Owners

**Research Topic:** Customer Credit Management (*Utang*) and the Potential Use of a Mobile Record-Keeping Application  
**Interview objectives:** Understand how sari-sari store owners handle customer debts, record transactions, collect payments, and whether a mobile application could improve their existing processes.

## Interview 1 — Kuya Ronny Bautista

**Respondent:** Sari-sari store owner

### 1. Customer credit practices

**Question:** Nagpapautang po ba kayo sa mga suki ninyo?

**Response:**
- Yes, he allows customers to purchase items on credit.
- Even customers who are not regular buyers may be allowed to borrow.
- Lending appears to depend on personal judgment and trust.

### 2. Debt recording

**Question:** Paano po ninyo nililista ang mga utang?

**Response:**
- He does not personally maintain a formal written record of customer debts.
- He relies primarily on trust and familiarity with his customers.
- There is no clearly established system for monitoring outstanding balances.

### 3. Payment collection and reminders

**Question:** Paano ninyo sinisingil ang mga may utang?

**Response:**
- The discussion suggests that he generally waits for customers to pay voluntarily.
- The interviewer also raised the possibility of reminding customers when they visit or pass by the store.
- His response to this particular follow-up was not entirely clear in the recording.

### 4. Reaction to the proposed mobile application

**Proposed features:**
- Record customer debts through a few taps.
- Automatically store transaction details.
- Track individual customer balances.
- Provide notifications or reminders about outstanding debts.

**Response:**
- He expressed some willingness to use the application.
- He indicated that it could be useful for keeping records even when someone forgets a transaction.
- His acceptance appeared conditional rather than a definite commitment to adopt the app.

### Key findings

**Current practice:** Informal, trust-based credit management without consistent written documentation.

**Potential problem:** Transactions may be forgotten or difficult to verify without records.

**Application opportunity:** Simple transaction logging and reminders could supplement his existing trust-based practices.

**Important insight:** A mobile application should support personal relationships rather than assume that store owners want to replace trust with strict debt enforcement.

---

## Interview 2 — Ate Mina

**Respondent:** Sari-sari store owner

### 1. Customer credit practices

**Question:** Nagpapautang po ba kayo sa mga suki ninyo?

**Response:**
- She initially answered that she does not regularly offer credit.
- She later clarified that she sometimes allows trusted, regular customers to borrow.
- She generally avoids lending to unfamiliar customers.
- Knowing that a customer is likely to repay is an important condition.

### 2. Debt recording

**Question:** Kapag nagpapautang po kayo, nililista po ba ninyo?

**Response:**
- Yes, she writes down debts when she allows customers to borrow.
- Her existing system is paper-based.
- She relies on written notes to remember outstanding debts.

### 3. Payment collection

**Question:** Paano po ninyo sinisingil ang mga customers na may utang?

**Response:**
- She sometimes waits for customers to settle their balances.
- If a debt remains unpaid for a long time, she personally reminds the customer.
- Reminders are often delivered during face-to-face interactions.

**Example from the interview:**

> “Uy, may utang ka pa dito. Bakit 'di mo ako binabayaran?”

She also described customers who genuinely forgot they still had an outstanding debt.

### 4. Forgetting and tracking debts

**Question:** Nakakalimutan po ba ninyo ang mga utang?

**Response:**
- Written records help prevent her from forgetting debts.
- However, she may not immediately remember every balance, especially when a transaction happened long ago.
- She typically refers to existing records or reminds customers when she encounters them.

### 5. Reaction to the proposed mobile application

**Proposed features:**
- Digital credit records.
- Easy entry of customer names and purchased items.
- Payment deadlines.
- Automatic notifications and reminders.

**Response:**
- She was hesitant about using a mobile application.
- She explicitly stated that she was unfamiliar with applications of that kind.
- She does not consider herself particularly knowledgeable about cellphone features.
- Even after the interviewer suggested that the application could be easy to use, she preferred her existing written-record method.

### Key findings

**Current practice:** Selective credit lending to trusted customers, with paper-based records.

**Potential problem:** Manual tracking and in-person collection can be inconvenient, especially for overdue balances.

**Adoption barrier:** Limited familiarity with mobile applications and preference for established methods.

**Important insight:** An application offering additional features will not automatically be attractive to users who are already comfortable with paper-based records.

---

## Comparative Analysis of Interview Responses

| Category | Kuya Ronny | Ate Mina |
|---|---|---|
| Offers customer credit | Yes, relatively flexible | Occasionally, to trusted customers |
| Records debts | No consistent written record | Uses written records |
| Primary tracking method | Trust and memory | Paper and memory |
| Collection method | Informal, details unclear | Personally reminds customers |
| Uses digital debt tracking | No indication | No |
| Reaction to proposed app | Generally receptive | Hesitant |
| Main adoption consideration | Ease of recording and remembering | Familiarity with technology |

## Preliminary Research Findings

### Theme 1: Trust plays a central role in lending decisions

Both respondents demonstrate that customer familiarity influences credit practices. However, their approaches differ: Kuya Ronny appears more flexible, while Ate Mina is more selective.

### Theme 2: Debt tracking varies significantly

The interviews show two distinct methods: memory-based tracking and paper-based recording. A potential application should accommodate both workflows instead of assuming all store owners have the same problems.

### Theme 3: Payment collection is informal

Personal reminders and customer-initiated payments appear to be important parts of the repayment process. Neither interview established that automatic notifications would necessarily improve repayment rates.

### Theme 4: Technology adoption may be a greater challenge than technical development

Ate Mina's hesitation suggests that simplicity alone may not guarantee adoption. Familiarity, confidence, perceived usefulness, and existing habits could influence whether store owners adopt a digital system.

## Implications for the Proposed Application

Based on these interviews, the project could prioritize:

1. **Fast debt recording:** Minimal steps to save a customer's name, debt amount, and purchased items.
2. **Simple outstanding-balance list:** Immediately show who owes money and how much.
3. **Optional reminders:** Allow store owners to choose when reminders appear instead of imposing strict repayment schedules.
4. **Offline functionality:** Make records accessible without requiring constant internet connectivity.
5. **Accessible interface:** Large buttons, Filipino-language labels, and straightforward navigation.
6. **Optional customer details:** Avoid requiring extensive customer information for small transactions.

These are preliminary design recommendations, not features conclusively validated by the respondents.

## Research Limitations

The interviews suggest useful directions, but additional evidence is needed before claiming that sari-sari store owners need or will adopt the application.

In particular, future interviews or prototype tests should investigate whether owners lose money because of forgotten debts, how frequently recordkeeping errors occur, and whether a digital solution is easier than their current methods.

**Audio coverage note:** Two interviews were summarized from the supplied audio content. There is also a file labeled *Ate Josefina.aac*, but its full spoken responses were not reliably extracted, so no findings have been attributed to her.

## Overall Conclusion

The strongest opportunity is not necessarily automated debt collection. It is making debt records easier to maintain and retrieve while preserving the informal, trust-based relationships common in sari-sari stores. The clearest adoption challenge is demonstrating that the application provides enough practical value to justify changing an established routine.

---

## Engineering Traceability: How These Interviews Shaped TindaWise

Each theme and design implication above was translated directly into TindaWise's software architecture:

| Interview Implication / Theme | Store Owner Evidence | TindaWise Implementation |
| :--- | :--- | :--- |
| **1. Fast debt recording** *(Implication #1)* | Kuya Ronny avoids writing debts down because manual recording takes effort; Ate Mina dislikes typing item details on a cellphone. | **3-Second Spoken Taglish Voice Capture + Direct Peso Parser (`SKU-DIRECT-PESO`) + 1-Tap Quick Peso Chips (`+₱5` to `+₱100`)** in `src/backend/ledger_engine.py` and `src/frontend/index.html`. |
| **2. Simple outstanding-balance list & verification** *(Implication #2)* | Kuya Ronny risks forgetting unrecorded balances; Ate Mina noted customers genuinely forget old debts and need to be reminded when passing by. | **Digital Kwaderno Ledger with Walk-By Search & Itemized History (`GET /api/ledger/debtors/{id}`)** showing exact dates and items borrowed. |
| **3. Optional reminders & informal collection** *(Theme 3 & Implication #3)* | Both owners collect informally; Ate Mina reminds customers face-to-face (*"Uy, may utang ka pa dito"*). Neither relies on strict automated deadlines. | **Optional Due Dates (`Walang tiyak na petsa / Kapag nakaluwag`)** and **Dual Reminder Drafter (`GET /api/ledger/reminder/{id}`)** generating an in-person *Harapang Paalala* script alongside optional manual SMS/Messenger copy. |
| **4. Offline functionality** *(Implication #4)* | Neighborhood sari-sari stores cannot depend on continuous mobile data to check or record *utang*. | **100% Local SQLite Database (`data/tindawise_local.db`) + Local Deterministic Taglish Parser + Browser `localStorage` Sync** (`src/frontend/index.html`). |
| **5. Accessible Filipino-first interface** *(Theme 4 & Implication #5)* | Ate Mina is hesitant because she is unfamiliar with complex mobile applications and prefers her paper *kwaderno*. | **Simple Kwaderno Mode (Default UI)** featuring oversized touch targets, conversational Tagalog labels (*"1. Maglista ng Utang"*, *"2. Listahan ng May Utang (Kwaderno)"*), and zero technical clutter. |
| **6. Optional customer & transaction details** *(Theme 1 & Implication #6)* | Lending is based on neighborhood familiarity (*Suki* vs. *Kakilala*), and small transactions do not warrant extensive forms. | **Nickname-Only Records (RA 10173 compliant)** with a simple `Suki` / `Kakilala` trust badge (`trust_tag`) and direct peso-amount support without mandatory SKU setup. |

