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
rubrik2(new_doc, "Avstämning mot Avanza — omarbetad")
brödtext(new_doc,
    "Version 3.13 fokuserar på att göra Avstämning-fliken pålitlig och jämförbar med Avanzas "
    "egna översiktsvy. Flera fel som funnits sedan v3.03 är nu rättade."
)
punkt(new_doc, "Ny rubrik 'Avstämning mot Avanza' och framträdande summaryrad med Totalt värde och Tillgängligt för köp — samma layout som Avanza.")
punkt(new_doc, "Kontots totalt = investerat + tillgängligt för köp, vilket matchar Avanzas visning per konto.")
punkt(new_doc, "Avanza sparande Martin (SPAR) visas nu med korrekt saldo i Avstämning.")
punkt(new_doc, "Tillgängligt för köp per konto visade 0 kr trots inmatat värde — rättat.")

rubrik2(new_doc, "Buggfix: Eget fondsparande fel kontonr (sedan v3.03)")
brödtext(new_doc,
    "Kontot 'Eget fondsparande' var felaktigt kopplat till pensionskontot (9552-6014837) "
    "i stället för det riktiga ISK-kontot (9557-7346055). Felet medförde att Avanza Zero "
    "inte importerades korrekt och att kontovärdena var ~25 000 kr för låga."
)
punkt(new_doc, "Rätt kontonr: 9557-7346055 (ISK) — pensionskontot 9552-6014837 exkluderas nu korrekt.")
punkt(new_doc, "Befintlig kontokonfiguration och exkluderingslista migreras automatiskt vid laddning.")

rubrik2(new_doc, "Arkitektur: manuell kassa ingår inte i portföljvärdet")
brödtext(new_doc,
    "Manuella insättningar och uttag (Kassa-sektionen) räknas inte längre in i portföljvärdet. "
    "De används enbart för att beräkna nettoinsatt kapital och avkastning. "
    "Eliminerar dubbelräkning när sparkontosaldo redan finns med i Avstämning."
)
punkt(new_doc, "beräknaTillgängligLikviditet() = bara Avanza-kassa (tillgängligt för köp från positionsfilen).")
punkt(new_doc, "Nettoinsatt-kortet på Dashboard visar fortfarande summan av insättningar/uttag för avkastningsberäkning.")

p = new_doc.add_paragraph()
p.paragraph_format.space_before = Pt(20)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Strategiportföljen v3.13  ·  Byggt för Martin  ·  Strategi från januari 2026")
r.italic = True; r.font.size = Pt(9); r.font.color.rgb = MUTED

new_doc.save(dst)
print(f"Skapad: {dst}")
