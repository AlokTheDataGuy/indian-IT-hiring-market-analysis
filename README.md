# Indian IT Hiring Market Investigation, Q4 2025 – Q2 2026

> **Status:** 🚧 In progress. Data collection started April 2026.

## Why this project exists

Between October 2025 and April 2026, my own interview rate dropped by roughly 80%. I wanted to know whether this was specific to me, or whether something had shifted in the Indian IT hiring market more broadly.

This project is my attempt to answer that question with data — not to prove any single cause, but to document what's actually happening and honestly assess the candidate explanations.

## The question

**What is happening to the Indian IT hiring market between late 2024 and mid-2026, and what factors best explain it?**

Candidate explanations I'm investigating:

- The 2026 Iran war and associated global economic disruption
- AI displacement of junior and mid-level roles
- US policy shifts (H-1B, tariffs) affecting Indian IT services and GCC demand
- Interest rate environment and startup funding contraction
- Post-2021 over-hiring correction still working through the system
- Structural shifts in Global Capability Center (GCC) hiring patterns

I am explicitly **not** trying to prove that any one of these is *the* cause. The goal is to quantify the shift, rank the plausibility of each explanation against the evidence, and document what the data can and cannot tell us.

## Data sources

| Source | What it gives me | Status |
|---|---|---|
| Wayback Machine snapshots of 30 Indian startup career pages | 12–18 months of historical job listing counts and roles | 🚧 Collection in progress |
| layoffs.fyi (India filter) | Structured data on tech layoffs by company, month, function | ⏳ Pending |
| Hacker News "Who is Hiring?" monthly threads | 18+ months of role-level hiring signals, skills asked for | ⏳ Pending |
| Live scrape: Wellfound & Instahyre India listings | Current-state snapshot of open roles, skills, seniority | ⏳ Pending |
| Original survey of Indian IT workers | Ground-truth experience from 100+ respondents | ⏳ Pending |

## Methodology notes

- **All claims are scoped to what the data can support.** Where correlation is visible but causation cannot be established, I say so explicitly.
- **The war began on 28 February 2026.** With under 3 months of post-event data at the time of writing, any war-impact claim is preliminary and will be framed as such.
- **Survey data is self-reported** and subject to selection bias (respondents are people active on r/developersIndia, r/IndianStreetBets, and related communities).
- **Wayback Machine snapshots are uneven** — some pages are captured weekly, others monthly. I normalize to monthly aggregates to avoid false precision.

## Repository structure

```
.
├── README.md
├── data/
│   ├── raw/               # Untouched pulls from each source
│   ├── interim/           # Cleaned but not aggregated
│   └── processed/         # Final analysis-ready tables
├── notebooks/
│   ├── 01_wayback_exploration.ipynb
│   ├── 02_layoffs_analysis.ipynb
│   ├── 03_hn_hiring_threads.ipynb
│   ├── 04_live_scrape_snapshot.ipynb
│   ├── 05_survey_analysis.ipynb
│   └── 06_synthesis.ipynb
├── src/
│   ├── scrapers/          # Data collection scripts
│   ├── parsers/           # HTML/text parsing
│   └── analysis/          # Reusable analysis functions
├── survey/
│   └── questions.md       # Full survey instrument
├── reports/
│   └── figures/           # Charts for the final writeup
└── requirements.txt
```

## Findings

*This section will be populated as the analysis progresses. Updated weekly.*

### Headline numbers
*TBD*

### What the data shows
*TBD*

### What respondents are experiencing
*TBD — pending survey results (target: 100+ responses)*

### Candidate explanations, ranked by evidence
*TBD*

### What the data cannot answer
*TBD*

## Limitations and what I'd do with more time

*To be written at project close. This section will be honest about scope, bias, and gaps.*

## How to reproduce

*Setup instructions will be added once the core pipeline stabilizes.*

## About me

I'm a data analyst based in Bengaluru, currently job-searching. This project started as an attempt to understand my own situation and grew into a broader investigation. If you're hiring for product analytics or data analyst roles at Indian startups, I'd love to talk.

**Contact:** [alokdeep9925@gmail.com] · [www.linkedin.com/in/alokthedataguy]

## Acknowledgments

Thanks to everyone who responds to the survey — this project doesn't work without you. Aggregated findings will be shared back to r/developersIndia, r/IndianStreetBets, and the other communities where responses were collected.

---

*Last updated: April 2026*
