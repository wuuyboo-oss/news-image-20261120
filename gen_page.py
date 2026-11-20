#!/usr/bin/env python3
"""Draw the 1024x1024 newspaper front page for 20 November 2026.

Run: python3 gen_page.py  -> writes entry.png next to this script.
All text is drawn with PIL + Liberation fonts; no network, no AI images.
Layout mirrors the 18/19 November entries (same masthead, lead + 2x2 grid +
bottom strip), which passed all make.fun intake checks.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width = 952

PAPER = (248, 244, 234)
INK = (26, 26, 26)
RED = (163, 22, 33)
BLUE = (29, 78, 137)
GREY = (90, 86, 76)
RULE = (26, 26, 26)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
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


def draw_icon(d, kind, x, y, s, color):
    """Small line icon inside an s x s box at (x, y)."""
    if kind == "globe":
        d.ellipse([x, y, x + s, y + s], outline=color, width=3)
        d.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=color, width=2)
        d.line([x, y + s / 2, x + s, y + s / 2], fill=color, width=2)
        d.arc([x, y + s * 0.18, x + s, y + s * 0.82], 200, 340, fill=color, width=2)
        d.arc([x, y + s * 0.18, x + s, y + s * 0.82], 20, 160, fill=color, width=2)
    elif kind == "drone":
        for cx, cy in ((0.2, 0.25), (0.8, 0.25), (0.2, 0.75), (0.8, 0.75)):
            d.ellipse([x + s * cx - 7, y + s * cy - 7, x + s * cx + 7, y + s * cy + 7],
                      outline=color, width=2)
        d.line([x + s * 0.2, y + s * 0.25, x + s * 0.8, y + s * 0.75], fill=color, width=2)
        d.line([x + s * 0.8, y + s * 0.25, x + s * 0.2, y + s * 0.75], fill=color, width=2)
        d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62], fill=color)
    elif kind == "rocket":
        d.polygon([(x + s * 0.5, y + s * 0.05), (x + s * 0.72, y + s * 0.55),
                   (x + s * 0.28, y + s * 0.55)], fill=color)
        d.ellipse([x + s * 0.42, y + s * 0.28, x + s * 0.58, y + s * 0.44],
                  fill=PAPER, outline=color, width=2)
        d.polygon([(x + s * 0.28, y + s * 0.5), (x + s * 0.12, y + s * 0.85),
                   (x + s * 0.32, y + s * 0.72)], fill=color)
        d.polygon([(x + s * 0.72, y + s * 0.5), (x + s * 0.88, y + s * 0.85),
                   (x + s * 0.68, y + s * 0.72)], fill=color)
        d.polygon([(x + s * 0.42, y + s * 0.62), (x + s * 0.5, y + s * 0.95),
                   (x + s * 0.58, y + s * 0.62)], fill=color)
    elif kind == "gamepad":
        d.rounded_rectangle([x + s * 0.05, y + s * 0.25, x + s * 0.95, y + s * 0.75],
                            radius=12, outline=color, width=3)
        d.line([x + s * 0.2, y + s * 0.5, x + s * 0.38, y + s * 0.5], fill=color, width=3)
        d.line([x + s * 0.29, y + s * 0.41, x + s * 0.29, y + s * 0.59], fill=color, width=3)
        d.ellipse([x + s * 0.62, y + s * 0.42, x + s * 0.70, y + s * 0.50], fill=color)
        d.ellipse([x + s * 0.74, y + s * 0.54, x + s * 0.82, y + s * 0.62], fill=color)
    elif kind == "bridge":
        d.line([x + s * 0.1, y + s * 0.75, x + s * 0.9, y + s * 0.75], fill=color, width=3)
        d.line([x + s * 0.18, y + s * 0.75, x + s * 0.18, y + s * 0.3], fill=color, width=3)
        d.line([x + s * 0.82, y + s * 0.75, x + s * 0.82, y + s * 0.3], fill=color, width=3)
        d.arc([x + s * 0.18, y + s * 0.05, x + s * 0.82, y + s * 0.75], 180, 360, fill=color, width=3)
    elif kind == "storm":
        d.ellipse([x + s * 0.15, y + s * 0.1, x + s * 0.55, y + s * 0.45], outline=color, width=3)
        d.ellipse([x + s * 0.45, y + s * 0.2, x + s * 0.85, y + s * 0.55], outline=color, width=3)
        for cx in (0.3, 0.5, 0.7):
            d.line([x + s * cx, y + s * 0.62, x + s * (cx - 0.08), y + s * 0.9], fill=color, width=3)
    elif kind == "trade":
        d.line([x + s * 0.1, y + s * 0.35, x + s * 0.75, y + s * 0.35], fill=color, width=3)
        d.polygon([(x + s * 0.75, y + s * 0.2), (x + s * 0.95, y + s * 0.35),
                   (x + s * 0.75, y + s * 0.5)], fill=color)
        d.line([x + s * 0.9, y + s * 0.65, x + s * 0.25, y + s * 0.65], fill=color, width=3)
        d.polygon([(x + s * 0.25, y + s * 0.5), (x + s * 0.05, y + s * 0.65),
                   (x + s * 0.25, y + s * 0.8)], fill=color)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    mast = font(SERIF_B, 96)
    d.text((W / 2, 24), "THE WORLD", font=mast, fill=INK, anchor="ma")
    date_f = font(SANS_B, 21)
    d.text((W / 2, 128), "FRIDAY  20  NOVEMBER  2026", font=date_f, fill=INK, anchor="ma")
    d.line([M, 160, W - M, 160], fill=RULE, width=3)
    d.line([M, 165, W - M, 165], fill=RULE, width=1)
    tag_f = font(SERIF_I, 20)
    d.text((W / 2, 172), "Six stories from one day around the world",
           font=tag_f, fill=GREY, anchor="ma")

    # ---------- lead story (full width) ----------
    y = 206
    kick_f = font(SANS_B, 18)
    head_f = font(SERIF_B, 46)
    sum_f = font(SANS, 21)
    d.text((M, y), "SUMMIT  ·  SHENZHEN", font=kick_f, fill=RED)
    y += 30
    lead_head = "Trump, Xi and Putin hold first-ever three-way summit"
    for line in wrap(d, lead_head, head_f, CW):
        d.text((M, y), line, font=head_f, fill=INK)
        y += 54
    y += 4
    lead_sum = ("The three leaders meet in Shenzhen on the APEC sidelines and release "
                "a peace declaration, with nuclear arms control on the agenda.")
    for line in wrap(d, lead_sum, sum_f, CW):
        d.text((M, y), line, font=sum_f, fill=INK)
        y += 28
    y += 10
    d.line([M, y, W - M, y], fill=RULE, width=2)
    y += 14

    # ---------- grid stories ----------
    stories = [
        ("WORLD COURT", "ICJ rules Myanmar committed genocide",
         "The UN court finds Myanmar committed genocide against the Rohingya; the ruling cannot be appealed.",
         "globe", BLUE),
        ("GULF", "Iran widens attacks on Gulf states",
         "Tehran strikes Gulf targets and tankers as the IEA calls it the biggest energy threat in history.",
         "drone", RED),
        ("UKRAINE", "Crimean Bridge hit a third time",
         "Kyiv strikes the bridge again as Russian missiles damage two embassies in the capital.",
         "bridge", RED),
        ("WEATHER  ·  INDIA", "Cyclone Akvan nears east coast",
         "Odisha shuts schools and evacuates coastal areas as the storm approaches landfall.",
         "storm", BLUE),
    ]
    col_w = (CW - 20) // 2
    grid_head = font(SERIF_B, 31)
    grid_sum = font(SANS, 19)
    grid_kick = font(SANS_B, 16)
    row_h = 196
    for i, (kick, head, summ, icon, color) in enumerate(stories):
        col = i % 2
        row = i // 2
        x0 = M + col * (col_w + 20)
        y0 = y + row * row_h
        if col == 1:
            d.line([M + col_w + 10, y0 + 4, M + col_w + 10, y0 + row_h - 18], fill=(200, 192, 172), width=1)
        draw_icon(d, icon, x0, y0, 40, color)
        d.text((x0 + 50, y0 + 8), kick, font=grid_kick, fill=color)
        hy = y0 + 46
        for line in wrap(d, head, grid_head, col_w):
            d.text((x0, hy), line, font=grid_head, fill=INK)
            hy += 37
        hy += 4
        for line in wrap(d, summ, grid_sum, col_w):
            d.text((x0, hy), line, font=grid_sum, fill=INK)
            hy += 25
    y = y + 2 * row_h
    d.line([M, y, W - M, y], fill=RULE, width=2)
    y += 12

    # ---------- business strip (full width) ----------
    draw_icon(d, "trade", M, y + 6, 64, BLUE)
    d.text((M + 80, y), "BUSINESS", font=grid_kick, fill=BLUE)
    w_head = font(SERIF_B, 33)
    d.text((M + 80, y + 24), "Anthropic valuation reportedly $1.5 trillion",
           font=w_head, fill=INK)
    d.text((M + 80, y + 66),
           "The AI lab's reported valuation underlines the surge of global interest in AI.",
           font=grid_sum, fill=INK)
    y += 108
    d.line([M, y, W - M, y], fill=RULE, width=3)
    d.line([M, y + 5, W - M, y + 5], fill=RULE, width=1)

    # ---------- footer ----------
    foot_f = font(SANS, 15)
    d.text((W / 2, y + 14),
           "THE WORLD  ·  Friday 20 November 2026  ·  Compiled from reports published on 20 November 2026",
           font=foot_f, fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
