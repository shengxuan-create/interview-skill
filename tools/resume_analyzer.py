#!/usr/bin/env python3
"""
resume_analyzer.py — Resume Analyzer & JD Matcher

Parses resume (PDF or text) and compares against a parsed JD.
Outputs match score, skill gaps, and preparation priorities.

Usage:
    python3 resume_analyzer.py --resume /path/to/resume.pdf --jd /tmp/jd_parsed.json --output /tmp/resume_match.json
    python3 resume_analyzer.py --resume-text "..." --jd /tmp/jd_parsed.json --output /tmp/resume_match.json
    python3 resume_analyzer.py --help
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import pdfplumber
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

# Common skill synonyms for fuzzy matching
SKILL_SYNONYMS = {
    "js": "javascript", "ts": "typescript", "py": "python",
    "node": "node.js", "react.js": "react", "vue.js": "vue",
    "postgres": "postgresql", "mongo": "mongodb",
    "k8s": "kubernetes", "tf": "terraform",
    "ml": "machine learning", "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision", "ai": "artificial intelligence",
}


def extract_pdf_text(path: str) -> str:
    """Extract text from PDF resume."""
    if not HAS_PDF:
        return ""
    try:
        text_parts = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_parts.append(t)
        return "\n".join(text_parts)
    except Exception:
        return ""


def normalize_skill(skill: str) -> str:
    """Normalize skill name for comparison."""
    s = skill.lower().strip()
    return SKILL_SYNONYMS.get(s, s)

def extract_skills_from_text(text: str) -> set:
    """Extract skills mentioned in resume text."""
    # Import the skill list from jd_parser
    tech_skills = [
        "Python", "Java", "JavaScript", "TypeScript", "Go", "Rust", "C++", "C#",
        "Ruby", "PHP", "Swift", "Kotlin", "SQL", "R", "MATLAB",
        "React", "Vue", "Angular", "Node.js", "Django", "Flask", "Spring",
        "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Terraform",
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "Git", "CI/CD", "Linux", "REST", "GraphQL", "gRPC", "Kafka",
        "Machine Learning", "Deep Learning", "NLP", "TensorFlow", "PyTorch",
        "Spark", "Hadoop", "Airflow", "Figma", "Tableau",
    ]
    text_lower = text.lower()
    found = set()
    for skill in tech_skills:
        skill_lower = skill.lower()
        if len(skill_lower) <= 2:
            if re.search(r'\b' + re.escape(skill_lower) + r'\b', text_lower):
                found.add(skill)
        else:
            if skill_lower in text_lower:
                found.add(skill)
    return found


def extract_years(text: str) -> str:
    """Estimate years of experience from resume."""
    patterns = [
        r"(\d+)\+?\s*years?\s*(?:of\s+)?experience",
        r"(\d+)年.*经验",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return f"~{m.group(1)} years"
    return "Unknown"

def match_skills(resume_skills: set, jd_data: dict) -> dict:
    """Compare resume skills against JD requirements."""
    jd_required = set(normalize_skill(s) for s in jd_data.get("required_skills", []))
    jd_preferred = set(normalize_skill(s) for s in jd_data.get("preferred_skills", []))
    resume_norm = set(normalize_skill(s) for s in resume_skills)

    matched = resume_norm & (jd_required | jd_preferred)
    gap_required = jd_required - resume_norm
    gap_preferred = jd_preferred - resume_norm

    total = len(jd_required | jd_preferred)
    score = int((len(matched) / max(total, 1)) * 100)

    return {
        "match_score": score,
        "matched_skills": sorted(matched),
        "gap_skills": sorted(gap_required),
        "gap_preferred": sorted(gap_preferred),
        "preparation_priority": sorted(gap_required)[:5],
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze resume and match against JD")
    parser.add_argument("--resume", help="Path to resume PDF")
    parser.add_argument("--resume-text", help="Resume as plain text")
    parser.add_argument("--jd", required=True, help="Path to parsed JD JSON")
    parser.add_argument("--output", default="/tmp/resume_match.json", help="Output JSON path")
    args = parser.parse_args()
    # Get resume text
    resume_text = ""
    if args.resume:
        if args.resume.lower().endswith(".pdf"):
            if not HAS_PDF:
                print(json.dumps({"error": "missing_deps", "message": "Install pdfplumber: pip3 install pdfplumber"}))
                sys.exit(1)
            resume_text = extract_pdf_text(args.resume)
            if not resume_text:
                print(json.dumps({"error": "pdf_parse_failed", "message": "Could not extract text from PDF. Try pasting resume text instead."}))
                sys.exit(1)
        else:
            resume_text = Path(args.resume).read_text(encoding="utf-8")
    elif args.resume_text:
        resume_text = args.resume_text
    else:
        print(json.dumps({"error": "no_input", "message": "Provide --resume or --resume-text"}))
        sys.exit(1)

    # Load JD
    jd_data = json.loads(Path(args.jd).read_text(encoding="utf-8"))

    # Analyze
    resume_skills = extract_skills_from_text(resume_text)
    years = extract_years(resume_text)
    match_result = match_skills(resume_skills, jd_data)
    match_result["experience_detected"] = years
    match_result["resume_skills_found"] = sorted(resume_skills)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(match_result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(match_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()