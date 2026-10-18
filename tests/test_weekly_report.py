"""Tests for scripts/weekly_report.py: config validation, noise test, findings,
and an end-to-end run with the Google API layer mocked out."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import weekly_report as wr  # noqa: E402


def _write_clients(tmp_path, clients):
    path = tmp_path / "clients.json"
    path.write_text(json.dumps({"clients": clients}), encoding="utf-8")
    return str(path)


def test_load_clients_valid_and_defaults(tmp_path):
    path = _write_clients(tmp_path, [{"slug": "acme", "gsc_property": "sc-domain:acme.com"}])
    clients = wr.load_clients(path)
    assert clients[0]["name"] == "acme"


@pytest.mark.parametrize("client,msg", [
    ({"slug": "Acme Co", "gsc_property": "sc-domain:acme.com"}, "kebab-case"),
    ({"slug": "acme", "gsc_property": "acme.com"}, "gsc_property"),
    ({"slug": "acme", "gsc_property": "sc-domain:acme.com", "ga4_property": "G-123"}, "ga4_property"),
    ({"slug": "acme", "gsc_property": "sc-domain:acme.com", "brand_terms": [""]}, "brand_terms"),
    ({"slug": "acme", "gsc_property": "sc-domain:acme.com", "inspect_limit": 500}, "inspect_limit"),
])
def test_load_clients_rejects_bad_config(tmp_path, client, msg):
    with pytest.raises(ValueError, match=msg):
        wr.load_clients(_write_clients(tmp_path, [client]))


def test_load_clients_rejects_duplicate_slugs(tmp_path):
    c = {"slug": "acme", "gsc_property": "sc-domain:acme.com"}
    with pytest.raises(ValueError, match="Duplicate"):
        wr.load_clients(_write_clients(tmp_path, [c, dict(c)]))


def test_windows_respect_api_lag_and_do_not_overlap():
    win = wr.compute_windows(date(2026, 10, 19))  # a Monday
    assert win["ga4"]["cur7"] == {"start": "2026-10-12", "end": "2026-10-18"}
    assert win["ga4"]["prev7"] == {"start": "2026-10-05", "end": "2026-10-11"}
    assert win["gsc"]["cur28"]["end"] == "2026-10-16"
    assert win["gsc"]["prev28"]["end"] == "2026-09-18"
    assert win["gsc"]["cur28"]["start"] == "2026-09-19"


def test_change_verdict_treats_small_site_swings_as_noise():
    # 8 -> 6 sessions is noise, not a decline.
    assert wr.change_verdict(6, 8)["verdict"] == "flat"
    # 40 -> 20 clears 2*sqrt(60) ~= 15.5.
    assert wr.change_verdict(20, 40)["verdict"] == "down"
    assert wr.change_verdict(1200, 1000)["verdict"] == "up"
    assert wr.change_verdict(0, 0) == {"cur": 0, "prev": 0, "delta": 0, "pct": None, "verdict": "flat"}


def test_low_ctr_pages_excludes_pages_beyond_page_one():
    rows = [
        {"page": "/deep", "position": 22.3, "impressions": 289, "clicks": 0, "ctr": 0.0},
        {"page": "/p1", "position": 3.0, "impressions": 1000, "clicks": 10, "ctr": 1.0},
        {"page": "/fine", "position": 3.0, "impressions": 1000, "clicks": 90, "ctr": 9.0},
    ]
    flagged = wr.low_ctr_pages(rows)
    assert [p["page"] for p in flagged] == ["/p1"]
    assert flagged[0]["missed_clicks"] == 80


def test_striking_distance_and_brand_split():
    rows = [
        {"query": "acme pricing", "page": "/pricing", "position": 6, "impressions": 300, "clicks": 9},
        {"query": "best widgets", "page": "/widgets", "position": 12, "impressions": 500, "clicks": 2},
        {"query": "widgets", "page": "/widgets", "position": 45, "impressions": 900, "clicks": 0},
    ]
    sd = wr.striking_distance(rows)
    assert [q["query"] for q in sd] == ["best widgets", "acme pricing"]
    split = wr.brand_split(rows, ["Acme"])
    assert split["brand"]["clicks"] == 9 and split["non_brand"]["clicks"] == 2
    assert wr.brand_split(rows, []) is None


def test_page_movers_only_reports_changes_beyond_noise():
    cur = [{"page": "/a", "clicks": 10}, {"page": "/b", "clicks": 101}, {"page": "/c", "clicks": 200}]
    prev = [{"page": "/a", "clicks": 100}, {"page": "/b", "clicks": 99}]
    movers = wr.page_movers(cur, prev)
    assert [m["page"] for m in movers["losers"]] == ["/a"]
    assert [m["page"] for m in movers["gainers"]] == ["/c"]


def _fake_gsc_module():
    def query(prop, start, end, dimensions=None, row_limit=1000, **_):
        if dimensions == []:
            clicks = 100 if start >= "2026-09-19" else 200
            return {"totals": {"clicks": clicks, "impressions": clicks * 50, "ctr": 2.0, "position": 9.1},
                    "warnings": [], "error": None}
        if dimensions == ["page"]:
            if start >= "2026-09-19":
                rows = [{"page": "https://acme.com/a", "clicks": 5, "impressions": 900,
                         "ctr": 0.5, "position": 4.0}]
            else:
                rows = [{"page": "https://acme.com/a", "clicks": 90, "impressions": 900,
                         "ctr": 10.0, "position": 2.0}]
            return {"rows": rows, "error": None}
        return {"rows": [{"query": "acme a", "page": "https://acme.com/a", "clicks": 5,
                          "impressions": 400, "ctr": 1.25, "position": 7.0}], "error": None}

    return mock.Mock(
        query_search_analytics=query,
        list_sitemaps=lambda prop: {"sitemaps": [{"path": "https://acme.com/sitemap.xml",
                                                  "errors": 2, "warnings": 0}], "error": None},
    )


def _fake_inspect_module():
    return mock.Mock(inspect_url=lambda url, prop: {
        "verdict": "FAIL", "index_status": {"coverage_state": "Crawled - currently not indexed"},
        "canonical": {"match": None}, "error": None})


def test_end_to_end_run_with_mocked_apis(tmp_path, capsys):
    clients = _write_clients(tmp_path, [
        {"slug": "acme", "name": "Acme", "gsc_property": "sc-domain:acme.com", "brand_terms": ["acme"]},
    ])
    out = tmp_path / "out"
    with mock.patch.dict(sys.modules, {"gsc_query": _fake_gsc_module(),
                                       "gsc_inspect": _fake_inspect_module()}):
        with mock.patch.object(sys, "argv", ["weekly_report.py", "run", "--clients", clients,
                                             "--out", str(out), "--today", "2026-10-19", "--json"]):
            code = wr.main()
    assert code == 0
    meta = json.loads(capsys.readouterr().out)
    report = json.loads(Path(meta["clients"][0]["files"]["json"]).read_text())
    assert "_pdf_payload" not in report["gsc"]
    assert report["gsc"]["compare28"]["clicks"]["verdict"] == "down"
    texts = [a["text"] for a in report["alerts"]]
    assert any("not indexed" in t for t in texts)
    assert any("2 error(s)" in t for t in texts)
    assert report["alerts"][0]["severity"] == "critical"
    md = Path(meta["clients"][0]["files"]["markdown"]).read_text()
    assert "# Acme: weekly SEO report" in md
    assert "No ga4_property configured" in md
    assert "Crawled - currently not indexed" in md
    summary = Path(meta["summary"]).read_text()
    assert "| Acme | 100 |" in summary


def test_missing_gsc_data_is_reported_not_skipped(tmp_path, capsys):
    clients = _write_clients(tmp_path, [{"slug": "acme", "gsc_property": "sc-domain:acme.com"}])
    broken = mock.Mock(query_search_analytics=lambda *a, **k: {"error": "Permission denied"})
    with mock.patch.dict(sys.modules, {"gsc_query": broken}):
        with mock.patch.object(sys, "argv", ["weekly_report.py", "run", "--clients", clients,
                                             "--out", str(tmp_path / "o"), "--today", "2026-10-19"]):
            code = wr.main()
    assert code == 2
    md = next((tmp_path / "o").rglob("weekly.md")).read_text()
    assert "Search Console data missing: Permission denied" in md
    assert "Search Console data is missing for this run" in md


def test_render_roundtrip(tmp_path, capsys):
    report = {"client": {"slug": "x", "name": "X"}, "report_date": "2026-10-19",
              "windows": wr.compute_windows(date(2026, 10, 19)), "errors": {},
              "gsc": {}, "ga4": {"skipped": "No ga4_property configured for this client."},
              "alerts": [], "actions": []}
    path = tmp_path / "weekly.json"
    path.write_text(json.dumps(report))
    with mock.patch.object(sys, "argv", ["weekly_report.py", "render", str(path)]):
        assert wr.main() == 0
    assert "No alerts this week." in capsys.readouterr().out


def test_ga4_channels_parse_multi_date_range_response():
    pytest.importorskip("google.analytics.data_v1beta")
    from types import SimpleNamespace as NS

    def row(channel, window, sessions):
        return NS(dimension_values=[NS(value=channel), NS(value=window)],
                  metric_values=[NS(value=str(v)) for v in (sessions, sessions // 2, 0.5, 60.0, 3)])

    resp = NS(dimension_headers=[NS(name="sessionDefaultChannelGroup"), NS(name="dateRange")],
              rows=[row("Organic Search", "cur28", 400), row("Organic Search", "prev28", 300),
                    row("Organic Search", "cur7", 100), row("Organic Search", "prev7", 95),
                    row("AI Assistant", "cur28", 6), row("AI Assistant", "prev28", 8)])
    fake = mock.Mock(_build_ga4_client=lambda: mock.Mock(run_report=lambda req: resp),
                     _resolve_property=lambda p: f"properties/{p}")
    win = wr.compute_windows(date(2026, 10, 19))["ga4"]
    with mock.patch.dict(sys.modules, {"ga4_report": fake}):
        ga4, err = wr.collect_ga4({"ga4_property": "123"}, win, 5)
    assert err is None
    organic, ai = ga4["channels"]
    assert organic["channel"] == "Organic Search"
    assert organic["sessions28"]["verdict"] == "up"
    assert organic["sessions7"]["verdict"] == "flat"
    assert organic["cur28"]["engagement_rate"] == 50.0
    assert ai["low_volume"] is True and ai["sessions28"]["verdict"] == "flat"
