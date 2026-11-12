# TindaWise Empirical Evaluation & Timing Benchmark Report

- **Total Spoken Taglish Utterances Evaluated:** `36` across `6` speakers and `4` noise conditions
- **Debtor Name Extraction Accuracy:** `94.4%` (34/36)
- **Item SKU + Quantity Extraction Accuracy:** `94.4%` (34/36)
- **Deterministic Price-List Total Match:** `94.4%` (34/36)
- **Promised Due Date Extraction Accuracy:** `100.0%` (36/36)
- **Measured Local Extraction + Price Lookup Latency:** `p50 = 1.4 ms`, `p95 = 2.11 ms`, `mean = 1.62 ms`
- **End-to-End Time-to-Log (Speak + Owner Confirm vs. Paper Notebook):** `6.76s` vs. `25.46s` (`73.4%` faster per entry)

## Breakdown by Counter Noise Condition

| Noise Condition | Samples | Debtor Name Accuracy | Item + Quantity Accuracy |
| :--- | :---: | :---: | :---: |
| `quiet_counter` | 10 | 100.0% (10/10) | 100.0% (10/10) |
| `electric_fan` | 8 | 100.0% (8/8) | 100.0% (8/8) |
| `street_tricycle` | 10 | 100.0% (10/10) | 80.0% (8/10) |
| `radio_chatter` | 8 | 75.0% (6/8) | 100.0% (8/8) |

## Field Interview Validation & Persona Scenario Alignment

In addition to the 36 catalog benchmark utterances above, TindaWise was validated against the two store-owner workflows documented in [`data/research/sarisaristore_interview.md`](../research/sarisaristore_interview.md):

| Store Owner Persona | Interview Workflow & Pain Point | Validated TindaWise Capability | Status |
| :--- | :--- | :--- | :---: |
| **Kuya Ronny Bautista** | Memory & trust-based lending (`Suki` & `Kakilala`); no written records; needs fast non-SKU logging so debts aren't forgotten. | Spoken & 1-Tap **Direct Peso-Amount Utang (`SKU-DIRECT-PESO`)** (e.g., *'Palista kay Kuya Ronny singkwenta pesos na ulam'* -> `PHP 50.00`) | **PASS (100%)** |
| **Ate Mina** | Paper *kwaderno* user; selective *suki* lending; reminds customers **face-to-face** when they pass by; hesitant about complex typing apps. | **Simple Kwaderno Mode**, optional due dates (`Walang tiyak na petsa`), **Walk-By Itemized History Lookup**, and **Face-to-Face Reminder Script (*Harapang Paalala*)** | **PASS (100%)** |

## Sample-by-Sample Verification Log

| ID | Speaker | Noise | Expected Debtor | Extracted Debtor | Expected Total | Deterministic Total | Extract ms | Paper (s) | Voice+Confirm (s) |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| UTG-001 | SPK-01 | `quiet_counter` | Aling Nena | Aling Nena | PHP 58.00 | PHP 58.00 | 6.73 | 24.5s | 6.2s |
| UTG-002 | SPK-01 | `electric_fan` | Kuya Jojo | Kuya Jojo | PHP 45.00 | PHP 45.00 | 1.51 | 27.0s | 6.8s |
| UTG-003 | SPK-02 | `street_tricycle` | Ate Marites | Ate Marites | PHP 83.00 | PHP 83.00 | 1.42 | 25.2s | 6.5s |
| UTG-004 | SPK-02 | `radio_chatter` | Mang Kanor | Mang Kanor | PHP 52.00 | PHP 52.00 | 1.48 | 29.4s | 7.4s |
| UTG-005 | SPK-03 | `quiet_counter` | Nanay Cora | Nanay Cora | PHP 47.00 | PHP 47.00 | 1.34 | 22.8s | 5.9s |
| UTG-006 | SPK-03 | `electric_fan` | Pareng Boyet | Pareng Boyet | PHP 106.00 | PHP 106.00 | 1.51 | 26.1s | 6.4s |
| UTG-007 | SPK-04 | `street_tricycle` | Tita Baby | Tita Baby | PHP 56.00 | PHP 56.00 | 1.3 | 25.0s | 6.6s |
| UTG-008 | SPK-04 | `radio_chatter` | Kuya Ben | Kuya Ben | PHP 76.00 | PHP 76.00 | 1.38 | 28.3s | 7.1s |
| UTG-009 | SPK-05 | `quiet_counter` | Ate Lorna | Ate Lorna | PHP 98.00 | PHP 98.00 | 1.34 | 21.5s | 5.8s |
| UTG-010 | SPK-05 | `electric_fan` | Mang Tomas | Mang Tomas | PHP 56.00 | PHP 56.00 | 1.75 | 24.0s | 6.3s |
| UTG-011 | SPK-06 | `street_tricycle` | Aling Rosa | Aling Rosa | PHP 96.00 | PHP 96.00 | 2.11 | 27.5s | 7.0s |
| UTG-012 | SPK-06 | `radio_chatter` | Kuya Mark | Kuya Mark | PHP 89.00 | PHP 89.00 | 2.17 | 26.8s | 6.9s |
| UTG-013 | SPK-01 | `quiet_counter` | Tatay Doming | Tatay Doming | PHP 146.00 | PHP 146.00 | 1.95 | 23.4s | 6.0s |
| UTG-014 | SPK-01 | `street_tricycle` | Mareng Gina | Mareng Gina | PHP 65.00 | PHP 65.00 | 1.45 | 24.8s | 6.5s |
| UTG-015 | SPK-02 | `quiet_counter` | Boss Ricky | Boss Ricky | PHP 81.00 | PHP 81.00 | 1.3 | 23.9s | 6.1s |
| UTG-016 | SPK-02 | `electric_fan` | Ate Jenny | Ate Jenny | PHP 72.00 | PHP 72.00 | 1.32 | 25.6s | 6.4s |
| UTG-017 | SPK-03 | `street_tricycle` | Mang Bert | Mang Bert | PHP 53.00 | PHP 53.00 | 1.54 | 26.2s | 6.7s |
| UTG-018 | SPK-03 | `radio_chatter` | Aling Bebang | Aling Bebang | PHP 66.00 | PHP 66.00 | 1.49 | 28.0s | 7.2s |
| UTG-019 | SPK-04 | `quiet_counter` | Kuya Jun | Kuya Jun | PHP 130.00 | PHP 130.00 | 1.64 | 23.1s | 5.9s |
| UTG-020 | SPK-04 | `electric_fan` | Nanay Pina | Nanay Pina | PHP 78.00 | PHP 78.00 | 1.37 | 24.7s | 6.3s |
| UTG-021 | SPK-05 | `street_tricycle` | Pareng Allan | Pareng Allan | PHP 40.00 | PHP 40.00 | 1.38 | 22.9s | 6.2s |
| UTG-022 | SPK-05 | `radio_chatter` | Tita Evelyn | Tita Evelyn | PHP 42.00 | PHP 42.00 | 1.37 | 29.1s | 7.3s |
| UTG-023 | SPK-06 | `quiet_counter` | Mang Nestor | Mang Nestor | PHP 186.00 | PHP 186.00 | 1.42 | 24.2s | 6.1s |
| UTG-024 | SPK-06 | `electric_fan` | Ate Grace | Ate Grace | PHP 40.00 | PHP 40.00 | 1.46 | 25.0s | 6.4s |
| UTG-025 | SPK-01 | `radio_chatter` | Kuya Noel | Kuya Noel | PHP 81.00 | PHP 81.00 | 1.34 | 27.3s | 6.9s |
| UTG-026 | SPK-02 | `street_tricycle` | Aling Mila | Aling Mila | PHP 44.00 | PHP 44.00 | 1.38 | 25.8s | 6.6s |
| UTG-027 | SPK-03 | `quiet_counter` | Tatay Efren | Tatay Efren | PHP 68.00 | PHP 68.00 | 1.5 | 23.5s | 6.0s |
| UTG-028 | SPK-04 | `street_tricycle` | Mareng Susan | Mareng Susan | PHP 59.00 | PHP 59.00 | 1.38 | 24.4s | 6.5s |
| UTG-029 | SPK-05 | `electric_fan` | Boss Dindo | Boss Dindo | PHP 70.00 | PHP 70.00 | 1.28 | 25.1s | 6.3s |
| UTG-030 | SPK-06 | `quiet_counter` | Ate Bing | Ate Bing | PHP 106.00 | PHP 106.00 | 1.47 | 26.0s | 6.8s |
| UTG-031 | SPK-01 | `street_tricycle` | Kuya Dante | Kuya Dante | PHP 80.00 | PHP 132.00 | 1.32 | 26.5s | 8.9s |
| UTG-032 | SPK-02 | `radio_chatter` | Aling Fe | Aling Tess | PHP 50.00 | PHP 50.00 | 1.25 | 25.9s | 9.2s |
| UTG-033 | SPK-03 | `street_tricycle` | Mang Larry | Mang Larry | PHP 59.00 | PHP 68.00 | 1.27 | 27.1s | 8.7s |
| UTG-034 | SPK-04 | `quiet_counter` | Ate Vicky | Ate Vicky | PHP 114.00 | PHP 114.00 | 1.3 | 23.8s | 6.1s |
| UTG-035 | SPK-05 | `electric_fan` | Kuya Bong | Kuya Bong | PHP 130.00 | PHP 130.00 | 1.3 | 25.4s | 6.4s |
| UTG-036 | SPK-06 | `radio_chatter` | Nanay Ely | Nanayely | PHP 65.00 | PHP 65.00 | 1.8 | 26.7s | 8.8s |
