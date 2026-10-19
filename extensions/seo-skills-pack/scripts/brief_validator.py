#!/usr/bin/env python3
"""
SEO Content Brief Validator
Checks a generated brief for completeness and SEO compliance.

Usage:
  python scripts/brief_validator.py --brief "path/to/brief.md"
  python scripts/brief_validator.py --demo
"""

import sys
import re
import argparse


DEMO_BRIEF = """
CONTENT BRIEF
=============
Primary Keyword:     how to write a meta description
Intent:              Informational
Content Type:        How-to guide
Target Audience:     Beginner
Word Count Target:   1,500 - 2,000 words

H1: How to Write a Meta Description That Gets Clicks

H2: What Is a Meta Description?
  H3: Meta Description vs Title Tag
  H3: How Google Uses Meta Descriptions

H2: Meta Description Best Practices
  H3: Optimal Character Length
  H3: Including Your Target Keyword
  H3: Writing a Clear Call to Action

H2: Meta Description Examples (Good vs Bad)

H2: Common Meta Description Mistakes

H2: Frequently Asked Questions

Meta Title:       How to Write a Meta Description (60-65 chars)
Meta Description: Learn how to write a meta description that boosts CTR. Includes length guidelines, keyword tips, and examples. (155 chars)
URL Slug:         /how-to-write-meta-description
Schema Type:      Article
"""


def validate_brief(content: str) -> dict:
    results = {
        "score": 0,
        "max_score": 100,
        "checks": [],
        "warnings": [],
        "critical": []
    }

    def add_check(label, passed, points, note=""):
        results["checks"].append({
            "label": label,
            "passed": passed,
            "points": points,
            "note": note
        })
        if passed:
            results["score"] += points

    # --- H1 checks ---
    h1_matches = re.findall(r'H1:\s+(.+)', content)
    has_h1 = len(h1_matches) == 1
    add_check("H1 present (exactly one)", has_h1, 15,
              f"Found: {len(h1_matches)}")

    if has_h1:
        h1_text = h1_matches[0]
        h1_len = len(h1_text)
        add_check("H1 under 65 characters", h1_len <= 65, 5,
                  f"H1 length: {h1_len}")

    # --- H2 checks ---
    h2_matches = re.findall(r'H2:\s+(.+)', content)
    has_h2s = len(h2_matches) >= 3
    add_check("At least 3 H2 sections", has_h2s, 10,
              f"Found: {len(h2_matches)} H2s")

    has_faq_h2 = any("faq" in h.lower() or "frequently asked" in h.lower()
                     for h in h2_matches)
    add_check("FAQ section in heading structure", has_faq_h2, 5)

    # --- Word count target ---
    wc_match = re.search(r'[Ww]ord [Cc]ount.*?(\d[\d,]+)\s*[-–]\s*(\d[\d,]+)', content)
    has_word_count = wc_match is not None
    add_check("Word count target specified", has_word_count, 10)
    if has_word_count:
        low = int(wc_match.group(1).replace(",", ""))
        high = int(wc_match.group(2).replace(",", ""))
        range_ok = 500 <= low <= 10000 and high > low
        add_check("Word count range is plausible", range_ok, 5,
                  f"Range: {low}-{high}")

    # --- Meta fields ---
    has_meta_title = bool(re.search(r'[Mm]eta [Tt]itle', content))
    add_check("Meta title included", has_meta_title, 10)

    has_meta_desc = bool(re.search(r'[Mm]eta [Dd]escription', content))
    add_check("Meta description included", has_meta_desc, 10)

    has_url_slug = bool(re.search(r'URL [Ss]lug|/[a-z-]+', content))
    add_check("URL slug specified", has_url_slug, 5)

    has_schema = bool(re.search(r'[Ss]chema', content))
    add_check("Schema type noted", has_schema, 5)

    # --- Semantic keywords ---
    has_tier1 = bool(re.search(r'[Tt]ier 1|[Mm]ust [Ii]nclude', content))
    has_keywords = bool(re.search(r'[Ss]emantic [Kk]eyword|[Kk]eyword [Cc]luster|LSI', content))
    add_check("Semantic keywords section present", has_tier1 or has_keywords, 10)

    # --- Internal links ---
    has_internal = bool(re.search(r'[Ii]nternal [Ll]ink', content))
    add_check("Internal link suggestions included", has_internal, 5)

    # --- Intent classification ---
    has_intent = bool(re.search(r'[Ii]nformational|[Cc]ommercial|[Tt]ransactional|[Nn]avigational', content))
    add_check("Intent classification stated", has_intent, 5)

    # Warnings
    if len(h2_matches) > 12:
        results["warnings"].append(f"High H2 count ({len(h2_matches)}) — consider whether all sections are necessary")

    if not re.search(r'[Gg]ap|[Cc]ompetitor', content):
        results["warnings"].append("No competitor gap analysis detected — brief may be weaker without this")

    if not re.search(r'[Ff]unnel|TOFU|MOFU|BOFU', content):
        results["warnings"].append("No funnel stage mentioned — consider adding for content strategy alignment")

    return results


def print_report(results: dict, label: str = "Brief"):
    score = results["score"]
    max_s = results["max_score"]
    pct = (score / max_s) * 100

    grade = "A" if pct >= 90 else "B" if pct >= 75 else "C" if pct >= 60 else "D"

    print(f"\n{'='*50}")
    print(f"SEO CONTENT BRIEF VALIDATOR")
    print(f"{'='*50}")
    print(f"Brief:  {label}")
    print(f"Score:  {score}/{max_s} ({pct:.0f}%) — Grade: {grade}")
    print()

    print("CHECKS:")
    for c in results["checks"]:
        icon = "PASS" if c["passed"] else "FAIL"
        note = f" [{c['note']}]" if c.get("note") else ""
        pts = f"+{c['points']}pts" if c["passed"] else f"  0/{c['points']}pts"
        print(f"  [{icon}] {pts}  {c['label']}{note}")

    if results["warnings"]:
        print("\nWARNINGS:")
        for w in results["warnings"]:
            print(f"  [WARN] {w}")

    if results["critical"]:
        print("\nCRITICAL:")
        for c in results["critical"]:
            print(f"  [CRIT] {c}")

    print()
    if pct >= 90:
        print("Result: EXCELLENT — Brief is comprehensive and ready for writers.")
    elif pct >= 75:
        print("Result: GOOD — Brief is solid. Address failing checks to strengthen it.")
    elif pct >= 60:
        print("Result: FAIR — Several sections missing. Review failing checks before sending to writers.")
    else:
        print("Result: INCOMPLETE — Brief needs significant additions before it is writer-ready.")
    print(f"{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Validate an SEO content brief for completeness."
    )
    parser.add_argument("--brief", help="Path to brief markdown file")
    parser.add_argument("--demo", action="store_true", help="Run with demo brief")
    args = parser.parse_args()

    if args.demo:
        content = DEMO_BRIEF
        label = "Demo Brief (how to write a meta description)"
    elif args.brief:
        try:
            with open(args.brief, "r") as f:
                content = f.read()
            label = args.brief
        except FileNotFoundError:
            print(f"Error: File not found: {args.brief}")
            sys.exit(1)
    else:
        print("Usage: python scripts/brief_validator.py --brief path/to/brief.md")
        print("       python scripts/brief_validator.py --demo")
        sys.exit(0)

    results = validate_brief(content)
    print_report(results, label)


if __name__ == "__main__":
    main()
