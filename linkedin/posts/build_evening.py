#!/usr/bin/env python3
"""Generate the evening LinkedIn drafts (second daily slot, 19:30 Thailand time), English, fact-first.
Run: python linkedin/posts/build_evening.py. Status stays 'awaiting approval'; nothing is scheduled from this script."""
import datetime as dt, pathlib

HERE = pathlib.Path(__file__).resolve().parent / "evening"
EVENING = [
 ("2026-10-20", "Call–put spread definition",
  """Fact you should know: a call–put implied-volatility spread only means something when the two options match on underlying, strike, expiry, exercise style and multiplier. Change one field and the number measures something else.

Example definition and limits: github.com/bravforcode/Quant-paper"""),
 ("2026-10-22", "Scope of a research repository",
  """Fact you should know: a research repository that mixes unrelated code is harder to audit. State the scope of each release in the README, and say which folders are outside it.

github.com/bravforcode/Quant-paper"""),
 ("2026-10-23", "Lockfiles and two operating systems",
  """Fact you should know: many "it runs on my machine" failures come from dependencies that were never pinned. A lockfile plus a CI run on two operating systems catches most of them before a reader does.

github.com/bravforcode/Quant-paper"""),
 ("2026-10-25", "Synthetic data and method claims",
  """Fact you should know: synthetic data can test a measurement method. It cannot show how that method behaves on real market data. Say which one you tested, in the first paragraph.

github.com/bravforcode/Quant-paper"""),
 ("2026-10-26", "Queue priority depends on the broker",
  """Fact you should know: queue arguments such as x-max-priority are AMQP settings. Before you rely on Celery queue priorities, confirm which broker you run and that it honours them.

github.com/bravforcode/graxia-os (backend/app/tasks/queues.py)"""),
 ("2026-10-27", "Failed tasks need a visible place",
  """Fact you should know: a failed background task should land somewhere you can read it. A dead-letter queue keeps failures visible, and replaying them should be an explicit action, not an automatic retry.

github.com/bravforcode/graxia-os (backend/app/api/admin.py)"""),
 ("2026-10-29", "Run the scheduler once",
  """Fact you should know: Celery beat should run as a single process. Running more than one scheduler duplicates every scheduled job, and scaling workers does not fix that.

github.com/bravforcode/graxia-os (docker-compose.yml)"""),
 ("2026-10-30", "Counting policies is not counting rules",
  """Fact you should know: counting SQL policy statements does not count access rules. A policy re-created in a later migration is one rule written more than once.

github.com/bravforcode/adminmate-ai (supabase/migrations)"""),
 ("2026-11-01", "Golden-file tests for calculations",
  """Fact you should know: a golden-file test pins a calculation to reviewed expected values. When a rate changes, the test shows a diff instead of a silent change in the output.

github.com/bravforcode/adminmate-ai (tests/unit/payroll)"""),
 ("2026-11-02", "Schedules belong in code",
  """Fact you should know: a recurring job defined in code goes through review like any other change. A job set up by hand on a server does not, and it is hard to find later.

github.com/bravforcode/graxia-os (backend/app/tasks/celery_app.py)"""),
 ("2026-11-03", "A hash list proves less than it seems",
  """Fact you should know: a SHA-256 manifest proves the files have not changed since it was written. It does not prove the files are correct.

github.com/bravforcode/Quant-paper (reports/)"""),
 ("2026-11-05", "Say what a result is not",
  """Fact you should know: every result in the CPIV note is synthetic, and the README says so first. A reader needs that line before the numbers, because it sets what the numbers can support.

github.com/bravforcode/Quant-paper"""),
 ("2026-11-06", "Why CI on Windows and Linux",
  """Fact you should know: Windows and Linux differ in path separators and line endings. Running a CI matrix on both catches the failures a reader on the other system would hit first.

github.com/bravforcode/Quant-paper (.github/workflows/cpiv-repro.yml)"""),
 ("2026-11-08", "Database checks on every pull request",
  """Fact you should know: a database test that runs on every pull request shows a broken access rule before the merge decision. Run it on push as well, so the main branch gets the same check.

github.com/bravforcode/adminmate-ai (.github/workflows/db-test.yml)"""),
 ("2026-11-09", "Quote the CI run, not the README",
  """Fact you should know: a test count written in a README goes stale. Quote numbers from the latest CI run, and link to that run.

github.com/bravforcode/adminmate-ai"""),
 ("2026-11-10", "Access control belongs in the database",
  """Fact you should know: row-level security is enforced by the database. A hidden button in the interface is not an access control.

github.com/bravforcode/adminmate-ai (supabase/migrations)"""),
 ("2026-11-12", "A certificate proves participation",
  """Fact you should know: a competition certificate proves you took part. Reviewers look for what the work produced, such as code, a write-up, and what failed along the way.

github.com/bravforcode"""),
 ("2026-11-13", "A method note is not a trading strategy",
  """Fact you should know: a method note can be correct and still say nothing about trading. A result on synthetic data supports a measurement, not a strategy.

github.com/bravforcode/Quant-paper"""),
 ("2026-11-15", "Define failure before the data arrives",
  """Fact you should know: a pre-registered protocol names what would count as failure before the data arrives. Without that line, a result can be described as a success whatever it shows.

github.com/bravforcode/gmx-g5-prospective-2026"""),
 ("2026-11-16", "Hash the protocol before collection",
  """Fact you should know: hashing a study protocol before data collection makes later changes visible. The timestamp and hash do the work that a promise cannot.

github.com/bravforcode/gmx-g5-prospective-2026"""),
 ("2026-11-17", "Limitations come before results",
  """Fact you should know: a limitations section belongs before the results. A reader who cannot find what a method cannot show will assume it shows everything.

github.com/bravforcode/Quant-paper"""),
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
    "# Evening drafts, 20 Oct to 17 Nov 2026 (second slot, English, fact-first)\n\n"
    "Status: awaiting approval. Nothing here is scheduled.\n\n"
    "| Date | Day | Topic | Status |\n|---|---|---|---|\n" + "\n".join(rows) + "\n",
    encoding="utf-8")
print("wrote", len(EVENING), "evening drafts")
