# Step 3a: 多维搜索策略 / Search Strategy

> **Previous**: Step 2 resume_matcher.md (or Step 1 intake.md) | **Next**: Step 3b result_evaluator.md

Generate 10-15 targeted search queries across 5 dimensions.
Do NOT run a single generic search. Each dimension gets 2-3 specific queries.

## Input
- Company name, role, level (from intake)
- JD parsed data (if available)

## 5 Search Dimensions

| Dimension | Goal | Example Query |
|-----------|------|---------------|
| Company fundamentals | Size, business, tech stack, funding | "{company} engineering tech stack 2026" |
| Interview process | Rounds, format, who interviews, duration | "{company} {role} interview process site:glassdoor.com" |
| Real interview questions | Actual questions, focus areas | "{company} interview questions {role} 2025 2026 site:leetcode.com OR site:1point3acres.com" |
| Company culture | Values, work style, management | "{company} engineering culture values what it's like to work" |
| Recent news | Layoffs, hiring, new products, earnings | "{company} 2026 hiring layoffs news" |

## For Technical Roles, Additionally Run:
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/leetcode_tracker.py --company {name} --months 6 --output /tmp/leetcode_freq.json
```

## Output

For each query executed, produce a structured result:

```
Dimension: {dimension_name}
Query: {search_query}
Results found: {N}
Top results:
  - {source_url}: {one-line summary} (date: {date})
  - ...
```

Pass all search results to Step 3b (result_evaluator.md) for scoring.
