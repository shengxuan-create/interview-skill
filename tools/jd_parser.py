#!/usr/bin/env python3
"""
jd_parser.py — JD (Job Description) Parser

Extracts structured information from job descriptions.
Supports: URL fetching, plain text input, file input.

Usage:
    python3 jd_parser.py --url https://careers.google.com/jobs/xxx --output /tmp/jd_parsed.json
    python3 jd_parser.py --text "We are looking for..." --output /tmp/jd_parsed.json
    python3 jd_parser.py --file /path/to/jd.txt --output /tmp/jd_parsed.json
    python3 jd_parser.py --help
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_WEB = True
except ImportError:
    HAS_WEB = False

# Common technical skills for matching
TECH_SKILLS = [
    "Python", "Java", "JavaScript", "TypeScript", "Go", "Rust", "C++", "C#",
    "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB", "SQL", "NoSQL",
    "React", "Vue", "Angular", "Node.js", "Django", "Flask", "Spring",
    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Terraform",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
    "Git", "CI/CD", "Linux", "REST", "GraphQL", "gRPC", "Kafka",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "TensorFlow", "PyTorch", "Spark", "Hadoop", "Airflow",
    "Agile", "Scrum", "Jira", "Figma", "Tableau", "Power BI",
]

SOFT_SKILLS_PATTERNS = [
    r"communicat\w+", r"collaborat\w+", r"leadership", r"team\s*work",
    r"problem[- ]solving", r"critical\s+thinking", r"mentor\w*",
    r"cross[- ]functional", r"stakeholder", r"present\w+",
]


def fetch_url(url: str) -> str:
    """Fetch JD content from URL."""
    if not HAS_WEB:
        return ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        return ""

PREFERRED_MARKERS = [
    r"nice\s+to\s+have", r"preferred", r"bonus", r"plus",
    r"ideally", r"a\s+plus", r"not\s+required",
    r"优先", r"加分", r"有.*优先",
]


def _find_preferred_section(text: str) -> str:
    """Extract the 'nice to have' / 'preferred' section of a JD, if any."""
    text_lower = text.lower()
    for marker in PREFERRED_MARKERS:
        m = re.search(marker, text_lower)
        if m:
            # Return text from marker to next section heading or end (max 500 chars)
            start = m.start()
            return text[start:start + 500]
    return ""


def extract_skills(text: str) -> dict:
    """Extract technical and soft skills from JD text, split into required vs preferred."""
    text_lower = text.lower()
    preferred_section = _find_preferred_section(text)
    preferred_lower = preferred_section.lower()

    found_required = []
    found_preferred = []
    for skill in TECH_SKILLS:
        skill_lower = skill.lower()
        if len(skill_lower) <= 2:
            matched = bool(re.search(r'\b' + re.escape(skill_lower) + r'\b', text_lower))
            in_preferred = bool(re.search(r'\b' + re.escape(skill_lower) + r'\b', preferred_lower)) if preferred_lower else False
        else:
            matched = skill_lower in text_lower
            in_preferred = skill_lower in preferred_lower if preferred_lower else False

        if matched:
            if in_preferred:
                found_preferred.append(skill)
            else:
                found_required.append(skill)

    found_soft = []
    for pattern in SOFT_SKILLS_PATTERNS:
        matches = re.findall(pattern, text_lower)
        if matches:
            found_soft.append(matches[0])

    return {
        "technical": list(set(found_required)),
        "preferred": list(set(found_preferred)),
        "soft": list(set(found_soft)),
    }


def extract_experience(text: str) -> str:
    """Extract years of experience requirement."""
    patterns = [
        r"(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?\w+",
        r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?experience",
        r"(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)",
        r"(\d+)年以上",
        r"(\d+)-(\d+)年",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(0)
    return "Not specified"

def extract_level(text: str) -> str:
    """Extract job level/seniority."""
    level_patterns = [
        r"(L\d+)", r"(Senior|Junior|Staff|Principal|Lead|Entry[- ]Level)",
        r"(IC\d+)", r"(P\d+)", r"(T\d+)",
        r"(初级|中级|高级|资深|专家)",
    ]
    for p in level_patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return "Not specified"


def parse_jd(text: str) -> dict:
    """Parse JD text into structured format."""
    skills = extract_skills(text)
    lines = text.split("\n")
    
    # Try to extract title from first meaningful line
    title = "Unknown"
    for line in lines[:10]:
        line = line.strip()
        if len(line) > 5 and len(line) < 200:
            title = line
            break

    return {
        "title": title,
        "level": extract_level(text),
        "required_skills": skills["technical"],
        "preferred_skills": skills["preferred"],
        "soft_skills": skills["soft"],
        "years_experience": extract_experience(text),
        "raw_text": text[:5000],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Parse job descriptions into structured JSON"
    )
    parser.add_argument("--url", help="URL to fetch JD from")
    parser.add_argument("--text", help="JD as plain text")
    parser.add_argument("--file", help="Path to JD file")
    parser.add_argument("--output", help="Output JSON path", default="/tmp/jd_parsed.json")
    args = parser.parse_args()
    # Get JD text
    jd_text = ""
    if args.url:
        if not HAS_WEB:
            print(json.dumps({"error": "missing_deps", "message": "Install requests and beautifulsoup4: pip3 install requests beautifulsoup4"}))
            sys.exit(1)
        jd_text = fetch_url(args.url)
        if not jd_text:
            print(json.dumps({"error": "fetch_failed", "message": f"Could not fetch URL: {args.url}. Try pasting the JD text instead."}))
            sys.exit(1)
    elif args.text:
        jd_text = args.text
    elif args.file:
        p = Path(args.file)
        if not p.exists():
            print(json.dumps({"error": "file_not_found", "message": f"File not found: {args.file}"}))
            sys.exit(1)
        jd_text = p.read_text(encoding="utf-8")
    else:
        parser.print_help()
        sys.exit(1)

    result = parse_jd(jd_text)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()