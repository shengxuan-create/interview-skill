#!/usr/bin/env python3
"""
interview_scraper.py — Interview Experience Aggregator

Aggregates interview experiences from multiple sources via search engines.
Does NOT directly scrape Glassdoor/Blind (will get blocked).
Instead, uses search engine queries to find publicly available interview data.

Usage:
    python3 interview_scraper.py --company Google --role "Software Engineer" --output /tmp/interviews.json
    python3 interview_scraper.py --company 字节跳动 --role "后端工程师" --sources glassdoor,blind,1point3acres --output /tmp/interviews.json
    python3 interview_scraper.py --help
"""

import argparse
import json
import sys
import re
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_WEB = True
except ImportError:
    HAS_WEB = False

# Data source configurations
SOURCES = {
    "glassdoor": {
        "query_template": '"{company}" interview experience "{role}" site:glassdoor.com',
        "name": "Glassdoor",
    },
    "blind": {
        "query_template": '"{company}" interview "{role}" site:teamblind.com',
        "name": "Blind/TeamBlind",
    },
    "1point3acres": {
        "query_template": '"{company}" 面试 "{role}" site:1point3acres.com',
        "name": "一亩三分地",
    },
    "reddit": {
        "query_template": '"{company}" interview experience "{role}" site:reddit.com',
        "name": "Reddit",
    },
    "leetcode": {
        "query_template": '"{company}" interview "{role}" site:leetcode.com/discuss',
        "name": "LeetCode Discuss",
    },
}


def build_queries(company: str, role: str, sources: list) -> list:
    """Build search queries for each source."""
    queries = []
    for src in sources:
        if src in SOURCES:
            q = SOURCES[src]["query_template"].format(company=company, role=role)
            queries.append({"source": src, "query": q, "name": SOURCES[src]["name"]})
    return queries

def search_source(query_info: dict) -> dict:
    """
    Search a single source. In practice, this would use a search API.
    The tool outputs structured query info for the AI agent to execute via WebSearch.
    """
    result = {
        "source": query_info["source"],
        "source_name": query_info["name"],
        "query": query_info["query"],
        "status": "query_ready",
        "message": f"Execute this query via WebSearch: {query_info['query']}",
        "data_points": [],
    }
    
    # If requests is available, attempt a basic search
    if HAS_WEB:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
            search_url = f"https://www.google.com/search?q={requests.utils.quote(query_info['query'])}&num=10"
            resp = requests.get(search_url, headers=headers, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                links = []
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if href.startswith("/url?q="):
                        url = href.split("/url?q=")[1].split("&")[0]
                        if "google.com" not in url:
                            links.append(url)
                result["status"] = "urls_found"
                result["urls"] = links[:5]
        except Exception as e:
            result["status"] = "search_failed"
            result["error"] = str(e)
    
    return result

def aggregate(company: str, role: str, sources: list) -> dict:
    """Aggregate interview data from multiple sources."""
    queries = build_queries(company, role, sources)
    results = []
    errors = []
    
    for q in queries:
        r = search_source(q)
        if r["status"] == "search_failed":
            errors.append({"source": r["source"], "error": r.get("error", "unknown"), "query": r["query"]})
        else:
            results.append(r)
    
    return {
        "company": company,
        "role": role,
        "timestamp": datetime.now().isoformat(),
        "sources_searched": len(queries),
        "sources_with_results": len([r for r in results if r["status"] == "urls_found"]),
        "queries": results,
        "errors": errors,
        "instructions": "Use the queries above with WebSearch to fetch actual interview data. "
                       "Each query targets a specific source. Process results through result_evaluator.md.",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate interview experiences from multiple sources"
    )
    parser.add_argument("--company", required=True, help="Target company name")
    parser.add_argument("--role", default="", help="Target role/position")
    parser.add_argument("--sources", default="glassdoor,blind,1point3acres,reddit",
                       help="Comma-separated list of sources")
    parser.add_argument("--output", default="/tmp/interviews.json", help="Output JSON path")
    args = parser.parse_args()
    source_list = [s.strip() for s in args.sources.split(",")]
    result = aggregate(args.company, args.role, source_list)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()