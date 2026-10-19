---
name: technical-seo-auditor
description: "Performs comprehensive technical SEO audits covering crawlability, indexation, site architecture, URL structure, canonicalization, hreflang, redirects, page speed, mobile usability, security, and structured data. Use when user says technical SEO, site audit, technical audit, crawl errors, indexation issues, robots.txt, sitemap issues, canonical issues, hreflang errors, redirect chains, duplicate content, crawl budget, log file analysis, Google Search Console errors, or wants a full technical health check of their website."
version: 0.1.0
---

# Technical SEO Auditor

Conducts a systematic technical SEO audit across all critical areas: crawlability and indexation, on-page signals, site architecture, speed, mobile, security, and structured data. Delivers prioritized findings with specific fix instructions.

## What to Collect Before Starting

- **Domain URL** — the site to audit
- **Google Search Console access** — paste any error summaries if available
- **Crawl data** — paste Screaming Frog or Ahrefs crawl export if available
- **CMS/tech stack** — WordPress, Shopify, custom, headless, etc.
- **Primary goals** — e-commerce, lead gen, publisher, local business

Proceed with whatever is provided. Flag assumptions made when data is unavailable.

---

## Audit Area 1: Crawlability & Robots

Check and document:
- **robots.txt** — is it accessible, blocking important paths?
- **Crawl directives** — any disallow rules that block key sections?
- **Crawl budget signals** — is the site wasting crawl budget on low-value URLs (infinite scroll, faceted navigation, parameters)?
- **JavaScript rendering** — are key pages reliant on client-side JS that Googlebot may not fully render?

Flags: robots.txt blocking key directories, parameter-generated URLs, JS-only content without SSR/prerendering.

## Audit Area 2: Indexation

Assess:
- **Index coverage** — number of indexed pages vs. total pages
- **Noindex tags** — any important pages accidentally noindexed?
- **Canonical tags** — correct self-referencing canonicals, no canonical chains
- **Duplicate content** — www vs non-www, http vs https, trailing slash variants all handled with redirects or canonicals
- **Soft 404s** — pages returning 200 status but showing "page not found" content

Flags: noindex on important pages, missing or incorrect canonicals, excessive near-duplicate URLs.

## Audit Area 3: Site Architecture & URL Structure

Evaluate:
- **URL depth** — key pages reachable within 3 clicks from homepage?
- **URL format** — readable, keyword-containing, lowercase, hyphens (not underscores)
- **Pagination** — rel=next/prev deprecated; recommend individual page indexing or consolidated page
- **Orphan pages** — pages with no inbound internal links
- **Category/tag proliferation** — WordPress tag archives creating thin-content URLs

## Audit Area 4: Redirects

Audit:
- **Redirect chains** — A→B→C should be A→C
- **Redirect loops** — A→B→A
- **Broken redirects** — redirect to a 404
- **301 vs 302** — temporary redirects used where permanent intended
- **HTTPS redirect** — HTTP properly redirecting to HTTPS

## Audit Area 5: On-Page Technical Signals

Check per page:
- **Title tags** — present, unique, under 60 characters, keyword-containing
- **Meta descriptions** — present, unique, under 160 characters
- **H1 tags** — exactly one per page, matches or relates to title
- **Image alt text** — all meaningful images have descriptive alt attributes
- **Hreflang** — if multilingual, correctly implemented and bi-directional

## Audit Area 6: Core Web Vitals & Speed

(For detailed fixes, pass to Core Web Vitals Optimizer skill)
- LCP, INP, CLS status from Search Console
- Mobile vs Desktop score discrepancy
- Render-blocking resources count

## Audit Area 7: Mobile Usability

- Mobile-friendly test status
- Viewport meta tag present
- Font sizes readable on mobile
- Touch targets at least 48×48px
- No horizontal scrolling

## Audit Area 8: Security & HTTPS

- Valid SSL certificate
- All pages served over HTTPS
- Mixed content warnings (HTTP resources on HTTPS pages)
- HSTS header present

## Audit Area 9: Structured Data

- Any schema markup present?
- Errors in Google Rich Results Test?
- Missing schema opportunities (FAQ, Product, Article, etc.)
(Pass to Schema Tag Generator skill for implementation)

## Priority Classification

| Severity | Description | Fix Timeline |
|----------|-------------|-------------|
| Critical | Blocking indexation or causing significant ranking loss | Immediately |
| High | Affecting multiple pages or key pages | Within 2 weeks |
| Medium | Suboptimal but not causing immediate damage | Within 1 month |
| Low | Best practice improvements | Ongoing |

## Output Format

Deliver:
1. **Executive summary** — overall health score and top 5 findings
2. **Issue register** — each issue with severity, affected URLs, and fix instructions
3. **Fix priority order** — what to tackle first for maximum impact
4. **Quick wins** — fixes that take under 1 hour with immediate benefit
5. **Monitoring recommendations** — what to track in Search Console going forward
