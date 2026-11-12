"""Rebuild the editable TindaWise pitch; dependencies are isolated in .deck-deps."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.pitch-deps'))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement

OUT = ROOT / 'deliverables'
OUT.mkdir(exist_ok=True)
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333333), Inches(7.5)
BG='F6F4F0'; GREEN='14532D'; INK='1B2430'; MUTED='596573'; AMBER='B45309'; PALE='E5EBDD'; WHITE='FFFFFF'; LINE='DCD6C8'
notes=[]

def box(s,x,y,w,h,color,line=None,round=False):
    q=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round else MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    q.fill.solid(); q.fill.fore_color.rgb=RGBColor.from_string(color)
    if line: q.line.color.rgb=RGBColor.from_string(line)
    else: q.line.fill.background()
    if round: q.adjustments[0]=0.12
    q._element.spPr.append(OxmlElement('a:effectLst'))
    return q

def text(s,x,y,w,h,txt,size=24,color=INK,bold=False,font='Aptos',align=None):
    q=s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf=q.text_frame; tf.clear(); tf.word_wrap=True
    tf.margin_left=tf.margin_right=0; tf.margin_top=tf.margin_bottom=0
    for i,line in enumerate(txt.split('\n')):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.text=line; p.font.name=font; p.font.size=Pt(size); p.font.bold=bold; p.font.color.rgb=RGBColor.from_string(color)
        p.space_after=Pt(7)
        if align is not None: p.alignment=align
    return q

def slide(k,title=None,sub=None,dark=False):
    s=prs.slides.add_slide(prs.slide_layouts[6]); s.background.fill.solid(); s.background.fill.fore_color.rgb=RGBColor.from_string(GREEN if dark else BG)
    c=WHITE if dark else GREEN
    text(s,.6,.3,10,.25,'TINDAWISE   /   '+('JUDGES’ Q&A' if k>7 else 'TECH CONNECT: SYNC AIDEATHON 2026'),11,c,True)
    box(s,.6,7.07,12.1,.012,'577C59' if dark else LINE)
    text(s,.6,7.17,11,.18,'TAGLISH VOICE-TO-LISTA  •  BATSTATEU THE NEU – ALANGILAN',9,c)
    text(s,12.2,7.13,.6,.25,f'{k:02d}',12,c,True)
    if title: text(s,.6,.9,12.05,1.32,title,36,c if dark else INK,True)
    if sub: text(s,.63,2.29 if '\n' in (title or '') else 2.03,11.9,.55,sub,19,'DDE8D8' if dark else MUTED)
    return s

def note(s,timing,script,sources,detail=''):
    body=f'TIMING: {timing}\n\nSPEAKER SCRIPT\n{script}\n\nSOURCE NOTES\n{sources}\n\nQUALIFICATIONS / Q&A\n{detail}'
    s.notes_slide.notes_text_frame.text=body
    notes.append((len(prs.slides),timing,script,sources,detail))

# 1 — product introduction
s=slide(1,dark=True)
text(s,.68,1.28,7.7,.92,'TindaWise',60,WHITE,True)
text(s,.7,2.45,7.7,1.3,'Taglish voice-to-lista\nfor sari-sari stores.',34,WHITE,True)
text(s,.72,4.15,7.2,.9,'Record utang. Recall the details.\nKeep the owner in control.',24,'DDE8D8')
box(s,.72,5.6,5.9,.65,'DDE8D8',round=True)
text(s,.97,5.76,5.4,.35,'SPEAK  →  REVIEW  →  SAVE',20,GREEN,True)
box(s,9.01,.85,3.55,5.98,INK,round=True)
s.shapes.add_picture(str(ROOT/'dist/tindawise_apk_live.png'),Inches(9.13),Inches(.99),height=Inches(5.71))
note(s,'0:00–0:08 · 8 seconds','TindaWise turns spoken Taglish into a reviewable utang entry, helping sari-sari store owners record credit while keeping control.',
     'README.md; src/frontend/index.html; dist/tindawise_apk_live.png','Existing Android screenshot, not a new demonstration of live AI.')

# 2 — grounded problem
s=slide(2,'Utang runs on trust.\nRecords need help.','Two owner interviews revealed different habits—and a shared need for easy recall.')
for x,name,tag,body,need in [(.65,'Kuya Ronny','MEMORY & FAMILIARITY','Relies on trust, without\nconsistent written records.','Make recording effortless.'),(6.85,'Ate Mina','PAPER KWADERNO','Writes debts down; reminds\nher suki face-to-face.','Make past entries easy to find.')]:
    box(s,x,2.9,5.8,2.78,WHITE,LINE,True)
    text(s,x+.27,3.15,5.2,.25,tag,12,AMBER,True)
    text(s,x+.27,3.61,5.2,.48,name,28,GREEN,True)
    text(s,x+.27,4.28,5.2,.9,body,22)
    text(s,x+.05,5.96,5.6,.7,need,23,GREEN,True)
note(s,'0:08–0:28 · 20 seconds','For neighborhood stores, utang depends on trust. Our interviews found two habits: Kuya Ronny relies on memory, while Ate Mina keeps a paper kwaderno. Records can be hard to recall, and complex phone workflows create another barrier.',
     'data/research/sarisaristore_interview.md — Interviews 1 and 2, preliminary findings and limitations.',
     'Two qualitative interviews; neither proves adoption, measured financial loss, or market-wide prevalence. The personas are interview respondents, not paying users.')

# 3 — demo with editable confirmation
s=slide(3,'Speak. Review. Save.','One familiar sentence becomes an entry the owner can check.')
box(s,.65,2.88,5.15,2.75,GREEN,round=True)
text(s,.95,3.12,4.5,.25,'01  /  SAY IT IN TAGLISH',12,'DDE8D8',True)
text(s,.95,3.69,4.48,1.65,'“Palista kay Aling Nena\ndalawang Lucky Me canton\nsaka isang sardinas.”',25,WHITE,True)
text(s,5.98,3.94,.6,.7,'→',32,GREEN)
box(s,6.8,2.88,5.85,3.73,WHITE,LINE,True)
text(s,7.08,3.13,5.2,.25,'02  /  REVIEW THE DRAFT',12,AMBER,True)
text(s,7.08,3.57,4.8,.4,'Aling Nena',26,GREEN,True)
text(s,7.08,4.18,3.8,.85,'2 × Canton @ ₱16\n1 × Sardinas @ ₱26',20)
text(s,11.1,4.18,1.1,.85,'₱32\n₱26',20,INK,True)
box(s,7.08,5.11,5.18,.016,LINE)
text(s,7.08,5.31,2.8,.5,'TOTAL',16,MUTED,True)
text(s,10.76,5.2,1.65,.55,'₱58',32,GREEN,True)
box(s,7.08,5.91,5.2,.47,GREEN,round=True)
text(s,7.28,5.99,4.8,.27,'03  /  OWNER CONFIRMS TO SAVE',14,WHITE,True)
text(s,.7,5.96,5.25,.57,'Draft first. Correct errors before saving.',18,MUTED)
note(s,'0:28–0:53 · 25 seconds','The owner says, “Palista kay Aling Nena dalawang Lucky Me canton saka isang sardinas.” TindaWise prepares a draft: two Canton packs at sixteen pesos and one sardines can at twenty-six—fifty-eight pesos. The owner checks the details, corrects any misheard items, then confirms to save it in the local kwaderno.',
     'src/backend/ledger_engine.py — DEFAULT_PRICE_LIST, extract_utang_preview, confirmation flow; src/frontend/index.html — confirmation UI.',
     'Editable explanatory reconstruction of the documented example, not a captured live response. ₱16 × 2 + ₱26 = ₱58. Prices are store-editable.')

# 4 — AI clarity
s=slide(4,'AI extracts the details.\nThe owner approves the entry.','Speech recognition supplies text; optional Gemini interprets the Taglish transaction.')
steps=[('01','SPEECH → TEXT','Device / browser\nspeech recognition'),('02','AI EXTRACTION','Customer, items,\nquantities, due date'),('03','CATALOG PRICING','Store prices ×\nitem quantities'),('04','OWNER REVIEW','Check, correct,\nconfirm & save')]
for i,(n,h,b) in enumerate(steps):
    x=.65+i*3.08
    box(s,x,2.95,2.83,2.46,GREEN if i==1 else WHITE,None if i==1 else LINE,True)
    text(s,x+.23,3.16,2.35,.45,n,25,'DDE8D8' if i==1 else AMBER,True)
    text(s,x+.23,3.88,2.45,.3,h,13,WHITE if i==1 else GREEN,True)
    text(s,x+.23,4.42,2.4,.76,b,18,WHITE if i==1 else INK)
    if i<3: text(s,x+2.87,3.88,.22,.35,'›',19,GREEN,True)
box(s,.65,5.77,12.05,.68,PALE,round=True)
text(s,.9,5.96,11.5,.32,'Local rule-based fallback + tap entry   •   Catalog prices are not generated by AI',18,GREEN,True)
note(s,'0:53–1:18 · 25 seconds','Here is the AI’s role. Speech recognition supplies text. Optional Gemini extracts the customer, products, quantities, and due date. Catalog prices drive the calculation, and the owner approves the entry. A local rule-based parser provides a fallback. Cloud AI needs internet; voice availability depends on the device.',
     'src/frontend/index.html — extractViaGemini, extractTaglishUtang, toggleVoiceCapture; src/backend/ledger_engine.py — _extract_via_gemini; Android MainActivity.java — speech recognition bridge.',
     'Gemini is optional, with local mode the default. Rule-based parsing is not an on-device generative model. Speech recognition is a separate service. Cloud requests include transaction text and SKU catalog information. Extraction may be wrong; review remains essential. Python backend uses Decimal; browser implementation uses JavaScript calculations rounded to cents.')

# 5 — counter fit
s=slide(5,'Built around the counter.','Simple actions for the moments when owners need them.')
for x,num,title,body in [(.65,'01','Too noisy to speak?','Use quick-peso or\nproduct taps.'),(4.77,'02','A suki walks by?','Find the balance and\nitemized history.'),(8.89,'03','Time for a reminder?','Review a personal\nreminder. Send manually.')]:
    box(s,x,2.96,3.78,2.76,WHITE,LINE,True)
    text(s,x+.25,3.2,3.2,.5,num,31,AMBER,True)
    text(s,x+.25,3.95,3.3,.72,title,23,GREEN,True)
    text(s,x+.25,4.71,3.3,.87,body,20)
text(s,.7,6.12,11.9,.42,'Filipino labels. Optional due dates. Familiar names.',24,GREEN,True)
note(s,'1:18–1:35 · 17 seconds','At a noisy counter, owners can tap peso amounts instead. When a suki passes by, they can retrieve the balance and itemized history. Filipino labels, optional due dates, and owner-controlled reminders fit the familiar kwaderno workflow.',
     'src/frontend/index.html — tap controls, debtor history, reminders; src/backend/ledger_engine.py — direct peso, get_debtor_history, reminders; data/research/sarisaristore_interview.md.',
     'Feature presence is not evidence that owners find it easier. Reminders remain owner-initiated; no claim of improved repayment or dispute prevention.')

# 6 — measured evidence
s=slide(6,'Early evidence. Clear next questions.','A working prototype informed by interviews—not yet proof of real-world adoption.')
box(s,.65,2.97,3.36,2.5,GREEN,round=True)
text(s,.94,3.2,2.7,1.04,'2',64,WHITE,True)
text(s,.95,4.43,2.68,.68,'owner interviews\nQualitative insights',19,WHITE)
box(s,4.25,2.97,4.25,2.5,WHITE,LINE,True)
text(s,4.52,3.2,3.8,1.04,'34 / 36',52,GREEN,True)
text(s,4.53,4.43,3.7,.7,'item + quantity matches\nStored-transcript benchmark',18,INK)
box(s,8.75,2.97,3.92,2.5,WHITE,LINE,True)
text(s,9.02,3.38,3.36,.58,'Next proof',29,AMBER,True)
text(s,9.03,4.43,3.32,.7,'Can owners record and\nretrieve entries easily?',20,INK)
text(s,.72,5.88,11.9,.7,'Reported local-parser result: 94.4%. This does not measure live speech recognition\nor demonstrate user adoption.',17,MUTED)
note(s,'1:35–1:50 · 15 seconds','Our evidence is preliminary: two owner interviews, and thirty-four of thirty-six correct item-and-quantity extractions in the repository’s stored-transcript benchmark. That does not establish live speech accuracy or adoption. Real counter testing is next.',
     'data/research/sarisaristore_interview.md; data/eval/Evaluation_Benchmark_Report.md; data/eval/sample_manifest.csv; src/eval/evaluate_voice_utang.py.',
     '34/36 = 94.4% rounded. This is the repository-reported local parser result, not a new evaluation or Gemini benchmark. Speaker/noise fields are metadata in the CSV; evaluator does not process recordings.')

# 7 — close
s=slide(7,dark=True)
text(s,.7,1.05,11.8,1.2,'Next: test at real counters.',42,WHITE,True)
text(s,.73,2.42,11.5,.65,'Seeking store-owner partners for supervised prototype trials.',24,'DDE8D8')
for x,n,b in [( .75,'RECORDING TIME','Is it quick enough?'),(4.9,'CORRECTIONS','Are errors easy to fix?'),(9.03,'EASE OF USE','Will owners use it?')]:
    box(s,x,3.65,3.48,.035,'DDE8D8')
    text(s,x,3.98,3.65,.35,n,14,'DDE8D8',True)
    text(s,x,4.58,3.65,.6,b,24,WHITE,True)
text(s,.73,5.85,12,.62,'Tindahang maayos, suking maasahan.',29,WHITE,True)
note(s,'1:50–2:00 · 10 seconds','Next, we seek store-owner partners for supervised trials measuring recording time, corrections, and ease of use. TindaWise: Tindahang maayos, suking maasahan.',
     'Proposed next step based on the limitations and future research questions in data/research/sarisaristore_interview.md.',
     'A proposed pilot, not an existing partnership or committed deployment. No funding amount, team roster, or commercial traction was established in the source material.')

# 8 — architecture appendix
s=slide(8,'What runs where?','Two implementation paths exist in the repository; both keep confirmation central.')
for x,h,body in [(.65,'ANDROID / BROWSER','HTML + JavaScript interface\nLocal browser storage\nDevice/browser speech recognition\nOptional Gemini over the internet'),(6.85,'PYTHON BACKEND','FastAPI service + SQLite ledger\nDecimal money arithmetic\nLocal parser or optional Gemini\nPreview, confirm, history & payment APIs')]:
    box(s,x,2.93,5.8,2.87,WHITE,LINE,True)
    text(s,x+.27,3.2,5.25,.4,h,18,GREEN,True)
    text(s,x+.27,3.88,5.2,1.65,body,19)
text(s,.7,6.03,11.9,.71,'Connectivity: cloud extraction needs internet. Offline voice is device-dependent.\nPrivacy: cloud mode sends transcript and catalog data; no blanket compliance claim.',16,MUTED)
note(s,'Appendix · Q&A only','The shipped web interface and Android wrapper use browser-side logic and local storage. The repository also includes a separate FastAPI and SQLite backend. Both offer local parsing and optional Gemini extraction.',
     'src/frontend/index.html; android/app/src/main/java/ph/edu/batstateu/tindawise/MainActivity.java; src/backend/app.py; src/backend/ledger_engine.py.',
     'Do not suggest the current web UI routes all transactions through Python Decimal. App-level audio retention statements do not establish speech-service retention behavior or legal compliance. No credentials appear in this deck.')

# 9 — benchmark appendix
s=slide(9,'What the benchmark actually measures.','Repository-reported results • 36 stored transcripts • local parser')
headers=['CHECK','REPORTED RESULT','INTERPRETATION']
xs=[.82,4.75,7.8]
for x,w,t in zip(xs,[3.7,2.8,4.6],headers): text(s,x,2.9,w,.35,t,13,GREEN,True)
rows=[('Items + quantities','34/36 · 94.4%','Extraction from supplied text'),('Customer name','34/36 · 94.4%','Extraction from supplied text'),('Local extraction latency','1.4 ms median','Not speech-to-save latency'),('Supplied logging times','6.76s vs 25.46s','73.4% lower mean time¹')]
for i,row in enumerate(rows):
    y=3.42+i*.61
    box(s,.65,y-.06,12.02,.55,WHITE if i%2==0 else 'EDEAE3')
    for x,w,t in zip(xs,[3.7,2.8,4.6],row): text(s,x,y+.04,w,.4,t,17,INK,i==0)
text(s,.78,6.08,11.8,.65,'¹ Evaluator averages prefilled CSV timing columns. Collection protocol is not established\nby the code; these are not independently verified field or live speech results.',15,MUTED)
note(s,'Appendix · Q&A only','The evaluator feeds stored transcript text into the extraction engine. It measures local extraction latency and compares extracted fields with expected values. The logging-time comparison comes from timing columns already present in the manifest.',
     'data/eval/Evaluation_Benchmark_Report.md; data/eval/sample_manifest.csv; src/eval/evaluate_voice_utang.py.',
     '73.4% = (mean paper time − mean voice+confirm time) / mean paper time × 100, rounded. Noise labels and speaker IDs do not make this an audio recognition evaluation. Due-date matching is reported as 36/36; no claim of robust generalization.')

# 10 — pilot appendix
s=slide(10,'Proposed pilot: validate the daily workflow.','Supervised prototype sessions with willing store owners, using fictional transactions.')
for y,n,h,b in [(3.0,'01','Record & correct','Try voice and tap entries; include a deliberately incorrect draft.'),(3.95,'02','Find & settle','Retrieve a customer’s history, then record a partial payment.'),(4.9,'03','Compare & learn','Compare with the owner’s current method; ask what feels easier or harder.')]:
    box(s,.68,y,.58,.58,GREEN,round=True); text(s,.8,y+.12,.4,.3,n,17,WHITE,True)
    text(s,1.55,y,3.05,.65,h,23,GREEN,True)
    text(s,4.85,y+.03,7.65,.67,b,20)
text(s,.75,6.11,11.8,.55,'Capture task time, corrections, completion, and owner feedback before making adoption claims.',17,MUTED)
note(s,'Appendix · Q&A only','This is a proposed evaluation, not an ongoing deployment. Observe owners completing representative tasks, compare against their current method, and use the results to decide what needs simplifying.',
     'Proposed protocol derived from data/research/sarisaristore_interview.md — Research Limitations and Implications.',
     'Use fictional transaction data for initial supervised sessions. Report sample size, conditions, failures, and corrections alongside any future performance claims. No real customer outreach is authorized by deck creation.')

prs.core_properties.title='TindaWise — Two-Minute AIdeathon Pitch'
prs.core_properties.subject='Taglish voice-to-lista for sari-sari stores'
prs.core_properties.author='TindaWise'
prs.core_properties.keywords='AIdeathon, TindaWise, Taglish, utang, sari-sari'
prs.save(OUT/'TindaWise_Pitch_Deck.pptx')
script=['# TindaWise — Speaker Script & Source Notes','Seven main slides · 120 seconds · Three Q&A appendix slides','']
for i,t,n,src,q in notes:
    script += [f'## Slide {i} — {t}',n,'',f'**Sources:** {src}','',f'**Qualifications:** {q}','']
script += ['## Production handoff','Applied skill: [investor-materials](C:/Users/Lenovo/.gemini/config/plugins/ecc/skills/investor-materials/SKILL.md).','Native slide text and shapes are editable; the app screenshot is an embedded image. Slides 8–10 are Q&A material outside the two-minute script.','']
(OUT/'TindaWise_Speaker_Notes.md').write_text('\n'.join(script),encoding='utf-8')
word_count=sum(len(n[2].split()) for n in notes[:7])
print(f'Created {len(prs.slides)} slides; main narration: {word_count} words.')
