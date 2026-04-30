"""
Automatiserat releasetest för Strategiportföljen
Körs av Claude efter varje commit — fångar upp uppenbara fel utan att öppna webbläsaren.

Utdata: rapport med ✅ / ⚠️ / ❌ per kontroll.
Exit-kod 0 = godkänt, 1 = minst ett fel.
"""
import re, subprocess, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DIR  = Path(r"C:\Users\hejma\Projekt_Claude\strategiportfoljen")
HTML = DIR / "index.html"

errors, warnings, ok = [], [], []

def err(msg):  errors.append(f"❌  {msg}")
def warn(msg): warnings.append(f"⚠️   {msg}")
def good(msg): ok.append(f"✅  {msg}")

html = HTML.read_text(encoding="utf-8", errors="replace")

# ── 1. JavaScript-syntax ──────────────────────────────────────────────
try:
    js_check = subprocess.run(
        ["node", "-e", """
const fs=require('fs');
const html=fs.readFileSync(process.argv[1],'utf8');
const s=html.lastIndexOf('<script>'), e=html.lastIndexOf('</script>');
try{new Function(html.slice(s+8,e));process.exit(0);}
catch(ex){console.error(ex.message);process.exit(1);}
""", str(HTML)], capture_output=True, text=True)
    if js_check.returncode == 0:
        good("JavaScript-syntax OK")
    else:
        err(f"JavaScript-syntaxfel: {js_check.stderr.strip()[:200]}")
except FileNotFoundError:
    warn("Node.js ej installerat — hoppar över JS-syntaxkontroll")

# ── 2. Versionsnummer-konsekvens ─────────────────────────────────────
v_title = re.search(r'<title>Strategiportföljen (v[\d.]+)</title>', html)
v_badge = re.search(r'class="header-badge">(v[\d.]+)</span>', html)
readme  = (DIR / "README.md").read_text(encoding="utf-8")
v_readme = re.search(r'\- \*\*(v[\d.]+)\*\*', readme)

if v_title and v_badge:
    vt, vb = v_title.group(1), v_badge.group(1)
    if vt == vb:
        good(f"Versionsnummer i title och badge matchar: {vt}")
    else:
        err(f"Versionsskillnad — title: {vt}, badge: {vb}")
    ver = vt  # t.ex. "v3.10"
    ver_filnamn = ver.replace("v","").replace(".","")  # t.ex. "310"
else:
    err("Kan inte hitta versionsnummer i title eller badge")
    ver, ver_filnamn = "?", "?"

if v_readme:
    if v_readme.group(1) == ver:
        good(f"README-ändringslogg börjar med {ver}")
    else:
        warn(f"README-version ({v_readme.group(1)}) matchar inte app ({ver})")

# ── 3. Kritiska funktioner ───────────────────────────────────────────
required_funcs = [
    # Render
    ("renderDashboard",          "Dashboard-rendering"),
    ("renderKassa",              "Kassa-rendering"),
    ("renderAvstemning",         "Avstämning-rendering"),
    ("renderImportOrdningsguide","Importordningsguide (v3.10)"),
    ("renderAvsteg3",            "Diff-wizard steg 3"),
    # Diagram
    ("ritaHuvudDiagram",         "Huvud-diagram (v3.10)"),
    ("byttHDPeriod",             "Huvud-diagram periodval"),
    # Import/export
    ("importeraPositioner",      "Positionsimport"),
    ("importeraTransaktioner",   "Transaktionsimport"),
    ("importeraInkopskurs",      "Inköpskursimport"),
    ("exporteraExcel",           "Excel-backup export"),
    ("importeraExcelBackup",     "Excel-backup import"),
    # Konto/register
    ("beräknaAvanzaKassaPerKonto","Kassaberäkning per konto"),
    ("uppdateraKontoRegister",   "Kontoregister-uppdatering (v3.10)"),
    ("laddaKontoRegister",       "Kontoregister-laddning (v3.10)"),
    # Beräkning
    ("beräknaTotalVärde",        "Totalvärdesberäkning"),
    ("beräknaNettoInsatt",       "Nettoinsatt-beräkning"),
    ("ma200Signal",              "MA200-signalberäkning"),
]
func_ok = 0
for fname, label in required_funcs:
    if f"function {fname}" in html or f"{fname} =" in html or f"{fname}=" in html:
        func_ok += 1
    else:
        err(f"Funktion saknas: {fname} ({label})")
if func_ok == len(required_funcs):
    good(f"Alla {func_ok} kritiska funktioner finns")

# ── 4. Kritiska HTML-element ─────────────────────────────────────────
required_ids = [
    ("nk-total",             "Portföljvärde-kort"),
    ("nk-avkastning",        "Avkastnings-kort"),
    ("nk-nettoinsatt",       "Nettoinsatt-kort"),
    ("nk-kassa",             "Kassa-kort"),
    ("huvud-diagram",        "Huvud-diagram canvas (v3.10)"),
    ("hd-cb-portfölj",       "Portföljvärde-kryssruta"),
    ("hd-cb-nettoinsatt",    "Nettoinsatt-kryssruta"),
    ("hd-kat-rad",           "Kategori-kryssrutor container"),
    ("avanza-kassa-lista",   "Kassa-kontolista"),
    ("avst-konto-tabell",    "Avstämning kontotabell"),
    ("avst-total-tabell",    "Avstämning totaltabell"),
    ("import-ordningsguide", "Importordningsguide-kort (v3.10)"),
    ("import-ordning-steg",  "Importordningsguide-steg"),
    ("signal-band",          "Signalband"),
    ("nyckeltal-grid",       "Nyckeltal-grid"),
    ("huvud-diagram-kort",   "Huvud-diagram-kort"),
]
id_ok = 0
for eid, label in required_ids:
    if f'id="{eid}"' in html:
        id_ok += 1
    else:
        err(f"HTML-element saknas: #{eid} ({label})")
if id_ok == len(required_ids):
    good(f"Alla {id_ok} kritiska HTML-element finns")

# ── 5. Kända fällor / fältnamn ───────────────────────────────────────
# Historik: fältet ska heta totalVärde
bad_historik = [m.start() for m in re.finditer(r'h\.värde\b', html)]
if bad_historik:
    # Tillåt i kommentarer och strängar som inte är historik-kontext
    suspect = [html[max(0,p-30):p+30] for p in bad_historik[:3]]
    warn(f"'h.värde' hittades {len(bad_historik)} gånger — verifiera att det inte är historik-kontext. Exempel: {suspect[0]!r}")
else:
    good("Ingen 'h.värde' — historik-fältnamnsbugg undviken (ska vara 'h.totalVärde')")

# positionsKontoVärden ska finnas i restore-objektet
if "positionsKontoVärden: {}" in html:
    good("positionsKontoVärden initieras korrekt i Excel-restore")
else:
    warn("Kontrollera att 'positionsKontoVärden: {}' finns i importeraExcelBackup()")

# Excel-export: ska använda totalVärde
if "h.totalVärde" in html:
    good("Excel-export använder h.totalVärde (korrekt fältnamn)")
else:
    err("Excel-export: 'h.totalVärde' saknas — historikdata exporteras troligen fel")

# Excel-export: ska inkludera KatVärden
if "'KatVärden'" in html or '"KatVärden"' in html:
    good("KatVärden inkluderas i Excel-export (kategorihistorik bevaras)")
else:
    warn("KatVärden saknas i Excel-exporten — kategoriutvecklingshistorik förloras vid restore")

# ── 6. Dokumentfiler för aktuell version ─────────────────────────────
docs = [
    (DIR / f"Strategiportfoljen_Beskrivning_v{ver_filnamn}.docx", "Beskrivning"),
    (DIR / f"Kursmaterial_Strategiportfoljen_v{ver_filnamn}.pptx", "Kursmaterial"),
    (DIR / f"Testprotokoll_Strategiportfoljen_v{ver_filnamn}.xlsx", "Testprotokoll"),
]
for path, label in docs:
    if path.exists():
        size_kb = path.stat().st_size // 1024
        good(f"{label} finns: {path.name} ({size_kb} KB)")
    else:
        warn(f"{label} saknas för {ver} — generera med skapa_*_v{ver_filnamn}.py")

# ── 7. Hjälpfil uppdaterad ───────────────────────────────────────────
if f"version {ver}" in html or f"version {ver.replace('v','')}" in html:
    good(f"Hjälpfilen nämner {ver}")
else:
    warn(f"Hjälpfilen verkar inte nämna {ver} — kolla id='hk-nyheter'")

# ── 8. Git-status ─────────────────────────────────────────────────────
try:
    git_log = subprocess.run(["git", "log", "--oneline", "-1"], capture_output=True,
                              text=True, cwd=DIR)
    latest = git_log.stdout.strip()
    git_status = subprocess.run(["git", "status", "--short"], capture_output=True,
                                 text=True, cwd=DIR)
    uncommitted = git_status.stdout.strip()
    good(f"Senaste commit: {latest}")
    if uncommitted:
        warn(f"Ocommittade ändringar finns:\n{uncommitted}")
    else:
        good("Inga ocommittade ändringar")
except Exception as e:
    warn(f"Kunde inte köra git: {e}")

# ── RAPPORT ───────────────────────────────────────────────────────────
print(f"\n{'='*64}")
print(f"  RELEASETEST — Strategiportföljen {ver}")
print(f"{'='*64}")
if ok:
    print(f"\n  {len(ok)} kontroller godkända:")
    for m in ok: print(f"    {m}")
if warnings:
    print(f"\n  {len(warnings)} varningar (ej blockerande):")
    for m in warnings: print(f"    {m}")
if errors:
    print(f"\n  {len(errors)} FEL (blockerande):")
    for m in errors: print(f"    {m}")
status = "GODKÄNT ✅" if not errors else "UNDERKÄNT ❌"
print(f"\n{'='*64}")
print(f"  Resultat: {status} — {len(errors)} fel, {len(warnings)} varningar, {len(ok)} OK")
print(f"{'='*64}\n")
sys.exit(1 if errors else 0)
