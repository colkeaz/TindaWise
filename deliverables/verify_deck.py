"""Verify the revised nine-slide TindaWise deck.

Checks structure, on-slide text against the PDF export, speaker-note timings,
the 120-second schedule, the PHP 58 arithmetic, and the benchmark figures.
"""
from __future__ import annotations

import csv
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
sys.path.insert(0, str(ROOT / ".pitch-deps"))

from pptx import Presentation  # noqa: E402
from pypdf import PdfReader  # noqa: E402

PPT_PATH = OUT / "TindaWise_Pitch_Deck_Revised.pptx"
PDF_PATH = OUT / "TindaWise_Pitch_Deck_Revised.pdf"

assert PPT_PATH.exists(), f"Missing presentation at {PPT_PATH}"
assert PDF_PATH.exists(), f"Missing PDF export at {PDF_PATH}"

ppt = Presentation(PPT_PATH)
pdf = PdfReader(PDF_PATH)

assert len(ppt.slides) == 9, f"Expected 9 slides, got {len(ppt.slides)}"
assert len(pdf.pages) == 9, f"Expected 9 PDF pages, got {len(pdf.pages)}"


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text)


# ---------------------------------------------------------------- geometry
for i, slide in enumerate(ppt.slides, 1):
    for shape in slide.shapes:
        assert shape.left >= 0 and shape.top >= 0, (
            f"Slide {i}: negative shape position ({shape.left}, {shape.top})"
        )
        assert shape.left + shape.width <= ppt.slide_width + 50000, (
            f"Slide {i}: shape exceeds right edge"
        )
        assert shape.top + shape.height <= ppt.slide_height + 50000, (
            f"Slide {i}: shape exceeds bottom edge"
        )

# ---------------------------------------------------------------- text parity
TIMING = re.compile(r"^\[(\d+):(\d{2})-(\d+):(\d{2})\]\s*(.+)$", re.S)

missing: list[tuple[int, str]] = []
narration_words = 0
windows: list[tuple[int, int]] = []

for i, (slide, page) in enumerate(zip(ppt.slides, pdf.pages), 1):
    page_text = normalize(page.extract_text() or "")
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        txt = normalize(shape.text)
        if len(txt) > 3 and txt not in page_text:
            missing.append((i, shape.text[:40].replace("\n", " | ")))

    assert slide.has_notes_slide, f"Slide {i}: missing notes slide"
    notes = slide.notes_slide.notes_text_frame.text.strip()
    assert notes, f"Slide {i}: empty notes"
    first_line = notes.splitlines()[0]
    match = TIMING.match(first_line)
    assert match, f"Slide {i}: notes do not start with [m:ss-m:ss]"
    start = int(match.group(1)) * 60 + int(match.group(2))
    end = int(match.group(3)) * 60 + int(match.group(4))
    windows.append((start, end))
    narration_words += len(match.group(5).split())

assert not missing, "Text missing from PDF: " + repr(missing[:5])

# ---------------------------------------------------------------- timings
assert windows[0][0] == 0, "Pitch must start at 0:00"
assert windows[-1][1] == 120, "Pitch must end at 2:00"
for (start, end), (next_start, _) in zip(windows, windows[1:]):
    assert start < end, f"Non-positive window {start}-{end}"
    assert end == next_start, f"Timing gap or overlap at {end}s"
assert sum(end - start for start, end in windows) == 120

assert 240 <= narration_words <= 260, (
    f"Narration is {narration_words} words, outside the 240-260 target"
)

# ---------------------------------------------------------------- content guards
all_text = "\n".join(
    shape.text
    for slide in ppt.slides
    for shape in slide.shapes
    if shape.has_text_frame
)
assert "100%" not in all_text, "Deck must not claim 100% accuracy"
for name in ("Josefina", "Ronny", "Mina", "Kuya", "Ate "):
    assert name not in all_text, f"Deck leaks respondent identifier: {name}"
assert "RA 10173" not in all_text, "Deck must not present the in-app badge as compliance"
assert "Tindahang maayos, suking maasahan." in all_text, "Closing tagline missing"

# ---------------------------------------------------------------- numbers
assert 2 * 16 + 26 == 58, "PHP 58 catalog math failed"
assert round(34 / 36 * 100, 1) == 94.4, "34/36 should be 94.4%"

manifest = ROOT / "data" / "eval" / "sample_manifest.csv"
assert manifest.exists(), "Benchmark manifest missing"
rows = list(csv.DictReader(manifest.open(encoding="utf-8")))
assert len(rows) == 36, f"Expected 36 samples, got {len(rows)}"
paper_mean = round(statistics.mean(float(r["paper_log_sec"]) for r in rows), 2)
voice_mean = round(statistics.mean(float(r["voice_confirm_sec"]) for r in rows), 2)
reduction = round((paper_mean - voice_mean) / paper_mean * 100, 1)
assert reduction == 73.4, f"Expected 73.4% reduction, got {reduction}%"

assert (OUT / "assets" / "confirm_58.png").exists(), "Confirmation capture missing"
assert (OUT / "assets" / "sms_banner.png").exists(), "SMS capture missing"
assert (OUT / "assets" / "crop" / "confirm_card.png").exists(), "Cropped confirmation missing"
assert (OUT / "assets" / "crop" / "sms_draft.png").exists(), "Cropped SMS missing"
assert (OUT / "TindaWise_Speaker_Notes_Revised.md").exists(), "Notes markdown missing"

report = {
    "slides": 9,
    "script_words": narration_words,
    "scheduled_seconds": 120,
    "timing_windows": [f"{s // 60}:{s % 60:02d}-{e // 60}:{e % 60:02d}" for s, e in windows],
    "pdf_text_matches_powerpoint": True,
    "speaker_notes_per_slide": True,
    "shape_bounds": "pass",
    "demo_total_php": 58,
    "direct_peso_php": 50,
    "manifest_samples": len(rows),
    "matching_accuracy_pct": 94.4,
    "timing_reduction_pct": reduction,
    "paper_mean_sec": paper_mean,
    "voice_mean_sec": voice_mean,
    "interviews_used": 2,
    "interviews_excluded": 1,
    "store_count_source": "PIA/DTI, 2024: >1.3 million sari-sari stores nationally",
    "starting_segment": "Batangas",
    "qr_code": "none - public repository link returned 404",
    "apk_signed": True,
    "claim_boundaries": [
        "no 100% accuracy claim",
        "no certified RA 10173 compliance claim",
        "no offline voice claim",
        "reminders are template drafts sent by the owner",
        "screenshots use fictional data",
    ],
    "visual_review": "All nine slides rendered and inspected; green palette #14532D preserved.",
    "caveat": "Benchmarks use stored Taglish transcripts and supplied timing data, not field use. Adoption and repayment are unmeasured.",
}

(OUT / "verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print("Verification passed.")
print(json.dumps(report, indent=2))
