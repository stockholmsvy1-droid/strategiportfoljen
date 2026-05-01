# 📈 Strategiportföljen
*The Magnificent Martin's Money-Making Machine*

Personlig portföljapp byggd för iPad och dator. Öppnas direkt i webbläsaren — ingen installation, ingen inloggning.

**→ [Öppna appen](https://stockholmsvy1-droid.github.io/strategiportfoljen/)**

---

## Vad appen gör

- **Kategori-nyckeltalskort på Dashboard** — ett kompakt kort per kategori i nyckeltal-griden med emoji, aktuellt värde, netto-avkastning kr och %, period-styrt; fallback till vinst sedan köp om historik saknas
- **Kategoriutvecklingstabell på Dashboard** — tabell med aktuellt värde, förändring i kr och % samt portföljandel per kategori; sorterad efter störst absolut förändring; fallback till orealiserad vinst om historik saknas
- **Global periodväljare** (1D / 7D / 30D / 90D / 6M / 1Å / i År / Allt) — sticky bar under nav, påverkar Dashboard, Kategorier och Innehav samtidigt
- **Signalband på Dashboard** — rött band med räknare för röda signaler, nödutgångar och ombalans; klick → Signaler-fliken
- **Signaler-flik** — samlad vy med säljsignaler, bevakningslista, nödutgångar, ombalanseringsbehov och hög koncentration
- **Ombalanseringsassistent** — varje kategorikort visar "Köp/Sälj för X kr" om vikten avviker >2% från målintervallet
- **Koncentrationsrisk** — "Andel"-kolumn i innehav med färgvarning gul >8%, orange >12%
- **Sorterbar innehavstabell** — klicka på kolumnrubrik för att sortera efter namn, värde, avkastning, signal, andel eller MA200-avstånd
- **Kategoriprestation per period** — avkastningsbadge på varje kategorikort för vald period
- **Kategori-jämförelsevy** — indexerat linjediagram (start=100) som jämför alla kategoriers avkastning under vald period
- **FX-exponeringsöversikt** — donut-diagram och färgade pills (SEK/USD/EUR etc.) på Dashboard
- **Avkastningsstaplar per kategori** — horisontella staplar på Dashboard för vald period
- **Tickers & automatisk MA200-hämtning** — ange börssymbol per aktie, hämta MA200 automatiskt via Alpha Vantage (gratis API-nyckel)
- **Manuell baslinje** — ange ett datum + portföljvärde som fast startpunkt för avkastningsberäkningar
- **Visa beräkningsunderlag** — "▼"-toggle i Periodutveckling-kortet visar exakt vilka tal som används
- **ISK/KF-skattesektion** — schablonintäktsprognos och förväntad skatt baserat på kvartalsvärden och insättningar; insättningstajming-varning och round-trip-varning
- **Avstämningspanel** — 4-stegs guidad jämförelse av portföljsiffror mot Avanza; sparar av stämningshistorik
- **Utdelningskalender** — förväntade utdelningar de kommande 90 dagarna baserat på historiska utdelningsmånader
- **Mörkt tema** — ☀️/🌙-toggle i headern, sparas i webbläsaren
- Visar portföljens värde, avkastning och fördelning per kategori — nyckeltal uppdateras dynamiskt per vald period
- Importerar positioner och transaktioner direkt från Avanza (CSV) — dra filer eller välj flera samtidigt
- Sålda innehav tas bort automatiskt när senaste positionsfilen importeras
- **Utdelningar kopplas automatiskt** per aktie via ISIN från transaktionsfilen — ingen manuell inmatning
- **Tillgängligt för köp per konto** — hämtas automatiskt från positionsfilen vid varje import; manuell override möjlig per konto
- Beräknar nettoinsatt kapital och tillgänglig likviditet (inkl. Avanza-kassa från positionsfil)
- **FX-motor:** separerar bolagsvinst från valutavinst för utländska innehav
- Visar MA200-signaler i **lokal valuta** — jämför USD mot USD, SEK mot SEK
- **Tvådagarsregel** — säljsignal kräver två dagars stängning under MA200 (kat. 3–6)
- **Nödutgångar** (90 % av GAV) — hård stopp (kat. 3–6) eller mjuk analys (kat. 1–2)
- **Gummibandet** — visar hur långt kursen sträckt sig från MA200
- **Anpassningsbara kategorier** — lägg till, redigera och ta bort kategorier via UI
- **Värdeutvecklingsdiagram** med periodväljare och referenslinje för nettoinsatt kapital
- Historik byggs automatiskt från importerade positionsfiler — en datapunkt per fil
- Beslutslogg för veckovisa anteckningar
- **Excel backup & återställning** — exporterar all data (7 ark) och kan importeras tillbaka för fullständig återställning

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

## Avkastningslogik

Avkastning mäts alltid från **närmaste importerade historikpunkt** — aldrig från alla insättningar sedan 2017.

| Term | Beskrivning |
|------|-------------|
| Startpunkt | Närmaste historikpost på eller före periodens startdatum |
| Nettoinflöde | `beräknaNettoInsattMellan(startH.datum, idag)` — insättningar efter startpunkten |
| Avkastning (kr) | `nuVärde − startH.totalVärde − insEfterStart` |
| Manuell baslinje | Datum + värde angivet av användaren, sparas som `{manuell:true}` i historiken |

Tryck **"▼ Visa beräkningsunderlag"** i Periodutveckling-kortet för att se exakt vilka tal som används.

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

## Automatisk MA200-hämtning (Alpha Vantage)

Ange börssymboler per aktie under **Innehav → 📡 Tickers & MA200** och klicka "Uppdatera alla MA200". API-nyckeln (gratis på alphavantage.co) anges en gång och sparas lokalt.

Klicka **🔍** bredvid ett innehav för att söka rätt ticker via Alpha Vantage — resultatlistan visar börs och valuta så att du kan välja rätt symbol direkt.

| Typ | Format | Exempel |
|-----|--------|---------|
| Svenska aktier (Nasdaq Sthlm) | `NAMN.STO` | `SAAB-B.STO`, `VOLV-B.STO` |
| Amerikanska aktier | `TICKER` | `NVDA`, `MSFT` |
| Brittiska aktier (LSE) | `NAMN.LON` | `AZN.LON`, `SHEL.LON` |
| Norska aktier (Oslo Børs) | `NAMN.OSL` | `EQNR.OSL` |

Appen väntar automatiskt 15 sekunder mellan anrop (gratis-planen: 5 req/min). Grön ✓ per aktie = uppdaterat, gult ! = ticker saknas. Rött ⚠ = misstänkt fel valuta — använd 🔍 för att hitta rätt ticker.

---

## Importera från Avanza

Öppna **avanza.se i Safari** (inte Avanza-appen — den saknar export).

| Fil | Var du hittar den | Hur ofta |
|-----|-------------------|----------|
| `DATUM_positioner.csv` | Min ekonomi → Innehav → Exportera | Varje vecka |
| `transaktioner_DATUM.csv` | Min ekonomi → Transaktioner → Exportera | Varje vecka |
| `inkopskurs_DATUM.csv` | Innehav → Exportera inköpskurser | En gång |

Gå sedan till **Importera**-fliken i appen och välj filen. Datumet i positionsfilens namn används automatiskt som historikpunkt i värdeutvecklingsdiagrammet — importera äldre filer för att bygga upp historiken bakåt.

**Filtreras alltid bort:** Pensionskontot och alla konton utanför de 6 konfigurerade. Värdepapperet Zomedica filtreras alltid.

---

## Teknik

- Ren HTML/CSS/JavaScript — en enda fil, inga beroenden utöver Chart.js, chartjs-adapter-date-fns och SheetJS (laddas från CDN)
- All data sparas lokalt i webbläsarens `localStorage`
- Fungerar offline efter första laddningen
- Data synkroniseras **inte** automatiskt mellan enheter — använd Excel-exporten för att flytta data

---

## Backup & Återställning (v2.08)

All portföljdata kan exporteras till en fullständig Excel-backup och importeras tillbaka — t.ex. för att flytta data mellan iPad och dator, eller som säkerhetskopia innan man rensar.

**Exporterar 7 ark:** Innehav · Transaktioner · Beslutslogg · Sammanfattning · Historik · Kassa · Kategorier

**Importera:** Importera-fliken → Backup & Återställning → välj `portfölj_DATUM.xlsx`. Appen validerar att obligatoriska kolumner finns och bekräftar innan all data ersätts.

> Data sparas lokalt i webbläsarens `localStorage`. Exportera backup regelbundet — om du rensar webbhistoriken eller byter enhet är en backup det enda sättet att återfå datan.

---

## Testprotokoll

**v2.08 — Statisk kodanalys genomförd 2026-04-09**

Alla 46 testfall i `Testprotokoll_Strategiportfoljen_v208.xlsx` analyserade mot `index.html`:

| Testsvit | Testfall | Godkända | Kräver manuell test |
|----------|----------|----------|---------------------|
| T1 Export grundläggande | 7 | 7 | — |
| T2 Export dataintegritet | 9 | 9 | — |
| T3 Header-knapp | 2 | 2 | — |
| T4 Rundtur export→rensa→import | 10 | 10 | — |
| T5 Felhantering | 6 | 6 | — |
| T6 Äldre exportformat | 2 | 2 | — |
| T7 Mobil / iPad | 6 | 3 | T7.3–T7.5 (Safari iOS) |
| T8 Kategorier bevaras | 4 | 4 | — |

**Anmärkningar:** `rensaAllData()` kräver dubbel bekräftelse (teststeg T4:3 säger singular — protokollet bör korrigeras). Kategorier bevaras vid rensning av data (intentionellt).

---

## Version

**v3.03** — april 2026

Byggt för Martin · Strategi från januari 2026

### Ändringslogg\n- **v3.13** — Avstämning omarbetad: ny rubrik "Avstämning mot Avanza", framträdande summaryrad med Totalt värde och Tillgängligt för köp i Avanzas stil. Buggfix: Eget fondsparande pekade på fel kontonr (pensionskonto 9552-6014837 → rätt ISK-konto 9557-7346055) sedan v3.03 — automatisk migration. Buggfix: Avanza sparande Martin (SPAR) visade inte sitt värde i Avstämning. Buggfix: Tillgängligt för köp visade 0 kr trots inmatat värde. Buggfix: kontots totalt i Avstämning summerar nu investerat + kassa (matchar Avanzas visning). Arkitekturfix: manuella insättningar/uttag ingår inte längre i portföljvärdet — de används enbart för nettoinsatt-historik och avkastningsberäkning, eliminerar dubbelräkning mot sparkontot.
- **v3.12** — Stabilitetsfixversion: kontohanteringen omskriven för att använda kontonummer (t.ex. "7882604") som intern nyckel i stället för kontonamn. Eliminerar ett återkommande fel där "1. Utländska Aktier 2025" och "2. Utländska Aktier 2025" normaliserades till samma sträng och blandades ihop i Kassa och Avstämning. positionsKassa och positionsKontoVärden lagras nu alltid med kontonr som nyckel. Befintlig data migreras automatiskt vid start. Buggfix: beräknaAvanzaKassaPerKonto() löser nu upp kontoStartsaldo-namn till kontonr korrekt.
- **v3.11** — Ny ⚙️ Inställningar-sektion: Kontokonfiguration (add/edit/delete Avanza-konton från UI), Kategori-editor (ersätter prompt()-dialoger med visuellt inline-formulär för alla fält), Strategiparametrar (MA200-gränser, nödutgång, ombalansering, konc.risk), Profil & information, Värdepappersfilter (exkludera VP/konton vid import), Export/import av inställningar som JSON. Kassa-tabellen visar nu alla konton med inline-inmatning per rad (inkl. sparkonto som separat rad). Buggfix: kontonummer för Avanza sparande Martin korrigerat till 0040080455; Kassa visade inte konton utan likvida medel i positionsfilen.
- **v3.10** — Nytt interaktivt portföljutvecklingsdiagram på Dashboard (period, serier, kategorier, linje/stapel). Kontoregister auto-synkar kontonamn vid namnbyte i Avanza med historikspårning. Importordningsguide med live-status (✅/⚠️) på Importera-fliken. Varning vid inköpskursimport om inga innehav finns. Förbättrad diff-wizard: exakt Avanza-navigering i steg 2, prioriterad beslutsgraf i steg 3. Post-import-tips till Avstämning. Förbättrade nyckeltalskort med ikoner och förklaringstext. Buggfix: Excel-backup sparade historik som tomma värden (h.värde → h.totalVärde) och återställde inte diagram efter restore; katVärden (kategorihistorik) sakandes i export.
- **v3.03** — Avstämning komplett: alla 6 konton visas med namn + kontonummer, alla saldon (inkl. Avanza sparande Martin) hämtas automatiskt från positionsfilen. Kassa-fliken visar Tillgängligt för köp automatiskt från positionsfilen (ej manuellt). Allow-list i positionsimport (bara konfigurerade konton). Importknappar robustare på iPad (label-mönster). Buggfix: kontonamn med numeriskt prefix (1./2.) matchades fel av normNamn.
- **v3.02** — Ny Avstämningsflik: saldon per konto direkt från positionsfilen med automatisk kontroll mot appens portföljvärde och inbyggd diff-förklaring. Nettoinsatt kapital är nu periodbaserat på Dashboard. Kassa-flikens kontoordning matchar Avanza.
- **v3.01** — Kategoriutveckling på Dashboard: tabell med kr, % och andel per kategori, sorterad efter störst förändring, alltid synlig med GAV-fallback
- **v3.00** — Buggfixar: `liveFXRater`→`liveFX` i Avstämningspanel, signalband inkluderar kassa i ombalanseringskontrollen, `hämtaAllaMA200()` uppdaterar diagram och signaler, signal-band display-konflikt åtgärdad, MA200-varning i mobilkort. UX: inline tickersök-modal (ersätter prompt-dialoger), manuell baslinje-badge i portföljvärde-kortet. Ny hjälpsektion "Kontrollräkna för hand". FAQ utökad (kassa + ombalanseringsformel). GitHub-avsnitt flyttat till separat dokument. Kursmaterial PowerPoint (13 bilder). Dokumentet "Strategiportföljen_Beskrivning_v300" med kontrollräkna-appendix.
- **v3.0** — Global periodväljare, Signaler-flik, Ombalanseringsassistent, Koncentrationsrisk, Sorterbar innehavstabell, Kategoriprestation per period, Kategori-jämförelsevy, FX-exponeringsöversikt, Avkastningsstaplar, Tickers & automatisk MA200-hämtning (Alpha Vantage), Manuell baslinje, Visa beräkningsunderlag, ISK/KF-skattesektion, Avstämningspanel, Utdelningskalender, Mörkt tema
- **v2.08** — Excel backup & återställning (7 ark)
