#!/usr/bin/env python3
"""
ANKLE OS SURF Prompt Matcher & Semantic Image Retriever
Connects any text prompt or creative scene description to the 530K+ image SURF Protocol
using deep metadata tags, vision descriptions, and stylistic layer filtering.

Enables ANKLE OS agents to dynamically pull matching imagery (including pervasive Ankle
motifs like the Foot and Dotted Box) to use as video start frames, Midjourney style refs,
or visual scene assets.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

SURF_API_URL = "https://aleqth.com/api/surf/search"
SURF_PROXY_HOST = "https://ankle.website"

# Core ANKLE iconography and pervasive motifs
ANKLE_SIGNATURE_MOTIFS = [
    "ankle",
    "foot",
    "dotted box",
    "shoe",
    "sculpture",
    "netart"
]

STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves", "shot", "film", "photo", "image", "style", "render"
}


def extract_keywords(prompt: str, top_n: int = 5) -> List[str]:
    """Extract substantive visual keywords from a creative prompt."""
    # Remove flags and urls
    p = re.sub(r"--\w+(?:\s+[^\s-][\w:.%]*)?", " ", prompt)
    p = re.sub(r"https?://\S+", " ", p)
    tokens = re.findall(r"[a-zA-Z]{3,}", p.lower())
    meaningful = [t for t in tokens if t not in STOP_WORDS]
    # Deduplicate while preserving order
    seen = set()
    result = []
    for t in meaningful:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result[:top_n]


def query_surf(query: str, limit: int = 5, layer: Optional[str] = None) -> List[Dict[str, Any]]:
    """Query the live SURF archive API."""
    params = {"q": query, "limit": limit}
    if layer:
        params["layer"] = layer
    url = f"{SURF_API_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "AnkleAgent/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8", "ignore"))
            return data.get("items", [])
    except Exception as e:
        print(f"[!] Warning: Query '{query}' to SURF API failed: {e}", file=sys.stderr)
        return []


def match_prompt_to_surf(
    prompt: str,
    limit_per_keyword: int = 3,
    inject_ankle_motifs: bool = True,
    layer: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Given a user/agent prompt, semantically searches SURF for relevant imagery.
    Optionally weaves in pervasive ANKLE iconography (foot, box, sculpture).
    """
    keywords = extract_keywords(prompt, top_n=4)
    search_terms = list(keywords)

    if inject_ankle_motifs:
        # Check if ankle motifs are already present, otherwise add 1-2 motifs
        if not any(k in ["ankle", "foot"] for k in search_terms):
            search_terms.append("foot")
        if not any(k in ["box", "icon", "logo"] for k in search_terms):
            search_terms.append("sculpture")

    results_by_term = {}
    seen_urls = set()
    collected_matches = []

    for term in search_terms:
        items = query_surf(term, limit=limit_per_keyword, layer=layer)
        term_matches = []
        for it in items:
            raw_url = it.get("url")
            if not raw_url or raw_url in seen_urls:
                continue
            seen_urls.add(raw_url)

            meta = it.get("meta") or {}
            tags = it.get("tags") or meta.get("tags") or []
            vision_desc = meta.get("vision_description") or ""
            vision_summary = meta.get("vision_summary") or {}

            match_entry = {
                "name": it.get("name"),
                "url": raw_url,
                "render_url": f"{SURF_PROXY_HOST}{it.get('render_url', '')}",
                "layer": it.get("layer"),
                "tags": tags[:8],
                "vision_description": vision_desc,
                "vision_style": vision_summary.get("style", ""),
                "vision_mood": vision_summary.get("mood", ""),
                "matched_term": term,
                "is_ankle_motif": term in ["ankle", "foot", "dotted box", "sculpture"]
            }
            term_matches.append(match_entry)
            collected_matches.append(match_entry)

        results_by_term[term] = term_matches

    return {
        "original_prompt": prompt,
        "extracted_keywords": keywords,
        "queried_terms": search_terms,
        "total_unique_matches": len(collected_matches),
        "matches": collected_matches,
        "matches_by_term": results_by_term
    }


def main():
    parser = argparse.ArgumentParser(
        description="SURF Prompt Matcher: Pull imagery from the 530K+ SURF protocol matching any prompt description."
    )
    parser.add_argument("prompt", type=str, help="Text prompt or scene description to match against SURF")
    parser.add_argument("--limit", "-l", type=int, default=3, help="Max results per search term (default: 3)")
    parser.add_argument("--layer", type=str, default=None, help="Optional SURF layer filter (e.g. netart, blindmist, fashion)")
    parser.add_argument("--no-ankle-motifs", action="store_true", help="Disable automatic injection of signature ANKLE motifs (foot, box, sculpture)")
    parser.add_argument("--json", action="store_true", help="Output results in raw JSON format")

    args = parser.parse_args()

    results = match_prompt_to_surf(
        prompt=args.prompt,
        limit_per_keyword=args.limit,
        inject_ankle_motifs=not args.no_ankle_motifs,
        layer=args.layer
    )

    if args.json:
        print(json.dumps(results, indent=2))
        return

    print("=" * 70)
    print(" ANKLE OS SURF PROMPT MATCHER")
    print("=" * 70)
    print(f"Prompt: {results['original_prompt']}")
    print(f"Extracted Keywords: {', '.join(results['extracted_keywords'])}")
    print(f"Queried Terms: {', '.join(results['queried_terms'])}")
    print(f"Total Matches Found: {results['total_unique_matches']}\n")

    for i, m in enumerate(results["matches"], 1):
        motif_badge = "[ANKLE MOTIF]" if m["is_ankle_motif"] else "[SEMANTIC MATCH]"
        print(f"[{i:02d}] {motif_badge} (Matched on '{m['matched_term']}' in layer '{m['layer']}')")
        print(f"     Title/Name: {m['name']}")
        print(f"     Direct URL: {m['url']}")
        print(f"     Proxy Render: {m['render_url']}")
        if m["tags"]:
            print(f"     Metadata Tags: {', '.join(m['tags'])}")
        if m["vision_description"]:
            print(f"     Vision Summary: {m['vision_description']}")
        print()


if __name__ == "__main__":
    main()
