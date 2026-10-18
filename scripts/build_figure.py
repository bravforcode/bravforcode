#!/usr/bin/env python3
"""Build Fig. 1 (work log on graph paper) for the profile README.
Run: python scripts/build_figure.py  -> assets/log-light.svg, assets/log-dark.svg
The SVG is drawn at its display width (880px) so text is never scaled down."""
import datetime as dt, pathlib, html

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)
W, H = 880, 476
X0, X1 = 24, 856
D0, D1 = dt.date(2025, 7, 1), dt.date(2026, 11, 1)
SANS = "-apple-system,'Segoe UI','Noto Sans Thai','Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,'SFMono-Regular',Consolas,Menlo,monospace"
RES_Y, COMP_Y, AXIS_Y = 100, 314, 432

THEMES = {
    "light": dict(bg="#FFFFFF", minor="#E3EDE9", major="#C9DBD4", ink="#15201C", muted="#55645F", pen="#B42318", rule="#15201C"),
    "dark":  dict(bg="#0D1117", minor="#161F24", major="#223038", ink="#E6EDF3", muted="#A3B1BB", pen="#FF8A75", rule="#E6EDF3"),
}

def x_of(d):
    return X0 + (d - D0).days / (D1 - D0).days * (X1 - X0)

COMP = [
    (dt.date(2025, 7, 26), "THNIC Academy", "Jul 2025", "up", 2),
    (dt.date(2025, 8, 30), "Cyber Top Talent", "Aug 2025", "up", 1),
    (dt.date(2026, 3, 17), "AI Thailand · LOTUSDIS", "Mar 2026", "up", 2),
    (dt.date(2026, 4, 3), "Mahidol × Harvard", "Apr 2026", "up", 1),
    (dt.date(2026, 5, 20), "AI Thailand · Minutes", "May 2026", "down", 1),
    (dt.date(2026, 7, 15), "AI Thailand · LLM", "Jul 2026", "up", 2),
    (dt.date(2026, 8, 19), "EEC-SDG pitch", "Aug 2026", "up", 1),
]

def build(name, t):
    e = html.escape
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">',
         '<title id="t">Work log, July 2025 to October 2026</title>',
         '<desc id="d">Two lanes on graph paper. Competitions: THNIC Academy Jul 2025, Cyber Top Talent Aug 2025, AI Thailand LOTUSDIS Mar 2026, Mahidol x Harvard Apr 2026, AI Thailand Minutes May 2026, AI Thailand LLM Jul 2026, EEC-SDG pitching Aug 2026. Research: GMX G5 protocol frozen 26 Sep 2026 with collection to 11 Oct, CPIV v28 archived 17 Oct 2026.</desc>',
         f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>']
    step = 16
    for i, x in enumerate(range(0, W + 1, step)):
        c = t["major"] if i % 5 == 0 else t["minor"]
        o.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{c}" stroke-width="1"/>')
    for i, y in enumerate(range(0, H + 1, step)):
        c = t["major"] if i % 5 == 0 else t["minor"]
        o.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{c}" stroke-width="1"/>')
    o.append(f'<rect x="{X0}" y="18" width="340" height="34" fill="{t["bg"]}"/>')
    o.append(f'<text x="{X0+4}" y="42" font-family="{SANS}" font-size="18" font-weight="700" fill="{t["ink"]}">Work log, Jul 2025 – Oct 2026</text>')
    for y in (RES_Y, COMP_Y):
        o.append(f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{t["rule"]}" stroke-width="2"/>')
    o.append(f'<line x1="{X0}" y1="{AXIS_Y}" x2="{X1}" y2="{AXIS_Y}" stroke="{t["rule"]}" stroke-width="1.5"/>')
    d = D0
    while d < D1:
        x = x_of(d)
        nd = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        mx = x_of(nd)
        o.append(f'<line x1="{x:.1f}" y1="{AXIS_Y}" x2="{x:.1f}" y2="{AXIS_Y+7}" stroke="{t["rule"]}" stroke-width="1.5"/>')
        o.append(f'<text x="{(x+mx)/2:.1f}" y="{AXIS_Y+24}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{d.strftime("%b")[0]}</text>')
        if d == D0 or d.month == 1:
            o.append(f'<rect x="{x+1:.1f}" y="{AXIS_Y+30}" width="40" height="18" fill="{t["bg"]}"/>')
            o.append(f'<text x="{x+3:.1f}" y="{AXIS_Y+44}" font-family="{MONO}" font-size="13" font-weight="700" fill="{t["ink"]}">{d.year}</text>')
        d = nd
    o.append(f'<rect x="{X0}" y="{RES_Y+8}" width="100" height="22" fill="{t["bg"]}"/>')
    o.append(f'<text x="{X0+4}" y="{RES_Y+25}" font-family="{SANS}" font-size="15" font-weight="700" fill="{t["ink"]}">Research</text>')
    o.append(f'<rect x="{X0}" y="{COMP_Y+8}" width="120" height="22" fill="{t["bg"]}"/>')
    o.append(f'<text x="{X0+4}" y="{COMP_Y+25}" font-family="{SANS}" font-size="15" font-weight="700" fill="{t["ink"]}">Competitions</text>')
    for d, label, dtxt, side, lvl in COMP:
        x = x_of(d)
        dy = 50 * lvl
        y2 = COMP_Y - dy if side == "up" else COMP_Y + dy
        o.append(f'<line x1="{x:.1f}" y1="{COMP_Y}" x2="{x:.1f}" y2="{y2}" stroke="{t["ink"]}" stroke-width="1.5"/>')
        o.append(f'<circle cx="{x:.1f}" cy="{COMP_Y}" r="5" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="2.5"/>')
        ty = y2 - 22 if side == "up" else y2 + 16
        w = len(label) * 8.4 + 14
        o.append(f'<rect x="{x+4:.1f}" y="{ty-16:.1f}" width="{w:.0f}" height="40" fill="{t["bg"]}"/>')
        o.append(f'<text x="{x+8:.1f}" y="{ty:.1f}" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["ink"]}">{e(label)}</text>')
        o.append(f'<text x="{x+8:.1f}" y="{ty+17:.1f}" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{e(dtxt)}</text>')
    gx0, gx1 = x_of(dt.date(2026, 9, 27)), x_of(dt.date(2026, 10, 11))
    px = x_of(dt.date(2026, 9, 26))
    o.append(f'<line x1="{px:.1f}" y1="{RES_Y-9}" x2="{px:.1f}" y2="{RES_Y-48}" stroke="{t["pen"]}" stroke-width="1.5"/>')
    o.append(f'<rect x="{px-190:.0f}" y="{RES_Y-80}" width="184" height="44" fill="{t["bg"]}"/>')
    o.append(f'<text x="{px-6:.1f}" y="{RES_Y-62}" text-anchor="end" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["ink"]}">GMX G5 protocol frozen,</text>')
    o.append(f'<text x="{px-6:.1f}" y="{RES_Y-44}" text-anchor="end" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["ink"]}">collection to 11 Oct</text>')
    o.append(f'<rect x="{gx0:.1f}" y="{RES_Y-9}" width="{gx1-gx0:.1f}" height="18" fill="{t["pen"]}"/>')
    o.append(f'<line x1="{px:.1f}" y1="{RES_Y-14}" x2="{px:.1f}" y2="{RES_Y+14}" stroke="{t["pen"]}" stroke-width="3"/>')
    cx = x_of(dt.date(2026, 10, 17))
    o.append(f'<line x1="{cx:.1f}" y1="{RES_Y}" x2="{cx:.1f}" y2="{RES_Y+38}" stroke="{t["pen"]}" stroke-width="1.5"/>')
    o.append(f'<circle cx="{cx:.1f}" cy="{RES_Y}" r="6" fill="{t["pen"]}"/>')
    o.append(f'<rect x="{cx-158:.0f}" y="{RES_Y+22}" width="152" height="42" fill="{t["bg"]}"/>')
    o.append(f'<text x="{cx-8:.1f}" y="{RES_Y+42}" text-anchor="end" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["ink"]}">CPIV v28 archived</text>')
    o.append(f'<text x="{cx-8:.1f}" y="{RES_Y+59}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t["muted"]}">17 Oct 2026 · DOI</text>')
    o.append('</svg>')
    (OUT / f"log-{name}.svg").write_text("\n".join(o), encoding="utf-8")

for n, t in THEMES.items():
    build(n, t)
print("wrote", OUT)
