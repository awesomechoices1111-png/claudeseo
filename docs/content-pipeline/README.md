# Content Pipeline: AI Drafts, Human Approval

A repeatable workflow for producing client content with AI while a human editor
approves everything before it goes live. AI does the research, drafting, and
mechanical checks; the editor does judgment, first-hand detail, and sign-off.

**Nothing in this pipeline publishes automatically.** The last automated step
produces a review sheet. Publishing is a manual action by the editor.

## Where client data lives

Keep client work **outside this repository** (it is a public project):

```
~/seo-clients/
  acme-dental/
    facts.md          # from templates/client-facts.md (filled at onboarding)
    briefs/           # one brief per article
    drafts/           # AI drafts
    review/           # gate output: .cleaned.md + .review.md
    published/        # final approved copy (used for overlap checks)
    edit-log.md       # from templates/edit-log.md
```

## The six steps

| # | Step | Who | Time |
|---|------|-----|------|
| 1 | Facts sheet | Editor + client, once at onboarding | 30-45 min |
| 2 | Brief | AI drafts, editor approves the angle | 2-5 min |
| 3 | Draft | AI, following `templates/draft-instructions.md` | automatic |
| 4 | Gate | `content_gate.py` | automatic |
| 5 | Edit + sign-off | Editor, using the generated review sheet | 20-30 min |
| 6 | Publish + track | Editor publishes; tracking runs after | 2 min |

### 1. Facts sheet

Copy `templates/client-facts.md` to the client folder and fill it with the
client. This is the single biggest lever on draft accuracy: the draft
instructions forbid stating any client detail that is not on this sheet.

### 2. Brief

```
/seo content-brief "<target query>"
```

Save the result to `briefs/<slug>.md` using `templates/brief.md` as the shape.
Approve or change the angle before drafting. A wrong angle wastes the whole
review.

### 3. Draft

Ask Claude to write the article from the brief, with the facts sheet and
`templates/draft-instructions.md` attached. Save to `drafts/<slug>.md`.

### 4. Gate

```bash
claude-seo run content_gate.py ~/seo-clients/acme-dental/drafts/<slug>.md \
  --facts   ~/seo-clients/acme-dental/facts.md \
  --corpus  ~/seo-clients \
  --keyword "<target query>" \
  --out-dir ~/seo-clients/acme-dental/review
```

| Result | Meaning | Next |
|--------|---------|------|
| `BLOCKED` (exit 1) | Unfilled `[[TODO]]`, a price/phone not in the facts sheet, or >30% overlap with an existing page (any client) | Fix the facts sheet or regenerate. Do not spend editor time yet. |
| `READY_WITH_WARNINGS` | Low quality score, uncited claims, or the opening does not answer the query | Editor reviews, focusing on the listed warnings |
| `READY` | All automated checks passed | Editor reviews normally |

`READY` means "worth a human's time", not "safe to publish". The gate cannot
tell whether a claim is true, only whether it is cited.

A `[[TODO]]` usually means the facts sheet is missing something. Add it there
so the next draft does not ask again.

### 5. Edit + sign-off

Open `review/<slug>.review.md`. It lists the uncited claims to check, the
automated scores, and the editor checklist. Edit `review/<slug>.cleaned.md`,
tick every checklist item, and fill in the sign-off line. If any item cannot be
ticked, the article does not ship.

Log what you changed in `edit-log.md`. After a few weeks, recurring fixes show
which instructions or facts-sheet fields to improve.

### 6. Publish + track

Publish manually in the CMS, then copy the final text to `published/<slug>.md`
so future drafts are checked for overlap against it. Optional follow-ups:

```bash
# Notify Bing/Yandex/etc. (Google does not use IndexNow)
claude-seo run indexnow_submit.py --host example.com --key ... \
  --key-location https://example.com/<key>.txt --urls https://example.com/<slug>

# Record a baseline so later regressions are caught
claude-seo run drift_baseline.py https://example.com/<slug>
```

## Capacity planning

Editor review, not generation, is the limit. At ~25 minutes per article plus
technical work, plan for about 8-12 retainer clients at 4 articles per month.
To grow beyond that, raise prices or hire an editor; do not shorten review.

## Tuning the gate

| Flag | Default | Raise it when | Lower it when |
|------|---------|---------------|---------------|
| `--min-quality` | 60 | Client is YMYL (medical, legal, finance) | Short service pages score low on density |
| `--max-uncited` | 0.2 | Never for YMYL | Opinion pieces with few factual claims |
| `--max-similarity` | 0.3 | (rarely) | Several clients share a legally required disclaimer |
