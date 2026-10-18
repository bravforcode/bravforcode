#!/usr/bin/env python3
"""Generate the self-hosted SVG assets for the profile README.
Run: python scripts/build_assets.py   (writes into ./assets)"""
import html, pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)
SANS = "'Segoe UI','Helvetica Neue',Arial,'Noto Sans Thai','Leelawadee UI',sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,Menlo,monospace"
e = html.escape

def defs(uid):
    return f'''<defs>
  <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070B18"/><stop offset=".55" stop-color="#0E1736"/><stop offset="1" stop-color="#1A1245"/></linearGradient>
  <linearGradient id="ac{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#38BDF8"/><stop offset=".5" stop-color="#A78BFA"/><stop offset="1" stop-color="#F472B6"/></linearGradient>
  <radialGradient id="o1{uid}"><stop offset="0" stop-color="#38BDF8" stop-opacity=".55"/><stop offset="1" stop-color="#38BDF8" stop-opacity="0"/></radialGradient>
  <radialGradient id="o2{uid}"><stop offset="0" stop-color="#A78BFA" stop-opacity=".5"/><stop offset="1" stop-color="#A78BFA" stop-opacity="0"/></radialGradient>
  <radialGradient id="o3{uid}"><stop offset="0" stop-color="#F472B6" stop-opacity=".4"/><stop offset="1" stop-color="#F472B6" stop-opacity="0"/></radialGradient>
  <pattern id="gr{uid}" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity=".05"/></pattern>
</defs>'''

def hero():
    u = "h"
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="360" viewBox="0 0 1280 360" role="img" aria-labelledby="t d">
<title id="t">Phirawit Jitnarong</title><desc id="d">Full-Stack and AI Engineer, Data and Quant research, Burapha University, Thailand</desc>
{defs(u)}
<rect width="1280" height="360" rx="22" fill="url(#bg{u})"/>
<rect width="1280" height="360" rx="22" fill="url(#gr{u})"/>
<g>
  <circle cx="200" cy="80" r="200" fill="url(#o1{u})"><animate attributeName="cx" values="200;300;200" dur="14s" repeatCount="indefinite"/><animate attributeName="cy" values="80;130;80" dur="11s" repeatCount="indefinite"/></circle>
  <circle cx="1040" cy="300" r="240" fill="url(#o2{u})"><animate attributeName="cx" values="1040;940;1040" dur="16s" repeatCount="indefinite"/></circle>
  <circle cx="760" cy="40" r="170" fill="url(#o3{u})"><animate attributeName="cy" values="40;110;40" dur="13s" repeatCount="indefinite"/></circle>
</g>
<g font-family="{MONO}" font-size="14" fill="#7DD3FC" opacity=".85">
  <text x="84" y="78">// hello, world<animate attributeName="opacity" values="0;1" dur="1.2s" fill="freeze"/></text>
</g>
<text x="82" y="168" font-family="{SANS}" font-size="78" font-weight="800" fill="url(#ac{u})" letter-spacing="-1.5">Phirawit Jitnarong
  <animate attributeName="opacity" values="0;1" dur="1s" fill="freeze"/></text>
<text x="86" y="214" font-family="{SANS}" font-size="30" font-weight="500" fill="#E6EDF7">Full-Stack &amp; AI Engineer<tspan fill="#64748B"> · </tspan>Data / Quant Research</text>
<text x="86" y="252" font-family="{SANS}" font-size="22" fill="#94A3B8">พีรวิชญ์ จิตณรงค์ · Burapha University · Thailand</text>
<g font-family="{MONO}" font-size="17" fill="#CBD5E1">
  <rect x="84" y="282" width="318" height="40" rx="20" fill="#fff" fill-opacity=".07" stroke="#fff" stroke-opacity=".15"/>
  <circle cx="108" cy="302" r="6" fill="#34D399"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>
  <text x="124" y="308">open to internships · 2027</text>
</g>
<rect x="1180" y="60" width="2" height="240" fill="url(#ac{u})" opacity=".6"/>
</svg>'''
    (OUT / "hero.svg").write_text(s, encoding="utf-8")

def stats():
    items = [("25", "public repositories"), ("3", "NECTEC AI challenges"), ("1", "DOI-archived paper"), ("145", "tests in JobShield AI")]
    w, h, gap = 300, 120, 20
    W = len(items) * w + (len(items) - 1) * gap
    u = "s"
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="Profile statistics">{defs(u)}']
    for i, (n, label) in enumerate(items):
        x = i * (w + gap)
        out.append(f'''<g transform="translate({x},0)">
<rect width="{w}" height="{h}" rx="18" fill="url(#bg{u})" stroke="#fff" stroke-opacity=".08"/>
<rect x="0" y="0" width="{w}" height="4" rx="2" fill="url(#ac{u})"/>
<text x="26" y="68" font-family="{SANS}" font-size="52" font-weight="800" fill="url(#ac{u})">{n}</text>
<text x="26" y="98" font-family="{SANS}" font-size="16" fill="#A7B4C8">{e(label)}</text></g>''')
    out.append("</svg>")
    (OUT / "stats.svg").write_text("".join(out), encoding="utf-8")

CARDS = [
 ("research", "RESEARCH", "CPIV methods note", "Call–put implied-volatility spreads: exact BSM inversion and robustness under synthetic quote noise.", ["Python", "uv", "CI", "SHA-256"], "DOI · 10.5281/zenodo.23442601"),
 ("gmx", "RESEARCH", "GMX G5 prospective record", "Pre-registered protocol with fixed-time, hash-chained aggregate receipts collected four times a day.", ["Python", "GitHub Actions", "Protocol hash"], "Frozen protocol · timestamped Gist"),
 ("graxia", "PRODUCT", "Graxia OS", "Personal AI chief of staff: lead scoring, drafting and approval workflow with cost-aware model routing.", ["FastAPI", "Celery", "Redis", "React"], "Docker Compose quickstart"),
 ("adminmate", "PRODUCT", "AdminMate AI", "HR platform for SEA SMEs, from recruitment to payroll, with row-level security and Gemini assistance.", ["React 19", "Supabase", "Gemini"], "pgTAP suite · RLS policies"),
 ("agentos", "AI", "Enterprise Agent OS", "MCP server with 15 specialised sub-agents and 7 orchestration patterns over Qdrant and PostgreSQL.", ["Python", "MCP", "Qdrant"], "Reference implementation"),
 ("jobshield", "DATA", "JobShield AI", "Explainable career-path recommender on a PPMI skill graph with a wage-gap radar. Mock data, stated openly.", ["Next.js", "Python", "Dijkstra"], "Live demo · 145 tests"),
]
HUE = {"RESEARCH": ("#38BDF8", "#818CF8"), "PRODUCT": ("#A78BFA", "#F472B6"), "AI": ("#34D399", "#38BDF8"), "DATA": ("#FBBF24", "#F472B6")}

def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        if len(cur) + len(w_) + 1 > n and cur:
            lines.append(cur); cur = w_
        else:
            cur = (cur + " " + w_).strip()
    if cur: lines.append(cur)
    return lines[:3]

def cards():
    for key, kind, title, desc, tags, evid in CARDS:
        a, b = HUE[kind]
        u = "c" + key
        W, H = 620, 230
        lines = wrap(desc, 64)
        tspans = "".join(f'<tspan x="34" dy="{0 if i == 0 else 23}">{e(l)}</tspan>' for i, l in enumerate(lines))
        tx, chips = 34, []
        for t in tags:
            cw = 18 + len(t) * 8.4
            chips.append(f'<g transform="translate({tx},152)"><rect width="{cw:.0f}" height="28" rx="14" fill="#fff" fill-opacity=".07" stroke="#fff" stroke-opacity=".14"/><text x="{cw/2:.0f}" y="19" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#CBD5E1">{e(t)}</text></g>')
            tx += cw + 8
        s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{e(title)}">
<defs>
<linearGradient id="bg{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0A0F1F"/><stop offset="1" stop-color="#151C3D"/></linearGradient>
<linearGradient id="ac{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>
<radialGradient id="gl{u}"><stop offset="0" stop-color="{a}" stop-opacity=".35"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" rx="20" fill="url(#bg{u})" stroke="#fff" stroke-opacity=".09"/>
<circle cx="{W-40}" cy="30" r="150" fill="url(#gl{u})"><animate attributeName="r" values="150;180;150" dur="9s" repeatCount="indefinite"/></circle>
<rect x="34" y="30" width="{16+len(kind)*8.6:.0f}" height="22" rx="11" fill="url(#ac{u})" fill-opacity=".18" stroke="{a}" stroke-opacity=".5"/>
<text x="{34+(16+len(kind)*8.6)/2:.0f}" y="45" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="1.5" fill="{a}">{kind}</text>
<text x="34" y="86" font-family="{SANS}" font-size="29" font-weight="800" fill="#F1F5F9">{e(title)}</text>
<text x="34" y="112" font-family="{SANS}" font-size="15" fill="#A7B4C8">{tspans}</text>
{''.join(chips)}
<line x1="34" y1="196" x2="{W-34}" y2="196" stroke="#fff" stroke-opacity=".08"/>
<text x="34" y="217" font-family="{MONO}" font-size="13" fill="{a}">✓ {e(evid)}</text>
<text x="{W-34}" y="217" text-anchor="end" font-family="{MONO}" font-size="13" fill="#64748B">view repository →</text>
</svg>'''
        (OUT / f"card-{key}.svg").write_text(s, encoding="utf-8")

def skills():
    groups = [("Languages", ["Python", "TypeScript", "SQL"]), ("Backend", ["FastAPI", "Celery", "Supabase / PostgreSQL", "Redis"]),
              ("Frontend", ["React", "Next.js", "Tailwind"]), ("Data & AI", ["RAG", "Multi-agent / MCP", "Qdrant", "Statistics"]), ("Infra", ["Docker", "GitHub Actions"])]
    u = "k"; W = 1280; y = 52; rows = []
    for g, items in groups:
        x = 190
        rows.append(f'<text x="34" y="{y+19}" font-family="{MONO}" font-size="14" letter-spacing="1" fill="#7DD3FC">{e(g.upper())}</text>')
        for it in items:
            cw = 26 + len(it) * 9.2
            rows.append(f'<g transform="translate({x:.0f},{y})"><rect width="{cw:.0f}" height="30" rx="15" fill="#fff" fill-opacity=".07" stroke="#fff" stroke-opacity=".15"/><text x="{cw/2:.0f}" y="20" text-anchor="middle" font-family="{SANS}" font-size="15" fill="#E2E8F0">{e(it)}</text></g>')
            x += cw + 10
        y += 46
    H = y + 12
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Skills">{defs(u)}<rect width="{W}" height="{H}" rx="20" fill="url(#bg{u})" stroke="#fff" stroke-opacity=".08"/><rect width="{W}" height="4" rx="2" fill="url(#ac{u})"/>{"".join(rows)}</svg>'
    (OUT / "skills.svg").write_text(s, encoding="utf-8")

def divider(name, label):
    u = "d" + name
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="64" viewBox="0 0 1280 64" role="img" aria-label="{e(label)}">{defs(u)}
<text x="2" y="38" font-family="{SANS}" font-size="30" font-weight="800" fill="url(#ac{u})">{e(label)}</text>
<rect x="2" y="50" width="1276" height="2" rx="1" fill="url(#ac{u})" opacity=".35"/><rect x="2" y="50" width="120" height="2" rx="1" fill="url(#ac{u})"/></svg>'''
    (OUT / f"h-{name}.svg").write_text(s, encoding="utf-8")

def button(name, label, color):
    w = 62 + len(label) * 11.5
    u = "b" + name
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="46" viewBox="0 0 {w:.0f} 46" role="img" aria-label="{e(label)}">
<defs><linearGradient id="g{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0E1736"/><stop offset="1" stop-color="#1A1245"/></linearGradient></defs>
<rect x=".5" y=".5" width="{w-1:.0f}" height="45" rx="23" fill="url(#g{u})" stroke="{color}" stroke-opacity=".7"/>
<circle cx="24" cy="23" r="5" fill="{color}"/>
<text x="42" y="29" font-family="{SANS}" font-size="16" font-weight="600" fill="#F1F5F9">{e(label)}</text></svg>'''
    (OUT / f"btn-{name}.svg").write_text(s, encoding="utf-8")

def footer():
    u = "f"
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="140" viewBox="0 0 1280 140" role="img" aria-label="Footer">{defs(u)}
<rect width="1280" height="140" rx="20" fill="url(#bg{u})"/>
<path d="M0 90 C 200 50, 400 130, 640 90 S 1080 50, 1280 90 V140 H0Z" fill="url(#ac{u})" opacity=".25"><animate attributeName="d" dur="9s" repeatCount="indefinite" values="M0 90 C 200 50, 400 130, 640 90 S 1080 50, 1280 90 V140 H0Z;M0 90 C 200 130, 400 50, 640 90 S 1080 130, 1280 90 V140 H0Z;M0 90 C 200 50, 400 130, 640 90 S 1080 50, 1280 90 V140 H0Z"/></path>
<path d="M0 105 C 240 70, 420 140, 700 105 S 1100 75, 1280 105 V140 H0Z" fill="url(#ac{u})" opacity=".45"/>
<text x="640" y="52" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="700" fill="#F1F5F9">Thanks for stopping by</text>
<text x="640" y="80" text-anchor="middle" font-family="{SANS}" font-size="15" fill="#94A3B8">Built to be read in 30 seconds. Every claim links to evidence.</text></svg>'''
    (OUT / "footer.svg").write_text(s, encoding="utf-8")

if __name__ == "__main__":
    hero(); stats(); cards(); skills(); footer()
    for n, l in [("work", "Selected work"), ("skills", "Skills"), ("activity", "Activity"), ("recognition", "Recognition"), ("now", "Now")]:
        divider(n, l)
    button("linkedin", "LinkedIn", "#38BDF8"); button("email", "Email me", "#F472B6"); button("doi", "Research · Zenodo", "#A78BFA"); button("th", "ภาษาไทย", "#34D399")
    print("assets written to", OUT)
