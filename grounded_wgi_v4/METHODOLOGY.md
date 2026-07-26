# Grounded WGI v4 — Source-First Methodology & Work Steps

This directory documents and reproduces the **source-first, grounded** rebuild of the
experimental AR7 Working Group I volume — the build behind *Climate Change 202X: The
Physical Science Basis, Second Revised Edition* (Variant Earths / Nimble Books,
ISBN 979-8-2595-0680-0).

It exists to make one contrast inspectable: **the same model family, writing the same
volume, parametrically vs. grounded.**

- **Parametric (v3, first edition):** the model wrote each chapter from its internal
  knowledge; citations were emitted during writing and only checked for internal
  consistency, never against real literature.
- **Grounded (v4, this edition):** research first — build a verified database of real,
  DOI-bearing works, then constrain the model to cite only from it, then machine-verify
  every citation as a build gate.

Everything here is the actual tooling and data that produced the second edition. Nothing
is a mock-up.

## The pipeline

| Stage | Script | Needs | Output |
|---|---|---|---|
| 1. Harvest | `harvest_sources.py` | network (OpenAlex, free, no key) | `sources.db` + `sources/<chapter>.json` — only works with a resolvable DOI |
| 2. Grounded write | (Claude Max subagents; prompt = `write_grounded.py` `SYSTEM` + `sources_block`) | Claude subscription | `drafts/<chapter>.md`, citing only allowed sources |
| 3. Verify | `verify_citations.py` | local only | unverifiable-citation report; **exit 1 gates the build** |

### Stage 1 — Harvest (research first)

`harvest_sources.py` queries the OpenAlex works API per chapter using the phrases in
`chapter_topics.json`, filtered to the **post-AR6 window (2021–2026)**, to journal
articles, and to `has_doi:true`, ranked by citation count. Reconstructs abstracts from
OpenAlex's inverted index. Keeps only DOI-bearing works, so every entry resolves to a
real publication.

Refreshed 2026-07-25: **1,506 unique verified works**, **2,275 chapter-tagged source
entries**, 183–288 per chapter.

```bash
python3 harvest_sources.py --mailto you@example.com
```

### Stage 2 — Grounded write (constrained generation)

Each chapter was drafted by a separate **Claude Fable 5** subagent on the Claude Max
subscription (no paid API). Each agent received the **top-80 works by citation count**
for its chapter as a numbered allowed-source list, and the strict `write_grounded.py`
`SYSTEM` prompt: cite ONLY from the list; if a claim has no allowed source, state it
without a citation or drop it — never recall or invent a reference. Written append-only
in ~3,500-word passes to a 12–15k-word target, closing with a References section of only
the sources actually cited.

`write_grounded.py` is the reference implementation of that step (it defaults to an API
model; the second edition ran the identical prompt/allowed-list logic through Max
subagents instead).

### Stage 3 — Verify (the gate)

`verify_citations.py` extracts every in-text (Author, Year) citation and matches it on
first-author surname + year against `sources.db`; it checks every References DOI against
the database. One unmatched citation fails the build.

```bash
python3 verify_citations.py --db sources.db drafts/*.md
```

**Final result across all 10 chapters: 0 unverifiable in-text citations, 0 unknown DOIs.**

## Results

| Chapter | Words | Distinct sources cited | Topical share of top-80 pool |
|---|---|---|---|
| 01 Framing, Context, and Methods | 13,117 | 52 | 35/80 |
| 02 Large-Scale Changes and Causes | 13,062 | 52 | 68/80 |
| 03 Regional Climate and Extremes | 12,642 | 27 | 43/80 |
| 04 Process Understanding | 12,954 | 48 | 57/80 |
| 05 Scenarios and Near-Term Projections | 12,658 | 32 | 59/80 |
| 06 Long-Term Global Projections | 12,882 | 35 | 45/80 |
| 07 Regional Projections | 13,214 | 57 | 64/80 |
| 08 Tipping Points and Abrupt Change | 12,656 | 27 | 29/80 |
| 09 Stabilization, Reversibility, Intervention | 12,774 | 36 | 40/80 |
| 10 Climate Information for Decisions | 12,724 | 30 | 32/80 |
| **Volume** | **128,683** | **~400 citations** | — |

Citation density tracks source-pool quality: chapters with cleaner harvests (02, 07)
cite the most distinct works; contaminated chapters (08, 03) honestly cite fewer and
state the rest in an uncited assessment voice, per the source-first rule.

## Known limitations

- **Source-pool contamination.** Ranking a keyword harvest by raw citation count lets
  highly-cited off-topic work (6G/wireless, batteries, biomedical reviews) into the
  top-80. Topical share ranged 29/80–68/80 by chapter. Fix: add an OpenAlex topic/field
  filter + post-fetch relevance screen, then re-harvest.
- **Verifier constraints.** (a) Multi-citation parentheticals — every year is paired with
  the first surname, so grouped cites were split into single-cite parentheses to pass.
  (b) Author surnames with non-ASCII characters (U+2010 hyphens, certain diacritics) are
  unmatchable and were dropped as citations, claims retained uncited. Both are tracked
  fixes.
- **No expert human review.** This is a machine-generated assessment, not peer-reviewed
  science, and not an IPCC product.

## Reproduce

```bash
python3 harvest_sources.py --mailto you@example.com      # Stage 1 (rebuilds sources.db)
# Stage 2: drive each chapter through a Claude subagent with the write_grounded.py
#          SYSTEM prompt + that chapter's top-80 sources_block; write drafts/<chapter>.md
python3 verify_citations.py --db sources.db drafts/*.md   # Stage 3 (must exit 0)
```

## Disclaimer & rights

Not an IPCC product. Not peer-reviewed. No affiliation with the IPCC, Cambridge
University Press, WMO, or UNEP. Genuine IPCC reports are **copyrighted** (© IPCC,
published by Cambridge University Press) — **not** public domain; this project neither
reproduces nor derives its text from them, imitating only the unprotected *format and
register* of an assessment report. Substantive content is synthesized from separately
harvested, openly indexed DOI-bearing journal articles, not from IPCC text.

The generated prose is **© 2026 Fred Zimmerman / Nimble Books LLC.** To invite
third-party replication and comparison, **the contents of this repository** (the drafts,
SPM, TS, front/back matter, and the included PDF) are released under **CC BY-NC 4.0** —
this repo copy only, non-commercial, with attribution; not public domain. The pipeline
**code** is MIT-licensed. The separately published commercial trade edition
(ISBN 979-8-2595-0680-0) is all-rights-reserved and not under CC. See
[COPYRIGHT.md](COPYRIGHT.md) for the full statement.

An experiment in AI-generated nonfiction, published with radical transparency so it can
be inspected, criticized, and reproduced.
