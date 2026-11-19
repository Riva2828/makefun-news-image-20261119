#!/usr/bin/env python3
"""Render the news-image-20261119 front page: 1024x1024, PIL only, deterministic.
Newspaper front page for Thursday 19 November 2026.
Stories verified from BBC / Al Jazeera / NDTV / The Hindu BusinessLine / JagranJosh
on 19 Nov 2026 (see buildlog for sources).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 86, 78)
RULE = (18, 18, 18)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return draw.textbbox((0, 0), text, font=fnt)[3]


def gradient(draw, box, stops):
    """Vertical gradient through color stops (deterministic)."""
    x0, y0, x1, y1 = box
    n = y1 - y0
    for i in range(n):
        t = i / max(1, n - 1) * (len(stops) - 1)
        k = int(t)
        f = t - k
        if k >= len(stops) - 1:
            c = stops[-1]
        else:
            c = tuple(int(stops[k][j] + (stops[k + 1][j] - stops[k][j]) * f) for j in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 44  # margin

    # ---- Masthead ----
    f_mast = font(SERIF_B, 74)
    draw_centered(d, W // 2, 22, "THE WORLD TODAY", f_mast, INK)
    d.line([(M, 116), (W - M, 116)], fill=RULE, width=4)
    d.line([(M, 124), (W - M, 124)], fill=RULE, width=1)

    # ---- Dateline bar ----
    f_date = font(SANS_B, 21)
    d.text((M, 134), "THURSDAY, 19 NOVEMBER 2026", font=f_date, fill=RED)
    right = "THE DAY IN ONE PAGE"
    rw = d.textlength(right, font=f_date)
    d.text((W - M - rw, 134), right, font=f_date, fill=INK)

    # ---- Hero band: Vice City sunset (GTA VI launch) ----
    hx0, hy0, hx1, hy1 = M, 166, W - M, 440
    gradient(d, (hx0, hy0, hx1, hy1), [
        (36, 22, 64), (94, 38, 94), (184, 59, 94), (232, 131, 58), (249, 217, 118),
    ])
    # sun
    d.ellipse([(742, 236), (862, 356)], fill=(255, 240, 180))
    # birds
    for bx, by in [(180, 210), (240, 196), (300, 226), (640, 200)]:
        d.line([(bx, by), (bx + 9, by - 6), (bx + 18, by)], fill=(30, 12, 40), width=3)
    # skyline silhouette
    SKY = (26, 12, 40)
    buildings = [(M, 96, 92), (M + 96, 148, 66), (M + 166, 118, 84), (M + 254, 168, 58),
                 (M + 316, 128, 92), (M + 412, 158, 62), (M + 478, 108, 88),
                 (M + 570, 150, 70), (M + 644, 122, 80), (M + 728, 160, 60),
                 (M + 792, 116, 86), (M + 882, 146, 54)]
    base = hy1 - 34
    for bx, bw, bh in buildings:
        d.rectangle([(bx, base - bh), (bx + bw - 6, base)], fill=SKY)
    # lit windows (deterministic grid)
    for i, (bx, bw, bh) in enumerate(buildings):
        for wy in range(base - bh + 12, base - 8, 18):
            for wx in range(bx + 8, bx + bw - 14, 16):
                if (wx * 7 + wy * 13 + i * 5) % 3 == 0:
                    d.rectangle([(wx, wy), (wx + 5, wy + 7)], fill=(255, 214, 120))
    # ocean strip
    d.rectangle([(hx0, base), (hx1, hy1)], fill=(24, 52, 84))
    for yy in (base + 10, base + 20, base + 29):
        d.line([(hx0 + 14, yy), (hx1 - 14, yy)], fill=(120, 170, 210), width=2)
    # palm silhouettes (two, left and right)
    for px, s in [(110, 1.0), (905, 0.85)]:
        top_y = hy1 - 34 - int(120 * s)
        # trunk: segmented curve
        pts = []
        for k in range(9):
            t = k / 8
            pts.append((px + int(18 * s * t * t), hy1 - 34 - int(120 * s * t)))
        d.line(pts, fill=SKY, width=int(9 * s))
        cx, cy = pts[-1]
        # fronds
        for ang in (-155, -125, -95, -62, -28):
            import math
            r = int(46 * s)
            ex = cx + int(r * math.cos(math.radians(ang)))
            ey = cy + int(r * math.sin(math.radians(ang)) * 0.55) + int(8 * s)
            mx = cx + int(r * 0.55 * math.cos(math.radians(ang)))
            my = cy + int(r * 0.55 * math.sin(math.radians(ang)) * 0.55) - int(4 * s)
            d.line([(cx, cy), (mx, my), (ex, ey)], fill=SKY, width=int(5 * s))
    # hero frame
    d.rectangle([(hx0, hy0), (hx1, hy1)], outline=INK, width=2)
    # red tag on hero
    tag = "LAUNCH DAY"
    f_tag = font(SANS_B, 20)
    tw = d.textlength(tag, font=f_tag) + 24
    d.rectangle([(hx0, hy0), (hx0 + tw, hy0 + 34)], fill=RED)
    d.text((hx0 + 12, hy0 + 5), tag, font=f_tag, fill=(255, 255, 255))

    # ---- Main headline ----
    f_kick = font(SANS_B, 19)
    d.text((M, 456), "GAMES  •  ROCKSTAR  •  VICE CITY", font=f_kick, fill=RED)
    f_head = font(SERIF_B, 82)
    draw_centered(d, W // 2, 482, "GTA VI IS HERE", f_head, INK)
    f_stand = font(SANS, 22)
    stand = "After a 13-year wait, Rockstar's return to Vice City launches worldwide today \u2014 fans celebrate from Miami to Dublin."
    lines = wrap(d, stand, f_stand, W - 2 * M - 60)
    y = 578
    for ln in lines:
        draw_centered(d, W // 2, y, ln, f_stand, INK)
        y += 30

    d.line([(M, 650), (W - M, 650)], fill=RULE, width=2)

    # ---- Secondary stories: 2 cols x 3 rows ----
    stories = [
        ("SUMMIT", "Trump, Xi and Putin to meet at APEC in China",
         "Trump lands in Shenzhen for trilateral talks."),
        ("POLITICS", "Jeffries poised to be first Black Speaker",
         "Democrats nominate Jeffries to lead the House."),
        ("TECH", "Anthropic's $81.3bn IPO \u2014 biggest ever",
         "AI lab's Nasdaq debut sets an all-time record."),
        ("SCIENCE", "Voyager 1 reaches one light-day",
         "NASA's probe is the farthest human object ever."),
        ("LAW", "ICJ to rule on Rohingya case",
         "World court judges Myanmar genocide claims."),
        ("EUROPE", "EU proposes \u20ac45bn loan for Ukraine",
         "Repaid from Russian assets after the war."),
    ]
    f_k = font(SANS_B, 16)
    f_h = font(SANS_B, 25)
    f_s = font(SANS, 17)
    col_w = (W - 2 * M - 28) // 2
    row_h = 106
    for i, (kick, head, summ) in enumerate(stories):
        col = i % 2
        row = i // 2
        x = M + col * (col_w + 28)
        y0 = 668 + row * row_h
        d.text((x, y0), kick, font=f_k, fill=RED)
        hl = wrap(d, head, f_h, col_w)
        assert len(hl) <= 2, f"headline too long: {head}"
        yy = y0 + 22
        for ln in hl[:2]:
            d.text((x, yy), ln, font=f_h, fill=INK)
            yy += 29
        sl = wrap(d, summ, f_s, col_w)
        assert len(sl) == 1, f"summary too long: {summ}"
        d.text((x, yy), sl[0], font=f_s, fill=GREY)
        if col == 0:
            d.line([(x + col_w + 14, y0 + 4), (x + col_w + 14, y0 + 96)], fill=(200, 192, 176), width=1)
        if row < 2:
            d.line([(x, y0 + 101), (x + col_w, y0 + 101)], fill=(200, 192, 176), width=1)

    # ---- Footer ----
    d.line([(M, 992), (W - M, 992)], fill=RULE, width=1)
    f_f = font(SANS, 14)
    foot = "Compiled 19 Nov 2026 from BBC  \u2022  Al Jazeera  \u2022  NDTV  \u2022  The Hindu BusinessLine  \u2022  JagranJosh"
    draw_centered(d, W // 2, 998, foot, f_f, GREY)

    img.save("/home/hatch/workspace/makefun/news-image-20261119/image.png", optimize=True)
    print("saved image.png", img.size)


if __name__ == "__main__":
    main()
