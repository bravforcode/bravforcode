#!/usr/bin/env python3
"""LinkedIn banner (1584x396) on graph paper. Run: python scripts/build_banner.py
Writes assets/linkedin-banner.svg; render to PNG with any browser or `npx playwright` (see linkedin/README)."""
import datetime as dt, pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)
W, H = 1584, 396
SANS = "-apple-system,'Segoe UI','Noto Sans Thai','Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,'SFMono-Regular',Consolas,Menlo,monospace"
BG, MINOR, MAJOR, INK, MUTED, PEN = "#FFFFFF", "#E3EDE9", "#C9DBD4", "#15201C", "#55645F", "#B42318"
D0, D1 = dt.date(2025, 7, 1), dt.date(2026, 11, 1)
TX0, TX1, TY = 560, 1500, 330       # timeline strip, right of the avatar zone
def x_of(d): return TX0 + (d - D0).days / (D1 - D0).days * (TX1 - TX0)
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Phirawit Jitnarong, Full-Stack and AI engineer, Data and Quant research">',
     f'<rect width="{W}" height="{H}" fill="{BG}"/>']
for i, x in enumerate(range(0, W + 1, 24)):
    o.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{MAJOR if i % 5 == 0 else MINOR}"/>')
for i, y in enumerate(range(0, H + 1, 24)):
    o.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{MAJOR if i % 5 == 0 else MINOR}"/>')
o.append(f'<rect x="528" y="64" width="940" height="212" fill="{BG}"/>')
o.append(f'<text x="552" y="132" font-family="{SANS}" font-size="62" font-weight="800" fill="{INK}">Full-Stack &amp; AI engineer</text>')
o.append(f'<text x="552" y="196" font-family="{SANS}" font-size="38" font-weight="500" fill="{INK}">Data / Quant research, reproducible by default</text>')
o.append(f'<text x="552" y="248" font-family="{MONO}" font-size="26" fill="{MUTED}">Burapha University · Thailand · internship 2027</text>')
o.append(f'<line x1="{TX0}" y1="{TY}" x2="{TX1}" y2="{TY}" stroke="{INK}" stroke-width="3"/>')
for d in [dt.date(2025,7,26), dt.date(2025,8,30), dt.date(2026,3,17), dt.date(2026,4,3), dt.date(2026,5,20), dt.date(2026,7,15), dt.date(2026,8,19)]:
    x = x_of(d); o.append(f'<circle cx="{x:.1f}" cy="{TY}" r="8" fill="{BG}" stroke="{INK}" stroke-width="3.5"/>')
gx0, gx1 = x_of(dt.date(2026,9,27)), x_of(dt.date(2026,10,11))
o.append(f'<rect x="{gx0:.1f}" y="{TY-11}" width="{gx1-gx0:.1f}" height="22" fill="{PEN}"/>')
o.append(f'<circle cx="{x_of(dt.date(2026,10,17)):.1f}" cy="{TY}" r="9" fill="{PEN}"/>')
o.append(f'<rect x="{TX0}" y="{TY+14}" width="260" height="30" fill="{BG}"/>')
o.append(f'<text x="{TX0}" y="{TY+36}" font-family="{MONO}" font-size="20" fill="{MUTED}">Jul 2025</text>')
o.append(f'<rect x="{TX1-110}" y="{TY+14}" width="130" height="30" fill="{BG}"/>')
o.append(f'<text x="{TX1}" y="{TY+36}" text-anchor="end" font-family="{MONO}" font-size="20" fill="{MUTED}">Oct 2026</text>')
o.append('</svg>')
(OUT / "linkedin-banner.svg").write_text("\n".join(o), encoding="utf-8")
print("wrote assets/linkedin-banner.svg")
