#!/usr/bin/env python3
"""Generate the 30-day LinkedIn calendar (19 Oct to 17 Nov 2026).
Run: python linkedin/posts/build_posts.py. Every number in the text must match a file in the linked repositories.
Comment templates use [your ...] slots that you write yourself at the time of commenting."""
import datetime as dt, pathlib

HERE = pathlib.Path(__file__).resolve().parent
START = dt.date(2026, 10, 19)
POSTED = {"2026-10-19": "posted 18 Oct 2026, urn:li:share:7517647345912610816"}
HASH = {"full": "#SoftwareEngineering #DataScience #ReproducibleResearch", "short": "#ReproducibleResearch #QuantitativeFinance", "engage": "", "summary": "#Internship #BuildInPublic"}

FULL = [
 ("Introduction: what I built this year", "Fig. 1 (assets/log-light.svg)",
  """I am a first-year student at Burapha University. This year I built three things I can point to:
• CPIV methods note: exact Black–Scholes–Merton inversion for call–put pairs, archived with a DOI (10.5281/zenodo.23442601).
• GMX G5 prospective record: protocol hashed before the baseline, then collected on a fixed UTC schedule.
• JobShield AI: a career-path recommender with a live demo and 145 tests. Its input is 153 hand-written sample postings, not live labour-market data.
I am looking for a 2027 internship in software, data, machine learning or quantitative research. Every claim links to its repository.

ผมเป็นนักศึกษาปี 1 มหาวิทยาลัยบูรพา กำลังหาฝึกงานปี 2027 ผลงานทุกชิ้นมีลิงก์หลักฐาน""",
  "github.com/bravforcode · doi.org/10.5281/zenodo.23442601"),
 ("CPIV deep-dive", "Screenshot of the CI run and the SHA-256 manifest file in Quant-paper (capture from GitHub)",
  """Question: how reliable is a call–put implied-volatility spread when quotes are noisy?

Method: exact BSM inversion for matched pairs, then simulated quote noise to see where the spread stops being informative.

What it does not show: no market data, no trading claim, and no independent replication yet. The results come from a synthetic generator, not from market quotes.

What makes it checkable: a uv lockfile, CI on Ubuntu and Windows across Python 3.12–3.14, and SHA-256 manifests for the review package (268 entries) and the CPIV-only subset (171 entries).

Read the note and its limitations: github.com/bravforcode/Quant-paper""",
  "github.com/bravforcode/Quant-paper · doi.org/10.5281/zenodo.23442601"),
 ("Why query a historical UTC snapshot", "Snapshot schedule table from gmx-g5-prospective-2026/README (capture)",
  """Why does the GMX G5 collector query a specified historical UTC snapshot instead of "now"?

Scheduled jobs can run late or be skipped. If the script used the runner's clock, a late run would silently record a different moment. The collector always queries the snapshot it was asked for.

The protocol was hashed on 26 Sep 2026, before the 27 Sep baseline. Protocol SHA-256 efa241ab…

Lesson: the time a value refers to should be an input to the code, not the time the code happens to run.""",
  "github.com/bravforcode/gmx-g5-prospective-2026"),
 ("Why wage stays out of the path cost", "Architecture diagram from jobsume.vercel.app/mechanism (capture)",
  """Why keep wage out of the path cost in a career recommender?

If wage is part of the edge cost, a high-paying job can make a path look cheaper, and the non-negative weights that Dijkstra needs stop being guaranteed.

So JobShield splits the work. Layer 1 finds paths with non-negative edge costs. Layer 2 ranks destinations using wage, so wage never changes the path search itself.

The input is 153 hand-written sample postings, so read the output as a demonstration of the method, not as labour-market fact. 145 tests in the repository: github.com/bravforcode/jobshield-ai""",
  "github.com/bravforcode/jobshield-ai"),
 ("Human approval before anything is sent", "Celery queue diagram (draw from graxia-os README architecture)",
  """Agent tools should not send anything on their own.

In Graxia OS a lead can be scored and a draft written automatically, but the draft waits for a human approval before anything goes out.

Background work runs on Celery in four queues: critical, default, background and dead-letter. A failing task ends up in the dead-letter queue instead of disappearing.

Stack: FastAPI, async SQLAlchemy, PostgreSQL, Redis and React. Docker Compose quickstart: github.com/bravforcode/graxia-os""",
  "github.com/bravforcode/graxia-os"),
 ("A checksum is only useful if a stranger can run it", "Terminal screenshot of the verifier (capture)",
  """A checksum manifest is only useful if a stranger can run it.

The CPIV review package has SHA-256 manifests: 268 entries for the full package and 171 for the CPIV-only subset.

The verifier I have is a PowerShell script (scripts/verify_sha256_manifest.ps1). Linux and macOS users would need PowerShell installed first, so the check is not portable yet. A portable version is the next step.

Lesson: write the verification step in a language your readers already have, then test it on a clean machine.""",
  "github.com/bravforcode/Quant-paper/tree/master/reports"),
 ("Access rules belong in the database", "Screenshot of a pgTAP run (capture from adminmate-ai CI)",
  """Where should access control live in an HR app?

In AdminMate AI I put row-level security in the database, not only in the interface. A hidden button is not a permission.

The database rules are tested with pgTAP files in supabase/tests.

Thai tax calculations are checked with a golden-file test, so a change to a tax result shows up as a test diff.

Stack: React 19, TypeScript and Supabase. github.com/bravforcode/adminmate-ai""",
  "github.com/bravforcode/adminmate-ai"),
 ("AI Thailand Benchmark 2026", "Certificate image (blur names and IDs first)",
  """AI Thailand Benchmark (NECTEC), 2026: I qualified for three challenges.
• LOTUSDIS, distant-meeting transcription (March)
• Meeting Minutes Summarization (May)
• LLM Trustworthiness (July)

Profile and evidence index: github.com/bravforcode""",
  "github.com/bravforcode/bravforcode"),
 ("Mahidol × Harvard Health Systems Hackathon", "Schedule document (blur names first)",
  """In April 2026 I was selected as a participant in the Mahidol × Harvard Health Systems Innovation Lab Hackathon.""",
  "github.com/bravforcode"),
]

SHORT = [
 "A DOI does not make research correct. It makes it citable and checkable. The CPIV README says what it does not show: synthetic data, no alpha claim, no independent replication.",
 "Freeze the protocol before you look at the data. The GMX G5 protocol was hashed on 26 Sep 2026, the day before the baseline. Changing it later would be visible.",
 "Fixed-time snapshots beat 'whenever the job ran'. The time a number refers to is an input, not the clock of the machine that computed it.",
 "A recommender should be able to explain its path. If the explanation is weak, the ranking is not trustworthy either.",
 "An AI draft is not an action. Graxia OS keeps a human approval step before anything is sent.",
 "A test that passes on my laptop is a start. I now run CI on Ubuntu and Windows, because a script that needs one specific shell is not reproducible.",
 "A rule is only as good as the test that checks it. Name the rule in the test title, so a failure tells you what broke.",
 "Synthetic data is fine for a method note, if the first paragraph says so.",
 "Limits are part of the result. Say them first.",
]

ENGAGE_TEMPLATES = [
 ("Add a concrete experience", "Good point. I ran into something similar when [your own situation]. What did you do about [specific detail from their post]?"),
 ("Ask a specific question", "How did you handle [specific detail]? I am working on [your related project] and I am not sure whether [your open question]."),
 ("Name a limit politely", "Useful. One limit I would add, based on my own work: [your limit, stated plainly]."),
]
CONNECT = [
 "AI Thailand challenge participants (2026 cohort)",
 "Burapha University students and lecturers in computer science or electrical engineering",
 "Authors of a paper or repository you actually read this week",
 "Engineers at companies where you would apply for an internship",
 "Recruiters or hiring managers who posted an internship role",
]
CONNECT_NOTE = "Hi [name], I'm a first-year at Burapha working on reproducible data and quant research. I read your [specific post or project]. Would be glad to connect."

SUMMARIES = [
 """Question for readers: when you review a data or quant project, what do you check first: the code, the data, or the stated limits?

Projects with links: github.com/bravforcode""",
 """Question for readers: for a first internship, is a public repository with tests or a paper with a DOI more useful to a recruiter? Why?

Projects with links: github.com/bravforcode""",
 """Question for readers: what is one thing you wish a student project README had told you before you started?

Projects with links: github.com/bravforcode""",
 """Question for readers: which result would make you stop trusting a backtest?

Projects with links: github.com/bravforcode""",
]

def day_type(d):
    return {0: "full", 1: "short", 2: "engage", 3: "full", 4: "short", 5: "engage", 6: "summary"}[d.weekday()]

rows, full_i, short_i, ENG_i, sum_i = [], 0, 0, 0, 0
for n in range(30):
    d = START + dt.timedelta(days=n)
    kind = day_type(d)
    fn = HERE / f"{d.isoformat()}.md"
    if kind == "full":
        topic, image, text, link = FULL[full_i]; full_i += 1
        body = f"## Text (EN and TH)\n\n{text}\n\n"
        meta = f"Image: {image}\nLink: {link}\nHashtags: {HASH['full']}"
        label = topic
    elif kind == "short":
        text = SHORT[short_i % len(SHORT)]; short_i += 1
        body = f"## Text\n\n{text}\n"
        meta = f"Image: optional (text card)\nHashtags: {HASH['short']}"
        label = "Short note"
    elif kind == "engage":
        ENG_i += 1
        tpl = "\n".join(f"- **{t}:** {x}" for t, x in ENGAGE_TEMPLATES)
        tgt = "\n".join(f"- {c}" for c in CONNECT)
        body = (f"## Comment templates (3 comments, on posts by people in your field)\n\n{tpl}\n\n"
                f"## Connect requests (5 people, note under 300 characters)\n\n{tgt}\n\n"
                f"Note text: {CONNECT_NOTE}\n")
        meta = "Image: none\nHashtags: none"
        label = "Engage (comments and connections)"
    else:
        body = f"## Text\n\n{SUMMARIES[sum_i % len(SUMMARIES)]}\n"; sum_i += 1
        meta = f"Image: optional (weekly log screenshot)\nHashtags: {HASH['summary']}"
        label = "Weekly summary"
    head = (f"# {d.isoformat()} · {d.strftime('%A')} · {label}\n\n"
            f"Post time: 08:00–10:00 Thailand time (suggested)\n{meta}\nStatus: {POSTED.get(d.isoformat(), 'draft')}\n\n")
    check = "## Evidence check\n\nEvery number above must be a file or link in the repositories named in the post.\n"
    fn.write_text(head + body + check, encoding="utf-8")
    rows.append(f"| {d.isoformat()} | {d.strftime('%a')} | {label} | {meta.splitlines()[0].removeprefix('Image: ')} | {POSTED.get(d.isoformat(), 'draft')} |")

(HERE / "CALENDAR.md").write_text(
    "# 30-day LinkedIn calendar, 19 Oct to 17 Nov 2026\n\n"
    "Status values: draft → ready → posted.\n\n"
    "| Date | Day | Type | Image | Status |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n",
    encoding="utf-8")
print("wrote", len(list(HERE.glob("2026-*.md"))), "post files")
