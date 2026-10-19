---
name: dataforseo
description: >
  Live SEO data via the DataForSEO MCP server: SERP analysis, keyword research
  (volume, difficulty, intent, trends), backlink profiles, on-page analysis,
  competitor and content analysis, business listings, AI visibility (LLM
  mention tracking), and domain analytics. Requires the DataForSEO MCP server
  to be connected. Use when the user says "dataforseo", "live SERP", "keyword
  volume", "backlink data", "AI visibility check", or "real search data".
---

# DataForSEO: Live SEO Data

Live search data via the DataForSEO MCP server. Provides real-time SERP results
(organic and images), keyword metrics, backlink profiles, on-page analysis, content
analysis, business listings, AI visibility checking, and LLM mention tracking
across 9 API modules with 79+ MCP tools.

## Prerequisites

This skill requires the DataForSEO MCP server to be connected.

**Check availability:** Before using any DataForSEO tool, verify the MCP server
is connected by checking if `serp_organic_live_advanced` or any DataForSEO tool
is available. If tools are not available, inform the user the DataForSEO MCP
server is not connected and that it needs to be set up before this skill can run.

## API Credit Awareness

DataForSEO charges per API call. Be efficient:
- Prefer bulk endpoints over multiple single calls
- Use default parameters (US, English) unless the user specifies otherwise
- Cache results mentally within a session; do not re-fetch the same data
- Warn the user before running expensive operations (full backlink crawls, large keyword lists)

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo dataforseo serp <keyword>` | Google organic SERP results |
| `/seo dataforseo serp-images <keyword>` | Google Images SERP results |
| `/seo dataforseo serp-youtube <keyword>` | YouTube search results |
| `/seo dataforseo youtube <video_id>` | YouTube video deep analysis |
| `/seo dataforseo keywords <seed>` | Keyword ideas and suggestions |
| `/seo dataforseo volume <keywords>` | Search volume for keywords |
| `/seo dataforseo difficulty <keywords>` | Keyword difficulty scores |
| `/seo dataforseo intent <keywords>` | Search intent classification |
| `/seo dataforseo trends <keyword>` | Google Trends data |
| `/seo dataforseo backlinks <domain>` | Full backlink profile |
| `/seo dataforseo competitors <domain>` | Competitor domain analysis |
| `/seo dataforseo ranked <domain>` | Ranked keywords for domain |
| `/seo dataforseo intersection <domains>` | Keyword/backlink overlap |
| `/seo dataforseo traffic <domains>` | Bulk traffic estimation |
| `/seo dataforseo subdomains <domain>` | Subdomains with ranking data |
| `/seo dataforseo top-searches <domain>` | Top queries mentioning domain |
| `/seo dataforseo onpage <url>` | On-page analysis (Lighthouse + parsing) |
| `/seo dataforseo tech <domain>` | Technology stack detection |
| `/seo dataforseo whois <domain>` | WHOIS registration data |
| `/seo dataforseo content <keyword/url>` | Content analysis and trends |
| `/seo dataforseo listings <keyword>` | Business listings search |
| `/seo dataforseo ai-scrape <query>` | ChatGPT web scraper for GEO |
| `/seo dataforseo ai-mentions <keyword>` | LLM mention tracking for GEO |

---

## SERP Analysis

### `/seo dataforseo serp <keyword>`

Fetch live Google organic search results.

**MCP tools:** `serp_organic_live_advanced`

**Default parameters:** location_code=2840 (US), language_code=en, device=desktop, depth=100

**Also supports:** The `serp_organic_live_advanced` tool supports Google, Bing, and Yahoo via the `se` parameter. Specify "bing" or "yahoo" to switch search engines.

**Output:** Rank, URL, title, description, domain, featured snippets, AI overview references, People Also Ask.

### `/seo dataforseo serp-youtube <keyword>`

Fetch YouTube search results. Valuable for GEO. YouTube mentions correlate most strongly with AI citations.

**MCP tools:** `serp_youtube_organic_live_advanced`

**Output:** Video title, channel, views, upload date, description, URL.

### `/seo dataforseo youtube <video_id>`

Deep analysis of a specific YouTube video: info, comments, and subtitles. Some third-party studies report a 0.737 correlation between YouTube mentions and AI visibility, so treat this as a methodology-dependent GEO signal.

**MCP tools:** `serp_youtube_video_info_live_advanced`, `serp_youtube_video_comments_live_advanced`, `serp_youtube_video_subtitles_live_advanced`

**Parameters:** video_id (the YouTube video ID, e.g., "dQw4w9WgXcQ")

**Output:** Video metadata (title, channel, views, likes, description), top comments with engagement, subtitle/transcript text.

### `/seo dataforseo serp-images <keyword>`

Fetch live Google Images search results. See which images rank for a keyword,
which domains dominate image results, and identify visual content opportunities.

**MCP tools:** `serp_google_images_live_advanced`

**Default parameters:** location_code=2840 (US), language_code=en, device=desktop, depth=100

**Parameters:** keyword (required), depth (optional, max 700, billed per 100-result increment), search_param (optional, e.g. "site:example.com")

**Cost warning:** Using `site:` or `filetype:` operators incurs **5x API cost**. Warn the user before running filtered queries.

**Output:** Position, title, alt text, source page URL, direct image URL, domain, encoded URL.

**Analysis to provide:**
- Domain dominance: which sites own the most image positions (top 10 domains by count)
- Alt text patterns: common title/alt text patterns in top-ranking images
- Format distribution: WebP vs JPEG vs PNG in top results (infer from image_url extension)
- Opportunity identification: keywords where the user has organic rankings but no image presence

---

## Keyword Research

### `/seo dataforseo keywords <seed>`

Generate keyword ideas, suggestions, and related terms from a seed keyword.

**MCP tools:** `dataforseo_labs_google_keyword_ideas`, `dataforseo_labs_google_keyword_suggestions`, `dataforseo_labs_google_related_keywords`

**Default parameters:** location_code=2840 (US), language_code=en, limit=50

**Output:** Keyword, search volume, CPC, competition level, keyword difficulty, trend.

### `/seo dataforseo volume <keywords>`

Get search volume and metrics for a list of keywords.

**MCP tools:** `kw_data_google_ads_search_volume`

**Parameters:** keywords (array, comma-separated), location_code, language_code

**Output:** Keyword, monthly search volume, CPC, competition, monthly trend data.

### `/seo dataforseo difficulty <keywords>`

Calculate keyword difficulty scores for ranking competitiveness.

**MCP tools:** `dataforseo_labs_bulk_keyword_difficulty`

**Parameters:** keywords (array), location_code, language_code

**Output:** Keyword, difficulty score (0-100), interpretation (Easy/Medium/Hard/Very Hard).

### `/seo dataforseo intent <keywords>`

Classify keywords by user search intent.

**MCP tools:** `dataforseo_labs_search_intent`

**Parameters:** keywords (array), location_code, language_code

**Output:** Keyword, intent type (informational, navigational, commercial, transactional), confidence score.

### `/seo dataforseo trends <keyword>`

Analyze keyword trends over time using Google Trends data.

**MCP tools:** `kw_data_google_trends_explore`

**Parameters:** keywords (array), location_code, date_from, date_to, language_code

**Output:** Keyword, time series data, trend direction, seasonality signals.

---

## Domain and Competitor Analysis

### `/seo dataforseo backlinks <domain>`

Comprehensive backlink profile analysis.

**MCP tools:** `backlinks_summary`, `backlinks_backlinks`, `backlinks_anchors`, `backlinks_referring_domains`, `backlinks_bulk_spam_score`, `backlinks_timeseries_summary`

**Default parameters:** limit=100 per sub-call

**Output:** Total backlinks, referring domains, domain rank, spam score, top anchors, new/lost backlinks over time, dofollow ratio, top referring domains.

### `/seo dataforseo competitors <domain>`

Identify competing domains and estimate traffic.

**MCP tools:** `dataforseo_labs_google_competitors_domain`, `dataforseo_labs_google_domain_rank_overview`, `dataforseo_labs_bulk_traffic_estimation`

**Output:** Competitor domains, keyword overlap %, estimated traffic, domain rank, common keywords.

### `/seo dataforseo ranked <domain>`

List keywords a domain ranks for with positions and page data.

**MCP tools:** `dataforseo_labs_google_ranked_keywords`, `dataforseo_labs_google_relevant_pages`

**Default parameters:** limit=100, location_code=2840

**Output:** Keyword, position, URL, search volume, traffic share, SERP features.

### `/seo dataforseo intersection <domain1> <domain2> [...]`

Find shared keywords and backlink sources across 2-20 domains.

**MCP tools:** `dataforseo_labs_google_domain_intersection`, `backlinks_domain_intersection`

**Parameters:** domains (2-20 array)

**Output:** Shared keywords with positions per domain, shared backlink sources, unique keywords per domain.

### `/seo dataforseo traffic <domains>`

Estimate organic search traffic for one or more domains.

**MCP tools:** `dataforseo_labs_bulk_traffic_estimation`

**Parameters:** domains (array)

**Output:** Domain, estimated organic traffic, estimated traffic cost, top keywords.

### `/seo dataforseo subdomains <domain>`

Enumerate subdomains with their ranking data and traffic estimates.

**MCP tools:** `dataforseo_labs_google_subdomains`

**Parameters:** target (domain), location_code, language_code

**Output:** Subdomain, ranked keywords count, estimated traffic, organic cost.

### `/seo dataforseo top-searches <domain>`

Find the most popular search queries that mention a specific domain in results.

**MCP tools:** `dataforseo_labs_google_top_searches`

**Parameters:** target (domain), location_code, language_code

**Output:** Query, search volume, domain position, SERP features, traffic share.

---

## Technical and On-Page

### `/seo dataforseo onpage <url>`

Run on-page analysis including a Lighthouse audit and content parsing.

**MCP tools:** `on_page_instant_pages`, `on_page_content_parsing`, `on_page_lighthouse`

**Usage:**
- `on_page_instant_pages`: Quick page analysis (status codes, meta tags, content size, page timing, broken links, on-page checks)
- `on_page_content_parsing`: Extract and parse page content (plain text, word count, structure)
- `on_page_lighthouse`: Full Lighthouse audit (performance score, accessibility, best practices, SEO, Core Web Vitals)

**Output:** Pages crawled, status codes, meta tags, titles, content size, load times, Lighthouse scores, broken links, resource analysis.

### `/seo dataforseo tech <domain>`

Detect technologies used on a domain.

**MCP tools:** `domain_analytics_technologies_domain_technologies`

**Output:** Technology name, version, category (CMS, analytics, CDN, framework, etc.).

### `/seo dataforseo whois <domain>`

Retrieve WHOIS registration data.

**MCP tools:** `domain_analytics_whois_overview`

**Output:** Registrar, creation date, expiration date, nameservers, registrant info (if public).

---

## Content and Business Data

### `/seo dataforseo content <keyword/url>`

Analyze content quality, search for content by topic, and track phrase trends.

**MCP tools:** `content_analysis_search`, `content_analysis_summary`, `content_analysis_phrase_trends`

**Parameters:** keyword (for search/trends) or URL (for summary)

**Output:** Content matches with quality scores, sentiment analysis, readability metrics, phrase trend data over time.

### `/seo dataforseo listings <keyword>`

Search business listings for local SEO competitive analysis.

**MCP tools:** `business_data_business_listings_search`

**Parameters:** keyword, location (optional)

**Output:** Business name, description, category, address, phone, domain, rating, review count, claimed status.

---

## AI Visibility / GEO

### `/seo dataforseo ai-scrape <query>`

Scrape what ChatGPT web search returns for a query. ChatGPT visibility check: see which sources ChatGPT cites for your target keywords. Check Google AI Overviews and AI Mode with Search Console gen-AI reports when available.

**MCP tools:** `ai_optimization_chat_gpt_scraper`

**Parameters:** query, location_code (optional), language_code (optional). Use `ai_optimization_chat_gpt_scraper_locations` to look up available locations.

**Output:** ChatGPT response content, cited sources/URLs, referenced domains.

### `/seo dataforseo ai-mentions <keyword>`

Track how LLMs mention brands, domains, and topics. Critical for GEO. Measures actual AI visibility across multiple LLM platforms.

**MCP tools:** `ai_opt_llm_ment_search`, `ai_opt_llm_ment_top_domains`, `ai_opt_llm_ment_top_pages`, `ai_opt_llm_ment_agg_metrics`

**Parameters:** keyword, location_code (optional), language_code (optional). Use `ai_opt_llm_ment_loc_and_lang` for available locations/languages and `ai_optimization_llm_models` for supported LLM models.

**Workflow:**
1. Search LLM mentions with `ai_opt_llm_ment_search` (find mentions of a brand/keyword across LLM responses)
2. Get top cited domains with `ai_opt_llm_ment_top_domains` (which domains are most cited for this topic)
3. Get top cited pages with `ai_opt_llm_ment_top_pages` (which specific pages are most cited)
4. Get aggregate metrics with `ai_opt_llm_ment_agg_metrics` (overall mention volume, trends)

**Output:** LLM mention count, top cited domains with frequency, top cited pages, mention trends over time, cross-platform visibility scores.

**Advanced:** Use `ai_opt_llm_ment_cross_agg_metrics` for cross-model comparison (how mentions differ across ChatGPT, Claude, Perplexity, etc.).

---

## Available Utility Tools

DataForSEO's MCP server exposes additional utility tools beyond the ones listed above (location lookups, bulk operations, historical data, filter options). These do not have dedicated commands here — when a task needs one, check the MCP server's tool list directly for the closest match.

## Error Handling

- **MCP server not connected**: Report that the DataForSEO MCP server is not connected and that it needs to be set up before this skill can run.
- **API authentication failed**: Report invalid credentials. Suggest checking the DataForSEO API login/password in the MCP configuration.
- **Rate limit exceeded**: Report the limit hit and suggest waiting before retrying.
- **No results returned**: Report "no data found" for the query rather than guessing. Suggest broadening the query or checking location/language codes.
- **Invalid location code**: Report the error and suggest using the locations lookup tool to find the correct code.

## Output Formatting

- Use tables for comparative data
- Prioritize issues as Critical > High > Medium > Low
- Include specific, actionable recommendations
- Show scores as XX/100 where applicable
- Note data source as "DataForSEO (live)" to distinguish from static analysis
