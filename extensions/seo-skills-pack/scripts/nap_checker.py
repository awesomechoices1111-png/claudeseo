#!/usr/bin/env python3
"""
NAP Consistency Checker
-----------------------
Checks a CSV of existing business citations against a canonical NAP record
and reports inconsistencies by severity.

Usage:
  python nap_checker.py --canonical "Business Name|123 Main St|555-0100" --input citations.csv
  python nap_checker.py --demo

CSV format (headers required):
  source, name, address, phone, website

Severity levels:
  CRITICAL  - Name or address mismatch (affects ranking signals directly)
  HIGH      - Phone mismatch or website mismatch
  MEDIUM    - Formatting inconsistency (abbreviations, punctuation)
  OK        - Matches canonical record
"""

import csv
import sys
import re
import argparse


# ---------------------------------------------------------------------------
# Normalisation helpers
# ---------------------------------------------------------------------------

def normalise_name(name: str) -> str:
    """Lowercase, strip extra whitespace."""
    return re.sub(r"\s+", " ", name.strip().lower())


def normalise_phone(phone: str) -> str:
    """Strip all non-digit characters."""
    return re.sub(r"\D", "", phone)


def normalise_address(address: str) -> str:
    """Lowercase, expand common abbreviations, strip punctuation."""
    address = address.strip().lower()
    replacements = {
        r"\bst\b\.?": "street",
        r"\bave?\b\.?": "avenue",
        r"\bblvd\b\.?": "boulevard",
        r"\bdr\b\.?": "drive",
        r"\brd\b\.?": "road",
        r"\bln\b\.?": "lane",
        r"\bct\b\.?": "court",
        r"\bpl\b\.?": "place",
        r"\bste\b\.?": "suite",
        r"\bapt\b\.?": "apartment",
        r"\bfl\b\.?": "floor",
        r"\bn\b\.?": "north",
        r"\bs\b\.?": "south",
        r"\be\b\.?": "east",
        r"\bw\b\.?": "west",
    }
    for pattern, replacement in replacements.items():
        address = re.sub(pattern, replacement, address)
    # Remove punctuation except comma and hyphen
    address = re.sub(r"[^\w\s,\-]", "", address)
    address = re.sub(r"\s+", " ", address)
    return address.strip()


def normalise_url(url: str) -> str:
    """Strip protocol, www, and trailing slash for comparison."""
    url = url.strip().lower()
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"^www\.", "", url)
    url = url.rstrip("/")
    return url


# ---------------------------------------------------------------------------
# Comparison logic
# ---------------------------------------------------------------------------

def check_name(canonical: str, listing: str) -> tuple:
    cn = normalise_name(canonical)
    ln = normalise_name(listing)
    if cn == ln:
        return "OK", None
    # Check if canonical is contained in listing (keyword padding)
    if cn in ln and cn != ln:
        return "MEDIUM", f"Listing name has extra content: '{listing}'"
    return "CRITICAL", f"Name mismatch: expected '{canonical}', found '{listing}'"


def check_phone(canonical: str, listing: str) -> tuple:
    cp = normalise_phone(canonical)
    lp = normalise_phone(listing)
    if not listing.strip():
        return "HIGH", "Phone number missing"
    if cp == lp:
        return "OK", None
    # Check last 10 digits match (ignore country code discrepancy)
    if cp[-10:] == lp[-10:] and len(cp) >= 10:
        return "MEDIUM", f"Phone format inconsistency (country code differs): '{listing}'"
    return "HIGH", f"Phone mismatch: expected '{canonical}', found '{listing}'"


def check_address(canonical: str, listing: str) -> tuple:
    ca = normalise_address(canonical)
    la = normalise_address(listing)
    if not listing.strip():
        return "CRITICAL", "Address missing"
    if ca == la:
        return "OK", None
    # Partial match check
    ca_parts = set(ca.split())
    la_parts = set(la.split())
    overlap = len(ca_parts & la_parts) / max(len(ca_parts), 1)
    if overlap >= 0.8:
        return "MEDIUM", f"Address formatting inconsistency: '{listing}'"
    return "CRITICAL", f"Address mismatch: expected '{canonical}', found '{listing}'"


def check_website(canonical: str, listing: str) -> tuple:
    if not listing.strip():
        return "HIGH", "Website URL missing"
    cu = normalise_url(canonical)
    lu = normalise_url(listing)
    if cu == lu:
        return "OK", None
    # Subdomain or path variation
    if cu in lu or lu in cu:
        return "MEDIUM", f"Website URL variation: '{listing}'"
    return "HIGH", f"Website mismatch: expected '{canonical}', found '{listing}'"


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "OK": 3}
SEVERITY_LABELS = {
    "CRITICAL": "[CRITICAL]",
    "HIGH":     "[HIGH    ]",
    "MEDIUM":   "[MEDIUM  ]",
    "OK":       "[OK      ]",
}


def run_audit(canonical_name, canonical_address, canonical_phone, canonical_website, rows):
    results = []

    for row in rows:
        source = row.get("source", "Unknown").strip()
        listing_name = row.get("name", "").strip()
        listing_address = row.get("address", "").strip()
        listing_phone = row.get("phone", "").strip()
        listing_website = row.get("website", "").strip()

        issues = []

        sev_n, msg_n = check_name(canonical_name, listing_name)
        sev_a, msg_a = check_address(canonical_address, listing_address)
        sev_p, msg_p = check_phone(canonical_phone, listing_phone)

        sev_w, msg_w = ("OK", None)
        if canonical_website:
            sev_w, msg_w = check_website(canonical_website, listing_website)

        for sev, msg in [(sev_n, msg_n), (sev_a, msg_a), (sev_p, msg_p), (sev_w, msg_w)]:
            if msg:
                issues.append((sev, msg))

        worst = min(issues, key=lambda x: SEVERITY_ORDER[x[0]])[0] if issues else "OK"

        results.append({
            "source": source,
            "overall": worst,
            "issues": issues,
        })

    return results


def print_report(results, canonical_name, canonical_address, canonical_phone, canonical_website):
    separator = "=" * 70

    print()
    print(separator)
    print("  NAP CONSISTENCY AUDIT REPORT")
    print(separator)
    print(f"  Canonical Name    : {canonical_name}")
    print(f"  Canonical Address : {canonical_address}")
    print(f"  Canonical Phone   : {canonical_phone}")
    if canonical_website:
        print(f"  Canonical Website : {canonical_website}")
    print(separator)

    total = len(results)
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "OK": 0}
    for r in results:
        counts[r["overall"]] += 1

    print()
    print(f"  Listings audited  : {total}")
    print(f"  CRITICAL issues   : {counts['CRITICAL']}")
    print(f"  HIGH issues       : {counts['HIGH']}")
    print(f"  MEDIUM issues     : {counts['MEDIUM']}")
    print(f"  Fully consistent  : {counts['OK']}")
    print()

    # Sort by severity
    sorted_results = sorted(results, key=lambda x: SEVERITY_ORDER[x["overall"]])

    for r in sorted_results:
        label = SEVERITY_LABELS[r["overall"]]
        print(f"  {label}  {r['source']}")
        if r["issues"]:
            for sev, msg in r["issues"]:
                print(f"             {SEVERITY_LABELS[sev]}  {msg}")
        else:
            print(f"             All fields match canonical record")
        print()

    print(separator)
    print("  RECOMMENDED ACTIONS")
    print(separator)
    if counts["CRITICAL"] > 0:
        print("  IMMEDIATE: Fix CRITICAL mismatches on GBP, website footer,")
        print("             and data aggregators within 1 week.")
    if counts["HIGH"] > 0:
        print("  SHORT TERM: Correct HIGH-severity issues across all platforms")
        print("              within 30 days.")
    if counts["MEDIUM"] > 0:
        print("  ONGOING: Standardise MEDIUM formatting issues as you encounter them.")
    if counts["CRITICAL"] == 0 and counts["HIGH"] == 0 and counts["MEDIUM"] == 0:
        print("  NAP consistency looks good. Schedule a quarterly re-audit.")
    print(separator)
    print()


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------

DEMO_CANONICAL = {
    "name": "Austin Pipe Pros",
    "address": "123 Main Street, Austin, TX 78701",
    "phone": "512-555-0100",
    "website": "https://www.austinpipepros.com",
}

DEMO_ROWS = [
    {"source": "Google Business Profile", "name": "Austin Pipe Pros", "address": "123 Main St, Austin, TX 78701", "phone": "(512) 555-0100", "website": "https://austinpipepros.com"},
    {"source": "Yelp", "name": "Austin Pipe Pros LLC", "address": "123 Main Street, Austin, Texas 78701", "phone": "512-555-0100", "website": "http://www.austinpipepros.com"},
    {"source": "Yellow Pages", "name": "Austin Pipe Pros Plumbing & HVAC", "address": "123 Main St Suite 2, Austin, TX 78701", "phone": "512-555-0100", "website": ""},
    {"source": "Angi", "name": "Austin Pipe Pros", "address": "123 Main Street, Austin, TX 78701", "phone": "512-555-0100", "website": "https://www.austinpipepros.com"},
    {"source": "HomeAdvisor", "name": "Austin Pipe Pros", "address": "456 Oak Ave, Austin, TX 78702", "phone": "512-555-0199", "website": "https://www.austinpipepros.com"},
    {"source": "BBB", "name": "Austin Pipe Pros", "address": "123 Main Street, Austin, TX 78701", "phone": "5125550100", "website": "austinpipepros.com"},
]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="NAP Consistency Checker for Local SEO")
    parser.add_argument("--canonical", help='Canonical NAP as "Name|Address|Phone" (website optional: "Name|Address|Phone|URL")')
    parser.add_argument("--input", help="CSV file with columns: source, name, address, phone, website")
    parser.add_argument("--demo", action="store_true", help="Run with built-in demo data")
    args = parser.parse_args()

    if args.demo:
        c = DEMO_CANONICAL
        rows = DEMO_ROWS
        print("\n  [Demo mode — using sample Austin Pipe Pros data]")
    elif args.canonical and args.input:
        parts = args.canonical.split("|")
        if len(parts) < 3:
            print("ERROR: --canonical requires at least 'Name|Address|Phone'")
            sys.exit(1)
        c = {
            "name": parts[0].strip(),
            "address": parts[1].strip(),
            "phone": parts[2].strip(),
            "website": parts[3].strip() if len(parts) > 3 else "",
        }
        try:
            with open(args.input, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except FileNotFoundError:
            print(f"ERROR: File not found: {args.input}")
            sys.exit(1)
    else:
        parser.print_help()
        print("\nTip: Run with --demo to see an example report.")
        sys.exit(0)

    results = run_audit(c["name"], c["address"], c["phone"], c["website"], rows)
    print_report(results, c["name"], c["address"], c["phone"], c["website"])


if __name__ == "__main__":
    main()
