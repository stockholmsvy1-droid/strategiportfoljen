"""
Skapar titelbild_v315.png — vit bakgrund, blå kurva som matchar app-ikonen,
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

PAD = 80
f_ttl = lf("GeorgiaPro-Bold.ttf",   72)
f_sub = lf("ArialNova-Light.ttf",    28)
f_ver = lf("ArialNova.ttf",          22)

draw.text((PAD, 52),  "Strategiportföljen", font=f_ttl, fill=(17, 24, 39))
draw.text((PAD, 142), "Personlig portföljapp — version 3.15", font=f_sub, fill=(75, 85, 99))

draw.rectangle([PAD, 182, PAD + 560, 185], fill=(14, 165, 233))

CURVE_TOP = 210
CURVE_BOT = H - 30

import random
random.seed(42)

n = 120
xs = [PAD + i * (W - 2*PAD) / (n-1) for i in range(n)]

pts_raw = []
val = 0.18
for i in range(n):
    trend = i / (n-1)
    noise = random.gauss(0, 0.018)
    val   = val * 0.85 + (trend * 0.92 + 0.06 + noise) * 0.15
    pts_raw.append(val)

mn, mx = min(pts_raw), max(pts_raw)
ys = [CURVE_BOT - (v - mn) / (mx - mn) * (CURVE_BOT - CURVE_TOP) for v in pts_raw]

fill_pts = list(zip(xs, ys)) + [(xs[-1], CURVE_BOT + 10), (xs[0], CURVE_BOT + 10)]
draw.polygon(fill_pts, fill=(219, 234, 254))

for i in range(len(xs) - 1):
    draw.line([(xs[i], ys[i]), (xs[i+1], ys[i+1])],
              fill=(37, 99, 235), width=4)

draw.ellipse([xs[-1]-8, ys[-1]-8, xs[-1]+8, ys[-1]+8],
             fill=(37, 99, 235), outline=(255,255,255), width=2)

y_ref = ys[0]
draw.line([(PAD, y_ref), (W - PAD, y_ref)],
          fill=(209, 213, 219), width=1)

f_ft = lf("ArialNova-Light.ttf", 18)
draw.text((PAD, H - 28), "Byggt för Martin  ·  Strategi sedan januari 2026",
          font=f_ft, fill=(156, 163, 175))

img.save(r"C:\Users\hejma\Projekt_Claude\strategiportfoljen\titelbild_v315.png",
         "PNG", dpi=(150, 150))
print("Skapad: titelbild_v315.png")
