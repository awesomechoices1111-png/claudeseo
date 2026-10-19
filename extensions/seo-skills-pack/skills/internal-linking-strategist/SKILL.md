---
name: internal-linking-strategist
description: "Plans and optimizes internal link architecture to distribute PageRank, improve crawlability, and strengthen topical authority. Use when user says internal linking, internal links, link structure, silo structure, link equity, PageRank distribution, orphan pages, pillar and cluster links, internal link audit, improve crawl depth, link from blog to product, anchor text strategy, hub and spoke content, or wants to improve how pages on their site link to each other."
version: 0.1.0
---

# Internal Linking Strategist

Designs and optimizes the internal link architecture of a website to maximize PageRank flow, reinforce topical clusters, surface orphan pages, and guide both users and crawlers through the most important content.

## What to Collect Before Starting

- **Domain or site URL**
- **List of key pages** (or sitemap) — paste URLs or describe page types
- **Business priorities** — which pages should rank / receive most link equity?
- **Existing structure** — flat site, blog + product pages, e-commerce, SaaS, etc.
- **Content clusters** — any existing topic groupings or pillar pages

Proceed with whatever is provided and make reasonable assumptions for the rest.

---

## Step 1: Site Architecture Assessment

Classify the site structure:

| Type | Description | Internal Linking Priority |
|------|-------------|--------------------------|
| Pillar/Cluster | Central pillar pages with supporting cluster posts | Pillar pages → cluster, cluster → pillar |
| E-commerce | Category → subcategory → product | Category consolidation, product cross-links |
| SaaS | Features, use cases, integrations | Hub pages linking to feature/use-case pages |
| Flat blog | Many standalone posts | Topic-based grouping needed |
| Local/Multi-location | Location pages | Location hub → individual location pages |

## Step 2: Link Equity Flow Mapping

Identify the priority page hierarchy:

**Tier 1 — Money pages** (target maximum inbound internal links)
- High-value product/service/conversion pages
- Category pages
- Pillar content

**Tier 2 — Supporting pages** (link to Tier 1, receive links from Tier 3)
- Topic-specific blog posts
- Comparison pages
- Use case pages

**Tier 3 — Supporting content** (link to Tier 2, minimal Tier 1 links needed)
- FAQ posts
- Glossary entries
- News/update posts

## Step 3: Anchor Text Strategy

Define anchor text guidelines:

- **Exact match**: Use sparingly (1-2 instances max per keyword across the site)
- **Partial match**: Primary keyword variation — preferred for most links
- **Branded**: Use for homepage and brand-specific pages
- **Generic ("click here", "learn more")**: Avoid — no SEO value
- **Descriptive**: "our guide to X" or "X explained" — best for natural linking

Anchor text should describe the destination page's primary keyword.

## Step 4: Orphan Page Detection

Flag pages with zero or very few inbound internal links:
- List all pages that appear to have no links pointing to them from other site pages
- Categorize: intentional orphans (thank-you pages, private) vs accidental
- Recommend which content pages to link to each orphan from

## Step 5: Cluster Link Map

Create a link map per topic cluster:

**Example cluster: "SEO"**
- Pillar: /seo-guide/ ← receives links from all cluster posts
- Cluster posts: /keyword-research/, /on-page-seo/, /link-building/
  - Each links to pillar with anchor: "complete SEO guide"
  - Each links to 2-3 other cluster posts with descriptive anchors
  - Pillar links to all cluster posts

## Step 6: Internal Link Recommendations Table

| Source Page | Destination Page | Recommended Anchor Text | Priority |
|-------------|-----------------|------------------------|----------|
| /blog/post-a | /service/service-x | "service x for [use case]" | High |
| /blog/post-b | /pillar-page | "complete guide to X" | High |

## Step 7: Technical Internal Link Checks

- Maximum clicks from homepage to any important page: target ≤ 3
- Redirect chains in internal links: fix to point to final destination
- Broken internal links: identify and update
- Nofollow on internal links: remove unless intentional (UGC, login pages)
- JavaScript-only links: ensure they are crawlable HTML links

## Output Format

Deliver:
1. **Architecture assessment** — site type and current state
2. **Priority page hierarchy** — Tier 1/2/3 classification
3. **Link map** — cluster-by-cluster linking recommendations
4. **Orphan page list** — with suggested source pages for each
5. **Anchor text guide** — dos and don'ts for the specific site
6. **Quick wins** — top 10 internal links to add immediately
