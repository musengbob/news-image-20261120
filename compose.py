#!/usr/bin/env python3
"""Render THE WORLD TODAY - a dense newspaper front page summing up
Friday 20 November 2026, as a 1024x1024 PNG for make.fun news-image-20261120.

Drawn entirely with Pillow: masthead, lead story, world map made from a
hand-built land grid, and a 4-column grid of 32 further stories.
Run:  python3 compose.py   (writes entry.png beside this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (246, 241, 229)      # warm newsprint
INK = (20, 18, 16)          # near-black ink
SOFT = (74, 70, 62)         # grey-brown for decks
RED = (163, 22, 33)         # single accent red
RULE = (20, 18, 16)
MAPINK = (52, 50, 44)       # dotted-map ink

F = {
    "mast": ImageFont.truetype(os.path.join(HERE, "fonts", "pf900-sub.ttf"), 78),
    "lead": ImageFont.truetype(os.path.join(HERE, "fonts", "pf700-sub.ttf"), 40),
    "sub": ImageFont.truetype(os.path.join(HERE, "fonts", "pf700-sub.ttf"), 23),
    "kick": ImageFont.truetype(os.path.join(HERE, "fonts", "lf900-sub.ttf"), 12),
    "kick_sm": ImageFont.truetype(os.path.join(HERE, "fonts", "lf900-sub.ttf"), 10),
    "head": ImageFont.truetype(os.path.join(HERE, "fonts", "lf700-sub.ttf"), 14),
    "dek": ImageFont.truetype(os.path.join(HERE, "fonts", "lf400-sub.ttf"), 11),
    "dek_sm": ImageFont.truetype(os.path.join(HERE, "fonts", "lf400-sub.ttf"), 11),
    "lead_dek": ImageFont.truetype(os.path.join(HERE, "fonts", "lf400-sub.ttf"), 15),
    "small": ImageFont.truetype(os.path.join(HERE, "fonts", "lf400-sub.ttf"), 10),
    "tiny": ImageFont.truetype(os.path.join(HERE, "fonts", "lf700-sub.ttf"), 10),
    "maplab": ImageFont.truetype(os.path.join(HERE, "fonts", "lf700-sub.ttf"), 11),
    "pin": ImageFont.truetype(os.path.join(HERE, "fonts", "lf900-sub.ttf"), 11),
}

# ---------------------------------------------------------------- stories
# (number, place, kicker, headline, deck) -- 34 stories, all reported
# on 20 November 2026 or first reported that day in some time zone.
LEAD = (
    "WASHINGTON",
    "TRUMP PUTS IRAN WAR DECISION OFF TO 2027",
    "The president says he will \u201csee what happens\u201d after Jan 1, pushing any "
    "call on military action into next year as the Gulf war grinds on and "
    "fuel prices climb at home.",
)
SUMMIT = (
    "SHENZHEN",
    "THREE AT ONE TABLE",
    "Trump, Xi and Putin hold the first-ever trilateral summit: 80 minutes, "
    "a four-point \u201cpeace declaration\u201d and talks on nuclear risk \u2014 but no "
    "breakthrough on Ukraine or Iran.",
)
GRID = [
    ("KYIV", "WORLD", "RUSSIAN STRIKES DAMAGE DUTCH AND AUSTRIAN EMBASSIES",
     "Two EU missions hit in the capital."),
    ("THE HAGUE", "WORLD", "MYANMAR COMMITTED GENOCIDE, TOP UN COURT RULES",
     "Intent to destroy the Rohingya found."),
    ("BRUSSELS", "EUROPE", "EUROPE READY FOR TALKS WITH RUSSIA ON ENDING WAR",
     "Leaders signal openness to negotiations."),
    ("CRIMEA", "WORLD", "UKRAINE HITS CRIMEAN BRIDGE WITH RUTA MISSILES",
     "Rail traffic to the peninsula halted."),
    ("RIYADH", "MIDDLE EAST", "HOUTHIS STRIKE RIYADH; WEALTH-FUND TOWER DAMAGED",
     "Attack hits the Saudi fund\u2019s tower."),
    ("WASHINGTON", "AMERICAS", "US AND VENEZUELA RESTORE MILITARY COOPERATION",
     "The two sides sign a deal to resume ties."),
    ("BLACK SEA", "WORLD", "LPG TANKER SUNK OFF BULGARIA \u2018HIT BY PROJECTILES\u2019",
     "Officials say the vessel was struck."),
    ("VIENNA", "WORLD", "NORTH KOREA EXPANDING YONGBYON SITE, IAEA SAYS",
     "Watchdog reports growth at the plant."),
    ("SEOUL", "ASIA", "TOP COURT OVERTURNS EX-PM HAN\u2019S CONVICTION",
     "Han Duck-soo cleared over the 2024 bid."),
    ("TOKYO", "ASIA", "TAKAICHI SEEKS CONTINUED DIALOGUE WITH CHINA",
     "Japan\u2019s PM moves to ease tensions."),
    ("CANBERRA", "ASIA", "AUSTRALIA SANCTIONS ISRAELI SETTLERS",
     "Measures target West Bank expansion."),
    ("ODISHA", "ASIA", "CYCLONE AKVAN: 300,000 EVACUATED AS LANDFALL NEARS",
     "Rescue teams deploy as the storm nears."),
    ("SUVA", "PACIFIC", "FIJI DECLARES NATIONAL DISASTER AS DROUGHT BITES",
     "El Ni\u00f1o shortages prompt the order."),
    ("DHAKA", "ASIA", "FIRE AT YUNUS ANCESTRAL HOME; ARSON SUSPECTED",
     "Blaze at the ex-leader\u2019s family house."),
    ("NEW DELHI", "ASIA", "PAKISTAN MINISTER TO LEAD DELEGATION TO DELHI",
     "Team to attend the SCO dialogue forum."),
    ("NEW DELHI", "INDIA", "US COURT ORDERS SUMMONSES FOR DOVAL, GOEL",
     "Summonses via Delhi courts, judge rules."),
    ("NEW DELHI", "INDIA", "MODI MEETS PRINCE AND PRINCESS OF WALES",
     "Talks cover India-UK ties and strategy."),
    ("NEW DELHI", "INDIA", "MODI OPENS FICCI CENTENARY, EYES 2047 GROWTH",
     "PM opens the industry body\u2019s 100th year."),
    ("NEW DELHI", "BUSINESS", "INDIA SIGNS \u20b91,976-CRORE NAVY MISSILE DEAL",
     "Barak upgrade pact with Israel Aerospace."),
    ("MUMBAI", "BUSINESS", "SENSEX UP 1.21% AS AUTO, BANK STOCKS RALLY",
     "Nifty gains 1.14% in a strong session."),
    ("SAN FRANCISCO", "TECH", "ANTHROPIC VALUATION REPORTED AT $1.5 TRILLION",
     "The AI boom keeps lifting valuations."),
    ("SHENZHEN", "BUSINESS", "APEC LEADERS TALK TRADE AS XI URGES OPEN MARKETS",
     "Asia-Pacific summit weighs trade and tech."),
    ("ANKARA", "CLIMATE", "COP31: INDIA PRESSES FOR CLIMATE FINANCE",
     "New Delhi pushes funding for resilience."),
    ("SPACE", "SCIENCE", "VOYAGER 1 PASSES \u2018LIGHT-DAY\u2019 MILESTONE, NASA SAYS",
     "The probe flies farther than any craft."),
    ("TOKYO", "SCIENCE", "HAYABUSA2 ENGINE FAULT ENDS ASTEROID LANDING PLAN",
     "Japan\u2019s probe changes course after trouble."),
    ("LOS ANGELES", "CULTURE", "GTA 6 SALES PASS THE ODYSSEY\u2019S $1.8BN RUN",
     "Rockstar\u2019s hit tops the year\u2019s top film."),
    ("MOUNTAIN VIEW", "TECH", "GOOGLE\u2019S GEMINI 4 NEON ROLLS OUT TO AI PRO USERS",
     "Newest Gemini 4 model reaches paid tiers."),
    ("WELLINGTON", "SPORT", "NICHOLLS 113* RESCUES NZ IN FIRST TEST VS INDIA",
     "NZ reach 243 for 5 on day one."),
    ("HONG KONG", "SPORT", "INDIA BEAT MALAYSIA IN HONG KONG OPEN BADMINTON",
     "Indian shuttlers advance on day one."),
    ("NEW DELHI", "SPORT", "WOMEN\u2019S ASIAN HOCKEY CHAMPIONS TROPHY BEGINS",
     "The continental tournament opens."),
    ("UNITED NATIONS", "WORLD", "WORLD CHILDREN\u2019S DAY MARKED AROUND THE GLOBE",
     "20 November: a day for children\u2019s rights."),
    ("KHARTOUM", "WORLD", "SUDAN\u2019S WAR GRINDS ON AS THREAT INDEX STAYS SEVERE",
     "Monitors list it among active conflicts."),
]
assert len(GRID) == 32, len(GRID)

# ------------------------------------------------------------ world map
# Hand-built land grid: rows 0..44 run 84N to 48S in 3-degree steps,
# columns 0..95 run 180W to 180E in 3.75-degree steps. Each entry is
# (row, col_start, col_end) of a land run.
LAND = [
    (0, 24, 28), (0, 34, 38),
    (1, 20, 30), (1, 33, 40),
    (2, 14, 31), (2, 33, 41),
    (3, 8, 31), (3, 33, 41), (3, 56, 90),
    (4, 6, 32), (4, 33, 41), (4, 55, 92),
    (5, 5, 33), (5, 34, 41), (5, 52, 93),
    (6, 4, 34), (6, 35, 41), (6, 50, 94),
    (7, 5, 34), (7, 36, 41), (7, 46, 94),
    (8, 6, 33), (8, 36, 40), (8, 42, 44), (8, 45, 95),
    (9, 8, 32), (9, 45, 95),
    (10, 10, 31), (10, 44, 95),
    (11, 12, 30), (11, 44, 94),
    (12, 13, 29), (12, 44, 93),
    (13, 14, 28), (13, 44, 92),
    (14, 15, 28), (14, 45, 91),
    (15, 16, 28), (15, 45, 90),
    (16, 17, 27), (16, 44, 89),
    (17, 18, 27), (17, 44, 88),
    (18, 19, 27), (18, 43, 87),
    (19, 20, 27), (19, 43, 80),
    (20, 21, 28), (20, 43, 79),
    (21, 22, 28), (21, 44, 78),
    (22, 23, 29), (22, 44, 77),
    (23, 24, 30), (23, 45, 76),
    (24, 25, 31), (24, 45, 75),
    (25, 26, 32), (25, 44, 61), (25, 68, 69), (25, 74, 76),
    (26, 27, 32), (26, 44, 60), (26, 74, 79),
    (27, 27, 32), (27, 50, 59), (27, 73, 76), (27, 77, 80),
    (28, 28, 33), (28, 49, 58), (28, 72, 81), (28, 82, 86),
    (29, 28, 33), (29, 49, 58), (29, 72, 80), (29, 83, 88),
    (30, 28, 34), (30, 49, 57), (30, 74, 79), (30, 84, 88),
    (31, 28, 38), (31, 49, 57), (31, 84, 87),
    (32, 28, 38), (32, 49, 56), (32, 85, 87),
    (33, 29, 37), (33, 50, 56),
    (34, 29, 36), (34, 50, 55),
    (35, 29, 35), (35, 51, 54), (35, 76, 85),
    (36, 29, 34), (36, 51, 54), (36, 76, 86),
    (37, 29, 33), (37, 52, 55), (37, 75, 87),
    (38, 28, 32), (38, 52, 55), (38, 75, 87),
    (39, 28, 31), (39, 52, 55), (39, 76, 86),
    (40, 28, 31), (40, 53, 55), (40, 77, 84),
    (41, 28, 30), (41, 78, 82),
    (42, 28, 30), (42, 80, 81),
    (43, 28, 29),
    (44, 28, 29),
]
# (number, grid col, grid row, label) -- pins mark 8 of the 34 stories.
PINS = [
    (1, 27, 15, "WASHINGTON"),
    (2, 78, 20, "SHENZHEN"),
    (3, 56, 11, "KYIV"),
    (4, 49, 10, "THE HAGUE"),
    (5, 71, 21, "ODISHA"),
    (6, 60, 20, "RIYADH"),
    (7, 90, 41, "WELLINGTON"),
    (8, 92, 34, "SUVA"),
]
MAP_LABELS = [
    ("NORTH AMERICA", 8, 11), ("GREENLAND", 30, 5),
    ("SOUTH AMERICA", 24, 30), ("EUROPE", 43, 6),
    ("AFRICA", 48, 24), ("ASIA", 70, 9), ("AUSTRALIA", 76, 38),
]

# ---------------------------------------------------------------- helpers
def wrap(draw, text, font, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, y, text, font, fill=INK, x0=0, x1=W):
    w = draw.textlength(text, font=font)
    draw.text(((x0 + x1 - w) / 2, y), text, font=font, fill=fill)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 24                      # side margin
    RX = W - MX                  # right edge

    # ---- top bar ------------------------------------------------------
    d.rectangle([0, 0, W, 24], fill=INK)
    d.text((MX, 5), "FRIDAY, 20 NOVEMBER 2026", font=F["kick_sm"], fill=PAPER)
    right = "34 STORIES  \u2022  ONE DAY  \u2022  EVERY CONTINENT"
    d.text((RX - d.textlength(right, font=F["kick_sm"]), 5), right,
           font=F["kick_sm"], fill=PAPER)

    # ---- masthead -----------------------------------------------------
    draw_center(d, 30, "THE WORLD TODAY", F["mast"])
    d.line([(MX, 122), (RX, 122)], fill=RULE, width=2)
    d.line([(MX, 126), (RX, 126)], fill=RULE, width=1)
    sub = ("THE DAY\u2019S NEWS FROM EVERY CONTINENT  \u2014  "
           "WASHINGTON  \u2022  SHENZHEN  \u2022  KYIV  \u2022  NEW DELHI  \u2022  WELLINGTON")
    draw_center(d, 133, sub, F["small"], fill=SOFT)

    # ---- lead band ----------------------------------------------------
    y = 158
    lead_x, lead_w = MX, 648
    d.text((lead_x, y), LEAD[0] + "  \u2014  THE IRAN DECISION", font=F["kick"], fill=RED)
    y += 18
    lines = wrap(d, LEAD[1], F["lead"], lead_w)
    for ln in lines[:2]:
        d.text((lead_x, y), ln, font=F["lead"], fill=INK)
        y += 42
    y += 2
    for ln in wrap(d, LEAD[2], F["lead_dek"], lead_w):
        d.text((lead_x, y), ln, font=F["lead_dek"], fill=SOFT)
        y += 19
    lead_bottom = y

    # summit box, right of the lead
    sx = lead_x + lead_w + 22
    sw = RX - sx
    d.line([(sx - 11, 158), (sx - 11, lead_bottom)], fill=RULE, width=1)
    sy = 158
    d.text((sx, sy), SUMMIT[0] + "  \u2014  THE SUMMIT", font=F["kick"], fill=RED)
    sy += 18
    for ln in wrap(d, SUMMIT[1], F["sub"], sw):
        d.text((sx, sy), ln, font=F["sub"], fill=INK)
        sy += 26
    sy += 2
    for ln in wrap(d, SUMMIT[2], F["dek_sm"], sw):
        d.text((sx, sy), ln, font=F["dek_sm"], fill=SOFT)
        sy += 14

    # ---- map band -----------------------------------------------------
    my = 296
    d.line([(MX, my), (RX, my)], fill=RULE, width=2)
    d.text((MX, my + 8), "THE DAY ON THE MAP", font=F["kick"], fill=INK)
    d.text((RX - d.textlength("WHERE THE NEWS HAPPENED", font=F["kick_sm"]), my + 9),
           "WHERE THE NEWS HAPPENED", font=F["kick_sm"], fill=SOFT)
    map_x0, map_y0 = MX, my + 30
    map_w, map_h = RX - MX, 150
    cw, ch = map_w / 96.0, map_h / 45.0
    # dotted land: one small dot per land cell, so the map reads light
    for (r, c0, c1) in LAND:
        for c in range(c0, c1 + 1):
            cx = map_x0 + (c + 0.5) * cw
            cy = map_y0 + (r + 0.5) * ch
            d.ellipse([cx - 3.4, cy - 1.5, cx + 3.4, cy + 1.5], fill=MAPINK)
    for (label, c, r) in MAP_LABELS:
        d.text((map_x0 + c * cw, map_y0 + r * ch), label,
               font=F["maplab"], fill=PAPER,
               stroke_width=2, stroke_fill=MAPINK)
    for (num, c, r, _lab) in PINS:
        px = map_x0 + (c + 0.5) * cw
        py = map_y0 + (r + 0.5) * ch
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=PAPER, width=1)
        t = str(num)
        d.text((px - d.textlength(t, font=F["pin"]) / 2, py - 6), t,
               font=F["pin"], fill=(255, 255, 255))
    leg_y = map_y0 + map_h + 6
    legend = ("  ".join(f"{n} {lab}" for (n, _c, _r, lab) in PINS))
    draw_center(d, leg_y, legend, F["tiny"], fill=SOFT)
    grid_top = leg_y + 18

    # ---- story grid ---------------------------------------------------
    d.line([(MX, grid_top), (RX, grid_top)], fill=RULE, width=2)
    cols, rows = 4, 8
    gutter = 14
    col_w = (RX - MX - gutter * (cols - 1)) // cols
    row_h = 60
    for i, (place, section, head, dek) in enumerate(GRID):
        col, row = i % cols, i // cols
        x = MX + col * (col_w + gutter)
        yy = grid_top + 8 + row * row_h
        # thin rule above each cell except the first row
        if row:
            d.line([(x, yy - 6), (x + col_w, yy - 6)], fill=(200, 192, 172), width=1)
        d.text((x, yy), f"{i + 3}.  {place}  \u2014  {section}",
               font=F["kick_sm"], fill=RED)
        hy = yy + 13
        hlines = wrap(d, head, F["head"], col_w)
        for ln in hlines[:2]:
            d.text((x, hy), ln, font=F["head"], fill=INK)
            hy += 16
        for ln in wrap(d, dek, F["dek"], col_w)[:1]:
            d.text((x, hy), ln, font=F["dek"], fill=SOFT)
            hy += 13

    # ---- footer -------------------------------------------------------
    d.line([(MX, H - 26), (RX, H - 26)], fill=RULE, width=1)
    draw_center(d, H - 20,
                "THE WORLD TODAY  \u2022  FRIDAY 20 NOVEMBER 2026  \u2022  "
                "WORLD  \u2022  EUROPE  \u2022  ASIA  \u2022  MIDDLE EAST  \u2022  "
                "BUSINESS  \u2022  TECH  \u2022  SCIENCE  \u2022  SPORT",
                F["small"], fill=SOFT)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
