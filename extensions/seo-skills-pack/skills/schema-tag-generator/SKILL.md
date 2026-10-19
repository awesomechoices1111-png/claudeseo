---
name: schema-tag-generator
description: "Generates valid JSON-LD structured data markup (schema.org) for any page type. Produces ready-to-paste code for Article, FAQ, HowTo, Product, LocalBusiness, Organization, BreadcrumbList, Event, Review, Person, JobPosting, and more. Use when user says schema markup, structured data, JSON-LD, schema.org, rich results, rich snippets, FAQ schema, product schema, local business schema, recipe schema, event schema, how to add schema, generate schema, schema for SEO, or wants to add structured data to their website."
version: 0.1.0
---

# Schema Tag Generator

Generates valid, Google-compliant JSON-LD structured data markup for any page type. Output is production-ready — paste into the `<head>` or `<body>` of the target page. Supports all major schema types eligible for Google Rich Results.

## What to Collect Before Starting

- **Page type** — what kind of page needs schema (article, product, FAQ, local business, etc.)
- **Page URL** — to populate the `@id` and `url` fields
- **Page content details** — title, description, author, date, prices, etc.
- **Site name and logo URL** — for Organization schema

If content is incomplete, generate a schema template with `[REPLACE: description]` placeholders.

---

## Step 1: Schema Type Selection

Match page type to the most appropriate schema:

| Page Type | Primary Schema | Supporting Schema |
|-----------|---------------|------------------|
| Blog post / Article | Article or BlogPosting | BreadcrumbList, Person (author) |
| Product page | Product | Offer, AggregateRating, BreadcrumbList |
| Homepage | Organization + WebSite | SiteLinksSearchBox |
| Local business | LocalBusiness | PostalAddress, GeoCoordinates, OpeningHours |
| FAQ page | FAQPage | — |
| How-to guide | HowTo | Article |
| Event page | Event | Offer |
| Recipe | Recipe | AggregateRating, Video |
| Person/Author | Person | — |
| Review | Review | AggregateRating |
| Job posting | JobPosting | — |
| Video | VideoObject | — |
| Course | Course | — |

## Step 2: Required Properties by Type

### Article / BlogPosting
Required: `headline`, `author`, `datePublished`, `image`
Recommended: `dateModified`, `publisher`, `description`, `mainEntityOfPage`

### Product
Required: `name`
Recommended: `image`, `description`, `sku`, `brand`, `offers` (price, currency, availability)

### FAQPage
Required: `mainEntity` array with `Question` and `acceptedAnswer`

### LocalBusiness
Required: `name`, `address` (PostalAddress)
Recommended: `telephone`, `url`, `openingHours`, `geo`, `priceRange`

### HowTo
Required: `name`, `step` array with `HowToStep`
Recommended: `totalTime`, `image`, `tool`, `supply`

## Step 3: JSON-LD Generation

Generate complete, valid JSON-LD for the requested schema type.

**Standard wrapper:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "[SchemaType]",
  ...
}
</script>
```

For multiple schema types on one page, generate separate `<script>` blocks or use an array:
```json
[
  { "@context": "...", "@type": "Article", ... },
  { "@context": "...", "@type": "BreadcrumbList", ... }
]
```

## Step 4: Validation Checklist

Before delivering, verify against these rules:
- [ ] `@context` is exactly `"https://schema.org"`
- [ ] All required fields for the type are present
- [ ] Image URLs are absolute (start with `https://`)
- [ ] Dates are in ISO 8601 format (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS+00:00`)
- [ ] Price values are numeric strings, not integers
- [ ] `@id` values are valid URLs
- [ ] No trailing commas in JSON

## Step 5: Implementation Instructions

Provide:
- Where to paste the code (before `</head>` or before `</body>`)
- CMS-specific instructions (WordPress: use plugin or theme functions.php; Shopify: theme.liquid; Webflow: custom code embed)
- Link to Google Rich Results Test: https://search.google.com/test/rich-results

## Output Format

Deliver:
1. **JSON-LD code block** — complete, ready-to-paste markup
2. **Placeholders flagged** — any fields requiring the user to fill in actual values
3. **Supporting schemas** — any additional schema types recommended for the same page
4. **Validation instructions** — how to test the output in Google Rich Results Test
5. **Rich result eligibility** — which Google rich result features this unlocks
