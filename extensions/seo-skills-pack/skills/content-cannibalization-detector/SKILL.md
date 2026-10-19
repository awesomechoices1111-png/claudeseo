---
name: content-cannibalization-detector
description: "Identifies keyword cannibalization and content overlap issues across a website's pages. Detects when multiple pages compete for the same keywords, diluting rankings and confusing search engines. Use when user says content cannibalization, keyword cannibalization, pages competing for same keyword, duplicate content issues, consolidate pages, which page should rank, cannibalization audit, overlapping content, content consolidation, pages splitting rankings, or wants to find URLs that compete with each other for the same search terms."
version: 0.1.0
---

# Content Cannibalization Detector

Identifies pages on a domain that compete for the same keywords, causing split rankings, authority dilution, and indexing confusion. Provides consolidation recommendations, canonical guidance, and redirect strategies.

## What to Collect Before Starting

**Option A — Full audit:**
- List of URLs from the site (paste sitemap or URL list)
- Target keywords per URL (if known)

**Option B — Keyword-specific check:**
- Specific keyword to investigate
- Domain name

**Option C — Content paste:**
- Paste content from 2+ pages suspected to cannibalize

Proceed with whichever input is provided.

---

## Step 1: Cannibalization Signal Detection

For each page/keyword group, identify cannibalization signals:

**Hard cannibalization (high impact):**
- Two or more pages targeting identical primary keyword
- Same title tag structure across multiple pages
- Near-identical H1 headings on different URLs

**Soft cannibalization (medium impact):**
- Overlapping secondary keywords across 3+ pages
- Similar content intent served by multiple pages
- Product/category page targeting same keyword as a blog post

**Indexing conflicts:**
- Both pages indexed and ranking for same query
- Fluctuating rankings switching between two URLs
- One page ranking lower than expected despite higher authority

## Step 2: Page-by-Page Overlap Matrix

Create a matrix showing keyword overlap between pages:

| URL | Primary Keyword | Overlapping with | Overlap Score |
|-----|----------------|------------------|---------------|
| /page-a | keyword X | /page-b, /page-c | High |
| /page-b | keyword X | /page-a | High |

Score overlap as: None / Low (under 20%) / Medium (20-50%) / High (over 50%)

## Step 3: Intent Differentiation Analysis

For each cannibalization pair, assess whether the pages serve different intents:
- **Informational vs commercial** — can be kept as separate pages
- **Exact same intent** — consolidation recommended
- **Partial overlap** — consider merging sections or adding canonical

## Step 4: Consolidation Recommendations

For each cannibalized pair, provide one of:

1. **Consolidate** — Merge both pages into one stronger page; 301 redirect the weaker URL
2. **Canonicalize** — Keep both but add rel=canonical pointing to the primary
3. **Differentiate** — Rewrite one page to target a distinct keyword or intent
4. **Noindex** — Keep the weaker page for UX but remove from search index
5. **Keep as-is** — If intent is genuinely different; monitor for ranking swaps

## Step 5: Priority Impact Assessment

Rank cannibalization issues by business impact:

- **Priority 1** — High-traffic keywords with clear cannibalization
- **Priority 2** — Commercial/transactional pages competing against each other
- **Priority 3** — Informational pages with soft overlap

## Output Format

Deliver:
1. **Cannibalization summary** — total issues found by severity
2. **Issue list** — each pair/group with overlap score and recommended action
3. **Consolidation plan** — ordered list of fixes with expected impact
4. **Redirect map** — source URL → destination URL for any recommended 301s
5. **Content rewrite notes** — specific sections to update for differentiation
