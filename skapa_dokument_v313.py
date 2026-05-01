"""
Skapar Strategiportfoljen_Beskrivning_v313.docx
- Baserad på v310, versionssträngar uppdaterade
- Ny avslutningssida: Nyheter i version 3.13
"""
from copy import deepcopy
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

DIR = r"C:\Users\hejma\Projekt_Claude\strategiportfoljen"
src = fr"{DIR}\Strategiportfoljen_Beskrivning_v310.docx"
dst = fr"{DIR}\Strategiportfoljen_Beskrivning_v313.docx"
IMG = fr"{DIR}\titelbild_v313.png"

NAVY   = RGBColor(0x1E, 0x3A, 0x5F)
ACCENT = RGBColor(0x0E, 0xA5, 0xE9)
MUTED  = RGBColor(0x6B, 0x72, 0x80)
BLACK  = RGBColor(0x11, 0x18, 0x27)

src_doc = Document(src)

pb_idx = None
for i, para in enumerate(src_doc.paragraphs):
    for br in para._element.findall(".//" + qn("w:br")):
        if br.get(qn("w:type")) == "page":
            pb_idx = i
            break
    if pb_idx is not None:
        break

new_doc = Document()
for sec in new_doc.sections:
    sec.top_margin    = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin   = Cm(3.0)
    sec.right_margin  = Cm(2.5)

new_doc.add_picture(IMG, width=Inches(6.1))
p = new_doc.paragraphs[-1]
p.alignment = WD_ALIGN_PARAGRAPH.LEFT
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after  = Pt(0)

new_doc.add_paragraph().add_run().add_break(
    __import__("docx.enum.text", fromlist=["WD_BREAK"]).WD_BREAK.PAGE
)

src_children = list(src_doc.element.body)
new_body     = new_doc.element.body

for child in src_children[pb_idx + 1:]:
    new_body.append(deepcopy(child))

for para in new_doc.paragraphs:
    for run in para.runs:
        for old, new in [("v3.10","v3.13"),("v310","v313"),
                         ("version 3.10","version 3.13"),
                         ("Version 3.10","Version 3.13"),
                         ("3.10","3.13")]:
            if old in run.text:
                run.text = run.text.replace(old, new)
for tbl in new_doc.tables:
    for row in tbl.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                for run in para.runs:
                    if "3.10" in run.text:
                        run.text = run.text.replace("3.10","3.13")

def sidbyte(doc):
    doc.add_paragraph().add_run().add_break(
        __import__("docx.enum.text", fromlist=["WD_BREAK"]).WD_BREAK.PAGE)

def rubrik1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20); p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text); r.bold = True; r.font.size = Pt(16); r.font.color.rgb = NAVY

def rubrik2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14); p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text); r.bold = True; r.font.size = Pt(12); r.font.color.rgb = ACCENT

def brödtext(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text); r.font.size = Pt(10.5); r.font.color.rgb = BLACK

def punkt(doc, text, prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent  = Cm(0.8)
    if prefix:
        r1 = p.add_run(prefix + " "); r1.bold = True
        r1.font.size = Pt(10.5); r1.font.color.rgb = NAVY
        r2 = p.add_run(text); r2.font.size = Pt(10.5); r2.font.color.rgb = BLACK
    else:
        r = p.add_run(text); r.font.size = Pt(10.5); r.font.color.rgb = BLACK

sidbyte(new_doc)
rubrik1(new_doc, "10. Nyheter i version 3.13")
rubrik2(new_doc, "Inställningar-sektion och förbättrad Kassa")
brödtext(new_doc,
    "Version 3.13 introducerar en komplett administrationsfunktion via en ny ⚙️ Inställningar-sektion "
    "och förbättrar Kassa-tabellen med inline-inmatning direkt per rad."
)

rubrik2(new_doc, "Ny Inställningar-sektion")
brödtext(new_doc,
    "Alla konfigurerbara parametrar samlas nu i en dedikerad sektion i navigeringsmenyn. "
    "Ingen kodredigering behövs för att anpassa appen."
)
punkt(new_doc, "Kontokonfiguration — lägg till, redigera, ta bort och ändra ordning på Avanza-konton via UI.")
punkt(new_doc, "Kategori-editor — ersätter prompt()-dialoger med visuellt inline-formulär (emoji, färg, vikter, signal).")
punkt(new_doc, "Strategiparametrar — exponerar MA200-gränser, nödutgångsgräns, ombalansering och koncentrationsrisk.")
punkt(new_doc, "Profil & information — redigerbara fält för namn och strategi-titel (används i exporter).")
punkt(new_doc, "Värdepappersfilter — lägg till/ta bort exkluderade värdepapper och konton från import.")
punkt(new_doc, "Export/import av inställningar — flytta hela strategikonfigurationen mellan enheter som JSON.")

rubrik2(new_doc, "Kassa — inline-inmatning per rad")
brödtext(new_doc,
    "Kassa-tabellen visar nu alltid alla konton (inkl. de utan likvida medel i positionsfilen). "
    "Varje rad har ett eget inmatningsfält och Spara-knapp — det separata formuläret är borttaget."
)
punkt(new_doc, "Sparkontot (Avanza sparande Martin) visas som en separat rad, ej inkluderat i totalt tillgängligt för köp.")
punkt(new_doc, "Konton utan positionsfildata visas med ⚠️-ikon tills värde anges manuellt eller importeras.")

rubrik2(new_doc, "Buggfixar")
brödtext(new_doc,
    "Kontonummer för Avanza sparande Martin korrigerat till 0040080455 (visades utan ledande nollor i Avstämning). "
    "Kassa-tabellen visade inte konton vars likvida medel saknades i positionsfilen."
)

p = new_doc.add_paragraph()
p.paragraph_format.space_before = Pt(20)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Strategiportföljen v3.13  ·  Byggt för Martin  ·  Strategi från januari 2026")
r.italic = True; r.font.size = Pt(9); r.font.color.rgb = MUTED

new_doc.save(dst)
print(f"Skapad: {dst}")
