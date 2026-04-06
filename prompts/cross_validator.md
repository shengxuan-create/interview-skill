# Step 3c: 交叉验证+模式识别 / Cross-Validation & Pattern Recognition

> **Previous**: Step 3b result_evaluator.md | **Next**: Step 3d user_supplement.md

This is the key differentiator — statistical analysis across multiple interview reports.
NOT just listing what you found. ANALYZE patterns.

## Input
- Filtered results from Layer 2 (with scores)
- Total N data sources searched, M with results

## Process
1. Cluster information by topic (process, questions, culture, difficulty)
2. Count how many independent sources confirm each claim
3. Assign confidence labels based on source count

## Confidence Labels
- **HIGH** — ≥50% of sources confirm (e.g., 8/15 sources)
- **MEDIUM** — 25-49% of sources confirm (e.g., 4/15)
- **LOW** — <25% or only 1-2 sources
- **GAP** — 0 sources, information not found

## Output

Present findings in this format, then pass to Step 3d (user_supplement.md):

```
从 {N} 个数据源中提取到 {M} 条面试信息。

面试流程（置信度：HIGH，{N1}/{N}来源一致）：
  1. Recruiter phone screen (30min)
  2. Technical phone screen (45min, 1 coding)
  3. Onsite: 4-5 rounds

高频考点（出现频率 >50% 标记 HIGH）：
  - System Design: 12/15 → HIGH（必考）
  - Behavioral leadership: 9/15 → HIGH
  - Coding Medium-Hard: 8/15 → MEDIUM

量化指标：
  - Glassdoor difficulty: 4.2/5
  - Positive experience rate: 61%

信息缺口（<3来源，标记 LOW/GAP）：
  - Specific team preferences: 1 source → suggest user confirm
```
