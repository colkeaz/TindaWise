"""
TindaWise Empirical Evaluation & Timing Benchmark Harness
Evaluates 30-50 spoken Taglish utang entries across multiple speakers and noise conditions.
Measures:
1. Debtor Name Extraction Accuracy (%)
2. Item SKU + Quantity Extraction Accuracy (%)
3. Deterministic Total Match Accuracy (%)
4. Measured Extraction + Price Lookup Latency (p50, p95, mean in ms)
5. End-to-End Time-to-Log (Voice + Owner Confirm vs. Paper Notebook Baseline in seconds)
"""

from __future__ import annotations

import argparse
import csv
import os
import statistics
import sys
from decimal import Decimal
from typing import Any, Dict, List

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"),
)
from ledger_engine import TindaWiseEngine, to_money, to_qty


def parse_expected_items(spec: str) -> Dict[str, Decimal]:
    result: Dict[str, Decimal] = {}
    for part in spec.split(";"):
        part = part.strip()
        if not part:
            continue
        sku, qty = part.split(":")
        result[sku.strip()] = to_qty(qty.strip())
    return result


def evaluate_manifest(manifest_path: str, output_md_path: str, use_cloud: bool = False) -> Dict[str, Any]:
    test_db = os.path.join(os.path.dirname(output_md_path), "_eval_temp.db")
    if os.path.exists(test_db):
        os.remove(test_db)

    engine = TindaWiseEngine(db_path=test_db)
    rows_out: List[Dict[str, Any]] = []
    latencies_ms: List[float] = []
    paper_secs: List[float] = []
    voice_secs: List[float] = []

    debtor_correct = 0
    items_qty_correct = 0
    total_correct = 0
    due_correct = 0
    by_noise: Dict[str, Dict[str, int]] = {}

    with open(manifest_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sample_id = row["sample_id"]
            speaker_id = row["speaker_id"]
            noise = row["noise_condition"]
            utterance = row["utterance"]
            exp_debtor = row["expected_debtor"].strip()
            exp_items = parse_expected_items(row["expected_items"])
            exp_total = to_money(row["expected_total"])
            exp_due = row["expected_due"].strip()
            p_sec = float(row["paper_log_sec"])
            v_sec = float(row["voice_confirm_sec"])

            preview = engine.extract_utang_preview(
                transcript_text=utterance,
                prefer_cloud_api=use_cloud,
            )

            lat_ms = preview.timings_ms["total_ms"]
            latencies_ms.append(lat_ms)
            paper_secs.append(p_sec)
            voice_secs.append(v_sec)

            pred_debtor_ok = preview.debtor_name.lower() == exp_debtor.lower()
            pred_items_map = {
                (it.matched_sku_id or "UNMATCHED"): to_qty(it.quantity)
                for it in preview.items
            }
            pred_items_ok = pred_items_map == exp_items
            pred_total_ok = to_money(preview.computed_total) == exp_total
            pred_due_ok = preview.due_date_raw.lower() == exp_due.lower()

            if pred_debtor_ok:
                debtor_correct += 1
            if pred_items_ok:
                items_qty_correct += 1
            if pred_total_ok:
                total_correct += 1
            if pred_due_ok:
                due_correct += 1

            bucket = by_noise.setdefault(noise, {"total": 0, "debtor_ok": 0, "items_ok": 0})
            bucket["total"] += 1
            if pred_debtor_ok:
                bucket["debtor_ok"] += 1
            if pred_items_ok:
                bucket["items_ok"] += 1

            rows_out.append(
                {
                    "sample_id": sample_id,
                    "speaker_id": speaker_id,
                    "noise": noise,
                    "debtor_ok": pred_debtor_ok,
                    "items_ok": pred_items_ok,
                    "total_ok": pred_total_ok,
                    "due_ok": pred_due_ok,
                    "pred_debtor": preview.debtor_name,
                    "exp_debtor": exp_debtor,
                    "pred_total": preview.computed_total,
                    "exp_total": str(exp_total),
                    "latency_ms": lat_ms,
                    "paper_sec": p_sec,
                    "voice_sec": v_sec,
                }
            )

    if os.path.exists(test_db):
        os.remove(test_db)

    n = len(rows_out)
    sorted_lat = sorted(latencies_ms)
    p50_ms = round(statistics.median(sorted_lat), 2) if sorted_lat else 0.0
    p95_idx = min(len(sorted_lat) - 1, int(round(0.95 * (len(sorted_lat) - 1)))) if sorted_lat else 0
    p95_ms = round(sorted_lat[p95_idx], 2) if sorted_lat else 0.0
    mean_ms = round(statistics.mean(sorted_lat), 2) if sorted_lat else 0.0

    mean_paper_s = round(statistics.mean(paper_secs), 2) if paper_secs else 0.0
    mean_voice_s = round(statistics.mean(voice_secs), 2) if voice_secs else 0.0
    time_saved_pct = round(((mean_paper_s - mean_voice_s) / mean_paper_s) * 100.0, 1) if mean_paper_s else 0.0

    summary = {
        "total_samples": n,
        "debtor_accuracy_pct": round((debtor_correct / n) * 100.0, 1) if n else 0.0,
        "items_qty_accuracy_pct": round((items_qty_correct / n) * 100.0, 1) if n else 0.0,
        "deterministic_total_accuracy_pct": round((total_correct / n) * 100.0, 1) if n else 0.0,
        "due_date_accuracy_pct": round((due_correct / n) * 100.0, 1) if n else 0.0,
        "p50_latency_ms": p50_ms,
        "p95_latency_ms": p95_ms,
        "mean_latency_ms": mean_ms,
        "mean_paper_log_sec": mean_paper_s,
        "mean_voice_confirm_sec": mean_voice_s,
        "time_saved_pct": time_saved_pct,
        "by_noise": by_noise,
    }

    os.makedirs(os.path.dirname(os.path.abspath(output_md_path)), exist_ok=True)
    with open(output_md_path, "w", encoding="utf-8") as mf:
        mf.write("# TindaWise Empirical Evaluation & Timing Benchmark Report\n\n")
        mf.write(f"- **Total Spoken Taglish Utterances Evaluated:** `{n}` across `6` speakers and `4` noise conditions\n")
        mf.write(f"- **Debtor Name Extraction Accuracy:** `{summary['debtor_accuracy_pct']}%` ({debtor_correct}/{n})\n")
        mf.write(f"- **Item SKU + Quantity Extraction Accuracy:** `{summary['items_qty_accuracy_pct']}%` ({items_qty_correct}/{n})\n")
        mf.write(f"- **Deterministic Price-List Total Match:** `{summary['deterministic_total_accuracy_pct']}%` ({total_correct}/{n})\n")
        mf.write(f"- **Promised Due Date Extraction Accuracy:** `{summary['due_date_accuracy_pct']}%` ({due_correct}/{n})\n")
        mf.write(f"- **Measured Local Extraction + Price Lookup Latency:** `p50 = {p50_ms} ms`, `p95 = {p95_ms} ms`, `mean = {mean_ms} ms`\n")
        mf.write(
            f"- **End-to-End Time-to-Log (Speak + Owner Confirm vs. Paper Notebook):** "
            f"`{mean_voice_s}s` vs. `{mean_paper_s}s` (`{time_saved_pct}%` faster per entry)\n\n"
        )
        mf.write("## Breakdown by Counter Noise Condition\n\n")
        mf.write("| Noise Condition | Samples | Debtor Name Accuracy | Item + Quantity Accuracy |\n")
        mf.write("| :--- | :---: | :---: | :---: |\n")
        for n_cond, stats in by_noise.items():
            t_cnt = stats["total"]
            d_pct = round((stats["debtor_ok"] / t_cnt) * 100.0, 1)
            i_pct = round((stats["items_ok"] / t_cnt) * 100.0, 1)
            mf.write(f"| `{n_cond}` | {t_cnt} | {d_pct}% ({stats['debtor_ok']}/{t_cnt}) | {i_pct}% ({stats['items_ok']}/{t_cnt}) |\n")

        mf.write("\n## Sample-by-Sample Verification Log\n\n")
        mf.write("| ID | Speaker | Noise | Expected Debtor | Extracted Debtor | Expected Total | Deterministic Total | Extract ms | Paper (s) | Voice+Confirm (s) |\n")
        mf.write("| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n")
        for r in rows_out:
            mf.write(
                f"| {r['sample_id']} | {r['speaker_id']} | `{r['noise']}` | {r['exp_debtor']} | {r['pred_debtor']} | "
                f"PHP {r['exp_total']} | PHP {r['pred_total']} | {r['latency_ms']} | {r['paper_sec']}s | {r['voice_sec']}s |\n"
            )

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run TindaWise 30-50 utterance evaluation benchmark.")
    parser.add_argument(
        "--manifest",
        default=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "data",
            "eval",
            "sample_manifest.csv",
        ),
    )
    parser.add_argument(
        "--output",
        default=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "data",
            "eval",
            "Evaluation_Benchmark_Report.md",
        ),
    )
    parser.add_argument("--cloud", action="store_true", help="Use live Gemini API if GEMINI_API_KEY is set")
    args = parser.parse_args()

    res = evaluate_manifest(args.manifest, args.output, use_cloud=args.cloud)
    print("=== TINDAWISE EVALUATION SUMMARY ===")
    for k, v in res.items():
        if k != "by_noise":
            print(f"{k}: {v}")
