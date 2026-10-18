#!/usr/bin/env python3
"""
Pre-review gate for AI-drafted content.

Runs every automated check on a draft *before* a human editor sees it,
so editor time goes to judgment instead of proofreading. Nothing here
publishes anything: the output is a cleaned copy of the draft plus a
review sheet the editor signs off on.

Checks
======
Blocking (draft goes back to the generator, not to the editor):
  - Unfilled ``[[TODO: …]]`` markers. Drafts are instructed to leave
    these wherever they need a fact the facts sheet does not supply.
  - Prices or phone numbers that do not appear in the client facts
    sheet (``--facts``). Catches invented or stale client details.
  - Near-duplicate of an existing page in ``--corpus`` (5-word shingle
    containment). Catches templated drafts reused across clients.

Warnings (editor must look closely):
  - ``content_quality.analyse`` overall score below ``--min-quality``.
  - ``content_verify.verify`` uncited-claim ratio above ``--max-uncited``.
  - Opening paragraph is not answer-first (too long, or missing the
    target ``--keyword``).

``content_humanize.humanize`` runs first. The quality score uses the
original draft (so auto-replacement does not hide how generic it was);
every other check uses the cleaned text. Replacements are listed in the
review sheet because a 1:1 swap can break grammar ("a important").

Usage::

    python scripts/content_gate.py drafts/teeth-whitening.md \\
        --facts clients/acme-dental/facts.md \\
        --corpus clients/ \\
        --keyword "teeth whitening cost" \\
        --out-dir clients/acme-dental/review

Writes ``<stem>.cleaned.md`` and ``<stem>.review.md`` to ``--out-dir``
(default: the draft's directory). Exit code 0 = ready for human
review, 1 = blocked.

Output JSON (``--json``)::

    {
      "status": "READY|READY_WITH_WARNINGS|BLOCKED",
      "blocking": ["…"], "warnings": ["…"],
      "todo_markers": [...], "unknown_prices": [...],
      "unknown_phones": [...], "similarity": {"max": 0..1, "file": …},
      "answer_first": {...}, "quality": {...}, "claims": {...},
      "humanize_changes": int,
      "cleaned_path": "…", "review_path": "…"
    }
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content_humanize import humanize  # noqa: E402
from content_quality import analyse  # noqa: E402
from content_verify import verify  # noqa: E402


TODO_RE = re.compile(r"\[\[\s*TODO\b[^\]]*\]\]", re.IGNORECASE)
PRICE_RE = re.compile(
    r"[$€£₹]\s?\d[\d,]*(?:\.\d+)?"
    r"|\b\d[\d,]*(?:\.\d+)?\s?(?:USD|EUR|GBP|INR|AUD|CAD|Rs\.?)(?![A-Za-z])",
    re.IGNORECASE,
)
PHONE_RE = re.compile(r"\+?\(?\d[\d\s().-]{8,}\d")
CORPUS_SUFFIXES = {".md", ".markdown", ".txt", ".html", ".htm"}
GATE_SUFFIXES = (".cleaned.md", ".review.md")
SHINGLE_SIZE = 5
ANSWER_FIRST_MAX_WORDS = 80

HUMAN_CHECKLIST = (
    "Every statistic and claim has a source I opened and read myself",
    "Contains at least one thing only we or the client could say "
    "(real case, number, photo, opinion)",
    "Answers the target question in the first 2-3 sentences",
    "Nothing is wrong for this client: prices, services, location, regulations",
    "Reads in the client's voice, not generic AI",
    "Not a near-copy of anything written for another client",
)


def _normalise_price(raw: str) -> str:
    return re.sub(r"[\s,]", "", raw).upper().replace("RS.", "RS")


def _digits(raw: str) -> str:
    return re.sub(r"\D", "", raw)


def _phones(text: str) -> set[str]:
    return {d for d in (_digits(m) for m in PHONE_RE.findall(text)) if 10 <= len(d) <= 15}


def _tokens(text: str) -> list[str]:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    return re.findall(r"\w+", text.lower())


def _shingles(text: str) -> set[tuple[str, ...]]:
    toks = _tokens(text)
    return {tuple(toks[i:i + SHINGLE_SIZE]) for i in range(len(toks) - SHINGLE_SIZE + 1)}


def check_client_facts(text: str, facts: str) -> dict:
    """Prices and phone numbers in the draft that the facts sheet lacks."""
    known_prices = {_normalise_price(p) for p in PRICE_RE.findall(facts)}
    known_phones = _phones(facts)
    prices = sorted({p.strip() for p in PRICE_RE.findall(text)
                     if _normalise_price(p) not in known_prices})
    phones = sorted(_phones(text) - known_phones)
    return {"unknown_prices": prices, "unknown_phones": phones}


def check_similarity(text: str, corpus: list[Path], exclude: set[Path]) -> dict:
    """Highest share of the draft's 5-word shingles found in one corpus file."""
    draft = _shingles(text)
    best = {"max": 0.0, "file": None}
    if not draft:
        return best
    for root in corpus:
        files = [root] if root.is_file() else sorted(root.rglob("*"))
        for path in files:
            if (not path.is_file() or path.suffix.lower() not in CORPUS_SUFFIXES
                    or path.name.endswith(GATE_SUFFIXES)
                    or path.resolve() in exclude):
                continue
            other = _shingles(path.read_text(encoding="utf-8", errors="replace"))
            score = len(draft & other) / len(draft)
            if score > best["max"]:
                best = {"max": round(score, 3), "file": str(path)}
    return best


def check_answer_first(text: str, keyword: str | None) -> dict:
    """The first body paragraph should answer the query quickly."""
    body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)
    paragraph = ""
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if block and not block.startswith(("#", "<!--", "![", "```")):
            paragraph = block
            break
    words = len(paragraph.split())
    has_keyword = keyword is None or keyword.lower() in paragraph.lower()
    return {
        "words": words,
        "has_keyword": has_keyword,
        "ok": 0 < words <= ANSWER_FIRST_MAX_WORDS and has_keyword,
    }


def run_gate(text: str, facts: str | None = None, corpus: list[Path] | None = None,
             exclude: set[Path] | None = None, keyword: str | None = None,
             min_quality: int = 60, max_uncited: float = 0.2,
             max_similarity: float = 0.3) -> dict:
    """Run every check on ``text``; return the result dict and cleaned text."""
    cleaned = humanize(text)
    body = cleaned["cleaned"]

    todos = TODO_RE.findall(body)
    facts_result = check_client_facts(body, facts) if facts is not None \
        else {"unknown_prices": [], "unknown_phones": []}
    similarity = check_similarity(body, corpus or [], exclude or set())
    answer = check_answer_first(body, keyword)
    quality = analyse(text)
    claims = verify(body)

    blocking: list[str] = []
    if todos:
        blocking.append(f"{len(todos)} unfilled [[TODO]] marker(s)")
    if facts_result["unknown_prices"]:
        blocking.append("price(s) not in facts sheet: "
                        + ", ".join(facts_result["unknown_prices"]))
    if facts_result["unknown_phones"]:
        blocking.append("phone number(s) not in facts sheet: "
                        + ", ".join(facts_result["unknown_phones"]))
    if similarity["max"] > max_similarity:
        blocking.append(f"{similarity['max']:.0%} overlap with {similarity['file']}")

    warnings: list[str] = []
    if quality["overall_quality"] < min_quality:
        warnings.append(f"quality score {quality['overall_quality']} < {min_quality} "
                        f"({', '.join(quality['flags']) or 'no flags'})")
    if claims["uncited_ratio"] > max_uncited:
        warnings.append(f"{claims['uncited_count']} of {claims['claim_count']} "
                        f"claims have no citation")
    if not answer["ok"]:
        reason = "missing target keyword" if not answer["has_keyword"] \
            else f"{answer['words']} words (max {ANSWER_FIRST_MAX_WORDS})"
        warnings.append(f"opening paragraph is not answer-first: {reason}")

    status = "BLOCKED" if blocking else \
        "READY_WITH_WARNINGS" if warnings else "READY"
    return {
        "status": status,
        "blocking": blocking,
        "warnings": warnings,
        "todo_markers": todos,
        **facts_result,
        "similarity": similarity,
        "answer_first": answer,
        "quality": {k: quality[k] for k in
                    ("overall_quality", "filler_score", "ai_pattern_score",
                     "information_density", "flags")},
        "claims": {
            "claim_count": claims["claim_count"],
            "uncited_count": claims["uncited_count"],
            "uncited_ratio": claims["uncited_ratio"],
            "uncited": [c["text"] for c in claims["claims"] if not c["has_citation"]],
        },
        "humanize_changes": cleaned["change_count"],
        "humanize_log": [f"{c['from']} -> {c['to']}" for c in cleaned["changes"]],
    }, body


def render_review_sheet(result: dict, draft_name: str) -> str:
    """Markdown review sheet: automated findings + the editor's checklist."""
    lines = [f"# Review: {draft_name}", "", f"**Gate status:** {result['status']}", ""]
    if result["blocking"]:
        lines += ["## Blocking (send back to the generator)", ""]
        lines += [f"- {b}" for b in result["blocking"]] + [""]
    if result["warnings"]:
        lines += ["## Warnings (check closely)", ""]
        lines += [f"- {w}" for w in result["warnings"]] + [""]
    if result["claims"]["uncited"]:
        lines += ["## Claims to verify or cite", ""]
        lines += [f"- [ ] {c}" for c in result["claims"]["uncited"]] + [""]
    q = result["quality"]
    lines += [
        "## Automated scores", "",
        f"- Quality: {q['overall_quality']}/100 (filler {q['filler_score']}, "
        f"AI patterns {q['ai_pattern_score']})",
        f"- Claims: {result['claims']['claim_count']} found, "
        f"{result['claims']['uncited_count']} uncited",
        f"- Max overlap with existing pages: {result['similarity']['max']:.0%}"
        + (f" ({result['similarity']['file']})" if result["similarity"]["file"] else ""),
        f"- AI phrasings auto-replaced: {result['humanize_changes']}",
        "",
    ]
    if result["humanize_log"]:
        lines += ["## Auto-replacements (re-read these sentences for grammar)", ""]
        lines += [f"- {c}" for c in result["humanize_log"]] + [""]
    lines += ["## Editor checklist", ""]
    lines += [f"- [ ] {item}" for item in HUMAN_CHECKLIST]
    lines += ["", "## Sign-off", "", "Reviewed by: ________  Date: ________  "
              "Approved to publish: yes / no", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pre-review gate for AI-drafted content (never publishes)."
    )
    parser.add_argument("draft", help="Path to the draft (markdown or HTML).")
    parser.add_argument("--facts", help="Client facts sheet (prices, phones, services).")
    parser.add_argument("--corpus", nargs="*", default=[],
                        help="Files/dirs of existing pages to check overlap against.")
    parser.add_argument("--keyword", help="Target query the opening should answer.")
    parser.add_argument("--out-dir", help="Where to write .cleaned.md and .review.md.")
    parser.add_argument("--min-quality", type=int, default=60)
    parser.add_argument("--max-uncited", type=float, default=0.2)
    parser.add_argument("--max-similarity", type=float, default=0.3)
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout.")
    args = parser.parse_args()

    draft = Path(args.draft)
    text = draft.read_text(encoding="utf-8", errors="replace")
    facts = Path(args.facts).read_text(encoding="utf-8", errors="replace") \
        if args.facts else None
    out_dir = Path(args.out_dir) if args.out_dir else draft.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    cleaned_path = out_dir / f"{draft.stem}.cleaned.md"
    review_path = out_dir / f"{draft.stem}.review.md"

    result, cleaned = run_gate(
        text, facts=facts, corpus=[Path(c) for c in args.corpus],
        exclude={draft.resolve(), cleaned_path.resolve()}, keyword=args.keyword,
        min_quality=args.min_quality, max_uncited=args.max_uncited,
        max_similarity=args.max_similarity,
    )
    cleaned_path.write_text(cleaned, encoding="utf-8")
    review_path.write_text(render_review_sheet(result, draft.name), encoding="utf-8")
    result["cleaned_path"] = str(cleaned_path)
    result["review_path"] = str(review_path)

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"Status: {result['status']}")
        for b in result["blocking"]:
            print(f"  BLOCK: {b}")
        for w in result["warnings"]:
            print(f"  WARN:  {w}")
        print(f"Review sheet: {review_path}")

    return 1 if result["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    sys.exit(main())
