# SEO Skills Pack (third-party bundle)

26 standalone Claude skills from the free BuildWire AI "SEO Skills Pack"
(https://buildwire.ai/claude-skills/seo-skills-pack/), kept together in one
extension so they can be reviewed, updated, or removed as a unit.

## Install / uninstall

- `install.sh` / `install.ps1` at the repo root copy every folder in
  `skills/` here to `~/.claude/skills/<name>/` and the helper scripts to
  `~/.claude/skills/seo/extensions/seo-skills-pack/scripts/`.
- `./uninstall.sh` in this folder removes all 26 skills.
- Plugin installs (`/plugin install`) only auto-discover the core `skills/`
  directory, so this bundle needs the script installer.

## Scripts

| Script | Used by | Run |
|--------|---------|-----|
| `nap_checker.py` | local-seo-playbook-generator | `claude-seo run --extension seo-skills-pack nap_checker.py --demo` |
| `brief_validator.py` | seo-content-brief-generator | `claude-seo run --extension seo-skills-pack brief_validator.py --demo` |
| `brief_formatter.py` | seo-content-brief-generator | `claude-seo run --extension seo-skills-pack brief_formatter.py --demo` |

The scripts work offline and make no network requests.

## Provenance and overlap

These 11 skills are lightly modified copies of this repository's own
claude-seo skills (MIT, Copyright (c) 2026 agricidaniel). They overlap the
core skills and can trigger on the same requests:

| Pack skill | Core skill |
|------------|------------|
| geo | seo-geo |
| ecommerce-seo | seo-ecommerce |
| images-seo | seo-images |
| sxo-seo | seo-sxo |
| maps-seo | seo-maps |
| hreflang-seo | seo-hreflang |
| sitemap-seo | seo-sitemap |
| programmatic-seo | seo-programmatic |
| competitor-pages-seo | seo-competitor-pages |
| page-seo | seo-page |
| dataforseo | seo-dataforseo |

The other 15 are original to the pack. Files are unmodified except that
the three scripts were moved to `scripts/` and the `nap_checker.py`
invocation now uses `claude-seo run`.
