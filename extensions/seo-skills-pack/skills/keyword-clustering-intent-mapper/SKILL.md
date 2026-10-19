---
name: keyword-clustering-intent-mapper
description: "Groups keywords into topic clusters and maps each cluster to a search intent type (informational, navigational, commercial, transactional). Produces a keyword architecture ready for content planning. Use when user says keyword clustering, group keywords, keyword mapping, intent mapping, keyword intent, keyword architecture, organize keywords, keyword strategy, map keywords to pages, TOFU/MOFU/BOFU keywords, funnel stage mapping, keyword grouping, cluster keywords by topic, or provides a list of keywords and wants them organized."
version: 0.1.0
---

# Keyword Clustering & Intent Mapper

Transforms a flat keyword list into a structured topic architecture. Groups semantically related keywords into clusters, assigns search intent to each cluster, maps clusters to funnel stages, and recommends the content format best suited to each group.

## What to Collect Before Starting

- **Keyword list** — paste keywords (one per line, or with volume/CPC data)
- **Domain or niche** — for context-aware grouping
- **Business type** — B2B/B2C, e-commerce, SaaS, local service, publisher
- **Content goals** — driving leads, affiliate traffic, brand awareness, e-commerce sales

Minimum: a list of keywords. More context improves cluster quality.

---

## Step 1: Semantic Clustering

Group keywords into clusters based on:
- **Shared parent topic** — all keywords about the same subject
- **Shared SERP similarity** — keywords that return similar search results (proxy for same intent)
- **Shared entity** — all variations of the same product, brand, or concept

**Clustering method:**
1. Identify the head term that best describes each group
2. Group all variations, modifiers, and related terms under that head term
3. Separate clusters where SERP results differ significantly (different intent = different page)

## Step 2: Intent Classification

Assign a primary intent type to each cluster:

| Intent | Signal Words | Best Content Format |
|--------|-------------|-------------------|
| **Informational** | what, how, why, guide, tutorial, explained | Blog post, pillar page, FAQ |
| **Navigational** | brand name + feature/page | Homepage, feature page, login page |
| **Commercial** | best, top, vs, review, alternative, comparison | Comparison page, roundup, review |
| **Transactional** | buy, price, cost, discount, hire, get, download | Product/service page, pricing page, landing page |

Each cluster gets one primary intent (and optionally a secondary intent).

## Step 3: Funnel Stage Mapping

Map clusters to funnel stages:

| Funnel Stage | Intent Match | Goal |
|-------------|-------------|------|
| **TOFU** (Top of Funnel) | Informational | Awareness, traffic |
| **MOFU** (Middle of Funnel) | Commercial | Consideration, lead gen |
| **BOFU** (Bottom of Funnel) | Transactional | Conversion, revenue |

## Step 4: Page Assignment

For each cluster, recommend:
- **New page needed** — no existing page matches this cluster's intent
- **Existing page to optimize** — a current page that should be updated to target this cluster
- **Consolidation candidate** — multiple existing pages that should be merged

## Step 5: Priority Scoring

Score each cluster by:
- **Volume** — total estimated monthly search volume
- **Competition** — estimated keyword difficulty (low/medium/high)
- **Business value** — alignment with conversion goals (high/medium/low)
- **Priority** = Volume × Business value / Competition

## Step 6: Keyword Cluster Output Table

| Cluster Name | Head Term | Keywords (sample) | Intent | Funnel Stage | Volume Est. | Difficulty | Business Value | Priority |
|-------------|-----------|-------------------|--------|--------------|-------------|------------|----------------|----------|
| Example | keyword X | kw1, kw2, kw3 | Info | TOFU | 5,400 | Medium | Low | Medium |

## Output Format

Deliver:
1. **Cluster map** — full table with all clusters, intent, funnel stage, and priority
2. **Quick-start clusters** — top 5 clusters to target first (high volume + low difficulty + high value)
3. **Content calendar seed** — suggested content pieces mapped to top clusters
4. **Page assignment plan** — which clusters need new pages vs. optimized existing ones
5. **Long-tail expansion** — 3-5 long-tail keywords per top cluster for quick wins
