"""Build the revised nine-slide TindaWise pitch deck.

Reproducible replacement for build_deck.py. It never overwrites the two
user-edited decks; output goes to TindaWise_Pitch_Deck_Revised.pptx.

Design tokens mirror the user's edited deck: 20 x 11.25in, Aptos, cream
F6F4F0 / green 14532D / ink 1B2430 / muted 596573 / accent B45309.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".pitch-deps"))

from PIL import Image  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402
from pptx.util import Inches, Pt  # noqa: E402

OUT = ROOT / "deliverables" / "TindaWise_Pitch_Deck_Revised.pptx"
ASSETS = ROOT / "deliverables" / "assets"
SOURCE_SHOTS = ASSETS / "src"
CROPPED = ASSETS / "crop"

CREAM = RGBColor(0xF6, 0xF4, 0xF0)
GREEN = RGBColor(0x14, 0x53, 0x2D)
INK = RGBColor(0x1B, 0x24, 0x30)
MUTED = RGBColor(0x59, 0x65, 0x73)
ACCENT = RGBColor(0xB4, 0x53, 0x09)
RULE = RGBColor(0xDC, 0xD6, 0xC8)
CARD_BORDER = RGBColor(0xE2, 0xDE, 0xD4)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALE = RGBColor(0xE7, 0xF1, 0xE7)
PALE_TEXT = RGBColor(0xDD, 0xE8, 0xD8)
FRAME = RGBColor(0x14, 0x1B, 0x26)
SOFT_GREEN = RGBColor(0x2E, 0x6B, 0x45)

FONT = "Aptos"
SLIDE_W, SLIDE_H = 20.0, 11.25

# ---------------------------------------------------------------- helpers


def textbox(
    slide,
    x,
    y,
    w,
    h,
    lines,
    size,
    color=INK,
    bold=False,
    align=PP_ALIGN.LEFT,
    line_spacing=None,
    space_after=None,
    anchor=MSO_ANCHOR.TOP,
):
    """lines: str | list[str] | list[list[tuple[str, dict]]] for mixed runs."""
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    if isinstance(lines, str):
        lines = [lines]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line_spacing:
            p.line_spacing = line_spacing
        if space_after is not None:
            p.space_after = Pt(space_after)
        runs = line if isinstance(line, list) else [(line, {})]
        for text, override in runs:
            r = p.add_run()
            r.text = text
            f = r.font
            f.name = FONT
            f.size = Pt(override.get("size", size))
            f.bold = override.get("bold", bold)
            f.color.rgb = override.get("color", color)
    return box


def card(slide, x, y, w, h, fill=WHITE, line=CARD_BORDER, radius=0.22):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shape.adjustments[0] = radius / min(w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    shape.shadow.inherit = False
    shape.text_frame.word_wrap = True
    return shape


def band(slide, x, y, w, h, fill):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def rule(slide, x, y, w, color=RULE):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.016))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def chrome(slide, number, dark=False):
    rule(slide, 0.90, 10.61, 18.15, SOFT_GREEN if dark else RULE)
    textbox(
        slide,
        17.95,
        10.68,
        1.05,
        0.40,
        f"{number:02d}",
        18,
        WHITE if dark else GREEN,
        bold=True,
        align=PP_ALIGN.RIGHT,
    )


def background(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def new_deck():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    return prs


def blank(prs, color=CREAM):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    background(slide, color)
    return slide


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text.strip()


# ---------------------------------------------------------------- images


def crop_assets():
    CROPPED.mkdir(parents=True, exist_ok=True)
    jobs = {
        "confirm_58.png": ((25, 452, 1055, 1648), "confirm_card.png"),
        "direct_peso_50.png": ((25, 580, 1055, 1662), "direct_peso_card.png"),
        "sms_banner.png": ((58, 1098, 1028, 1662), "sms_draft.png"),
    }
    for src_name, (box, out_name) in jobs.items():
        src = ASSETS / src_name
        if not src.exists():
            raise SystemExit(f"missing screenshot: {src}")
        Image.open(src).convert("RGB").crop(box).save(CROPPED / out_name)
    main = CROPPED / "confirm_card.png"
    provenance = ASSETS / "SCREENSHOTS.md"
    provenance.write_text(
        "# App screenshots used in the deck\n\n"
        "Captured from the signed v1.0.0 APK running on an Android emulator "
        "(1080x1920) with fictional data. No SMS was sent: the reminder is a "
        "draft the owner must send.\n\n"
        "- `confirm_58.png` - owner confirmation card, 2 x Canton PHP 16 + "
        "1 x Sardines PHP 26 = PHP 58.\n"
        "- `direct_peso_50.png` - direct-peso entry, PHP 50.\n"
        "- `sms_banner.png` - saved entry, balance PHP 58, drafted reply text.\n\n"
        "The screenshots are cropped to the confirmation area so the app's "
        "in-UI 'RA 10173' badge is not presented as a compliance claim.\n",
        encoding="utf-8",
    )
    return main


# ---------------------------------------------------------------- slides


def slide_cover(prs, shot):
    s = blank(prs, GREEN)
    chrome(s, 1, dark=True)
    textbox(s, 1.02, 1.92, 11.55, 1.38, "TindaWise", 90, WHITE, bold=True)
    textbox(
        s, 1.05, 3.66, 11.55, 1.96,
        ["Taglish voice-to-lista", "for sari-sari stores."], 51, WHITE, bold=True, line_spacing=0.92,
    )
    textbox(
        s, 1.08, 6.05, 10.60, 1.35,
        ["Record utang. Recall the details.", "Keep the owner in control."],
        36, PALE_TEXT, line_spacing=1.05,
    )
    pill = card(s, 1.08, 8.28, 8.85, 0.97, fill=PALE, line=None, radius=0.10)
    textbox(s, 1.46, 8.50, 8.10, 0.53, "SPEAK  \u2192  REVIEW  \u2192  SAVE", 30, GREEN, bold=True)

    frame_pad = 0.16
    shot_w = 5.20
    image = Image.open(shot)
    shot_h = shot_w * image.height / image.width
    frame_x, frame_w = 13.45, shot_w + frame_pad * 2
    frame_h = shot_h + frame_pad * 2
    frame_y = (SLIDE_H - frame_h) / 2
    card(s, frame_x, frame_y, frame_w, frame_h, fill=FRAME, line=None, radius=0.42)
    s.shapes.add_picture(
        str(shot),
        Inches(frame_x + frame_pad),
        Inches(frame_y + frame_pad),
        Inches(shot_w),
        Inches(shot_h),
    )
    notes(
        s,
        """[0:00-0:08] TindaWise is a Taglish voice-to-lista copilot for sari-sari stores. The owner speaks one sentence, checks the draft, and saves it.

Cue: cover image is the real confirmation screen from the signed Android build, fictional data. Say "prototype", not "launched product".""",
    )
    return s


def slide_problem(prs):
    s = blank(prs)
    chrome(s, 2)
    textbox(s, 0.90, 1.30, 18.07, 1.60, ["Utang runs on trust.", "Records need help."], 54, INK, bold=True, line_spacing=0.90)
    textbox(
        s, 0.94, 3.52, 17.85, 0.85,
        "Two owners we interviewed keep credit differently, and both find recall hard.",
        28.5, MUTED,
    )

    cards = [
        (0.97, "MEMORY & TRUST", "Kept in memory", "Lends to familiar suki without a written record; amounts rest on recall.", "Make recording effortless."),
        (10.27, "PAPER KWADERNO", "Written by hand", "Logs debts in a notebook and reminds customers face to face.", "Make past entries easy to find."),
    ]
    for x, eyebrow, head, body, takeaway in cards:
        card(s, x, 4.45, 8.72, 4.28)
        textbox(s, x + 0.41, 4.83, 7.80, 0.38, eyebrow, 18, ACCENT, bold=True)
        textbox(s, x + 0.41, 5.48, 7.80, 0.72, head, 40, GREEN, bold=True)
        textbox(s, x + 0.41, 6.50, 7.60, 1.30, body, 31, INK, line_spacing=1.05)
        rule(s, x + 0.41, 7.85, 7.80)
        textbox(s, x + 0.41, 8.05, 7.70, 0.50, takeaway, 29, GREEN, bold=True)

    textbox(
        s, 0.97, 9.28, 18.07, 0.70,
        "Anonymous summaries of two qualitative interviews. Not a representative sample.",
        22, MUTED,
    )
    notes(
        s,
        """[0:08-0:24] Utang runs on trust. One owner keeps balances in memory. Another writes debts in a kwaderno. Different habits, same weak point: both depend on remembering.

Cue: two anonymized qualitative interviews only. Do not generalize to all stores.""",
    )
    return s


def slide_flow(prs):
    s = blank(prs)
    chrome(s, 3)
    textbox(s, 0.90, 1.30, 18.07, 1.00, "Speak. Review. Save.", 54, INK, bold=True)
    textbox(
        s, 0.94, 2.62, 17.85, 0.85,
        "One familiar sentence becomes an entry the owner checks before it counts.",
        28.5, MUTED,
    )

    card(s, 0.97, 3.92, 7.72, 5.10, fill=GREEN, line=None)
    textbox(s, 1.43, 4.30, 6.75, 0.38, "01  /  SAY IT IN TAGLISH", 18, PALE_TEXT, bold=True)
    textbox(
        s, 1.43, 5.05, 6.75, 2.60,
        "\u201cPalista kay Aling Nena dalawang Lucky Me canton saka isang sardinas, sa Sabado bayad.\u201d",
        31, WHITE, bold=True, line_spacing=1.05,
    )
    textbox(s, 1.43, 7.35, 6.75, 0.70, "No typing, no menu hunting.", 24, PALE_TEXT)

    arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.88), Inches(6.05), Inches(0.94), Inches(0.62))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = GREEN
    arrow.line.fill.background()

    card(s, 10.10, 3.92, 8.88, 5.10)
    textbox(s, 10.55, 4.30, 7.80, 0.38, "02  /  REVIEW THE DRAFT", 18, ACCENT, bold=True)
    textbox(s, 10.55, 4.86, 7.20, 0.60, "Aling Nena", 38, GREEN, bold=True)
    textbox(s, 10.55, 5.72, 5.90, 1.05, ["2 \u00d7 Canton @ \u20b116", "1 \u00d7 Sardinas @ \u20b126"], 30, INK, line_spacing=1.10)
    textbox(s, 16.45, 5.72, 1.95, 1.05, ["\u20b132", "\u20b126"], 30, INK, align=PP_ALIGN.RIGHT, line_spacing=1.10)
    rule(s, 10.55, 7.02, 7.85)
    textbox(s, 10.55, 7.18, 4.20, 0.62, "TOTAL", 22, MUTED, bold=True)
    textbox(s, 15.95, 7.10, 2.45, 0.75, "\u20b158", 40, GREEN, bold=True, align=PP_ALIGN.RIGHT)
    card(s, 10.55, 8.02, 7.85, 0.70, fill=GREEN, line=None, radius=0.08)
    textbox(s, 10.85, 8.16, 7.20, 0.42, "03  /  OWNER CONFIRMS TO SAVE", 19, WHITE, bold=True)

    textbox(
        s, 0.97, 9.30, 18.07, 1.05,
        [
            [("No catalog item? ", {"bold": True, "color": GREEN}), ("Log a direct amount, like a \u20b150 utang, in one line.", {})],
            [("Reminder text is drafted from a template; the owner sends it.", {})],
        ],
        23, MUTED, line_spacing=1.12,
    )
    notes(
        s,
        """[0:24-0:46] She speaks naturally: "Palista kay Aling Nena, dalawang Lucky Me canton saka isang sardinas, sa Sabado bayad." The app drafts two canton at sixteen pesos, one sardinas at twenty-six, fifty-eight total. Nothing saves before she confirms.

Cue: 2 x PHP 16 = PHP 32; 1 x PHP 26 = PHP 26; total PHP 58. Add if asked: an item not on the price list can be logged as a direct amount, e.g. PHP 50.""",
    )
    return s


def slide_ai(prs):
    s = blank(prs)
    chrome(s, 4)
    textbox(s, 0.90, 1.30, 18.07, 1.60, ["Where AI adds value.", "Where the owner stays in charge."], 52, INK, bold=True, line_spacing=0.90)
    textbox(
        s, 0.94, 3.42, 17.85, 0.85,
        "Speech becomes text; extraction proposes the fields; the owner's price list does the math.",
        27, MUTED,
    )

    steps = [
        ("01", "SPEECH \u2192 TEXT", "Device speech recognition turns Taglish into a transcript."),
        ("02", "AI EXTRACTION", "Pulls customer, items, quantities and due date from that text."),
        ("03", "CATALOG PRICING", "Multiplies the owner's own prices \u2014 AI never invents a price."),
        ("04", "OWNER REVIEW", "She checks and corrects; nothing saves without her tap."),
    ]
    for i, (num, head, body) in enumerate(steps):
        x = 0.97 + i * 4.62
        card(s, x, 4.42, 4.26, 3.86)
        textbox(s, x + 0.35, 4.72, 3.52, 0.62, num, 34, ACCENT, bold=True)
        textbox(s, x + 0.35, 5.52, 3.60, 0.90, head, 21, GREEN, bold=True, line_spacing=1.0)
        textbox(s, x + 0.35, 6.55, 3.56, 1.50, body, 22, INK, line_spacing=1.08)

    card(s, 0.97, 8.62, 18.07, 1.62, fill=PALE, line=None, radius=0.16)
    textbox(
        s, 1.35, 8.84, 17.25, 1.20,
        [
            [("Optional cloud extraction (Gemini); the local rule-based parser is the default fallback.", {"bold": True, "color": GREEN})],
            [("Extraction can still misread a name or quantity. The review tap is the safeguard, not a guarantee.", {})],
        ],
        21, INK, line_spacing=1.10,
    )
    notes(
        s,
        """[0:46-1:04] Speech recognition turns Taglish into text. Extraction proposes customer, items, quantities, and due date. Prices come from her catalog, so AI never invents a peso amount. Local rules default; Gemini optional. She corrects, then saves.

Cue: do not claim 100% accuracy or fully offline voice. Extraction can misread a name or quantity; the review tap is the safeguard, not a guarantee.""",
    )
    return s


def slide_evidence(prs, confirm_img, sms_img):
    s = blank(prs)
    chrome(s, 5)
    textbox(s, 0.90, 1.30, 18.07, 0.95, "Prototype and evidence.", 54, INK, bold=True)
    textbox(
        s, 0.94, 2.55, 17.85, 0.85,
        "A signed Android build, tested on stored transcripts \u2014 not yet a field trial.",
        28.5, MUTED,
    )

    # One large, readable screenshot of the owner's confirmation step.
    confirm = Image.open(confirm_img)
    shot_h = 5.28
    shot_w = shot_h * confirm.width / confirm.height
    card(s, 0.97, 3.45, shot_w + 0.34, shot_h + 0.34, line=CARD_BORDER)
    s.shapes.add_picture(str(confirm_img), Inches(1.14), Inches(3.62), Inches(shot_w), Inches(shot_h))

    metrics = [
        ("94.4%", "item and quantity match", "34 of 36 stored transcripts"),
        ("73.4%", "faster than paper", "reported 25.46s \u2192 6.76s per entry"),
    ]
    for i, (big, mid, small) in enumerate(metrics):
        y = 3.45 + i * 1.66
        card(s, 7.10, y, 11.94, 1.50)
        textbox(s, 7.50, y + 0.16, 2.95, 1.00, big, 52, GREEN, bold=True)
        textbox(s, 10.55, y + 0.26, 7.90, 0.48, mid, 25, INK, bold=True)
        textbox(s, 10.55, y + 0.86, 8.00, 0.48, small, 20, MUTED)

    # SMS evidence, small and secondary.
    card(s, 7.10, 6.95, 11.94, 2.55)
    sms = Image.open(sms_img)
    sms_w = 3.95
    sms_h = sms_w * sms.height / sms.width
    s.shapes.add_picture(
        str(sms_img),
        Inches(7.38),
        Inches(6.95 + (2.55 - sms_h) / 2),
        Inches(sms_w),
        Inches(sms_h),
    )
    textbox(
        s,
        11.58, 7.28, 7.10, 1.90,
        [
            [("Drafted reminder \u2014 saved, not sent", {"bold": True, "color": INK})],
            [("The app fills a template with the saved entry. The owner reviews it, then sends it herself. No SMS goes out automatically.", {})],
        ],
        19, MUTED, line_spacing=1.14,
    )

    textbox(
        s, 0.97, 9.62, 18.07, 0.55,
        "Reported benchmark from supplied timing data; does not measure live speech recognition, adoption, or repayment.",
        18, MUTED,
    )
    notes(
        s,
        """[1:04-1:17] This is the signed build. On thirty-six stored transcripts it matched items and quantities in thirty-four—ninety-four point four percent. Supplied timing shows six point eight seconds versus twenty-five point five on paper. Both are benchmarks, not field results.

Cue: stored transcripts, not live speech. Timing protocol undocumented. No adoption or repayment data. Screenshots use fictional data; no SMS was sent.""",
    )
    return s


def slide_market(prs):
    s = blank(prs)
    chrome(s, 6)
    textbox(s, 0.90, 1.30, 18.07, 0.95, "A large market. A narrow entry point.", 52, INK, bold=True)
    textbox(
        s, 0.94, 2.55, 17.85, 0.85,
        "Over 1.3 million sari-sari stores were recorded nationally in 2024. Our starting point is much smaller.",
        26, MUTED,
    )

    stats = [
        ("1.3M+", "stores recorded by DTI in 2024", "A national count, not a customer base."),
        ("Batangas", "where we start", "Nearby stores we can support in person."),
        ("Voice-first", "the wedge", "For owners who will not type entries."),
    ]
    for i, (big, mid, small) in enumerate(stats):
        y = 3.62 + i * 1.94
        card(s, 0.97, y, 7.05, 1.78)
        textbox(s, 1.33, y + 0.18, 6.35, 0.64, big, 28 if big != "1.3M+" else 38, GREEN, bold=True)
        textbox(s, 1.33, y + 0.86, 6.35, 0.36, mid, 19, INK, bold=True)
        textbox(s, 1.33, y + 1.24, 6.35, 0.40, small, 17, MUTED)

    card(s, 8.42, 3.62, 10.62, 5.62)
    textbox(s, 8.78, 3.92, 9.90, 0.38, "WHO ELSE IS AT THE COUNTER", 18, ACCENT, bold=True)

    rows = [
        ("Peddlr", "POS, inventory, sales reports and a credit ledger."),
        ("Lista", "Sales, expenses, receivables; advertises SMS reminders."),
        ("Packworks", "Connected store ecosystem and mobile store tools."),
    ]
    y = 4.42
    for name, desc in rows:
        textbox(s, 8.78, y, 2.55, 0.45, name, 23, INK, bold=True)
        textbox(s, 11.40, y + 0.04, 7.30, 0.80, desc, 19, MUTED)
        y += 0.90

    rule(s, 8.78, 7.02, 9.86)
    textbox(s, 8.78, 7.22, 9.90, 0.40, "OUR DIFFERENCE", 18, ACCENT, bold=True)
    textbox(
        s, 8.78, 7.62, 9.86, 1.45,
        "These tools assume the owner will navigate a POS or type entries. We start from one spoken sentence in Taglish, then keep the owner's confirmation in the loop.",
        20, INK, line_spacing=1.08,
    )
    textbox(
        s, 0.97, 9.55, 18.07, 0.60,
        "Sources: PIA/DTI, 2024 store count; company pages for Peddlr, Lista and Packworks, accessed Nov 2026.",
        17, MUTED,
    )
    notes(
        s,
        """[1:17-1:33] DTI recorded over one point three million sari-sari stores nationally in 2024. A count, not an addressable market. We start in Batangas. Peddlr, Lista, and Packworks assume a POS or typed entries. Our wedge: voice-first Taglish.

Cue: the 1.3M figure is national, not a serviceable market or a user count. Sources and access dates are in the notes file.""",
    )
    return s


def slide_business(prs):
    s = blank(prs)
    chrome(s, 7)
    textbox(s, 0.90, 1.30, 18.07, 0.95, "The path to a business.", 54, INK, bold=True)
    textbox(
        s, 0.94, 2.55, 17.85, 0.85,
        "The store owner is the buyer. We earn daily use first, then test what she would pay for.",
        27, MUTED,
    )

    cols = [
        ("WHO PAYS", "The owner-operator", "A single store with regular utang: price-sensitive, and already paying in time lost to manual recall."),
        ("HOW WE START", "Free pilot, direct onboarding", "We set up the price list with her and stay reachable. No subscription during validation."),
        ("WHAT WE'D TEST", "Future paid features", "Backup and multi-device sync, or family and staff access. Hypotheses, not built or priced yet."),
    ]
    for i, (eyebrow, head, body) in enumerate(cols):
        x = 0.97 + i * 6.24
        card(s, x, 3.55, 5.83, 4.05)
        textbox(s, x + 0.38, 3.88, 5.10, 0.38, eyebrow, 18, ACCENT, bold=True)
        textbox(s, x + 0.38, 4.40, 5.10, 1.05, head, 27, GREEN, bold=True, line_spacing=1.02)
        textbox(s, x + 0.38, 5.55, 5.08, 1.85, body, 22, INK, line_spacing=1.14)

    band(s, 0.97, 8.05, 18.07, 1.25, PALE)
    textbox(
        s, 1.30, 8.26, 17.40, 0.90,
        [
            [("Validation goal: ", {"bold": True, "color": GREEN}),
             ("do owners keep using it after the novelty, and can they name what it is worth?", {})],
        ],
        24, INK, line_spacing=1.12,
    )
    notes(
        s,
        """[1:33-1:46] The buyer is the owner-operator. We begin with a free pilot and hands-on onboarding. Monetization stays open: backup, sync, or staff access are hypotheses, not priced features.

Cue: do not state a subscription price, revenue target, store target, or partner. If pressed, validation comes before pricing.""",
    )
    return s


def slide_pilot(prs):
    s = blank(prs)
    chrome(s, 8)
    textbox(s, 0.90, 1.30, 18.07, 0.95, "Pilot before promises.", 54, INK, bold=True)
    textbox(
        s, 0.94, 2.55, 17.85, 0.85,
        "Four stages, each ending in a decision rather than a download count.",
        28, MUTED,
    )

    steps = [
        ("01", "RECRUIT", "Nearby stores that already extend utang."),
        ("02", "OBSERVE", "Watch real counter tasks, not scripted demos."),
        ("03", "RETURN", "Check whether use survives the second week."),
        ("04", "DECIDE", "Test willingness to pay against cost to serve."),
    ]
    for i, (num, head, body) in enumerate(steps):
        x = 0.97 + i * 4.62
        card(s, x, 3.55, 4.26, 3.55)
        textbox(s, x + 0.35, 3.82, 3.52, 0.62, num, 34, ACCENT, bold=True)
        textbox(s, x + 0.35, 4.55, 3.55, 0.55, head, 27, GREEN, bold=True)
        textbox(s, x + 0.35, 5.30, 3.55, 1.60, body, 23, INK, line_spacing=1.10)

    rule(s, 0.97, 7.52, 18.07)
    textbox(
        s, 0.97, 7.78, 18.07, 0.90,
        "Go only if owners keep using it and can state a value. Otherwise, the wedge or segment is wrong.",
        24, INK, line_spacing=1.10,
    )
    textbox(
        s, 0.97, 8.62, 18.07, 0.55,
        "No store count, price, or launch date is committed; the pilot decides what comes next.",
        20, MUTED,
    )
    notes(
        s,
        """[1:46-1:54] The pilot is four decisions: recruit, observe real counter tasks, return after week two, test willingness to pay. No store count, price, or date is committed.

Cue: the gate is retention and a stated value, not download counts.""",
    )
    return s


def slide_closing(prs):
    s = blank(prs, GREEN)
    chrome(s, 9, dark=True)
    textbox(s, 0.90, 3.05, 17.70, 2.41, "TindaWise", 96, WHITE, bold=True)
    textbox(s, 1.10, 5.28, 9.60, 1.46, "Tindahang maayos, suking maasahan.", 40, PALE_TEXT, bold=True)
    textbox(
        s, 1.10, 7.35, 10.40, 0.90,
        "Try the Android prototype \u2014 speak one utang, check the draft, save.",
        24, PALE_TEXT,
    )
    notes(
        s,
        """[1:54-2:00] TindaWise: speak one utang, check the draft, save it. Tindahang maayos, suking maasahan. Thank you.

Cue: offer the installed APK. Do not show a QR code; the public repository link returned 404 during preparation.""",
    )
    return s


def main():
    confirm_img = crop_assets()
    direct = CROPPED / "direct_peso_card.png"
    sms = CROPPED / "sms_draft.png"

    prs = new_deck()
    slide_cover(prs, confirm_img)
    slide_problem(prs)
    slide_flow(prs)
    slide_ai(prs)
    slide_evidence(prs, confirm_img, sms)
    slide_market(prs)
    slide_business(prs)
    slide_pilot(prs)
    slide_closing(prs)

    prs.save(OUT)
    print(f"saved {OUT} with {len(prs.slides.__iter__.__self__._sldIdLst)} slides")
    print(f"direct-peso crop available: {direct.exists()}")


if __name__ == "__main__":
    main()
