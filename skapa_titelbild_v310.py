"""
Skapar titelbild_v310.png — vit bakgrund, blå kurva som matchar app-ikonen,
svart text för appnamn och underrubrik
"""
import math
from PIL import Image, ImageDraw, ImageFont

FONTS = r"C:\Windows\Fonts"
W, H  = 1760, 520

def lf(name, size):
    try:
        return ImageFont.truetype(fr"{FONTS}\{name}", size)
    except Exception:
        return ImageFont.load_default()

img  = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

# ── Titel (svart text, vänsterjusterad med vänstermarginal) ──────
PAD = 80
f_ttl = lf("GeorgiaPro-Bold.ttf",   72)
f_sub = lf("ArialNova-Light.ttf",    28)
f_ver = lf("ArialNova.ttf",          22)

draw.text((PAD, 52),  "Strategiportföljen", font=f_ttl, fill=(17, 24, 39))
draw.text((PAD, 142), "Personlig portföljapp — version 3.10", font=f_sub, fill=(75, 85, 99))

# Tunn accentlinje under subtiteln
draw.rectangle([PAD, 182, PAD + 560, 185], fill=(14, 165, 233))

# ── Blå kurva (matchar app-ikonen: stigande linje med fin svängning) ──
# Kurvan täcker hela bredden i nedre halvan av bilden
CURVE_TOP = 210
CURVE_BOT = H - 30

# Generera en kurva som liknar en börsgraf / app-ikon
# Startar lågt vänster, stiger med lite volatilitet, slutar högt höger
import random
random.seed(42)

n = 120
xs = [PAD + i * (W - 2*PAD) / (n-1) for i in range(n)]

# Kurva: smooth stigande med lite naturlig volatilitet
# Baslinjetrend: 0 → 1 (normaliserad)
pts_raw = []
val = 0.18
for i in range(n):
    trend = i / (n-1)
    noise = random.gauss(0, 0.018)
    val   = val * 0.85 + (trend * 0.92 + 0.06 + noise) * 0.15
    pts_raw.append(val)

# Normalisera till Y-koordinater
mn, mx = min(pts_raw), max(pts_raw)
ys = [CURVE_BOT - (v - mn) / (mx - mn) * (CURVE_BOT - CURVE_TOP) for v in pts_raw]

# Fyllning under kurvan (ljusblå gradient-effekt)
fill_pts = list(zip(xs, ys)) + [(xs[-1], CURVE_BOT + 10), (xs[0], CURVE_BOT + 10)]
draw.polygon(fill_pts, fill=(219, 234, 254))  # #DBE4FE ljusblå

# Rita kurvan (mörkblå, tjock)
for i in range(len(xs) - 1):
    draw.line([(xs[i], ys[i]), (xs[i+1], ys[i+1])],
              fill=(37, 99, 235), width=4)  # #2563EB

# Slutpunkt-markering (liten fylld cirkel)
draw.ellipse([xs[-1]-8, ys[-1]-8, xs[-1]+8, ys[-1]+8],
             fill=(37, 99, 235), outline=(255,255,255), width=2)

# Subtil horisontell referenslinje (startnivå)
y_ref = ys[0]
draw.line([(PAD, y_ref), (W - PAD, y_ref)],
          fill=(209, 213, 219), width=1)

# ── Footer ──
f_ft = lf("ArialNova-Light.ttf", 18)
draw.text((PAD, H - 28), "Byggt för Martin  ·  Strategi sedan januari 2026",
          font=f_ft, fill=(156, 163, 175))

img.save(r"C:\Users\hejma\Projekt_Claude\strategiportfoljen\titelbild_v310.png",
         "PNG", dpi=(150, 150))
print("Skapad: titelbild_v310.png")
