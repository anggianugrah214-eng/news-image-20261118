#!/usr/bin/env python3
"""Draw a newspaper front page for Wednesday 18 November 2026.

Everything is drawn with Pillow shapes and text; no external images.
Output: entry.png, 1024 x 1024, deterministic (no randomness, no dates
taken from the clock).
"""

from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (247, 243, 232)
INK = (24, 24, 28)
RED = (158, 28, 32)
BLUE = (28, 64, 128)
GOLD = (196, 148, 44)
TEAL = (18, 96, 92)
GREY = (96, 96, 100)
CARD = (255, 255, 252)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, face, width):
    """Greedy word wrap returning a list of lines fitting `width` pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=face) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, face, width, leading, color=INK):
    x, y = xy
    for line in wrap(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, weight=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=weight)


def flag(draw, x, y, w, h, stripes):
    """A little striped flag on a pole, stripes = list of colors top-down."""
    draw.line([(x, y + h), (x, y - 18)], fill=INK, width=3)
    n = len(stripes)
    for i, c in enumerate(stripes):
        draw.rectangle([x + 2, y + i * h // n, x + w, y + (i + 1) * h // n], fill=c)


def rocket(draw, cx, cy, s):
    """A small upright rocket with a flame."""
    body = [(cx - 12 * s, cy + 26 * s), (cx + 12 * s, cy + 26 * s),
            (cx + 12 * s, cy - 8 * s), (cx, cy - 30 * s), (cx - 12 * s, cy - 8 * s)]
    draw.polygon(body, fill=(220, 224, 230), outline=INK, width=2)
    draw.polygon([(cx - 12 * s, cy + 6 * s), (cx - 26 * s, cy + 26 * s),
                  (cx - 12 * s, cy + 26 * s)], fill=RED)
    draw.polygon([(cx + 12 * s, cy + 6 * s), (cx + 26 * s, cy + 26 * s),
                  (cx + 12 * s, cy + 26 * s)], fill=RED)
    draw.ellipse([cx - 6 * s, cy - 12 * s, cx + 6 * s, cy], fill=TEAL, outline=INK)
    draw.polygon([(cx - 8 * s, cy + 26 * s), (cx + 8 * s, cy + 26 * s),
                  (cx, cy + 44 * s)], fill=GOLD)


def ballot_box(draw, x, y, w, h):
    draw.rectangle([x, y + h * 0.35, x + w, y + h], fill=BLUE, outline=INK, width=2)
    draw.rectangle([x + w * 0.28, y, x + w * 0.72, y + h * 0.38], fill=(255, 255, 255),
                   outline=INK, width=2)
    draw.line([(x + w * 0.5, y - 14), (x + w * 0.62, y + 2)], fill=RED, width=4)
    draw.line([(x + w * 0.62, y + 2), (x + w * 0.82, y - 22)], fill=RED, width=4)
    draw.text((x + w * 0.18, y + h * 0.52), "VOTE", font=font(SANS_B, 20), fill=(255, 255, 255))


def drone(draw, cx, cy, s):
    draw.rectangle([cx - 26 * s, cy - 8 * s, cx + 26 * s, cy + 8 * s],
                   fill=(70, 74, 80), outline=INK, width=2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            ax, ay = cx + sx * 34 * s, cy + sy * 16 * s
            draw.line([(cx + sx * 24 * s, cy + sy * 6 * s), (ax, ay)], fill=INK, width=3)
            draw.ellipse([ax - 14 * s, ay - 4 * s, ax + 14 * s, ay + 4 * s],
                         fill=(180, 184, 190), outline=INK)
    draw.ellipse([cx - 6 * s, cy - 6 * s, cx + 6 * s, cy + 6 * s], fill=RED, outline=INK)


def summit_table(draw, x, y, w, h):
    draw.ellipse([x, y + h * 0.45, x + w, y + h * 0.95], fill=(122, 82, 52), outline=INK, width=2)
    for fx, fy, col in ((x + w * 0.22, y, RED), (x + w * 0.72, y, GOLD)):
        draw.ellipse([fx, fy, fx + 34, fy + 34], fill=col, outline=INK, width=2)
    draw.rectangle([x + w * 0.42, y + h * 0.28, x + w * 0.58, y + h * 0.45],
                   fill=(255, 255, 255), outline=INK, width=2)


def chip(draw, x, y, s):
    draw.rectangle([x, y, x + 64 * s, y + 64 * s], fill=(40, 40, 48), outline=GOLD, width=3)
    draw.rectangle([x + 16 * s, y + 16 * s, x + 48 * s, y + 48 * s], fill=TEAL, outline=GOLD)
    for i in range(4):
        off = 12 * s + i * 14 * s
        draw.line([(x + off, y - 10 * s), (x + off, y)], fill=GOLD, width=3)
        draw.line([(x + off, y + 64 * s), (x + off, y + 74 * s)], fill=GOLD, width=3)
        draw.line([(x - 10 * s, y + off), (x, y + off)], fill=GOLD, width=3)
        draw.line([(x + 64 * s, y + off), (x + 74 * s, y + off)], fill=GOLD, width=3)


def starfield(draw, cx, cy, spread, n=6):
    for i in range(n):
        ang = -90 + i * (360 / n)
        x = cx + spread * math.cos(math.radians(ang))
        y = cy + spread * math.sin(math.radians(ang))
        draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 255, 255))


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead band ----
    d.rectangle([0, 0, W, 128], fill=INK)
    d.text((36, 18), "THE WORLD TODAY", font=font(SERIF_B, 62), fill=(247, 243, 232))
    d.text((36, 92), "WEDNESDAY 18 NOVEMBER 2026  |  ONE DAY, SIX STORIES",
           font=font(SANS_B, 20), fill=GOLD)
    d.text((W - 36 - d.textlength("No. 322", font=font(SANS, 18)), 96),
           "No. 322", font=font(SANS, 18), fill=(200, 200, 200))
    rule(d, 0, 128, W, 4, RED)
    d.text((36, 136), "SHENZHEN  •  DEEP SPACE  •  ALASKA  •  KUWAIT  •  MANILA  •  SILICON VALLEY",
           font=font(SANS_B, 13), fill=GREY)

    # ---- Lead panel: Xi & Putin in Shenzhen ----
    lx, ly, lw, lh = 36, 158, 952, 280
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=INK, width=3)
    d.rectangle([lx, ly, lx + lw, ly + 40], fill=RED)
    d.text((lx + 18, ly + 7), "LEAD  —  SHENZHEN", font=font(SANS_B, 22), fill=(255, 255, 255))
    summit_table(d, lx + 640, ly + 86, 260, 140)
    flag(d, lx + 660, ly + 172, 74, 34, [RED, (255, 255, 255), RED])
    flag(d, lx + 830, ly + 172, 74, 34, [(255, 255, 255), BLUE, RED])
    y = para(d, (lx + 20, ly + 56),
             "Xi and Putin meet in Shenzhen", font(SERIF_B, 38), 590, 46)
    y = para(d, (lx + 20, y + 6),
             "China's Xi Jinping and Russia's Vladimir Putin hold talks "
             "in Shenzhen, on the eve of Thursday's summit with Trump.",
             font(SANS, 22), 590, 29)
    d.text((lx + 20, y + 8), "The trilateral is set for tomorrow.",
           font=font(SANS_B, 22), fill=RED)

    # ---- Story grid: 3 columns x 2 rows ----
    gx, gy = 36, 452
    cw, ch, gap = 304, 252, 14
    stories = [
        ("SPACE", TEAL, "rocket",
         "Voyager 1 one light-day out",
         "NASA's Voyager 1 is now 16 billion miles out. "
         "Its signal takes 24 hours to reach Earth."),
        ("UNITED STATES", BLUE, "ballot",
         "Peltola wins Alaska",
         "Mary Peltola takes Alaska's Senate seat, giving Democrats "
         "a 56-44 majority — the first Alaska Native senator."),
        ("MIDDLE EAST", RED, "drone",
         "Iran's drones reach Kuwait",
         "Drones from Iran reached Kuwait; Ali Al Salem base "
         "engaged them, and Bahrain intercepted more."),
        ("ASIA", GOLD, "table",
         "Quad leaders meet in Manila",
         "Leaders of the Quad meet in Manila, their first summit in "
         "over two years."),
        ("TECHNOLOGY", (90, 60, 140), "chip",
         "OpenAI launches GPT-6.2",
         "OpenAI unveils GPT-6.2 Astra and Sol, with lower prices "
         "for developers using its API."),
        ("THE DAY IN BRIEF", GREY, "globe",
         "Six stories, one day",
         "From Shenzhen to deep space, from Manila to Washington: "
         "Wednesday 18 November 2026 in one page."),
    ]
    for i, (kicker, accent, motif, headline, body) in enumerate(stories):
        col, row = i % 3, i // 3
        x = gx + col * (cw + gap)
        yy = gy + row * (ch + gap)
        d.rectangle([x, yy, x + cw, yy + ch], fill=CARD, outline=INK, width=2)
        d.rectangle([x, yy, x + cw, yy + 30], fill=accent)
        d.text((x + 12, yy + 5), kicker, font=font(SANS_B, 16), fill=(255, 255, 255))
        my = yy + 44
        if motif == "rocket":
            rocket(d, x + 48, my + 24, 0.85)
            d.ellipse([x + 92, my + 4, x + 168, my + 80], fill=(18, 24, 44))
            starfield(d, x + 130, my + 42, 24, 6)
            d.text((x + 180, my + 22), "1 light-day", font=font(SANS_B, 18), fill=TEAL)
            d.text((x + 180, my + 46), "16bn miles", font=font(SANS, 16), fill=INK)
        elif motif == "ballot":
            ballot_box(d, x + 30, my + 8, 92, 84)
            d.text((x + 142, my + 18), "56 - 44", font=font(SERIF_B, 34), fill=BLUE)
            d.text((x + 142, my + 60), "Senate", font=font(SANS_B, 18), fill=INK)
        elif motif == "drone":
            drone(d, x + 80, my + 44, 1.0)
            d.text((x + 176, my + 20), "Ali Al Salem", font=font(SANS_B, 18), fill=INK)
            d.text((x + 176, my + 46), "Bahrain", font=font(SANS, 18), fill=INK)
            d.text((x + 176, my + 70), "intercepted", font=font(SANS, 18), fill=INK)
        elif motif == "table":
            summit_table(d, x + 24, my + 4, 130, 84)
            d.text((x + 168, my + 8), "4 leaders", font=font(SANS_B, 16), fill=INK)
            d.text((x + 168, my + 30), "Manila", font=font(SANS, 16), fill=INK)
            d.text((x + 168, my + 52), "trade deal", font=font(SANS, 16), fill=INK)
        elif motif == "chip":
            chip(d, x + 30, my + 6, 1.0)
            d.text((x + 128, my + 14), "Astra", font=font(SERIF_B, 26), fill=(90, 60, 140))
            d.text((x + 128, my + 48), "Sol", font=font(SERIF_B, 26), fill=(90, 60, 140))
            d.text((x + 128, my + 76), "cheaper API", font=font(SANS, 16), fill=INK)
        else:
            d.ellipse([x + 26, my + 6, x + 116, my + 96], fill=TEAL, outline=INK, width=2)
            d.ellipse([x + 52, my + 6, x + 90, my + 96], outline=(255, 255, 255), width=2)
            d.line([(x + 26, my + 51), (x + 116, my + 51)], fill=(255, 255, 255), width=2)
            d.text((x + 132, my + 26), "18 NOV", font=font(SERIF_B, 28), fill=INK)
            d.text((x + 132, my + 60), "2026", font=font(SERIF_B, 28), fill=RED)
        ty = yy + 140
        ty = para(d, (x + 14, ty), headline, font(SERIF_B, 21), cw - 28, 25)
        para(d, (x + 14, ty + 2), body, font(SANS, 16), cw - 28, 19)

    # ---- Footer ----
    rule(d, 36, 988, 988, 2)
    d.text((36, 996), "Drawn in code  •  Wednesday 18 November 2026",
           font=font(SANS, 15), fill=GREY)
    d.text((W - 36 - d.textlength("THE WORLD TODAY", font=font(SANS_B, 15)), 996),
           "THE WORLD TODAY", font=font(SANS_B, 15), fill=GREY)
    return img


if __name__ == "__main__":
    page = draw_page()
    page.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", page.size)
