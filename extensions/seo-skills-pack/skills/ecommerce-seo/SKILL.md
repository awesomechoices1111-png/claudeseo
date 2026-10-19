---
name: ecommerce-seo
description: >
  E-commerce SEO analysis and copywriting: Google Shopping visibility, Amazon
  marketplace intelligence, product schema validation, competitor pricing
  analysis, marketplace keyword gaps, plus ready-to-use product page copy
  (title, meta, description, schema, alt text) and category/collection page
  copy (title, meta, H1, intro/bottom copy, faceted navigation guidance,
  keyword-to-category mapping). Combines on-page product SEO with marketplace
  data from the DataForSEO Merchant API when available. Use when the user
  says "ecommerce SEO", "product SEO", "Google Shopping", "marketplace SEO",
  "product schema", "Amazon SEO", "product listings", "shopping ads",
  "merchant SEO", "write SEO copy for this product page", "write SEO copy
  for this category page", or "faceted navigation SEO".
---

# E-commerce SEO Analysis

Comprehensive product page optimization, marketplace intelligence, and
competitive pricing analysis. Works standalone (on-page + schema) and gets
richer with a DataForSEO MCP connection for live Google Shopping and Amazon
data (Merchant API tools such as `merchant_google_products_search` and
`merchant_amazon_products_search`). If DataForSEO tools are not available,
skip the marketplace sections and note the limitation in the output.

## Choosing a Mode

- **Analysis/audit** (Sections 1-6): scoring an existing product page,
  pulling marketplace/pricing intelligence, finding keyword gaps, or
  validating schema. Default when a URL or domain is given for review.
- **Product page copywriting** (Section 7): the request wants new or
  rewritten product page copy - title, meta, description, schema, alt text -
  built for a shopper first, search engines second.
- **Category page copywriting** (Section 8): the request wants copy and
  structure for a category/collection page, including faceted navigation
  guidance and keyword-to-category mapping.

## Commands

| Command | Purpose | DataForSEO? |
|---------|---------|-------------|
| `/seo ecommerce <url>` | Full e-commerce SEO analysis of a product page or store | Optional |
| `/seo ecommerce products <keyword>` | Google Shopping competitive analysis | Required |
| `/seo ecommerce gaps <domain>` | Keyword gap: organic vs Shopping visibility | Required |
| `/seo ecommerce schema <url>` | Product schema validation and enhancement | No |
| `/seo ecommerce write product <product>` | Generate product page copy (Section 7) | No |
| `/seo ecommerce write category <category>` | Generate category page copy (Section 8) | No |

---

## 1. Product Page Analysis (No DataForSEO Needed)

Fetch and parse the product page, then evaluate the product-specific signals below.

### Product SEO Checklist

#### Title Tag
- [ ] Contains primary product keyword
- [ ] Includes brand name
- [ ] Under 60 characters (no truncation in SERPs)
- [ ] Format: `[Product Name] - [Key Feature] | [Brand]`

#### Meta Description
- [ ] Contains product keyword + benefit
- [ ] Includes price or "from $XX" (triggers rich snippet interest)
- [ ] Call-to-action present (Shop now, Buy, Free shipping)
- [ ] Under 155 characters

#### Heading Structure
- [ ] Single H1 matching primary product name
- [ ] H2s for: Features, Specifications, Reviews, Related Products
- [ ] No duplicate H1 tags across product variants

#### Product Images
- [ ] Alt text includes product name + distinguishing feature
- [ ] File names are descriptive (not `IMG_001.jpg`)
- [ ] WebP format served (with JPEG fallback)
- [ ] At least 3 images per product (hero, detail, lifestyle)
- [ ] Image dimensions >= 800px for Google Shopping eligibility
- [ ] Lazy loading on below-fold images only

#### Internal Linking
- [ ] Breadcrumb navigation: Home > Category > Subcategory > Product
- [ ] Related products section (cross-sell / upsell)
- [ ] Link back to category page with keyword-rich anchor
- [ ] Reviews section links to full review page (if separate)

#### Content Quality
- [ ] Unique product description (not manufacturer copy-paste)
- [ ] Word count >= 200 for product description body
- [ ] Specs table present (not just prose)
- [ ] User reviews on-page (UGC signals)

### Scoring

| Category | Weight | Criteria |
|----------|--------|----------|
| Schema completeness | 25% | Required + recommended Product fields |
| Title & meta | 15% | Keyword placement, length, format |
| Image optimization | 20% | Alt text, format, sizing, count |
| Content quality | 20% | Unique description, specs, reviews |
| Internal linking | 10% | Breadcrumbs, related products, categories |
| Technical | 10% | Page speed, mobile rendering, canonical |

---

## 2. Google Shopping Intelligence (DataForSEO Merchant API)

Live competitive analysis from Google Shopping results.

**Cost awareness:** Merchant API calls consume DataForSEO credits. Before
running a search or seller-analysis call, tell the user roughly what it will
cost (or that it will consume credits) and get confirmation before proceeding
if the call is non-trivial (bulk keyword lists, full seller crawls).

### Workflow

1. **Product search** — use the Merchant API's Google product search tool for the target keyword to see who sells what at what price.
2. **Seller analysis** — pull merchant ratings and listing counts to see which sellers dominate the results.
3. **Normalize** — combine the results into the pricing and seller tables below.

### Analysis Outputs

#### Pricing Intelligence
- Price distribution: min, max, median, P25, P75
- Price outliers (> 2 standard deviations from median)
- Price-to-rating correlation
- Currency normalization to USD (or user-specified)

#### Seller Landscape
- Top 10 sellers by listing count
- Merchant rating distribution
- Free shipping prevalence
- New vs established sellers

#### Product Listing Quality
- Title keyword patterns in top listings
- Average rating and review count benchmarks
- Image count per listing
- Availability status distribution

For full Merchant API parameter details (location codes, depth, filters), check the seo-dataforseo skill or the connected DataForSEO MCP tool descriptions directly.

---

## 3. Amazon Marketplace (DataForSEO)

Cross-marketplace intelligence comparing Google Shopping and Amazon.

**Cost awareness:** Amazon marketplace endpoints tend to be pricier than
Google Shopping calls — always confirm with the user before running one.

### Workflow

1. **Amazon product search** — run the Merchant API's Amazon product search for the keyword.
2. **Cross-marketplace comparison** — compare the Amazon results against the Google Shopping results gathered above.

### Cross-Marketplace Report

| Metric | Google Shopping | Amazon |
|--------|---------------|--------|
| Avg price | $ | $ |
| Median rating | X.X | X.X |
| Avg review count | N | N |
| Top seller share | % | % |
| Free shipping % | % | % |

---

## 4. Marketplace Keyword Gaps

Identify mismatches between organic and Shopping visibility.

### Workflow

1. Fetch organic rankings (ranked keywords for the domain) via DataForSEO Labs, or the seo-dataforseo skill.
2. Fetch Google Shopping presence via the Merchant API for the same top organic keywords.
3. Cross-reference the two result sets.

### Gap Types

| Gap Type | Meaning | Action |
|----------|---------|--------|
| **Organic Only** | Ranks organically but no Shopping ads | Create Google Merchant Center feed, bid on these keywords |
| **Shopping Only** | Shopping visibility but weak/no organic | Create content (buying guides, comparison pages) for these keywords |
| **Both Present** | Visible in both channels | Optimize: ensure price consistency, enhance schema |
| **Neither** | No visibility in either | Low priority unless high volume |

### Output Format

```
## Keyword Gap Analysis: example.com

### Opportunities: Organic → Shopping (12 keywords)
| Keyword | Organic Pos | Volume | CPC | Recommended Action |
|---------|------------|--------|-----|-------------------|

### Opportunities: Shopping → Organic (8 keywords)
| Keyword | Shopping Rank | Volume | CPC | Content Type Needed |
|---------|-------------|--------|-----|-------------------|
```

---

## 5. Product Schema Enhancement

Validate and generate Product schema following Google's current requirements.

### Confirmed Required Properties (Google Merchant)

Confirmed required fields are `name`, `image`, and `offers`; use `Offer`, not `AggregateOffer`, for merchant listings.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "",
  "image": [""],
  "offers": {
    "@type": "Offer",
    "url": "",
    "priceCurrency": "USD",
    "price": "0.00",
    "availability": "https://schema.org/InStock"
  }
}
```

### Recommended Properties (Enhance Rich Results)

- `sku` -- product identifier
- `description`, `brand`, `offers.seller` -- recommended context fields
- `gtin13` / `gtin14` / `mpn` -- global trade identifiers
- `aggregateRating` -- star rating + review count
- `review` -- individual reviews (minimum 1)
- `color`, `material`, `size` -- variant attributes
- `shippingDetails` -- ShippingDetails with rate and delivery time (merchant-level shipping via `ShippingService` is also supported; shipping/returns can be set in Search Console without a Merchant Center account)
- `hasMerchantReturnPolicy` -- MerchantReturnPolicy with type and days
- `hasAdultConsideration` -- **required for adult-oriented products** (added 2026-05-20 to Product variant / Merchant listing); Google Search supports only the value `https://schema.org/SexualContentConsideration`

### Validation Rules

1. `price` must be a number string, not "$29.99" (no currency symbol)
2. `availability` must use full Schema.org URL enum
3. `image` should be array with >= 1 high-res image URL
4. `priceCurrency` must be ISO 4217 (USD, EUR, GBP)
5. If `brand` is present, `brand.name` must not be empty or "N/A"
6. Dates in `priceValidUntil` must be ISO 8601
7. If `aggregateRating` present: `ratingValue` and `reviewCount` required

### Schema Scoring

| Completeness | Score |
|-------------|-------|
| All required fields | 50/100 |
| + aggregateRating | 65/100 |
| + sku/gtin/mpn | 75/100 |
| + shippingDetails | 85/100 |
| + merchantReturnPolicy | 90/100 |
| + reviews (3+) | 100/100 |

---

## 6. UCP: Universal Commerce Protocol (live)

Google-initiated open standard (co-developed with Shopify, Etsy, Wayfair,
Target, Walmart; payment partners Visa/Mastercard/Stripe/Adyen/Amex) for
letting AI agents discover, negotiate, and transact with merchants without
one-off integrations. Google confirms a first reference implementation for
conversational buying in AI Mode in Search. Broader Universal Cart rollout
details are reported from Google I/O 2026 keynote coverage; not confirmed on a
Google-owned source. ucp.dev lists **2026-04-08** as the latest release in its
**date-based versioning** scheme, not `1.0`; two integration paths: **Native**
(default) and **Embedded** (approved merchants). Pairs with **AP2** (reportedly
moving toward FIDO governance). Canonical: developers.google.com/merchant/ucp
and ucp.dev.

Merchants already on **Google Merchant Center** with clean Product schema can
declare a UCP profile at `/.well-known/ucp` listing capabilities
(`dev.ucp.shopping.checkout`, `.fulfillment`, `.discount`).

### Audit approach

Fetch `https://<domain>/.well-known/ucp` (use a safe fetch that resists SSRF —
resolve and validate the host before requesting, and don't follow redirects to
internal/private IP ranges). Then evaluate:

- **Profile presence and version** — flag a literal `"version": "1.0"` as
  invalid; UCP versions are date-based (e.g. `2026-04-08`).
- **Declared capabilities** — list each capability ID found and flag any that
  don't match the known `dev.ucp.shopping.*` namespace.
- **Structural issues** — missing required fields, malformed JSON, unknown
  capability IDs.
- **Endpoint reachability (optional)** — if asked to probe deeper, issue a
  HEAD request to each declared capability endpoint and report per-endpoint
  reachability. Report any endpoint that resolves to a private/internal
  address as blocked rather than requesting it.

A missing profile is an opportunity to report, not a failure — UCP itself is
live, but broad merchant adoption is still early.

---

## 7. Product Page Copywriting

Produces product page content that ranks and converts - written for the
shopper first, structured for search engines second, never the reverse.

**Inputs needed**: product name, key attributes/specs, target keyword(s),
price (for schema), availability status, and any existing description to
improve rather than replace from scratch. If this is a real product, ask for
actual specs rather than inventing them - schema markup with fabricated data
(price, availability, reviews) is a policy violation risk, never guess these
values.

**Title tag**: primary keyword near the front, product name clear, brand
name if it adds trust/differentiation, under ~60 characters. Include a
distinguishing attribute (size, color, material, model number) if there's
room and multiple variants could otherwise compete for the same query.

**Meta description**: under ~155 characters, includes the keyword and a
concrete reason to click - a specific benefit, differentiator, or offer, not
generic "shop our great selection."

**Product description copy**, two layers:
- *Above-the-fold/short* - 1-3 sentences, benefit-led, keyword appearing
  naturally.
- *Full description* - 100-300 words covering what the product is and who
  it's for, features translated into benefits (not a spec dump), semantic
  keyword variations woven in naturally (real related terms a shopper might
  search - e.g. for "waterproof hiking boots": "trail," "ankle support,"
  "breathable," "traction" - not keyword stuffing), and answers to likely
  pre-purchase questions (fit, compatibility, care/use).

**Schema markup** (JSON-LD), using only real values provided, never
fabricated: `name`, `description`, `image`, `offers` (price, priceCurrency,
availability - only if provided), `brand` if known, `sku`/`mpn` if provided,
`aggregateRating`/`review` only if real review data exists. State clearly if
any fields are left out due to missing information.

**Image alt text**: descriptive, includes product name + a relevant
attribute, never keyword-stuffed, written as if describing the image to
someone who can't see it.

**Output format**: title tag, meta description, short description, full
description, schema JSON-LD, alt text - each ready to copy-paste, in that
order. Flag assumptions or missing data clearly rather than silently filling
gaps.

---

## 8. Category Page Copywriting

Produces category/collection page copy and structural recommendations that
rank, without turning the page into keyword-stuffed text that hurts the
shopping experience.

**Inputs needed**: the category/collection, product range within it, target
keyword(s), and the broader site taxonomy (parent/sibling categories) for
internal linking and keyword differentiation.

**Keyword-to-category mapping**: identify the primary keyword this page
should target plus 2-4 closely related secondary keywords. Flag if the
category risks overlapping with a sibling category's keyword target (a
common e-commerce cannibalization source - see also content-cannibalization-
detector) and recommend how to differentiate (specificity, use case, or
consolidation).

**On-page elements**:
- *Title tag* - primary keyword near the front, category name clear, under
  ~60 characters, differentiator if relevant (brand, "Shop," a qualifier)
- *Meta description* - under ~155 characters, keyword + reason to click
  (selection size, key benefit, notable brands carried)
- *H1* - matches primary keyword intent, doesn't need to match the title tag
- *Intro copy* (above the product grid) - 2-4 sentences establishing what
  the category covers and its value, shopper-first, never keyword-stuffed
- *Bottom-of-page SEO copy* (below the grid, optional) - 150-400 words for
  search engines and shoppers wanting more context: buying guidance, what
  makes the category worth shopping, common use cases, FAQ-style content

**Faceted navigation guidance**: filters (size, color, price, brand) create
huge URL-combination counts that risk duplicate content and crawl budget
waste. Recommend which single-facet combinations deserve their own indexable
page (real, distinct search demand) vs. staying noindexed/canonicalized;
canonical strategy for multi-facet combinations (generally back to the base
category page unless there's clear demand evidence); and clean, consistent
URL parameter handling.

**Internal linking**: recommend links to relevant subcategories, top-selling
or featured products, related categories, and supporting content (buying
guides, comparisons) that should link back - natural, keyword-relevant
anchor text, not exact-match stuffed.

**Output format**: on-page copy first (ready to use), then faceted
navigation guidance, then keyword mapping and internal linking
recommendations. Flag any cannibalization risk near the top if found.

---

## Cross-Skill Notes

These findings pair well with skills you may already have for schema
generation and validation (e.g. a schema-tag-generator style skill), product
image auditing (alt text, format, `DigitalSourceType: TrainedAlgorithmicMedia`
IPTC labeling for AI-generated product images — a Merchant Center
requirement), product description E-E-A-T/uniqueness review, organic keyword
rankings (DataForSEO), Core Web Vitals for product pages (LCP on the hero
image), and GSC indexation/performance data for product URLs. Note that GSC
performance data is separate from Merchant Center feed validation — the
legacy Content API for Shopping sunsets 2026-08-18, use the Merchant API.

---

## Error Handling

| Error | Cause | Response |
|-------|-------|----------|
| No Product schema found | Page lacks JSON-LD | Analyze page content, generate recommended schema |
| DataForSEO credentials missing | MCP not connected | Run analysis without marketplace data, note limitation |
| Cost check declined | User didn't approve spend | Inform user, offer free-only analysis |
| Empty Shopping results | No products for keyword | Suggest broader keyword, check location settings |
| Amazon API timeout | Network/rate limit | Retry with backoff, fall back to Google-only |
| Invalid URL | Malformed input | Validate the URL format before fetching, show error |
| Non-product page | URL is category/homepage | Detect page type, suggest `/seo ecommerce schema` instead |

---

## Output Template

```
## E-commerce SEO Report: [URL or Keyword]

### Overall Score: XX/100

### Product Page SEO
- Schema Completeness: XX/100
- Title & Meta: XX/100
- Image Optimization: XX/100
- Content Quality: XX/100
- Internal Linking: XX/100

### Marketplace Intelligence (if DataForSEO available)
- Google Shopping Listings: N products found
- Price Range: $XX - $XX (median: $XX)
- Top Seller: [name] (XX% market share)
- Amazon Comparison: [available/not checked]

### Top Recommendations
1. [Critical] ...
2. [High] ...
3. [Medium] ...
```
