import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PPTX = r"C:\Users\Lenovo\Documents\AIdeathon\deliverables\TindaWise_Pitch_Deck_Revised.pptx"
SCREENS_DIR = r"C:\Users\Lenovo\Documents\AIdeathon\deliverables\screens"

# Palette
DARK_GREEN = RGBColor(20, 83, 45)      # #14532D
PALE_BG    = RGBColor(246, 244, 240)   # #F6F4F0
WHITE      = RGBColor(255, 255, 255)   # #FFFFFF
DARK_INK   = RGBColor(27, 36, 48)      # #1B2430
MUTED      = RGBColor(89, 101, 115)    # #596573
AMBER      = RGBColor(180, 83, 9)      # #B45309
MINT_TINT  = RGBColor(221, 232, 216)   # #DDE8D8
BORDER_COL = RGBColor(218, 222, 215)   # #DADED7
CARD_BG    = RGBColor(255, 255, 255)

FONT_HEADING = "Aptos"
FONT_BODY    = "Aptos"

def set_slide_background(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(20), Inches(11.25))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_header(slide, slide_num, title, subtitle, is_dark=False):
    # Slide Number pill
    num_box = slide.shapes.add_textbox(Inches(1.2), Inches(0.8), Inches(1.5), Inches(0.6))
    tf_num = num_box.text_frame
    tf_num.word_wrap = True
    p_num = tf_num.paragraphs[0]
    p_num.text = slide_num
    p_num.font.name = FONT_HEADING
    p_num.font.size = Pt(16)
    p_num.font.bold = True
    p_num.font.color.rgb = MINT_TINT if is_dark else AMBER

    # Title & Subtitle box
    head_box = slide.shapes.add_textbox(Inches(2.4), Inches(0.7), Inches(16.4), Inches(1.8))
    tf = head_box.text_frame
    tf.word_wrap = True
    
    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE if is_dark else DARK_INK
    p_title.space_after = Pt(6)

    p_sub = tf.add_paragraph()
    p_sub.text = subtitle
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = MINT_TINT if is_dark else MUTED

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COL):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
    else:
        card.line.fill.background()
    return card

def main():
    prs = pptx.Presentation()
    prs.slide_width = Inches(20.0)
    prs.slide_height = Inches(11.25)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TindaWise Title
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, DARK_GREEN)

    # Number pill
    p1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.2), Inches(1.5), Inches(0.6))
    p1.text_frame.paragraphs[0].text = "01"
    p1.text_frame.paragraphs[0].font.name = FONT_HEADING
    p1.text_frame.paragraphs[0].font.size = Pt(18)
    p1.text_frame.paragraphs[0].font.bold = True
    p1.text_frame.paragraphs[0].font.color.rgb = MINT_TINT

    # Big Brand Title & Subtitle
    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.5), Inches(7.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "TindaWise"
    p.font.name = FONT_HEADING
    p.font.size = Pt(76)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = "Taglish Voice-to-Lista Copilot"
    p.font.name = FONT_HEADING
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = MINT_TINT
    p.space_after = Pt(24)

    p = tf1.add_paragraph()
    p.text = "Hands-free counter credit recording for Philippine neighborhood sari-sari stores."
    p.font.name = FONT_BODY
    p.font.size = Pt(22)
    p.font.color.rgb = WHITE
    p.space_after = Pt(16)

    p = tf1.add_paragraph()
    p.text = "MSME Operations Track • Tech Connect: SYNC AIdeathon 2026"
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.color.rgb = MINT_TINT
    p.space_after = Pt(28)

    # Workflow badge
    badge = add_card(s1, Inches(1.5), Inches(7.8), Inches(7.2), Inches(1.2), bg_color=MINT_TINT, border_color=None)
    tb_b = s1.shapes.add_textbox(Inches(1.7), Inches(8.0), Inches(6.8), Inches(0.8))
    p = tb_b.text_frame.paragraphs[0]
    p.text = "SPEAK TAGLISH  →  REVIEW DRAFT  →  CONFIRM TO SAVE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN

    # Real Phone Screenshot Embed
    img_hero = os.path.join(SCREENS_DIR, "screen_confirm_p58.png")
    if os.path.exists(img_hero):
        add_card(s1, Inches(12.8), Inches(1.2), Inches(5.8), Inches(9.0), bg_color=DARK_INK, border_color=MINT_TINT)
        s1.shapes.add_picture(img_hero, Inches(13.2), Inches(1.5), Inches(5.0), Inches(8.4))

    s1.notes_slide.notes_text_frame.text = (
        "SLIDE 1 | TIMING: 8s | WORDS: 16\n\n"
        "NARRATION (120-Second Pitch Script):\n"
        "\"This is TindaWise—a hands-free Taglish voice-to-lista copilot designed for sari-sari store counter operations.\"\n\n"
        "SPEAKER & SOURCE NOTES:\n"
        "- Positioning: MSME Operations track, BatStateU The NEU – Alangilan (STEER Hub).\n"
        "- Demonstrates a focused counter application solving solo storekeeper friction without complex menus."
    )

    # =========================================================================
    # SLIDE 2: The Counter Problem
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, PALE_BG)
    add_header(s2, "02", "The Counter Problem", 
               "Verified store-owner interviews reveal two distinct debt-tracking workflows—both underserved by conventional apps.")

    # Two large workflow comparison cards (without respondent names / direct quotes)
    # Card 1: Memory-Based Workflow
    c1 = add_card(s2, Inches(1.5), Inches(2.7), Inches(8.2), Inches(6.0))
    tb_c1 = s2.shapes.add_textbox(Inches(1.9), Inches(3.0), Inches(7.4), Inches(5.4))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True

    p = tf_c1.paragraphs[0]
    p.text = "WORKFLOW PATTERN 1"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p.space_after = Pt(8)

    p = tf_c1.add_paragraph()
    p.text = "Memory-Based Lending (Trust-First)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN
    p.space_after = Pt(14)

    p = tf_c1.add_paragraph()
    p.text = "• Practice: Flexible customer credit extended on personal trust without consistent written documentation."
    p.font.name = FONT_BODY
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_INK
    p.space_after = Pt(10)

    p = tf_c1.add_paragraph()
    p.text = "• The Bottleneck: During 5:00 PM rush periods, writing takes too much effort; unrecorded credit risks being forgotten or disputed."
    p.font.name = FONT_BODY
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_INK
    p.space_after = Pt(14)

    p = tf_c1.add_paragraph()
    p.text = "Design Goal: Make recording completely effortless (3-second spoken sentence) so trust does not mean lost capital."
    p.font.name = FONT_HEADING
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN

    # Card 2: Paper-Based Workflow
    c2 = add_card(s2, Inches(10.3), Inches(2.7), Inches(8.2), Inches(6.0))
    tb_c2 = s2.shapes.add_textbox(Inches(10.7), Inches(3.0), Inches(7.4), Inches(5.4))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True

    p = tf_c2.paragraphs[0]
    p.text = "WORKFLOW PATTERN 2"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p.space_after = Pt(8)

    p = tf_c2.add_paragraph()
    p.text = "Paper Kwaderno (Notebook-First)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN
    p.space_after = Pt(14)

    p = tf_c2.add_paragraph()
    p.text = "• Practice: Selective credit granted to trusted regular customers, recorded by hand in a notebook."
    p.font.name = FONT_BODY
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_INK
    p.space_after = Pt(10)

    p = tf_c2.add_paragraph()
    p.text = "• The Bottleneck: Customers forget past debts; looking up old entries takes time. Owners hesitate to use conventional mobile apps due to complex menus and typing."
    p.font.name = FONT_BODY
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_INK
    p.space_after = Pt(14)

    p = tf_c2.add_paragraph()
    p.text = "Design Goal: Make past entries instantly accessible during face-to-face counter interactions without complex navigation."
    p.font.name = FONT_HEADING
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN

    # Bottom summary bar
    bot_b = add_card(s2, Inches(1.5), Inches(9.0), Inches(17.0), Inches(1.4), bg_color=DARK_GREEN, border_color=None)
    tb_bot = s2.shapes.add_textbox(Inches(1.8), Inches(9.1), Inches(16.4), Inches(1.2))
    p = tb_bot.text_frame.paragraphs[0]
    p.text = "The Counter Reality: Barcodes do not exist on repacked 'tingi' goods (sugar, rice, oil). Conventional apps demand 6-8 screen taps while hands are occupied. TindaWise preserves existing trust while eliminating manual friction."
    p.font.name = FONT_BODY
    p.font.size = Pt(17)
    p.font.color.rgb = WHITE

    s2.notes_slide.notes_text_frame.text = (
        "SLIDE 2 | TIMING: 16s | WORDS: 33\n\n"
        "NARRATION (120-Second Pitch Script):\n"
        "\"Store owners extend credit on trust. Memory-based lenders risk forgetting transactions during peak counter rush, while paper kwaderno users face slow manual lookup. Existing mobile apps fail because typing and barcodes don't fit busy hands.\"\n\n"
        "SPEAKER & SOURCE NOTES:\n"
        "- Interview Evidence: Based on 2 verified field interviews (Kuya Ronny, 147.5s, timestamp 00:33 'tiwala na lang po'; Ate Mina, 208.7s, timestamp 01:45 'Uy may utang ka pa dito', timestamp 03:08 'hindi ako maalam sa cellphone').\n"
        "- Third recording (Ate Josefina, 229.5s) was excluded from findings due to heavy background acoustic noise preventing reliable attribution.\n"
        "- Summarized without respondent names or direct quotes to maintain professional evidence standards."
    )

    # =========================================================================
    # SLIDE 3: Speak -> Review -> Save
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, PALE_BG)
    add_header(s3, "03", "Speak → Review → Save", 
               "One natural spoken sentence becomes an accurate, verified entry with owner-controlled receipts.")

    # 3 Columns: Spoken Flow, Real Confirmation Screens, SMS Handoff
    # Column 1: Spoken Taglish Input
    c1 = add_card(s3, Inches(1.2), Inches(2.7), Inches(5.4), Inches(7.6))
    tb_c1 = s3.shapes.add_textbox(Inches(1.5), Inches(3.0), Inches(4.8), Inches(7.0))
    tf1 = tb_c1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "STEP 1: SAY IT IN TAGLISH"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "Spoken Grocery Entry (₱58 Example):"
    p.font.name = FONT_HEADING
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN
    p.space_after = Pt(6)

    p = tf1.add_paragraph()
    p.text = "“Palista kay Aling Nena dalawang Lucky Me canton saka isang sardinas, sa Sabado bayad.”"
    p.font.name = FONT_BODY
    p.font.size = Pt(18)
    p.font.italic = True
    p.font.color.rgb = DARK_INK
    p.space_after = Pt(20)

    p = tf1.add_paragraph()
    p.text = "Compact Direct-Peso Entry (₱50 Example):"
    p.font.name = FONT_HEADING
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN
    p.space_after = Pt(6)

    p = tf1.add_paragraph()
    p.text = "“Palista kay Kuya Ronny singkwenta pesos na ulam, bukas bayad.”"
    p.font.name = FONT_BODY
    p.font.size = Pt(18)
    p.font.italic = True
    p.font.color.rgb = DARK_INK
    p.space_after = Pt(20)

    p = tf1.add_paragraph()
    p.text = "• 3-Second Spoken Capture\n• Zero screen typing required\n• Hands remain free for store goods"
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.color.rgb = MUTED

    # Column 2: Real Confirmation Screen Embed (₱58)
    c2 = add_card(s3, Inches(6.9), Inches(2.7), Inches(6.0), Inches(7.6))
    tb_c2 = s3.shapes.add_textbox(Inches(7.2), Inches(3.0), Inches(5.4), Inches(1.2))
    p = tb_c2.text_frame.paragraphs[0]
    p.text = "STEP 2: REVIEW DETERMINISTIC DRAFT"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = AMBER

    p = tb_c2.text_frame.add_paragraph()
    p.text = "Exact Catalog Math (Total: ₱58.00)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN

    img_p58 = os.path.join(SCREENS_DIR, "screen_confirm_p58.png")
    if os.path.exists(img_p58):
        s3.shapes.add_picture(img_p58, Inches(7.5), Inches(4.3), Inches(4.8), Inches(5.7))

    # Column 3: SMS Banner & Direct-Peso Screen Embed
    c3 = add_card(s3, Inches(13.2), Inches(2.7), Inches(5.6), Inches(7.6))
    tb_c3 = s3.shapes.add_textbox(Inches(13.5), Inches(3.0), Inches(5.0), Inches(1.2))
    p = tb_c3.text_frame.paragraphs[0]
    p.text = "STEP 3: CONFIRM & MANUAL SMS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = AMBER

    p = tb_c3.text_frame.add_paragraph()
    p.text = "Owner-Controlled Counter SMS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN

    img_sms = os.path.join(SCREENS_DIR, "screen_sms_banner.png")
    if os.path.exists(img_sms):
        s3.shapes.add_picture(img_sms, Inches(13.6), Inches(4.3), Inches(4.8), Inches(5.7))

    s3.notes_slide.notes_text_frame.text = (
        "SLIDE 3 | TIMING: 22s | WORDS: 46\n\n"
        "NARRATION (120-Second Pitch Script):\n"
        "\"The counter workflow takes three seconds: speak a natural Taglish sentence, review the extracted draft, and confirm. It supports catalog items like this ₱58 grocery entry, one-tap direct peso logging like ₱50 ulam, and manual owner-initiated SMS receipts that preserve neighborhood pakikisama.\"\n\n"
        "SPEAKER & SOURCE NOTES:\n"
        "- Product Screenshots: Captured directly from live Android WebView container on emulator using fictional customer records (Aling Nena, Kuya Ronny).\n"
        "- Direct Peso support enables logging without prior inventory cataloging (Implication #6 from research).\n"
        "- Owner-Initiated SMS: Drafts polite reminder on owner's phone via smsto: intent; avoids third-party aggregator liabilities under RA 10173."
    )

    # =========================================================================
    # SLIDE 4: Where AI Adds Value
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, PALE_BG)
    add_header(s4, "04", "Where AI Adds Value", 
               "Speech recognition and cognitive entity extraction paired with deterministic financial safety guardrails.")

    # 4 Architecture Stages
    stages = [
        ("01", "SPEECH RECOGNITION", "Perceptual AI",
         "• Android RecognizerIntent (fil-PH) / local Whisper.\n• Transcribes acoustic Taglish in counter noise.\n• 0-Day Audio Retention: In-memory only, no audio files saved to disk."),
        ("02", "COGNITIVE EXTRACTION", "The Core AI Engine",
         "• Extracts: {debtor, sku, quantity, due_date}.\n• Normalizes fractional units (kalahati=0.5, 1/4=0.25).\n• Dual Engine: Gemini 2.5 Flash cloud or local rule-based Taglish parser (0 ms, offline)."),
        ("03", "CATALOG PRICING", "Deterministic Guardrail",
         "• MODEL NEVER GUESSES PRICES.\n• Unit prices retrieved strictly from owner price list.\n• Exact Decimal arithmetic sums line items.\n• AI hallucination cannot corrupt money."),
        ("04", "OWNER APPROVAL", "Human-in-the-Loop",
         "• Visual Confirmation Card with +/- steppers.\n• 1-tap correction before mutating ledger.\n• Template-based, owner-initiated Tagalog reminder drafts.")
    ]

    col_w = Inches(4.1)
    col_gap = Inches(0.4)
    start_x = Inches(1.2)

    for idx, (num, title, badge_txt, desc) in enumerate(stages):
        x = start_x + idx * (col_w + col_gap)
        is_highlight = (idx == 2)
        card_bg = DARK_GREEN if is_highlight else CARD_BG
        txt_col = WHITE if is_highlight else DARK_INK
        sub_col = MINT_TINT if is_highlight else AMBER

        card = add_card(s4, x, Inches(2.7), col_w, Inches(6.4), 
                        bg_color=card_bg, border_color=AMBER if is_highlight else BORDER_COL)
        tb = s4.shapes.add_textbox(x + Inches(0.3), Inches(3.0), col_w - Inches(0.6), Inches(5.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{num} / {badge_txt.upper()}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = sub_col
        p.space_after = Pt(8)

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = txt_col
        p.space_after = Pt(14)

        for line in desc.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = FONT_BODY
            p.font.size = Pt(16)
            if "NEVER GUESSES" in line:
                p.font.bold = True
                p.font.color.rgb = WHITE if is_highlight else AMBER
            else:
                p.font.color.rgb = txt_col
            p.space_after = Pt(6)

    # Bottom Guardrail Banner
    bb = add_card(s4, Inches(1.2), Inches(9.3), Inches(17.6), Inches(1.1), bg_color=WHITE, border_color=DARK_GREEN)
    tb_bb = s4.shapes.add_textbox(Inches(1.5), Inches(9.4), Inches(17.0), Inches(0.9))
    p = tb_bb.text_frame.paragraphs[0]
    p.text = "Financial Safety Boundary: The AI model handles language interpretation only. All peso calculations are computed in plain code against the store owner's local price list. Wrong AI outputs can never corrupt ledger balances."
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN

    s4.notes_slide.notes_text_frame.text = (
        "SLIDE 4 | TIMING: 18s | WORDS: 38\n\n"
        "NARRATION (120-Second Pitch Script):\n"
        "\"Acoustic speech models transcribe Taglish audio. Cognitive NLP—via Gemini 2.5 Flash or an offline local parser—extracts debtor, items, and quantities. Crucially, the AI never guesses prices: deterministic arithmetic looks up verified store prices before owner confirmation.\"\n\n"
        "SPEAKER & SOURCE NOTES:\n"
        "- Architecture: 3-layer system separating acoustic perception, semantic entity parsing, and deterministic financial arithmetic.\n"
        "- Cloud vs Offline: On-device parser achieves ~1.4 ms latency with zero internet. Gemini 2.5 Flash provides structured JSON schema cloud extraction.\n"
        "- Privacy: Audio processed in RAM; 0-day retention aligns with Philippine Data Privacy Act (RA 10173)."
    )

    # =========================================================================
    # SLIDE 5: Prototype and Results
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, PALE_BG)
    add_header(s5, "05", "Prototype & Empirical Results", 
               "Verified measurements from our standalone signed Android APK and multi-speaker Taglish benchmark.")

    # 3 Stat Cards
    metrics = [
        ("94.4%", "Item & Quantity Matching", "34 / 36 Benchmark Matches",
         "Tested across 36 stored Taglish utterances from 6 distinct speakers under 4 counter noise conditions (quiet counter, electric fan, street tricycle, radio chatter)."),
        ("73.4%", "Lower Logging Time", "6.76s Voice vs. 25.46s Paper",
         "Measured end-to-end time to record a multi-item debt entry. Voice + owner confirmation averaged 6.76 seconds versus 25.46 seconds to find page and write by hand."),
        ("100%", "Deterministic Ledger Math", "0 Balance Errors Post-Confirm",
         "Packaged and signed Android prototype (TindaWise-v1.0.0.apk) verified with V2/V3 schemes, ensuring exact Decimal calculations against store price list.")
    ]

    card_w = Inches(5.6)
    card_gap = Inches(0.4)
    start_x = Inches(1.2)

    for idx, (stat, title, sub_metric, methodology) in enumerate(metrics):
        x = start_x + idx * (card_w + card_gap)
        card = add_card(s5, x, Inches(2.7), card_w, Inches(6.0), bg_color=CARD_BG, border_color=BORDER_COL)
        tb = s5.shapes.add_textbox(x + Inches(0.4), Inches(3.0), card_w - Inches(0.8), Inches(5.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = stat
        p.font.name = FONT_HEADING
        p.font.size = Pt(64)
        p.font.bold = True
        p.font.color.rgb = DARK_GREEN
        p.space_after = Pt(8)

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = DARK_INK
        p.space_after = Pt(6)

        p = tf.add_paragraph()
        p.text = sub_metric
        p.font.name = FONT_HEADING
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = AMBER
        p.space_after = Pt(16)

        p = tf.add_paragraph()
        p.text = methodology
        p.font.name = FONT_BODY
        p.font.size = Pt(16)
        p.font.color.rgb = MUTED

    # Bottom Prototype Box
    pb = add_card(s5, Inches(1.2), Inches(8.9), Inches(17.6), Inches(1.5), bg_color=DARK_GREEN, border_color=None)
    tb_pb = s5.shapes.add_textbox(Inches(1.5), Inches(9.0), Inches(17.0), Inches(1.3))
    tf_pb = tb_pb.text_frame
    tf_pb.word_wrap = True

    p = tf_pb.paragraphs[0]
    p.text = "Standalone Android Prototype (TindaWise-v1.0.0.apk) Highlights:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = MINT_TINT
    p.space_after = Pt(4)

    p = tf_pb.add_paragraph()
    p.text = "• Fully functional APK verified via apksigner (V2 & V3 schemes) • Built-in Push-to-Talk speech-to-text bridge • Direct Counter SMS banner with native smsto: composer • 100% offline-ready with local storage."
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.color.rgb = WHITE

    s5.notes_slide.notes_text_frame.text = (
        "SLIDE 5 | TIMING: 13s | WORDS: 28\n\n"
        "NARRATION (120-Second Pitch Script):\n"
        "\"We built a verified, signed Android prototype. In benchmark tests across thirty-six multi-speaker Taglish utterances, extraction reached 94.4% accuracy, saving 73.4% of the time required by paper notebook logging.\"\n\n"
        "SPEAKER & SOURCE NOTES:\n"
        "- Benchmark Methodology: Run via src/eval/evaluate_voice_utang.py on 36 multi-speaker Taglish utterances.\n"
        "- Timing Calculation: Paper kwaderno baseline averaged 25.46 seconds across multi-item transactions; TindaWise voice + confirmation averaged 6.76 seconds (73.4% reduction).\n"
        "- APK Verification: apksigner verify confirmed v2 and v3 signatures on TindaWise-v1.0.0.apk."
    )

    # =========================================================================
    # SLIDE 6: Market and Differentiation
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, PALE_BG)
    add_header(s6, "06", "Market Opportunity & Differentiation", 
               "Focusing on the high-frequency counter interaction where existing enterprise & POS apps do not fit.")

    # Left Box: Market Context (Dated DTI figure, Batangas beachhead)
    c_mkt = add_card(s6, Inches(1.2), Inches(2.7), Inches(5.8), Inches(7.6))
    tb_m = s6.shapes.add_textbox(Inches(1.5), Inches(3.0), Inches(5.2), Inches(7.0))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True

    p = tf_m.paragraphs[0]
    p.text = "MARKET CONTEXT"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p.space_after = Pt(10)

    p = tf_m.add_paragraph()
    p.text = "1.3M+ Stores"
    p.font.name = FONT_HEADING
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN
    p.space_after = Pt(4)

    p = tf_m.add_paragraph()
    p.text = "Nationwide Sari-Sari Store Presence"
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_INK
    p.space_after = Pt(8)

    p = tf_m.add_paragraph()
    p.text = "According to 2024 Department of Trade and Industry (DTI) data reported via the Philippine Information Agency (PIA), over 1.3 million sari-sari stores operate across the country, serving as micro-retail backbones."
    p.font.name = FONT_BODY
    p.font.size = Pt(15)
    p.font.color.rgb = MUTED
    p.space_after = Pt(18)

    p = tf_m.add_paragraph()
    p.text = "Initial Starting Segment: Batangas"
    p.font.name = FONT_HEADING
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN
    p.space_after = Pt(6)

    p = tf_m.add_paragraph()
    p.text = "Targeting neighborhood sari-sari stores and public market vendors across Batangas City and Alangilan community for initial prototype pilots."
    p.font.name = FONT_BODY
    p.font.size = Pt(15)
    p.font.color.rgb = MUTED

    # Right Box: Documented Competitor Comparison Table
    c_comp = add_card(s6, Inches(7.4), Inches(2.7), Inches(11.4), Inches(7.6))
    tb_c = s6.shapes.add_textbox(Inches(7.8), Inches(3.0), Inches(10.6), Inches(7.0))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "DOCUMENTED COMPETITOR POSITIONING"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p.space_after = Pt(12)

    # Competitor breakdown
    comps = [
        ("Peddlr", "Digital POS & Inventory Bookkeeping",
         "Documented Focus: Mobile POS, camera barcode scanning, inventory restock tracking, and credit ledger. Counter Gap: Requires barcode scanning or manual screen navigation; unbarcoded repacked tingi items require multiple manual taps."),
        ("Lista PH", "Financial Cashflow & Credit Tracking",
         "Documented Focus: Money In/Out management, debt tracking, customer SMS reminders, and credit score marketplace. Counter Gap: Designed for after-the-fact peso-total typing rather than hands-free itemized counter credit logging."),
        ("Packworks", "B2B FMCG Supply Chain & POS Analytics",
         "Documented Focus: B2B inventory procurement, distribution infrastructure, and DOST-supported store analytics. Counter Gap: Focuses on wholesale brand distribution rather than solo-storekeeper conversational counter utang capture."),
        ("TindaWise", "Hands-Free Spoken Counter Voice Copilot",
         "Our Distinct Wedge: Built specifically for the 3-second counter moment when hands are occupied. Spoken Taglish extraction, fractional tingi support, deterministic owner pricing, and manual polite reminders.")
    ]

    for name, focus, notes in comps:
        is_tw = (name == "TindaWise")
        p = tf_c.add_paragraph()
        p.text = f"{name} — {focus}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = DARK_GREEN if is_tw else DARK_INK
        p.space_after = Pt(3)

        p = tf_c.add_paragraph()
        p.text = notes
        p.font.name = FONT_BODY
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_GREEN if is_tw else MUTED
        p.space_after = Pt(12)

    s6.notes_slide.notes_text_frame.text = (
        "SLIDE 6 | TIMING: 16s | WORDS: 34\n\n"
        "NARRATION (120-Second Pitch Script):\n"
        "\"The DTI reports over 1.3 million sari-sari stores nationwide, with Batangas as our beachhead. While Peddlr focuses on POS inventory, Lista on financial bookkeeping, and Packworks on B2B supply, TindaWise uniquely owns hands-free counter logging.\"\n\n"
        "SPEAKER & SOURCE NOTES:\n"
        "- Market Data: DTI 2024 statistics published via Philippine Information Agency (PIA) release on MSME micro-enterprises.\n"
        "- Starting segment: Neighborhood stores in Batangas City / Alangilan without claiming unverified local store counts or credit adoption rates.\n"
        "- Competitors: Based on official Play Store listings and public product documentation (Peddlr POS, Lista PH cashflow app, Packworks Sari.PH Pro B2B network)."
    )

    # =========================================================================
    # SLIDE 7: Path to a Business
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, PALE_BG)
    add_header(s7, "07", "Path to a Business", 
               "Direct onboarding with the store owner as buyer, leading with a free pilot before testing future value hypotheses.")

    # 3 Strategy Cards
    bus_cards = [
        ("01", "DIRECT BUYER RELATIONSHIP", "Zero Institutional Gatekeepers",
         "• The solo storekeeper is the direct decision-maker.\n• No dependence on 12-month LGU procurement cycles or bank partner approvals.\n• Frictionless onboarding via direct APK installation or offline-first web container."),
        ("02", "FREE COUNTER PILOT FIRST", "Adoption & Trust Baseline",
         "• Core voice-to-lista, local kwaderno ledger, on-device NLP, and manual SMS drafts are 100% free.\n• Eliminates financial risk for hesitant owners.\n• Establishes daily counter habit and verifies real-world retention before introducing fees."),
        ("03", "FUTURE VALUE HYPOTHESES", "Testing Willingness to Pay",
         "• Hypothesis A (Cloud Sync): ₱49/mo optional automated cloud backup for multi-device store families.\n• Hypothesis B (Wholesale Compare): Supplier price benchmarks across local wholesalers.\n• Tested as post-pilot commercial hypotheses.")
    ]

    card_w = Inches(5.6)
    card_gap = Inches(0.4)
    start_x = Inches(1.2)

    for idx, (num, title, sub, desc) in enumerate(bus_cards):
        x = start_x + idx * (card_w + card_gap)
        card = add_card(s7, x, Inches(2.7), card_w, Inches(6.0), bg_color=CARD_BG, border_color=BORDER_COL)
        tb = s7.shapes.add_textbox(x + Inches(0.4), Inches(3.0), card_w - Inches(0.8), Inches(5.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{num} / STRATEGY"
        p.font.name = FONT_HEADING
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = AMBER
        p.space_after = Pt(8)

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = DARK_GREEN
        p.space_after = Pt(6)

        p = tf.add_paragraph()
        p.text = sub
        p.font.name = FONT_HEADING
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = DARK_INK
        p.space_after = Pt(16)

        for line in desc.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = FONT_BODY
            p.font.size = Pt(16)
            p.font.color.rgb = MUTED
            p.space_after = Pt(6)

    # Bottom Callout Box
    cb = add_card(s7, Inches(1.2), Inches(9.0), Inches(17.6), Inches(1.4), bg_color=WHITE, border_color=DARK_GREEN)
    tb_cb = s7.shapes.add_textbox(Inches(1.5), Inches(9.1), Inches(17.0), Inches(1.2))
    p = tb_cb.text_frame.paragraphs[0]
    p.text = "Commercial Discipline: We do not claim instant paid SaaS adoption from micro-merchants. We prove daily utility and retention through a free pilot first, validating operational delivery costs and actual willingness to pay before monetizing."
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_GREEN

    s7.notes_slide.notes_text_frame.text = (
        "SLIDE 7 | TIMING: 13s | WORDS: 28\n\n"
        "NARRATION (120-Second Pitch Script):\n"
        "\"The store owner is our direct buyer. We begin with a free counter pilot, testing future willingness to pay for optional cloud backup, multi-device family access, and supplier price comparisons.\"\n\n"
        "SPEAKER & SOURCE NOTES:\n"
        "- Business Model Rubric Alignment: Addresses 20 pts in Final Round.\n"
        "- Clear Buyer: Solo sari-sari store owner (zero enterprise procurement barriers).\n"
        "- Commercial Roadmap: Direct free onboarding establishes product habit; premium tiers (cloud backup, multi-device sync, analytics) treated as validated hypotheses."
    )

    # =========================================================================
    # SLIDE 8: Pilot and Next Milestones
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, PALE_BG)
    add_header(s8, "08", "Pilot Execution & Next Milestones", 
               "Structured field execution to validate repeat usage, user feedback, and operating costs.")

    # 4 Milestone Cards
    steps = [
        ("PHASE 1", "Recruit Willing Owners", "Month 1 (Immediate)",
         "• Onboard 15–20 pilot sari-sari stores in Batangas City / Alangilan.\n• Sideload Android prototype APK onto owners' phones.\n• Assist in initial price catalog setup for top 10 store SKUs."),
        ("PHASE 2", "Observe Daily Counter Use", "Month 2 (Field Shadowing)",
         "• Conduct counter observation during 5:00 PM peak rush hours.\n• Measure voice recognition accuracy in live street noise.\n• Track usage frequency of 1-tap fallback and direct peso entries."),
        ("PHASE 3", "Assess Repeat Retention", "Month 3 (Habit Verification)",
         "• Evaluate 30-day active retention: do owners continue logging without prompting?\n• Interview owners on forgotten transaction recovery.\n• Document user friction and feature requests."),
        ("PHASE 4", "Validate Delivery Costs", "Month 4+ (Scale Readiness)",
         "• Measure actual API cost per transaction (Gemini vs on-device NLP).\n• Test willingness to pay for optional cloud sync.\n• Prepare release packaging for broader regional rollout.")
    ]

    col_w = Inches(4.1)
    col_gap = Inches(0.4)
    start_x = Inches(1.2)

    for idx, (phase, title, timeframe, desc) in enumerate(steps):
        x = start_x + idx * (col_w + col_gap)
        card = add_card(s8, x, Inches(2.7), col_w, Inches(6.4), bg_color=CARD_BG, border_color=BORDER_COL)
        tb = s8.shapes.add_textbox(x + Inches(0.3), Inches(3.0), col_w - Inches(0.6), Inches(5.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = phase
        p.font.name = FONT_HEADING
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = AMBER
        p.space_after = Pt(6)

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = DARK_GREEN
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = timeframe
        p.font.name = FONT_HEADING
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = DARK_INK
        p.space_after = Pt(14)

        for line in desc.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = FONT_BODY
            p.font.size = Pt(16)
            p.font.color.rgb = MUTED
            p.space_after = Pt(6)

    # Bottom Milestone Banner
    mb = add_card(s8, Inches(1.2), Inches(9.3), Inches(17.6), Inches(1.1), bg_color=DARK_GREEN, border_color=None)
    tb_mb = s8.shapes.add_textbox(Inches(1.5), Inches(9.4), Inches(17.0), Inches(0.9))
    p = tb_mb.text_frame.paragraphs[0]
    p.text = "Execution Target: Dec 3 Demo Day Showcase at BatStateU STEER Hub with verified pilot evidence, live owner feedback, and hands-on judge demo."
    p.font.name = FONT_HEADING
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE

    s8.notes_slide.notes_text_frame.text = (
        "SLIDE 8 | TIMING: 8s | WORDS: 18\n\n"
        "NARRATION (120-Second Pitch Script):\n"
        "\"Our milestone: recruit pilot owners in Batangas, observe daily counter tasks, measure repeat adoption, and validate operational costs.\"\n\n"
        "SPEAKER & SOURCE NOTES:\n"
        "- Milestones: Directly aligns with AIdeathon mentoring sessions (Customer Discovery, AI Prototyping, Business Model).\n"
        "- Validates live counter adoption before making commercial expansion claims."
    )

    # =========================================================================
    # SLIDE 9: Closing
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, DARK_GREEN)

    # Slide number
    p9 = s9.shapes.add_textbox(Inches(1.5), Inches(1.2), Inches(1.5), Inches(0.6))
    p9.text_frame.paragraphs[0].text = "09"
    p9.text_frame.paragraphs[0].font.name = FONT_HEADING
    p9.text_frame.paragraphs[0].font.size = Pt(18)
    p9.text_frame.paragraphs[0].font.bold = True
    p9.text_frame.paragraphs[0].font.color.rgb = MINT_TINT

    # Big Brand Title & Tagline
    tb9 = s9.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(11.5), Inches(7.5))
    tf9 = tb9.text_frame
    tf9.word_wrap = True

    p = tf9.paragraphs[0]
    p.text = "TindaWise"
    p.font.name = FONT_HEADING
    p.font.size = Pt(88)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(16)

    p = tf9.add_paragraph()
    p.text = "Tindahang maayos, suking maasahan."
    p.font.name = FONT_HEADING
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = MINT_TINT
    p.space_after = Pt(28)

    p = tf9.add_paragraph()
    p.text = "Try the Android prototype today."
    p.font.name = FONT_BODY
    p.font.size = Pt(24)
    p.font.color.rgb = WHITE
    p.space_after = Pt(16)

    p = tf9.add_paragraph()
    p.text = "• Standalone signed APK ready for live installation\n• 100% offline-first architecture with zero audio storage\n• Preserving community trust for Philippine sari-sari stores"
    p.font.name = FONT_BODY
    p.font.size = Pt(18)
    p.font.color.rgb = MINT_TINT
    p.space_after = Pt(24)

    # QR Code Embed on the right
    qr_img = os.path.join(SCREENS_DIR, "qr_tindawise_repo.png")
    if os.path.exists(qr_img):
        add_card(s9, Inches(13.5), Inches(2.2), Inches(5.0), Inches(6.8), bg_color=WHITE, border_color=MINT_TINT)
        s9.shapes.add_picture(qr_img, Inches(14.0), Inches(2.6), Inches(4.0), Inches(4.0))

        tb_qr = s9.shapes.add_textbox(Inches(13.6), Inches(6.8), Inches(4.8), Inches(2.0))
        tf_qr = tb_qr.text_frame
        tf_qr.word_wrap = True
        p = tf_qr.paragraphs[0]
        p.text = "SCAN FOR PUBLIC REPO & APK"
        p.font.name = FONT_HEADING
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = DARK_GREEN
        p.alignment = PP_ALIGN.CENTER

        p = tf_qr.add_paragraph()
        p.text = "github.com/colkeaz/TindaWise"
        p.font.name = FONT_BODY
        p.font.size = Pt(14)
        p.font.color.rgb = MUTED
        p.alignment = PP_ALIGN.CENTER

    s9.notes_slide.notes_text_frame.text = (
        "SLIDE 9 | TIMING: 6s | WORDS: 13\n\n"
        "NARRATION (120-Second Pitch Script):\n"
        "\"TindaWise: Tindahang maayos, suking maasahan. Try our Android prototype today. Thank you.\"\n\n"
        "SPEAKER & SOURCE NOTES:\n"
        "- Public Repository & APK: https://github.com/colkeaz/TindaWise\n"
        "- Working QR code destination verified publicly accessible."
    )

    prs.save(OUTPUT_PPTX)
    print(f"Successfully generated 9-slide presentation: {OUTPUT_PPTX}")

if __name__ == "__main__":
    main()
