#!/usr/bin/env python3
"""
Weekly multi-client SEO report runner.

Pulls Google Search Console and GA4 data for every client in a clients file,
compares the latest 7- and 28-day windows against the windows before them,
and writes one Markdown + JSON report per client plus a cross-client summary.

Changes are only called "up" or "down" when they clear a noise test
(|cur - prev| >= 2 * sqrt(cur + prev) and at least --min-change). Small sites
move a lot week to week by chance; the report says so instead of alarming.

Clients file (default ~/.config/claude-seo/clients.json):
    {"clients": [{
        "slug": "acme",                       # kebab-case, used for folder names
        "name": "Acme Ltd",
        "gsc_property": "sc-domain:acme.com",
        "ga4_property": "123456789",          # optional
        "brand_terms": ["acme"],              # optional, for brand/non-brand split
        "inspect_limit": 5                    # optional, URL Inspection calls per run
    }]}

Usage:
    python weekly_report.py run --json
    python weekly_report.py run --client acme --out reports/ --pdf
    python weekly_report.py run --today 2026-10-19
    python weekly_report.py render reports/acme/2026-10-19/weekly.json
    python weekly_report.py validate --clients clients.json
"""

import argparse
import json
import math
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DEFAULT_CLIENTS_PATH = os.path.expanduser("~/.config/claude-seo/clients.json")
DEFAULT_OUT_DIR = "seo-weekly-reports"
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
GSC_LAG_DAYS = 3
GA4_LAG_DAYS = 1
DEFAULT_INSPECT_LIMIT = 5
LOW_VOLUME_SESSIONS = 30

# Approximate organic CTR by rounded position (desktop+mobile blend). Only used
# to flag pages far below typical; SERP features move real CTR a lot.
CTR_BENCHMARK = {1: 0.25, 2: 0.13, 3: 0.09, 4: 0.065, 5: 0.05,
                 6: 0.04, 7: 0.03, 8: 0.025, 9: 0.02, 10: 0.018}

SEVERITY_ORDER = {"critical": 0, "warning": 1, "info": 2}


# ─── Config ───────────────────────────────────────────────────────────────────

def load_clients(path: str) -> list:
    """Load and validate the clients file. Raises ValueError on bad config."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Clients file not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Clients file is not valid JSON: {e}")

    clients = raw.get("clients") if isinstance(raw, dict) else None
    if not isinstance(clients, list) or not clients:
        raise ValueError('Clients file must contain a non-empty "clients" list')

    seen = set()
    for i, c in enumerate(clients):
        if not isinstance(c, dict):
            raise ValueError(f"clients[{i}] must be an object")
        slug = c.get("slug")
        if not isinstance(slug, str) or not SLUG_RE.match(slug):
            raise ValueError(f"clients[{i}].slug must be kebab-case (a-z, 0-9, -)")
        if slug in seen:
            raise ValueError(f"Duplicate client slug: {slug}")
        seen.add(slug)
        prop = c.get("gsc_property")
        if not isinstance(prop, str) or not (
            prop.startswith("sc-domain:") or prop.startswith("https://") or prop.startswith("http://")
        ):
            raise ValueError(
                f"{slug}: gsc_property must be 'sc-domain:example.com' or a URL-prefix property"
            )
        ga4 = c.get("ga4_property")
        if ga4 is not None and not re.fullmatch(r"(properties/)?\d+", str(ga4)):
            raise ValueError(f"{slug}: ga4_property must be a numeric GA4 property ID")
        terms = c.get("brand_terms", [])
        if not isinstance(terms, list) or any(not isinstance(t, str) or not t.strip() for t in terms):
            raise ValueError(f"{slug}: brand_terms must be a list of non-empty strings")
        limit = c.get("inspect_limit", DEFAULT_INSPECT_LIMIT)
        if not isinstance(limit, int) or isinstance(limit, bool) or not 0 <= limit <= 50:
            raise ValueError(f"{slug}: inspect_limit must be an integer 0-50")
        c.setdefault("name", slug)
    return clients


# ─── Windows and comparisons (pure) ───────────────────────────────────────────

def compute_windows(today: date) -> dict:
    """Current/previous 7- and 28-day windows for GSC (3-day lag) and GA4 (1-day lag)."""
    def windows(end: date) -> dict:
        def rng(days, offset):
            e = end - timedelta(days=offset)
            return {"start": (e - timedelta(days=days - 1)).isoformat(), "end": e.isoformat()}
        return {"cur7": rng(7, 0), "prev7": rng(7, 7), "cur28": rng(28, 0), "prev28": rng(28, 28)}

    return {
        "gsc": windows(today - timedelta(days=GSC_LAG_DAYS)),
        "ga4": windows(today - timedelta(days=GA4_LAG_DAYS)),
    }


def change_verdict(cur: float, prev: float, min_change: int = 5) -> dict:
    """Classify a count change as up/down/flat using a Poisson noise test."""
    delta = cur - prev
    pct = round(delta / prev * 100, 1) if prev else None
    noise = 2 * math.sqrt(cur + prev) if (cur + prev) > 0 else 0
    if abs(delta) >= max(noise, min_change) and delta != 0:
        verdict = "up" if delta > 0 else "down"
    else:
        verdict = "flat"
    return {"cur": cur, "prev": prev, "delta": delta, "pct": pct, "verdict": verdict}


def compare_gsc_totals(cur: dict, prev: dict, min_change: int = 5) -> dict:
    """Compare two GSC totals dicts. Counts get a noise verdict; rates get deltas."""
    return {
        "clicks": change_verdict(cur.get("clicks", 0), prev.get("clicks", 0), min_change),
        "impressions": change_verdict(cur.get("impressions", 0), prev.get("impressions", 0), min_change),
        "ctr": {"cur": cur.get("ctr", 0), "prev": prev.get("ctr", 0),
                "delta": round(cur.get("ctr", 0) - prev.get("ctr", 0), 2)},
        "position": {"cur": cur.get("position", 0), "prev": prev.get("position", 0),
                     "delta": round(cur.get("position", 0) - prev.get("position", 0), 1)},
    }


def page_movers(cur_rows: list, prev_rows: list, min_change: int = 5, limit: int = 10) -> dict:
    """Pages whose clicks changed beyond noise between two page-dimension pulls."""
    cur = {r["page"]: r for r in cur_rows if r.get("page")}
    prev = {r["page"]: r for r in prev_rows if r.get("page")}
    movers = []
    for page in set(cur) | set(prev):
        c = cur.get(page, {})
        p = prev.get(page, {})
        v = change_verdict(c.get("clicks", 0), p.get("clicks", 0), min_change)
        if v["verdict"] == "flat":
            continue
        movers.append({
            "page": page,
            "clicks": v,
            "position_cur": c.get("position"),
            "position_prev": p.get("position"),
            "impressions_cur": c.get("impressions", 0),
            "impressions_prev": p.get("impressions", 0),
        })
    losers = sorted([m for m in movers if m["clicks"]["verdict"] == "down"],
                    key=lambda m: m["clicks"]["delta"])[:limit]
    gainers = sorted([m for m in movers if m["clicks"]["verdict"] == "up"],
                     key=lambda m: -m["clicks"]["delta"])[:limit]
    return {"losers": losers, "gainers": gainers}


def striking_distance(query_rows: list, min_pos: float = 5, max_pos: float = 20,
                      min_impressions: int = 20, limit: int = 15) -> list:
    """Queries ranking 5-20 ranked by impressions: the 'nearly there' list."""
    hits = [r for r in query_rows
            if min_pos <= r.get("position", 0) <= max_pos
            and r.get("impressions", 0) >= min_impressions]
    hits.sort(key=lambda r: -r.get("impressions", 0))
    return [{"query": r.get("query"), "page": r.get("page"),
             "impressions": r.get("impressions", 0), "clicks": r.get("clicks", 0),
             "position": r.get("position")} for r in hits[:limit]]


def low_ctr_pages(page_rows: list, min_impressions: int = 50, limit: int = 10) -> list:
    """Page-one pages earning under half the typical CTR for their position.

    Pages below position 10 are excluded on purpose: their problem is ranking,
    and rewriting a title will not fix it.
    """
    out = []
    for r in page_rows:
        pos = r.get("position", 0)
        impr = r.get("impressions", 0)
        if not (1 <= pos <= 10.4) or impr < min_impressions:
            continue
        expected = CTR_BENCHMARK[min(10, max(1, int(round(pos))))] * 100
        ctr = r.get("ctr", 0)
        if ctr < expected / 2:
            out.append({"page": r.get("page"), "impressions": impr, "clicks": r.get("clicks", 0),
                        "ctr": ctr, "expected_ctr": round(expected, 1), "position": pos,
                        "missed_clicks": int(impr * (expected / 100) - r.get("clicks", 0))})
    out.sort(key=lambda r: -r["missed_clicks"])
    return out[:limit]


def brand_split(query_rows: list, brand_terms: list) -> Optional[dict]:
    """Brand vs non-brand clicks over visible (non-anonymized) queries only."""
    if not brand_terms:
        return None
    pattern = re.compile("|".join(re.escape(t.lower()) for t in brand_terms))
    brand = {"clicks": 0, "impressions": 0}
    non = {"clicks": 0, "impressions": 0}
    for r in query_rows:
        bucket = brand if pattern.search((r.get("query") or "").lower()) else non
        bucket["clicks"] += r.get("clicks", 0)
        bucket["impressions"] += r.get("impressions", 0)
    return {"brand": brand, "non_brand": non,
            "note": "Visible queries only. GSC hides anonymized queries, so these "
                    "do not add up to site totals."}


def build_alerts(report: dict) -> list:
    """Turn findings into a severity-ordered alert list."""
    alerts = []
    for source, err in report.get("errors", {}).items():
        alerts.append({"severity": "critical", "text": f"{source} data missing: {err}"})

    gsc = report.get("gsc", {})
    cmp28 = gsc.get("compare28", {})
    if cmp28.get("clicks", {}).get("verdict") == "down":
        c = cmp28["clicks"]
        alerts.append({"severity": "warning",
                       "text": f"Organic clicks down beyond normal variation over 28 days "
                               f"({c['prev']} -> {c['cur']})."})
    for sm in gsc.get("sitemaps", []):
        if sm.get("errors"):
            alerts.append({"severity": "critical",
                           "text": f"Sitemap {sm.get('path')} reports {sm['errors']} error(s)."})
        elif sm.get("warnings"):
            alerts.append({"severity": "warning",
                           "text": f"Sitemap {sm.get('path')} reports {sm['warnings']} warning(s)."})

    for loser in gsc.get("movers", {}).get("losers", []):
        insp = loser.get("inspection") or {}
        if insp.get("verdict") == "FAIL":
            alerts.append({"severity": "critical",
                           "text": f"{loser['page']} lost clicks and is not indexed "
                                   f"({insp.get('coverage_state') or 'no coverage state'})."})
        elif insp.get("canonical_match") is False:
            alerts.append({"severity": "warning",
                           "text": f"{loser['page']} lost clicks and Google picked a different canonical."})

    for w in gsc.get("warnings", []):
        alerts.append({"severity": "info", "text": w})

    alerts.sort(key=lambda a: SEVERITY_ORDER.get(a["severity"], 9))
    return alerts


def draft_actions(report: dict) -> list:
    """Rule-based next actions. A draft for the analyst, not a final recommendation."""
    actions = []
    gsc = report.get("gsc", {})
    for a in report.get("alerts", []):
        if a["severity"] == "critical":
            actions.append(f"Fix: {a['text']}")
    for p in gsc.get("low_ctr_pages", [])[:3]:
        actions.append(f"Rewrite title/meta for {p['page']} (pos {p['position']}, CTR {p['ctr']}% "
                       f"vs ~{p['expected_ctr']}% typical, ~{p['missed_clicks']} clicks/28d missed).")
    for q in gsc.get("striking_distance", [])[:2]:
        actions.append(f"Strengthen {q['page']} for \"{q['query']}\" (pos {q['position']}, "
                       f"{q['impressions']} impressions): content depth and internal links.")
    for m in gsc.get("movers", {}).get("losers", [])[:2]:
        if (m.get("inspection") or {}).get("verdict") != "FAIL":
            actions.append(f"Investigate click loss on {m['page']} "
                           f"({m['clicks']['prev']} -> {m['clicks']['cur']}): compare SERP and recent edits.")
    return actions


# ─── Data collection (API) ────────────────────────────────────────────────────

def collect_gsc(client: dict, win: dict, min_change: int, inspect: bool) -> tuple:
    """Pull GSC totals, page and query rows, sitemaps, and loser inspections."""
    import gsc_query  # lazy: exits if google-api-python-client is missing

    prop = client["gsc_property"]
    out = {"warnings": []}

    totals = {}
    for key in ("cur7", "prev7", "cur28", "prev28"):
        res = gsc_query.query_search_analytics(prop, win[key]["start"], win[key]["end"],
                                               dimensions=[], row_limit=1)
        if res.get("error"):
            return None, res["error"]
        totals[key] = res["totals"]
        out["warnings"].extend(w for w in res.get("warnings", []) if w not in out["warnings"])
    out["totals"] = totals
    out["compare7"] = compare_gsc_totals(totals["cur7"], totals["prev7"], min_change)
    out["compare28"] = compare_gsc_totals(totals["cur28"], totals["prev28"], min_change)

    pages_cur = gsc_query.query_search_analytics(prop, win["cur28"]["start"], win["cur28"]["end"],
                                                 dimensions=["page"], row_limit=5000)
    pages_prev = gsc_query.query_search_analytics(prop, win["prev28"]["start"], win["prev28"]["end"],
                                                  dimensions=["page"], row_limit=5000)
    queries = gsc_query.query_search_analytics(prop, win["cur28"]["start"], win["cur28"]["end"],
                                               dimensions=["query", "page"], row_limit=5000)
    for res in (pages_cur, pages_prev, queries):
        if res.get("error"):
            out["warnings"].append(f"Partial GSC data: {res['error']}")

    out["movers"] = page_movers(pages_cur.get("rows", []), pages_prev.get("rows", []), min_change)
    out["low_ctr_pages"] = low_ctr_pages(pages_cur.get("rows", []))
    out["striking_distance"] = striking_distance(queries.get("rows", []))
    out["brand_split"] = brand_split(queries.get("rows", []), client.get("brand_terms", []))
    out["top_queries"] = sorted(queries.get("rows", []), key=lambda r: -r.get("clicks", 0))[:20]

    sm = gsc_query.list_sitemaps(prop)
    if sm.get("error"):
        out["warnings"].append(f"Sitemaps API: {sm['error']}")
    out["sitemaps"] = [{"path": s.get("path"), "errors": s.get("errors", 0),
                        "warnings": s.get("warnings", 0), "is_pending": s.get("is_pending"),
                        "last_submitted": s.get("last_submitted")} for s in sm.get("sitemaps", [])]

    limit = client.get("inspect_limit", DEFAULT_INSPECT_LIMIT) if inspect else 0
    if limit:
        import gsc_inspect
        for loser in out["movers"]["losers"][:limit]:
            r = gsc_inspect.inspect_url(loser["page"], prop)
            idx = r.get("index_status") or {}
            loser["inspection"] = {
                "verdict": r.get("verdict"),
                "coverage_state": idx.get("coverage_state"),
                "last_crawl_time": idx.get("last_crawl_time"),
                "canonical_match": (r.get("canonical") or {}).get("match"),
                "error": r.get("error"),
            }

    # Shape google_report.py's gsc-performance type expects, for --pdf.
    out["_pdf_payload"] = {"gsc": {**queries, "totals": totals["cur28"]}}
    return out, None


def collect_ga4(client: dict, win: dict, min_change: int) -> tuple:
    """Sessions, engagement and key events by default channel group, 4 windows in one call."""
    import ga4_report  # lazy: exits if google-analytics-data is missing
    from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

    ga = ga4_report._build_ga4_client()
    if not ga:
        return None, "Could not build GA4 client. Check credentials and property access."

    names = ("cur7", "prev7", "cur28", "prev28")
    metrics = ("sessions", "engagedSessions", "engagementRate", "averageSessionDuration", "keyEvents")
    try:
        resp = ga.run_report(RunReportRequest(
            property=ga4_report._resolve_property(str(client["ga4_property"])),
            dimensions=[Dimension(name="sessionDefaultChannelGroup")],
            metrics=[Metric(name=m) for m in metrics],
            date_ranges=[DateRange(start_date=win[n]["start"], end_date=win[n]["end"], name=n)
                         for n in names],
            limit=500,
        ))
    except Exception as e:
        return None, f"GA4 API error: {e}"

    dim_names = [h.name for h in resp.dimension_headers]
    ch_i = dim_names.index("sessionDefaultChannelGroup")
    dr_i = dim_names.index("dateRange") if "dateRange" in dim_names else None
    channels = {}
    for row in resp.rows:
        channel = row.dimension_values[ch_i].value
        window = row.dimension_values[dr_i].value if dr_i is not None else "cur28"
        vals = [float(v.value or 0) for v in row.metric_values]
        channels.setdefault(channel, {})[window] = {
            "sessions": int(vals[0]), "engaged_sessions": int(vals[1]),
            "engagement_rate": round(vals[2] * 100, 1),
            "avg_duration": round(vals[3], 1), "key_events": round(vals[4], 1),
        }
    return {"channels": summarize_channels(channels, min_change)}, None


def summarize_channels(channels: dict, min_change: int = 5) -> list:
    """Per-channel 28d and 7d comparisons, sorted by 28d sessions."""
    empty = {"sessions": 0, "engaged_sessions": 0, "engagement_rate": 0, "avg_duration": 0, "key_events": 0}
    rows = []
    for name, w in channels.items():
        cur28, prev28 = w.get("cur28", empty), w.get("prev28", empty)
        cur7, prev7 = w.get("cur7", empty), w.get("prev7", empty)
        rows.append({
            "channel": name,
            "cur28": cur28, "prev28": prev28,
            "sessions28": change_verdict(cur28["sessions"], prev28["sessions"], min_change),
            "sessions7": change_verdict(cur7["sessions"], prev7["sessions"], min_change),
            "key_events28": change_verdict(cur28["key_events"], prev28["key_events"], min_change),
            "low_volume": cur28["sessions"] < LOW_VOLUME_SESSIONS,
        })
    rows.sort(key=lambda r: -r["cur28"]["sessions"])
    return rows


def run_client(client: dict, today: date, min_change: int, inspect: bool) -> dict:
    """Collect everything for one client. Missing sources are recorded, never skipped silently."""
    win = compute_windows(today)
    report = {"client": {k: client.get(k) for k in ("slug", "name", "gsc_property", "ga4_property")},
              "generated": datetime.now().isoformat(timespec="seconds"),
              "report_date": today.isoformat(), "windows": win, "errors": {}}

    gsc, err = collect_gsc(client, win["gsc"], min_change, inspect)
    if err:
        report["errors"]["Search Console"] = err
    report["gsc"] = gsc or {}

    if client.get("ga4_property"):
        ga4, err = collect_ga4(client, win["ga4"], min_change)
        if err:
            report["errors"]["GA4"] = err
        report["ga4"] = ga4 or {}
    else:
        report["ga4"] = {"skipped": "No ga4_property configured for this client."}

    report["alerts"] = build_alerts(report)
    report["actions"] = draft_actions(report)
    return report


# ─── Rendering (pure) ─────────────────────────────────────────────────────────

def _fmt_change(v: dict) -> str:
    if not v:
        return "n/a"
    sign = "+" if v["delta"] > 0 else ""
    pct = f" ({sign}{v['pct']}%)" if v.get("pct") is not None else ""
    label = {"up": "up", "down": "down", "flat": "within normal variation"}[v["verdict"]]
    return f"{sign}{v['delta']:g}{pct}, {label}"


def _fmt_range(r: dict) -> str:
    return f"{r['start']} to {r['end']}"


def render_markdown(report: dict) -> str:
    """Client-ready Markdown for one report."""
    c = report["client"]
    win = report["windows"]
    gsc = report.get("gsc") or {}
    ga4 = report.get("ga4") or {}
    lines = [f"# {c['name']}: weekly SEO report", "",
             f"Report date {report['report_date']}. "
             f"Search Console last 28 days: {_fmt_range(win['gsc']['cur28'])} "
             f"(last 7: {_fmt_range(win['gsc']['cur7'])}). "
             f"GA4 last 28 days: {_fmt_range(win['ga4']['cur28'])}.", "",
             "Changes are compared with the period immediately before. A change marked "
             "\"within normal variation\" is too small to tell apart from chance.", ""]

    lines += ["## Alerts", ""]
    if report.get("alerts"):
        lines += [f"- **{a['severity'].upper()}**: {a['text']}" for a in report["alerts"]]
    else:
        lines.append("No alerts this week.")
    lines.append("")

    lines += ["## Search performance (Google Search Console)", ""]
    if gsc.get("totals"):
        t, c7, c28 = gsc["totals"], gsc["compare7"], gsc["compare28"]
        lines += ["| Metric | Last 7 days | Change vs prior 7 | Last 28 days | Change vs prior 28 |",
                  "|---|---|---|---|---|",
                  f"| Clicks | {t['cur7']['clicks']:,} | {_fmt_change(c7['clicks'])} | "
                  f"{t['cur28']['clicks']:,} | {_fmt_change(c28['clicks'])} |",
                  f"| Impressions | {t['cur7']['impressions']:,} | {_fmt_change(c7['impressions'])} | "
                  f"{t['cur28']['impressions']:,} | {_fmt_change(c28['impressions'])} |",
                  f"| CTR | {t['cur7']['ctr']}% | {c7['ctr']['delta']:+} pts | "
                  f"{t['cur28']['ctr']}% | {c28['ctr']['delta']:+} pts |",
                  f"| Avg position | {t['cur7']['position']} | {c7['position']['delta']:+} | "
                  f"{t['cur28']['position']} | {c28['position']['delta']:+} |", "",
                  "Totals come from Google's site-level aggregate, not from adding up queries "
                  "(query rows hide anonymized searches). For average position, a lower number is better.", ""]
    else:
        lines += ["Search Console data is missing for this run. See alerts.", ""]

    lines += ["## Organic traffic by channel (GA4)", ""]
    if ga4.get("skipped"):
        lines += [ga4["skipped"], ""]
    elif ga4.get("channels"):
        lines += ["| Channel | Sessions 28d | Change | Engagement rate | Key events 28d | Sessions 7d change |",
                  "|---|---|---|---|---|---|"]
        for ch in ga4["channels"]:
            s7 = "low volume, not called" if ch["low_volume"] else _fmt_change(ch["sessions7"])
            s28 = _fmt_change(ch["sessions28"]) + (" (low volume)" if ch["low_volume"] else "")
            lines.append(f"| {ch['channel']} | {ch['cur28']['sessions']:,} | {s28} | "
                         f"{ch['cur28']['engagement_rate']}% | {ch['cur28']['key_events']:g} | {s7} |")
        lines += ["", f"Channels under {LOW_VOLUME_SESSIONS} sessions in 28 days are too small to read "
                      "weekly. GA4's AI Assistant channel excludes Google AI Overviews and AI Mode, "
                      "which count as Organic Search.", ""]
    else:
        lines += ["GA4 data is missing for this run. See alerts.", ""]

    movers = gsc.get("movers") or {}
    if movers.get("losers") or movers.get("gainers"):
        lines += ["## Pages that moved (clicks, 28 days)", "",
                  "| Page | Clicks | Change | Position (prev -> now) | Index check |",
                  "|---|---|---|---|---|"]
        for m in movers.get("losers", []) + movers.get("gainers", []):
            insp = m.get("inspection")
            idx = "not checked" if not insp else (
                f"error: {insp['error']}" if insp.get("error")
                else f"{insp.get('verdict')} ({insp.get('coverage_state') or 'n/a'})")
            lines.append(f"| {m['page']} | {m['clicks']['cur']} | {_fmt_change(m['clicks'])} | "
                         f"{m['position_prev'] or '-'} -> {m['position_cur'] or '-'} | {idx} |")
        lines.append("")

    if gsc.get("low_ctr_pages"):
        lines += ["## Page-one pages losing the click", "",
                  "These rank on page one but get well under the usual click rate for their position. "
                  "The fix is the title and meta description, not ranking.", "",
                  "| Page | Position | Impressions | CTR | Typical CTR | Clicks missed (28d, est.) |",
                  "|---|---|---|---|---|---|"]
        lines += [f"| {p['page']} | {p['position']} | {p['impressions']:,} | {p['ctr']}% | "
                  f"~{p['expected_ctr']}% | ~{p['missed_clicks']} |" for p in gsc["low_ctr_pages"]]
        lines.append("")

    if gsc.get("striking_distance"):
        lines += ["## Striking distance (positions 5-20)", "",
                  "| Query | Page | Position | Impressions | Clicks |", "|---|---|---|---|---|"]
        lines += [f"| {q['query']} | {q['page']} | {q['position']} | {q['impressions']:,} | {q['clicks']} |"
                  for q in gsc["striking_distance"]]
        lines.append("")

    bs = gsc.get("brand_split")
    if bs:
        lines += ["## Brand vs non-brand (28 days)", "",
                  f"Brand: {bs['brand']['clicks']:,} clicks / {bs['brand']['impressions']:,} impressions. "
                  f"Non-brand: {bs['non_brand']['clicks']:,} clicks / {bs['non_brand']['impressions']:,} "
                  f"impressions. {bs['note']}", ""]

    if gsc.get("sitemaps") is not None and gsc.get("totals"):
        lines += ["## Sitemaps", ""]
        if gsc["sitemaps"]:
            lines += [f"- {s['path']}: {s['errors']} errors, {s['warnings']} warnings, "
                      f"last submitted {s.get('last_submitted') or 'unknown'}" for s in gsc["sitemaps"]]
        else:
            lines.append("No sitemaps submitted in Search Console.")
        lines.append("")

    lines += ["## Next actions (draft: review before sending)", ""]
    lines += [f"{i}. {a}" for i, a in enumerate(report.get("actions") or [], 1)] or ["Nothing urgent."]
    lines.append("")
    return "\n".join(lines)


def render_summary(reports: list, report_date: str) -> str:
    """One table across all clients, worst first."""
    def rank(r):
        alerts = r.get("alerts", [])
        return (-sum(a["severity"] == "critical" for a in alerts),
                -sum(a["severity"] == "warning" for a in alerts))

    lines = [f"# Weekly SEO summary: {report_date}", "",
             "| Client | Clicks 28d | Change | Organic sessions 28d | Critical | Warnings | Top alert |",
             "|---|---|---|---|---|---|---|"]
    for r in sorted(reports, key=rank):
        gsc = r.get("gsc") or {}
        clicks = gsc.get("compare28", {}).get("clicks")
        organic = next((ch for ch in (r.get("ga4") or {}).get("channels", [])
                        if ch["channel"] == "Organic Search"), None)
        alerts = r.get("alerts", [])
        top = alerts[0]["text"].replace("|", "/") if alerts else "-"
        lines.append(
            f"| {r['client']['name']} | {clicks['cur'] if clicks else 'n/a'} | "
            f"{_fmt_change(clicks) if clicks else 'n/a'} | "
            f"{organic['cur28']['sessions'] if organic else 'n/a'} | "
            f"{sum(a['severity'] == 'critical' for a in alerts)} | "
            f"{sum(a['severity'] == 'warning' for a in alerts)} | {top} |")
    lines.append("")
    return "\n".join(lines)


# ─── Output ───────────────────────────────────────────────────────────────────

def write_report(report: dict, out_dir: Path, pdf: bool) -> dict:
    """Write weekly.json + weekly.md (and optionally a PDF) for one client."""
    folder = out_dir / report["client"]["slug"] / report["report_date"]
    folder.mkdir(parents=True, exist_ok=True)
    payload = (report.get("gsc") or {}).pop("_pdf_payload", None)
    (folder / "weekly.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    (folder / "weekly.md").write_text(render_markdown(report), encoding="utf-8")
    files = {"json": str(folder / "weekly.json"), "markdown": str(folder / "weekly.md")}

    if pdf and payload:
        import google_report
        domain = re.sub(r"^(sc-domain:|https?://)", "", report["client"]["gsc_property"]).strip("/")
        res = google_report.generate_report("gsc-performance", payload, domain, str(folder), "pdf")
        files["pdf"] = res.get("files", [])
        files["pdf_review"] = (res.get("review") or {}).get("status")
        if res.get("error"):
            files["pdf_error"] = res["error"]
    return files


def cmd_run(args) -> int:
    try:
        clients = load_clients(args.clients)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    if args.client:
        wanted = set(args.client)
        missing = wanted - {c["slug"] for c in clients}
        if missing:
            print(f"Error: unknown client slug(s): {', '.join(sorted(missing))}", file=sys.stderr)
            return 1
        clients = [c for c in clients if c["slug"] in wanted]

    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else date.today()
    out_dir = Path(args.out)
    reports, results = [], []
    for client in clients:
        print(f"[{client['slug']}] collecting...", file=sys.stderr)
        report = run_client(client, today, args.min_change, not args.no_inspect)
        files = write_report(report, out_dir, args.pdf)
        reports.append(report)
        results.append({"slug": client["slug"], "files": files,
                        "alerts": len(report["alerts"]), "errors": report["errors"]})

    summary_path = out_dir / f"summary-{today.isoformat()}.md"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(render_summary(reports, today.isoformat()), encoding="utf-8")

    output = {"report_date": today.isoformat(), "summary": str(summary_path), "clients": results}
    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"Summary: {summary_path}")
        for r in results:
            flag = " (DATA MISSING)" if r["errors"] else ""
            print(f"  {r['slug']}: {r['files']['markdown']} ({r['alerts']} alerts){flag}")
    # Exit 2 lets a scheduler notice a client whose data could not be pulled.
    return 2 if any(r["errors"] for r in results) else 0


def cmd_render(args) -> int:
    try:
        with open(args.report_json, "r", encoding="utf-8") as f:
            report = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading report: {e}", file=sys.stderr)
        return 1
    print(render_markdown(report))
    return 0


def cmd_validate(args) -> int:
    try:
        clients = load_clients(args.clients)
    except ValueError as e:
        print(json.dumps({"valid": False, "error": str(e)}) if args.json else f"Invalid: {e}")
        return 1
    slugs = [c["slug"] for c in clients]
    print(json.dumps({"valid": True, "clients": slugs}) if args.json
          else f"Valid: {len(slugs)} client(s): {', '.join(slugs)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Weekly multi-client SEO report runner")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Pull data and write reports for all (or selected) clients")
    run.add_argument("--clients", default=DEFAULT_CLIENTS_PATH, help="Clients JSON file")
    run.add_argument("--client", action="append", help="Only this client slug (repeatable)")
    run.add_argument("--out", default=DEFAULT_OUT_DIR, help=f"Output directory (default: {DEFAULT_OUT_DIR})")
    run.add_argument("--today", help="Report date YYYY-MM-DD (default: today)")
    run.add_argument("--min-change", type=int, default=5,
                     help="Smallest absolute change ever called up/down (default: 5)")
    run.add_argument("--no-inspect", action="store_true", help="Skip URL Inspection of losing pages")
    run.add_argument("--pdf", action="store_true", help="Also render a PDF via google_report.py")
    run.add_argument("--json", "-j", action="store_true", help="Output run metadata as JSON")
    run.set_defaults(func=cmd_run)

    render = sub.add_parser("render", help="Re-render Markdown from a saved weekly.json")
    render.add_argument("report_json")
    render.set_defaults(func=cmd_render)

    val = sub.add_parser("validate", help="Validate a clients file without calling any API")
    val.add_argument("--clients", default=DEFAULT_CLIENTS_PATH)
    val.add_argument("--json", "-j", action="store_true")
    val.set_defaults(func=cmd_validate)

    args = parser.parse_args()
    if getattr(args, "today", None):
        try:
            datetime.strptime(args.today, "%Y-%m-%d")
        except ValueError:
            parser.error("--today must be YYYY-MM-DD")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
