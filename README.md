# ReviewMate — Intelligent Code Review & Quality Coach
Built on IBM Bob 2.0 | IBM Bob 2.0 Hackathon 2026

## Problem
Code review is slow and inconsistent. Reviewers miss subtle security risks,
test coverage gaps go unnoticed, and writing a clear review summary often
takes as long as the review itself — especially for junior engineers who
need context, not just a verdict.

## Solution
ReviewMate uses IBM Bob 2.0's Agent mode and subagents to analyze a pull
request from multiple angles in parallel:
- **Security subagent** — flags newly introduced risks (injection, auth
  bypass, exposed secrets)
- **Test coverage subagent** — finds uncovered logic and suggests concrete
  test cases
- **Complexity/style subagent** — flags complexity increases and style
  guide deviations
- **Synthesis subagent** — merges all findings into a single, plain-English
  review summary with a clear recommendation

## Why it matters
A manual senior-level review of a moderate PR takes ~20 minutes. ReviewMate
produces a structured, prioritized summary in under 3 minutes — freeing
reviewers to focus on judgment calls instead of first-pass scanning.

## Demo target
`sample-repo/` contains a small Express.js Task Manager API with two
intentionally seeded issues (see `sample-repo/README.md`):
1. No input validation on `POST /tasks`
2. No test coverage on `DELETE /tasks/:id`

These are what the Bob subagents catch in the demo.

## Architecture
```
[sample-repo PR/diff] --> Bob IDE (Agent mode)
                            ├── Security subagent
                            ├── Test coverage subagent
                            ├── Complexity subagent
                            └── Synthesis subagent --> structured output
                                                      --> src/app.py (Streamlit)
```

## Tech stack
- IBM Bob 2.0 (Bob IDE — Agent mode, subagents, document understanding)
- Python + Streamlit (frontend)
- Node.js + Express (sample repo under review)
- Optional: watsonx.ai for finding prioritization

## Repository structure
```
reviewmate-bob-hackathon/
├── bob_sessions/     # Required Bob IDE task session screenshots
├── sample-repo/      # Task Manager API used as the demo review target
├── src/              # Streamlit app (ReviewMate frontend)
├── docs/             # Architecture notes, problem statement
├── requirements.txt
└── README.md
```

## Setup
```
# Sample repo
cd sample-repo
npm install
npm test

# ReviewMate frontend
cd ..
pip install -r requirements.txt
streamlit run src/app.py
```

## Demo
- Live demo: [link]
- Video walkthrough: [link]

## Team
[Names / roles]

## Future plans
- CI/CD integration (auto-run on every PR)
- Slack/GitHub bot for inline comments
- Team-specific style guide learning over time
