#!/usr/bin/env python3
"""
storybank_manager.py — STAR Story Bank Manager

CRUD + matching + gap analysis for reusable STAR stories.
Stories are stored in storybank/ with an index.json master file.

Usage:
    python3 storybank_manager.py --action create --title "Led migration" --competencies "leadership,technical_decision" --industry "tech_faang" --strength 4 --base-dir ./storybank
    python3 storybank_manager.py --action list --base-dir ./storybank
    python3 storybank_manager.py --action match --question "Tell me about a time you led..." --company-culture amazon_lp --base-dir ./storybank
    python3 storybank_manager.py --action gaps --base-dir ./storybank
    python3 storybank_manager.py --action evolve --id story_001 --feedback "Improve Result section" --source-prep google-swe --new-score 4.2 --base-dir ./storybank
    python3 storybank_manager.py --action link --id story_001 --prep-slug meta-swe --base-dir ./storybank
    python3 storybank_manager.py --action delete --id story_001 --base-dir ./storybank
    python3 storybank_manager.py --help
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


ALL_COMPETENCIES = [
    "leadership", "conflict", "failure", "teamwork", "customer_obsession",
    "innovation", "communication", "technical_decision", "mentoring",
    "ambiguity", "ownership", "influence_without_authority", "prioritization",
    "adaptability", "ethical_dilemma"
]

COMPETENCY_KEYWORDS = {
    "leadership": ["led", "managed", "directed", "drove", "spearheaded", "team lead", "took charge", "coordinated"],
    "conflict": ["disagreed", "conflict", "pushed back", "opposing", "tension", "compromise", "negotiate"],
    "failure": ["failed", "mistake", "wrong", "missed deadline", "underperformed", "learned from", "setback"],
    "teamwork": ["collaborated", "cross-functional", "partnered", "together", "helped", "supported", "aligned"],
    "customer_obsession": ["customer", "user", "client", "feedback", "user research", "nps", "retention"],
    "innovation": ["innovative", "creative", "new approach", "rethought", "redesigned", "proposed", "invented"],
    "communication": ["presented", "explained", "convinced", "articulated", "stakeholder", "demo"],
    "technical_decision": ["architecture", "chose", "trade-off", "evaluated", "designed", "scalability", "migration"],
    "mentoring": ["mentored", "coached", "taught", "onboarded", "grew", "developed", "pair programming"],
    "ambiguity": ["ambiguous", "unclear", "uncertain", "no direction", "figured out", "scoped", "defined"],
    "ownership": ["owned", "end-to-end", "took initiative", "volunteered", "beyond my role", "responsible"],
    "influence_without_authority": ["influenced", "persuaded", "aligned", "no authority", "cross-team", "buy-in"],
    "prioritization": ["prioritized", "trade-off", "deadline", "competing", "triaged", "said no", "focused"],
    "adaptability": ["adapted", "pivoted", "changed", "new technology", "learned quickly", "shifted", "flexible"],
    "ethical_dilemma": ["ethical", "right thing", "integrity", "pushback", "transparency", "honest", "principle"],
}

CULTURE_COMPETENCY_WEIGHTS = {
    "amazon_lp": {"customer_obsession": 2.0, "ownership": 2.0, "leadership": 1.5, "prioritization": 1.5},
    "google_googliness": {"teamwork": 2.0, "innovation": 1.5, "communication": 1.5, "technical_decision": 1.5},
    "meta_impact": {"ownership": 2.0, "innovation": 1.5, "adaptability": 1.5, "prioritization": 1.5},
    "startup_hustle": {"ownership": 2.0, "adaptability": 2.0, "ambiguity": 1.5, "innovation": 1.5},
    "bank_formal": {"communication": 2.0, "ethical_dilemma": 1.5, "prioritization": 1.5, "leadership": 1.5},
}


def load_index(base_dir: Path) -> dict:
    """Load or initialize the storybank index."""
    index_path = base_dir / "index.json"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "version": "1.0",
        "stories": [],
        "competency_coverage": {c: [] for c in ALL_COMPETENCIES},
        "gap_competencies": list(ALL_COMPETENCIES)
    }


def save_index(base_dir: Path, index: dict):
    """Save the storybank index."""
    base_dir.mkdir(parents=True, exist_ok=True)
    index_path = base_dir / "index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def recalculate_coverage(index: dict):
    """Recalculate competency_coverage and gap_competencies from stories."""
    coverage = {c: [] for c in ALL_COMPETENCIES}
    for story in index["stories"]:
        for comp in story.get("competencies", []):
            if comp in coverage:
                coverage[comp].append(story["id"])
    index["competency_coverage"] = coverage
    index["gap_competencies"] = [c for c, ids in coverage.items() if len(ids) == 0]


def next_story_id(index: dict) -> str:
    """Generate the next story ID."""
    existing = [s["id"] for s in index["stories"]]
    n = 1
    while f"story_{n:03d}" in existing:
        n += 1
    return f"story_{n:03d}"


def create_story(base_dir: Path, title: str, competencies: list, industry: list, strength: int) -> dict:
    """Create a new story entry."""
    index = load_index(base_dir)
    story_id = next_story_id(index)
    now = datetime.now().isoformat() + "Z"

    story = {
        "id": story_id,
        "title": title,
        "competencies": competencies,
        "industry_relevance": industry,
        "strength": max(1, min(5, strength)),
        "star_scores": {"situation": 0, "task": 0, "action": 0, "result": 0},
        "times_used_in_mock": 0,
        "last_evaluator_score": None,
        "prep_refs": [],
        "created_at": now,
        "updated_at": now,
        "evolution_history": [],
        "file": f"{story_id}.md"
    }

    index["stories"].append(story)
    recalculate_coverage(index)
    save_index(base_dir, index)

    # Create story template file
    story_path = base_dir / f"{story_id}.md"
    template = f"""# Story: {title}

> ID: {story_id} | Strength: {strength}/5 | Last updated: {now[:10]}

## Competencies
{', '.join(competencies)}

## Industry Relevance
{', '.join(industry)}

## STAR Content

### Situation
[Describe the background: what project, when, what team, what context]

### Task
[Describe YOUR specific role and goal — not the team's goal]

### Action
[Describe what YOU specifically did — step by step, with detail]

### Result
[Quantified outcomes + what you learned. Use numbers.]

## Evaluator Feedback History
(No feedback yet)

## Adaptation Notes
- **Amazon LP mapping**: [which LPs does this story demonstrate?]
- **Google Googleyness**: [how does this show collaboration/curiosity?]
- **Startup framing**: [how to emphasize speed/ownership?]
"""
    story_path.write_text(template, encoding="utf-8")

    return {
        "status": "created",
        "story": story,
        "file": str(story_path),
        "gap_competencies": index["gap_competencies"]
    }


def list_stories(base_dir: Path) -> dict:
    """List all stories with summary info."""
    index = load_index(base_dir)
    stories = []
    for s in index["stories"]:
        stories.append({
            "id": s["id"],
            "title": s["title"],
            "competencies": s["competencies"],
            "strength": s["strength"],
            "prep_refs": s["prep_refs"],
            "last_evaluator_score": s.get("last_evaluator_score"),
            "times_used_in_mock": s.get("times_used_in_mock", 0)
        })
    return {
        "status": "ok",
        "stories": stories,
        "total": len(stories),
        "gap_competencies": index.get("gap_competencies", [])
    }


def match_stories(base_dir: Path, question: str, company_culture: Optional[str] = None) -> dict:
    """Match stories to a question based on competency overlap and culture alignment."""
    index = load_index(base_dir)
    if not index["stories"]:
        return {"status": "ok", "matches": [], "message": "No stories in storybank"}

    question_lower = question.lower()

    # Detect which competencies the question targets
    question_competencies = {}
    for comp, keywords in COMPETENCY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in question_lower)
        if score > 0:
            question_competencies[comp] = score

    if not question_competencies:
        # Fallback: match all stories by strength
        question_competencies = {c: 0.5 for c in ALL_COMPETENCIES}

    # Get culture weights
    culture_weights = CULTURE_COMPETENCY_WEIGHTS.get(company_culture, {})

    # Score each story
    scored = []
    for story in index["stories"]:
        # Competency match
        comp_match = 0
        for comp in story["competencies"]:
            if comp in question_competencies:
                base = question_competencies[comp]
                culture_boost = culture_weights.get(comp, 1.0)
                comp_match += base * culture_boost

        # Normalize
        max_possible = max(sum(question_competencies.values()), 1)
        comp_score = min(comp_match / max_possible, 1.0)

        # Culture alignment
        culture_score = 0
        if culture_weights:
            for comp in story["competencies"]:
                culture_score += culture_weights.get(comp, 0)
            culture_score = min(culture_score / max(sum(culture_weights.values()), 1), 1.0)

        # Strength
        strength_score = story["strength"] / 5.0

        # Final score
        final = comp_score * 0.5 + culture_score * 0.3 + strength_score * 0.2
        if final > 0.1:
            scored.append({
                "id": story["id"],
                "title": story["title"],
                "match_score": round(final * 100),
                "strength": story["strength"],
                "competencies": story["competencies"],
                "matched_competencies": [c for c in story["competencies"] if c in question_competencies]
            })

    scored.sort(key=lambda x: x["match_score"], reverse=True)

    # Identify gap competencies for this question
    gap_comps = [c for c in question_competencies if c in index.get("gap_competencies", [])]

    return {
        "status": "ok",
        "matches": scored[:3],
        "question_competencies": list(question_competencies.keys()),
        "gap_competencies_for_question": gap_comps
    }


def analyze_gaps(base_dir: Path) -> dict:
    """Analyze competency coverage gaps."""
    index = load_index(base_dir)
    recalculate_coverage(index)

    coverage = {}
    for comp in ALL_COMPETENCIES:
        story_ids = index["competency_coverage"].get(comp, [])
        count = len(story_ids)
        if count == 0:
            level = "GAP"
        elif count == 1:
            level = "WEAK"
        elif count == 2:
            level = "OK"
        else:
            level = "STRONG"
        coverage[comp] = {
            "count": count,
            "level": level,
            "story_ids": story_ids
        }

    return {
        "status": "ok",
        "coverage": coverage,
        "gap_competencies": index["gap_competencies"],
        "total_stories": len(index["stories"]),
        "summary": {
            "STRONG": len([c for c, v in coverage.items() if v["level"] == "STRONG"]),
            "OK": len([c for c, v in coverage.items() if v["level"] == "OK"]),
            "WEAK": len([c for c, v in coverage.items() if v["level"] == "WEAK"]),
            "GAP": len([c for c, v in coverage.items() if v["level"] == "GAP"]),
        }
    }


def evolve_story(base_dir: Path, story_id: str, feedback: str,
                 source_prep: str, new_score: float) -> dict:
    """Evolve a story with evaluator feedback."""
    index = load_index(base_dir)

    story = None
    for s in index["stories"]:
        if s["id"] == story_id:
            story = s
            break

    if not story:
        return {"status": "error", "message": f"Story {story_id} not found"}

    now = datetime.now().isoformat() + "Z"

    story["evolution_history"].append({
        "date": now[:10],
        "source_prep": source_prep,
        "feedback": feedback,
        "previous_score": story.get("last_evaluator_score"),
        "new_score": new_score
    })
    story["last_evaluator_score"] = new_score
    story["times_used_in_mock"] = story.get("times_used_in_mock", 0) + 1
    story["updated_at"] = now

    save_index(base_dir, index)

    # Append feedback to story file
    story_path = base_dir / story["file"]
    if story_path.exists():
        content = story_path.read_text(encoding="utf-8")
        feedback_entry = f"\n- [{now[:10]}, {source_prep} mock] Score: {new_score}/5. \"{feedback}\""
        if "## Evaluator Feedback History" in content:
            content = content.replace(
                "## Evaluator Feedback History",
                f"## Evaluator Feedback History{feedback_entry}",
                1
            )
        else:
            content += f"\n## Evaluator Feedback History{feedback_entry}\n"
        story_path.write_text(content, encoding="utf-8")

    return {
        "status": "evolved",
        "story_id": story_id,
        "new_score": new_score,
        "evolution_count": len(story["evolution_history"]),
        "times_used": story["times_used_in_mock"]
    }


def link_story(base_dir: Path, story_id: str, prep_slug: str) -> dict:
    """Link a story to a prep (cross-prep reuse tracking)."""
    index = load_index(base_dir)

    for story in index["stories"]:
        if story["id"] == story_id:
            if prep_slug not in story["prep_refs"]:
                story["prep_refs"].append(prep_slug)
                story["updated_at"] = datetime.now().isoformat() + "Z"
            save_index(base_dir, index)
            return {
                "status": "linked",
                "story_id": story_id,
                "prep_refs": story["prep_refs"]
            }

    return {"status": "error", "message": f"Story {story_id} not found"}


def delete_story(base_dir: Path, story_id: str) -> dict:
    """Delete a story and recalculate coverage."""
    index = load_index(base_dir)

    story = None
    for s in index["stories"]:
        if s["id"] == story_id:
            story = s
            break

    if not story:
        return {"status": "error", "message": f"Story {story_id} not found"}

    index["stories"] = [s for s in index["stories"] if s["id"] != story_id]
    recalculate_coverage(index)
    save_index(base_dir, index)

    # Remove story file
    story_path = base_dir / story["file"]
    if story_path.exists():
        story_path.unlink()

    return {
        "status": "deleted",
        "story_id": story_id,
        "remaining_stories": len(index["stories"]),
        "gap_competencies": index["gap_competencies"]
    }


def main():
    parser = argparse.ArgumentParser(description="STAR Story Bank Manager")
    parser.add_argument("--action", required=True,
                        choices=["create", "list", "match", "gaps", "evolve", "link", "delete"])
    parser.add_argument("--base-dir", default="./storybank", help="Storybank directory")
    parser.add_argument("--title", help="Story title (for create)")
    parser.add_argument("--competencies", help="Comma-separated competency tags (for create)")
    parser.add_argument("--industry", help="Comma-separated industry tags (for create)")
    parser.add_argument("--strength", type=int, default=3, help="Story strength 1-5 (for create)")
    parser.add_argument("--question", help="Interview question text (for match)")
    parser.add_argument("--company-culture", help="Company culture tag (for match)")
    parser.add_argument("--id", help="Story ID (for evolve/link/delete)")
    parser.add_argument("--feedback", help="Evaluator feedback (for evolve)")
    parser.add_argument("--source-prep", help="Source prep slug (for evolve)")
    parser.add_argument("--new-score", type=float, help="New evaluator score (for evolve)")
    parser.add_argument("--prep-slug", help="Prep slug to link (for link)")

    args = parser.parse_args()
    base_dir = Path(args.base_dir)

    try:
        if args.action == "create":
            if not args.title or not args.competencies:
                result = {"status": "error", "message": "--title and --competencies required for create"}
            else:
                comps = [c.strip() for c in args.competencies.split(",")]
                industries = [i.strip() for i in args.industry.split(",")] if args.industry else []
                result = create_story(base_dir, args.title, comps, industries, args.strength)

        elif args.action == "list":
            result = list_stories(base_dir)

        elif args.action == "match":
            if not args.question:
                result = {"status": "error", "message": "--question required for match"}
            else:
                result = match_stories(base_dir, args.question, args.company_culture)

        elif args.action == "gaps":
            result = analyze_gaps(base_dir)

        elif args.action == "evolve":
            if not all([args.id, args.feedback, args.source_prep, args.new_score]):
                result = {"status": "error", "message": "--id, --feedback, --source-prep, --new-score required for evolve"}
            else:
                result = evolve_story(base_dir, args.id, args.feedback, args.source_prep, args.new_score)

        elif args.action == "link":
            if not args.id or not args.prep_slug:
                result = {"status": "error", "message": "--id and --prep-slug required for link"}
            else:
                result = link_story(base_dir, args.id, args.prep_slug)

        elif args.action == "delete":
            if not args.id:
                result = {"status": "error", "message": "--id required for delete"}
            else:
                result = delete_story(base_dir, args.id)

        else:
            result = {"status": "error", "message": f"Unknown action: {args.action}"}

    except Exception as e:
        result = {"status": "error", "message": str(e)}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
