#!/usr/bin/env python3
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw

# Config
W, H = 3840, 2160  # 4K UHD
SCALE = 4  # pixelation factor (work at lower res then upscale)
LOW_W, LOW_H = W // SCALE, H // SCALE

OUTPUT_DIR = Path("/Users/hexlo/.dotfiles/ghostty")
PNG_PATH = OUTPUT_DIR / "nightsky_retro_pixel.png"
JPG_PATH = OUTPUT_DIR / "nightsky_retro_pixel.jpg"

# Retro-futuristic palette (purples, cyans, pinks)
PALETTE = {
    "bg_top": (10, 8, 26),
    "bg_bottom": (4, 2, 10),
    "star1": (245, 245, 245),
    "star2": (180, 220, 255),
    "star3": (255, 180, 240),
    "moon_light": (240, 240, 255),
    "moon_dark": (200, 200, 230),
    "andromeda_core": (255, 160, 200),
    "andromeda_arm": (160, 200, 255),
    "glow_cyan": (0, 255, 220),
    "glow_magenta": (255, 60, 200),
}

rnd = random.Random(42)


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))


# Draw background gradient
img_low = Image.new("RGB", (LOW_W, LOW_H), PALETTE["bg_bottom"])
draw = ImageDraw.Draw(img_low)
for y in range(LOW_H):
    t = y / (LOW_H - 1)
    col = lerp_color(PALETTE["bg_top"], PALETTE["bg_bottom"], t)
    draw.line([(0, y), (LOW_W, y)], fill=col)

# Stars (random plus a few twinkles)
for _ in range(int(LOW_W * LOW_H * 0.0012)):
    x = rnd.randrange(0, LOW_W)
    y = rnd.randrange(0, LOW_H)
    color = rnd.choice([PALETTE["star1"], PALETTE["star2"], PALETTE["star3"]])
    draw.point((x, y), fill=color)
    if rnd.random() < 0.1:
        # small cross twinkle
        if 1 < x < LOW_W - 2 and 1 < y < LOW_H - 2:
            draw.point((x - 1, y), fill=color)
            draw.point((x + 1, y), fill=color)
            draw.point((x, y - 1), fill=color)
            draw.point((x, y + 1), fill=color)

# Moon (full)
moon_r = LOW_H // 9
moon_cx = int(LOW_W * 0.78)
moon_cy = int(LOW_H * 0.28)
for r in range(moon_r, 0, -1):
    t = r / moon_r
    col = lerp_color(PALETTE["moon_light"], PALETTE["moon_dark"], 1 - t * 0.7)
    bbox = [moon_cx - r, moon_cy - r, moon_cx + r, moon_cy + r]
    draw.ellipse(bbox, outline=None, fill=col)
# simple pixel craters
for _ in range(30):
    ang = rnd.random() * 2 * math.pi
    rr = rnd.random() * (moon_r * 0.7)
    cx = int(moon_cx + math.cos(ang) * rr)
    cy = int(moon_cy + math.sin(ang) * rr)
    cr = rnd.randint(1, 3)
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(185, 185, 210))

# Andromeda-like spiral galaxy
# center left/top quadrant
gx, gy = int(LOW_W * 0.32), int(LOW_H * 0.35)
for arm in range(2):
    theta_offset = arm * math.pi
    for i in range(500):
        t = i / 500
        theta = 8 * math.pi * t + theta_offset
        radius = lerp(5, LOW_H * 0.28, t) * (0.9 + 0.2 * rnd.random())
        x = int(gx + math.cos(theta) * radius)
        y = int(gy + math.sin(theta) * radius)
        if 0 <= x < LOW_W and 0 <= y < LOW_H:
            # mix color toward core near center
            d = math.hypot(x - gx, y - gy) / (LOW_H * 0.28)
            col = lerp_color(PALETTE["andromeda_core"], PALETTE["andromeda_arm"], min(1, d))
            draw.point((x, y), fill=col)
            # slight fuzzy halo
            if rnd.random() < 0.2:
                for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < LOW_W and 0 <= yy < LOW_H:
                        draw.point((xx, yy), fill=col)

# Astronaut silhouette (retro pixelated)
# Construct from rectangles and circles (helmet)
base_x = int(LOW_W * 0.62)
base_y = int(LOW_H * 0.62)
unit = max(2, LOW_H // 72)

# body
draw.rectangle([base_x - 3*unit, base_y - 8*unit, base_x + 3*unit, base_y + 5*unit], fill=(20, 20, 30))
# helmet
draw.ellipse([base_x - 4*unit, base_y - 12*unit, base_x + 4*unit, base_y - 4*unit], fill=(30, 30, 45))
# visor
draw.rectangle([base_x - 3*unit, base_y - 10*unit, base_x + 3*unit, base_y - 7*unit], fill=(10, 180, 200))
# backpack
draw.rectangle([base_x + 3*unit, base_y - 6*unit, base_x + 6*unit, base_y + 3*unit], fill=(25, 25, 40))
# arms
draw.rectangle([base_x - 6*unit, base_y - 4*unit, base_x - 3*unit, base_y - 1*unit], fill=(25, 25, 40))
draw.rectangle([base_x + 3*unit, base_y - 4*unit, base_x + 6*unit, base_y - 1*unit], fill=(25, 25, 40))
# legs
draw.rectangle([base_x - 2*unit, base_y + 5*unit, base_x - 1*unit, base_y + 10*unit], fill=(25, 25, 40))
draw.rectangle([base_x + 1*unit, base_y + 5*unit, base_x + 2*unit, base_y + 10*unit], fill=(25, 25, 40))

# subtle neon ground grid at bottom (retro-futuristic)
for i in range(0, LOW_H // 3):
    y = LOW_H - i - 1
    if y % 8 == 0:
        draw.line([(0, y), (LOW_W, y)], fill=PALETTE["glow_cyan"])
for x in range(0, LOW_W, 32):
    draw.line([(x, int(LOW_H * 0.7)), (x, LOW_H)], fill=PALETTE["glow_magenta"])

# Upscale to 4k with nearest neighbor for crisp pixels
img = img_low.resize((W, H), resample=Image.Resampling.NEAREST)

# Optional slight vignette to draw eye to center (fix mask order)
R = max(W, H) // 2
vignette = Image.new("L", (W, H), 0)
vdraw = ImageDraw.Draw(vignette)
for r in range(R, 0, -60):  # draw large -> small so center ends brighter
    t = r / R
    alpha = int(180 * (1 - t))  # 0 at edges, up to ~180 at center
    bbox = [W//2 - r, H//2 - r, W//2 + r, H//2 + r]
    vdraw.ellipse(bbox, outline=None, fill=alpha)
img.putalpha(255)
img = Image.composite(img, Image.new("RGBA", (W, H), (0,0,0,255)), vignette)
img = img.convert("RGB")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
img.save(PNG_PATH, format="PNG", optimize=True)
img.save(JPG_PATH, format="JPEG", quality=92, optimize=True, progressive=True)

print(f"Wrote: {PNG_PATH}")
print(f"Wrote: {JPG_PATH}")
