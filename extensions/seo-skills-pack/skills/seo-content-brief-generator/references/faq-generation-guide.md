# FAQ Generation Guide

## Why FAQs Matter for SEO

FAQ sections serve two compounding purposes:
1. **Featured snippets** — Individual Q&A pairs can win "People Also Ask" boxes and position-zero results
2. **Long-tail keyword coverage** — Questions naturally contain long-tail variants that would be awkward in body copy

A well-constructed FAQ section can generate as much organic traffic as the core article content.

---

## FAQ Research Methods

### Method 1: Google PAA Mining
Search the primary keyword. The "People Also Ask" box shows the questions Google already surfaces for this topic.

Expand each PAA result — this triggers more related questions to appear. Collect 10-15 candidate questions, then filter to the best 5-8.

### Method 2: AlsoAsked.com
Free tool that maps PAA question trees by keyword. Shows how questions branch and relate to each other. Excellent for identifying question clusters.

### Method 3: AnswerThePublic
Generates questions, prepositions, and comparisons around any seed keyword. Useful for finding angle-specific questions competitors miss.

### Method 4: Reddit and Quora Research
Search the primary keyword on Reddit and Quora. Real user questions reveal language patterns, misconceptions, and edge case concerns that PAA may not capture.

### Method 5: Competitor FAQ Sections
Review the FAQ sections of the top 5 ranking pages. Identify which questions they answer and — critically — which they skip.

---

## FAQ Selection Criteria

Rate each candidate question on these four dimensions:

| Criterion | What to Ask |
|-----------|------------|
| Search intent match | Does this question extend or deepen the article's core intent? |
| Answer conciseness | Can it be answered in 50-150 words? (snippet-optimal) |
| Conversion relevance | Does answering this move the reader closer to action? |
| Gap opportunity | Do competitors skip this question or answer it poorly? |

Select questions that score highest across multiple criteria. Avoid questions that require 500+ word answers — these belong in the body, not the FAQ.

---

## FAQ Answer Structure

Each FAQ answer should follow a consistent pattern for featured snippet optimization:

1. **Direct answer first** — Answer the question in the first sentence, without preamble
2. **Supporting context** — 2-3 sentences of explanation, nuance, or data
3. **Optional CTA or link** — Where relevant, point to a related section or page

**Example:**
```
Q: How long should a meta description be?

A: Meta descriptions should be between 150 and 160 characters. Google typically truncates descriptions longer than this in search results, cutting off your message. While Google may rewrite meta descriptions, writing a compelling 155-character description gives you the best chance of controlling your SERP snippet.
```

---

## Schema Markup for FAQs

FAQPage schema allows Google to display FAQs directly in search results, sometimes expanding into rich results that take up more SERP real estate.

### Implementation

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How long should a meta description be?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Meta descriptions should be between 150 and 160 characters. Google typically truncates descriptions longer than this in search results."
      }
    }
  ]
}
```

### FAQPage Schema Rules
- Include all FAQ questions present on the page in the schema
- The "text" field in acceptedAnswer should match the visible on-page answer closely
- Do not include FAQs in schema that are not visible on the page
- Google may choose not to show FAQPage rich results if the content is promotional

---

## FAQ Ordering Logic

Order FAQ questions from most to least commonly asked:
1. Questions that would appear as barriers to reading on (definitional concerns)
2. Questions about process or implementation
3. Questions about edge cases or troubleshooting
4. Questions that advance toward conversion

The most common beginner question goes first. The most conversion-adjacent question goes last.
