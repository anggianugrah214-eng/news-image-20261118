#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (entry.png).

Flat, code-drawn newspaper front page: masthead with the date, one lead
story and five more across regions and fields. Every headline and figure
comes from the day's reporting (wires and broadcasters, 18 Nov 2026).
Run: python3 draw_image.py  -> writes entry.png (1024x1024, JPEG).
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
RED = (185, 28, 28)
GREY = (90, 90, 90)
WHITE = (255, 253, 248)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
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


def text_block(draw, x, y, text, fnt, color, max_w, leading):
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, s, fnt):
    draw.text((x, y), s, font=fnt, fill=RED)
    return y + 26


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead: 24..168 ----------
d.rectangle([28, 24, 996, 168], fill=NAVY)
d.text((52, 38), "T H E   W O R L D   I N   O N E   D A Y",
       font=font(SANS, 21), fill=GOLD)
d.text((52, 64), "WEDNESDAY 18 NOVEMBER 2026",
       font=font(SERIF, 54), fill=WHITE)
d.rectangle([52, 132, 972, 135], fill=GOLD)
d.text((52, 142), "Six stories that defined the day — from Shenzhen to deep space, Manila to Alaska",
       font=font(SANS_R, 18), fill=(200, 205, 220))

# ---------- lead story: 180..484 ----------
d.rectangle([28, 180, 996, 484], fill=WHITE, outline=INK, width=2)
# illustration: dusk over the Shenzhen skyline (left half)
d.rectangle([30, 182, 430, 482], fill=(30, 44, 78))
for sx, sy, r in [(70, 210, 2), (140, 226, 2), (250, 202, 2), (330, 232, 2),
                  (110, 258, 2), (300, 262, 2), (390, 212, 2), (200, 240, 2)]:
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=WHITE)
d.ellipse([352, 200, 398, 246], fill=(235, 220, 170))  # low sun
# skyline towers
for bx, bw, bh in [(44, 44, 150), (96, 30, 190), (134, 52, 120),
                   (196, 34, 210), (238, 46, 140), (292, 30, 175),
                   (330, 56, 110), (392, 30, 150)]:
    d.rectangle([bx, 482 - bh, bx + bw, 482], fill=(12, 20, 38))
    for wy in range(482 - bh + 12, 470, 22):
        for wx in range(bx + 6, bx + bw - 4, 12):
            d.rectangle([wx, wy, wx + 4, wy + 6], fill=(240, 200, 90))
# three flag circles: China, Russia, U.S.
d.ellipse([66, 376, 126, 436], fill=(222, 41, 16), outline=WHITE, width=2)
d.text((84, 392), "*", font=font(SANS, 30), fill=GOLD)
d.ellipse([146, 376, 206, 436], fill=WHITE, outline=NAVY, width=2)
d.rectangle([146, 376, 206, 396], fill=(0, 57, 166))
d.rectangle([146, 416, 206, 436], fill=(213, 0, 50))
d.ellipse([226, 376, 286, 436], fill=(60, 59, 110), outline=WHITE, width=2)
d.text((238, 390), "USA", font=font(SANS, 16), fill=WHITE)
d.text((44, 452), "SHENZHEN, CHINA", font=font(SANS, 16), fill=(180, 200, 220))
# lead text (right half)
tx = 452
y = kicker(d, tx, 198, "ASIA  •  LEAD STORY", font(SANS, 20))
y = text_block(d, tx, y, "XI AND PUTIN MEET IN SHENZHEN BEFORE TRUMP TALKS",
               font(SANS, 40), INK, 996 - tx - 24, 48)
y += 8
text_block(d, tx, y,
           "China's Xi and Russia's Putin opened APEC in Shenzhen. A rare "
           "three-way summit with U.S. President Trump is set for Thursday.",
           font(SANS_R, 23), (60, 60, 60), 996 - tx - 24, 30)

# ---------- middle row: 496..736 ----------
# Voyager 1
d.rectangle([28, 496, 500, 736], fill=WHITE, outline=INK, width=2)
d.rectangle([30, 498, 498, 600], fill=(5, 8, 20))  # deep space
for sx, sy, r in [(70, 520, 2), (150, 560, 2), (260, 515, 2), (350, 570, 2),
                  (430, 530, 2), (200, 585, 2), (320, 545, 1), (110, 585, 1)]:
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=WHITE)
# probe: bus, dish, boom
d.rectangle([150, 540, 210, 570], fill=(180, 180, 190), outline=(120, 120, 130), width=2)
d.polygon([(210, 542), (258, 528), (258, 584), (210, 570)], fill=(200, 200, 210),
          outline=(120, 120, 130))
d.line([150, 555, 96, 540], fill=(200, 200, 210), width=4)
d.line([150, 555, 96, 572], fill=(200, 200, 210), width=4)
d.ellipse([88, 532, 104, 548], fill=GOLD)
d.text((264, 545), "16 BN MILES", font=font(SERIF, 28), fill=GOLD)
y = kicker(d, 44, 608, "SPACE  •  SCIENCE", font(SANS, 18))
y = text_block(d, 44, y, "VOYAGER 1 REACHES ONE LIGHT-DAY FROM EARTH",
               font(SANS, 29), INK, 500 - 44 - 16, 34)
text_block(d, 44, y + 4, "First human-made object that far out.",
           font(SANS_R, 19), (60, 60, 60), 500 - 44 - 16, 25)

# Peltola / Senate
d.rectangle([524, 496, 996, 736], fill=WHITE, outline=INK, width=2)
d.rectangle([526, 498, 994, 600], fill=(16, 40, 80))  # senate blue
d.rectangle([526, 586, 994, 600], fill=(185, 28, 28))  # red stripe
d.rectangle([526, 572, 994, 586], fill=WHITE)
d.ellipse([710, 506, 810, 570], fill=WHITE, outline=NAVY, width=3)
d.text((742, 512), "56", font=font(SERIF, 36), fill=NAVY)
d.text((748, 546), "–44", font=font(SANS, 15), fill=NAVY)
for sx, sy in [(600, 530), (640, 560), (880, 530), (920, 560)]:
    d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=GOLD)
y = kicker(d, 540, 608, "U.S.  •  POLITICS", font(SANS, 18))
y = text_block(d, 540, y, "PELTOLA WINS ALASKA; SENATE 56–44",
               font(SANS, 29), INK, 996 - 540 - 16, 34)
text_block(d, 540, y + 4, "First Alaska Native elected to the Senate.",
           font(SANS_R, 19), (60, 60, 60), 996 - 540 - 16, 25)


def small_panel(x0, x1, kick, head, stand, art):
    d.rectangle([x0, 748, x1, 972], fill=WHITE, outline=INK, width=2)
    art(x0, x1)
    y = kicker(d, x0 + 14, 830, kick, font(SANS, 16))
    y = text_block(d, x0 + 14, y, head, font(SANS, 23), INK, x1 - x0 - 28, 28)
    text_block(d, x0 + 14, y + 4, stand, font(SANS_R, 17), (60, 60, 60),
               x1 - x0 - 28, 22)


def art_drone(x0, x1):
    cx, cy = (x0 + x1) // 2, 790
    d.rectangle([x0 + 2, 820, x1 - 2, 830], fill=(210, 180, 120))  # desert
    for dx, dy in [(-40, -16), (10, -30), (46, -8)]:
        d.ellipse([cx + dx - 14, cy + dy - 5, cx + dx + 14, cy + dy + 5],
                  fill=(60, 60, 60))
        d.line([cx + dx - 22, cy + dy, cx + dx + 22, cy + dy], fill=(60, 60, 60), width=3)
    d.arc([cx - 52, cy - 46, cx + 52, cy + 20], start=200, end=340,
          fill=RED, width=2)


def art_quad(x0, x1):
    cx, cy = (x0 + x1) // 2, 790
    d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=(40, 90, 160),
              outline=NAVY, width=2)
    d.ellipse([cx - 13, cy - 32, cx + 13, cy + 32], outline=(180, 210, 235), width=2)
    d.line([cx - 32, cy, cx + 32, cy], fill=(180, 210, 235), width=2)
    for dx, dy, col in [(-24, -20, (185, 28, 28)), (24, -20, (0, 57, 166)),
                        (-24, 20, (255, 153, 51)), (24, 20, (0, 130, 130))]:
        d.ellipse([cx + dx - 8, cy + dy - 8, cx + dx + 8, cy + dy + 8],
                  fill=col, outline=WHITE, width=2)


def art_ai(x0, x1):
    cx, cy = (x0 + x1) // 2, 790
    d.rectangle([cx - 46, cy - 26, cx + 46, cy + 26], fill=(16, 24, 16),
                outline=(120, 200, 90), width=3)
    d.text((cx, cy - 14), "GPT-6.2", font=font(SANS, 20), fill=(140, 220, 120),
           anchor="ma")
    for ang in range(0, 360, 45):
        x2 = cx + 58 * math.cos(math.radians(ang))
        y2 = cy + 58 * math.sin(math.radians(ang))
        d.line([cx + 52 * math.cos(math.radians(ang)),
                cy + 52 * math.sin(math.radians(ang)), x2, y2],
               fill=GOLD, width=3)


small_panel(28, 344, "MIDDLE EAST  •  GULF",
            "IRAN'S DRONES REACH KUWAIT",
            "Kuwait engaged drones at Ali Al Salem base; Bahrain stopped more.",
            art_drone)
small_panel(360, 664, "ASIA-PACIFIC  •  SECURITY",
            "QUAD MEETS IN MANILA",
            "First leaders' meeting in two years; a Philippines deal.",
            art_quad)
small_panel(680, 996, "TECH  •  AI",
            "OPENAI LAUNCHES GPT-6.2",
            "New Astra and Sol models arrive with lower API prices.",
            art_ai)

# ---------- footer ----------
d.text((512, 986), "18 NOVEMBER 2026  •  From the day's wires and broadcasters",
       font=font(SANS_R, 16), fill=GREY, anchor="ma")

img.save("entry.png", format="JPEG", quality=88)
print("wrote entry.png")
