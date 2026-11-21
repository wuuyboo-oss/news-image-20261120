#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page as a 1024x1024 RGB PNG.

Fresh, from-scratch re-authoring for the news-image-20261120 bounty.
Layout (from the brief): masthead on top, one lead story, a 2x2 grid of
four stories, and a business strip along the bottom. Drawn with PIL and
Liberation fonts only; no network, no AI imagery. Deterministic: running
this script twice produces byte-identical output.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "LiberationSerif-Bold.ttf"
SERIF_REG = "LiberationSerif-Regular.ttf"
SANS = "LiberationSans-Regular.ttf"
SANS_BOLD = "LiberationSans-Bold.ttf"

# Palette: newsprint paper, near-black ink, one red accent, one navy band.
PAPER = (253, 251, 245)
INK = (18, 18, 18)
GREY = (105, 105, 100)
RULE = (40, 40, 40)
RED = (178, 34, 34)
NAVY = (19, 32, 56)
GOLD = (212, 175, 55)
LIGHT_LINE = (190, 185, 175)

MARGIN = 40
CONTENT_W = W - 2 * MARGIN


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, y, x0, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons
# All icons are simple dark-ink line drawings made from primitives.


def icon_summit(draw, x, y, s):
    """Shenzhen skyline: three towers with flags, a sun, ground line."""
    draw.line([(x, y + s), (x + s, y + s)], fill=INK, width=3)
    towers = [(0.05, 0.55, 0.18), (0.30, 0.30, 0.16), (0.55, 0.42, 0.18),
              (0.78, 0.60, 0.16)]
    for fx, fy, fw in towers:
        bx, by = x + fx * s, y + fy * s
        bw = fw * s
        draw.rectangle([bx, by, bx + bw, y + s], outline=INK, width=2)
        draw.line([(bx + bw / 2, by), (bx + bw / 2, by - 0.16 * s)],
                  fill=INK, width=2)
        draw.polygon([(bx + bw / 2, by - 0.16 * s),
                      (bx + bw / 2 + 0.14 * s, by - 0.11 * s),
                      (bx + bw / 2, by - 0.06 * s)], fill=RED)
    draw.ellipse([x + 0.72 * s, y + 0.02 * s, x + 0.92 * s, y + 0.22 * s],
                 outline=INK, width=2)


def icon_scales(draw, x, y, s):
    """Scales of justice: post, beam, two hanging pans."""
    cx = x + s / 2
    draw.line([(cx, y + 0.08 * s), (cx, y + 0.92 * s)], fill=INK, width=3)
    draw.line([(x + 0.08 * s, y + 0.22 * s), (x + 0.92 * s, y + 0.22 * s)],
              fill=INK, width=3)
    draw.ellipse([cx - 0.05 * s, y + 0.02 * s, cx + 0.05 * s, y + 0.12 * s],
                 outline=INK, width=2)
    for side in (-1, 1):
        px = cx + side * 0.36 * s
        draw.line([(cx + side * 0.42 * s, y + 0.22 * s),
                   (px, y + 0.55 * s)], fill=INK, width=2)
        draw.line([(cx + side * 0.30 * s, y + 0.22 * s),
                   (px, y + 0.55 * s)], fill=INK, width=2)
        draw.arc([px - 0.16 * s, y + 0.50 * s, px + 0.16 * s, y + 0.78 * s],
                 0, 180, fill=INK, width=2)
    draw.line([(x + 0.28 * s, y + 0.92 * s), (x + 0.72 * s, y + 0.92 * s)],
              fill=INK, width=3)


def icon_tanker(draw, x, y, s):
    """Oil tanker on waves: hull, deck boxes, funnel, sea lines."""
    draw.polygon([(x + 0.04 * s, y + 0.55 * s), (x + 0.96 * s, y + 0.55 * s),
                  (x + 0.88 * s, y + 0.78 * s), (x + 0.12 * s, y + 0.78 * s)],
                 outline=INK, width=2)
    draw.rectangle([x + 0.14 * s, y + 0.38 * s, x + 0.34 * s, y + 0.55 * s],
                   outline=INK, width=2)
    draw.rectangle([x + 0.38 * s, y + 0.30 * s, x + 0.58 * s, y + 0.55 * s],
                   outline=INK, width=2)
    draw.rectangle([x + 0.70 * s, y + 0.28 * s, x + 0.84 * s, y + 0.55 * s],
                   fill=RED)
    for i, yy in enumerate((0.86, 0.94)):
        wave_y = y + yy * s
        draw.arc([x + 0.05 * s, wave_y, x + 0.35 * s, wave_y + 0.10 * s],
                 180, 360, fill=INK, width=2)
        draw.arc([x + 0.38 * s, wave_y, x + 0.68 * s, wave_y + 0.10 * s],
                 180, 360, fill=INK, width=2)
        draw.arc([x + 0.70 * s, wave_y, x + 0.97 * s, wave_y + 0.10 * s],
                 180, 360, fill=INK, width=2)


def icon_bridge(draw, x, y, s):
    """Suspension bridge: deck, two towers, main cable, hangers."""
    draw.line([(x, y + 0.72 * s), (x + s, y + 0.72 * s)], fill=INK, width=3)
    for tx in (0.22, 0.72):
        bx = x + tx * s
        draw.line([(bx, y + 0.18 * s), (bx, y + 0.72 * s)], fill=INK, width=3)
        draw.line([(bx - 0.05 * s, y + 0.18 * s), (bx + 0.05 * s, y + 0.18 * s)],
                  fill=INK, width=3)
    # main cable: sagging arc between towers, dipping below the deck line
    draw.arc([x + 0.05 * s, y - 0.05 * s, x + 0.95 * s, y + 1.05 * s],
             20, 160, fill=INK, width=2)
    for hx in (0.30, 0.38, 0.47, 0.55, 0.63):
        draw.line([(x + hx * s, y + 0.42 * s), (x + hx * s, y + 0.72 * s)],
                  fill=INK, width=1)
    draw.line([(x + 0.05 * s, y + 0.86 * s), (x + 0.95 * s, y + 0.86 * s)],
              fill=INK, width=2)
    draw.line([(x + 0.05 * s, y + 0.94 * s), (x + 0.95 * s, y + 0.94 * s)],
              fill=INK, width=2)


def icon_storm(draw, x, y, s):
    """Cyclone: spiral cloud arcs above slanted rain strokes."""
    cx, cy = x + s / 2, y + 0.38 * s
    for r, start, end in ((0.42, 200, 20), (0.30, 160, 340), (0.18, 120, 300)):
        draw.arc([cx - r * s, cy - r * s * 0.7, cx + r * s, cy + r * s * 0.7],
                 start, end, fill=INK, width=3)
    for i in range(5):
        rx = x + (0.12 + i * 0.18) * s
        draw.line([(rx, y + 0.72 * s), (rx - 0.06 * s, y + 0.92 * s)],
                  fill=RED if i % 2 else INK, width=3)


def icon_chart(draw, x, y, s):
    """Rising market chart: axes, stepped line, arrowhead."""
    draw.line([(x, y + 0.85 * s), (x + s, y + 0.85 * s)], fill=GOLD, width=3)
    draw.line([(x, y + 0.85 * s), (x, y + 0.05 * s)], fill=GOLD, width=3)
    pts = [(0.08, 0.70), (0.28, 0.62), (0.42, 0.66), (0.58, 0.42),
           (0.72, 0.46), (0.92, 0.12)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        draw.line([(x + ax * s, y + ay * s), (x + bx * s, y + by * s)],
                  fill=GOLD, width=3)
    ex, ey = x + 0.92 * s, y + 0.12 * s
    draw.polygon([(ex, ey), (ex - 0.14 * s, ey + 0.02 * s),
                  (ex - 0.02 * s, ey + 0.14 * s)], fill=GOLD)


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    title_f = font(SERIF, 72)
    d.text((W / 2, 30), "THE WORLD TODAY", font=title_f, fill=INK,
           anchor="ma")
    date_f = font(SANS_BOLD, 22)
    d.text((W / 2, 118), "FRIDAY, 20 NOVEMBER 2026", font=date_f, fill=RED,
           anchor="ma")
    hrule(d, 152, MARGIN, W - MARGIN, 3)
    hrule(d, 158, MARGIN, W - MARGIN, 1)

    # ---- Lead story -----------------------------------------------------
    ly = 178
    kick_f = font(SANS_BOLD, 19)
    d.text((MARGIN, ly), "LEAD  •  SUMMIT IN SHENZHEN", font=kick_f, fill=RED)
    head_f = font(SERIF, 40)
    head = ("Trump, Xi and Putin hold first-ever "
            "three-way summit in Shenzhen")
    head_lines = wrap(d, head, head_f, 610)
    hy = draw_lines(d, head_lines, head_f, MARGIN, ly + 30, INK, 48)
    deck_f = font(SANS, 21)
    deck = ("The three leaders release a peace declaration on the "
            "APEC sidelines; nuclear arms control is on the agenda.")
    deck_lines = wrap(d, deck, deck_f, 610)
    draw_lines(d, deck_lines, deck_f, MARGIN, hy + 8, GREY, 28)
    icon_summit(d, 700, ly + 22, 210)
    hrule(d, 420, MARGIN, W - MARGIN, 2)

    # ---- 2x2 story grid -------------------------------------------------
    grid_top = 440
    col_w = (CONTENT_W - 28) // 2
    row_h = 196
    stories = [
        ("WORLD COURT", RED,
         "ICJ rules Myanmar committed genocide against the Rohingya",
         "The World Court finds Myanmar committed genocide against the "
         "Rohingya people. The ruling cannot be appealed.",
         icon_scales),
        ("GULF", RED,
         "Iran widens attacks on Gulf states and tankers",
         "Tehran widens its attacks on Gulf states and oil tankers. The "
         "IEA calls it the biggest energy security threat in history.",
         icon_tanker),
        ("UKRAINE", RED,
         "Crimean Bridge attacked a third time this week",
         "The Crimean Bridge is hit again, the third attack this week. "
         "Russian strikes damage the Austrian and Dutch embassies in Kyiv.",
         icon_bridge),
        ("WEATHER", RED,
         "Cyclone Akvan nears India's east coast",
         "Cyclone Akvan closes in, with landfall expected on 20 November. "
         "Odisha shuts schools and evacuates coastal areas.",
         icon_storm),
    ]
    for i, (kicker, color, headline, body, icon) in enumerate(stories):
        cx = MARGIN + (i % 2) * (col_w + 28)
        cy = grid_top + (i // 2) * (row_h + 14)
        d.text((cx, cy), kicker, font=kick_f, fill=color)
        icon(d, cx + col_w - 62, cy - 4, 58)
        sh_f = font(SERIF, 25)
        s_lines = wrap(d, headline, sh_f, col_w - 70)
        by = draw_lines(d, s_lines, sh_f, cx, cy + 28, INK, 31)
        body_f = font(SANS, 18)
        b_lines = wrap(d, body, body_f, col_w)
        draw_lines(d, b_lines, body_f, cx, by + 6, GREY, 24)
        if i % 2 == 0:
            d.line([(cx + col_w + 14, cy), (cx + col_w + 14, cy + row_h - 8)],
                   fill=LIGHT_LINE, width=1)
        if i < 2:
            hrule(d, cy + row_h + 2, cx, cx + col_w, 1, LIGHT_LINE)

    grid_bottom = grid_top + 2 * row_h + 14

    # ---- Business strip -------------------------------------------------
    strip_y = grid_bottom + 18
    strip_h = H - strip_y - 34
    d.rectangle([MARGIN, strip_y, W - MARGIN, strip_y + strip_h], fill=NAVY)
    d.text((MARGIN + 24, strip_y + 16), "BUSINESS", font=kick_f, fill=GOLD)
    icon_chart(d, W - MARGIN - 108, strip_y + 18, 84)
    bh_f = font(SERIF, 30)
    d.text((MARGIN + 24, strip_y + 48),
           "Anthropic's valuation reportedly reaches $1.5 trillion",
           font=bh_f, fill=(255, 255, 255))
    bb_f = font(SANS, 19)
    d.text((MARGIN + 24, strip_y + 92),
           "The AI lab's valuation reportedly climbs to $1.5 trillion.",
           font=bb_f, fill=(205, 210, 220))

    # ---- Footer ---------------------------------------------------------
    foot_f = font(SANS, 14)
    d.text((W / 2, H - 26), "THE WORLD TODAY  •  FRIDAY, 20 NOVEMBER 2026",
           font=foot_f, fill=GREY, anchor="ma")

    img.save(OUT, format="PNG")
    return OUT


if __name__ == "__main__":
    print(build())
