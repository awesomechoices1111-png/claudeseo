# Weekly Multi-Client Report

`scripts/weekly_report.py` runs one report per client from a clients file and
writes a cross-client summary. It reuses `gsc_query.py`, `ga4_report.py` and
`gsc_inspect.py`, so credentials come from the usual `google_auth.py` setup.

## Access per client

- **Search Console:** add the service account (or OAuth user) to each client
  property as a Full user. URL Inspection of losing pages needs this level.
- **GA4:** add it as Viewer under Admin > Property Access Management.
- Check once with `claude-seo run gsc_query.py sites --json`: every
  `gsc_property` in the clients file must appear.

## Clients file

Default path `~/.config/claude-seo/clients.json`, kept outside the repo
because it names client properties.

```json
{
  "clients": [
    {
      "slug": "acme",
      "name": "Acme Ltd",
      "gsc_property": "sc-domain:acme.com",
      "ga4_property": "123456789",
      "brand_terms": ["acme", "acme widgets"],
      "inspect_limit": 5
    },
    {
      "slug": "beta-dental",
      "name": "Beta Dental",
      "gsc_property": "https://www.betadental.co.uk/"
    }
  ]
}
```

| Field | Required | Notes |
|---|---|---|
| `slug` | yes | kebab-case; folder name |
| `name` | no | shown in the report; defaults to slug |
| `gsc_property` | yes | `sc-domain:` or URL-prefix property |
| `ga4_property` | no | numeric ID; GA4 section is skipped (and says so) without it |
| `brand_terms` | no | case-insensitive substrings for the brand/non-brand split |
| `inspect_limit` | no | URL Inspection calls on losing pages, 0-50, default 5 |

Validate without calling any API: `claude-seo run weekly_report.py validate --json`.

## Running

```bash
claude-seo run weekly_report.py run --json                    # all clients
claude-seo run weekly_report.py run --client acme --pdf        # one client + PDF
claude-seo run weekly_report.py run --today 2026-10-19         # reproducible date
claude-seo run weekly_report.py render seo-weekly-reports/acme/2026-10-19/weekly.json
```

Output layout:

```
seo-weekly-reports/
  summary-2026-10-19.md            # all clients, worst first
  acme/2026-10-19/weekly.md        # client-ready
  acme/2026-10-19/weekly.json      # full data, re-renderable
  acme/2026-10-19/*.pdf            # with --pdf (google_report.py gsc-performance)
```

With `--pdf`, check `pdf_review` in the run output is `PASS` before sending.

Exit codes: `0` all clients complete, `1` bad config or arguments, `2` at
least one client is missing a data source. Missing data is written into that
client's report as a critical alert; it is never skipped silently.

## Windows

| Source | Lag | Last 7 days on a Monday run | 28-day window |
|---|---|---|---|
| GA4 | 1 day | previous Mon-Sun | ends yesterday |
| GSC | 3 days | ends the previous Friday | ends 3 days ago |

Each window is compared with the one immediately before it. Lead with the
28-day comparison; the 7-day line is context.

## Noise test

A count change is called `up` or `down` only when
`|cur - prev| >= max(2 * sqrt(cur + prev), --min-change)` (default 5).
Otherwise it is "within normal variation". Example: 8 -> 6 sessions is noise;
400 -> 300 is a real drop. GA4 channels under 30 sessions in 28 days are
labelled low volume and their 7-day change is not called. This matters most
for the AI Assistant channel, which is usually single digits.

## Findings and their limits

- **Totals:** dimensionless GSC aggregate, never a sum of query rows.
- **Page movers:** pages whose 28-day clicks changed beyond noise. Losers get
  a URL Inspection check; a loser that is not indexed is a critical alert.
- **Low-CTR pages:** position <= 10 and >= 50 impressions, with CTR under half
  of a rough position benchmark. Pages ranking below position 10 are left out
  on purpose: their problem is ranking, which a title rewrite will not fix.
- **Striking distance:** queries at positions 5-20 with >= 20 impressions.
- **Brand split:** visible queries only, so it will not add up to site totals.
- **Next actions:** rule-based draft. An analyst reviews it before it goes to a client.

Not covered (no API): GSC Generative AI report (AI Overviews / AI Mode
impressions) and AI-assistant citation sampling. Add these by hand if the
client pays for AEO reporting.

## Scheduling

Cron on a machine that holds the credentials (Monday 07:10):

```cron
10 7 * * 1 cd ~/seo-reports && claude-seo run weekly_report.py run --json >> weekly.log 2>&1
```

Or use a Claude Code scheduled task with the prompt "Run `/seo google weekly`,
review each client's alerts and next actions, and summarise what needs my
attention." The task can only run where the Google credentials are available.
