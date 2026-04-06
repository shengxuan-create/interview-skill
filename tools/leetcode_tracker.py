#!/usr/bin/env python3
"""
leetcode_tracker.py — LeetCode Frequency Tracker

Finds frequently asked LeetCode problems for a given company.
Uses search-based approach (not direct API scraping).

Usage:
    python3 leetcode_tracker.py --company Google --months 6 --output /tmp/leetcode_freq.json
    python3 leetcode_tracker.py --company 字节跳动 --limit 20 --output /tmp/leetcode_freq.json
    python3 leetcode_tracker.py --help
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
    HAS_WEB = True
except ImportError:
    HAS_WEB = False


# Well-known company LeetCode tag mappings
COMPANY_ALIASES = {
    "google": "google", "谷歌": "google",
    "meta": "facebook", "facebook": "facebook",
    "amazon": "amazon", "亚马逊": "amazon",    "apple": "apple", "苹果": "apple",
    "microsoft": "microsoft", "微软": "microsoft",
    "netflix": "netflix",
    "uber": "uber", "tesla": "tesla",
    "字节跳动": "bytedance", "bytedance": "bytedance",
    "阿里巴巴": "alibaba", "alibaba": "alibaba",
    "腾讯": "tencent", "tencent": "tencent",
}


def normalize_company(name: str) -> str:
    """Normalize company name to LeetCode tag."""
    return COMPANY_ALIASES.get(name.lower(), name.lower().replace(" ", "-"))


def build_search_queries(company: str, months: int) -> list:
    """Build search queries to find LeetCode frequency data."""
    tag = normalize_company(company)
    return [
        {
            "purpose": "leetcode_company_tag",
            "query": f"site:leetcode.com/company/{tag}",
            "description": f"LeetCode company tag page for {company}",
        },
        {
            "purpose": "leetcode_discuss_frequency",
            "query": f'site:leetcode.com/discuss "{company}" frequency top problems {datetime.now().year}',
            "description": f"LeetCode discussion about {company} frequent problems",
        },
        {
            "purpose": "external_frequency_list",
            "query": f'"{company}" leetcode top frequent interview problems {datetime.now().year}',
            "description": f"External sites tracking {company} LeetCode frequency",
        },
    ]

def main():
    parser = argparse.ArgumentParser(
        description="Track LeetCode frequency for a company"
    )
    parser.add_argument("--company", required=True, help="Target company name")
    parser.add_argument("--months", type=int, default=6, help="Look back period in months")
    parser.add_argument("--limit", type=int, default=20, help="Max problems to return")
    parser.add_argument("--output", default="/tmp/leetcode_freq.json", help="Output JSON path")
    args = parser.parse_args()

    queries = build_search_queries(args.company, args.months)
    tag = normalize_company(args.company)

    result = {
        "company": args.company,
        "company_tag": tag,
        "period": f"last_{args.months}_months",
        "timestamp": datetime.now().isoformat(),
        "leetcode_url": f"https://leetcode.com/company/{tag}/",
        "search_queries": queries,
        "instructions": (
            "Use WebSearch to execute the queries above. "
            "Extract problem names, difficulty, and frequency from results. "
            "If direct LeetCode access fails, use external frequency trackers."
        ),
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()