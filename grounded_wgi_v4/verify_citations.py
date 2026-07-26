#!/usr/bin/env python3
"""Stage 3 of the AR7 WGI v4 source-first pipeline: verify citations against the DB.

Extracts every in-text (Author, Year) citation from a generated chapter/section
and checks it against the verified sources.db built in Stage 1, matching on
(first-author surname, year). Any citation with no matching verified source is
flagged as UNVERIFIABLE — in a correct source-first run this list should be empty.

Also checks the chapter's "## References" entries resolve to real DOIs in the DB.

Stdlib only. No network needed (reads the local sources.db). Exit code 1 if any
unverifiable citation is found, so it can gate a build.

Usage:
    python verify_citations.py --db sources.db drafts_v4/chapter_02*.md
"""
import argparse
import re
import sqlite3
import sys
from pathlib import Path

YEAR = r"(?:19|20)\d{2}"
INTEXT = re.compile(r"\(([A-Z][^()]*?\b" + YEAR + r"[a-z]?)\)")
# Narrative form: "Author (Year)", "Author et al. (Year)", "Author and Other (Year)".
# The post-surname group is optional so "et al." with no trailing name still matches.
NARR = re.compile(
    r"\b([A-Z][A-Za-zÀ-ÿ'\-]+)"
    r"(?:\s+et al\.|\s+and\s+[A-Z][A-Za-zÀ-ÿ'\-]+|\s*&\s*[A-Z][A-Za-zÀ-ÿ'\-]+)?"
    r"\s*\((" + YEAR + r")")
DOI = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
INSTITUTIONAL = {"ipcc", "wmo", "noaa", "copernicus", "unep", "gcos", "imbie", "nasa"}


def load_keys(db_path):
    db = sqlite3.connect(db_path)
    keys, dois = set(), set()
    for surname, year, doi in db.execute("SELECT first_author, year, doi FROM sources"):
        sn = (surname or "").split()[-1].lower() if surname else ""
        if sn:
            keys.add((sn, str(year)))
        dois.add((doi or "").lower())
    return keys, dois


def first_surname(frag):
    frag = frag.strip().lstrip("eg.,;: ")
    m = re.match(r"([A-Z][A-Za-zÀ-ÿ'\-]+)", frag)
    return m.group(1).lower() if m else None


def cites(body):
    out = set()
    for m in INTEXT.finditer(body):
        sn = first_surname(m.group(1))
        for y in re.findall(YEAR, m.group(1)):
            if sn:
                out.add((sn, y))
    for m in NARR.finditer(body):
        sn = first_surname(m.group(1))
        if sn:
            out.add((sn, m.group(2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(Path(__file__).with_name("sources.db")))
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()

    keys, dois = load_keys(args.db)
    total_bad = 0
    for fp in args.files:
        t = Path(fp).read_text()
        body = t.split("## References", 1)[0]
        unver = sorted(
            (sn, y) for (sn, y) in cites(body)
            if sn not in INSTITUTIONAL and (sn, y) not in keys)
        ref_dois = set(d.lower() for d in DOI.findall(t))
        bad_dois = sorted(d for d in ref_dois if d not in dois)
        total_bad += len(unver)
        print(f"\n=== {Path(fp).name} ===  unverifiable_cites={len(unver)} "
              f"refs_with_unknown_doi={len(bad_dois)}")
        for sn, y in unver:
            print(f"  UNVERIFIABLE: {sn.capitalize()} {y} (no matching source in DB)")
        for d in bad_dois:
            print(f"  DOI not in DB: {d}")
    print(f"\nTOTAL unverifiable in-text citations: {total_bad}")
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main())
