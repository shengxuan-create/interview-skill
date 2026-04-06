# Step 2: 简历匹配 / Resume Matching

> **Previous**: Step 1 intake.md | **Next**: Step 3a search_strategist.md

**Only execute if user provided a resume in Step 1. Otherwise skip entirely.**

## Input
- Resume content (text or parsed PDF)
- JD parsed result (from jd_parser.py or text)

## Process
1. Extract skills, experience, education from resume
2. Compare against JD requirements
3. If resume is a file: `python3 ${CLAUDE_SKILL_DIR}/tools/resume_analyzer.py --resume {path} --jd /tmp/jd_parsed.json --output /tmp/resume_match.json`

## Output Format
```json
{
  "match_score": 72,
  "matched_skills": ["Python", "distributed systems", "SQL"],
  "gap_skills": ["Kubernetes", "Go", "ML experience"],
  "experience_gap": "JD requires 3-5 years, resume shows ~2 years relevant",
  "strength_highlights": ["Strong system design background", "Large-scale data processing experience"],
  "preparation_priority": ["Kubernetes basics", "Go fundamentals", "ML system design"]
}
```

## How This Feeds Forward
- `gap_skills` → question_generator will create questions targeting these gaps
- `preparation_priority` → prep_plan will prioritize these areas
- `strength_highlights` → mock_interviewer will probe these for depth
