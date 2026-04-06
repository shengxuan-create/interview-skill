#!/usr/bin/env python3
"""
hype_generator.py — Pre-Interview Confidence Data Aggregator

Aggregates mock scores, research data, and storybank info to generate
structured data for the hype (pre-interview confidence) document.

Usage:
    python3 hype_generator.py --slug google-swe --timing day_before --base-dir ./preps
    python3 hype_generator.py --slug google-swe --timing morning_of --interview-date 2026-04-15 --base-dir ./preps
    python3 hype_generator.py --slug google-swe --timing week_before --base-dir ./preps --storybank-dir ./storybank
    python3 hype_generator.py --help
"""

import argparse
import json
import re
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional


COMPANY_CULTURE_MAP = {
    "google": "google_googliness",
    "alphabet": "google_googliness",
    "meta": "meta_impact",
    "facebook": "meta_impact",
    "amazon": "amazon_lp",
    "aws": "amazon_lp",
    "apple": "default",
    "microsoft": "default",
    "netflix": "default",
    "bytedance": "startup_hustle",
    "tiktok": "startup_hustle",
    "stripe": "startup_hustle",
    "goldman sachs": "bank_formal",
    "jpmorgan": "bank_formal",
    "morgan stanley": "bank_formal",
    "mckinsey": "bank_formal",
    "bain": "bank_formal",
    "bcg": "bank_formal",
}


def detect_culture_tag(company: str) -> str:
    """Detect company culture tag from company name."""
    company_lower = company.lower().strip()
    for key, tag in COMPANY_CULTURE_MAP.items():
        if key in company_lower:
            return tag
    return "default"


def parse_mock_scores(mock_path: Path) -> dict:
    """Parse mock_script.md for per-question scores and categories."""
    scores = {"behavioral": [], "technical": [], "system_design": [], "situational": [], "all": []}

    if not mock_path.exists():
        return {"has_mock": False, "scores": scores}

    content = mock_path.read_text(encoding="utf-8")

    # Look for score patterns like "评分：4/5" or "Score: 3.5/5" or "你的回答评分：4/5"
    score_pattern = re.compile(r'(?:评分|Score|score)[：:]\s*(\d+(?:\.\d+)?)\s*/\s*5', re.IGNORECASE)
    all_scores = [float(m.group(1)) for m in score_pattern.finditer(content)]

    # Try to categorize by section headers
    sections = re.split(r'^## ', content, flags=re.MULTILINE)
    for section in sections:
        section_scores = [float(m.group(1)) for m in score_pattern.finditer(section)]
        if not section_scores:
            continue

        section_lower = section.lower()
        if any(kw in section_lower for kw in ["behavioral", "star", "行为"]):
            scores["behavioral"].extend(section_scores)
        elif any(kw in section_lower for kw in ["system design", "系统设计"]):
            scores["system_design"].extend(section_scores)
        elif any(kw in section_lower for kw in ["technical", "coding", "技术"]):
            scores["technical"].extend(section_scores)
        elif any(kw in section_lower for kw in ["situational", "情景"]):
            scores["situational"].extend(section_scores)

    scores["all"] = all_scores

    return {"has_mock": len(all_scores) > 0, "scores": scores}


def parse_prep_plan_progress(plan_path: Path) -> dict:
    """Parse prep_plan.md for task completion progress."""
    if not plan_path.exists():
        return {"has_plan": False, "total": 0, "completed": 0, "percentage": 0}

    content = plan_path.read_text(encoding="utf-8")
    checked = len(re.findall(r'- \[x\]', content, re.IGNORECASE))
    unchecked = len(re.findall(r'- \[ \]', content))
    total = checked + unchecked

    return {
        "has_plan": total > 0,
        "total": total,
        "completed": checked,
        "percentage": round(checked / max(total, 1) * 100)
    }


def load_linked_stories(storybank_dir: Path, slug: str) -> dict:
    """Load stories linked to this prep from storybank."""
    index_path = storybank_dir / "index.json"
    if not index_path.exists():
        return {"has_storybank": False, "linked_stories": [], "story_gaps": []}

    with open(index_path, "r", encoding="utf-8") as f:
        index = json.load(f)

    linked = []
    for story in index.get("stories", []):
        if slug in story.get("prep_refs", []):
            linked.append({
                "id": story["id"],
                "title": story["title"],
                "competencies": story["competencies"],
                "strength": story["strength"],
                "last_evaluator_score": story.get("last_evaluator_score")
            })

    return {
        "has_storybank": True,
        "linked_stories": linked,
        "story_gaps": index.get("gap_competencies", []),
        "total_stories": len(index.get("stories", []))
    }


def calculate_timing(interview_date_str: Optional[str], timing_override: Optional[str]) -> dict:
    """Calculate timing window based on interview date or override."""
    if timing_override:
        return {"timing": timing_override, "days_until": None, "interview_date": interview_date_str}

    if not interview_date_str:
        return {"timing": "day_before", "days_until": None, "interview_date": None}

    try:
        interview = datetime.fromisoformat(interview_date_str.replace("Z", "")).date()
        today = date.today()
        days = (interview - today).days

        if days <= 0:
            timing = "morning_of"
        elif days <= 2:
            timing = "day_before"
        else:
            timing = "week_before"

        return {"timing": timing, "days_until": days, "interview_date": interview_date_str}
    except (ValueError, TypeError):
        return {"timing": "day_before", "days_until": None, "interview_date": interview_date_str}


def avg(lst):
    """Safe average."""
    return round(sum(lst) / len(lst), 1) if lst else None


def generate_hype_data(slug: str, timing: Optional[str], interview_date: Optional[str],
                       base_dir: Path, storybank_dir: Optional[Path]) -> dict:
    """Aggregate all data needed for hype document generation."""
    prep_dir = base_dir / slug

    if not prep_dir.exists():
        return {"status": "error", "message": f"Prep '{slug}' not found at {prep_dir}"}

    # Load meta.json
    meta_path = prep_dir / "meta.json"
    meta = {}
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

    company = meta.get("company", slug)
    role = meta.get("role", "Unknown")

    # Determine timing
    meta_interview_date = meta.get("interview_date", interview_date)
    timing_info = calculate_timing(meta_interview_date, timing)

    # Detect culture tag
    culture_tag = detect_culture_tag(company)

    # Parse mock scores
    mock_data = parse_mock_scores(prep_dir / "mock_script.md")

    # Calculate score averages
    scores_raw = mock_data["scores"]
    scores = {
        "overall": avg(scores_raw["all"]),
        "behavioral": avg(scores_raw["behavioral"]),
        "technical": avg(scores_raw["technical"]),
        "system_design": avg(scores_raw["system_design"]),
    }

    # Find strongest and weakest areas
    category_scores = {k: v for k, v in scores.items() if v is not None and k != "overall"}
    strongest = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
    weakest = sorted(category_scores.items(), key=lambda x: x[1])

    # Parse prep plan progress
    plan_progress = parse_prep_plan_progress(prep_dir / "prep_plan.md")

    # Load storybank data
    storybank_data = {"has_storybank": False, "linked_stories": [], "story_gaps": []}
    if storybank_dir:
        storybank_data = load_linked_stories(storybank_dir, slug)

    # Calculate prep duration
    created = meta.get("created_at", "")
    prep_days = None
    if created:
        try:
            created_date = datetime.fromisoformat(created.replace("Z", "")).date()
            prep_days = (date.today() - created_date).days
        except (ValueError, TypeError):
            pass

    result = {
        "status": "ok",
        "slug": slug,
        "company": company,
        "role": role,
        "timing": timing_info["timing"],
        "days_until_interview": timing_info["days_until"],
        "interview_date": timing_info["interview_date"],
        "culture_tag": culture_tag,
        "has_mock": mock_data["has_mock"],
        "scores": scores,
        "strongest_areas": [s[0] for s in strongest[:3]] if strongest else [],
        "weakest_areas": [s[0] for s in weakest[:2]] if weakest else [],
        "research_confidence": meta.get("research_confidence", "unknown"),
        "questions_practiced": meta.get("questions_count", 0),
        "prep_days": prep_days,
        "prep_progress": plan_progress,
        "mock_score": meta.get("mock_score"),
        "storybank": storybank_data,
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="Pre-Interview Confidence Data Aggregator")
    parser.add_argument("--slug", required=True, help="Prep slug identifier")
    parser.add_argument("--timing", choices=["week_before", "day_before", "morning_of"],
                        help="Override timing window")
    parser.add_argument("--interview-date", help="Interview date (ISO format)")
    parser.add_argument("--base-dir", default="./preps", help="Preps base directory")
    parser.add_argument("--storybank-dir", default="./storybank", help="Storybank directory")

    args = parser.parse_args()

    storybank_dir = Path(args.storybank_dir)
    if not storybank_dir.exists():
        storybank_dir = None

    result = generate_hype_data(
        slug=args.slug,
        timing=args.timing,
        interview_date=args.interview_date,
        base_dir=Path(args.base_dir),
        storybank_dir=storybank_dir
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
