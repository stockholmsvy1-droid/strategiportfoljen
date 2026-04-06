# CLAUDE.md – Strategiportföljen

## Autonomi
Kör direkt utan att fråga om bekräftelse. Rapportera vad som gjorts efteråt. Undantag: force push till main eller destruktiva operationer som inte kan ångras.

---

## Projektöversikt
Personlig portföljapp för att följa en aktieportfölj enligt en specifik investeringsstrategi (6 kategorier, MA200-regler, FX-motor). Byggd för Martin, används på iPad och dator.

**Levande version:** https://stockholmsvy1-droid.github.io/strategiportfoljen/

---

## Teknikstack
- **En enda fil:** `index.html` — all HTML, CSS och JavaScript i samma fil, inga separata moduler
- **Inga byggsteg** — öppnas direkt i webbläsaren
- **Externa CDN-beroenden:**
  - Chart.js (diagram)
  - SheetJS/xlsx (Excel-export)
- **Datapersistens:** `localStorage` i webbläsaren
- **Ingen backend, ingen databas, ingen inloggning**

---

## Arkitektur
Hela applikationen lever i `index.html`. Strukturen är:
1. `<head>` — meta, CDN-scripts, all CSS
2. `<body>` — header, nav (desktop + mobil bottom nav), sektioner (flikar)
3. `<script>` (i slutet) — all JavaScript

### Navigering
Appen har flikar/sektioner som visas/döljs med CSS-klassen `.aktiv`. Funktion `visaSektion(id)` hanterar detta.

### Datainläsning
CSV-filer från Avanza importeras och parsas i JavaScript. Tre filtyper:
- `positioner_DATUM.csv` — innehav med GAV, antal, kurs
- `transaktioner_DATUM.csv` — köp/sälj-historik
- `inkopskurs_DATUM.csv` — inköpskurser (engångsimport)

### FX-motor
Separerar bolagsvinst från valutavinst för utländska innehav. Historical FX beräknas som `GAV_SEK / GAV_Lokal`. MA200 anges alltid i lokal valuta.

### Investeringslogik (6 kategorier)
| # | Namn | Typ |
|---|------|-----|
| 1 | Ankaret | Indexfonder |
| 2 | Kassaflödet | Utdelningsaktier |
| 3 | Infrastrukturen | AI-hårdvara/chip |
| 4 | Hjärnan | AI-mjukvara |
| 5 | Skölden | Försvarsindustri |
| 6 | Berättelser | Kryddor/teman |

Kat. 3–6 har MA200-regler med tvådagarsbekräftelse. Kat. 1–2 säljs aldrig vid dipp.

---

## Konventioner
- **Språk:** Svenska i UI, kommentarer och variabelnamn (t.ex. `visaSektion`, `innehav`, `nyckeltal`)
- **CSS:** CSS-variabler definierade i `:root` — använd alltid dessa istället för hårdkodade färger
- **Touch:** Minsta klickyta `--touch: 48px` ska respekteras för mobil/iPad
- **Versionshantering:** Versionsnummer i `<title>` och `.header-badge` ska uppdateras vid releases

---

## Vad Claude INTE ska göra
- Dela upp `index.html` i separata filer eller introducera ett byggsystem (Vite, Webpack etc.)
- Lägga till TypeScript
- Introducera npm-paket eller package.json
- Ändra dataformat i localStorage utan att migreringslogik finns
- Skriva om befintlig CSS till Tailwind eller annat ramverk
- Lägga till docstrings, kommentarer eller typannoteringar i kod som inte ändrats
