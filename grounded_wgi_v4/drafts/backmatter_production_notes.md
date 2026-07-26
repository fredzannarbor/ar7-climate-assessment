<!-- model=claude-fable-5 (Claude Max subagent), stage=3 apparatus, date=2026-07-25 -->

# Production Notes

This edition was produced by a three-stage, source-first pipeline. Every step below is factual and reproducible; the complete tooling and the intermediate data are published in the project's public repository. Where a number appears, it is the number the process actually produced, not a target.

## Stage 1 — Harvest a verified source database

The evidentiary substrate was built before any drafting began. A stdlib-only harvester queried the OpenAlex works API (free, no key required) using a curated set of search phrases for each of the ten chapters. The query filter constrained results to the post-AR6 window — publication dates **2021 through 2026** — to journal articles, and, critically, to works with a resolvable DOI (`has_doi:true`). Results were ranked by citation count.

Only works with a resolvable DOI were retained, so that every entry in the database corresponds to a real, locatable publication. The harvest, refreshed on 2026-07-25, yielded **1,506 unique verified works**, tagged across the ten chapters as **2,275 chapter-level source entries** (a work relevant to more than one chapter is counted in each). Per chapter, the verified pool ranged from 183 to 288 works. Each work was stored with its DOI, title, publication year, author list, venue, citation count, and reconstructed abstract, in a SQLite database (`sources.db`) plus one JSON file per chapter.

## Stage 2 — Grounded writing, constrained to the database

Each chapter was drafted by a separate instance of Anthropic's **Claude Fable 5**, run through the Claude Max subscription as an agentic subagent — no paid API calls were used for any generation in this edition. The ten chapters were drafted in parallel.

Each drafting agent was given the **top eighty works by citation count** from its chapter's verified pool, formatted as a numbered "allowed sources" list. The system prompt was strict and identical across chapters: write in the calibrated assessment voice of a Working Group I report; open each numbered subsection with a bold headline statement ending in italicized calibrated-uncertainty language; and **cite only from the numbered allowed list**. If a claim could not be supported by an allowed source, the agent was required to state it without a citation or to omit it — never to recall, invent, or import a reference from outside the list.

Chapters were written **append-only** in successive passes of roughly 3,500 words, to a target of 12,000–15,000 words each, and closed with a References section listing only the allowed sources actually cited. The Summary for Policymakers and Technical Summary in this edition were synthesized afterward from the finished grounded chapters, and reference those chapters by cross-reference only; they introduce no new citations.

## Stage 3 — Machine verification as a build gate

After drafting, an independent verification program (`verify_citations.py`, local, no network) extracted every in-text author–year citation from every chapter and matched it, on first-author surname and year, against `sources.db`; it separately checked every DOI in each References section against the database. Any citation or DOI without a match was flagged, and the presence of a single unverifiable citation failed the build.

The final full-volume verification across all ten chapters returned **zero unverifiable in-text citations and zero unknown DOIs**. The completed volume comprises **128,683 words** across the ten chapters (each 12,600–13,200 words, inclusive of its reference list), citing between **27 and 57 distinct verified sources** per chapter.

## Known limitations

We state these plainly, because the value of a transparency experiment lies in its honest boundaries.

- **Source-pool contamination.** Ranking an automated keyword harvest by raw citation count allows highly-cited works from unrelated fields (for example, wireless-communications, battery-materials, and general biomedical review papers) to enter a chapter's top-eighty list. Measured across the volume, the topical share of each chapter's top-eighty pool ranged from **29 of 80 to 68 of 80**. In the more contaminated chapters, the agent correctly cited only the genuinely relevant works and wrote the remaining material in an uncited assessment voice, which reduced citation density. A topic-filtered re-harvest is the identified fix and is tracked for a future edition.
- **Verifier constraints.** The verification tool attributes every year inside a multi-citation parenthesis to the first-listed surname, so grouped citations were split into single-citation parentheticals to pass the gate — a cosmetic effect on some sentences. Separately, a handful of allowed sources whose author surnames contain non-ASCII characters (Unicode hyphens, certain diacritics) could not be matched by the verifier and were dropped as citations, with the underlying claims retained uncited.
- **Word counts include references.** The per-chapter figures above count each chapter's reference list.
- **No expert human review.** This remains a machine-generated assessment. It has not been reviewed by climate scientists and must not be treated as authoritative.

## Reproducibility

The harvester, the writer prompt and its allowed-source formatting, the verifier, the per-chapter source JSONs, and all ten grounded chapter drafts are published in the public repository accompanying this edition, so that the entire build can be inspected and re-run.
