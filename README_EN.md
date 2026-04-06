<div align="center">

# interview-skill

> Interview Assistant — auto-research target companies, generate tailored questions, run mock interviews, and evaluate answers with the STAR framework.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

[**中文**](README.md) · [Install](INSTALL.md) · [Architecture](docs/ARCHITECTURE.md)

</div>

---

## How It Compares to Manual Prep

| | Manual | interview-skill |
|---|---|---|
| Search | One query at a time | 5 dimensions × 3 queries = 15 targeted searches |
| Results | 10 links, read them yourself | Auto-scored and filtered, only high-quality data kept |
| Analysis | Summarize it yourself | Statistical cross-validation across 15+ sources with confidence labels |
| Questions | Generic interview questions | Tailored to the company + role + round |
| Practice | No feedback loop | AI plays the interviewer in that company's style, with follow-ups |

## Features

- **4-Layer Research Engine** — Multi-dimensional search → Score & filter → Cross-validate → User supplement
- **Structured Interview Analysis** — Statistical analysis across multiple interview reports (e.g. "12/15 sources mention System Design → likely to be tested")
- **STAR Framework Scoring** — Each answer rated 1-5 with improvement suggestions and reference answers
- **Mock Interviews** — AI role-plays as that company's interviewer, follows up on weak points
- **Post-Interview Debrief** — Feed real questions back into the system to improve future preps
- **Bilingual** — Automatically detects Chinese or English from your first message

## Quick Start

```bash
# Install to your Claude Code project
mkdir -p .claude/skills
git clone https://github.com/shengxuan-create/interview-skill .claude/skills/interview-skill

# Install dependencies (optional)
pip3 install -r .claude/skills/interview-skill/requirements.txt
```

Then in Claude Code, just say:

```
I have an interview at Google for a SWE L4 position
```

The skill takes it from there.

## Project Structure

```
interview-skill/
├── SKILL.md              # Entry point (AgentSkills standard frontmatter)
├── prompts/              # 14 prompt templates (7-step main flow + evolution/correction/debrief)
├── tools/                # 7 Python tools (JD parser, interview scraper, resume analyzer, etc.)
├── references/           # 4 reference docs (STAR framework, question bank, culture tags, formats)
├── preps/                # Generated interview prep materials (includes 3 complete examples)
├── evals/                # Trigger test cases
└── docs/                 # Architecture documentation
```

## Commands

| Command | Description |
|---------|-------------|
| `/interview-prep` | Start a new interview preparation |
| `/mock {slug}` | Run a mock interview for an existing prep |
| `/update-prep {slug}` | Add new interview intel |
| `/list-preps` | List all generated preps |
| `/prep-rollback {slug} {v}` | Roll back to a previous version |
| `/debrief {slug}` | Post-interview debrief |

## Compatible With

Claude Code · OpenClaw · Cursor · Codex

## Limitations

- Search results depend on network access
- Interview data varies by company: FAANG companies have rich data (Grade A), startups may have less (Grade C/D)
- Mock interview quality depends on available data — the debrief feature feeds real questions back to improve future preps
- LeetCode frequency tracking relies on public data and may not be perfectly accurate

## License

MIT © [shengxuan-create](https://github.com/shengxuan-create)
