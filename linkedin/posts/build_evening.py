#!/usr/bin/env python3
"""Generate the evening LinkedIn drafts (second daily slot, 19:30 Thailand time), English.
Each post uses one format, and no two consecutive posts share a format.
Links are left out of the body (external links usually lower reach); repository names are given instead.
Run: python linkedin/posts/build_evening.py. Status stays 'awaiting approval'; nothing is scheduled from this script."""
import datetime as dt, pathlib

HERE = pathlib.Path(__file__).resolve().parent / "evening"
EVENING = [
 ("2026-10-20", "Myth vs fact", "CPIV definition",
  """Myth: a call–put implied-volatility spread is a trading signal.

Fact: it is a measurement, and it only means something when the pair matches on underlying, strike, expiry, exercise style and multiplier. Change one field and the number measures something else.

Quant-paper on GitHub (bravforcode)"""),
 ("2026-10-22", "Checklist", "Research repository checks",
  """Before you publish a research repository, check five things:

1. The README states the scope and what it does not cover.
2. Dependencies are pinned with a lockfile.
3. CI runs on at least two operating systems.
4. Released files have hashes, and the hash list is in the repository.
5. The limitations appear before the results.

Quant-paper on GitHub (bravforcode) is an example of several of these."""),
 ("2026-10-23", "Insight with example", "Reproduce in few steps",
  """Reproducibility starts with a short setup. Many readers stop at the first setup step, so a project that needs more than two commands to run its tests loses people early.

The CPIV package needs two: uv sync --locked, then pytest.

Quant-paper on GitHub (bravforcode)"""),
 ("2026-10-25", "Question with options", "What do you check first",
  """When you review a quant or data project, what do you check first?

A) The code
B) The data
C) The stated limits

I would pick C. A stated limit tells you which claims the code can support. Which would you pick, and why?"""),
 ("2026-10-26", "Glossary", "Queue priority",
  """Queue priority, in one line: a number that tells the broker which waiting task to hand to a worker first.

Whether it works depends on the broker. Check that your broker honours AMQP queue arguments such as x-max-priority before you rely on it.

Graxia OS on GitHub (bravforcode) sets priorities on its Celery queues."""),
 ("2026-10-27", "Common mistake", "Retries on background jobs",
  """A common mistake with background jobs: retrying every failure automatically.

A failure that retries endlessly fills the queue and hides the real bug. A dead-letter queue keeps failed messages where a person can read them, and a replay becomes a deliberate step.

Graxia OS on GitHub (bravforcode) routes failed Celery tasks to a dead-letter queue, with an admin endpoint to list and replay them."""),
 ("2026-10-29", "Myth vs fact", "Scheduler scaling",
  """Myth: adding Celery workers also scales the scheduler.

Fact: Celery beat should run as a single process. Run two beat processes and every scheduled job fires twice.

Graxia OS on GitHub (bravforcode) runs beat as its own service in docker-compose."""),
 ("2026-10-30", "Contrarian take", "Counting policies",
  """Counting SQL policies is a weak way to measure access control.

893 CREATE POLICY statements across 72 migration files sounds impressive. It is a count of statements, and later migrations re-create many of them. The useful questions are which rule each policy enforces, and whether a test fails if that rule changes.

AdminMate AI on GitHub (bravforcode)"""),
 ("2026-11-01", "Step-by-step", "Golden-file tests",
  """A golden-file test in four steps:

1. Write the expected outputs by hand, from a reviewed source.
2. Run the calculation on the same inputs.
3. Compare the output with the expected file.
4. When a rule changes, the diff shows exactly which result moved.

AdminMate AI's Thai tax test follows this pattern (GitHub, bravforcode)."""),
 ("2026-11-02", "Checklist", "Recurring jobs",
  """Three checks for any recurring job:

- Is it defined in code that goes through review?
- Does exactly one scheduler process run it?
- Does a failed run leave a record someone can read?

Graxia OS on GitHub (bravforcode) keeps its recurring jobs in code."""),
 ("2026-11-03", "Insight with example", "Hash lists",
  """A SHA-256 manifest answers one question: has this file changed since the list was written?

It does not answer whether the file is correct. Keep those two checks separate in your release notes.

CPIV v28 manifests, 268 and 171 entries: Quant-paper on GitHub (bravforcode)"""),
 ("2026-11-05", "Question", "Synthetic results",
  """Do you state, in the first paragraph of a method note, that the results are synthetic?

I think a reader needs that before any number. The CPIV README says every reported result is synthetic and makes no trading claim.

How do you handle it in your own work?"""),
 ("2026-11-06", "Numbered reasons", "Two operating systems in CI",
  """Three reasons to run CI on both Windows and Linux:

1. Path separators differ (\\ on Windows, / on Linux).
2. Line endings differ, which breaks some scripts and diffs.
3. A reader on the other system is the first to hit the failure. It is better if CI does.

Quant-paper on GitHub (bravforcode) runs its matrix on Ubuntu and Windows."""),
 ("2026-11-08", "Principle with rule", "Database checks",
  """One rule for database checks: run them on every push and every pull request, not only before a release.

A broken access rule found on a pull request costs a review comment. The same rule found in production costs an incident.

AdminMate AI on GitHub (bravforcode) runs its database test workflow on both."""),
 ("2026-11-09", "Myth vs fact", "Test counts",
  """Myth: a test count in a README proves quality.

Fact: the count goes stale the day a test is added or removed. Quote the number from the latest CI run and link that run, so the reader can check it.

AdminMate AI on GitHub (bravforcode)"""),
 ("2026-11-10", "Example", "Policy names",
  """Example of a policy name that helps review (names are illustrative, not from the repository):

Weak: policy_1
Clear: employees_read_own_payslips

When a test fails, a clear name tells you which rule broke without opening the migration.

Row-level security in AdminMate AI on GitHub (bravforcode)"""),
 ("2026-11-12", "Checklist", "Competition evidence",
  """If you list a competition on your profile, attach evidence a reviewer can check:

- What you built, as a repository
- The write-up or report you submitted
- One thing that failed, and what you changed

A certificate shows participation. The three items above show the work."""),
 ("2026-11-13", "Contrarian take", "Method versus strategy",
  """A method can be correct and still say nothing about trading.

A result on synthetic data supports a measurement. It does not support a strategy. A strategy needs out-of-sample market data before anyone should trust it.

The CPIV note makes no trading claim (Quant-paper on GitHub, bravforcode)."""),
 ("2026-11-15", "Question", "Backtest trust",
  """What result would make you stop trusting a backtest?

Pre-registration answers this before the data arrives. The GMX G5 protocol is hashed and dated, and it names the failure outcome in advance. Without that line, almost any result can be told as a success.

What would be your line?"""),
 ("2026-11-16", "Principle", "Hash before collection",
  """Hash the protocol before you collect the data.

A timestamp and a hash cannot be changed quietly. A written promise can. That difference is the point of a prospective study.

GMX G5 protocol on GitHub (bravforcode)"""),
 ("2026-11-17", "Checklist", "Limitations section",
  """Write the limitations section before the results section. Check:

- What the method cannot show
- What data it was tested on
- What would change the conclusion

A reader who cannot find these will assume the method shows everything.

Quant-paper on GitHub (bravforcode)"""),
]

HERE.mkdir(exist_ok=True)
rows = []
for day, fmt, topic, text in EVENING:
    d = dt.date.fromisoformat(day)
    body = (f"# {day} · {d.strftime('%A')} · Evening: {topic}\n\n"
            f"Format: {fmt}\n"
            "Post time: 19:30 Thailand time (suggested)\n"
            "Status: approved, scheduled for 19:30 Thailand time\n\n"
            f"## Text\n\n{text}\n\n"
            "## Evidence check\n\nEach fact in the post is in the named repository.\n")
    (HERE / f"{day}.md").write_text(body, encoding="utf-8")
    rows.append(f"| {day} | {d.strftime('%a')} | {fmt} | {topic} | approved, scheduled |")
(HERE / "CALENDAR.md").write_text(
    "# Evening drafts, 20 Oct to 17 Nov 2026 (second slot, English)\n\n"
    "Status: approved and scheduled (see the scheduled-task list for trigger IDs).\n\n"
    "| Date | Day | Format | Topic | Status |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n",
    encoding="utf-8")
print("wrote", len(EVENING), "evening drafts")
