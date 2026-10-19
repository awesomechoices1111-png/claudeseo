---
name: seo-content-brief-generator
description: "Generates complete SEO content briefs from a target keyword. Produces a ready-to-write brief with H1/H2/H3 heading structure, word count target, semantic keywords to include, competitor content gap analysis, FAQ section, and internal link suggestions. Use when user says create content brief, write a content brief, SEO brief for keyword, brief for blog post, content outline for SEO, what should I write about for keyword, heading structure for article, semantic keywords for topic, competitor gap analysis for content, FAQ ideas for article, how long should my article be, or provides a keyword and asks how to write content that ranks."
---

# SEO Content Brief Generator

Produces a full, writer-ready SEO content brief from a single target keyword. Each brief covers heading architecture, word count target, semantic keyword clusters, competitor gap analysis, FAQ opportunities, and internal link suggestions.

## What to Collect Before Generating

**Minimum required:**
- Target keyword (primary)

**Optional inputs that improve the brief:**
- Domain or site URL (enables tailored internal link suggestions)
- Competing URLs to analyze (for gap analysis)
- Content type preference (blog post, landing page, comparison, listicle, how-to)
- Target audience (beginner / intermediate / expert)
- Existing content on the site (for internal linking)

If the user provides only a keyword, proceed with the full brief using search-based inference. Do not block on missing inputs.

---

## Step 1: Keyword Intent Classification

Classify the primary keyword before writing anything else. This drives every downstream decision.

Determine:
- **Intent type**: Informational / Navigational / Commercial / Transactional
- **Content format signal**: Blog post, listicle, how-to guide, comparison, landing page, definition/glossary
- **Audience sophistication**: Beginner, intermediate, expert
- **Funnel stage**: TOFU (awareness), MOFU (consideration), BOFU (decision)

Output a one-line intent summary:
```
Intent: Informational | Format: How-to guide | Audience: Beginner | Funnel: TOFU
```

Consult `references/intent-classification-guide.md` for edge cases and dual-intent keywords.

---

## Step 2: SERP and Competitor Analysis

Identify the content patterns Google rewards for this keyword.

Analyze:
1. **Dominant content type** — What format holds positions 1-5? (listicles, long-form guides, product pages, etc.)
2. **Average word count** — Estimate from top-ranking pages
3. **Heading patterns** — Common H2/H3 topics that recur across top results
4. **Missing angles** — Topics that competitors cover poorly or skip entirely
5. **Featured snippet opportunity** — Is there a definition box, list, or table to target?

Use web search to examine 3-5 competitor URLs if available. Summarize gaps in a table:

| Competitor Topic | Covered Well | Partially Covered | Missing |
|-----------------|-------------|------------------|---------|
| [Topic A]       | Yes         |                  |         |
| [Topic B]       |             | Yes              |         |
| [Topic C]       |             |                  | Yes     |

Mark missing topics as brief priorities.

Consult `references/competitor-gap-analysis.md` for the full gap analysis methodology.

---

## Step 3: Word Count Target

Set a data-driven word count range, not an arbitrary number.

Use this framework:

| Intent Type | Typical Range | Rationale |
|------------|--------------|-----------|
| Transactional (product/landing) | 800-1,500 | Conversion-focused, minimal friction |
| Informational (definition/glossary) | 1,200-2,000 | Thorough but not bloated |
| Informational (how-to guide) | 1,500-3,000 | Step-by-step depth required |
| Informational (ultimate guide) | 3,000-5,000+ | Comprehensive authority piece |
| Comparison / Best-of listicle | 2,000-4,000 | Depth per option required |

Adjust based on:
- Average competitor word count (match or beat by 10-20%)
- Audience expertise (experts need less hand-holding)
- Content gap volume (more gaps = more content needed)

Output a specific target range: e.g., **2,200-2,800 words**

---

## Step 4: Heading Structure (H1 / H2 / H3)

Generate the full heading architecture. This is the core deliverable of the brief.

### H1 Rules
- One H1 only — the page title
- Include the exact primary keyword
- Match search intent (question format for informational, benefit-led for commercial)
- Under 65 characters for clean SERP display

### H2 Rules
- Each H2 = a major topic section
- Cover the top competitor topics AND the identified gap topics
- Order logically: foundational concepts before advanced, general before specific
- Include secondary keywords naturally where relevant

### H3 Rules
- Each H3 = a subtopic within its parent H2
- Use for step-by-step sequences, feature breakdowns, examples, or comparisons
- Not every H2 needs H3s — use when content genuinely has distinct sub-sections

### Output Format

```
H1: [Page Title Including Primary Keyword]

H2: [Section 1 — foundational / definitional]
  H3: [Subtopic 1.1]
  H3: [Subtopic 1.2]

H2: [Section 2 — main how-to or core topic]
  H3: [Step / Feature / Method 1]
  H3: [Step / Feature / Method 2]
  H3: [Step / Feature / Method 3]

H2: [Section 3 — advanced or differentiated angle]
  H3: [Subtopic 3.1]

H2: [Section 4 — FAQ or common mistakes]

H2: [Conclusion / Summary / Next Steps]
```

Consult `references/heading-architecture-guide.md` for keyword placement rules and heading patterns by content type.

---

## Step 5: Semantic Keywords

Generate a semantic keyword list the writer should incorporate naturally throughout the article.

Organize into three tiers:

**Tier 1 — Must Include (high relevance, frequently appear in top results):**
List 8-12 terms. These are closely related phrases, synonyms, and LSI keywords that signal topic completeness to Google.

**Tier 2 — Should Include (secondary signals, enrich content):**
List 6-10 terms. Related entities, tools, people, brands, or concepts that authoritative content on this topic typically mentions.

**Tier 3 — Consider Including (long-tail, niche depth signals):**
List 4-6 terms. Question-based phrases, specific variations, or emerging terminology in the space.

For each term, note:
- Suggested placement (H2, H3, body, meta description, alt text)
- Natural usage context (one sentence example if helpful)

Consult `references/semantic-keyword-guide.md` for entity mapping and NLP-based keyword clustering methodology.

---

## Step 6: FAQ Section

Generate 5-8 FAQ questions with brief answer guidance.

FAQ selection criteria:
1. **People Also Ask** — Pull questions from Google PAA boxes for this keyword
2. **Search intent gaps** — Questions competitors answer poorly
3. **Funnel advancement** — Questions that move readers toward conversion
4. **Featured snippet opportunity** — Questions with clear, concise answers that could win position zero

Output format:
```
Q: [Question]
Answer guidance: [2-3 sentences on what the answer should cover. Include key facts or data points if known.]
Word target: [50-150 words]
Schema opportunity: FAQPage markup
```

Consult `references/faq-generation-guide.md` for PAA research methodology and schema markup guidance.

---

## Step 7: Internal Link Suggestions

Generate internal link recommendations to strengthen topical authority and support crawlability.

### If site URL provided:
Suggest specific pages on the user's site to link to/from based on topical relevance. Frame each as:
- **Link from**: [new article section] to **Link to**: [existing page URL/topic]
- **Anchor text**: [recommended anchor text]
- **Rationale**: [why this link supports both pages]

### If no site URL provided:
Suggest the types of content that should exist internally and link to/from this article:
- **Supporting content** (link to from this article): pages that provide foundational context
- **Pillar content** (link from this article to): broader topic hubs this article supports
- **Sibling content** (lateral links): similar-depth articles on related subtopics

Target 3-5 outbound internal links per article. Note where in the heading structure each link fits naturally.

---

## Step 8: Output the Full Brief

Deliver the complete content brief in a clean, copy-paste ready format.

### Brief Header
```
CONTENT BRIEF
=============
Primary Keyword:     [keyword]
Intent:              [Informational / Commercial / etc.]
Content Type:        [Blog post / How-to guide / etc.]
Target Audience:     [Beginner / Intermediate / Expert]
Word Count Target:   [X,XXX - X,XXX words]
Priority:            [High / Medium]
Brief Created:       [Date]
```

Then output each section in order:
1. Heading Structure (H1/H2/H3 tree)
2. Semantic Keywords (3 tiers)
3. Competitor Gap Summary (table)
4. FAQ Section (5-8 questions with guidance)
5. Internal Link Suggestions
6. On-Page SEO Checklist

### On-Page SEO Checklist (always include)
```
Meta Title:        [60-65 chars, includes primary keyword near start]
Meta Description:  [150-160 chars, includes keyword + CTA]
URL Slug:          /[short-kebab-case-url]
Primary Keyword:   In H1, first 100 words of body, at least one H2
Image Alt Text:    Describe images with keyword context
Schema Type:       [Article / HowTo / FAQPage / Product]
Featured Snippet:  [Target type: definition box / numbered list / table]
```

---

## Examples

### Example 1: Informational keyword

**User says:** "Create a content brief for 'how to write a meta description'"

**Actions:**
1. Classify intent: Informational, How-to, Beginner-intermediate, TOFU
2. Analyze SERP: step-by-step guides, 1,200-2,000 words
3. Set word count: 1,500-2,000 words
4. Generate heading tree: definition, character limits, best practices, examples, common mistakes
5. Build semantic list: "meta description length", "click-through rate", "SERP snippet", "call to action"
6. Generate FAQs from PAA: "How long should a meta description be?", "Do meta descriptions affect SEO?"
7. Suggest internal links: SEO basics guide, on-page SEO checklist, title tag guide

**Result:** Full writer-ready brief delivered in one response.

### Example 2: Commercial keyword with competitor URLs

**User says:** "Content brief for 'best CRM for small business' — here are 3 competitor URLs"

**Actions:**
1. Classify intent: Commercial investigation, Best-of listicle, SMB audience, MOFU
2. Fetch and analyze competitor URLs for heading patterns and gaps
3. Set word count: 3,000-4,000 words
4. Generate heading tree with H2 per CRM + pricing comparison + use case recommendations
5. Flag gaps: competitors skip freelancer use case and free tier options
6. FAQs focused on decision-making: "Which CRM is easiest to set up?", "What is the best free CRM?"
7. Internal links: sales process guide, email marketing tools comparison

**Result:** Gap-first brief positioned to outrank existing listicles.

---

## Troubleshooting

### Issue: Keyword has very low search volume
Proceed with the brief. Low-volume keywords often have high conversion intent. Note the volume context in the brief header but do not refuse.

### Issue: Keyword has ambiguous dual intent (informational + commercial)
Flag the dual intent explicitly. Generate a heading structure that serves both — informational introduction, commercial middle sections with recommendations. Note the decision in the brief.

### Issue: No competitor URLs and SERP data is unclear
Default to informational how-to structure. It is the most versatile format and performs across most keyword types. Note the assumption at the top of the brief.

### Issue: Very technical topic
Adjust audience to Expert, reduce definitional content, increase H3 depth. Technical content typically targets longer word counts (3,000+) and more granular semantic keywords.
