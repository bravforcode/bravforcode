# LinkedIn copy, advanced version (paste-ready)

Every number below comes from a file in the linked repository. Do not add a number you cannot link.

## Headline
Full-Stack and AI engineer · Data / Quant research · Reproducible systems · Burapha University · Seeking 2027 internship

## About
I build software and research that other people can re-run and check.

My strongest evidence is research. The CPIV methods note (call–put implied-volatility spreads) is archived with a DOI, ships a SHA-256 manifest for its 268-file review package, and passes CI on Ubuntu and Windows across Python 3.12, 3.13 and 3.14. For the GMX G5 study I froze and hashed the protocol before the first observation, then collected four fixed-UTC snapshots a day and stored aggregate receipts only. Both state their limits: synthetic data, no alpha claim, no independent replication yet.

On the engineering side I build data and agent systems end to end: FastAPI and Celery workers with a cost-aware model router and a human approval step (Graxia OS); a React 19 and Supabase HR platform whose access rules live in row-level security (AdminMate AI); a skill-graph career recommender with a two-layer Dijkstra and ranking model and a live demo (JobShield AI, 145 tests).

I am a first-year student at Burapha University, qualified for three NECTEC AI Thailand challenges in 2026, and I am looking for a 2027 internship in software engineering, data science, machine learning or quantitative research.

Evidence for every claim: github.com/bravforcode · nxme176@gmail.com

ผมทำซอฟต์แวร์และงานวิจัยที่คนอื่นรันซ้ำและตรวจสอบได้ กำลังมองหาฝึกงานปี 2027

## Experience

### Independent Researcher (Quantitative Finance) · Self-employed · Sep 2025 – Present · Chonburi, Thailand
Independent, reproducible research on options and on-chain derivatives data.
• Derived exact Black–Scholes–Merton inversion for matched call–put pairs and measured how reliable the implied-volatility spread is under simulated quote noise; archived the review package (v28) with a DOI.
• Shipped the work as a reproducible artefact: locked dependencies (uv), CI on 2 operating systems × 3 Python versions, and SHA-256 manifests of 268 and 171 files with a verifier script.
• Pre-registered a prospective study (GMX G5): froze and hashed the protocol before the baseline, scheduled four fixed-UTC snapshots a day through GitHub Actions, and kept only aggregate receipts with no wallet addresses.
• Wrote the limitations first: synthetic data only, no trading claim, no independent replication yet.
Skills: Python · Statistics · GitHub Actions · SQL
Media: https://doi.org/10.5281/zenodo.23442601 · https://github.com/bravforcode/gmx-g5-prospective-2026

### Freelance Full-Stack Developer · Self-employed · Jan 2026 – Present · Chonburi, Thailand
Built and delivered web applications for small clients through the Fastwork marketplace.
• Owned the full cycle alone: requirements, architecture, development, deployment and maintenance.
• Built dashboards, websites and automation scripts with React, Next.js, TypeScript and Python; added AI features (text generation, document parsing) where a brief needed them.
• [FILL if true and linkable: "N completed orders on Fastwork" or one client-approved case study.]
Skills: React.js · Next.js · TypeScript · Python · SQL

### Participant · NECTEC, AI Thailand Benchmark Programs · Mar 2026 – Jul 2026
Qualified for three national challenges: LOTUSDIS distant-meeting transcription (Mar), Meeting Minutes Summarization (May) and LLM Trustworthiness (Jul).
Skills: Speech Recognition (ASR) · Large Language Models
Media: certificates/ai-thailand-*.pdf in github.com/bravforcode/bravforcode

## Projects

**CPIV methods note** · Oct 2026 · github.com/bravforcode/Quant-paper
• Problem: is the call–put implied-volatility spread a reliable measurement when quotes are noisy? Method: exact BSM inversion plus simulated quote noise. Result: a DOI-archived note whose rankings are stated to hold only for the chosen synthetic generator and seeds.
• Reproducible by design: `uv sync --locked`, pytest in CI on Ubuntu and Windows (Python 3.12–3.14), SHA-256 manifests (268 and 171 entries).

**GMX G5 prospective record** · Sep–Oct 2026 · github.com/bravforcode/gmx-g5-prospective-2026
• Froze and hashed the protocol (SHA-256 `efa241ab…`) 6 hours before the baseline; collection at 00:25, 06:25, 12:25 and 18:25 UTC, always querying the specified historical snapshot rather than the runner's clock, with retries for missed receipts.

**JobShield AI** · Aug 2026 · jobsume.vercel.app
• Two-layer recommender: Dijkstra on a non-negative cost (skill distance and automation risk) for paths, then a separate ranking layer for wage gain, so wage never enters path cost.
• PPMI skill graph over 153 hand-written postings (18 occupations, 46 skills, 119 transitions); OLS wage-gap radar; 145 Python tests; Next.js 16 front end. Data is mock and the site says so.

**Graxia OS** · 2026 · github.com/bravforcode/graxia-os
• FastAPI + async SQLAlchemy + PostgreSQL control plane; Celery workers on four queues (critical, default, background, dead-letter); cost-aware model router with per-tier usage ceilings; every outbound draft waits for human approval.
• JWT, CSRF and rate limiting; Docker Compose quickstart; backend tests and Playwright end-to-end tests.

**AdminMate AI** · 2026 · github.com/bravforcode/adminmate-ai
• React 19, TypeScript and Supabase HR platform from recruitment to payroll; access control enforced with row-level security and tested with pgTAP; Thai payroll rules covered by a golden-file test.

## Featured captions
1. CPIV methods note — "DOI-archived measurement note. Reproducible: locked deps, CI on 2 OS × 3 Python, SHA-256 manifest."
2. GMX G5 prospective record — "Protocol hashed before the first observation. Fixed-UTC collection, aggregate receipts only."
3. JobShield AI (live) — "Explainable career-path recommender, two-layer model, 145 tests. Mock data, stated openly."
4. Graxia OS — "Agent control plane with a human approval gate. FastAPI, Celery, Redis."

## Skills order (top 3 pinned)
Python · SQL · TypeScript · PostgreSQL · FastAPI · React.js · Next.js · Docker · Supabase · Redis · Celery · Retrieval-Augmented Generation (RAG) · Model Context Protocol · Statistics · GitHub Actions
