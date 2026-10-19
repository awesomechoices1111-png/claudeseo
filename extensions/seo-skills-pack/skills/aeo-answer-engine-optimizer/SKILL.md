---
name: aeo-answer-engine-optimizer
description: Answer Engine Optimization (AEO) skill for capturing featured snippets, voice search results, People Also Ask boxes, zero-click answers, and position zero on Google and Bing. Use when user asks to "optimize for voice search", "get featured snippets", "win PAA boxes", "target position zero", "AEO strategy", "optimize for Alexa/Siri/Google Assistant", "zero-click optimization", "answer box optimization", "rank in People Also Ask", or wants their content to appear as the direct answer to queries. Also trigger when user wants to format content for question-answer optimization, FAQ strategy, or conversational search.
---

# AEO Answer Engine Optimizer

Answer Engine Optimization (AEO) is the practice of structuring content to capture direct answer placements in search: featured snippets (position zero), People Also Ask (PAA) boxes, voice search results, and knowledge panel answers. Unlike ranking for clicks, AEO targets zero-click visibility where your content becomes the answer.

## AEO vs SEO vs GEO: Quick Distinction

| Focus | Optimizes For | Primary Output |
|---|---|---|
| SEO | Traditional ranking | Blue link clicks |
| AEO | Featured snippets, PAA, voice | Zero-click answers |
| GEO | AI engine citations | AI-generated summaries |

AEO and GEO overlap heavily. Content optimized for AEO (direct answers, structured Q&A) is also well-positioned for GEO.

## Step 1: Query Type Classification

AEO strategy depends entirely on query type. Classify each target query before optimizing:

**Question Queries** (What, Why, Who, When, Where, How)
- "What is [topic]?" -- Definition snippet
- "How does [process] work?" -- Process/list snippet
- "Why does [phenomenon] happen?" -- Explanation snippet

**Comparison Queries** (vs, difference, compared to)
- "[X] vs [Y]" -- Table snippet
- "Difference between [X] and [Y]" -- List snippet

**Process Queries** (How to, Steps to, Guide to)
- "How to [task]" -- Numbered list snippet
- "Steps to [outcome]" -- Numbered list snippet

**Definition Queries** (What is, Define, Meaning of)
- "What is [term]?" -- Paragraph snippet (40-60 words)

**Value Queries** (Best, Top, Cheapest, Fastest)
- "Best [category]" -- Bulleted list snippet
- "Top [N] [category]" -- Numbered list snippet

**Voice Search Queries** (conversational, long-tail, spoken)
- "What's a good [product] for [use case]?"
- "How do I [task] without [constraint]?"
- Voice answers are typically under 45 words drawn from featured snippets

**Action:** For each target keyword, identify the query type and the corresponding snippet format to target.

## Step 2: Featured Snippet Optimization

### Paragraph Snippets (Definition / Explanation)

Target query pattern: "What is X?", "What does X mean?", "Why is X important?"

**Optimal structure:**
```
[Keyword] is [concise definition in 40-60 words]. [Key attribute 1]. [Key attribute 2]. 
[One differentiating fact or context sentence].
```

Rules:
- Place the answer paragraph immediately after the matching H2 or H3 heading
- Heading should mirror the target query ("What Is [Keyword]?")
- Answer paragraph: 40-60 words, no links, no lists
- Follow the answer paragraph with elaboration for depth

### List Snippets (Process / Steps)

Target query pattern: "How to X", "Steps to X", "How does X work?"

**Optimal structure:**
```
## How to [Task]

Brief intro sentence (1 sentence max).

1. [Step name]: [One-sentence description]
2. [Step name]: [One-sentence description]
3. [Step name]: [One-sentence description]
...
```

Rules:
- Use numbered lists for sequential processes
- Use bulleted lists for non-sequential sets of items
- Each list item: concise, under 20 words
- Include 5-9 items (Google rarely shows more than 8 in snippets)
- Add HowTo schema for how-to content (see `references/aeo-schema-guide.md`)

### Table Snippets (Comparison)

Target query pattern: "[X] vs [Y]", "Difference between X and Y"

**Optimal structure:**

```markdown
## [X] vs [Y]: Key Differences

| Feature | [X] | [Y] |
|---|---|---|
| [Attribute 1] | [Value] | [Value] |
| [Attribute 2] | [Value] | [Value] |
| [Attribute 3] | [Value] | [Value] |
```

Rules:
- 3-5 rows (Google truncates longer tables in snippets)
- First column = comparison attribute
- Keep cell values short (under 10 words each)
- Use plain text in cells -- no links, no formatting

## Step 3: People Also Ask (PAA) Optimization

PAA boxes appear for most informational queries and are a major AEO opportunity. Each PAA question is its own featured snippet.

**How to target PAA:**

1. **Find PAA questions for your topic** -- Google your primary keyword and note every PAA question that appears. Expand them to reveal nested questions.

2. **Build a Q&A content section** -- Create a dedicated FAQ or Q&A section on the page targeting 5-10 PAA questions from your topic.

3. **Format each answer correctly:**
   - Question as an H3 heading (exact phrasing preferred)
   - Followed immediately by a 40-60 word direct answer
   - Followed by 200-400 words of supporting detail

4. **Add FAQPage schema** -- Schema-marked FAQ content has higher snippet selection rates.

Read `references/paa-research-guide.md` for PAA discovery methods and tracking tools.

## Step 4: Voice Search Optimization

Voice answers (Google Assistant, Siri, Alexa, Bing Copilot) are almost always read from featured snippets. Optimize for voice by:

**Answer format requirements:**
- 29-45 words (average voice answer length)
- Written in full sentences, not fragments
- No bullet points (incompatible with text-to-speech)
- No tables or special characters
- Conversational tone, not academic

**Trigger phrase optimization:**
Voice queries are conversational and long-tail. Target:
- "How do I..." not just "how to..."
- "What's the best..." not just "best..."
- "Can I..." and "Should I..." patterns
- Near me / local queries if applicable

**Content adaptations for voice:**
- Add conversational question variants as subheadings
- Use contractions naturally ("it's", "you'll", "we're")
- Answer in second person ("You can..." not "Users can...")
- Start answers with the keyword ("Machine learning is..." not "It is a type of...")

## Step 5: Zero-Click Content Architecture

Some queries should be optimized for visibility even if they generate no clicks. This builds brand authority in AI ecosystems.

**When to pursue zero-click:**
- Brand/entity definition queries ("What is [Your Brand]?")
- Category definition queries where you're the authority
- High-volume informational queries in your topical cluster
- Voice search queries in your niche

**Zero-click page structure:**
```
[Target Query as H1 or H2]
[40-60 word direct answer]
[Entity definition paragraph with schema]
[Expanded explanation with depth signals]
[Related questions as H3s with PAA-formatted answers]
[Internal links to deeper content]
```

## Step 6: AEO Content Audit

Run this checklist against any page being AEO-optimized:

**Query Targeting**
- [ ] Primary query type identified (definition, process, comparison, list)
- [ ] Target snippet format selected (paragraph, list, table)
- [ ] 5+ PAA questions identified and incorporated
- [ ] Voice search variants included

**Answer Formatting**
- [ ] Direct answer paragraph (40-60 words) immediately after matching heading
- [ ] Heading phrasing matches target query
- [ ] List items under 20 words each
- [ ] Table cells under 10 words each
- [ ] No links or markdown formatting inside answer blocks

**Schema Implementation**
- [ ] FAQPage schema added for Q&A sections
- [ ] HowTo schema added for step-by-step guides
- [ ] Speakable schema added for voice targets (optional, advanced)

**Freshness and Authority**
- [ ] Publication date visible on page
- [ ] Last updated date visible
- [ ] Author with credentials identified

## Step 7: AEO Output Deliverables

**Snippet Targeting Plan:** Query list with snippet type classification and content format recommendation for each

**Rewritten Answer Blocks:** Direct answer paragraphs (40-60 words) for each target query, ready to paste into page

**PAA Content Section:** 5-10 Q&A pairs formatted for PAA capture with FAQPage schema code

**Voice Optimized Answers:** 29-45 word voice-format answers for top 5 queries

**AEO Audit Scorecard:** Checklist result with score (0-100) and prioritized action list

---

For PAA research methods and tracking tools, read `references/paa-research-guide.md`
For AEO schema markup templates, read `references/aeo-schema-guide.md`
For AEO measurement and reporting, read `references/aeo-measurement.md`
