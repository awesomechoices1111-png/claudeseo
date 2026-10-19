# AEO Schema Markup Guide

Schema markup increases the probability of featured snippet and PAA selection by helping search engines understand content structure, type, and intent.

## Priority Schema for AEO

### 1. FAQPage Schema

Most important for AEO. Explicitly marks Q&A content for snippet selection.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is [Topic]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Direct answer in 40-80 words. Full sentences only. No HTML tags inside text. Start with the topic keyword. Factual and specific."
      }
    },
    {
      "@type": "Question",
      "name": "How does [Process] work?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Explanation of the process in 40-80 words. Use plain language."
      }
    },
    {
      "@type": "Question",
      "name": "What are the benefits of [Topic]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The main benefits of [Topic] include X, Y, and Z. Each benefit contributes to [outcome]."
      }
    }
  ]
}
```

**AEO Rules for FAQPage:**
- `name` field = the exact question (match how users ask it)
- `text` field = plain text only, no HTML, no markdown
- Keep `text` between 40-300 words (shorter = better for snippets)
- Add 5-10 question/answer pairs per page minimum
- Questions should match real PAA questions from your research

---

### 2. HowTo Schema

Targets process/step-based featured snippets and voice search.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to [Task]",
  "description": "What this guide helps you accomplish in 1-2 sentences.",
  "totalTime": "PT15M",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "Step 1 Short Name",
      "itemListElement": {
        "@type": "HowToDirection",
        "text": "Full instruction for this step. Be specific and actionable. Under 30 words."
      }
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "Step 2 Short Name",
      "itemListElement": {
        "@type": "HowToDirection",
        "text": "Full instruction for step 2. Specific and actionable."
      }
    }
  ]
}
```

**AEO Rules for HowTo:**
- Keep step `text` under 30 words for voice compatibility
- Use strong action verbs to start each step ("Click", "Enter", "Select")
- Include `totalTime` in ISO 8601 duration format (PT15M = 15 minutes)
- Steps should match the numbered list in your visible content exactly

---

### 3. Speakable Schema (Voice Search)

Marks specific content blocks as suitable for voice assistant reading. Currently a Google beta feature.

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [
      ".article-body h2",
      ".direct-answer",
      "#key-takeaways"
    ]
  },
  "url": "https://www.example.com/page-url"
}
```

**When to use Speakable:**
- News articles and content with clear summary sections
- Pages targeting high-volume voice queries
- Any content with dedicated summary/TL;DR sections

---

### 4. QAPage Schema (Community Q&A)

Use when the page format is a single question with one primary expert answer (not multiple FAQs).

```json
{
  "@context": "https://schema.org",
  "@type": "QAPage",
  "mainEntity": {
    "@type": "Question",
    "name": "What is the best approach to [Topic]?",
    "text": "Full question context if needed.",
    "answerCount": 1,
    "upvoteCount": 47,
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Full expert answer. Can be longer than FAQPage answers. Still aim for direct opening sentence.",
      "upvoteCount": 38,
      "author": {
        "@type": "Person",
        "name": "Expert Name"
      }
    }
  }
}
```

---

## Schema Placement and Implementation

### Where to Place Schema

Always place JSON-LD schema inside `<script type="application/ld+json">` tags in the page `<head>` section.

```html
<head>
  <!-- Other head elements -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    ...
  }
  </script>
</head>
```

### Combining Multiple Schema Types

You can include multiple schema blocks on one page:

```html
<script type="application/ld+json">
{"@type": "Article", ...}
</script>

<script type="application/ld+json">
{"@type": "FAQPage", ...}
</script>

<script type="application/ld+json">
{"@type": "BreadcrumbList", ...}
</script>
```

Or combine into one block using @graph:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {"@type": "Article", ...},
    {"@type": "FAQPage", ...},
    {"@type": "BreadcrumbList", ...}
  ]
}
```

### Schema Validation

Before publishing, validate schema at:
1. Google Rich Results Test -- search.google.com/test/rich-results
2. Schema Markup Validator -- validator.schema.org
3. Bing Webmaster Tools -- Markup Validator section

Common errors to check:
- Missing required fields (causes no rich result)
- Answer text containing HTML tags
- Question text not matching visible content
- Invalid date formats
- Missing @context field
