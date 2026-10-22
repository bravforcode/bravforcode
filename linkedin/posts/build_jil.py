#!/usr/bin/env python3
"""Generate the JIL-paper LinkedIn drafts (third slot, 10:00 Thailand time, on each remaining posting day).
Facts come from the published article: 'AI Audit Lab: A Phase 1 Design-and-Development Framework and Evaluation
Protocol for Auditing AI-Assisted Machine-Learning Workflows' (JIL, published 15 Oct 2026).
Run: python linkedin/posts/build_jil.py. Links stay out of the body; the article is named instead."""
import datetime as dt, pathlib

HERE = pathlib.Path(__file__).resolve().parent / "jil"
JIL = [
 ("2026-10-23", "Announcement", "Paper published in JIL",
  """New paper, published in JIL on 15 October 2026: AI Audit Lab, a design-and-development framework for auditing AI-assisted machine-learning workflows.

Fact you should know: it is a Phase 1 paper. It describes the design and the development. It has not been tested with learners, and it makes no claim of teaching effectiveness.

Search "AI Audit Lab" in JIL (Mahidol University) to read it."""),
 ("2026-10-25", "Insight", "The skill gap",
  """Generative AI can write a working notebook in one prompt. Judging whether its conclusions hold is a separate skill, and most courses teach only the first one.

The AI Audit Lab paper treats AI output as a claim to verify, not as an answer to accept."""),
 ("2026-10-26", "Fact with source", "Leakage in published research",
  """Fact you should know: Kapoor and Narayanan (2023) found data leakage in at least 294 published studies written by trained researchers.

Leakage means information from outside the training set influences training or evaluation. In some of those studies, the leak inflated accuracy enough that the claim did not survive correction."""),
 ("2026-10-27", "Steps", "The five-step audit cycle",
  """The audit cycle in the AI Audit Lab has five steps:

1. Inspect the AI-written notebook and its summary.
2. Predict which step is suspect, before any tool help.
3. Test with deterministic checks that return only PASS or FAIL.
4. Repair the pipeline and rerun both versions.
5. Explain what was wrong and whether the corrected result still supports the recommendation."""),
 ("2026-10-29", "Contrarian take", "Same score, invalid workflow",
  """A workflow can be invalid and still produce the same score.

In the paper's first demonstration, a scaler fitted before the train–test split and a scaler fitted after it gave the same mean AUC to four decimals: 0.7808 on synthetic data.

A metric that does not move does not prove the pipeline is valid."""),
 ("2026-10-30", "Example with numbers", "A proxy that leaks the label",
  """The paper's second demonstration uses a noisy proxy of the outcome, recorded after the outcome, as a stand-in for target leakage.

On the same synthetic dataset, mean AUC was 0.9869 with the proxy and 0.7808 without it.

Synthetic data, one dataset, one run. The point is the size of the inflation, not a real-world estimate."""),
 ("2026-11-01", "Glossary", "Tier 1 feedback",
  """Tier 1 feedback in the AI Audit Lab checks one deterministic property, such as no row appearing in both train and test sets.

It returns PASS or FAIL and does not name the cause. The learner has to find the cause.

Passing Tier 1 does not mean the whole workflow is valid. It checks only the property it tests."""),
 ("2026-11-02", "Principle", "Hypothesis before help",
  """A tutor should not explain the specific bug until the learner has committed to a hypothesis.

The AI Audit Lab tutor works this way. Before a hypothesis is submitted, it only asks questions or explains general concepts. The rule is written as a policy layer, not a single prompt, because a prompt alone is easy to bypass."""),
 ("2026-11-03", "Numbered list", "Eight error scenarios",
  """The AI Audit Lab specifies eight error scenarios in three validity categories:

Data and pipeline leakage: feature availability, temporally invalid splits, target leakage, preprocessing leakage, group leakage, test-set reuse.

Evaluation: misuse of accuracy on imbalanced labels.

Interpretation: correlation described as causation.

Only four of the eight are implemented in the Phase 1 package. The rest are design-level."""),
 ("2026-11-05", "Limits first", "What the paper does not claim",
  """Limits, stated first, as the paper does:

- No expert review yet
- No usability test yet
- No learner trial yet
- No claim of pedagogical effectiveness

A framework is a design until someone tests it. The paper says so in its abstract."""),
 ("2026-11-06", "Walkthrough", "How the synthetic data was built",
  """How the demonstration data was built, so anyone can check it:

- Synthetic, generated with scikit-learn make_classification
- 4,000 records and 20 features (8 informative, 4 redundant)
- 20% positive class, random seed 42
- AUC averaged over 20 stratified 75/25 splits

Pinned versions: numpy 2.2.6 and scikit-learn 1.7.1. The code is in the paper's supplementary material under MIT."""),
 ("2026-11-08", "Design outline", "Phase 2 protocol",
  """The Phase 2 protocol in the AI Audit Lab is a split-plot design:

1. Learners are randomized to standard AI tutoring or the Audit Lab.
2. Both conditions use the same model, scenarios and checks.
3. A delayed transfer task is done without AI.
4. The primary outcome is the Tier 1 pass rate after the first repair.

It names seven threats to internal validity, each with a control. None of this has been run yet."""),
 ("2026-11-09", "Connection to research", "Productive failure",
  """Productive failure (Kapur, 2008) holds that learners who struggle first can build more durable understanding, if the struggle is structured and followed by instruction.

A meta-analysis found this for conceptual knowledge and transfer, but not for procedural knowledge (Sinha and Kapur, 2021). The AI Audit Lab borrows the first idea. Whether it works for auditing code is an open question."""),
 ("2026-11-10", "Question", "Fix or write",
  """Do you learn more from finding and fixing an error in a worked example, or from writing the correct solution yourself?

Research on erroneous examples reports transfer benefits for learners with enough prior knowledge (Große and Renkl, 2007). The answer depends on what you already know."""),
 ("2026-11-12", "Disclosure", "How AI was used",
  """Disclosure for my paper in JIL: I used AI tools for literature search, programming help and language editing.

I personally ran and checked all code, verified every numerical result, and checked every reference against its original source. The paper says this in its acknowledgements."""),
 ("2026-11-13", "Example", "Association is not a cause",
  """Example of one error the AI Audit Lab targets:

"Feature X predicts churn, so feature X drives churn."

A predictive association is not a causal driver. The framework treats this as a validity failure in the report, separate from leakage."""),
 ("2026-11-15", "Question", "Trusting AI analysis",
  """What would you need to see before trusting an AI-written data analysis?

For me the list starts with: the split logic, the fit order of preprocessing, and a result that changes when the pipeline is wrong on purpose."""),
 ("2026-11-16", "Principle", "Write the failure criteria first",
  """Write the failure criteria before you run the test.

The Phase 2 protocol of the AI Audit Lab names its primary outcome, its controls and its threats in advance. Without that, any result can be described as a success."""),
 ("2026-11-17", "Checklist", "Before any effectiveness claim",
  """Before any claim that an educational tool works, check:

- Expert review of the design
- A pilot with real learners
- A power simulation from pilot data
- Red-team testing of the tutor policy
- A pre-registered outcome

The AI Audit Lab has none of these yet. Its paper is a Phase 1 design."""),
]

HERE.mkdir(exist_ok=True)
rows = []
for day, fmt, topic, text in JIL:
    d = dt.date.fromisoformat(day)
    body = (f"# {day} · {d.strftime('%A')} · JIL paper: {topic}\n\n"
            f"Format: {fmt}\n"
            "Post time: 10:00 Thailand time (suggested)\n"
            "Status: scheduled (see calendar)\n\n"
            f"## Text\n\n{text}\n\n"
            "## Evidence check\n\nEvery number and claim is in the published article.\n")
    (HERE / f"{day}.md").write_text(body, encoding="utf-8")
    rows.append(f"| {day} | {d.strftime('%a')} | {fmt} | {topic} | scheduled |")
(HERE / "CALENDAR.md").write_text(
    "# JIL paper posts, 23 Oct to 17 Nov 2026 (third slot, 10:00 Thailand time)\n\n"
    "Source: AI Audit Lab, JIL (published 15 Oct 2026). Phase 1 only; no effectiveness claims.\n\n"
    "| Date | Day | Format | Topic | Status |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n",
    encoding="utf-8")
print("wrote", len(JIL), "JIL drafts")
