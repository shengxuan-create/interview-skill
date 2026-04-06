# Step 3b: 结果评分过滤 / Result Scoring & Filtering

> **Previous**: Step 3a search_strategist.md | **Next**: Step 3c cross_validator.md

Score each search result from Layer 1 on 3 dimensions (1-5 each).
Discard results scoring below 2.5 composite.

## Scoring Rubric

| Dimension | Weight | 5 (Best) | 1 (Worst) |
|-----------|--------|-----------|-----------|
| Recency | 0.3 | Within 6 months | Over 3 years old |
| Source credibility | 0.4 | Official site / Glassdoor / 1point3acres / LeetCode | Unknown blog / marketing content |
| Relevance | 0.3 | Exact match: company + role + round | Generic interview advice |

## Composite Score
`score = (recency × 0.3) + (credibility × 0.4) + (relevance × 0.3)`

## Rules
- Score < 2.5 → DISCARD, do not pass to Layer 3
- Score ≥ 2.5 → Pass to cross_validator.md with score attached
- Log discarded results count for transparency

## Output
Filtered list of results, each with:
- Source URL or identifier
- Content summary
- Composite score
- Individual dimension scores
