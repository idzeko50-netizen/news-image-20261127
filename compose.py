#!/usr/bin/env python3
"""Draw entry/entry.png: a newspaper front page summing up Friday
27 November 2026 in one image. Every illustration is drawn in code
with PIL; no photographs, no downloaded images. Run: python3 compose.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)
INK = (26, 26, 26)
INK_SOFT = (74, 68, 58)
RED = (164, 31, 31)
BLUE = (31, 78, 121)
GOLD = (176, 141, 58)
GREEN = (46, 110, 74)
SKY = (214, 228, 238)
SEA = (168, 196, 214)
SAND = (226, 205, 164)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(lines, max_lines, what):
    assert len(lines) <= max_lines, "%s needs %d lines: %r" % (
        what, len(lines), lines)
    return lines


def hline(d, x0, x1, y, wdt=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def vline(d, x, y0, y1, wdt=1, fill=INK):
    d.line([(x, y0), (x, y1)], fill=fill, width=wdt)


def centred(d, y, text, fnt, fill=INK, cx=W // 2):
    d.text((cx - fnt.getlength(text) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- masthead

def draw_masthead(d):
    hline(d, 24, 1000, 10, 3)
    hline(d, 24, 1000, 15, 1)
    centred(d, 24, "Friday 27 November 2026", SERIF_B(46))
    strap = ("Every story below happened, or was first reported, "
             "on Friday 27 November 2026.")
    centred(d, 82, strap, SERIF(15), fill=INK_SOFT)


def draw_number_strip(d):
    """Six numbered facts in a row, y 106..150."""
    nums = [
        ("65", "seats: NZ coalition one short"),
        ("400", "flights cancelled in US storm"),
        ("9", "killed in Gaza strikes"),
        ("16", "dead in Indonesia mine"),
        ("$49bn", "Ukraine loan deadlocked"),
        ("$353bn", "Japan defence plan"),
    ]
    x0, y0, cw, chh = 24, 106, 160, 44
    gap = 3
    for i, (num, label) in enumerate(nums):
        x = x0 + i * (cw + gap)
        d.rectangle([x, y0, x + cw, y0 + chh], outline=INK, width=1)
        d.rectangle([x, y0, x + cw, y0 + 15], fill=INK)
        centred(d, y0 + 2, num, SANS_B(11), fill=PAPER, cx=x + cw // 2)
        lines = fit(wrap(label, SANS(10), cw - 10), 2, "strip %s" % num)
        ly = y0 + 18
        for ln in lines:
            centred(d, ly, ln, SANS(10), cx=x + cw // 2)
            ly += 12


REGION_COLORS = {
    "Americas": (164, 31, 31),
    "Asia": (31, 78, 121),
    "Middle East": (176, 141, 58),
    "Europe": (46, 110, 74),
    "Oceania": (110, 84, 148),
    "Africa": (196, 98, 44),
    "Global": (90, 90, 90),
}
REGIONS = [("Americas", 7), ("Asia", 8), ("Middle East", 5),
           ("Europe", 4), ("Oceania", 3), ("Africa", 1), ("Global", 2)]


def draw_region_bar(d):
    """Stacked bar, widths proportional to counts; legend underneath."""
    y0, hgt = 160, 14
    total = sum(c for _, c in REGIONS)
    x = 24
    for name, count in REGIONS:
        wdt = int(round(976 * count / total))
        d.rectangle([x, y0, x + wdt - 1, y0 + hgt],
                    fill=REGION_COLORS[name])
        x += wdt
    # legend, one line
    parts, lx = [], 24
    for name, count in REGIONS:
        parts.append("%s %d" % (name, count))
    legend = "   ·   ".join(parts)
    assert SANS(11).getlength(legend) <= 976, "legend too long"
    d.text((24, 178), legend, font=SANS(11), fill=INK_SOFT)
    d.text((24, 196), "THE DAY IN FULL  —  13 STORIES IN PICTURES",
           font=SANS_B(12), fill=RED)


# ------------------------------------------------------------------- scenes
# Each scene draws into (x, y, w, h) with flat vector-style shapes.
# Geometry is height-relative so the same scene works at large (h~108)
# and small (h~62) sizes.

def scene_nz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(120, 150, 110))
    # parliament block + beehive tower
    d.rectangle([x + w * 0.10, y + h * 0.34, x + w * 0.58, y + h * 0.72],
                fill=(90, 96, 110))
    d.rectangle([x + w * 0.62, y + h * 0.18, x + w * 0.90, y + h * 0.72],
                fill=(70, 76, 92))
    d.ellipse([x + w * 0.64, y + h * 0.06, x + w * 0.88, y + h * 0.22],
              fill=(70, 76, 92))
    for i in range(5):
        wx = x + w * (0.15 + i * 0.09)
        d.rectangle([wx, y + h * 0.42, wx + w * 0.05, y + h * 0.56],
                    fill=(220, 225, 230))
    # flagpole + flag
    d.line([(x + w * 0.76, y + h * 0.06), (x + w * 0.76, y)],
           fill=INK, width=2)
    d.polygon([(x + w * 0.76, y), (x + w * 0.94, y + h * 0.05),
               (x + w * 0.76, y + h * 0.10)], fill=RED)
    # seat bars: coalition 65 vs 65 needed
    bx, by = x + w * 0.08, y + h * 0.78
    d.rectangle([bx, by, bx + w * 0.42, by + h * 0.08], fill=BLUE)
    d.rectangle([bx, by + h * 0.11, bx + w * 0.42, by + h * 0.19],
                fill=(150, 150, 150))
    d.text((bx + w * 0.46, by - 2), "65 – 65", font=SANS_B(max(9, h // 8)),
           fill=INK)


def scene_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 74, 92))
    # clouds
    for cx, cy, r in [(0.22, 0.22, 0.16), (0.38, 0.16, 0.13),
                      (0.62, 0.22, 0.15), (0.80, 0.16, 0.12)]:
        d.ellipse([x + w * (cx - r), y + h * (cy - r * 0.7),
                   x + w * (cx + r), y + h * (cy + r * 0.7)],
                  fill=(200, 208, 216))
    # rain
    for i in range(9):
        rx = x + w * (0.08 + i * 0.10)
        d.line([(rx, y + h * 0.42), (rx - w * 0.02, y + h * 0.58)],
               fill=(170, 190, 210), width=2)
    # lightning
    d.polygon([(x + w * 0.55, y + h * 0.30), (x + w * 0.62, y + h * 0.30),
               (x + w * 0.56, y + h * 0.52), (x + w * 0.63, y + h * 0.52),
               (x + w * 0.50, y + h * 0.78), (x + w * 0.54, y + h * 0.55),
               (x + w * 0.48, y + h * 0.55)], fill=GOLD)
    # grounded plane
    d.rectangle([x, y + h * 0.82, x + w, y + h], fill=(40, 48, 58))
    d.ellipse([x + w * 0.12, y + h * 0.84, x + w * 0.88, y + h * 0.94],
              fill=(200, 205, 210))
    d.polygon([(x + w * 0.80, y + h * 0.86), (x + w * 0.92, y + h * 0.80),
               (x + w * 0.92, y + h * 0.88)], fill=(200, 205, 210))


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 188))
    # smoke
    for cx, cy, r in [(0.30, 0.20, 0.12), (0.45, 0.14, 0.10),
                      (0.65, 0.22, 0.11)]:
        d.ellipse([x + w * (cx - r), y + h * (cy - r * 0.6),
                   x + w * (cx + r), y + h * (cy + r * 0.6)],
                  fill=(150, 140, 130))
    # ruined building, broken top
    d.polygon([(x + w * 0.12, y + h), (x + w * 0.12, y + h * 0.45),
               (x + w * 0.22, y + h * 0.34), (x + w * 0.30, y + h * 0.46),
               (x + w * 0.40, y + h * 0.36), (x + w * 0.50, y + h * 0.48),
               (x + w * 0.50, y + h)], fill=(120, 108, 96))
    d.rectangle([x + w * 0.56, y + h * 0.55, x + w * 0.88, y + h],
                fill=(96, 86, 76))
    for i in range(3):
        wy = y + h * (0.60 + i * 0.13)
        d.rectangle([x + w * 0.62, wy, x + w * 0.70, wy + h * 0.06],
                    fill=(40, 36, 32))
        d.rectangle([x + w * 0.76, wy, x + w * 0.84, wy + h * 0.06],
                    fill=(40, 36, 32))
    # rubble
    for cx, cw in [(0.18, 0.10), (0.30, 0.08), (0.92, 0.09)]:
        d.polygon([(x + w * (cx - cw), y + h),
                   (x + w * cx, y + h * 0.90),
                   (x + w * (cx + cw), y + h)], fill=(90, 80, 70))


def scene_kuwait(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 34, 52))
    # stars
    for sx, sy in [(0.1, 0.12), (0.3, 0.08), (0.55, 0.14), (0.8, 0.08),
                   (0.92, 0.18)]:
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 2, y + h * sy + 2],
                  fill=(220, 220, 200))
    # oil facility: towers + flare
    d.rectangle([x + w * 0.08, y + h * 0.55, x + w * 0.20, y + h * 0.88],
                fill=(120, 128, 140))
    d.rectangle([x + w * 0.26, y + h * 0.42, x + w * 0.36, y + h * 0.88],
                fill=(100, 108, 122))
    d.rectangle([x + w * 0.42, y + h * 0.62, x + w * 0.62, y + h * 0.88],
                fill=(120, 128, 140))
    d.polygon([(x + w * 0.28, y + h * 0.42), (x + w * 0.34, y + h * 0.30),
               (x + w * 0.40, y + h * 0.42)], fill=GOLD)
    d.rectangle([x, y + h * 0.88, x + w, y + h], fill=(16, 22, 34))
    # drone above, with red alert ring
    dx, dy = x + w * 0.72, y + h * 0.24
    d.ellipse([dx - w * 0.10, dy - h * 0.10, dx + w * 0.10,
               dy + h * 0.10], outline=RED, width=2)
    d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(220, 220, 220))
    for ox, oy in [(-0.07, -0.05), (0.07, -0.05), (-0.07, 0.05),
                   (0.07, 0.05)]:
        d.ellipse([dx + w * ox - 3, dy + h * oy - 3,
                   dx + w * ox + 3, dy + h * oy + 3],
                  outline=(220, 220, 220), width=1)


def scene_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 244))
    # EU flag disc, cracked in two
    cx, cy, r = x + w * 0.50, y + h * 0.46, min(w, h) * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE)
    import math
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        sx, sy = cx + r * 0.72 * math.cos(a), cy + r * 0.72 * math.sin(a)
        d.polygon([(sx, sy - 3), (sx + 1, sy + 1), (sx + 3, sy + 1),
                   (sx + 1.5, sy + 2.5), (sx + 2, sy + 5),
                   (sx, sy + 3.5), (sx - 2, sy + 5), (sx - 1.5, sy + 2.5),
                   (sx - 3, sy + 1), (sx - 1, sy + 1)], fill=GOLD)
    # jagged crack down the disc
    pts = [(cx - r * 0.10, cy - r), (cx + r * 0.12, cy - r * 0.5),
           (cx - r * 0.08, cy), (cx + r * 0.12, cy + r * 0.5),
           (cx - r * 0.05, cy + r)]
    d.line(pts, fill=PAPER, width=3)
    # two halves pulled apart: euro sign left, question right
    d.text((x + w * 0.06, y + h * 0.82), "€45bn", font=SANS_B(max(9, h // 7)),
           fill=BLUE)
    d.text((x + w * 0.72, y + h * 0.82), "no deal", font=SANS_B(max(9, h // 7)),
           fill=RED)


def scene_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(44, 52, 70))
    # skyline
    for bx, bw, bh in [(0.04, 0.14, 0.34), (0.22, 0.12, 0.46),
                       (0.38, 0.16, 0.30), (0.58, 0.12, 0.50),
                       (0.74, 0.14, 0.36), (0.90, 0.08, 0.28)]:
        d.rectangle([x + w * bx, y + h * (0.88 - bh), x + w * (bx + bw),
                     y + h * 0.88], fill=(20, 24, 34))
        for wy in range(3):
            d.rectangle([x + w * (bx + 0.03), y + h * (0.90 - bh + wy * 0.10),
                         x + w * (bx + 0.06), y + h * (0.92 - bh + wy * 0.10)],
                        fill=GOLD)
    d.rectangle([x, y + h * 0.88, x + w, y + h], fill=(14, 16, 22))
    # lightning over the grid
    d.polygon([(x + w * 0.48, y + h * 0.06), (x + w * 0.55, y + h * 0.06),
               (x + w * 0.49, y + h * 0.30), (x + w * 0.56, y + h * 0.30),
               (x + w * 0.44, y + h * 0.56), (x + w * 0.47, y + h * 0.33),
               (x + w * 0.41, y + h * 0.33)], fill=GOLD)
    # pylon
    px = x + w * 0.82
    d.line([(px, y + h * 0.88), (px, y + h * 0.55)], fill=(150, 150, 150),
           width=2)
    d.line([(px - w * 0.06, y + h * 0.60), (px + w * 0.06, y + h * 0.60)],
           fill=(150, 150, 150), width=2)


def scene_guinea(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 204))
    # ballot box
    d.rectangle([x + w * 0.14, y + h * 0.48, x + w * 0.62, y + h * 0.88],
                fill=(206, 32, 41))
    d.rectangle([x + w * 0.10, y + h * 0.40, x + w * 0.66, y + h * 0.48],
                fill=(150, 20, 28))
    d.rectangle([x + w * 0.34, y + h * 0.43, x + w * 0.42, y + h * 0.45],
                fill=PAPER)
    # ballot going in
    d.polygon([(x + w * 0.30, y + h * 0.10), (x + w * 0.46, y + h * 0.10),
               (x + w * 0.46, y + h * 0.40), (x + w * 0.30, y + h * 0.40)],
              fill=(255, 255, 255), outline=INK)
    d.text((x + w * 0.33, y + h * 0.20), "✓", font=SANS_B(max(10, h // 6)),
           fill=GREEN)
    # calendar page stamped 2028
    d.rectangle([x + w * 0.68, y + h * 0.14, x + w * 0.94, y + h * 0.62],
                fill=(255, 255, 255), outline=INK)
    d.rectangle([x + w * 0.68, y + h * 0.14, x + w * 0.94, y + h * 0.28],
                fill=RED)
    d.text((x + w * 0.72, y + h * 0.34), "2028",
           font=SANS_B(max(10, h // 6)), fill=RED)
    d.line([(x + w * 0.66, y + h * 0.80), (x + w * 0.96, y + h * 0.80)],
           fill=RED, width=2)


def scene_mine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(188, 158, 118))
    # hill + shaft cross-section
    d.polygon([(x, y + h * 0.45), (x + w * 0.30, y + h * 0.18),
               (x + w * 0.70, y + h * 0.18), (x + w, y + h * 0.45),
               (x + w, y + h), (x, y + h)], fill=(122, 94, 62))
    d.polygon([(x + w * 0.42, y + h * 0.30), (x + w * 0.58, y + h * 0.30),
               (x + w * 0.66, y + h), (x + w * 0.34, y + h)],
              fill=(40, 30, 22))
    # ropes
    d.line([(x + w * 0.46, y + h * 0.28), (x + w * 0.40, y + h * 0.95)],
           fill=(230, 220, 200), width=2)
    d.line([(x + w * 0.54, y + h * 0.28), (x + w * 0.60, y + h * 0.95)],
           fill=(230, 220, 200), width=2)
    # helmet + lamp at the shaft mouth
    d.ellipse([x + w * 0.44, y + h * 0.20, x + w * 0.56, y + h * 0.30],
              fill=GOLD)
    d.ellipse([x + w * 0.485, y + h * 0.235, x + w * 0.515,
               y + h * 0.265], fill=(255, 255, 220))
    # water line in the shaft
    d.rectangle([x + w * 0.40, y + h * 0.72, x + w * 0.62, y + h * 0.78],
                fill=(60, 110, 160))
    # rescue figures
    d.ellipse([x + w * 0.12, y + h * 0.55, x + w * 0.20, y + h * 0.63],
              fill=(200, 60, 40))
    d.rectangle([x + w * 0.13, y + h * 0.63, x + w * 0.19, y + h * 0.82],
                fill=(200, 60, 40))


def scene_brazil(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 236, 222))
    # bank facade with columns
    d.polygon([(x + w * 0.10, y + h * 0.30), (x + w * 0.50, y + h * 0.12),
               (x + w * 0.90, y + h * 0.30)], fill=(30, 90, 50))
    d.rectangle([x + w * 0.12, y + h * 0.30, x + w * 0.88, y + h * 0.88],
                fill=(240, 244, 238))
    for i in range(4):
        cx = x + w * (0.22 + i * 0.18)
        d.rectangle([cx, y + h * 0.36, cx + w * 0.07, y + h * 0.82],
                    fill=(30, 90, 50))
    d.rectangle([x + w * 0.12, y + h * 0.82, x + w * 0.88, y + h * 0.88],
                fill=(30, 90, 50))
    # flag stripe on the pediment
    d.rectangle([x + w * 0.42, y + h * 0.20, x + w * 0.58, y + h * 0.26],
                fill=GOLD)
    # briefcase
    d.rectangle([x + w * 0.68, y + h * 0.68, x + w * 0.92, y + h * 0.84],
                fill=(90, 60, 30))
    d.rectangle([x + w * 0.76, y + h * 0.62, x + w * 0.84, y + h * 0.68],
                outline=(90, 60, 30), width=2)


def scene_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # rising sun
    d.ellipse([x + w * 0.68, y + h * 0.08, x + w * 0.92, y + h * 0.38],
              fill=(188, 40, 40))
    # warship
    d.polygon([(x + w * 0.06, y + h * 0.62), (x + w * 0.94, y + h * 0.62),
               (x + w * 0.86, y + h * 0.78), (x + w * 0.14, y + h * 0.78)],
              fill=(70, 80, 92))
    d.rectangle([x + w * 0.30, y + h * 0.46, x + w * 0.52, y + h * 0.62],
                fill=(90, 100, 112))
    d.rectangle([x + w * 0.40, y + h * 0.36, x + w * 0.44, y + h * 0.46],
                fill=(90, 100, 112))
    # jet above
    d.polygon([(x + w * 0.14, y + h * 0.22), (x + w * 0.40, y + h * 0.22),
               (x + w * 0.34, y + h * 0.28), (x + w * 0.20, y + h * 0.28)],
              fill=(50, 58, 70))
    d.polygon([(x + w * 0.26, y + h * 0.22), (x + w * 0.30, y + h * 0.14),
               (x + w * 0.33, y + h * 0.22)], fill=(50, 58, 70))
    # sea
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=SEA)
    for i in range(3):
        wy = y + h * (0.84 + i * 0.06)
        d.line([(x + w * 0.08, wy), (x + w * 0.30, wy)], fill=(255, 255, 255),
               width=1)


def scene_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 220, 170))
    # pitch strip
    d.rectangle([x + w * 0.30, y + h * 0.15, x + w * 0.70, y + h],
                fill=(222, 200, 150))
    # stumps
    for i in range(3):
        sx = x + w * (0.44 + i * 0.05)
        d.rectangle([sx, y + h * 0.18, sx + 3, y + h * 0.34],
                    fill=(240, 200, 60))
    d.rectangle([x + w * 0.44, y + h * 0.16, x + w * 0.58, y + h * 0.18],
                fill=(240, 200, 60))
    # batsman silhouette
    d.ellipse([x + w * 0.48, y + h * 0.42, x + w * 0.56, y + h * 0.50],
              fill=(30, 40, 60))
    d.rectangle([x + w * 0.47, y + h * 0.50, x + w * 0.57, y + h * 0.72],
                fill=(30, 40, 60))
    d.rectangle([x + w * 0.47, y + h * 0.72, x + w * 0.51, y + h * 0.92],
                fill=(240, 240, 240))
    d.rectangle([x + w * 0.53, y + h * 0.72, x + w * 0.57, y + h * 0.92],
                fill=(30, 40, 60))
    # bat
    d.line([(x + w * 0.56, y + h * 0.52), (x + w * 0.68, y + h * 0.72)],
           fill=(150, 110, 60), width=4)
    # red ball
    d.ellipse([x + w * 0.72, y + h * 0.66, x + w * 0.78, y + h * 0.72],
              fill=RED)
    # score strip
    d.rectangle([x, y + h * 0.86, x + w, y + h], fill=INK)
    d.text((x + w * 0.06, y + h * 0.88), "77 / 1",
           font=SANS_B(max(9, h // 7)), fill=PAPER)


def scene_argentina(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 240))
    # central bank building
    d.rectangle([x + w * 0.16, y + h * 0.30, x + w * 0.84, y + h * 0.86],
                fill=(200, 208, 216))
    d.polygon([(x + w * 0.10, y + h * 0.30), (x + w * 0.50, y + h * 0.14),
               (x + w * 0.90, y + h * 0.30)], fill=(120, 130, 142))
    for i in range(3):
        cx = x + w * (0.26 + i * 0.20)
        d.rectangle([cx, y + h * 0.38, cx + w * 0.08, y + h * 0.80],
                    fill=(120, 130, 142))
    # banknote coming out of a press, crossed out
    d.rectangle([x + w * 0.60, y + h * 0.55, x + w * 0.92, y + h * 0.75],
                fill=(180, 220, 150), outline=INK)
    d.text((x + w * 0.70, y + h * 0.60), "$", font=SANS_B(max(10, h // 5)),
           fill=GREEN)
    d.line([(x + w * 0.58, y + h * 0.52), (x + w * 0.94, y + h * 0.78)],
           fill=RED, width=4)
    d.line([(x + w * 0.94, y + h * 0.52), (x + w * 0.58, y + h * 0.78)],
           fill=RED, width=4)


def scene_afp(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 34, 44))
    # monitor
    d.rectangle([x + w * 0.14, y + h * 0.16, x + w * 0.86, y + h * 0.66],
                fill=(200, 208, 216), outline=INK)
    d.rectangle([x + w * 0.42, y + h * 0.66, x + w * 0.58, y + h * 0.78],
                fill=(120, 128, 140))
    d.rectangle([x + w * 0.30, y + h * 0.78, x + w * 0.70, y + h * 0.84],
                fill=(120, 128, 140))
    # warning triangle on screen
    d.polygon([(x + w * 0.50, y + h * 0.24), (x + w * 0.66, y + h * 0.54),
               (x + w * 0.34, y + h * 0.54)], fill=GOLD, outline=INK)
    d.text((x + w * 0.475, y + h * 0.36), "!",
           font=SANS_B(max(12, h // 4)), fill=INK)
    # broken cable
    d.line([(x + w * 0.10, y + h * 0.92), (x + w * 0.44, y + h * 0.92)],
           fill=RED, width=2)
    d.line([(x + w * 0.56, y + h * 0.92), (x + w * 0.90, y + h * 0.92)],
           fill=RED, width=2)
    d.ellipse([x + w * 0.47, y + h * 0.88, x + w * 0.53, y + h * 0.96],
              fill=GOLD)


# ------------------------------------------------------------------ panels

PANELS = [
    # (scene, tag, headline, deck, large?)
    (scene_nz, "OCEANIA · POLITICS", "Luxon left one seat short",
     "NZ coalition wins 65 of 130 seats; the Opportunity Party now holds "
     "the balance.", True),
    (scene_storm, "AMERICAS · WEATHER", "Storm wrecks Thanksgiving travel",
     "About 400 flights cancelled and 724,000 homes left without power.",
     True),
    (scene_gaza, "MIDDLE EAST · CONFLICT", "Nine killed in Gaza strikes",
     "Deputy education minister among the dead on a third night of "
     "attacks.", True),
    (scene_kuwait, "MIDDLE EAST · CONFLICT",
     "Two Italians killed in Kuwait drone strike",
     "Iran denies any role in the attack.", False),
    (scene_eu, "EUROPE · POLITICS", "EU splits over $49bn Ukraine loan",
     "Leaders fail to agree on the budget after 12 hours of talks.",
     False),
    (scene_kyiv, "EUROPE · WAR", "Zelensky warns of new mass strike",
     "Says the US is too focused on the Middle East.", False),
    (scene_guinea, "AFRICA · POLITICS", "Junta delays election to 2028",
     "Vote due on 6 December pushed back two years.", False),
    (scene_mine, "ASIA · DISASTER", "Mine toll rises to 16",
     "Ten miners still missing in the flooded West Java shaft.", False),
    (scene_brazil, "AMERICAS · POLITICS", "Lula names banker finance chief",
     "Bradesco chairman Trabuco takes the ministry.", False),
    (scene_japan, "ASIA · DEFENCE", "Japan eyes $353bn defence plan",
     "Five-year spending below what the military sought.", False),
    (scene_cricket, "OCEANIA · SPORT", "NZ 77/1 at lunch in Christchurch",
     "Debutant Brar strikes on the last ball of the session.", False),
    (scene_argentina, "AMERICAS · ECONOMY", "Argentina bans money printing",
     "Central bank barred from funding the government.", False),
    (scene_afp, "GLOBAL · MEDIA", "Cyberattack hits news agency AFP",
     "Content platform shut down after the attack.", False),
]


def draw_panel(d, x, y, w, h, num, scene, tag, headline, deck, large):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    scene_h = 108 if large else 62
    scene(d, x + 1, y + 1, w - 2, scene_h)
    hline(d, x, x + w, y + scene_h + 1, 1)
    # number badge over the scene's top-left corner
    d.rectangle([x + 1, y + 1, x + 23, y + 19], fill=RED)
    d.text((x + 6, y + 3), str(num), font=SANS_B(11), fill=PAPER)
    tx = x + 6
    ty = y + scene_h + 6
    tag_size = 9 if large else 8
    d.text((tx, ty), tag, font=SANS_B(tag_size), fill=RED)
    ty += tag_size + 5
    hl_size = 15 if large else 12
    hl_lines = fit(wrap(headline, SANS_B(hl_size), w - 12), 2,
                   "headline %d" % num)
    for ln in hl_lines:
        d.text((tx, ty), ln, font=SANS_B(hl_size), fill=INK)
        ty += hl_size + 3
    dk_size = 12 if large else 11
    dk_lines = fit(wrap(deck, SANS(dk_size), w - 12), 2, "deck %d" % num)
    for ln in dk_lines:
        d.text((tx, ty), ln, font=SANS(dk_size), fill=INK_SOFT)
        ty += dk_size + 3
    assert ty <= y + h - 3, "panel %d overflows by %d" % (num, ty - y - h)


def draw_panels(d):
    # 3 large panels, y 214..426
    lx = [24, 354, 684]
    for i in range(3):
        scene, tag, hl, dk, large = PANELS[i]
        draw_panel(d, lx[i], 214, 316, 212, i + 1, scene, tag, hl, dk, large)
    # 10 small panels, two rows of five, y 434..586 and 592..744
    sx = [24, 220, 416, 612, 808]
    for row in range(2):
        for col in range(5):
            idx = 3 + row * 5 + col
            scene, tag, hl, dk, large = PANELS[idx]
            draw_panel(d, sx[col], 434 + row * 158, 191, 152, idx + 1,
                       scene, tag, hl, dk, large)


# --------------------------------------------------------------------- map

CONTINENTS = {
    "N America": [(-168, 66), (-140, 70), (-125, 72), (-110, 68),
                  (-95, 69), (-85, 66), (-80, 73), (-65, 60), (-55, 52),
                  (-60, 46), (-70, 42), (-75, 35), (-80, 32), (-85, 30),
                  (-90, 29), (-97, 26), (-105, 22), (-110, 24),
                  (-115, 30), (-120, 34), (-125, 40), (-125, 48),
                  (-135, 58), (-155, 58), (-165, 60)],
    "Greenland": [(-55, 60), (-45, 60), (-40, 64), (-30, 68), (-22, 70),
                  (-25, 76), (-40, 80), (-58, 76), (-60, 70)],
    "S America": [(-80, 9), (-75, 11), (-70, 12), (-62, 11), (-52, 5),
                  (-50, 0), (-44, -3), (-35, -8), (-40, -20), (-48, -27),
                  (-57, -38), (-65, -45), (-70, -52), (-73, -50),
                  (-73, -40), (-72, -30), (-70, -18), (-77, -12),
                  (-81, -5), (-80, 2)],
    "Europe": [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53),
               (8, 57), (10, 59), (5, 60), (12, 62), (18, 69), (25, 71),
               (30, 70), (40, 68), (45, 66), (40, 60), (35, 55), (30, 50),
               (28, 45), (23, 40), (19, 42), (12, 44), (8, 44), (3, 43),
               (0, 40), (-2, 37), (-6, 36)],
    "Africa": [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (32, 31),
               (35, 28), (38, 22), (43, 12), (48, 11), (51, 10), (44, 0),
               (40, -10), (35, -18), (32, -26), (28, -33), (20, -35),
               (15, -30), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8),
               (-17, 15), (-16, 20), (-15, 27), (-10, 31)],
    "Asia": [(30, 70), (40, 68), (55, 68), (70, 72), (90, 75), (110, 76),
             (130, 72), (150, 70), (170, 66), (178, 65), (170, 60),
             (162, 56), (158, 52), (142, 50), (140, 45), (135, 43),
             (130, 38), (127, 35), (122, 38), (120, 32), (115, 28),
             (110, 22), (108, 18), (105, 10), (100, 8), (98, 12),
             (95, 16), (92, 21), (88, 22), (85, 19), (80, 15), (77, 8),
             (75, 12), (72, 20), (68, 23), (62, 25), (57, 26), (54, 27),
             (50, 29), (48, 30), (44, 29), (40, 32), (36, 36), (35, 36),
             (30, 41), (28, 41), (26, 38), (23, 36)],
    "Australia": [(113, -22), (114, -30), (115, -35), (120, -34),
                  (129, -32), (132, -32), (135, -35), (138, -35),
                  (140, -38), (145, -38), (150, -37), (153, -32),
                  (153, -27), (150, -22), (146, -19), (142, -15),
                  (142, -11), (136, -12), (132, -11), (130, -13),
                  (126, -14), (122, -17), (118, -20)],
    "UK": [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
           (1, 51)],
    "Japan": [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37),
              (140, 39), (141, 41), (143, 42), (145, 44), (143, 45),
              (141, 43), (140, 40), (139, 38), (137, 36), (135, 33),
              (131, 32)],
    "NZ": [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
           (175, -40), (173, -42), (170, -44), (167, -46)],
}

# (panel number, lon, lat, label dx, label dy) — label offsets in px
PINS = [
    (1, 174.8, -41.3, -38, -22),
    (2, -74.0, 40.7, -30, -12),
    (3, 34.5, 31.5, 12, -14),
    (4, 48.0, 29.4, 12, 4),
    (5, 4.4, 50.8, -30, 6),
    (6, 30.5, 50.4, 10, -16),
    (7, -15.6, 11.9, -28, -16),
    (8, 106.8, -6.6, 10, 6),
    (9, -47.9, -15.8, 14, -18),
    (10, 139.7, 35.7, 10, -14),
    (11, 172.6, -43.5, 6, -20),
    (12, -58.4, -34.6, -30, 4),
    (13, 2.35, 48.85, -32, -14),
]

MAP_X, MAP_Y, MAP_W, MAP_H = 24, 752, 340, 122


def project(lon, lat):
    px = MAP_X + (lon + 180) / 360 * MAP_W
    py = MAP_Y + (75 - lat) / 135 * MAP_H
    return px, py


def draw_map(d):
    d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H],
                outline=INK, width=1, fill=(232, 238, 240))
    for pts in CONTINENTS.values():
        d.polygon([project(lon, lat) for lon, lat in pts],
                  fill=(176, 188, 160), outline=(107, 122, 94))
    d.text((MAP_X + 6, MAP_Y + 4), "WHERE IT HAPPENED",
           font=SANS_B(9), fill=INK_SOFT)
    for num, lon, lat, dx, dy in PINS:
        px, py = project(lon, lat)
        dia = 16 if num >= 10 else 14
        lx, ly = px + dx, py + dy
        lx = min(max(lx, MAP_X + 2), MAP_X + MAP_W - dia - 2)
        ly = min(max(ly, MAP_Y + 2), MAP_Y + MAP_H - dia - 2)
        d.line([(px, py), (lx + dia // 2, ly + dia // 2)], fill=INK, width=1)
        d.ellipse([lx, ly, lx + dia, ly + dia], fill=RED, outline=PAPER)
        tsize = 8 if num >= 10 else 9
        d.text((lx + (4 if num < 10 else 2), ly + 2), str(num),
               font=SANS_B(tsize), fill=PAPER)


# ------------------------------------------------------- index + date check

INDEX = [
    (14, "Trump urges Putin to pull back; G20 invite open"),
    (15, "Trump demands probe of 'fake' GDP figures"),
    (16, "US approves F-16 maintenance sale to Ukraine"),
    (17, "Ukraine intel: N. Korea paused aid to Russia"),
    (18, "Ukraine strikes Russian oil sites overnight"),
    (19, "Ukraine, Russia swap fallen soldiers' remains"),
    (20, "Iran reports blasts on three Hormuz tankers"),
    (21, "Saudis down missiles aimed at Riyadh anew"),
    (22, "Thousands protest in Irbil over Kurdish oil"),
    (23, "Myanmar defies parts of ICJ ruling"),
    (24, "Hong Kong marks deadly fire anniversary"),
    (25, "Wildfires raze homes on Australian island"),
    (26, "Duterte ICC trial set to start"),
    (27, "Delhi police free 164 from cyber-slavery ring"),
    (28, "Tokyo core inflation 2.9% in November"),
    (29, "Black Friday: cautious US shoppers"),
    (30, "Brent near $97 as Gulf attacks hit supply"),
]

DATE_CHECK = [
    "Trump's tariffs on 14 partners — 26 Nov",
    "Macy's parade postponed — 26 Nov",
    "Nigeria clash toll reaches 74 — 26 Nov",
    "Kenya cult leader convicted — 25 Nov",
]


def draw_bottom(d):
    draw_map(d)
    # DATE CHECK box under the map
    bx, by, bw, bh = 24, 886, 340, 94
    d.rectangle([bx, by, bx + bw, by + bh], outline=RED, width=2)
    d.rectangle([bx, by, bx + bw, by + 20], fill=RED)
    d.text((bx + 8, by + 4), "DATE CHECK — NOT TODAY'S NEWS",
           font=SANS_B(11), fill=PAPER)
    ly = by + 26
    for line in DATE_CHECK:
        assert SANS(11).getlength(line) <= bw - 16, line
        d.text((bx + 8, ly), line, font=SANS(11), fill=INK)
        ly += 17
    # index, two columns
    ix = 380
    d.text((ix, 752), "ALSO TODAY — 17 MORE STORIES",
           font=SANS_B(12), fill=RED)
    hline(d, ix, 1000, 770, 1)
    col_w = 306
    for i, (num, text) in enumerate(INDEX):
        col = i // 9
        row = i % 9
        x = ix + col * (col_w + 8)
        y = 780 + row * 22
        item = "%d. %s" % (num, text)
        assert SANS(11).getlength(item) <= col_w, item
        d.text((x, y), item, font=SANS(11), fill=INK)


def draw_footer(d):
    hline(d, 24, 1000, 992, 2)
    centred(d, 1000,
            "Drawn in code · No photographs · All 30 stories verified "
            "against reporting dated 27 November 2026",
            SANS(10), fill=INK_SOFT)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_number_strip(d)
    draw_region_bar(d)
    draw_panels(d)
    draw_bottom(d)
    draw_footer(d)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry", "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
