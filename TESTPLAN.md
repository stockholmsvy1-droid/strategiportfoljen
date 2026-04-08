# Testplan — Strategiportföljen v2.08
**Excel Backup & Återställning**

Utförd av: _____________________ &nbsp;&nbsp; Datum: _____________________ &nbsp;&nbsp; Version: v2.08

---

## Förutsättningar

Innan testerna startar, säkerställ att:
- Appen är öppen i webbläsaren (Safari/Chrome)
- Det finns **befintlig data** i portföljen (minst några innehav, transaktioner och en loggpost)
- En Avanza-positionsfil har importerats så att historikpunkter finns
- Du har tillgång till Excel eller Numbers för att granska exportfiler

---

## T1 — Export: grundläggande funktionalitet

### Beskrivning
Kontrollerar att exportknappen skapar en giltig Excel-fil med rätt antal ark och korrekt metadata.

### Steg
1. Gå till **Importera**-fliken → sektionen **Backup & Återställning**
2. Tryck **⬇ Ladda ner Excel-backup**
3. Öppna den nedladdade filen `portfölj_DATUM.xlsx` i Excel eller Numbers
4. Kontrollera antal ark och deras namn
5. Öppna arket **Sammanfattning** och granska rad 1–2
6. Öppna arket **Innehav** och granska kolumnrubrikerna

### Förväntade resultat

| # | Vad kontrolleras | Förväntat | Utfall | OK? |
|---|-----------------|-----------|--------|-----|
| 1.1 | Fil laddas ned automatiskt | Fil med namn `portfölj_ÅÅÅÅ-MM-DD.xlsx` | | ☐ |
| 1.2 | Antal ark i filen | 7 ark | | ☐ |
| 1.3 | Arknamn | Innehav · Transaktioner · Beslutslogg · Sammanfattning · Historik · Kassa · Kategorier | | ☐ |
| 1.4 | Sammanfattning rad 1 | `BACKUP_VERSION` = `2.08` | | ☐ |
| 1.5 | Sammanfattning rad 2 | `BACKUP_DATUM` = ISO-datum (t.ex. `2026-04-08T…`) | | ☐ |
| 1.6 | Innehav: obligatoriska kolumner finns | `id`, `Namn`, `Antal`, `GAV_SEK`, `Kurs_SEK`, `Kategori`, `GAV_Lokal`, `Historical_FX`, `TvåDagarsAktiv` | | ☐ |
| 1.7 | Importlogg (nedre på sidan) | Grön rad: "Excel-backup exporterad: X innehav, Y transaktioner" | | ☐ |

**Noteringar:**

_______________________________________________

---

## T2 — Export: dataintegritet per ark

### Beskrivning
Kontrollerar att varje ark innehåller rätt antal rader och att värdena stämmer med vad appen visar.

### Steg
1. Notera antal innehav i **Innehav**-fliken i appen
2. Notera antal transaktioner i **Transaktioner**-fliken
3. Notera antal loggposter i **Beslutslogg**-fliken
4. Exportera backup
5. Jämför rad-antalet i varje ark med vad appen visar

### Förväntade resultat

| # | Vad kontrolleras | Förväntat | Appens värde | Excel-värde | OK? |
|---|-----------------|-----------|-------------|-------------|-----|
| 2.1 | Innehav: antal datarader | = antal innehav i appen | | | ☐ |
| 2.2 | Transaktioner: antal datarader | = antal transaktioner i appen | | | ☐ |
| 2.3 | Beslutslogg: antal datarader | = antal loggposter i appen | | | ☐ |
| 2.4 | Historik: antal datarader | = antal historikpunkter (se Importera → Historikposter) | | | ☐ |
| 2.5 | Kassa: sektionsrubrik rad 1 | `SEKTION` / `KassaTransaktioner` | | | ☐ |
| 2.6 | Kassa: sektionsrubrik efter kassatransaktioner | `SEKTION` / `KontoStartsaldo` | | | ☐ |
| 2.7 | Kategorier: antal rader | = antal kategorier (standard: 6) | | | ☐ |
| 2.8 | Innehav: ett slumpmässigt valt innehav — GAV_SEK stämmer | Matchar värdet i Innehav-tabellen i appen | | | ☐ |
| 2.9 | Sammanfattning: Innehavens marknadsvärde | Matchar "Innehavens värde" på Dashboard | | | ☐ |

**Noteringar:**

_______________________________________________

---

## T3 — Export: header-knappen

### Beskrivning
Kontrollerar att exportknappen uppe till höger i headern fungerar identiskt.

### Steg
1. Tryck **⬇ Excel**-knappen i appens header (övre högra hörnet)
2. Granska den nedladdade filen

### Förväntade resultat

| # | Vad kontrolleras | Förväntat | Utfall | OK? |
|---|-----------------|-----------|--------|-----|
| 3.1 | Fil skapas | Samma format som T1 | | ☐ |
| 3.2 | Samma 7 ark | Identisk struktur | | | ☐ |

**Noteringar:**

_______________________________________________

---

## T4 — Import: lyckad återställning (rundtur)

### Beskrivning
Huvudtest. Exportera → rensa all data → importera → verifiera att allt återställts korrekt.

### Steg
1. Notera portföljens nyckeltal (skriv ned i tabellen nedan)
2. Exportera backup via **Backup & Återställning → ⬇ Ladda ner Excel-backup**
3. Gå till **Underhåll → 🗑 Rensa all data** — bekräfta
4. Verifiera att appen är tom (Dashboard visar "—")
5. Gå till **Backup & Återställning → ⬆ Importera från backup**
6. Välj den exporterade filen
7. Läs bekräftelsedialogens text — tryck OK
8. Verifiera att data återställts

### Nyckeltal att jämföra (fyll i INNAN rensning):

| Nyckeltal | Värde FÖRE | Värde EFTER | Matchar? |
|-----------|-----------|-------------|----------|
| Antal innehav | | | ☐ |
| Totalt portföljvärde | | | ☐ |
| Innehavens värde | | | ☐ |
| Nettoinsatt kapital | | | ☐ |
| Tillgänglig likviditet | | | ☐ |
| Antal transaktioner (se Transaktioner-fliken) | | | ☐ |
| Antal loggposter (se Beslutslogg-fliken) | | | ☐ |

### Förväntade resultat

| # | Vad kontrolleras | Förväntat | Utfall | OK? |
|---|-----------------|-----------|--------|-----|
| 4.1 | Bekräftelsedialog visas | Visar backup-version och datum | | ☐ |
| 4.2 | Import genomförs utan felmeddelande | Alert: "Backup återställd!" med statistik | | ☐ |
| 4.3 | Importlogg | Grön rad med antal återställda poster | | ☐ |
| 4.4 | Dashboard: nyckeltal matchar | Se tabell ovan | | ☐ |
| 4.5 | Innehav-fliken: samma antal aktier | Se tabell ovan | | ☐ |
| 4.6 | Transaktioner: samma antal | Se tabell ovan | | ☐ |
| 4.7 | Beslutslogg: samma loggposter | Se tabell ovan | | ☐ |
| 4.8 | Värdeutvecklingsdiagram: historik visas | Diagrammet fylls med historikpunkter | | ☐ |
| 4.9 | Kategorier: samma namn och färger | Inga kategorier har återgått till standard-namn | | ☐ |
| 4.10 | Kassa-fliken: manuella saldon | Kontosaldon matchar vad de var före rensning | | ☐ |

**Noteringar:**

_______________________________________________

---

## T5 — Import: validering av felaktiga filer

### Beskrivning
Kontrollerar att appen hanterar felaktiga filer gracefully — inga krascher, tydliga felmeddelanden.

### Steg per deltest (utför ett i taget):

**T5a — Fel filtyp (CSV)**
1. Välj en Avanza-CSV-fil i importknappen för backup
2. Förväntat: Felmeddelande "arket Innehav saknas"

**T5b — Saknad obligatorisk kolumn**
1. Exportera en backup
2. Öppna i Excel, ta bort kolumnen `Namn` i Innehav-arket, spara
3. Importera den modifierade filen
4. Förväntat: Felmeddelande om saknad kolumn

**T5c — Avbruten import (Avbryt i dialog)**
1. Välj en giltig backup-fil
2. Tryck **Avbryt** i bekräftelsedialogens
3. Förväntat: Ingen data ändras

**T5d — Tom Innehav-tabell**
1. Exportera en backup
2. Öppna i Excel, ta bort alla datarader i Innehav-arket (behåll rubrikraden), spara
3. Importera
4. Förväntat: Varningsdialog visas, möjligt att fortsätta

| # | Deltest | Förväntat | Utfall | OK? |
|---|---------|-----------|--------|-----|
| 5a | CSV-fil importeras | Felmeddelande: arket "Innehav" saknas | | ☐ |
| 5a | Appen kraschar inte | Fortsätter fungera normalt | | ☐ |
| 5b | Saknad kolumn `Namn` | Felmeddelande listar saknade kolumner | | ☐ |
| 5b | Data ändras inte | Befintlig portfölj intakt | | ☐ |
| 5c | Avbryt i dialog | Ingen data ändras | | ☐ |
| 5d | Tom Innehav | Varningsdialogruta visas | | ☐ |

**Noteringar:**

_______________________________________________

---

## T6 — Import: äldre exportformat (v2.07)

### Beskrivning
Kontrollerar att en export utan `BACKUP_VERSION` (t.ex. från v2.07) hanteras med varning men fungerar om Innehav-kolumnerna stämmer.

> **Obs:** Kräver tillgång till en gammal exportfil. Hoppa över om sådan saknas.

### Steg
1. Öppna en backup exporterad med v2.07 (eller ta bort rad 1–2 i Sammanfattning-arket)
2. Välj filen i importknappen
3. Observera dialogen

| # | Vad kontrolleras | Förväntat | Utfall | OK? |
|---|-----------------|-----------|--------|-----|
| 6.1 | Dialog om saknad backup-markering | Visas med fråga om att fortsätta | | ☐ |
| 6.2 | Import lyckas om kolumner finns | Data återställs | | ☐ |

**Noteringar:**

_______________________________________________

---

## T7 — Mobil/iPad

### Beskrivning
Kontrollerar att export- och importknapparna fungerar på iOS Safari (iPad/iPhone).

### Steg
1. Öppna appen i **Safari på iPad**
2. Navigera till Importera via bottom-nav
3. Scrolla ned till **Backup & Återställning**
4. Tryck **⬇ Ladda ner Excel-backup** — filen ska sparas i Filer-appen
5. Tryck **⬆ Importera från backup** — välj filen från Filer-appen

| # | Vad kontrolleras | Förväntat | Utfall | OK? |
|---|-----------------|-----------|--------|-----|
| 7.1 | Backup-sektionen visas | Synlig under Importera | | ☐ |
| 7.2 | Exportknappen är minst 48px hög | Tryckbar utan att missa | | ☐ |
| 7.3 | Export: fil hamnar i Filer-appen | iOS sparar filen korrekt | | ☐ |
| 7.4 | Import: Filer-appen öppnas vid tryck | Kan välja backup-filen | | ☐ |
| 7.5 | Import: bekräftelsedialog visas | Samma som på dator | | ☐ |
| 7.6 | Import: data återställs korrekt | Identisk med T4 | | ☐ |

**Noteringar:**

_______________________________________________

---

## T8 — Kategorier bevaras

### Beskrivning
Kontrollerar specifikt att anpassade kategorier (ej standard) exporteras och importeras korrekt.

### Förutsättning
En kategori ska ha ett anpassat namn, färg eller MA200-inställning som skiljer sig från standard.

### Steg
1. Notera en anpassad kategoris namn, färg och målvikter (Kategorier-fliken → ✏️ redigera)
2. Exportera backup
3. Rensa all data
4. Importera backup
5. Öppna Kategorier-fliken och verifiera

| # | Vad kontrolleras | Förväntat | Utfall | OK? |
|---|-----------------|-----------|--------|-----|
| 8.1 | Kategorinamn bevaras | Anpassat namn återställt | | ☐ |
| 8.2 | Kategori-färg bevaras | Samma hex-färg | | ☐ |
| 8.3 | MA200-regel bevaras | `ma200` eller `ingen` korrekt | | ☐ |
| 8.4 | Målvikter bevaras | Min/Max % samma som före | | ☐ |

**Noteringar:**

_______________________________________________

---

## Sammanfattning

| Testsvit | Antal test | Godkända | Underkända | Ej utförda |
|----------|-----------|---------|-----------|-----------|
| T1 — Export: grundläggande | 7 | | | |
| T2 — Export: dataintegritet | 9 | | | |
| T3 — Export: header-knapp | 2 | | | |
| T4 — Rundtur: export→rensa→import | 10 | | | |
| T5 — Felhantering | 6 | | | |
| T6 — Äldre format | 2 | | | |
| T7 — Mobil/iPad | 6 | | | |
| T8 — Kategorier | 4 | | | |
| **Totalt** | **46** | | | |

**Godkänd?** ☐ Ja &nbsp;&nbsp; ☐ Nej &nbsp;&nbsp; ☐ Godkänd med anmärkningar

**Signatur:** _____________________ &nbsp;&nbsp; **Datum:** _____________________

**Övergripande kommentarer:**

_______________________________________________

_______________________________________________
