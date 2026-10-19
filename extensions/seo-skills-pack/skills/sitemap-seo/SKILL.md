---
name: sitemap-seo
description: >
  Analyze existing XML sitemaps or generate new ones with industry templates.
  Validates format, URLs, and structure. Use when the user says "sitemap",
  "generate sitemap", "sitemap issues", or "XML sitemap".
---

# Sitemap Analysis & Generation

## Mode 1: Analyze Existing Sitemap

Discover candidates before reporting a sitemap missing:

1. Fetch `robots.txt` and read every `Sitemap:` declaration in it.
2. Validate each declared sitemap by fetching it (through a safe, SSRF-resistant
   fetch — resolve and check the host before requesting, and treat cross-host
   sitemap targets with the same caution as any other cross-host fetch).
3. If a declared sitemap is stale, unreachable, or invalid, don't stop there —
   probe the common fallback paths: `/sitemap.xml`, `/sitemap_index.xml`,
   `/sitemap-index.xml`, `/wp-sitemap.xml`.
4. Only report "no sitemap found" once both the declared entries and the
   common paths have been checked and none resolved. Preserve any declared
   sitemap that failed as a finding (broken reference in robots.txt) rather
   than silently ignoring it.

### Validation Checks
- Valid XML format
- Per-file limit: **≤50,000 URLs AND ≤50MB uncompressed** (whichever is hit first)
- All URLs return HTTP 200
- `<lastmod>` accurate: must be a valid **W3C Datetime** and reflect the **last
  significant content change** (main content, structured data, links, not
  copyright/boilerplate edits). Google only honours `<lastmod>` when consistently
  and verifiably accurate, so warn when values are suspiciously uniform or newer
  than the page's real content.
- No deprecated tags: `<priority>` and `<changefreq>` are ignored by Google
- Sitemap referenced in robots.txt
- Compare crawled pages vs sitemap; flag missing pages

### Quality Signals
- Sitemap index file if >50k URLs
- Split by content type (pages, posts, images, videos)
- No non-canonical URLs in sitemap
- No noindexed URLs in sitemap
- No redirected URLs in sitemap
- HTTPS URLs only (no HTTP)

### Common Issues
| Issue | Severity | Fix |
|-------|----------|-----|
| >50k URLs in single file | Critical | Split with sitemap index |
| >50MB uncompressed single file | Critical | Split with sitemap index |
| Non-200 URLs | High | Remove or fix broken URLs |
| Noindexed URLs included | High | Remove from sitemap |
| Redirected URLs included | Medium | Update to final URLs |
| All identical lastmod | Low | Use actual modification dates |
| Priority/changefreq used | Info | Can remove (ignored by Google) |

### Extension sitemaps (image / video / news)

Google documents three subtypes with their own rules, validate per-subtype:
- **Image** (`http://www.google.com/schemas/sitemap-image/1.1`): only two valid
  tags remain, `<image:image>` and `<image:loc>` (max **1,000** `<image:image>`
  per `<url>`). `<image:caption>`/`<image:geo_location>`/`<image:title>`/
 `<image:license>` were deprecated (2022), flag as info-level removable.
- **Video**: required `<video:video>` with `<video:thumbnail_loc>`,
  `<video:title>`, `<video:description>`, plus `<video:content_loc>` or
  `<video:player_loc>`; mRSS also supported. Flag deprecated/removed tags
  (`<video:category>`, `<video:gallery_loc>`, `<video:price>`, `<video:tvshow>`,
  player autoplay/allow_embed) as info-level removable; recheck Google docs before citing a removal date.
- **News**: max **1,000** `<news:news>` per file (not 50,000); include only
  articles from the **last 2 days**; required `<news:publication>`/`<news:name>`/
  `<news:language>`/`<news:publication_date>`/`<news:title>`; submit/discover through
  Search Console or robots.txt/sitemap index; use Publisher Center only for
  publication management where relevant. When the `news:` namespace is detected, override the generic
  50k check with the 1,000 cap.

## Mode 2: Generate New Sitemap

### Process
1. Ask for business type (or auto-detect from existing site).
2. Plan the site structure interactively with the user — for a given business
   type, sketch the category/page hierarchy the sitemap should represent
   (e.g. an e-commerce site typically needs category, product, and
   informational-page sitemaps; a local-service business typically needs
   service and location pages plus content).
3. Apply quality gates:
   - ⚠️ WARNING at 30+ location pages (require 60%+ unique content)
   - 🛑 HARD STOP at 50+ location pages (require justification)
4. Generate valid XML output.
5. Split at whichever comes first: 50,000 URLs or 50MB uncompressed, with sitemap index.
6. Generate a short structure summary documenting the architecture produced.

### Safe Programmatic Pages (OK at scale)
✅ Integration pages (with real setup docs)
✅ Template/tool pages (with downloadable content)
✅ Glossary pages (200+ word definitions)
✅ Product pages (unique specs, reviews)
✅ User profile pages (user-generated content)

### Penalty Risk (avoid at scale)
❌ Location pages with only city name swapped
❌ "Best [tool] for [industry]" without industry-specific value
❌ "[Competitor] alternative" without real comparison data
❌ AI-generated pages without human review and unique value

## Sitemap Format

### Standard Sitemap
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page</loc>
    <lastmod>2026-02-07</lastmod>
  </url>
</urlset>
```

### Sitemap Index (for >50k URLs)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-pages.xml</loc>
    <lastmod>2026-02-07</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-posts.xml</loc>
    <lastmod>2026-02-07</lastmod>
  </sitemap>
</sitemapindex>
```

## Error Handling

- **URL unreachable**: Report the HTTP status code and suggest checking if the site is live
- **No sitemap found**: Report "not found" only after both robots.txt-declared
  sitemaps and the common fallback paths have been checked and none resolved
- **Invalid XML format**: Report specific parsing errors with line numbers
- **Rate limiting detected**: Back off and report partial results with a note about retry timing

## Output

### For Analysis
- Validation report with findings
- Issues list with severity
- Recommendations

### For Generation
- `sitemap.xml` (or split files with index)
- A short structure summary documenting the site architecture
- URL count and organization summary
