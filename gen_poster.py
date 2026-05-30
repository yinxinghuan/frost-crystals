#!/usr/bin/env python3
"""Compose frost-crystals poster — shader screenshot + italic title at top."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, '_dev_poster_raw.png')
OUT  = os.path.join(ROOT, 'poster.png')
TARGET = 1024

FONT_CANDIDATES = [
    '/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf',
    '/System/Library/Fonts/Supplemental/Georgia Italic.ttf',
    '/System/Library/Fonts/NewYorkItalic.ttf',
]
def find_font(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

font_serif = find_font(FONT_CANDIDATES)

img = Image.open(SRC).convert('RGB')
w, h = img.size
print(f'src size: {w}x{h}')

# Resize to fit-width 1024 then pad/offset down so the snowflake sits at the
# lower 70% (giving the title a clean cosmic band up top).
scale = TARGET / w
new_w = TARGET
new_h = int(h * scale)
src = img.resize((new_w, new_h), Image.LANCZOS)
canvas = Image.new('RGB', (TARGET, TARGET), (4, 6, 13))
# Offset down so snowflake center lands ~58% from top of poster
canvas.paste(src, (0, int(TARGET * 0.18)))
img = canvas

# Top darkening fade for title legibility
mask = Image.new('L', (TARGET, TARGET), 0)
mdraw = ImageDraw.Draw(mask)
for y in range(0, 360):
    a = int((1 - y / 360) ** 1.4 * 230)
    mdraw.line([(0, y), (TARGET, y)], fill=a)
darken = Image.new('RGB', (TARGET, TARGET), (2, 4, 10))
img.paste(darken, (0, 0), mask)

draw = ImageDraw.Draw(img, 'RGBA')

ICE = (228, 240, 255, 248)
SUB_ICE = (200, 224, 255, 170)

title = 'frost'
TITLE_SIZE = 160
font_title = ImageFont.truetype(font_serif, TITLE_SIZE) if font_serif else ImageFont.load_default()
bbox = draw.textbbox((0, 0), title, font=font_title)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
tx = (TARGET - tw) // 2
ty = 85
# Subtle frost halo behind the title
for dx, dy, alpha in [(-2,-2,80),(2,-2,80),(-2,2,80),(2,2,80),(0,0,150)]:
    draw.text((tx+dx, ty+dy), title, fill=(120, 180, 230, alpha), font=font_title)
draw.text((tx, ty), title, fill=ICE, font=font_title)

sub = 'breathe on the glass'
SUB_SIZE = 32
font_sub = ImageFont.truetype(font_serif, SUB_SIZE) if font_serif else ImageFont.load_default()
sbbox = draw.textbbox((0, 0), sub, font=font_sub)
sw = sbbox[2] - sbbox[0]
sx = (TARGET - sw) // 2
sy = ty + th + 38
draw.text((sx, sy), sub, fill=SUB_ICE, font=font_sub)

img.save(OUT, 'PNG', optimize=True)
print(f'wrote {OUT}  {TARGET}x{TARGET}')
