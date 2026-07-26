#!/usr/bin/env python3
"""Stage 1 of the AR7 WGI v4 source-first pipeline: harvest a VERIFIED source DB.

Queries the OpenAlex works API (free, no key) per chapter using the phrases in
chapter_topics.json, restricted to the post-AR6 window, and writes:

  - sources.db        SQLite: one row per real work (DOI, title, year, authors,
                      venue, abstract, cited_by_count, chapter tags)
  - sources/<chapter>.json   the verified source set handed to the writer agent

Only works with a resolvable DOI are kept, so every entry is a real, locatable
publication. This is the ground-truth substrate that Stage 2 (write_grounded.py)
is allowed to cite from, and Stage 3 (verify_citations.py) checks against.

Network required. Stdlib only (urllib) — no third-party deps, per the repo
supply-chain policy. Run on a networked machine (THINK lane), not the web sandbox.

Usage:
    python harvest_sources.py [--topics chapter_topics.json] [--out-dir .]
                              [--mailto you@example.com] [--sleep 0.2]
"""
import argparse
import json
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

OPENALEX = "https://api.openalex.org/works"


def reconstruct_abstract(inv):
    """OpenAlex returns abstracts as an inverted index {word: [positions]}."""
    if not inv:
        return ""
    positions = {}
    for word, idxs in inv.items():
        for i in idxs:
            positions[i] = word
    return " ".join(positions[i] for i in sorted(positions))[:1500]


def fetch(query, min_year, max_year, per_query, mailto):
    params = {
        "search": query,
        "filter": f"from_publication_date:{min_year}-01-01,"
                  f"to_publication_date:{max_year}-12-31,"
                  "has_doi:true,type:article",
        "sort": "cited_by_count:desc",
        "per-page": str(min(per_query, 200)),
    }
    if mailto:
        params["mailto"] = mailto
    url = f"{OPENALEX}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "ar7-source-first/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r).get("results", [])


def normalize(w):
    doi = (w.get("doi") or "").replace("https://doi.org/", "").lower()
    auths = [a["author"]["display_name"]
             for a in w.get("authorships", []) if a.get("author")]
    venue = ""
    pl = w.get("primary_location") or {}
    src = pl.get("source") or {}
    venue = src.get("display_name") or ""
    return {
        "doi": doi,
        "title": (w.get("title") or "").strip(),
        "year": w.get("publication_year"),
        "authors": auths,
        "first_author": auths[0] if auths else "",
        "venue": venue,
        "cited_by_count": w.get("cited_by_count", 0),
        "abstract": reconstruct_abstract(w.get("abstract_inverted_index")),
        "openalex_id": w.get("id", ""),
    }


def init_db(path):
    db = sqlite3.connect(path)
    db.execute("""CREATE TABLE IF NOT EXISTS sources(
        doi TEXT PRIMARY KEY, title TEXT, year INTEGER, first_author TEXT,
        authors TEXT, venue TEXT, cited_by_count INTEGER, abstract TEXT,
        openalex_id TEXT, chapters TEXT)""")
    return db


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", default=str(Path(__file__).with_name("chapter_topics.json")))
    ap.add_argument("--out-dir", default=str(Path(__file__).parent))
    ap.add_argument("--mailto", default="", help="OpenAlex polite-pool email")
    ap.add_argument("--sleep", type=float, default=0.2)
    args = ap.parse_args()

    cfg = json.load(open(args.topics))
    out = Path(args.out_dir)
    (out / "sources").mkdir(parents=True, exist_ok=True)
    db = init_db(out / "sources.db")

    by_doi = {}
    for chap, spec in cfg["chapters"].items():
        chapter_set = {}
        for q in spec["queries"]:
            try:
                works = fetch(q, cfg["min_year"], cfg["max_year"], cfg["per_query"], args.mailto)
            except Exception as e:
                print(f"  ! {chap}: query {q!r} failed: {e}", file=sys.stderr)
                continue
            for w in works:
                n = normalize(w)
                if not n["doi"] or not n["title"]:
                    continue
                chapter_set[n["doi"]] = n
                rec = by_doi.setdefault(n["doi"], dict(n, chapters=set()))
                rec["chapters"].add(chap)
            time.sleep(args.sleep)
        # per-chapter verified source set for the writer agent
        srcs = sorted(chapter_set.values(), key=lambda x: -x["cited_by_count"])
        json.dump(
            {"chapter": chap, "title": spec["title"], "count": len(srcs), "sources": srcs},
            open(out / "sources" / f"{chap}.json", "w"), indent=2)
        print(f"{chap}: {len(srcs)} verified sources")

    for r in by_doi.values():
        db.execute(
            "INSERT OR REPLACE INTO sources VALUES(?,?,?,?,?,?,?,?,?,?)",
            (r["doi"], r["title"], r["year"], r["first_author"],
             json.dumps(r["authors"]), r["venue"], r["cited_by_count"],
             r["abstract"], r["openalex_id"], ",".join(sorted(r["chapters"]))))
    db.commit()
    print(f"\nsources.db: {len(by_doi)} unique verified works -> {out / 'sources.db'}")


if __name__ == "__main__":
    main()
