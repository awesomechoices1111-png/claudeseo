#!/usr/bin/env python3
"""
SEO Content Brief Formatter
Parses a structured content brief from plain text or JSON and outputs
a clean, formatted markdown file ready for writer handoff.

Usage:
  python brief_formatter.py --keyword "your target keyword"
  python brief_formatter.py --input brief_data.json
  python brief_formatter.py --demo
"""

import argparse
import json
import sys
from datetime import datetime


DEMO_BRIEF = {
    "keyword": "how to do keyword research",
    "content_type": "How-To Tutorial",
    "intent": "Informational",
    "funnel_stage": "ToFu",
    "word_count_min": 2000,
    "word_count_max": 3000,
    "audience": "Beginner to intermediate SEOs and content marketers",
    "headings": [
        {"level": "H1", "text": "How to Do Keyword Research: A Step-by-Step Guide for 2024"},
        {"level": "H2", "text": "What Is Keyword Research and Why Does It Matter?"},
        {"level": "H3", "text": "How Keywords Connect to Search Intent"},
        {"level": "H2", "text": "Step 1 -- Define Your Topic and Seed Keywords"},
        {"level": "H3", "text": "How to Brainstorm Seed Keywords"},
        {"level": "H3", "text": "Using Your Product or Service as a Starting Point"},
        {"level": "H2", "text": "Step 2 -- Use Keyword Research Tools to Expand Your List"},
        {"level": "H3", "text": "Free Keyword Research Tools"},
        {"level": "H3", "text": "Paid Keyword Research Tools"},
        {"level": "H2", "text": "Step 3 -- Analyze Search Volume and Keyword Difficulty"},
        {"level": "H2", "text": "Step 4 -- Identify Search Intent for Each Keyword"},
        {"level": "H2", "text": "Step 5 -- Prioritize and Finalize Your Keyword List"},
        {"level": "H2", "text": "Common Keyword Research Mistakes to Avoid"},
        {"level": "H2", "text": "Frequently Asked Questions"},
        {"level": "H3", "text": "How long does keyword research take?"},
        {"level": "H3", "text": "What is a good search volume for a keyword?"},
        {"level": "H3", "text": "Can I do keyword research without paid tools?"},
    ],
    "semantic_keywords": {
        "tier1": [
            {"term": "search volume", "placement": "H2/body", "reason": "Core metric for keyword evaluation"},
            {"term": "keyword difficulty", "placement": "H2/body", "reason": "Essential concept for prioritization"},
            {"term": "search intent", "placement": "H2/body", "reason": "Critical for modern SEO strategy"},
            {"term": "long-tail keywords", "placement": "H3/body", "reason": "Key strategy concept"},
            {"term": "SERP analysis", "placement": "body", "reason": "Methodology term"},
            {"term": "organic traffic", "placement": "body", "reason": "Outcome metric"},
            {"term": "seed keywords", "placement": "H2/H3", "reason": "Process starting point"},
            {"term": "keyword intent", "placement": "H2/body", "reason": "Modern SEO core concept"},
        ],
        "tier2": [
            {"term": "keyword gap analysis", "placement": "body", "reason": "Competitive research angle"},
            {"term": "keyword clustering", "placement": "body", "reason": "Advanced technique"},
            {"term": "click-through rate", "placement": "body", "reason": "SERP performance metric"},
            {"term": "content strategy", "placement": "body/conclusion", "reason": "Broader context"},
            {"term": "competitor keywords", "placement": "body", "reason": "Research method"},
            {"term": "monthly search volume", "placement": "body", "reason": "Specific metric variant"},
            {"term": "keyword ranking", "placement": "body", "reason": "Outcome term"},
            {"term": "topic clusters", "placement": "body", "reason": "Modern SEO architecture"},
        ],
        "tier3": [
            {"term": "keyword cannibalization", "placement": "FAQ", "reason": "Common concern"},
            {"term": "zero-click searches", "placement": "body", "reason": "Trend awareness"},
            {"term": "featured snippets", "placement": "body", "reason": "SERP feature angle"},
            {"term": "keyword research spreadsheet", "placement": "H3/body", "reason": "Practical tool"},
        ]
    },
    "competitor_gaps": {
        "common_angles": [
            "How to use Google Keyword Planner",
            "Understanding keyword difficulty scores",
            "Difference between head terms and long-tail keywords",
            "How to analyze competitor keywords",
            "Keyword research for content marketing"
        ],
        "differentiation_opportunities": [
            "Free-tools-only workflow not covered in most guides",
            "B2B vs B2C keyword research differences",
            "Keyword research for local SEO -- underserved angle",
        ],
        "format_gaps": [
            "No comparison table of free vs paid tools",
            "No downloadable keyword research template",
        ]
    },
    "faqs": [
        {
            "question": "How long does keyword research take?",
            "answer_guidance": "For a new site, budget 4-8 hours for thorough research. For a single piece of content, 30-60 minutes is typical. Using the right tools and a repeatable process can cut this significantly.",
            "schema": "FAQPage",
            "target": "PAA box"
        },
        {
            "question": "What is a good search volume for a keyword?",
            "answer_guidance": "There is no universal threshold. A keyword with 100 monthly searches and low competition may drive more ROI than one with 10,000 searches and high competition. Match volume to your site's current authority.",
            "schema": "FAQPage",
            "target": "Featured snippet"
        },
        {
            "question": "Can I do keyword research without paid tools?",
            "answer_guidance": "Yes. Google Keyword Planner, Google Search Console, Google Autocomplete, and AnswerThePublic are all free. Paid tools like Ahrefs or Semrush add volume data and difficulty scores but are not required.",
            "schema": "FAQPage",
            "target": "PAA box"
        },
    ],
    "internal_links": [
        {
            "anchor": "keyword difficulty",
            "destination": "Pillar page on SEO fundamentals",
            "placement": "Step 3 section",
            "purpose": "Contextual relevance"
        },
        {
            "anchor": "content strategy",
            "destination": "Blog post on content planning",
            "placement": "Introduction or conclusion",
            "purpose": "Topical cluster linking"
        },
        {
            "anchor": "search intent",
            "destination": "Guide on search intent types",
            "placement": "Step 4 section",
            "purpose": "Depth + navigation"
        },
    ],
    "writing_notes": [
        "Include at least 2 screenshots of keyword research tools in action",
        "Add a free keyword research template download as a lead magnet CTA",
        "Use personal experience language (E-E-A-T): 'When I analyze keywords for a new client...'",
        "Target reading level: Grade 9-10 (Hemingway App)",
        "Step H2s should use numbered format: 'Step 1 --', 'Step 2 --' for featured snippet eligibility"
    ]
}


def render_heading_tree(headings):
    """Render a visual heading tree."""
    lines = []
    for h in headings:
        level = int(h["level"][1])  # H1=1, H2=2, H3=3
        indent = "  " * (level - 1)
        lines.append(f"{indent}{h['level']}: {h['text']}")
    return "\n".join(lines)


def render_semantic_keywords(semantics):
    """Render semantic keywords by tier."""
    lines = []
    for tier, label in [("tier1", "TIER 1 -- MUST INCLUDE"), ("tier2", "TIER 2 -- SHOULD INCLUDE"), ("tier3", "TIER 3 -- NICE TO INCLUDE")]:
        lines.append(f"\n### {label}\n")
        lines.append(f"{'Term':<30} {'Placement':<20} {'Why It Matters'}")
        lines.append("-" * 75)
        for kw in semantics.get(tier, []):
            lines.append(f"{kw['term']:<30} {kw['placement']:<20} {kw['reason']}")
    return "\n".join(lines)


def render_brief(data):
    """Render a full markdown content brief from structured data."""
    kw = data.get("keyword", "[keyword]")
    now = datetime.now().strftime("%B %d, %Y")

    sections = []

    # Header
    sections.append(f"# SEO Content Brief: {kw.title()}")
    sections.append(f"*Generated: {now}*\n")
    sections.append("---\n")

    # Metadata table
    sections.append("## Brief Overview\n")
    sections.append(f"| Field | Value |")
    sections.append(f"|---|---|")
    sections.append(f"| **Target Keyword** | {kw} |")
    sections.append(f"| **Content Type** | {data.get('content_type', '--')} |")
    sections.append(f"| **Search Intent** | {data.get('intent', '--')} |")
    sections.append(f"| **Funnel Stage** | {data.get('funnel_stage', '--')} |")
    sections.append(f"| **Word Count Target** | {data.get('word_count_min', '--')} -- {data.get('word_count_max', '--')} words |")
    sections.append(f"| **Target Audience** | {data.get('audience', '--')} |")
    sections.append("")

    # Heading structure
    sections.append("---\n")
    sections.append("## Heading Structure\n")
    sections.append("```")
    sections.append(render_heading_tree(data.get("headings", [])))
    sections.append("```\n")

    # Semantic keywords
    sections.append("---\n")
    sections.append("## Semantic Keywords to Include\n")
    sections.append(render_semantic_keywords(data.get("semantic_keywords", {})))
    sections.append("")

    # Competitor gaps
    gaps = data.get("competitor_gaps", {})
    sections.append("---\n")
    sections.append("## Competitor Content Gap Analysis\n")

    sections.append("### Common Angles to Cover (Baseline Requirements)\n")
    for angle in gaps.get("common_angles", []):
        sections.append(f"- {angle}")
    sections.append("")

    sections.append("### Differentiation Opportunities\n")
    for opp in gaps.get("differentiation_opportunities", []):
        sections.append(f"- {opp}")
    sections.append("")

    sections.append("### Format Gaps in Competing Content\n")
    for gap in gaps.get("format_gaps", []):
        sections.append(f"- {gap}")
    sections.append("")

    # FAQs
    sections.append("---\n")
    sections.append("## FAQ Section\n")
    for i, faq in enumerate(data.get("faqs", []), 1):
        sections.append(f"**Q{i}: {faq['question']}**")
        sections.append(f"*Answer guidance:* {faq['answer_guidance']}")
        sections.append(f"*Schema:* {faq.get('schema', 'FAQPage')} | *Target:* {faq.get('target', 'PAA box')}")
        sections.append("")

    sections.append("### FAQPage Schema Template\n")
    sections.append("```json")
    sections.append('{')
    sections.append('  "@context": "https://schema.org",')
    sections.append('  "@type": "FAQPage",')
    sections.append('  "mainEntity": [')
    for faq in data.get("faqs", []):
        sections.append('    {')
        sections.append('      "@type": "Question",')
        sections.append(f'      "name": "{faq["question"]}",')
        sections.append('      "acceptedAnswer": {')
        sections.append('        "@type": "Answer",')
        sections.append('        "text": "[Insert final answer here]"')
        sections.append('      }')
        sections.append('    },')
    sections.append('  ]')
    sections.append('}')
    sections.append("```\n")

    # Internal links
    sections.append("---\n")
    sections.append("## Internal Link Suggestions\n")
    sections.append(f"| Anchor Text | Link To | Placement | Purpose |")
    sections.append(f"|---|---|---|---|")
    for link in data.get("internal_links", []):
        sections.append(f"| {link['anchor']} | {link['destination']} | {link['placement']} | {link['purpose']} |")
    sections.append("")

    # Writing notes
    sections.append("---\n")
    sections.append("## Writing Notes\n")
    for note in data.get("writing_notes", []):
        sections.append(f"- {note}")
    sections.append("")

    sections.append("---\n")
    sections.append("*Brief generated by SEO Content Brief Generator skill for Claude*")

    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description="SEO Content Brief Formatter")
    parser.add_argument("--demo", action="store_true", help="Run with demo data")
    parser.add_argument("--input", type=str, help="Path to JSON brief data file")
    parser.add_argument("--keyword", type=str, help="Target keyword (generates template)")
    parser.add_argument("--output", type=str, help="Output file path (default: stdout)")
    args = parser.parse_args()

    if args.demo:
        data = DEMO_BRIEF
    elif args.input:
        try:
            with open(args.input, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR: Could not load input file -- {e}", file=sys.stderr)
            sys.exit(1)
    elif args.keyword:
        # Return a skeleton template for the keyword
        data = {
            "keyword": args.keyword,
            "content_type": "[Fill in after intent classification]",
            "intent": "[Informational / Commercial / Transactional / Navigational]",
            "funnel_stage": "[ToFu / MoFu / BoFu]",
            "word_count_min": 0,
            "word_count_max": 0,
            "audience": "[Fill in target audience]",
            "headings": [{"level": "H1", "text": f"[Fill in H1 for: {args.keyword}]"}],
            "semantic_keywords": {"tier1": [], "tier2": [], "tier3": []},
            "competitor_gaps": {"common_angles": [], "differentiation_opportunities": [], "format_gaps": []},
            "faqs": [],
            "internal_links": [],
            "writing_notes": []
        }
    else:
        print("Usage: python brief_formatter.py --demo | --input file.json | --keyword 'your keyword'")
        sys.exit(0)

    output = render_brief(data)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Brief written to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
