import os
import comtypes.client

pptx_path = os.path.abspath(r"C:\Users\Lenovo\Documents\AIdeathon\deliverables\TindaWise_Pitch_Deck_Revised.pptx")
pdf_path = os.path.abspath(r"C:\Users\Lenovo\Documents\AIdeathon\deliverables\TindaWise_Pitch_Deck_Revised.pdf")

ppt = comtypes.client.CreateObject("PowerPoint.Application")
try:
    pres = ppt.Presentations.Open(pptx_path, WithWindow=False)
    # 32 = ppSaveAsPDF
    pres.SaveAs(pdf_path, 32)
    pres.Close()
    print("PDF export successful:", pdf_path)
finally:
    ppt.Quit()
