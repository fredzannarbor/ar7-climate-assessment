# Outreach Campaign — Grounded AI Assessment (AR7 WGI v4, 2nd Revised Edition)

**Prepared:** 2026-07-25
**Owner:** Variant Earths / Nimble Books (Fred Zimmerman)
**Status:** DRAFT — nothing sends or posts without Fred's explicit go-ahead per item.

## The hook (one sentence)

We had the same AI model write the same 130,000-word IPCC-style climate assessment twice —
once from memory, once forced to cite only a database of 1,506 real papers and
machine-checked on every citation — and published both so you can see the difference.

## Why this is newsworthy (not just another AI book)

- **A controlled experiment, not a demo.** Same model family, same volume, one variable
  (parametric vs. grounded). That's a methodology story, which travels further than a
  product story.
- **A falsifiable claim with a clean number.** 0 unverifiable citations / 0 unknown DOIs
  across 10 chapters. It either holds or it doesn't; we publish the tooling so anyone can
  check.
- **It speaks to the live anxiety about AI hallucination in nonfiction** — and offers a
  concrete, reproducible discipline rather than hand-waving.
- **Radical transparency as brand.** The book says on page one that it's machine-generated
  and not peer-reviewed; the repo ships the whole pipeline. That candor is the story's
  spine and its defense.

## Audiences & angles

| Audience | Angle | Channel |
|---|---|---|
| AI/ML researchers & practitioners | grounding beats parametric recall; reproducible harness | arXiv-adjacent blog post, HN, repo |
| Science-communication & climate-comms | how to publish AI climate text responsibly | LinkedIn, direct to a few writers |
| Publishing / futures-of-books | verified-citation pipeline as the minimum standard for AI nonfiction | trade posts, newsletters |
| Skeptics / critics | "both-sides AI slop?" → pre-empt with the disclaimer-first, verify-everything framing | FAQ in repo, honest limitations section |

## Assets to prepare (in order)

1. **Public repo is the anchor.** `grounded_wgi_v4/` with METHODOLOGY.md, tooling, source
   DBs, all 10 drafts. Everything else links here. *(built this session; needs commit + push)*
2. **A methods blog / research note** (~1,200 words): the contrast, the numbers, the honest
   limitations. Reuse `social-research-note` skill tone — sober, not hype.
3. **Multi-platform social posts** — one self-contained version per platform via Zernio.
   Lead with the experiment, not the book sale. Book link in a second slot.
4. **A 2×2 or before/after visual**: parametric-citation vs. grounded-citation; and the
   contamination chart (topical share of top-80 by chapter, 29–68/80) as an honest-limits
   graphic.
5. **The book itself** (LSI 2nd edition) as the destination for readers who want the object.

## Draft messages (for review — DO NOT POST until approved)

### Research note / long-form lead paragraph
> We ran a controlled experiment in AI-generated nonfiction. The same model family wrote
> the same 130,000-word, IPCC-style climate assessment two ways. In the first edition it
> wrote parametrically — from internal knowledge, citations unchecked against real
> literature. In the second we inverted the order: harvest a verified database of 1,506
> real, DOI-bearing papers first, constrain the model to cite only from per-chapter
> allowed lists, then machine-verify every citation as a build gate. Across ten chapters
> and ~400 citations: zero unverifiable, zero unknown DOIs. The grounded model makes
> fewer, better-anchored claims — and says less where its sources are thin, instead of
> manufacturing support. Both editions and the full pipeline are public.

### Short social (X/Bluesky/Threads-length)
> Same AI, same 130k-word climate assessment, written twice: once from memory, once forced
> to cite only a database of 1,506 real papers + verified on every citation. Result:
> 0 unverifiable citations across 10 chapters. Both versions + the tooling are public. This
> is what grounded AI nonfiction should look like. [repo link]

### The honest-limitations line (include everywhere — it's the credibility)
> It's not peer-reviewed, it's not an IPCC product, and automated harvesting let some
> off-topic papers into the source pools (we show exactly how much). That's the point of
> publishing the method, not just the claim.

## Sequencing

1. **Commit + push** `grounded_wgi_v4/` to the public repo (workstream B). Nothing goes out
   before the anchor is live.
2. Fred reviews this campaign + the draft messages; approves or edits.
3. Publish the research note (repo `docs/` or blog).
4. Social posts via Zernio — **preview, then post only on explicit go-ahead** (outward-facing).
5. Direct, personal outreach to a short hand-picked list (researchers/writers) — no mass mail.

## Guardrails

- Every public claim is disclaimer-first: not IPCC, not peer-reviewed, machine-generated.
- No overstating: "grounded, machine-verified citations," never "accurate climate science."
- Lead with the method and the honesty; the book sale is secondary.
- Posting is outward-facing → preview and explicit approval before anything sends.
