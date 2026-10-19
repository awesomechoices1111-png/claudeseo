---
name: local-seo-playbook-generator
description: "Builds a complete local SEO strategy for any business location. Generates a GBP (Google Business Profile) optimization checklist, local citation target list, review response templates, NAP consistency audit, and geo-targeted content recommendations. Use when user says local SEO, Google Business Profile, GBP optimization, local citations, local search ranking, local pack, map pack, review management, NAP audit, Name Address Phone consistency, local listing, local SEO audit, rank in local search, local SEO strategy, improve local visibility, or provides a business name and location to optimize."
---

# Local SEO Playbook Generator

Produces a complete, actionable local SEO playbook for a single business location. Output covers five core pillars: GBP optimization, citation building, review management, NAP consistency, and geo-targeted content.

## What to Collect Before Starting

Ask the user for the following. If not provided, proceed with what is available and note any assumptions.

- **Business name** (exact legal name and any DBA)
- **Full address** (street, city, state/region, postcode, country)
- **Phone number** (primary local number)
- **Website URL**
- **Primary business category** (e.g., plumber, dentist, Italian restaurant)
- **Secondary categories** if any
- **Service area** (if business serves customers at their location rather than a fixed storefront)
- **Existing GBP status** (claimed/unclaimed/unknown)
- **Top 3 competitor names** (optional but improves citation gap analysis)
- **Current review count and average rating** (optional)

---

## Step 1: Business Profile Summary

Summarize the business in a standardized format. This becomes the "source of truth" NAP record.

```
CANONICAL NAP RECORD
Business Name : [exact name]
Address       : [street], [city], [state] [postcode], [country]
Phone         : [number in local format]
Website       : [URL with https://]
Primary Cat.  : [GBP primary category]
Secondary Cat.: [list if applicable]
Service Area  : [cities/regions if SAB]
```

Flag any inconsistencies the user mentioned vs. what appears on their website.

---

## Step 2: GBP Optimization Checklist

Work through each section of the Google Business Profile. Mark each item as DONE, NEEDS WORK, or MISSING based on user input.

Before generating this section, consult `references/gbp-optimization-guide.md` for field-level guidance and common mistakes per category type.

### Profile Completeness

| Item | Status | Priority |
|------|--------|----------|
| Business name matches legal/DBA name exactly | | HIGH |
| Primary category is the most specific available | | HIGH |
| All relevant secondary categories added (max 9) | | HIGH |
| Full address entered and matches website | | HIGH |
| Local phone number (not call center/toll-free) | | HIGH |
| Website URL links to location-specific page | | HIGH |
| Business hours complete including special hours | | HIGH |
| Holiday hours set for next 3 months | | MEDIUM |
| Business description written (750 chars, keyword-rich) | | HIGH |
| Opening date populated | | LOW |

### Visual Assets

| Item | Status | Priority |
|------|--------|----------|
| Cover photo (1332x750px) is brand-appropriate | | HIGH |
| Logo uploaded (250x250px, square) | | HIGH |
| At least 10 interior/exterior photos added | | HIGH |
| Product or service photos added | | MEDIUM |
| Team photos added | | LOW |
| Video uploaded (max 30 seconds, 75MB) | | LOW |
| 360-degree photos (if physical location) | | LOW |

### Products and Services

| Item | Status | Priority |
|------|--------|----------|
| All core services listed with descriptions | | HIGH |
| Service areas defined (if SAB) | | HIGH |
| Products added with photos and prices | | MEDIUM |
| Menu linked or added (if food service) | | HIGH |

### Q&A and Posts

| Item | Status | Priority |
|------|--------|----------|
| Top 5 FAQs pre-seeded and answered | | HIGH |
| GBP Post published in last 7 days | | MEDIUM |
| Offer Posts used for current promotions | | MEDIUM |
| Event Posts added for upcoming events | | LOW |

### Attributes and Additional Info

| Item | Status | Priority |
|------|--------|----------|
| All applicable attributes ticked (accessibility, payments, etc.) | | MEDIUM |
| Highlights selected (e.g., Women-led, Veteran-owned) | | LOW |
| URL fields populated (appointment, menu, order) | | MEDIUM |
| Messaging enabled (if monitored) | | LOW |

**GBP Score:** Count DONE items vs total and express as percentage. Flag any HIGH-priority items marked MISSING as critical.

---

## Step 3: Local Citation Target List

Generate a tiered citation target list based on the business category and location.

Before generating, consult `references/citation-strategy-guide.md` for tier definitions and category-specific directories.

### Tier 1: Universal Foundations (All Businesses)

These must be claimed and consistent first:

1. Google Business Profile (gbp.google.com)
2. Apple Maps Connect (mapsconnect.apple.com)
3. Bing Places (bingplaces.com)
4. Yelp for Business (biz.yelp.com)
5. Facebook Business Page
6. LinkedIn Company Page (B2B/professional services)
7. Foursquare for Business
8. Yellow Pages (yellowpages.com)
9. Better Business Bureau (bbb.org)
10. Chamber of Commerce website (local)

### Tier 2: Data Aggregators (Critical for Citation Syndication)

Submit to these first — they feed hundreds of downstream directories:

1. Data Axle (formerly Infogroup)
2. Neustar Localeze
3. Foursquare (also feeds Apple Maps and others)
4. Factual / Foursquare OS

**Note:** Aggregator submissions can take 6-12 weeks to propagate. Use Yext, Moz Local, or BrightLocal to accelerate.

### Tier 3: Category-Specific Directories

Based on `[PRIMARY CATEGORY]`, add the relevant section from `references/citation-strategy-guide.md`.

Present as a table:

| Directory | URL | Priority | Notes |
|-----------|-----|----------|-------|
| [Name] | [URL] | HIGH/MED/LOW | [Any notes] |

### Tier 4: Local and Regional Directories

- Local newspaper or media site business directory
- City or council business directory
- Local Chamber of Commerce member listing
- Regional business association

### Citation Gap Summary

If competitor names were provided, note:
```
RECOMMENDED NEXT STEPS
1. Claim and complete all Tier 1 profiles (target: 2 weeks)
2. Submit to all 4 data aggregators (target: week 1)
3. Work through Tier 3 directories relevant to [category] (target: 4-6 weeks)
4. Set a quarterly citation audit reminder
```

---

## Step 4: NAP Consistency Audit

Check for NAP inconsistencies across the most common citation sources. If the user provides existing listings, flag discrepancies against the Canonical NAP Record from Step 1.

Run `nap_checker.py` if a CSV of existing citations is provided:
```
claude-seo run --extension seo-skills-pack nap_checker.py --input citations.csv --canonical "Business Name|123 Main St|555-0100"
```

### Manual Audit Checklist

Even without a CSV, walk the user through checking these:

| Check | Pass/Fail | Notes |
|-------|-----------|-------|
| Business name spelling consistent across all platforms | | |
| Suite/unit number included or excluded consistently | | |
| Phone format consistent (with/without dashes, country code) | | |
| Website URL canonical (www vs non-www, http vs https) | | |
| No old addresses appearing on active listings | | |
| No duplicate listings on same platform | | |

### Common NAP Error Patterns

Flag if any of these are detected:

- **Abbreviation inconsistency**: "St" vs "Street" vs "St." (pick one and standardize)
- **Suite formatting**: "Suite 4" vs "#4" vs "Ste 4"
- **Phone format**: Include/exclude country code consistently
- **DBA confusion**: Never mix legal name and DBA on the same listing
- **Tracking numbers**: If call tracking numbers are used, ensure they are not submitted to aggregators (they create false NAP variants)

### NAP Correction Priority

```
IMMEDIATE (same week)    : Fix GBP, website footer, and Tier 1 directories
SHORT TERM (1 month)     : Fix data aggregators and Tier 2 directories
ONGOING (quarterly)      : Audit for new inconsistencies and directory drift
```

---

## Step 5: Review Management Templates

Generate a set of review response templates tailored to the business type. Personalize tone based on business category (professional/clinical vs. friendly/casual).

Before generating templates, consider:
- Business category tone (e.g., dental clinic = warm but professional; pizza restaurant = casual and upbeat)
- Any specific services or products the business offers (weave in naturally)
- Local city/neighborhood references where appropriate

Consult `references/review-response-templates.md` for tone calibration and more template variants.

### Positive Review Responses (4-5 stars)

**Template P1 — Generic Positive**
```
Thank you so much, [First Name]! We're thrilled you had a great experience at [Business Name]. 
[Personalized line referencing specific service/product if mentioned in review.]
We look forward to seeing you again soon!

— [Owner/Manager Name], [Business Name]
```

**Template P2 — Long Positive (Detailed Review)**
```
[First Name], this made our day — thank you! We work hard to [specific value prop], 
so hearing this means a lot to the whole team. [Reference specific detail they mentioned.]
If there's ever anything we can do to make your next visit even better, please don't 
hesitate to ask. We appreciate your support!

— [Business Name] Team
```

**Template P3 — Referral Nudge**
```
Thank you, [First Name]! Reviews like yours are what keep us going. If you know anyone 
looking for [service category] in [city], we'd love to help them too. See you next time!

— [Business Name]
```

### Neutral Review Responses (3 stars)

**Template N1 — Acknowledge and Improve**
```
Thank you for taking the time to share your experience, [First Name]. We're glad you 
[positive element], but we're sorry we didn't fully meet your expectations regarding 
[issue if mentioned]. We take all feedback seriously and are working to improve. 
We'd love the chance to make it right — please contact us directly at [email/phone].

— [Manager Name], [Business Name]
```

### Negative Review Responses (1-2 stars)

**Template G1 — Empathetic Acknowledgment**
```
[First Name], thank you for sharing this — even though it's hard to hear, it helps us improve.
I'm sorry your experience didn't reflect the standard we set for ourselves. 
I'd really like to understand what happened and make it right. 
Please reach out to me directly at [email] or [phone] so we can resolve this properly.

— [Owner/Manager Name], [Business Name]
```

**Template G2 — Factually Incorrect Review**
```
Thank you for the feedback. We take all reviews seriously and have reviewed our records 
for your visit. We weren't able to find a record matching this experience, which suggests 
there may have been a misunderstanding. We would genuinely welcome the chance to speak 
with you directly — please contact us at [email/phone] so we can help clarify and resolve 
any concerns.

— [Business Name] Team
```

**Template G3 — Service Recovery**
```
[First Name], I'm sorry to hear this. This is not the experience we work to provide, 
and I completely understand your frustration. I would personally like to make this right. 
Please reach out to me at [direct email] — I'd like to offer [appropriate resolution].

— [Owner/Manager Name]
```

### Review Generation Strategy

```
BEST PRACTICES FOR GETTING MORE REVIEWS
1. Ask in person within 24 hours of service completion
2. Send a follow-up SMS or email with a direct GBP review link
3. Add a review QR code at point of sale or on receipts
4. Never incentivize reviews (violates Google's guidelines)
5. Respond to every review within 24-48 hours
6. GBP review link: https://g.page/r/[your-place-id]/review
```

---

## Step 6: Geo-Targeted Content Recommendations

Generate a content strategy targeting local intent keywords. Prioritize pages and topics based on business type and location.

### Local Landing Page Audit

Check if the website has:

| Page Type | Status | Priority |
|-----------|--------|----------|
| Homepage with city name in H1 and title tag | | HIGH |
| Dedicated location page for each physical location | | HIGH |
| Service area pages for each city/suburb served | | HIGH |
| "Near me" optimized content on key pages | | MEDIUM |
| Local schema markup (LocalBusiness, GeoCoordinates) | | HIGH |

### Geo-Targeted Content Calendar (12-Month Framework)

Produce a quarterly content plan targeting local intent:

**Q1: Authority and Trust**
- "[Service] in [City] — Complete Guide" (pillar page)
- "[City] [Category] FAQ" (targets PAA and voice search)
- "Why [Business Name] is [City]'s choice for [service]"

**Q2: Seasonal and Event-Based**
- "[Seasonal event] + [service] content" (e.g., "Spring HVAC tune-up in [City]")
- Local event sponsorship or participation recap
- "[Holiday] hours and deals at [Business Name] in [City]"

**Q3: Community and Local Authority**
- "[City] neighbourhood guides" related to your service
- "Best [category] in [City] — What to Look For" (positions as authority)
- Local partnership spotlight or case study

**Q4: Review and Year-End**
- Year-in-review content featuring customer success stories
- "Top [service] tips for [City] residents this winter/year"
- New year offer announcement geo-targeted landing page

### Local Keyword Framework

Generate a keyword set using this structure:

```
PRIMARY (highest volume, highest intent)
- "[service] [city]"
- "[service] near me"
- "[service] [city] [state]"

SECONDARY (neighbourhood/suburb targeting)
- "[service] [suburb/neighbourhood]"
- "[service] near [landmark or area]"

LONG-TAIL (low competition, high conversion)
- "best [service] in [city]"
- "affordable [service] [city]"
- "[service] open [day/time] [city]"
- "emergency [service] [city]"

VOICE SEARCH
- "who is the best [service provider type] near me"
- "where can I find [service] in [city]"
- "how much does [service] cost in [city]"
```

### Local Schema Markup Recommendation

Provide a LocalBusiness JSON-LD snippet pre-filled with the user's details:

```json
{
  "@context": "https://schema.org",
  "@type": "[BusinessType]",
  "name": "[Business Name]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street]",
    "addressLocality": "[City]",
    "addressRegion": "[State]",
    "postalCode": "[Postcode]",
    "addressCountry": "[Country Code]"
  },
  "telephone": "[Phone]",
  "url": "[Website URL]",
  "openingHours": ["Mo-Fr 09:00-17:00"],
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[lat]",
    "longitude": "[lng]"
  },
  "sameAs": [
    "[GBP URL]",
    "[Facebook URL]",
    "[Yelp URL]"
  ]
}
```

---

## Step 7: Master Playbook Output

After completing all six steps, consolidate into a master summary:

```
LOCAL SEO PLAYBOOK — [BUSINESS NAME]
Generated: [Date]

IMMEDIATE ACTIONS (Week 1-2)
1. [Top 3 GBP issues flagged as HIGH/MISSING]
2. Submit to all 4 data aggregators
3. Fix NAP inconsistencies on GBP and website

SHORT TERM (Month 1-3)
4. Build out Tier 1 and Tier 2 citations
5. Implement LocalBusiness schema on website
6. Publish first 2 geo-targeted content pieces
7. Set up review response workflow

ONGOING (Quarterly)
8. NAP consistency audit
9. GBP post cadence (weekly)
10. Review monitoring and response (within 48 hours)
11. Citation audit for new gaps

TRACKING METRICS
- GBP Insights: Calls, direction requests, website clicks
- Local pack rankings for primary keywords
- Review count and average rating trend
- Citation accuracy score (via BrightLocal or Moz Local)
```

---

## Examples

### Example 1: Single-Location Restaurant

**User says:** "Help me with local SEO for my pizza restaurant in Austin, Texas"

**Actions:**
1. Collect business details (name, address, phone, website)
2. Generate GBP checklist with restaurant-specific fields (menu, food photos, ordering URL)
3. Produce citation list prioritizing food-specific directories (TripAdvisor, OpenTable, Zomato, Google Maps)
4. Create casual, warm review response templates matching restaurant brand voice
5. NAP audit against website footer and existing Google listing
6. Content plan targeting "pizza Austin", "best pizza near me", "late night pizza Austin"

**Result:** Full playbook with restaurant-specific citation targets, menu-photo GBP checklist, and casual review templates.

### Example 2: Multi-Service B2B Company

**User says:** "We're a commercial cleaning company in Chicago, do a local SEO audit"

**Actions:**
1. Classify as Service Area Business (SAB) — no storefront address displayed
2. Adjust GBP checklist to SAB mode (hide address, configure service area)
3. Generate citation list for commercial cleaning (Angi, Thumbtack, BuildZoom, industry associations)
4. Professional tone for review templates
5. Content plan targeting service-area suburbs ("commercial cleaning Naperville", "office cleaning Evanston")

**Result:** SAB-optimized playbook with hidden-address NAP guidance and suburb-level content targeting.

---

## Troubleshooting

### User has no GBP listing yet
Walk them through the GBP creation process: Visit business.google.com, select "Add your business", enter details matching the Canonical NAP Record. Suggest immediate verification by postcard or phone if eligible. Note that new listings take 1-4 weeks before appearing in local pack results.

### Suspended or penalized GBP listing
Do not attempt to re-optimize a suspended listing. Advise the user to review Google's guidelines for eligible businesses, complete the reinstatement request form, and remove any guideline violations from the profile before submitting. Common suspension causes: keyword stuffing in business name, incorrect category, virtual office address.

### Business serves multiple cities (SAB)
Set the profile to "Service Area Business" mode. Do not display a physical address. Configure service areas to match the actual geographic reach (max 20 areas per profile). Create individual service-area landing pages per city for content targeting.

### Conflicting information across platforms
Prioritize fixing in this order: GBP first, website second, data aggregators third, then individual directories. Changing aggregators propagates corrections downstream and saves manual effort on hundreds of directories.
