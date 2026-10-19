#!/usr/bin/env bash
set -euo pipefail
SKILLS_ROOT="${HOME}/.claude/skills"
for name in \
  aeo-answer-engine-optimizer competitor-pages-seo content-cannibalization-detector \
  core-web-vitals-optimizer dataforseo ecommerce-seo geo gsc-data-interpreter \
  hreflang-seo images-seo internal-linking-strategist keyword-clustering-intent-mapper \
  keyword-optimization-seo link-building-strategist local-seo-playbook-generator \
  maps-seo page-seo programmatic-seo readability-seo-scorer schema-tag-generator \
  seo-content-brief-generator seo-monthly-report-generator sitemap-seo sxo-seo \
  technical-seo-auditor topical-authority-planner; do
  [ -d "${SKILLS_ROOT}/${name}" ] && rm -rf "${SKILLS_ROOT}/${name}" && echo "✓ Removed ${SKILLS_ROOT}/${name}"
done
EXT_DIR="${SKILLS_ROOT}/seo/extensions/seo-skills-pack"
[ -d "${EXT_DIR}" ] && rm -rf "${EXT_DIR}" && echo "✓ Removed ${EXT_DIR}"
exit 0
