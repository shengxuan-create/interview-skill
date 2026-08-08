# interview-skill — Full Workflow (English)

> Routed here from SKILL.md. Contains the complete 7-step flow, evolution/correction/debrief modes, storybank and hype details.
> New in v2.0: evidence discipline (Step 3), AI-era question types (Step 4), scoring anchors & de-AI pass (Step 6) — flagged inline.

---

## Trigger Conditions

**Create Mode:**
- `/interview-prep`
- "Help me prepare for an interview" / "I have an interview at XX"

**Mock Mode:**
- `/mock {slug}`
- "mock interview for XX"

**Evolution Mode:**
- "I have new interview intel" / "add more info" / `/update-prep {slug}`

**Correction Mode:**
- "That's wrong" / "The interview process is actually..."

**Debrief Mode:**
- "I finished the interview" / "interview is done" / `/debrief {slug}`

**Storybank Mode:**
- `/storybank` — Manage STAR story bank
- `/storybank add` — Add a new story
- `/storybank list` — View all stories
- `/storybank gaps` — View competency gaps
- "my stories" / "add a story"

**Hype Mode (Pre-Interview Confidence):**
- `/hype {slug}` — Generate pre-interview confidence briefing
- "I need confidence" / "interview coming up"

**Management Commands:**
- `/list-preps` — List all generated preps
- `/mock {slug}` — Start mock interview
- `/update-prep {slug}` — Add new intel
- `/prep-rollback {slug} {version}` — Rollback version
- `/delete-prep {slug}` — Delete prep (requires confirmation)

---

## Tool Usage Rules

| Task | Tool |
|------|------|
| Read PDF resume/JD | `Read` tool (native PDF support) |
| Read image/screenshot | `Read` tool (native image support) |
| Read MD/TXT | `Read` tool |
| Parse JD (URL or text) | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/jd_parser.py` |
| Interview experience aggregation | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/interview_scraper.py` |
| Company intelligence | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/company_intel.py` |
| LeetCode frequency tracker | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/leetcode_tracker.py` |
| Resume analysis + JD matching | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/resume_analyzer.py` |
| Web search | `WebSearch` tool or `Bash` → Python requests |
| Write/update prep files | `Write` / `Edit` tool |
| Prep document management | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/prep_writer.py` |
| Version management | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| STAR story management | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py` |
| Pre-interview confidence | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/hype_generator.py` |

**Base Directory**: Prep files written to `./preps/{slug}/`, storybank to `./storybank/` (relative to project directory).

---

## Main Flow (7 Steps)

### Step 1: Intake

Ask the user 5 questions. Only Q1 and Q2 are required. Summarize and confirm before proceeding.

**Q1: Target Company (required)**
```
Which company are you interviewing at?
Example: Google / ByteDance / https://careers.google.com/jobs/xxx
```

**Q2: Target Role (required)**
```
What role?
Example: Software Engineer L4 / Backend Engineer / Product Manager
```

**Q3: JD Source (5 options, skippable)**
```
Do you have a JD? How to provide it?

  [A] Paste JD text
  [B] Give URL (LinkedIn/Indeed/official site), auto-fetch
  [C] Upload PDF or screenshot
  [D] Describe manually (requirements and tech stack)
  [E] Skip
```

Processing rules:
- A → Use as text directly
- B → `python3 ${CLAUDE_SKILL_DIR}/tools/jd_parser.py --url {url} --output /tmp/jd_parsed.json`
- C → Use `Read` tool to read PDF/image
- D → Use as text directly
- E → Skip, use generic framework later

**Q4: Interview Round (skippable)**
```
Which round?
  Phone Screen / Technical / Behavioral / Onsite (full day) / Final Round / Not sure
```

**Q5: Resume (skippable)**
```
Do you have a resume? You can upload a PDF or paste text. You can also skip.
```

**Summary confirmation:**
```
Information collected:
  - Company: {company}
  - Role: {role}
  - JD: {provided / skipped}
  - Round: {round or "not specified"}
  - Resume: {provided / skipped}

Confirm and proceed?
```

After confirmation: if resume provided → Step 2, otherwise → Step 3.

---

### Step 2: Resume Matching

**Only execute if user provided a resume in Step 1. Otherwise skip to Step 3.**

1. Extract skills, experience, education from resume
2. Compare against JD requirements
3. If resume is a file: `python3 ${CLAUDE_SKILL_DIR}/tools/resume_analyzer.py --resume {path} --jd /tmp/jd_parsed.json --output /tmp/resume_match.json`

**Output format (JSON):**
```json
{
  "match_score": 72,
  "matched_skills": ["Python", "distributed systems", "SQL"],
  "gap_skills": ["Kubernetes", "Go", "ML experience"],
  "experience_gap": "JD requires 3-5 years, resume shows ~2 years relevant",
  "strength_highlights": ["Strong system design background", "Large-scale data processing"],
  "preparation_priority": ["Kubernetes basics", "Go fundamentals", "ML system design"]
}
```

**How this feeds forward:**
- `gap_skills` → Step 4 generates questions targeting these gaps
- `preparation_priority` → Step 7 prep_plan prioritizes these areas
- `strength_highlights` → Step 5 mock_interviewer probes these for depth

---

### Step 3: Research Engine (4 Layers)

Core differentiator. Not just Googling for the user — **structured intelligence analysis**.

#### Layer 1: Multi-Dimensional Search

Generate 10-15 targeted queries across 5 dimensions.

| Dimension | Goal | Example Query |
|-----------|------|---------------|
| Company fundamentals | Size, business, tech stack, funding | "{company} engineering tech stack 2026" |
| Interview process | Rounds, format, who interviews, duration | "{company} {role} interview process site:glassdoor.com" |
| Real interview questions | Actual questions, focus areas | "{company} interview questions {role} 2025 2026 site:leetcode.com OR site:1point3acres.com" |
| Company culture | Values, work style, management | "{company} engineering culture values what it's like to work" |
| Recent news | Layoffs, hiring, new products, earnings | "{company} 2026 hiring layoffs news" |

For technical roles, additionally run:
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/leetcode_tracker.py --company {name} --months 6 --output /tmp/leetcode_freq.json
```

Record each result: source URL, content summary, date. Pass all to Layer 2.

#### Layer 2: Result Scoring & Filtering

Score each Layer 1 result on 3 dimensions (1-5 each):

| Dimension | Weight | 5 (Best) | 1 (Worst) |
|-----------|--------|-----------|-----------|
| Recency | 0.3 | Within 6 months | Over 3 years old |
| Source credibility | 0.4 | Official / Glassdoor / 1point3acres / LeetCode | Unknown blog / marketing |
| Relevance | 0.3 | Exact match: company + role + round | Generic interview advice |

`score = (recency × 0.3) + (credibility × 0.4) + (relevance × 0.3)`

- Score < 2.5 → DISCARD
- Score >= 2.5 → Pass to Layer 3 with score attached
- Log discarded count for transparency

#### Layer 3: Cross-Validation & Pattern Recognition

Statistical analysis across multiple interview reports.

1. Cluster by topic (process, questions, culture, difficulty)
2. Count how many independent sources confirm each claim
3. Assign confidence labels:

| Label | Condition |
|-------|-----------|
| **HIGH** | >=50% of sources confirm |
| **MEDIUM** | 25-49% of sources confirm |
| **LOW** | <25% or only 1-2 sources |
| **GAP** | 0 sources, not found |

**Output format:**
```
Extracted {M} interview data points from {N} sources.

Interview process (confidence: HIGH, {N1}/{N} sources agree):
  1. Recruiter phone screen (30min)
  2. Technical phone screen (45min, 1 coding)
  3. Onsite: 4-5 rounds

High-frequency topics (>50% marked HIGH):
  - System Design: 12/15 → HIGH (must prepare)
  - Behavioral leadership: 9/15 → HIGH
  - Coding Medium-Hard: 8/15 → MEDIUM

Quantitative metrics:
  - Glassdoor difficulty: 4.2/5
  - Positive experience rate: 61%

Information gaps (<3 sources, marked LOW/GAP):
  - Specific team preferences: 1 source → suggest user confirm
```

#### Layer 4: User Supplement

Present Layer 1-3 results to user, collect additional intel.

```
Here are the research results. Please review:

[HIGH] High-confidence information (multi-source corroboration)
[LOW] Low-confidence information (limited sources)
[GAP] Information gaps (not found)

Do you have any additional intel? For example:
- Inside info from friends or your recruiter
- Interview reports you've seen on forums
- Anything you know that I didn't find

Paste or describe it, and I'll integrate. Or say "no, continue".
```

**If user says "no, continue":** proceed to company brief generation.

**If user provides new info:**
1. Classify: which dimension does it belong to
2. Targeted verification: 1-2 queries to verify user's info
3. Merge into cross_validation results
4. Update confidence: user's direct experience = high-weight source
5. Show updated summary, confirm before proceeding

#### Research Degradation Strategy

- **Grade A** (>=15 valid results) → Full 4-layer analysis
- **Grade B** (5-14) → 3-layer analysis, relaxed cross-validation
- **Grade C** (1-4) → Primarily JD + industry framework
- **Grade D** (0) → Inform user of insufficient data, generate based on JD only

#### [v2.1] Degrading means switching evidence type, not falling back to generic

**This is the biggest flaw real usage exposed (2026-08-08).** In a prep for an RBC real-estate
investment banking analyst role, that desk had zero group-specific interview reports and research
came back Grade B. The system fell back to the generic bank, and the user's feedback was "most of
these questions are pretty general." A targeted second pass then easily surfaced three hard assets:
the firm's own marquee transactions page (one of the deals was the very building the interview is
held in), the current policy rate plus an industry cap-rate report, and a verbatim question from
that specific desk. **That material was there the whole time; nobody went and got it.**

So the rule changes: **when interview-report evidence is thin, don't pocket the search budget —
spend it on the other three evidence types.**

| Interview-report evidence | Correct response |
|---|---|
| Plentiful (Grade A/B) | Proceed as normal; still run the anchor layer (Step 3.5) as an upgrade |
| Thin or zero (Grade C/D) | **Do not** ship the generic bank and call it done. Redirect the search budget into Step 3.5 anchor material, and disclose the generic share honestly at Checkpoint #2 |

### Step 3.5: Company anchor material (v2.1 — a standard step, not a rescue)

Goal: give the candidate specific facts only someone who did the homework could say. This material
exists for nearly any company and comes entirely from verifiable first-party sources, so no
inference is required.

**Four types to collect (1-3 items each, always with source URL and date):**

1. **Recent concrete moves** — deals, launches, projects, client work from the company's own pages.
   Finance: transactions/deals pages. Product: changelog/newsroom. Services: case studies.
2. **Where this desk/team sits** — what the group does inside the company, its scale, how it works
   with other groups (official business-line pages).
3. **Key numbers in the industry right now** — policy rates, industry averages, market size, always
   **with attribution and as-of date** ("the Colliers Q2 report puts the national average cap rate
   at 6.58%"). Numbers recalled from memory are not allowed.
4. **Quotable company self-description** — values, strategy language, leadership statements
   (verbatim from official pages, annual reports, press releases).

**Once collected:**
- Turn each item into one sentence the candidate can actually say in the room, and put it in a
  dedicated anchor section of questions.md
- Prioritize whatever overlaps the candidate's own situation (the interview location, their alma
  mater, an industry they've worked in). Higher overlap reads more like genuine homework.
- If nothing can be found, label it a GAP. Never invent deal names, numbers, or quotes.

#### Checkpoint #1: Company Brief

Consolidate all Research Engine data into `preps/{slug}/company_brief.md`.

**company_brief.md format:**
```markdown
# {company} — {role} Company Brief

> Research confidence: {A/B/C/D} | Valid sources: {N} | Generated: {timestamp}

## Company Overview
- Industry: {industry}
- Size: {size}
- HQ: {hq}
- Founded: {founded}
- Tech stack: {tech_stack} (source: {sources})
- Glassdoor rating: {rating}/5

## Culture & Values
{culture_values, each with source attribution}

## Interview Process
{process, each round: format/duration/interviewer level/focus areas}
- Confidence: {confidence} ({N}/{total} sources agree)

## High-Frequency Topics
{each topic: frequency, confidence label, source count}

## LeetCode Frequent Problems (technical roles)
{top 10: problem number/name/difficulty/frequency rank}

## Recent News
{last 3 months, each with date and source}

## Information Gaps
{list unfound information, suggest how user can supplement}
```

**Rules:**
1. Every piece of information must cite its source
2. Confidence labels must appear next to key conclusions
3. Information gaps must be honestly disclosed
3b. [v2 zero-guess hardening] Register questions, salaries and process steps only when they appear **verbatim** on the source page; search snippets and AI overviews fabricate — never trust them directly. When in doubt, downgrade to LOW and attach the original link. A brief with 60% coverage and full trust beats one with 100% coverage and hallucinations mixed in.
3c. [v2] Additionally research whether this company/role uses **AI interview rounds** (async video / AI screening) and its live-coding AI-usage policy; if found, note it in the brief's process section and read `ai-era-interviews.md` to generate matching prep tasks; if unknown, list as a gap and advise asking the recruiter directly
4. For Grade C/D research, add warning at top: `Note: This brief is based on limited data sources (Grade {X}). Some information may be incomplete.`

**Show summary for user confirmation:**
```
Company brief summary:
  - Company: {name}, {industry}, {size}
  - Interview process: {process summary}
  - Key topics: {top 3}
  - Research confidence: {A/B/C/D}
  - Gaps: {gaps}

Confirm to continue? Or need adjustments?
```

After confirmation → Step 4.

---

### Step 4: Question Generation

Generate tailored interview questions based on company brief, JD, round, and resume match.

**Question source priority:**
1. Real interview questions (marked [REAL] in company_brief)
2. Custom questions based on HIGH-frequency topics
3. JD skill-matched technical questions
4. Resume gap questions (if resume_match exists)
5. Generic high-frequency questions from `references/question_bank.md`
6. [v2] **AI-era questions**: if the role touches AI/ML/LLM, mix in 3-6 from question_bank's AI-Era section (strategy in `ai-era-interviews.md`); for any role add one "how do you use AI to work better"; if the brief flags an AI interview round, add 90-second story-cut drill tasks

**[v2.1] S0 opener: first question in every bank, every round, every industry**

"Walk me through your resume" / "Tell me about yourself" opens most interviews, but the v2.0 count
table sorts by Behavioral/Technical/System Design/Situational and **left it no slot, so it got
dropped entirely** (exposed by real usage 2026-08-08). Fumbling question one means spending the
rest of the interview recovering.

So: **question 1 of every bank is the opener**, outside the quotas below, with a 90-120 second
answer skeleton built in four moves (background → most relevant experience → differentiating second
experience → why this company and this team), landing on this role. Run that answer through the
de-AI checklist in §Step 6.

**Question count by round (excludes the S0 opener):**

| Round | Behavioral | Technical | System Design | Situational | Total |
|-------|-----------|-----------|--------------|-------------|-------|
| Phone Screen | 3 | 3 | 0 | 1 | 7 |
| Technical | 2 | 6 | 2 | 0 | 10 |
| Behavioral | 8 | 0 | 0 | 3 | 11 |
| Onsite (full day) | 8 | 8 | 3 | 2 | 21 |
| Final Round | 5 | 0 | 1 | 3 | 9 |

**[v2.1] Every question carries an evidence tag** (next to the number; totals get reported at delivery):

| Tag | Meaning |
|---|---|
| `[verified·verbatim]` | Appears word-for-word on a source page |
| `[verified·reworded]` | Topic is evidenced; we rewrote the phrasing |
| `[industry-inferred]` | Standard canon for the industry/role, not evidenced at this company |
| `[generic-canon]` | Drawn from question_bank.md |
| `[anchor]` | Company-specific, built from Step 3.5 material |
| `[resume-gap]` | Targets a weakness from resume_match |

**Per-question format:**
```markdown
## {Question Type} Questions

1. [{frequency label}] {question}
   - Tests: {skills being tested}
   - Company angle: {company-specific angle from company_brief}
   - Approach: {brief approach, STAR hints for behavioral}
   - Difficulty: {level}
   - Time allocation: {if applicable}
```

**Resume gap questions (if resume_match exists):**
For each gap in `resume_match.gap_skills`, generate 1-2 questions. Goal: prepare user to answer "you don't have XX experience" by reframing as learning willingness and transferable skills.

**Checkpoint #2 (v2.1 — report the evidence mix, not just category counts):**
```
Generated {N} questions (plus the S0 opener):
  - Behavioral: {n1} · Technical: {n2} · System Design: {n3} · Situational: {n4}

Evidence mix:
  verified·verbatim {a} · verified·reworded {b} · anchor {c}
  industry-inferred {d} · generic-canon {e} · resume-gap {f}
  → {(d+e)/N}% not evidenced at this company{, because <zero reports for this desk /
    research grade C / etc.>}

{if the non-evidenced share exceeds 40%, add:}
  That share is high. I can run a targeted second pass and anchor these to their actual
  deals, recent moves, and current industry numbers, so the questions shift from "everyone
  in this field asks this" to "this team would ask this." Want me to?

Want to adjust focus areas? Or proceed to mock interview?
```

**Why this accounting is mandatory:** evidence discipline was wired into the company brief but not
into the question bank, so users saw a flat, uniform-looking list and concluded "these are all
pretty general" (real feedback, 2026-08-08). Disclosing the mix and offering the second pass beats
waiting for the complaint. Note that **generic canon is not itself a defect** — IB technical rounds
really are the canon, and tech interviews have their own must-know classics. The defect is letting
the user assume that's all there is.

After confirmation → Step 5.

---

### Step 5: Mock Interview

AI plays the company's interviewer, adopting that company's interview style. No feedback during the interview — evaluate after completion.

**Interviewer style (based on company type):**

| Company Type | Style | Opening |
|-------------|-------|---------|
| FAANG | Structured, rubric-driven | Brief intro then start |
| Startup | Casual, conversational | Chat about company and team |
| Banking/Consulting | Formal, hierarchical | Formal greeting + process overview |
| Chinese Big Tech | Direct, efficient | Brief small talk then jump to technical |

**Control logic:**
1. Select 6-8 questions from question bank, sorted by importance
2. Target 30-45 minutes (inform user before starting)
3. Follow-up rules: max 2 follow-ups per question
   - Vague answer → "Can you be more specific about what you did?"
   - Missing data → "What was the outcome? Any specific numbers?"
   - Excellent answer → Move to next question
4. Skip: user says "next question" → skip current
5. Exit: user says "end" → exit mock mode
6. No scoring during interview

**Interview flow:**
```
[Opening]
Interviewer (company style): {opening}

[Questions]
Interviewer: {question 1}
→ Wait for user answer
→ Follow up or move to next based on answer quality

[Closing]
Interviewer: That concludes our interview. Thank you for your time.
We'll be in touch with next steps. Do you have any questions for me?
→ User questions (optional)
→ End
```

**Record format** (written to `mock_script.md`):
```markdown
# Mock Interview — {company} {role}

> Date: {date} | Round: {round} | Questions: {N}

## Q1: {question text}
**Answer**: {user's full answer}
**Follow-up 1**: {follow-up, if any}
**Answer**: {user's answer}

## Q2: ...
```

After interview ends → automatically proceed to Step 6.

---

### Step 6: Answer Evaluation

Structured scoring of every mock interview answer. Reference `${CLAUDE_SKILL_DIR}/references/star_framework.md` for scoring criteria and examples.

[v2 — two hard rules]
- **Before scoring**: read the anchored examples in star_framework.md and align your scale to them; afterwards check the distribution — 6-8 answers all landing on the same score means the scale failed, re-score.
- **After generating each "improved reference answer"**: run it through the `humanize-answers.md` checklist (or the `humanizer` skill if installed) before delivering; remind the user the reference answer is a skeleton to retell in their own words.

**Behavioral questions (STAR framework):**

| Dimension | 5 (Best) | 1 (Worst) |
|-----------|----------|-----------|
| Situation | Clear, specific, with time/place | Vague or missing |
| Task | Personal role and goal clear | Role unclear, mixed with team |
| Action | Specific steps, individual contribution | "We did..." vague |
| Result | Quantified results + reflection | No results or just "it worked" |

Score = (S + T + A×2 + R×2) / 6 (Action and Result double-weighted)

**Technical questions:**

| Dimension | 5 (Best) | 1 (Worst) |
|-----------|----------|-----------|
| Correctness | Solution correct, edge cases covered | Logical errors |
| Depth | Discusses trade-offs and optimization | Surface-level only |
| Communication | Clear thinking, proactively confirms requirements | Silent or jumpy |
| Engineering sense | Considers scalability, maintainability | Only focuses on functionality |

**Per-question output:**
```markdown
## Question {N}: {question text}

Your score: {score}/5

### STAR Analysis / Technical Analysis:
- {dimension}: {GOOD/OK/WEAK} {comment}
- ...

### Improvement suggestions:
- {specific, actionable improvement}

### Improved reference answer:
"{complete high-scoring reference answer}"
```

**Overall evaluation:**
```markdown
## Overall Assessment

Overall performance: {average_score}/5
Strengths: {list strong areas}
Areas to improve: {list weak areas}
Suggested practice focus: Questions {numbers}

### Category Performance
- Behavioral: {avg}/5
- Technical: {avg}/5
- System Design: {avg}/5 (if applicable)

### Next Steps
{1-3 specific action items based on evaluation}
```

After evaluation → automatically proceed to Step 7.

---

### Step 7: Output Prep Package

Consolidate all prior step outputs into a complete interview prep document package.

**Create directory:**
```bash
mkdir -p preps/{slug}/knowledge preps/{slug}/versions
```

**Write files:**
1. `preps/{slug}/company_brief.md` — Company brief with confidence labels + sources
2. `preps/{slug}/questions.md` — Question bank + approach notes
3. `preps/{slug}/mock_script.md` — Mock interview transcript + scores
4. `preps/{slug}/prep_plan.md` — Timeline-based preparation plan
5. `preps/{slug}/meta.json` — Metadata (same schema as Chinese version above)
6. `preps/{slug}/SKILL.md` — Standalone runnable skill file

**Completion message:**
```
Interview prep materials generated.

Location: preps/{slug}/
Commands:
   /mock {slug}        — Run another mock interview
   /update-prep {slug} — Add new intel

After your real interview, come back and say "I finished the interview"
for a debrief + real questions recorded into the system.
```

---

## Evolution Modes

### Add New Intel (Merger)

**Trigger**: "I have new interview intel" / "add more info" / `/update-prep {slug}`

1. Read existing data from `preps/{slug}/`
2. Classify new content (new questions → questions.md, company info → company_brief.md, etc.)
3. Conflict detection — if new info contradicts existing data, ask user to choose: adopt new / keep both / ignore
4. Version backup: `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./preps`
5. Merge using `Edit` tool
6. Update SKILL.md and meta.json (version++, updated_at, research_sources++)
7. Confirm changes to user

---

### User Correction

**Trigger**: "That's wrong" / "The interview process is actually..."

1. Identify what's wrong, what's correct, which file it belongs to
2. Version backup
3. Precise edit using `Edit` tool (not full rewrite)
4. Check downstream impact (if company_brief changed, do questions need updating?)
5. Update meta.json (corrections_count++, version++)
6. Confirm changes

User corrections have highest priority — above any search results.

---

### Post-Interview Debrief

**Trigger**: "I finished the interview" / "interview is done" / `/debrief {slug}`

1. Collect: actual questions asked, self-assessment per question, interviewer style, surprises, overall feeling
2. Analyze prediction accuracy: hit rate, missed questions, over-prepared topics
3. Performance assessment with next-round recommendations
4. Data feedback: add real questions to questions.md (marked [REAL]), update company_brief.md, update meta.json
5. Summary with hit rate and next steps

---

## Storybank

Manage reusable STAR stories across multiple company interviews. Stories evolve automatically through mock practice.

### Add Story

**Trigger**: `/storybank add` or "I want to add a story"

1. User describes an experience in free-form text
2. Parse into STAR structure, flag weak/missing parts
3. Auto-tag competencies via `references/competency_taxonomy.md` (15 categories: leadership, conflict, failure, etc.)
4. User confirms tags and strength rating (1-5)
5. Create: `python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action create --title "{title}" --competencies "{tags}" --industry "{industries}" --strength {N} --base-dir ./storybank`
6. Write full STAR content to story file
7. Show coverage update (STRONG/OK/WEAK/GAP)

### List Stories

**Trigger**: `/storybank list`
Run: `python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action list --base-dir ./storybank`

### Gap Analysis

**Trigger**: `/storybank gaps`
Run: `python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action gaps --base-dir ./storybank`

For each gap, suggest what kind of experience to look for:
```
GAP: failure — You have no failure stories.
Think about: a project that went wrong, a missed deadline, a technical
decision you regret. Even small failures work if you show learning.
```

### Auto-Integration (Internal)

**Step 4**: Auto-match stories to behavioral questions via `storybank_manager.py --action match`.
**Step 5**: Show story cheat-sheet before mock starts (once only).
**Step 6**: Auto-evolve stories with evaluator feedback via `storybank_manager.py --action evolve`.
**Step 7**: Reference specific stories in prep_plan.md with practice tasks.

---

## Hype (Pre-Interview Confidence)

Data-driven, personalized pre-interview confidence briefing based on mock scores and prep data. No generic motivation.

### Trigger

`/hype {slug}` or "I need confidence" / "interview coming up"

### Timing Windows

Auto-detected from `interview_date` in meta.json, or asked:
- **WEEK_BEFORE** (7-3 days): Strategic prep, gap filling, score dashboard
- **DAY_BEFORE** (1-2 days): Confidence snapshot, logistics, power phrases, story review
- **MORNING_OF** (same day): 60-second boost, 3 key stories, opening script, calm-down protocol

### Data Aggregation

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/hype_generator.py \
  --slug {slug} --timing {timing} --base-dir ./preps --storybank-dir ./storybank
```

### Company Culture Styles

Auto-matched to company:
- **Amazon**: Frame through Leadership Principles, "I took ownership by..."
- **Google**: Emphasize thinking process, "Let me think through the tradeoffs..."
- **Meta**: Focus on impact and speed, "This impacted X million users..."
- **Startup**: Emphasize versatility, "I built this from scratch..."
- **Banking**: Emphasize precision, "The analysis showed..."

See `references/hype_templates.md` for full templates and phrases.

### Tone Rules

- NEVER use generic motivation ("you got this!", "believe in yourself!")
- ALWAYS anchor confidence to specific data points from THEIR prep
- Frame weaknesses as "areas of improvement" not "things you're bad at"
- For low scores (<2.5), be honest but constructive
- Match energy to timing: strategic → consolidating → energizing

### Output

Write to `preps/{slug}/hype.md` and display in conversation. Update meta.json.

---

## Error Handling

```
Flexibility Principle:
  Python scripts in tools/ are helpers, not mandatory paths.
  If a script fails (missing deps, network issues), use WebSearch or Bash directly.
  The goal is getting information — the method is flexible.

Specific Error Handling:
  - jd_parser.py URL fails → Ask user to paste JD text
  - interview_scraper.py source fails → Log, continue with other sources
  - interview_scraper.py all fail → Fall back to WebSearch
  - leetcode_tracker.py unavailable → Skip, use question_bank generic questions
  - resume_analyzer.py PDF parse fails → Ask user to paste text
  - company_intel.py no results → Degrade to C/D research strategy
  - Any tool failure → Log error, skip step, do not block overall flow
```
