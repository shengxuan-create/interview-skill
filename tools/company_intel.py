#!/usr/bin/env python3
"""
company_intel.py — Company Intelligence Aggregator

Aggregates company information from multiple sources.
Generates structured queries for the AI agent to execute via WebSearch.

Usage:
    python3 company_intel.py --company Google --output /tmp/company_intel.json
    python3 company_intel.py --company 字节跳动 --output /tmp/company_intel.json
    python3 company_intel.py --help
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SEARCH_DIMENSIONS = [
    {
        "dimension": "company_overview",
        "queries": [
            '"{company}" company overview employees size revenue',
            '"{company}" Wikipedia',
        ],
        "description": "Company basics: size, industry, HQ, founding",
    },
    {
        "dimension": "tech_stack",
        "queries": [
            '"{company}" engineering tech stack technology blog',
            '"{company}" developer tools infrastructure',
        ],
        "description": "Technology stack and engineering culture",
    },
    {
        "dimension": "culture_values",
        "queries": [
            '"{company}" company culture values work environment',
            '"{company}" glassdoor reviews culture',
        ],
        "description": "Company culture, values, work style",
    },
    {
        "dimension": "recent_news",
        "queries": [
            '"{company}" hiring layoffs news {year}',
            '"{company}" latest news product launch {year}',
        ],
        "description": "Recent 3-month news and developments",
    },
]

def build_queries(company: str) -> dict:
    """Build all search queries for company intelligence."""
    year = datetime.now().year
    all_queries = []
    
    for dim in SEARCH_DIMENSIONS:
        for q_template in dim["queries"]:
            q = q_template.format(company=company, year=year)
            all_queries.append({
                "dimension": dim["dimension"],
                "query": q,
                "description": dim["description"],
            })
    
    return all_queries


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate company intelligence from multiple sources"
    )
    parser.add_argument("--company", required=True, help="Target company name")
    parser.add_argument("--output", default="/tmp/company_intel.json", help="Output JSON path")
    args = parser.parse_args()

    queries = build_queries(args.company)
    
    result = {
        "company": args.company,
        "timestamp": datetime.now().isoformat(),
        "dimensions": [d["dimension"] for d in SEARCH_DIMENSIONS],
        "total_queries": len(queries),
        "queries": queries,
        "instructions": (
            "Execute each query via WebSearch. For each dimension, "
            "extract relevant structured data. Pass results to "
            "result_evaluator.md for scoring and filtering."
        ),
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()