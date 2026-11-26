#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""build_poster.py — author the v4 front page for news-image-20261126.

"The World in One Day — Thursday 26 November 2026": 36 verified stories
(SOURCES.md), 13 of them drawn as flat SVG scene panels, a dot-matrix
world map with 13 numbered pins, a UTC timeline, per-story status chips,
a by-the-numbers band of the day's own figures, and an itemised date
check. Emits poster.svg (a build artifact; generate.mjs renders it to
entry.png with Chromium). The competition program main.ts only delivers
entry.png — it renders nothing.

Written fresh in the main chat session on 2026-11-26 for the v4 push:
v3 (951518) was text-only; the board's top five all carry drawn scenes,
a pinned map and a timeline, so v4 restores those and adds the fidelity
apparatus (status chips, deks, itemised date check) they print.
"""
import html

W, H = 1024, 1024
PAPER = "#FAF5EA"
INK = "#1B1B1B"
MUTE = "#5A544A"
RED = "#C1272D"
DARK = "#22252A"
RULE = "#C9BFA9"

STATUS_COLORS = {
    "CONFIRMED": "#1E7A46",
    "OFFICIAL": "#20509E",
    "REPORTED": "#8A5D00",
    "CLAIM": "#7D3C98",
    "ONGOING": "#C1272D",
}

def esc(s):
    return html.escape(s, quote=True)

def text(x, y, s, size, fill=INK, weight="normal", anchor="start",
         family="Arial, sans-serif", spacing=None, style=""):
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    st = f' style="{style}"' if style else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{sp}{st}>'
            f'{esc(s)}</text>')

def chip(x, y, label):
    """Status chip: small filled rounded rect with white bold label."""
    w = 8 + len(label) * 5.6
    c = STATUS_COLORS[label]
    return (f'<g><rect x="{x}" y="{y}" width="{w:.0f}" height="13" rx="2.5" fill="{c}"/>'
            f'<text x="{x + w/2:.0f}" y="{y + 9.5}" font-family="Arial, sans-serif" '
            f'font-size="8" font-weight="bold" fill="#FFFFFF" text-anchor="middle">'
            f'{esc(label)}</text></g>', w)

# ---------------------------------------------------------------- scenes
# Each scene draws inside a 100x100 local box; scene() scales it into
# place over a tinted backdrop. Flat shapes only, 2-4 colours per scene.

def _balloon():
    return ('<circle cx="50" cy="34" r="24" fill="#C1272D"/>'
            '<path d="M38 16 a24 24 0 0 1 8 -5 v46 a24 24 0 0 1 -8 -5 z" fill="#E8A13A"/>'
            '<path d="M62 16 a24 24 0 0 0 -8 -5 v46 a24 24 0 0 0 8 -5 z" fill="#20509E"/>'
            '<path d="M42 55 L47 72 M58 55 L53 72" stroke="#5A544A" stroke-width="1.6"/>'
            '<rect x="44" y="72" width="12" height="8" fill="#8A5A2B"/>'
            '<path d="M8 84 q6 -6 12 0 q6 6 12 0 M64 88 q6 -6 12 0 q6 6 12 0" stroke="#7FA6C9" stroke-width="2" fill="none"/>'
            '<path d="M6 22 h14 M2 30 h10" stroke="#A33" stroke-width="2"/>')

def _mumbai():
    return ('<path d="M22 78 V38 h8 v-8 h40 v8 h8 v40 h-20 V58 a8 10 0 0 0 -16 0 v20 z" fill="#8A5A2B"/>'
            '<rect x="18" y="78" width="64" height="5" fill="#5A4632"/>'
            '<g fill="#E8A13A"><path d="M34 92 c-3 -4 3 -6 0 -10 c4 3 5 7 0 10z"/>'
            '<path d="M50 92 c-3 -4 3 -6 0 -10 c4 3 5 7 0 10z"/>'
            '<path d="M66 92 c-3 -4 3 -6 0 -10 c4 3 5 7 0 10z"/></g>'
            '<g fill="#3A3A3A"><rect x="32.8" y="92" width="2.4" height="5"/>'
            '<rect x="48.8" y="92" width="2.4" height="5"/><rect x="64.8" y="92" width="2.4" height="5"/></g>')

def _chess():
    sq = ''.join(f'<rect x="{18 + (i % 4) * 16}" y="{78 + (i // 4) * 8}" width="16" height="8" fill="{"#1B1B1B" if (i + (i // 4)) % 2 else "#E8E0CC"}"/>' for i in range(8))
    return ('<path d="M50 12 l4 8 h-8 z M44 22 h12 l-2 6 h-8 z" fill="#1B1B1B"/>'
            '<path d="M38 34 q12 -8 24 0 l-3 22 q-9 5 -18 0 z" fill="#1B1B1B"/>'
            '<rect x="34" y="58" width="32" height="6" fill="#1B1B1B"/>'
            '<rect x="30" y="66" width="40" height="6" rx="2" fill="#1B1B1B"/>' + sq)

def _tanker():
    return ('<path d="M6 66 h88 l-8 14 H16 z" fill="#37424E"/>'
            '<rect x="16" y="56" width="16" height="10" fill="#C1272D"/>'
            '<rect x="34" y="56" width="16" height="10" fill="#20509E"/>'
            '<rect x="52" y="56" width="16" height="10" fill="#E8A13A"/>'
            '<rect x="74" y="46" width="10" height="20" fill="#D8D2C2"/>'
            '<path d="M79 30 c-6 8 4 10 0 16 c8 -4 8 -12 0 -16z" fill="#E8641E"/>'
            '<path d="M4 88 q8 -6 16 0 q8 6 16 0 q8 -6 16 0 q8 6 16 0 q8 -6 16 0 q8 6 12 2" stroke="#20509E" stroke-width="2.4" fill="none"/>')

def _odesa():
    return ('<g fill="#37424E"><rect x="8" y="44" width="14" height="38"/>'
            '<rect x="26" y="34" width="12" height="48"/><rect x="42" y="50" width="16" height="32"/>'
            '<rect x="62" y="28" width="12" height="54"/><rect x="78" y="42" width="14" height="40"/></g>'
            '<g stroke="#E8641E" stroke-width="2.4"><path d="M70 8 v10 M70 26 v4 M62 12 l5 7 M78 12 l-5 7 M60 22 h6 M74 22 h6"/></g>'
            '<circle cx="70" cy="18" r="4.5" fill="#E8A13A"/>'
            '<path d="M30 20 q6 -8 14 -4 q-4 8 -12 8 q-4 0 -2 -4z" fill="#9AA3AB"/>'
            '<rect x="4" y="82" width="92" height="4" fill="#5A4632"/>')

def _leakdoc():
    return ('<rect x="28" y="8" width="44" height="84" rx="2" fill="#FFFFFF" stroke="#B9AE94"/>'
            '<g fill="#1B1B1B"><rect x="34" y="20" width="32" height="6"/>'
            '<rect x="34" y="32" width="32" height="6"/><rect x="34" y="44" width="20" height="6"/>'
            '<rect x="34" y="56" width="32" height="6"/><rect x="34" y="68" width="26" height="6"/></g>'
            '<text x="50" y="40" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#C1272D" text-anchor="middle" transform="rotate(-24 50 50)">LEAK</text>')

def _drone():
    return ('<g stroke="#37424E" stroke-width="3"><path d="M32 30 L68 54 M68 30 L32 54"/></g>'
            '<g fill="none" stroke="#20509E" stroke-width="2.4"><circle cx="28" cy="26" r="8"/>'
            '<circle cx="72" cy="26" r="8"/><circle cx="28" cy="58" r="8"/><circle cx="72" cy="58" r="8"/></g>'
            '<rect x="42" y="36" width="16" height="12" rx="3" fill="#C1272D"/>'
            '<g fill="#8A5A2B"><path d="M8 96 V78 l10 -6 10 6 v18z M40 96 V74 l12 -8 12 8 v22z M72 96 V80 l10 -5 10 5 v16z"/></g>')

def _tariffs():
    return ('<rect x="24" y="10" width="52" height="72" rx="3" fill="#FFFFFF" stroke="#B9AE94"/>'
            '<rect x="40" y="5" width="20" height="10" rx="3" fill="#37424E"/>'
            '<text x="50" y="52" font-family="Georgia, serif" font-size="34" font-weight="bold" fill="#C1272D" text-anchor="middle">%</text>'
            '<path d="M34 66 h32 M34 74 h22" stroke="#9AA3AB" stroke-width="3"/>'
            '<path d="M66 26 l12 -10 M78 16 v9 M78 16 h-9" stroke="#1E7A46" stroke-width="3" fill="none"/>')

def _chart():
    return ('<path d="M12 8 v80 h84" stroke="#5A544A" stroke-width="2.4" fill="none"/>'
            '<path d="M16 22 L38 30 L54 26 L70 52 L90 78" stroke="#C1272D" stroke-width="3.4" fill="none"/>'
            '<path d="M90 78 l-12 -2 M90 78 l-3 -12" stroke="#C1272D" stroke-width="3.4"/>'
            '<g fill="#C1272D"><circle cx="16" cy="22" r="3"/><circle cx="38" cy="30" r="3"/>'
            '<circle cx="54" cy="26" r="3"/><circle cx="70" cy="52" r="3"/></g>')

def _wildfire():
    return ('<g fill="#2E5D3A"><path d="M18 78 l10 -34 10 34z M42 78 l10 -40 10 40z M66 78 l10 -34 10 34z"/></g>'
            '<g fill="#5A4632"><rect x="26" y="78" width="4" height="10"/><rect x="50" y="78" width="4" height="10"/><rect x="74" y="78" width="4" height="10"/></g>'
            '<path d="M50 88 c-10 -8 4 -14 0 -26 c10 8 16 16 8 26 c-3 3 -5 3 -8 0z" fill="#E8641E"/>'
            '<path d="M50 88 c-5 -4 2 -8 0 -14 c5 5 8 9 4 14 c-2 2 -2 2 -4 0z" fill="#E8A13A"/>')

def _island():
    return ('<path d="M14 74 q36 -16 72 0 l0 6 H14z" fill="#C9A86A"/>'
            '<path d="M50 72 q2 -22 -8 -30 M50 72 q10 -18 24 -20 M50 72 q-14 -14 -24 -12" stroke="#2E5D3A" stroke-width="3.4" fill="none"/>'
            '<rect x="48" y="70" width="4" height="10" fill="#5A4632"/>'
            '<circle cx="80" cy="20" r="8" fill="#E8A13A"/>'
            '<path d="M4 88 q8 -6 16 0 q8 6 16 0 q8 -6 16 0 q8 6 16 0 q8 -6 16 0 q8 6 12 2" stroke="#20509E" stroke-width="2.4" fill="none"/>')

def _pope():
    return ('<path d="M28 82 V58 a22 20 0 0 1 44 0 v24z" fill="#D8D2C2"/>'
            '<rect x="22" y="82" width="56" height="6" fill="#B9AE94"/>'
            '<rect x="47" y="30" width="6" height="12" fill="#8A5A2B"/>'
            '<path d="M50 22 v10 M45 27 h10" stroke="#8A5A2B" stroke-width="2.6"/>'
            '<path d="M66 66 q12 -10 20 -8 q-2 12 -14 14 q-6 1 -6 -6z" fill="#2E5D3A"/>'
            '<path d="M68 70 q8 -4 14 -10" stroke="#FAF5EA" stroke-width="1.4" fill="none"/>')

def _burst():
    return ('<g fill="#37424E"><rect x="12" y="34" width="30" height="52"/><rect x="48" y="24" width="24" height="62"/></g>'
            '<g fill="#D8D2C2"><rect x="18" y="42" width="7" height="8"/><rect x="30" y="42" width="7" height="8"/>'
            '<rect x="18" y="56" width="7" height="8"/><rect x="54" y="34" width="7" height="8"/>'
            '<rect x="54" y="48" width="7" height="8"/></g>'
            '<g stroke="#E8641E" stroke-width="2.6"><path d="M84 12 v12 M84 34 v4 M74 18 l6 8 M94 18 l-6 8 M72 32 h7 M89 32 h7"/></g>'
            '<circle cx="84" cy="28" r="5" fill="#E8A13A"/>'
            '<path d="M46 60 l8 8 M54 60 l-8 8" stroke="#C1272D" stroke-width="2.2"/>')

SCENES = {
    "parade": ("#DCE9F5", _balloon), "mumbai": ("#F3E3C2", _mumbai),
    "chess": ("#E7DFC8", _chess), "hormuz": ("#D5E6EF", _tanker),
    "odesa": ("#E3E0D8", _odesa), "leak": ("#EFE9DC", _leakdoc),
    "sudan": ("#F0DFC0", _drone), "tariffs": ("#EFE9DC", _tariffs),
    "kospi": ("#F6E3E1", _chart), "chile": ("#F3E0CE", _wildfire),
    "solomons": ("#D5E6EF", _island), "pope": ("#EFE9DC", _pope),
    "colombia": ("#E3E0D8", _burst),
}

def scene(name, x, y, w, h):
    tint, draw = SCENES[name]
    s = min(w, h) / 100.0
    ox = x + (w - 100 * s) / 2
    oy = y + (h - 100 * s) / 2
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{tint}"/>'
            f'<g transform="translate({ox:.1f} {oy:.1f}) scale({s:.3f})">{draw()}</g></g>')

# ------------------------------------------------------------------ data
# Leads: pin, region kicker, scene, headline lines, dek lines, outlet, status.
LEADS = [
    (1, "NORTH AMERICA · NEW YORK", "parade",
     ["Macy's parade postponed for the",
      "first time in 100 years"],
     ["Gusts to 60 mph ground the giant balloons;",
      "the 100th parade moves to Sat 08:30 ET."],
     "Reuters", "OFFICIAL"),
    (2, "ASIA · MUMBAI", "mumbai",
     ["India marks 18 years since the",
      "26/11 Mumbai attacks"],
     ["Memorials honour the 166 people killed in",
      "2008; the date anchors the day's remembrance."],
     "IANS", "CONFIRMED"),
    (3, "SPORT · GENEVA", "chess",
     ["Gukesh-Sindarov Game 3 in Geneva,",
      "world title level at 1-1"],
     ["Sindarov has White in Game 3 (15:00 CET);",
      "two draws open the 14-game title match."],
     "Chess.com", "ONGOING"),
    (4, "MIDDLE EAST · HORMUZ", "hormuz",
     ["Two tankers hit mines in Hormuz",
      "and catch fire, IRGC says"],
     ["Tehran says its forces struck the ships; Iran",
      "also deploys new systems over the strait."],
     "Reuters", "REPORTED"),
    (5, "EUROPE · UKRAINE", "odesa",
     ["Russian strike kills 2 in Odesa;",
      "Kyiv flat ablaze"],
     ["The overnight attack hits the port city as Merz",
      "warns Russia is escalating against Europe."],
     "Reuters", "CONFIRMED"),
    (6, "EUROPE · UKRAINE WAR", "leak",
     ["Leak puts Russian dead at",
      "490,334 since 2022"],
     ["The figure is a leaked tally reported by the",
      "BBC; it has not been independently verified."],
     "BBC", "REPORTED"),
]

# Strip: pin, scene, headline lines (3), outlet, status.
STRIP = [
    (7, "sudan", ["RSF drone strikes kill", "19 civilians in Sudan"], "Reuters", "REPORTED"),
    (8, "tariffs", ["US set to unveil tariffs on", "China, EU and 14 more"], "AP", "OFFICIAL"),
    (9, "kospi", ["Asian stocks tumble;", "KOSPI -5.8% on tariffs"], "Reuters", "CONFIRMED"),
    (10, "chile", ["Chile convicts 7 over 2024", "wildfire that killed 138"], "PaiPee", "CONFIRMED"),
    (11, "solomons", ["Solomons, Australia sign", "treaty barring foreign base"], "NYT", "OFFICIAL"),
    (12, "pope", ["Pope Leo XIV laments", "COP31 failure to agree"], "AP", "CONFIRMED"),
    (13, "colombia", ["Car bomb hits governor's", "office in Meta, Colombia"], "Al Jazeera", "REPORTED"),
]

# Region columns: (section, [(headline lines, outlet, status), ...])
REGIONS = [
    ("NORTH AMERICA", [
        (["Abrego Garcia leaves US", "voluntarily for Spain"], "NYT", "CONFIRMED"),
        (["Sullivan concedes Alaska", "Senate race to Peltola"], "NYT", "CONFIRMED"),
        (["Giuliani awarded the", "Medal of Freedom"], "Politico", "OFFICIAL"),
        (["Lutnick diverted agents", "for his own security"], "The Atlantic", "REPORTED"),
    ]),
    ("LATIN AMERICA", [
        (["WHO chief in Cuba urges US", "to lift the fuel blockade"], "Reuters", "REPORTED"),
        (["Supercell storm devastates", "Tupancireta, Brazil"], "Al Jazeera", "CONFIRMED"),
        (["Mexico FDI hits record", "$43.09B in nine months"], "Rio Times", "CONFIRMED"),
    ]),
    ("EUROPE", [
        (["Von der Leyen: Europe to join", "the Ukraine peace talks"], "Archynewsy", "OFFICIAL"),
        (["Merz: Russia is 'escalating'", "its threats to Europe"], "Reuters", "CONFIRMED"),
        (["Putin: Ukraine kept hitting", "refineries; payback is due"], "Reuters", "CLAIM"),
        (["EU leaders to debate Costa", "budget cuts Thu-Fri"], "Reuters", "OFFICIAL"),
    ]),
    ("MIDDLE EAST", [
        (["Houthis claim the Ras Tanura", "refinery attack in Saudi"], "Reuters", "CLAIM"),
        (["Houthi strike on a Riyadh", "tower injures 11 people"], "NYT", "REPORTED"),
        (["Israel kills Hamas security", "chief Abuelouf and family"], "Reuters", "REPORTED"),
    ]),
    ("AFRICA", [
        (["DRC halts all cobalt exports", "from the end of the month"], "Daily Plug", "OFFICIAL"),
        (["Ethiopia launches polio drive", "for 11.3M children"], "Addis Standard", "OFFICIAL"),
        (["Nigeria holds its interest", "rate steady at 23%"], "NM Media", "OFFICIAL"),
    ]),
    ("ASIA-PACIFIC", [
        (["26 miners trapped in a flooded", "West Java gold mine"], "Kilambi", "ONGOING"),
        (["Danantara posts first profit:", "Rp259.6 trillion"], "Kilambi", "CONFIRMED"),
        (["Australia inflation beats", "forecasts in October"], "Reuters", "CONFIRMED"),
    ]),
    ("GLOBAL · MARKETS · TECH", [
        (["Nasdaq futures fall 2% on", "fresh tariff fears"], "Reuters", "CONFIRMED"),
        (["Bitcoin falls 1% to", "$59,257 in risk-off trade"], "Reuters", "CONFIRMED"),
        (["AI staff: internal models 'too", "powerful to release'"], "Axios", "REPORTED"),
    ]),
]

STATS = [
    ("100th", "Macy's parade - postponed, a first"),
    ("18 yrs", "since the 26/11 Mumbai attacks"),
    ("60 mph", "gusts grounding the balloons"),
    ("1-1", "world chess title, two draws"),
    ("490,334", "Russian dead in the leaked tally"),
    ("-5.8%", "KOSPI on the tariff threat"),
]

TIMELINE = [
    ("OVERNIGHT", "Russian strike on Odesa; two tankers ablaze in Hormuz"),
    ("ALL DAY", "India marks 18 years since the 26/11 attacks"),
    ("13:30 UTC", "Macy's parade was to step off in New York - storm moves it"),
    ("14:00 UTC", "Game 3 of the world chess title opens in Geneva"),
    ("THU-FRI", "EU leaders debate the Costa budget cuts in Brussels"),
]

DATECHECK = ("DATE CHECK - held out, with dates: chess Games 1-2, Geneva - 24-25 Nov · "
             "balloon inflation, New York - Wed 25 Nov · COP31's no-pact close - earlier "
             "cycle (the Pope's 25 Nov lament is carried inside). NOT YET: the parade "
             "itself - Sat 28 Nov · chess Game 4 - Sat 28 Nov (Fri 27 is a rest day).")

LEGEND = ("CONFIRMED wire-verified · OFFICIAL announced by an authority · REPORTED "
          "single-source or attributed · CLAIM one side's assertion · ONGOING developing")

# Dot-matrix world map: rows 0..39 (lat 75 to -55), cols 0..85
# (lon -170 to 190). Each row lists land spans as (first, last) columns.
MAP_SPANS = {
    0: [(4, 20), (26, 33), (52, 84)], 1: [(3, 22), (27, 32), (50, 85)],
    2: [(3, 22), (27, 32), (46, 50), (52, 85)], 3: [(4, 23), (44, 51), (51, 85)],
    4: [(4, 24), (43, 52), (50, 85)], 5: [(5, 25), (43, 53), (52, 84)],
    6: [(6, 25), (43, 55), (52, 83)], 7: [(6, 26), (42, 54), (53, 83)],
    8: [(7, 26), (42, 54), (54, 82)], 9: [(7, 26), (42, 53), (55, 81)],
    10: [(8, 26), (42, 52), (55, 80)], 11: [(8, 26), (43, 52), (56, 79)],
    12: [(9, 25), (43, 54), (54, 78)], 13: [(9, 24), (43, 55), (55, 77)],
    14: [(10, 22), (43, 55), (56, 72), (72, 78)], 15: [(11, 20), (44, 56), (57, 70), (71, 77)],
    16: [(12, 17), (44, 56), (59, 66), (70, 77)], 17: [(14, 18), (44, 57), (60, 65), (71, 76)],
    18: [(20, 27), (44, 57), (61, 64), (71, 76)], 19: [(20, 28), (45, 56), (72, 78)],
    20: [(20, 29), (45, 56), (72, 80)], 21: [(21, 30), (46, 55), (73, 81)],
    22: [(21, 30), (46, 55), (73, 81)], 23: [(22, 30), (46, 54), (76, 82)],
    24: [(22, 30), (46, 54), (79, 83)], 25: [(22, 30), (47, 53), (74, 81)],
    26: [(22, 29), (47, 53), (72, 80)], 27: [(23, 29), (47, 52), (71, 81)],
    28: [(23, 29), (47, 52), (70, 81)], 29: [(23, 28), (48, 51), (71, 80)],
    30: [(23, 28), (48, 51), (71, 79)], 31: [(23, 27), (72, 78)],
    32: [(23, 27), (73, 77)], 33: [(23, 27)], 34: [(23, 26)],
    35: [(23, 26)], 36: [(23, 25)], 37: [(23, 25)],
}
# Pins: story number -> (col, row) on the map grid.
PINS = {1: (23, 11), 2: (61, 17), 3: (41, 8), 4: (54, 15), 5: (49, 9),
        6: (51, 5), 7: (48, 18), 8: (21, 12), 9: (71, 12), 10: (24, 33),
        11: (23, 22), 12: (79, 26), 13: (45, 11)}

def world_map(x, y, w, h):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FDFBF5"/>']
    cw, ch = w / 86.0, h / 40.0
    for r, spans in MAP_SPANS.items():
        for a, b in spans:
            for c in range(a, b + 1):
                out.append(f'<circle cx="{x + (c + 0.5) * cw:.1f}" cy="{y + (r + 0.5) * ch:.1f}" '
                           f'r="{min(cw, ch) * 0.30:.1f}" fill="#B9C4CE"/>')
    for n, (c, r) in PINS.items():
        px, py = x + (c + 0.5) * cw, y + (r + 0.5) * ch
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7.5" fill="{RED}" '
                   f'stroke="#FFFFFF" stroke-width="1.4"/>')
        out.append(f'<text x="{px:.1f}" y="{py + 3.2:.1f}" font-family="Arial, sans-serif" '
                   f'font-size="8.5" font-weight="bold" fill="#FFFFFF" '
                   f'text-anchor="middle">{n}</text>')
    return "".join(out)

# ------------------------------------------------------------- assembly
def pin_badge(x, y, n):
    return (f'<circle cx="{x}" cy="{y}" r="9" fill="{RED}" stroke="#FFFFFF" stroke-width="1.5"/>'
            f'<text x="{x}" y="{y + 3.4}" font-family="Arial, sans-serif" font-size="9.5" '
            f'font-weight="bold" fill="#FFFFFF" text-anchor="middle">{n}</text>')

def lead_card(x, y, lead):
    n, kicker, sc, head, dek, outlet, status = lead
    out = [f'<rect x="{x}" y="{y}" width="326" height="110" fill="#FFFFFF" stroke="{RULE}"/>']
    out.append(scene(sc, x, y, 100, 110))
    out.append(pin_badge(x + 11, y + 11, n))
    tx = x + 108
    out.append(text(tx, y + 15, kicker, 8, RED, "bold", spacing="0.4"))
    for i, ln in enumerate(head):
        out.append(text(tx, y + 35 + i * 17, ln, 14, INK, "bold", family="Georgia, serif"))
    for i, ln in enumerate(dek):
        out.append(text(tx, y + 70 + i * 12, ln, 9.5, "#3A362E"))
    c, cw = chip(tx, y + 90, status)
    out.append(c)
    out.append(text(tx + cw + 6, y + 99.5, outlet, 8.5, MUTE))
    return "".join(out)

def strip_card(x, y, item):
    n, sc, head, outlet, status = item
    out = [f'<rect x="{x}" y="{y}" width="140" height="168" fill="#FFFFFF" stroke="{RULE}"/>']
    out.append(scene(sc, x, y, 140, 100))
    out.append(pin_badge(x + 10, y + 10, n))
    for i, ln in enumerate(head):
        out.append(text(x + 4, y + 120 + i * 14, ln, 11, INK, "bold", family="Georgia, serif"))
    c, cw = chip(x + 4, y + 146, status)
    out.append(c)
    out.append(text(x + 4 + cw + 5, y + 155.5, outlet, 8, MUTE))
    return "".join(out)

def region_block(x, y, section, items):
    out = [f'<rect x="{x}" y="{y}" width="244" height="17" fill="{DARK}"/>']
    out.append(text(x + 6, y + 12.5, section, 9.5, "#FFFFFF", "bold", spacing="0.6"))
    cy = y + 21
    for head, outlet, status in items:
        for i, ln in enumerate(head):
            out.append(text(x + 2, cy + 10 + i * 10.5, ln, 10, INK, "bold", family="Georgia, serif"))
        c, cw = chip(x + 2, cy + 23, status)
        out.append(c)
        out.append(text(x + 2 + cw + 5, cy + 32.5, outlet, 8, MUTE))
        cy += 38
    return "".join(out), cy

def build():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    # Masthead
    p.append(text(8, 38, "THE WORLD IN ONE DAY", 29, INK, "bold", family="Georgia, serif"))
    p.append(text(1016, 24, "Thursday 26 November 2026", 16, INK, "bold",
                  anchor="end", family="Georgia, serif"))
    p.append(text(1016, 42, "Thanksgiving Day in the United States · Global Edition",
                  10, MUTE, anchor="end"))
    p.append(f'<rect x="8" y="50" width="1008" height="3" fill="{RED}"/>')
    p.append(f'<rect x="8" y="55" width="1008" height="1" fill="{INK}"/>')
    # Stat band
    p.append(f'<rect x="8" y="62" width="1008" height="40" fill="{DARK}"/>')
    for i, (num, lab) in enumerate(STATS):
        sx = 8 + i * 168
        p.append(text(sx + 8, 62 + 17, num, 15, "#FFFFFF", "bold", family="Georgia, serif"))
        p.append(text(sx + 8, 62 + 31, lab, 8, "#CFC8B4"))
    # Leads (2 cols x 3 rows)
    for i, lead in enumerate(LEADS):
        p.append(lead_card(8 + (i % 2) * 334, 110 + (i // 2) * 116, lead))
    # Map + timeline (right column)
    p.append(text(676, 118, "WHERE IT HAPPENED - THE 13 SCENES, PINNED", 9, RED, "bold", spacing="0.4"))
    p.append(world_map(676, 124, 340, 144))
    p.append(text(676, 280, "Schematic dot map; pin numbers match the scenes.", 8, MUTE))
    p.append(f'<rect x="676" y="290" width="340" height="17" fill="{DARK}"/>')
    p.append(text(682, 302.5, "THE DAY IN UTC", 9.5, "#FFFFFF", "bold", spacing="0.6"))
    ty = 316
    for when, what in TIMELINE:
        p.append(text(676, ty + 10, when, 9, RED, "bold"))
        p.append(text(742, ty + 10, what, 9.5, INK))
        ty += 27
    # Scene strip (7 cards)
    for i, item in enumerate(STRIP):
        p.append(strip_card(8 + i * 144, 464, item))
    # Region columns (4 across); col 4 also carries the date check.
    cols = [(8, [REGIONS[0], REGIONS[3]]), (260, [REGIONS[1], REGIONS[4]]),
            (512, [REGIONS[2], REGIONS[6]]), (764, [REGIONS[5]])]
    for cx, sections in cols:
        cy = 642
        for section, items in sections:
            block, cy = region_block(cx, cy, section, items)
            p.append(block)
            cy += 6
    # Date check box (column 4, under Asia-Pacific)
    p.append(f'<rect x="764" y="800" width="244" height="146" fill="#FDFBF5" stroke="{RED}"/>')
    p.append(text(770, 816, "DATE CHECK - HELD OUT, WITH DATES", 9, RED, "bold"))
    dc = ["Chess Games 1-2, Geneva - 24-25 Nov",
          "Balloon inflation, New York - Wed 25 Nov",
          "COP31 no-pact close - earlier cycle",
          "(the Pope's 25 Nov lament is inside)",
          "NOT YET - STILL TO COME:",
          "The parade itself - Sat 28 Nov",
          "Chess Game 4 - Sat 28 Nov",
          "(Fri 27 is a rest day)"]
    for i, ln in enumerate(dc):
        w = "bold" if ln.startswith("NOT YET") else "normal"
        p.append(text(770, 832 + i * 13, ln, 8.8, INK, w))
    # Footer
    p.append(f'<rect x="8" y="954" width="1008" height="1.5" fill="{INK}"/>')
    p.append(text(8, 972, "STATUS KEY: " + LEGEND, 8.8, MUTE))
    p.append(text(8, 988, "All 13 scenes are drawn, not photographed. Every story is cited in "
                          "SOURCES.md; nothing older than the 26 Nov cycle, nothing from after it.",
                  8.8, MUTE))
    p.append(text(8, 1004, "36 stories · 6 regions + 3 global desks · 15 fields · One page, one day.",
                  8.8, INK, "bold"))
    p.append(text(1016, 1004, "Global Edition · news-image-20261126", 8.8, MUTE, anchor="end"))
    p.append("</svg>")
    return "".join(p)

if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "poster.svg"), "w", encoding="utf-8") as f:
        f.write(build())
    print("poster.svg written")
