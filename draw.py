"""Draw the news-image entry for Tuesday 24 November 2026.

Renders a 1024x1024 newspaper front page: masthead, giant date, stat strip,
region strip, UTC timeline, 3 illustrated lead cards, 10 numbered medium
cards, a brief digest, a numbered world map, a DATE CHECK box and a footer.
All stories were researched fresh on 24 Nov 2026 and are recorded in the
story bank (story-bank/news-image-20261124.json in the builder's workspace).
Font: Lexend (OFL), static weights committed under fonts/.

Run:  python3 draw.py            -> writes entry.png next to this file
       python3 draw.py out.png   -> writes to the given path
Deterministic: same bytes on every run (no timestamps, no randomness).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

PAPER = (246, 241, 229)
INK = (25, 25, 25)
RED = (180, 35, 24)
DARKRED = (143, 29, 20)
NAVY = (29, 53, 87)
TEAL = (14, 107, 92)
AMBER = (161, 98, 7)
GREEN = (22, 101, 52)
PURPLE = (107, 33, 168)
SLATE = (71, 85, 105)
MUTED = (107, 107, 102)
PANEL = (239, 232, 214)
MAPSEA = (220, 232, 234)
MAPLAND = (217, 201, 163)
MAPLINE = (160, 140, 105)
WHITE = (255, 255, 255)
CREAM = (250, 246, 236)


def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", "Lexend-%s.ttf" % name), size)


F_DATE = None
F_SUB = None
F_STAT_N = None
F_STAT_L = None
F_REGION = None
F_TIME = None
F_LEAD_H = None
F_LEAD_D = None
F_LEAD_S = None
F_MED_H = None
F_MED_D = None
F_MED_S = None
F_BRIEF = None
F_SMALL = None
F_TINY = None


def load_fonts():
    global F_DATE, F_SUB, F_STAT_N, F_STAT_L, F_REGION, F_TIME
    global F_LEAD_H, F_LEAD_D, F_LEAD_S, F_MED_H, F_MED_D, F_MED_S
    global F_BRIEF, F_SMALL, F_TINY
    F_DATE = font("Bold", 60)
    F_SUB = font("Medium", 16)
    F_STAT_N = font("Bold", 25)
    F_STAT_L = font("Regular", 10)
    F_REGION = font("SemiBold", 11)
    F_TIME = font("Regular", 11)
    F_LEAD_H = font("Bold", 20)
    F_LEAD_D = font("Regular", 12)
    F_LEAD_S = font("SemiBold", 10)
    F_MED_H = font("Bold", 13)
    F_MED_D = font("Regular", 11)
    F_MED_S = font("SemiBold", 9)
    F_BRIEF = font("Regular", 10)
    F_SMALL = font("Regular", 11)
    F_TINY = font("Regular", 10)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines = []
    cur = ""
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


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- illustrations
def ill_ulleung(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 32, 64))
    for sx, sy in [(20, 14), (70, 26), (130, 10), (200, 30), (260, 12), (300, 22)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=WHITE)
    d.ellipse([x + w - 52, y + 10, x + w - 18, y + 44], fill=(232, 226, 200))
    d.polygon([(x + 30, y + h), (x + 70, y + h - 42), (x + 120, y + h - 30),
               (x + 170, y + h - 48), (x + 220, y + h - 26), (x + 260, y + h - 40),
               (x + w, y + h - 20), (x + w, y + h), (x, y + h)], fill=(8, 18, 38))
    d.line([(x + 40, y + 66), (x + 130, y + 44), (x + 210, y + 30), (x + 280, y + 22)],
           fill=(240, 200, 90), width=2)
    for i, px in enumerate([130, 180, 230]):
        d.ellipse([x + px - 2, y + 46 - i * 8 - 2, x + px + 2, y + 46 - i * 8 + 2],
                  fill=(240, 200, 90))
    d.polygon([(x + 258, y + 18), (x + 282, y + 24), (x + 258, y + 30)], fill=(240, 200, 90))
    d.ellipse([x + w - 78, y + h - 52, x + w - 30, y + h - 4], outline=RED, width=4)
    d.text((x + w - 66, y + h - 40), "!", font=font("Bold", 24), fill=RED)


def ill_nvidia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 26, 18))
    for gx in range(0, w, 26):
        d.line([(x + gx, y), (x + gx, y + h)], fill=(24, 48, 34), width=1)
    for gy in range(0, h, 26):
        d.line([(x, y + gy), (x + w, y + gy)], fill=(24, 48, 34), width=1)
    d.rectangle([x + 16, y + 30, x + 76, y + 90], outline=(118, 185, 0), width=3)
    d.rectangle([x + 30, y + 44, x + 62, y + 76], outline=(118, 185, 0), width=2)
    d.line([(x + 84, y + 88), (x + 140, y + 66), (x + 190, y + 72), (x + 250, y + 34),
            (x + 300, y + 16)], fill=(118, 185, 0), width=4)
    d.polygon([(x + 288, y + 8), (x + 306, y + 18), (x + 290, y + 26)], fill=(118, 185, 0))
    d.rectangle([x + w - 96, y + 12, x + w - 12, y + 40], fill=(118, 185, 0))
    d.text((x + w - 90, y + 15), "+31%", font=font("Bold", 20), fill=(12, 26, 18))


def ill_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(64, 48, 40))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(38, 28, 24))
    d.rectangle([x + 24, y + 40, x + 130, y + h - 14], fill=(120, 84, 60))
    d.rectangle([x + 150, y + 56, x + 250, y + h - 14], fill=(96, 66, 48))
    for wx in [40, 70, 100, 166, 196, 226]:
        d.rectangle([x + wx, y + 54, x + wx + 16, y + 68], fill=(240, 200, 90))
    d.rectangle([x + 270, y + 16, x + 282, y + h - 14], fill=(150, 110, 80))
    for cx, cy, r in [(285, 12, 10), (300, 2, 12), (262, 4, 8)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=(200, 190, 175))
    d.line([(x + 60, y + h - 14), (x + 60, y + h - 34)], fill=(240, 200, 90), width=3)
    d.polygon([(x + 44, y + h - 34), (x + 76, y + h - 34), (x + 60, y + h - 48)],
              fill=(240, 200, 90))


def ill_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 198))
    sq = 14
    for r in range(4):
        for c in range(8):
            if (r + c) % 2 == 0:
                d.rectangle([x + c * sq + 8, y + r * sq, x + (c + 1) * sq + 8,
                             y + (r + 1) * sq], fill=(60, 48, 36))
    d.ellipse([x + 140, y + 8, x + 168, y + 36], fill=INK)
    d.ellipse([x + 152, y + 2, x + 166, y + 16], fill=INK)
    d.rectangle([x + 176, y + 20, x + 188, y + 52], fill=(200, 170, 120))
    d.ellipse([x + 174, y + 8, x + 190, y + 24], fill=(200, 170, 120))


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(88, 96, 78))
    d.polygon([(x + w // 2, y + 6), (x + w - 14, y + h - 8), (x + 14, y + h - 8)],
              outline=(240, 200, 90), width=3)
    d.text((x + w // 2 - 5, y + 22), "!", font=font("Bold", 18), fill=(240, 200, 90))
    for dx, dy in [(30, 44), (150, 40), (60, 48), (120, 46)]:
        d.ellipse([x + dx, y + dy, x + dx + 6, y + dy + 8], fill=(150, 190, 200))


def ill_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 30, 24))
    d.line([(x + 10, y + 12), (x + 60, y + 26), (x + 110, y + 20), (x + 160, y + 44),
            (x + 190, y + 50)], fill=WHITE, width=3)
    d.polygon([(x + 150, y + 8), (x + 168, y + 8), (x + 168, y + 26), (x + 150, y + 26)],
              outline=WHITE, width=2)
    d.line([(x + 150, y + 26), (x + 168, y + 8)], fill=WHITE, width=2)


def ill_grok(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 28, 96))
    d.rectangle([x + 78, y + 6, x + 118, y + h - 6], outline=WHITE, width=2)
    d.line([(x + 78, y + 16), (x + 118, y + 16)], fill=WHITE, width=1)
    d.ellipse([x + 140, y + 14, x + 176, y + 50], outline=(240, 200, 90), width=3)
    d.line([(x + 140, y + 14), (x + 176, y + 50)], fill=(240, 200, 90), width=3)
    d.line([(x + 176, y + 14), (x + 140, y + 50)], fill=(240, 200, 90), width=3)


def ill_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 68, 120))
    d.ellipse([x + 70, y + 4, x + 126, y + 52], outline=WHITE, width=2)
    d.ellipse([x + 78, y + 12, x + 118, y + 44], fill=(90, 170, 120))
    d.rectangle([x + 140, y + 30, x + 186, y + 36], fill=(240, 200, 90))
    for gx in [146, 158, 170, 182]:
        d.rectangle([x + gx, y + 20, x + gx + 6, y + 30], fill=(240, 200, 90))


def ill_macron(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 52, 110))
    d.rectangle([x + 130, y + 8, x + 170, y + h - 8], fill=(240, 200, 90))
    d.ellipse([x + 138, y + 4, x + 162, y + 28], outline=(200, 160, 60), width=2)
    d.text((x + 144, y + 8), "$", font=font("Bold", 16), fill=(200, 160, 60))
    d.rectangle([x + 12, y + 10, x + 52, y + h - 10], fill=(0, 60, 140))
    d.rectangle([x + 52, y + 10, x + 92, y + h - 10], fill=WHITE)
    d.rectangle([x + 92, y + 10, x + 120, y + h - 10], fill=RED)


def ill_bars(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 64, 72))
    d.rectangle([x + 16, y + 18, x + 90, y + h - 10], fill=(120, 110, 96))
    d.rectangle([x + 100, y + 30, x + 180, y + h - 10], fill=(90, 82, 72))
    for bx in [30, 52, 74, 118, 142, 166]:
        d.line([(x + bx, y + 6), (x + bx, y + h - 6)], fill=INK, width=3)


def ill_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(44, 62, 80))
    d.ellipse([x + 30, y + 8, x + 90, y + 38], fill=(200, 205, 210))
    d.ellipse([x + 70, y + 16, x + 140, y + 44], fill=(170, 178, 185))
    for rx in [50, 80, 110]:
        d.line([(x + rx, y + 44), (x + rx - 6, y + 54)], fill=(120, 170, 220), width=2)
    d.polygon([(x + 150, y + 34), (x + 186, y + 40), (x + 150, y + 46)], fill=WHITE)


def ill_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 101, 52))
    d.rectangle([x + 30, y + 10, x + 44, y + 46], fill=(210, 180, 130))
    d.ellipse([x + 150, y + 30, x + 164, y + 44], fill=RED)
    d.line([(x + 60, y + 44), (x + 150, y + 44)], fill=WHITE, width=2)
    d.line([(x + 90, y + 12), (x + 90, y + 52)], fill=WHITE, width=2)
    d.line([(x + 120, y + 12), (x + 120, y + 52)], fill=WHITE, width=2)


def ill_radar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 40, 70))
    d.ellipse([x + 66, y + 2, x + 130, y + 54], outline=(90, 200, 120), width=2)
    d.ellipse([x + 80, y + 14, x + 116, y + 44], outline=(90, 200, 120), width=1)
    d.line([(x + 98, y + 28), (x + 128, y + 8)], fill=(90, 200, 120), width=3)
    d.polygon([(x + 150, y + 16), (x + 184, y + 24), (x + 150, y + 32)], fill=(200, 200, 200))


ILL = {1: ill_ulleung, 2: ill_nvidia, 3: ill_factory, 4: ill_chess, 5: ill_gaza,
       6: ill_markets, 7: ill_grok, 8: ill_globe, 9: ill_macron, 10: ill_bars,
       11: ill_storm, 12: ill_cricket, 13: ill_radar}

LEADS = [
    ("1  ULLEUNG ISLAND \u00b7 SECURITY",
     "Seoul sounds air-raid alert as jets near island",
     "Alert at 7:52am; lifted minutes later. Military says jets entered the air defence zone.",
     "REUTERS"),
    ("2  WALL STREET \u00b7 MARKETS",
     "Huang's comeback shakes Wall Street",
     "Shares jumped 31% Monday; Nasdaq +6.5%. Lawmakers attack the U-turn today.",
     "REUTERS"),
    ("3  CIKANDE, INDONESIA \u00b7 DISASTER",
     "More bodies found at Indonesia candy factory",
     "Rescuers keep searching the wreckage; 24 dead, about 30 missing; 29 safe.",
     "REUTERS"),
]

MEDIUM = [
    ("4  GENEVA \u00b7 CHESS", "Gukesh defends chess crown in Geneva",
     "Game 1 today vs Sindarov; both 20; 14 games, $2.5m prize.", "FIDE"),
    ("5  GAZA \u00b7 ENVIRONMENT", "Gaza a \u2018toxic wasteland\u2019, Oxfam warns",
     "99% shows contamination; 78% of its land hit.", "OXFAM"),
    ("6  SEOUL \u00b7 MARKETS", "Asia acts to stop the AI sell-off",
     "Korea eases buybacks, readies a fund; Taiwan curbs short sales.", "REUTERS"),
    ("7  WASHINGTON \u00b7 TECH", "Two states sue Musk's SpaceX over Grok images",
     "Virginia and Oregon file the first state suits.", "REUTERS"),
    ("8  BARBADOS \u00b7 TECH", "UN chief calls for global AI rules in a year",
     "Guterres calls for shared safety tests and oversight.", "UN NEWS"),
    ("9  PARIS \u00b7 POLITICS", "Macron weighs a \u2018golden rule\u2019 on spending",
     "Deficit 5.4% of GDP, above the EU's 3% limit; vote eyed Jan.", "AFP"),
    ("10  MURMANSK \u00b7 RUSSIA", "Russian governor held in graft probe",
     "Chibis detained over budget funds; court decides today.", "REUTERS"),
    ("11  FLORIDA \u00b7 WEATHER", "Storm threatens Thanksgiving travel",
     "Storm forms in the Gulf today; 81.5m travel; gusts above 50mph.", "ACCUWEATHER"),
    ("12  WELLINGTON \u00b7 CRICKET", "New Zealand bat out a draw in Wellington",
     "Mitchell 49* and Phillips 26* survive 120 overs; India 720/9.", "ICC"),
    ("13  POLAND \u00b7 SECURITY", "NATO sends spy plane to Poland",
     "Early-warning aircraft to deploy after three missiles landed on Friday.", "REUTERS"),
]

BRIEFS = [
    ("14", "Gaza strikes kill three, including UN aid worker", "Reuters"),
    ("15", "Iran vows to confront US naval blockade", "Reuters"),
    ("16", "Iran flogs singer and her team, 74 lashes", "Reuters"),
    ("17", "US sanctions Iran shadow-banking networks", "Reuters"),
    ("18", "US weighs first training mission for Syrian forces", "Reuters"),
    ("19", "Mexico captures \u2018Chapo Isidro\u2019 with US help", "Reuters"),
    ("20", "Deputy FBI director to retire in December", "Reuters"),
    ("21", "Trump pauses lead-azide detonation in Iowa", "Reuters"),
    ("22", "CrowdStrike buys Zscaler for $43.9bn", "Reuters"),
    ("23", "Brent crude at $92.10 a barrel", "AP"),
    ("24", "India weighs 20% rice export duties", "Reuters"),
    ("25", "Modi opens AI centre at IIT Patna", "Times of India"),
    ("26", "India-China hold military talks in Arunachal", "Times of India"),
    ("27", "Victoria votes Saturday; One Nation eyes 10 seats", "Reuters"),
    ("28", "COP31 backlash: Australia, Pacific despair", "Reuters"),
    ("29", "S&P 500 down 12% since October peak", "Reuters"),
    ("30", "Taiwan stocks suffer worst week in 35 years", "Reuters"),
    ("31", "US Treasury sells $70bn of five-year notes", "Reuters"),
    ("32", "Nepal PM in India for economy, energy talks", "Manila Times"),
    ("33", "Congressman Gomez quits after ethics report", "AP"),
    ("34", "Germany to use Ukraine's Delta battlefield tool", "Reuters"),
    ("35", "Nigeria president admits villa power cuts", "Sunday Guardian"),
]

REGIONS = [("Europe", 5, NAVY), ("Asia", 8, RED), ("Middle East", 5, AMBER),
           ("Africa", 1, GREEN), ("Americas", 11, PURPLE), ("Oceania", 3, TEAL),
           ("Global", 2, SLATE)]

STATS = [
    ("31%", "Nvidia shares jump"),
    ("24", "dead in factory fire"),
    ("99%", "of Gaza contaminated"),
    ("81.5m", "Thanksgiving travellers"),
    ("+6.5%", "Nasdaq rebound Monday"),
    ("$43.9bn", "CrowdStrike buys Zscaler"),
]

TIMELINE = ("00:30 Japan PMI lands \u00b7 08:00 Germany Ifo due \u00b7 14:00 Chess Game 1, "
            "Geneva \u00b7 14:45 US flash PMIs \u00b7 18:00 Treasury sells $70bn notes")

DATE_CHECK = ("DATE CHECK \u2014 LEFT OUT AS OLDER NEWS:  COP31 collapse (Sun 22)  \u00b7  "
              "Kyiv strikes kill 14 (Sun 22)  \u00b7  Indonesia fire breaks out (Sat 21)  \u00b7  "
              "Alcaraz wins ATP Finals (Sun 22)  \u00b7  Istanbul media protest (Sun 22)  \u00b7  "
              "Khartoum drone attack (Sun 22).   NOT YET: US inflation (Wed) \u00b7 Thanksgiving (Thu).")

# World map: coarse continent polygons in (lon, lat).
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80), (-75, 73),
     (-60, 62), (-55, 52), (-65, 45), (-75, 35), (-80, 25), (-85, 20), (-90, 15),
     (-95, 18), (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    [(-80, 10), (-75, 5), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-50, -30),
     (-60, -38), (-70, -50), (-75, -40), (-70, -20), (-80, -5)],
    [(-10, 36), (-5, 43), (0, 46), (-2, 50), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (23, 60), (30, 62), (30, 70), (25, 71), (18, 69), (12, 65), (5, 60),
     (5, 58), (0, 51), (-5, 48), (-9, 43)],
    [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15), (48, 11),
     (51, 10), (48, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -30),
     (12, -18), (8, 4), (-8, 5), (-15, 12), (-17, 20), (-15, 28)],
    [(30, 70), (40, 68), (55, 70), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70),
     (170, 66), (178, 65), (170, 60), (160, 55), (150, 45), (140, 40), (130, 35),
     (127, 35), (120, 30), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22),
     (80, 15), (75, 8), (70, 20), (60, 25), (55, 26), (50, 28), (45, 30), (40, 35), (35, 36)],
    [(113, -22), (120, -15), (130, -12), (135, -12), (142, -10), (150, -22),
     (153, -27), (150, -37), (140, -38), (130, -32), (120, -34), (113, -25)],
    [(167, -45), (174, -41), (178, -37)],
]

# (number, lon, lat) pins for the 13 numbered cards.
PINS = [(1, 130.9, 37.5), (2, -74.0, 40.7), (3, 106.3, -6.2), (4, 6.1, 46.2),
        (5, 34.5, 31.5), (6, 127.0, 37.5), (7, -77.0, 38.9), (8, -59.6, 13.2),
        (9, 2.35, 48.85), (10, 33.1, 69.0), (11, -81.0, 28.0), (12, 174.8, -41.3),
        (13, 21.0, 52.2)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=MAPSEA)
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360.0 * w, y + (90 - lat) / 180.0 * h)
               for lon, lat in poly]
        d.polygon(pts, fill=MAPLAND, outline=MAPLINE)
    for num, lon, lat in PINS:
        px = x + (lon + 180) / 360.0 * w
        py = y + (90 - lat) / 180.0 * h
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
        d.text((px - 3 if num < 10 else px - 6, py - 6), str(num),
               font=font("Bold", 10), fill=WHITE)


def draw():
    load_fonts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((12, 8), "THE WORLD IN ONE DAY", font=font("Bold", 16), fill=RED)
    right = "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED TUESDAY 24 NOVEMBER 2026"
    d.text((W - 12 - d.textlength(right, font=font("Bold", 11)), 12), right,
           font=font("Bold", 11), fill=INK)
    hline(d, 12, W - 12, 34, width=3)
    hline(d, 12, W - 12, 39, width=1)

    # ---- giant date
    d.text((12, 46), "Tuesday 24 November 2026", font=F_DATE, fill=INK)

    # ---- red sub-headline
    d.text((12, 116), "Russian jets rattle Seoul \u00b7 Huang's comeback lifts Wall Street \u00b7 "
                      "Rescuers dig on in Indonesia", font=F_SUB, fill=RED)

    # ---- stat strip
    y0, y1 = 138, 190
    bw = (W - 24 - 5 * 6) / 6.0
    for i, (num, label) in enumerate(STATS):
        bx = 12 + i * (bw + 6)
        d.rectangle([bx, y0, bx + bw, y1], outline=INK, width=1)
        d.text((bx + 8, y0 + 4), num, font=F_STAT_N, fill=RED)
        lines = wrap(d, label, F_STAT_L, bw - 16)
        text_block(d, bx + 8, y0 + 31, lines[:2], F_STAT_L, MUTED, 11)

    # ---- region legend (coloured squares + counts, no cramped segments)
    y0 = 196
    items = []
    for name, count, color in REGIONS:
        items.append((name, count, color))
    total_w = 0
    parts = []
    for name, count, color in items:
        label = "%s %d" % (name, count)
        tw = d.textlength(label, font=F_REGION)
        parts.append((label, tw, color))
        total_w += 14 + tw + 18
    total_w -= 18
    rx = (W - total_w) / 2
    for label, tw, color in parts:
        d.rectangle([rx, y0 + 2, rx + 10, y0 + 12], fill=color)
        d.text((rx + 14, y0), label, font=F_REGION, fill=INK)
        rx += 14 + tw + 18

    # ---- timeline
    d.text((12, 224), "THE DAY IN UTC", font=font("Bold", 11), fill=RED)
    d.text((128, 224), TIMELINE, font=F_TIME, fill=INK)
    hline(d, 12, W - 12, 242, width=1)

    # ---- lead cards
    lw = 322
    for i, (tag, head, deck, src) in enumerate(LEADS):
        lx = 12 + i * (lw + 12)
        ly = 250
        ILL[i + 1](d, lx, ly, lw, 96)
        d.text((lx, ly + 102), tag, font=font("Bold", 11), fill=RED)
        lines = wrap(d, head, F_LEAD_H, lw)
        y = text_block(d, lx, ly + 120, lines[:2], F_LEAD_H, INK, 23)
        dlines = wrap(d, deck, F_LEAD_D, lw)
        text_block(d, lx, y + 2, dlines[:2], F_LEAD_D, INK, 15)
        d.text((lx, ly + 200), src, font=F_LEAD_S, fill=MUTED)
        hline(d, lx, lx + lw, ly + 214, fill=MUTED, width=1)

    # ---- medium cards, two rows of five
    mw = 196
    for row in range(2):
        for col in range(5):
            idx = row * 5 + col
            tag, head, deck, src = MEDIUM[idx]
            mx = 12 + col * (mw + 8)
            my = 476 + row * 160
            ILL[idx + 4](d, mx, my, mw, 56)
            d.text((mx, my + 60), tag, font=font("Bold", 10), fill=RED)
            lines = wrap(d, head, F_MED_H, mw)
            y = text_block(d, mx, my + 76, lines[:2], F_MED_H, INK, 15)
            dlines = wrap(d, deck, F_MED_D, mw)
            text_block(d, mx, y + 2, dlines[:2], F_MED_D, INK, 13)
            d.text((mx, my + 144), src, font=F_MED_S, fill=MUTED)

    # ---- also-on header
    d.text((12, 800), "ALSO ON TUESDAY 24 NOVEMBER \u2014 22 MORE STORIES",
           font=font("Bold", 12), fill=INK)
    hline(d, 12, W - 12, 818, width=1)

    # ---- map (left) + briefs (right, two columns)
    d.text((12, 826), "WHERE IT HAPPENED \u2014 numbers match the stories",
           font=font("Bold", 11), fill=RED)
    draw_map(d, 12, 844, 288, 124)
    col_w = 348
    for i, (num, head, src) in enumerate(BRIEFS):
        col = i // 11
        row = i % 11
        bx = 316 + col * (col_w + 8)
        by = 828 + row * 13
        tail = "  (%s)" % src
        prefix = "%s  %s" % (num, head)
        while d.textlength(prefix + tail, font=F_BRIEF) > col_w and len(prefix) > 12:
            prefix = prefix[:-1]
        d.text((bx, by), prefix + tail, font=F_BRIEF, fill=INK)

    # ---- date check
    dc_lines = wrap(d, DATE_CHECK, F_SMALL, W - 40)
    d.rectangle([12, 976, W - 12, 1010], outline=RED, width=2)
    text_block(d, 20, 980, dc_lines[:2], F_SMALL, DARKRED, 13)

    # ---- footer
    d.text((12, 1014), "Every story here happened, or was first reported, on "
                        "Tuesday 24 November 2026.", font=F_TINY, fill=INK)
    foot_r = "Sources named beside each story \u00b7 original drawings"
    d.text((W - 12 - d.textlength(foot_r, font=F_TINY), 1014), foot_r,
           font=F_TINY, fill=MUTED)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry.png")
    img = draw()
    img.save(out, format="PNG")
    print("wrote %s (%dx%d)" % (out, img.width, img.height))


if __name__ == "__main__":
    main()
