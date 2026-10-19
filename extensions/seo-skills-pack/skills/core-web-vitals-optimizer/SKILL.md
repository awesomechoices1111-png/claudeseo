---
name: core-web-vitals-optimizer
description: "Analyzes and improves Google Core Web Vitals scores including LCP (Largest Contentful Paint), INP (Interaction to Next Paint), and CLS (Cumulative Layout Shift). Use when user says Core Web Vitals, CWV, LCP, INP, CLS, page speed, site speed, PageSpeed Insights, improve performance score, slow loading site, layout shift, poor interactivity, optimize images for speed, fix render-blocking resources, reduce CLS, improve LCP, or wants to improve Google's page experience signals."
version: 0.1.0
---

# Core Web Vitals Optimizer

Diagnoses and fixes Core Web Vitals issues to hit Google's "Good" thresholds: LCP under 2.5s, INP under 200ms, CLS under 0.1. Provides prioritized, implementation-ready recommendations across images, fonts, CSS, JavaScript, and server configuration.

## What to Collect Before Starting

- **URL** to audit (preferred)
- **PageSpeed Insights results** — paste the JSON or screenshot if available
- **Tech stack** — WordPress, Shopify, Next.js, custom, etc.
- **Hosting/CDN** — Cloudflare, AWS, Vercel, etc.
- **Current scores** — if known (Mobile and Desktop separately)

If only a URL is given, analyze based on common CWV failure patterns for that type of site.

---

## Step 1: Score Baseline

Establish current state for each metric:

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| LCP | X.Xs | < 2.5s | Poor/Needs Improvement/Good |
| INP | Xms | < 200ms | Poor/Needs Improvement/Good |
| CLS | X.XX | < 0.1 | Poor/Needs Improvement/Good |
| TTFB | X.Xs | < 0.8s | (diagnostic, not a CWV) |

---

## Step 2: LCP Optimization

**Common LCP issues and fixes:**

**Image-based LCP element:**
- Add `fetchpriority="high"` to the LCP image
- Preload LCP image: `<link rel="preload" as="image" href="...">`
- Serve images in WebP/AVIF format
- Set explicit width and height attributes
- Use responsive images with `srcset` and `sizes`
- Eliminate lazy loading on above-the-fold images

**Text-based LCP element:**
- Eliminate render-blocking CSS/JS
- Inline critical CSS
- Use `font-display: swap` for web fonts
- Preconnect to font origins

**Server contribution:**
- Implement server-side caching
- Use a CDN for static assets
- Enable HTTP/2 or HTTP/3
- Reduce Time to First Byte (TTFB)

## Step 3: INP Optimization

**Common INP issues and fixes:**
- Break up long JavaScript tasks (> 50ms) with `scheduler.yield()`
- Defer non-critical JavaScript: `<script defer>` or dynamic imports
- Remove unused JavaScript (audit with Coverage tab in DevTools)
- Avoid synchronous XHR
- Minimize third-party script impact using Partytown or facade patterns
- Optimize event handlers — debounce scroll/resize listeners

## Step 4: CLS Optimization

**Common CLS issues and fixes:**
- Set explicit `width` and `height` on all images and videos
- Reserve space for ads and embeds with CSS `aspect-ratio`
- Avoid injecting content above existing content
- Use `transform` animations instead of layout-triggering properties
- Preload fonts to prevent FOIT/FOUT-caused shifts
- Avoid dynamically injected banners/cookie notices above the fold

## Step 5: Quick Wins by Platform

**WordPress:**
- Install caching plugin (WP Rocket, LiteSpeed Cache)
- Enable lazy loading for below-fold images
- Use WebP conversion plugin (Imagify, ShortPixel)
- Defer render-blocking plugins

**Shopify:**
- Use Shopify's built-in image CDN
- Minimize app scripts loading on all pages
- Use `critical` CSS technique for above-fold styles

**Next.js:**
- Use `next/image` for automatic optimization
- Enable ISR or SSG where possible
- Use `next/font` for optimized font loading

## Output Format

Deliver:
1. **CWV scorecard** — current vs target for each metric
2. **Priority fix list** — ordered by impact, with specific code snippets
3. **Platform-specific implementation guide**
4. **Expected improvement** — estimated score gain per fix
5. **Monitoring setup** — how to track CWV in Google Search Console
