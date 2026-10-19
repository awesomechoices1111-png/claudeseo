---
name: maps-seo
description: >
  Maps intelligence for local SEO: geo-grid rank tracking, Google Business
  Profile auditing, review intelligence across Google/Tripadvisor/Trustpilot,
  cross-platform NAP verification, competitor radius mapping, and
  LocalBusiness schema generation. Works free-tier with public APIs, and gets
  richer with a DataForSEO MCP connection (and optionally a Google Maps API
  key). Use when the user says "maps", "geo-grid", "rank tracking", "GBP
  audit", "review velocity", "competitor radius", or "SoLV".
---

# Maps Intelligence (March 2026)

Maps platform analysis for local businesses. Works with external APIs to assess
how a business appears on Google Maps, Bing Places, Apple Maps, and OpenStreetMap.

**Boundary with on-page local SEO skills:** This skill analyzes the business on
maps PLATFORMS (via APIs). If you have a separate local-SEO skill, that one
should handle local signals on the WEBSITE itself (via HTML fetch) — don't
duplicate that on-page analysis here; recommend it for website-level checks.

---

## Quick Reference

| Command | What it does | Tier |
|---------|-------------|------|
| `/seo maps <url>` | Full maps presence audit (auto-selects tier) | 0+ |
| `/seo maps grid <keyword> <location>` | Geo-grid rank scan (7x7, 1 keyword default) | 1+ |
| `/seo maps reviews <business> <location>` | Cross-platform review intelligence | 1+ |
| `/seo maps competitors <keyword> <location>` | Competitor radius mapping | 0+ |
| `/seo maps nap <business-name>` | Cross-platform NAP verification | 0+ |
| `/seo maps schema <business-name>` | Generate LocalBusiness JSON-LD from data | 0+ |
| `/seo maps gbp <business> <location>` | GBP completeness audit | 1+ |

---

## Three-Tier Capability Detection

Before any analysis, detect the available capability tier:

### Tier 0 (Free)
**Detection:** DataForSEO MCP tools NOT available.
**Capabilities:** Overpass API competitor discovery, Geoapify POI search, Nominatim geocoding, static GBP checklist, schema generation, cross-platform NAP guidance.

### Tier 1 (DataForSEO)
**Detection:** `business_data_business_listings_search` MCP tool IS available.
**Capabilities:** Everything in Tier 0 PLUS geo-grid rank tracking, live GBP profile audit, review intelligence (velocity, sentiment, distribution), GBP post activity, Q&A data, Tripadvisor/Trustpilot reviews.

### Tier 2 (DataForSEO + Google Maps Platform)
**Detection:** Tier 1 available AND a Google Maps API key in environment.
**Capabilities:** Everything in Tier 1 PLUS Google Places details, real-time business status, AI-powered place summaries, photo analysis.
**Note:** Google's ToS restricts storage to `place_id` only. Lat/lng should be cached 30 days max.

**Always communicate the detected tier to the user** at the start of analysis.

---

## Geo-Grid Rank Tracking (Tier 1+)

Simulates Google Maps searches from multiple GPS coordinates to show ranking
variation across a geographic area. Requires DataForSEO.

### Workflow

1. Geocode the business address to get its center lat/lng.
2. Generate grid points (default: 7x7, 5km radius) using the Haversine offset
   formula to place each point at an even distance from center.
3. **Display a cost estimate and ask for confirmation before proceeding** —
   each grid point is a separate DataForSEO Maps SERP call, so a 7x7 grid is
   49 calls.
4. Fire DataForSEO Maps SERP API calls with `location_coordinate` per grid point.
5. Find the target business's rank at each point.
6. Calculate Share of Local Voice (SoLV): `(top_3_count / total_points) * 100`
   — the percentage of grid points where the business ranks in the top 3.
7. Render an ASCII heatmap in the output, one cell per grid point, colored/
   labeled by rank tier (e.g. top 3, 4-10, not found).

### Cost Warning (REQUIRED)

Before every geo-grid scan, display:
```
Geo-Grid Scan: [keyword] at [location]
Grid: 7x7 (49 points) | Keywords: [N] | Est. cost: $[amount]
DataForSEO credits will be consumed. Proceed?
```

---

## GBP Profile Audit (Tier 1 preferred, Tier 0 manual)

Audits the fields that affect Google Business Profile quality and ranking:
category selection and count, business description, hours (including special
hours), attributes, products/services listings, Q&A activity, photo count and
recency, post activity/cadence, messaging/booking setup, and review response
rate. Weight these by industry — for example, booking/appointment attributes
matter more for service businesses than for retail.

> **AI & 2026 context (third-party reported):** **Ask Maps**, reported by AP News
> as a Gemini conversational Maps feature launched 2026-03-12 (iOS/Android,
> US + India). **AI Mode** (1B+ MAU, reported from Google I/O 2026 keynote coverage; not confirmed on a Google-owned source)
> increasingly surfaces business info through conversational local AI interfaces in third-party terminology, and **agentic
> booking/calling** for local services (home repair, beauty, pet care) rolls out
> to all US users summer 2026 (Google can call businesses on the user's behalf).
> New 2026 GBP API additions: review media URLs, recurring local-post scheduling,
> review reply-state/moderation, and invitation Place ID. Source:
> blog.google/products-and-platforms/products/search/search-io-2026/ ·
> developers.google.com/my-business/content/latest-updates

### Tier 1 Workflow

1. Fetch the business profile via the DataForSEO My Business Info API (keyword or CID).
2. Map the API response fields to the checklist above.
3. Score each field: Present + Optimized = 2pts, Present = 1pt, Missing = 0pts.
4. Apply industry-specific weight multipliers.
5. Normalize to a 0-100 scale.

### Tier 0 Workflow

1. Fetch the business website.
2. Extract any visible GBP signals (Maps embed, place references, review widgets).
3. Apply the static checklist based on detectable signals.
4. Mark undetectable fields as "Unknown (requires DataForSEO for live data)".

---

## Review Intelligence (Tier 1+)

Cross-platform review analysis: velocity, sentiment, rating distribution, fake detection.

### Workflow

1. Fetch Google reviews via the DataForSEO Reviews API (sort by newest).
2. Calculate review velocity: reviews per month over the last 6 months.
3. Check the "18-day rule" (a commonly cited local-SEO heuristic): any 3-week
   gap in new reviews is treated as a ranking risk signal worth flagging.
4. Analyze rating distribution: a healthy distribution is a bell curve skewed
   toward 5-star, not a bimodal 5-star/1-star split.
5. Calculate owner response rate: responses / total reviews.
6. Fetch Tripadvisor and Trustpilot reviews if the business is in a relevant
   category (hospitality, travel, retail with a Trustpilot presence).
7. Build a cross-platform comparison table.

### Fake Review Detection Signals

Flag reviews matching 2+ of these patterns:
- Uniform timing (multiple reviews same day/hour)
- Reviewer accounts with limited history or single review
- Geographic inconsistencies (reviewer location vs business location)
- Exclusively 5-star velocity spike (vs historical baseline)
- Identical or near-identical text across reviews
- Sudden volume spike without corresponding marketing activity

---

## Competitor Radius Mapping (Tier 0+)

Identify and analyze competitors within a defined radius.

### Tier 0 (Overpass API)

1. Geocode the business address.
2. Query the Overpass API for businesses with the same OSM tag within the radius.
3. Parse results: name, address, phone, website, distance from center.
4. Sort by distance, present as a competitor landscape table.

### Tier 1 (DataForSEO)

1. Use the Maps SERP API with the business keyword + location.
2. Extract the top 20 competitors with full profile data.
3. Compare: rating, review count, categories, photos, attributes.
4. Calculate a competitive density score: competitors per km².

---

## Cross-Platform NAP Verification (Tier 0+)

Check business listing consistency across Google, Bing Places, Apple, and OSM.

### Workflow

1. Search for the business name on each platform:
   - Google: infer from GBP data or a Maps SERP result
   - Bing: search Bing Maps for the business name + location
   - Apple: no reliable public API — note this requires manual verification via
     Apple Business Connect
   - OSM: Overpass or Nominatim search
2. Extract NAP (Name, Address, Phone) from each source.
3. Compare for consistency: exact match, partial match, missing, or conflicting.
4. Flag discrepancies as Critical (name mismatch), High (address mismatch), Medium (phone mismatch).
5. Recommend claiming unclaimed profiles.

---

## Schema Generation (Tier 0+)

Generate LocalBusiness JSON-LD markup from collected data.

### Workflow

1. Determine the most specific schema subtype for the industry (e.g.
   `Restaurant`, `Dentist`, `Plumber` rather than the generic `LocalBusiness`).
2. Populate required properties: `@type`, `name`, `address`, `image`.
3. Add recommended properties: `telephone`, `url`, `geo`, `openingHoursSpecification`, `priceRange`.
4. Add strategic properties for multi-location businesses: `branchOf`, `areaServed`, `sameAs`.
5. Add `aggregateRating` if review data is available.
6. Output a valid JSON-LD block ready for implementation.

**Do NOT generate self-serving review markup** -- Google ignores LocalBusiness review markup from the business itself. Only mark up third-party reviews visible on the page.

---

## Output

Generate a maps analysis report with:

1. **Maps Health Score: XX/100** with dimension breakdown table
2. **Capability tier detected** (Tier 0, 1, or 2) with explanation of what's available
3. **Geo-grid heatmap** (Tier 1): ASCII grid with SoLV percentage and average rank
4. **GBP profile audit**: field-by-field scoring with industry-specific weights
5. **Review intelligence**: velocity chart, rating distribution, response rate, cross-platform comparison
6. **Competitor landscape**: count in radius, top 5 by rating/reviews, competitive density
7. **Cross-platform presence**: Google/Bing/Apple/OSM listing status
8. **Schema recommendation**: generated LocalBusiness JSON-LD (if missing or incomplete)
9. **Top 10 prioritized actions** (Critical > High > Medium > Low)
10. **Cost report**: DataForSEO credits consumed during analysis (Tier 1 only)
11. **Limitations disclaimer**: what could not be assessed at the current tier

---

## Cross-Skill Notes

Once this maps-platform audit is done, hand off:
- Website on-page local signals → a local-SEO skill, on the site itself
- Full AI search visibility → a GEO/AI-visibility skill
- Schema validation and fixes → a schema-generation skill
- Live SERP and keyword data → the seo-dataforseo skill

---

## Error Handling

| Scenario | Action |
|----------|--------|
| DataForSEO MCP not available | Drop to Tier 0. Inform user: "DataForSEO not detected. Running free-tier analysis. For geo-grid tracking and review intelligence, connect a DataForSEO MCP server." |
| Business not found in Maps SERP | Try My Business Info with keyword. If still not found, report "Business not found in Google Maps for this location." |
| Geocoding fails (Nominatim) | Ask user to provide coordinates or a more specific address. |
| API rate limit hit | Report the limit. Suggest waiting or using standard (queued) method instead of live. |
| No reviews found | Report zero review state. Recommend review generation strategy with 18-day cadence target. |
| Multi-location detected | Ask user which location to analyze, or offer batch mode with per-location cost estimate. |
