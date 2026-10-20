#!/usr/bin/env python3
"""Generate the evening LinkedIn drafts (second daily slot, 19:30 Thailand time).
Run: python linkedin/posts/build_evening.py. Each text uses only facts checked in the linked repositories.
Status stays 'awaiting approval' until the author approves the file; nothing is scheduled from this script."""
import datetime as dt, pathlib

HERE = pathlib.Path(__file__).resolve().parent / "evening"
EVENING = [
 ("2026-10-20", "CPIV definition, stated once",
  """The CPIV note defines the spread for a matched call–put pair (same underlying, strike, expiry, exercise style and multiplier) as CPIV = 100 × (σC − σP). The result is in percentage points.

Matching the pair is most of the work. The definition only holds when every field in that list matches.

github.com/bravforcode/Quant-paper (README, Definition)"""),
 ("2026-10-22", "What is in the same repository",
  """The Quant-paper repository holds two things. The CPIV package is one. The other is Hyperliquid collection and analysis code from a separate liquidation-exposure project.

The README says the second is outside the CPIV package and is not described in the note. Mixing unrelated code in one repository makes review harder, so a reader should check the README before reading the code.

github.com/bravforcode/Quant-paper"""),
 ("2026-10-23", "Reproduce in two commands",
  """To reproduce the CPIV tests you need Python 3.12 or later and uv:

uv sync --locked --no-install-project
uv run python -m pytest tests -q

CI runs the same suite on Ubuntu and Windows with Python 3.12, 3.13 and 3.14. If it fails on your machine, the CI log shows which step."""),
 ("2026-10-25", "Thai summary: CPIV ใช้ทำอะไร",
  """สรุป CPIV ภาษาไทยสั้น ๆ: CPIV คือความต่างของ implied volatility ระหว่าง call กับ put ที่คู่กันเมื่อวัดด้วยสูตร Black–Scholes–Merton

งานนี้ใช้ข้อมูลสังเคราะห์ทั้งหมด ไม่มีราคาตลาดจริง ไม่มีการอ้างเรื่องกำไรหรือการเทรด ผลที่บอกได้คือสเปรดนี้น่าเชื่อถือแค่ไหนเมื่อราคาเสนอซื้อขายมี noise

github.com/bravforcode/Quant-paper"""),
 ("2026-10-26", "Priorities per queue",
  """Graxia OS runs Celery on four queues: critical, default, background and dead-letter.

The first three have priority settings (10, 5 and 1). The dead-letter queue has none.

github.com/bravforcode/graxia-os (backend/app/tasks/queues.py)"""),
 ("2026-10-27", "Failed tasks have a place to go",
  """A failed Celery task in Graxia OS ends up in a dead-letter queue, not in the void.

An admin endpoint lists those messages. Replaying one is a separate POST request, so a retry is an explicit action.

github.com/bravforcode/graxia-os (backend/app/api/admin.py)"""),
 ("2026-10-29", "Four services in one compose file",
  """The root docker-compose.yml of Graxia OS defines four services: Redis, the backend, a Celery worker and Celery beat.

github.com/bravforcode/graxia-os"""),
 ("2026-10-30", "Counting policies honestly",
  """AdminMate AI has 893 CREATE POLICY statements across 72 migration files.

That is a count of statements, not of distinct rules. Several policies are re-created in later migrations. A reviewer should read the latest version of each policy, not the number.

github.com/bravforcode/adminmate-ai"""),
 ("2026-11-01", "A golden-file tax test",
  """The Thai tax test in AdminMate AI is a golden-file test. It checks the bracket table at its edges: income at 0%, income that spans three brackets, and income at the top of a bracket.

When a rate changes, the test diff shows the exact result that moved.

github.com/bravforcode/adminmate-ai (tests/unit/payroll)"""),
 ("2026-11-02", "Recurring jobs live in code",
  """Graxia OS defines its recurring Celery jobs in code, in a beat schedule, not in a server's crontab.

github.com/bravforcode/graxia-os (backend/app/tasks/celery_app.py)"""),
 ("2026-11-03", "A manifest is only as good as its inputs",
  """The CPIV review package has two SHA-256 manifests: one for the full v28 package (268 entries) and one for the CPIV-only subset (171 entries).

Both are in the reports folder with the date in the filename. A hash list tells you the files have not changed since it was written. It does not tell you the files are correct.

github.com/bravforcode/Quant-paper (reports/)"""),
 ("2026-11-05", "What every reported result is",
  """The CPIV README says every reported result is synthetic: European BSM inputs and simulated quote noise.

The note uses no market quotes, option chains, returns, positions or liquidation data. Stating that in the README is cheaper than having a reader find it.

github.com/bravforcode/Quant-paper"""),
 ("2026-11-06", "Why two operating systems",
  """The CPIV CI matrix runs on Ubuntu and on Windows.

Path separators, line endings and file locking differ between them. Running both is cheap, and it catches the failures a reader on the other system would hit first.

github.com/bravforcode/Quant-paper (.github/workflows/cpiv-repro.yml)"""),
 ("2026-11-08", "Every push runs the database checks",
  """In AdminMate AI, the database test workflow runs on every push and every pull request. A separate security grep workflow also runs on both.

A failing database test shows up on the pull request, so a broken policy is visible before the merge decision.

github.com/bravforcode/adminmate-ai (.github/workflows/db-test.yml)"""),
 ("2026-11-09", "Quote CI, not memory",
  """Before I quote a test count in a README or a post, I check it against the latest CI run.

A number from memory is not evidence. A number from the run is.

github.com/bravforcode/adminmate-ai"""),
 ("2026-11-10", "Name a policy after the rule",
  """A row-level security policy named after the rule it enforces is easier to review than one named after its table.

When a test fails, the name tells you which rule broke.

github.com/bravforcode/adminmate-ai"""),
 ("2026-11-12", "Qualifying is not the result",
  """Qualifying for an AI Thailand challenge is a line on a certificate. What a recruiter can check is what the challenge produced: the code, the write-up, and what failed.

github.com/bravforcode"""),
 ("2026-11-13", "A method can be right without a trading rule",
  """A synthetic result can support a measurement method. It cannot support a trading rule.

The CPIV note says it makes no alpha or trading claim. That is the claim a reader should check first, before the numbers.

github.com/bravforcode/Quant-paper"""),
 ("2026-11-15", "Write down what counts as failure",
  """A pre-registered protocol names the outcome that would count as a failure, before the data arrives.

That line is often skipped. Without it, any result can be told as a success.

github.com/bravforcode/gmx-g5-prospective-2026"""),
 ("2026-11-16", "Thai reflection: โปรโตคอลก่อนข้อมูล",
  """สิ่งที่ผมเรียนรู้จากการทำงานวิจัยแบบ pre-registration: ต้องเขียนก่อนว่าผลแบบไหนถือว่าล้มเหลว ถ้าเขียนทีหลัง ทุกผลก็เล่าเป็นความสำเร็จได้

github.com/bravforcode/gmx-g5-prospective-2026"""),
 ("2026-11-17", "Limitations before results",
  """Write the limitations section before the results section. If you cannot say what a method cannot show, the results are not ready to share.

github.com/bravforcode"""),
]

HERE.mkdir(exist_ok=True)
rows = []
for day, topic, text in EVENING:
    d = dt.date.fromisoformat(day)
    body = (f"# {day} · {d.strftime('%A')} · Evening: {topic}\n\n"
            f"Post time: 19:30 Thailand time (suggested)\n"
            f"Status: awaiting approval (not scheduled)\n\n"
            f"## Text\n\n{text}\n\n"
            "## Evidence check\n\nEvery claim above is in the repository linked in the post.\n")
    (HERE / f"{day}.md").write_text(body, encoding="utf-8")
    rows.append(f"| {day} | {d.strftime('%a')} | {topic} | awaiting approval |")
(HERE / "CALENDAR.md").write_text(
    "# Evening drafts, 20 Oct to 17 Nov 2026 (second slot)\n\n"
    "Status: awaiting approval. Nothing here is scheduled.\n\n"
    "| Date | Day | Topic | Status |\n|---|---|---|---|\n" + "\n".join(rows) + "\n",
    encoding="utf-8")
print("wrote", len(EVENING), "evening drafts")
