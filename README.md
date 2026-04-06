# 📈 Strategiportföljen
*Martin's Magnificent Money-Making Machine*

Personlig portföljapp byggd för iPad och dator. Öppnas direkt i webbläsaren — ingen installation, ingen inloggning.

**→ [Öppna appen](https://stockholmsvy1-droid.github.io/strategiportfoljen/)**

---

## Vad appen gör

- Visar portföljens värde, avkastning och fördelning per kategori
- Importerar positioner och transaktioner direkt från Avanza (CSV)
- Beräknar nettoinsatt kapital och tillgänglig likviditet (inkl. Avanza-kassa från positionsfil)
- **FX-motor:** separerar bolagsvinst från valutavinst för utländska innehav
- Visar MA200-signaler i **lokal valuta** — jämför USD mot USD, SEK mot SEK
- **Tvådagarsregel** — säljsignal kräver två dagars stängning under MA200 (kat. 3–6)
- **Nödutgångar** (90 % av GAV) — hård stopp (kat. 3–6) eller mjuk analys (kat. 1–2)
- **Gummibandet** — visar hur långt kursen sträckt sig från MA200
- **Anpassningsbara kategorier** — lägg till, redigera och ta bort kategorier via UI
- **Värdeutvecklingsdiagram** med periodväljare (30D/90D/6M/1Å/Allt) och referenslinje för nettoinsatt kapital
- Beslutslogg för veckovisa anteckningar
- Exporterar data som Excel-säkerhetskopia

---

## Kategorier

Appen levereras med 6 standardkategorier men du kan anpassa dem fritt via Kategorier-fliken.

| # | Namn | Typ | Mål |
|---|------|-----|-----|
| 1 | ⚓ Ankaret | Indexfonder | 35–40 % |
| 2 | 💰 Kassaflödet | Utdelningsaktier | 20–25 % |
| 3 | ⚙️ Infrastrukturen | AI-hårdvara / chip | 15–20 % |
| 4 | 🧠 Hjärnan | AI-mjukvara | 8–12 % |
| 5 | 🛡️ Skölden | Försvarsindustri | 8–12 % |
| 6 | ✨ Berättelser | Kryddor / teman | 0–5 % |

**Hantera kategorier:** Varje kategorikort har ✏️ (redigera) och 🗑 (ta bort). Längst ner finns "+ Ny kategori" och "↩ Återställ standard". Kategori 3–6 styrs av MA200-regeln med tvådagarsbekräftelse. Kategori 1–2 säljs aldrig vid dipp.

---

## FX-motorn (v2.02+)

För utländska innehav (t.ex. NVIDIA i USD) beräknar appen automatiskt:

| Begrepp | Formel |
|---------|--------|
| Historical FX | `GAV_SEK / GAV_Lokal` — hämtas från positionsfilen |
| Lokal kurs nu | `Kurs_SEK / Historical_FX` |
| Bolagsvinst | `(Lokal_nu − GAV_Lokal) × Antal × FX` |
| Valutavinst | `Total_SEK − Bolagsvinst` |

MA200 anges alltid i **lokal valuta** (USD för amerikanska aktier, SEK för svenska).

---

## Importera från Avanza

Öppna **avanza.se i Safari** (inte Avanza-appen — den saknar export).

| Fil | Var du hittar den | Hur ofta |
|-----|-------------------|----------|
| `positioner_DATUM.csv` | Min ekonomi → Innehav → Exportera | Varje vecka |
| `transaktioner_DATUM.csv` | Min ekonomi → Transaktioner → Exportera | Varje vecka |
| `inkopskurs_DATUM.csv` | Innehav → Exportera inköpskurser | En gång |

Gå sedan till **Importera**-fliken i appen och välj filen.

---

## Teknik

- Ren HTML/CSS/JavaScript — en enda fil, inga beroenden utöver Chart.js och SheetJS (laddas från CDN)
- All data sparas lokalt i webbläsarens `localStorage`
- Fungerar offline efter första laddningen
- Data synkroniseras **inte** automatiskt mellan enheter — använd Excel-exporten för att flytta data

---

## Version

**v2.04** — april 2026

Byggt för Martin · Strategi från januari 2026
