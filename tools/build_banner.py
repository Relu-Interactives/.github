#!/usr/bin/env python3
"""Generate a theme-proof hero banner for the Relu Interactives GitHub org profile."""
import os
from PIL import Image, ImageDraw, ImageFont

ASSETS = os.path.join(os.path.dirname(__file__), "..", "profile", "assets")
ASSETS = os.path.abspath(ASSETS)

# ---- Brand palette -------------------------------------------------------
BG_TOP    = (12, 14, 20)     # #0C0E14 deep charcoal
BG_BOT    = (20, 23, 33)     # #141721
ORANGE    = (255, 122, 38)   # #FF7A26
RED       = (240, 62, 42)    # #F03E2A
WHITE     = (245, 247, 250)
MUTED     = (150, 158, 173)  # #969EAD

SCALE = 2
W, H = 1200 * SCALE, 360 * SCALE

# ---- Helpers -------------------------------------------------------------
def load_font(size, bold=True):
    candidates = [
        ("/System/Library/Fonts/Avenir Next.ttc", 7 if bold else 4),
        ("/System/Library/Fonts/HelveticaNeue.ttc", 1 if bold else 0),
        ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 0),
        ("/System/Library/Fonts/SFNS.ttf", 0),
    ]
    for path, idx in candidates:
        if os.path.exists(path):
            try:
                f = ImageFont.truetype(path, size, index=idx)
                return f
            except Exception:
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
    return ImageFont.load_default()

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# ---- Background: vertical gradient + warm orange glow --------------------
small = Image.new("RGB", (2, 64))
for y in range(64):
    small.putpixel((0, y), lerp(BG_TOP, BG_BOT, y / 63))
    small.putpixel((1, y), lerp(BG_TOP, BG_BOT, y / 63))
bg = small.resize((W, H), Image.BILINEAR)

# soft radial orange glow in the lower-left for brand warmth
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
cx, cy = int(W * 0.12), int(H * 0.95)
maxr = int(W * 0.55)
for i in range(maxr, 0, -6):
    alpha = int(70 * (1 - i / maxr) ** 2)
    gd.ellipse([cx - i, cy - i, cx + i, cy + i], fill=alpha)
orange_layer = Image.new("RGB", (W, H), ORANGE)
bg = Image.composite(orange_layer, bg, glow)

# faint second glow (red) top-right
glow2 = Image.new("L", (W, H), 0)
gd2 = ImageDraw.Draw(glow2)
cx2, cy2 = int(W * 0.92), int(H * 0.05)
maxr2 = int(W * 0.40)
for i in range(maxr2, 0, -6):
    alpha = int(45 * (1 - i / maxr2) ** 2)
    gd2.ellipse([cx2 - i, cy2 - i, cx2 + i, cy2 + i], fill=alpha)
red_layer = Image.new("RGB", (W, H), RED)
bg = Image.composite(red_layer, bg, glow2)

bg = bg.convert("RGBA")

# The android-chrome icon ships with its own white circular background, so it
# is already theme-proof — use it as-is (a clean white logo badge on the dark
# banner). No recolor needed.
icon = Image.open(os.path.join(ASSETS, "relu-icon.png")).convert("RGBA")

# scale icon for banner
icon_h = int(170 * SCALE)
icon_w = int(icon.width * icon_h / icon.height)
icon_b = icon.resize((icon_w, icon_h), Image.LANCZOS)

# ---- Text ----------------------------------------------------------------
name_font = load_font(int(70 * SCALE), bold=True)
tag_font  = load_font(int(27 * SCALE), bold=False)

draw = ImageDraw.Draw(bg)
name_text = "Relu Interactives"
tag_text  = "Immersive Tech · WebXR · AR / VR — built in Africa"

nb = draw.textbbox((0, 0), name_text, font=name_font)
tb = draw.textbbox((0, 0), tag_text, font=tag_font)
name_w, name_h = nb[2] - nb[0], nb[3] - nb[1]
tag_w,  tag_h  = tb[2] - tb[0], tb[3] - tb[1]

gap = int(38 * SCALE)
text_w = max(name_w, tag_w)
group_w = icon_w + gap + text_w
start_x = (W - group_w) // 2

# vertical centering of the icon
icon_y = (H - icon_h) // 2
bg.alpha_composite(icon_b, (start_x, icon_y))

# text block vertical layout
line_gap = int(20 * SCALE)
rule_h = int(5 * SCALE)
block_h = name_h + line_gap + tag_h
block_y = (H - block_h) // 2 - int(6 * SCALE)
text_x = start_x + icon_w + gap

draw.text((text_x - nb[0], block_y - nb[1]), name_text, font=name_font, fill=WHITE)

# orange gradient rule under the name
rule_y = block_y + name_h + int(10 * SCALE)
rule_w = int(name_w * 0.62)
for i in range(rule_w):
    draw.line([(text_x + i, rule_y), (text_x + i, rule_y + rule_h)],
              fill=lerp(ORANGE, RED, i / max(rule_w - 1, 1)))

tag_y = rule_y + rule_h + int(14 * SCALE)
draw.text((text_x - tb[0], tag_y - tb[1]), tag_text, font=tag_font, fill=MUTED)

# ---- Save (display width = W/SCALE) --------------------------------------
out = bg.resize((W // SCALE, H // SCALE), Image.LANCZOS)
out_path = os.path.join(ASSETS, "relu-banner.png")
out.save(out_path)
print("wrote", out_path, out.size)
