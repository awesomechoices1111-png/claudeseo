"""Tests for scripts/content_gate.py (pre-review gate for AI drafts)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

_SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

import content_gate  # noqa: E402

FACTS = """# Acme Dental facts
Teeth whitening: $350 per session. Call +1 (415) 555-0134.
"""

GOOD_DRAFT = """# How much does teeth whitening cost?

Teeth whitening cost at Acme Dental is $350 per session, and most patients
need one visit. Results last about a year with normal care.

## What affects the price

Our dentist Dr. Lee checks enamel first. Book on +1 (415) 555-0134.
"""


def test_good_draft_is_ready():
    result, _ = content_gate.run_gate(GOOD_DRAFT, facts=FACTS,
                                      keyword="teeth whitening cost")
    assert result["blocking"] == []
    assert result["answer_first"]["ok"]
    assert result["status"] in {"READY", "READY_WITH_WARNINGS"}


def test_todo_marker_blocks():
    draft = GOOD_DRAFT + "\nWe have [[TODO: years in practice]] years of experience.\n"
    result, _ = content_gate.run_gate(draft, facts=FACTS)
    assert result["status"] == "BLOCKED"
    assert result["todo_markers"]


def test_invented_price_and_phone_block():
    draft = GOOD_DRAFT.replace("$350", "$299").replace("555-0134", "555-9999")
    result, _ = content_gate.run_gate(draft, facts=FACTS)
    assert result["unknown_prices"] == ["$299"]
    assert result["unknown_phones"] == ["14155559999"]
    assert result["status"] == "BLOCKED"


def test_price_formats_normalise():
    facts = "Implants from $1,200 or 1200 USD."
    result = content_gate.check_client_facts("Implants cost $1200.", facts)
    assert result["unknown_prices"] == []


def test_near_duplicate_blocks(tmp_path: Path):
    other = tmp_path / "other-client" / "published.md"
    other.parent.mkdir()
    other.write_text(GOOD_DRAFT, encoding="utf-8")
    result, _ = content_gate.run_gate(GOOD_DRAFT, facts=FACTS, corpus=[tmp_path])
    assert result["similarity"]["max"] == 1.0
    assert result["status"] == "BLOCKED"


def test_gate_outputs_are_skipped_in_corpus(tmp_path: Path):
    (tmp_path / "post.review.md").write_text(GOOD_DRAFT, encoding="utf-8")
    result, _ = content_gate.run_gate(GOOD_DRAFT, facts=FACTS, corpus=[tmp_path])
    assert result["similarity"]["max"] == 0.0


def test_quality_scores_original_draft_and_logs_replacements():
    draft = GOOD_DRAFT + "\nIn today's fast-paced world, we delve into the landscape.\n"
    result, cleaned = content_gate.run_gate(draft, facts=FACTS)
    assert "delve" not in cleaned
    assert result["quality"]["ai_pattern_score"] > 0
    assert any("delve" in c for c in result["humanize_log"])
    sheet = content_gate.render_review_sheet(result, "post.md")
    assert "Auto-replacements" in sheet


def test_answer_first_flags_missing_keyword_and_long_intro():
    assert not content_gate.check_answer_first("# T\n\nIntro text.", "cost")["ok"]
    long_intro = "# T\n\n" + "word " * 120
    assert content_gate.check_answer_first(long_intro, None)["words"] == 120
    assert not content_gate.check_answer_first(long_intro, None)["ok"]


def test_answer_first_skips_front_matter():
    text = "---\ntitle: x\n---\n# Cost\n\nThe cost is low.\n"
    assert content_gate.check_answer_first(text, "cost")["ok"]


def test_cli_writes_review_sheet_and_exit_code(tmp_path: Path):
    draft = tmp_path / "post.md"
    draft.write_text(GOOD_DRAFT + "\n[[TODO: add photo]]\n", encoding="utf-8")
    facts = tmp_path / "facts.md"
    facts.write_text(FACTS, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, os.path.join(_SCRIPTS, "content_gate.py"), str(draft),
         "--facts", str(facts), "--corpus", str(tmp_path), "--json"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 1
    result = json.loads(proc.stdout)
    assert result["status"] == "BLOCKED"
    # The draft itself must not count as a duplicate of itself.
    assert result["similarity"]["max"] == 0.0
    sheet = Path(result["review_path"]).read_text(encoding="utf-8")
    assert "Editor checklist" in sheet and "Sign-off" in sheet
    assert Path(result["cleaned_path"]).exists()
