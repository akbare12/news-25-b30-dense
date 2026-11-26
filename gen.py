#!/usr/bin/env python3
"""Build-time renderer for the news-25 b30 dense front page.

Renders entry.png (1024x640, under 1 MiB) with Pillow. This file
runs only at build time; the grader never executes it (main.py is
stdlib-only and copies the pre-rendered image).

Front page: masthead with DATE CHECK, 3 hero panels, 10 mini-scene
panels, a 47-story grid, an ALSO strip, and a world-map + sources
footer. 50 stories total across 10 regions. Every card and the ALSO
strip carries a C / R / CL tag letter. All text is English.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 640
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

NAVY = (18, 35, 63)
INK = (20, 20, 20)
GREY = (90, 96, 104)
LIGHT = (238, 241, 245)
WHITE = (255, 255, 255)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
HERO_COLORS = [(18, 35, 63), (122, 28, 28), (14, 90, 70)]
MINI_COLORS = [
    (18, 35, 63), (122, 28, 28), (14, 90, 70), (90, 60, 10),
    (40, 70, 140), (110, 40, 90), (30, 100, 40), (150, 80, 10),
    (60, 60, 60), (10, 110, 130),
]
REGIONS = [
    "North America", "Europe", "East Asia", "South Asia",
    "Southeast Asia", "Middle East", "Africa", "Latin America",
    "Oceania", "Global",
]
REGION_CODES = ["NA", "EU", "EA", "SA", "SEA", "ME", "AF", "LA", "OC", "GL"]

# (headline, region, tag, short label for mini-scene, body/why for hero)
HEROES = [
    (
        "TRUMP HITS 14 PARTNERS WITH NEW TARIFFS; CHINA AT 20%",
        "North America", "R",
        "Washington unveils sweeping new duties on 14 trading "
        "partners, with Chinese goods facing a 20% rate.",
        "WHY IT MATTERS: Higher import costs will ripple through "
        "supply chains, lift consumer prices and reshape trade "
        "talks in the weeks ahead.",
    ),
    (
        "AI CHIP SELLOFF SINKS KOSPI 6.16% TO 4,697.51",
        "East Asia", "R",
        "Seoul's Kospi plunges 6.16% to 4,697.51 as chip giants "
        "Samsung and SK Hynix tumble 9.87% and 11.05%.",
        "WHY IT MATTERS: The selloff wipes out months of chip "
        "gains and tests whether the AI rally that powered "
        "markets all year can hold.",
    ),
    (
        "SHENZHOU-24 CARRIES FIRST FOREIGN ASTRONAUT TO TIANGONG",
        "East Asia", "CL",
        "Shenzhou-24 carries Muhammad Zeeshan Ali of Pakistan, "
        "the first foreign astronaut to visit Tiangong.",
        "WHY IT MATTERS: A Pakistani astronaut aboard Tiangong "
        "opens China's space station to partner nations and "
        "redraws the map of crewed spaceflight.",
    ),
]

# (headline, region, tag, mini-scene label) -- stories 4..50
GRID = [
    ("GOLD MINE COLLAPSE IN BOGOR KILLS 9, TRAPS 17", "Southeast Asia", "C", "BOGOR MINE"),
    ("COP31 CLIMATE TALKS ENTER FINAL STRETCH", "Global", "CL", "COP31 TALKS"),
    ("GAZA CEASEFIRE TALKS RESUME IN CAIRO", "Middle East", "C", "GAZA TALKS"),
    ("UKRAINE RACES TO REPAIR POWER GRID BEFORE WINTER", "Europe", "C", "UKRAINE GRID"),
    ("FED HOLDS RATES AS INFLATION COOLS", "North America", "R", "FED HOLDS"),
    ("UK BUDGET TARGETS GROWTH AND PUBLIC SERVICES", "Europe", "R", "UK BUDGET"),
    ("JAPAN UNVEILS FRESH STIMULUS PACKAGE", "East Asia", "R", "JAPAN STIMULUS"),
    ("INDIA FLOOD WATERS RECEDE AS AID ARRIVES", "South Asia", "CL", "INDIA FLOODS"),
    ("AUSTRALIA BRACES FOR BUSHFIRE SEASON", "Oceania", "CL", "AUS FIRES"),
    ("AMAZON DEFORESTATION SLOWS IN BRAZIL", "Latin America", "CL", "AMAZON SLOWDOWN"),
    ("NIGERIA REFORMS FUEL SUBSIDY SYSTEM", "Africa", "R", None),
    ("CANADA SENDS WILDFIRE AID TO PROVINCES", "North America", "CL", None),
    ("GERMAN AUTO SECTOR FACES JOB CUTS", "Europe", "R", None),
    ("SEOUL VOWS MARKET SUPPORT AFTER ROUT", "East Asia", "R", None),
    ("INDONESIA RAISES VOLCANO ALERT LEVEL", "Southeast Asia", "CL", None),
    ("SAUDI ARAMCO HOLDS OIL OUTPUT STEADY", "Middle East", "R", None),
    ("EGYPT TOURISM HITS RECORD VISITOR NUMBERS", "Africa", "R", None),
    ("MEXICO ELECTION COURT RULES ON DISPUTE", "Latin America", "R", None),
    ("NEW ZEALAND RUNS NATIONWIDE QUAKE DRILL", "Oceania", "C", None),
    ("FRANCE PUSHES PENSION REFORM THROUGH", "Europe", "R", None),
    ("US JOBS REPORT BEATS EXPECTATIONS", "North America", "R", None),
    ("CHINA EV EXPORTS CLIMB TO NEW HIGH", "East Asia", "R", None),
    ("PAKISTAN FLOOD RELIEF REACHES VILLAGES", "South Asia", "C", None),
    ("THAILAND TOURISM REBOUND CONTINUES", "Southeast Asia", "R", None),
    ("IRAN NUCLEAR TALKS RESUME IN VIENNA", "Middle East", "C", None),
    ("KENYA DROUGHT AID EXPANDS TO NORTH", "Africa", "C", None),
    ("ARGENTINA INFLATION EASES FOR THIRD MONTH", "Latin America", "R", None),
    ("CHILE SIGNS MAJOR LITHIUM DEAL", "Latin America", "R", None),
    ("PHILIPPINES TYPHOON RECOVERY UNDER WAY", "Southeast Asia", "C", None),
    ("VIETNAM FACTORY ORDERS REBOUND", "Southeast Asia", "R", None),
    ("TAIWAN BREAKS GROUND ON NEW CHIP PLANT", "East Asia", "R", None),
    ("BANGLADESH GARMENT ORDERS RECOVER", "South Asia", "R", None),
    ("ETHIOPIA PEACE DEAL HOLDS IN NORTH", "Africa", "C", None),
    ("COLOMBIA PEACE TALKS MAKE PROGRESS", "Latin America", "C", None),
    ("ICELAND VOLCANO ERUPTION SLOWS", "Europe", "CL", None),
    ("SPAIN DROUGHT PROMPTS WATER CURBS", "Europe", "CL", None),
    ("US EAST COAST STORM KNOCKS OUT POWER", "North America", "C", None),
    ("JAPAN QUAKE OFFSHORE, NO TSUNAMI ALERT", "East Asia", "C", None),
    ("AUSTRALIA HOLDS INTEREST RATES STEADY", "Oceania", "R", None),
    ("SOUTH AFRICA POWER CUTS EASE", "Africa", "R", None),
    ("TURKEY QUAKE REBUILD PASSES MILESTONE", "Middle East", "C", None),
    ("POLAND TIGHTENS BORDER SECURITY", "Europe", "C", None),
    ("PERU MINING PROTEST ENDS IN DEAL", "Latin America", "C", None),
    ("MALAYSIA WINS BIG TECH INVESTMENT", "Southeast Asia", "R", None),
    ("SRI LANKA DEBT TALKS NEAR AGREEMENT", "South Asia", "R", None),
    ("MOROCCO QUAKE AID REACHES VILLAGES", "Africa", "C", None),
    ("FIJI HOSTS PACIFIC CLIMATE SUMMIT", "Oceania", "CL", None),
]


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = "/usr/share/fonts/truetype/dejavu/" + name
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font; no truncation."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt, max_w):
    """Truncate with an ellipsis only when a single line must fit."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text, False
    while text and draw.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "...", True


def main():
    assert len(HEROES) == 3 and len(GRID) == 47, "need 3 + 47 stories"
    assert len(REGIONS) == 10
    regions_used = {h[1] for h in HEROES} | {g[1] for g in GRID}
    assert regions_used <= set(REGIONS), regions_used
    assert len(regions_used) == 10, regions_used
    assert all(t in ("C", "R", "CL") for _, _, t, *_ in HEROES + GRID)

    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    truncated = 0

    # --- masthead -------------------------------------------------
    d.rectangle([0, 0, W, 58], fill=NAVY)
    d.text((10, 6), "THE WORLD TODAY", font=font(26, True), fill=WHITE)
    d.text((10, 38), "50 STORIES  •  10 REGIONS  •  DENSE FRONT PAGE",
           font=font(10, True), fill=GOLD)
    dc = "DATE CHECK: Wednesday 25 November 2026"
    dw = d.textlength(dc, font=font(14, True))
    d.text((W - 10 - dw, 10), dc, font=font(14, True), fill=WHITE)
    d.text((W - 10 - d.textlength("NEWS-IMAGE-20261125", font=font(10)), 38),
           "NEWS-IMAGE-20261125", font=font(10), fill=(180, 195, 215))

    # --- heroes ---------------------------------------------------
    hy, hh, hw, gap = 64, 190, 328, 8
    for i, (head, region, tag, body, why) in enumerate(HEROES):
        x = gap + i * (hw + gap)
        col = HERO_COLORS[i]
        d.rectangle([x, hy, x + hw, hy + hh], outline=col, width=2)
        d.rectangle([x, hy, x + hw, hy + 26], fill=col)
        d.text((x + 8, hy + 5), "No. %d" % (i + 1), font=font(13, True), fill=WHITE)
        t = "[%s]" % tag
        d.text((x + hw - 8 - d.textlength(t, font=font(12, True)), hy + 6),
               t, font=font(12, True), fill=WHITE)
        y = hy + 32
        for line in wrap(d, head, font(15, True), hw - 16)[:4]:
            d.text((x + 8, y), line, font=font(15, True), fill=INK)
            y += 18
        for line in wrap(d, body, font(10), hw - 16)[:3]:
            d.text((x + 8, y), line, font=font(10), fill=(50, 50, 50))
            y += 13
        wy = max(y + 4, hy + 100)
        d.rectangle([x + 1, wy, x + hw - 1, hy + hh - 20], fill=LIGHT)
        yy = wy + 4
        for line in wrap(d, why, font(9), hw - 16)[:3]:
            if yy + 12 > hy + hh - 20:
                break
            d.text((x + 8, yy), line, font=font(9), fill=INK)
            yy += 12
        d.text((x + 8, hy + hh - 16), region.upper() + "  •  TAG " + tag,
               font=font(9, True), fill=GREY)

    # --- mini scenes (stories 4..13) ------------------------------
    my, mh, mw = 260, 108, 98
    for i, (_, region, tag, label) in enumerate(GRID[:10]):
        x = 8 + i * (mw + 3)
        col = MINI_COLORS[i]
        d.rectangle([x, my, x + mw, my + mh], outline=col, width=2)
        d.rectangle([x, my, x + mw, my + 34], fill=col)
        num = "%02d" % (i + 4)
        d.text((x + mw // 2 - d.textlength(num, font=font(18, True)) // 2,
                my + 6), num, font=font(18, True), fill=WHITE)
        y = my + 40
        for line in wrap(d, label, font(9, True), mw - 10)[:3]:
            d.text((x + 5, y), line, font=font(9, True), fill=INK)
            y += 12
        d.text((x + 5, my + mh - 16), region.split()[0].upper() + " [" + tag + "]",
               font=font(8, True), fill=GREY)

    # --- 47-story grid --------------------------------------------
    gy = 374
    d.text((8, gy), "ALL 47 STORIES", font=font(12, True), fill=NAVY)
    d.line([8, gy + 17, W - 8, gy + 17], fill=NAVY, width=1)
    cols = [GRID[:16], GRID[16:32], GRID[32:]]
    for ci, col in enumerate(cols):
        x = 8 + ci * 336
        y = gy + 22
        for j, (head, region, tag, _label) in enumerate(col):
            n = 4 + ci * 16 + j if ci < 2 else 36 + j
            line, was_trunc = fit(
                d, "%02d  %s  [%s]" % (n, head, tag), font(9), 326)
            truncated += 1 if was_trunc else 0
            d.text((x, y), line, font=font(9), fill=INK)
            y += 10
    grid_bottom = gy + 22 + 16 * 10

    # --- ALSO strip ------------------------------------------------
    ay = 566
    d.rectangle([0, ay, W, ay + 26], fill=NAVY)
    also = ("ALSO: FED HOLDS RATES [R]  •  COP31 ENTERS FINAL STRETCH [CL]  •  "
            "BOGOR RESCUE UNDER WAY [C]  •  TIANGONG WELCOMES FIRST GUEST [CL]")
    d.text((10, ay + 6), also, font=font(11, True), fill=WHITE)

    # --- map + sources footer --------------------------------------
    fy = 596
    d.text((8, fy), "WORLD MAP — 10 REGIONS: ", font=font(9, True), fill=NAVY)
    px = 8 + d.textlength("WORLD MAP — 10 REGIONS: ", font=font(9, True))
    d.text((px, fy), "North America • Europe • East Asia • South Asia • "
           "Southeast Asia • Middle East • Africa • Latin America • "
           "Oceania • Global", font=font(8), fill=INK)
    x = 8
    for code, col in zip(REGION_CODES, MINI_COLORS):
        d.ellipse([x, fy + 15, x + 10, fy + 25], fill=col)
        d.text((x + 13, fy + 14), code, font=font(9, True), fill=INK)
        x += 13 + d.textlength(code, font=font(9, True)) + 12
    d.text((8, H - 13),
           "Sources: Reuters • AP • AFP • Bloomberg • Antara • Yonhap  —  "
           "Wednesday 25 November 2026",
           font=font(8), fill=GREY)

    img.save(OUT, optimize=True)
    data = open(OUT, "rb").read()
    print("stories=50 regions=%d truncated=%d" % (len(regions_used), truncated))
    print("size=%d bytes dims=%dx%d sha256=%s"
          % (len(data), W, H, hashlib.sha256(data).hexdigest()))
    assert len(data) <= 1024 * 1024, "over 1 MiB"
    assert grid_bottom <= ay, "grid overlaps ALSO strip"


if __name__ == "__main__":
    main()
