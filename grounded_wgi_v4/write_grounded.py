#!/usr/bin/env python3
"""Stage 2 of the AR7 WGI v4 source-first pipeline: write GROUNDED chapter sections.

For a chapter, loads its verified source set (sources/<chapter>.json from Stage 1)
and asks the model to draft a section that may cite ONLY those works. The allowed
sources are injected as a numbered list with DOIs; the model is instructed to cite
in (Author, Year) form drawn exclusively from the list and to end with a References
section listing the works it used, each with its DOI.

This is the key difference from the v1-v3 parametric build: citations are
constrained at generation time to a real, pre-verified corpus, so Stage 3
verification should find zero unverifiable references by construction.

Routes through shared.llm_router (native SDKs; litellm removed March 2026).
Network + API key required (reads the repo root .env). Run on THINK, not the
web sandbox. Per repo policy, keep sections to ~3-4k words; pass --sections to
split a chapter and run them sequentially.

Usage:
    python write_grounded.py --chapter chapter_02_large_scale_changes \
        --model anthropic/claude-fable-5 --out-dir drafts_v4
"""
import argparse
import json
import os
import sys
from pathlib import Path

REPO_HINT = "shared.llm_router"


def load_router():
    # Make the monorepo root importable so `shared.llm_router` resolves.
    here = Path(__file__).resolve()
    root = here
    while root != root.parent and not (root / "shared" / "llm_router").exists():
        root = root.parent
    sys.path.insert(0, str(root))
    from shared.llm_router import completion  # noqa: E402
    return completion


def sources_block(sources, limit=80):
    lines = []
    for i, s in enumerate(sources[:limit], 1):
        a = s["first_author"].split()[-1] if s["first_author"] else "Anon"
        et = " et al." if len(s["authors"]) > 1 else ""
        lines.append(f"[{i}] {a}{et} ({s['year']}). {s['title']}. "
                     f"{s['venue']}. doi:{s['doi']}")
    return "\n".join(lines)


SYSTEM = """You are drafting one section of an experimental, IPCC-AR7-style Working \
Group I assessment chapter. This is a source-FIRST build: you may cite ONLY works \
from the numbered ALLOWED SOURCES list provided in the user message. You must not \
cite, invent, or recall any other reference, however well known. If a claim cannot \
be supported by an allowed source, state it without a citation or omit it.

Requirements:
- Write in the calibrated, assessment voice of an IPCC WGI report. Open each \
numbered subsection with a bold headline statement ending in italic calibrated \
language (e.g. *high confidence*, *likely*, *virtually certain*).
- Cite in (First-author surname, Year) form, matching an allowed source exactly.
- Use plain-text scientific notation: "degrees C", "CO2", "W m-2".
- End the section with a "## References" list containing ONLY the allowed sources \
you actually cited, each formatted "Author, A., et al. (Year). Title. Venue. \
https://doi.org/<doi>".
- Do not include preamble or meta-commentary; begin directly with the content."""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", required=True)
    ap.add_argument("--section-title", default="", help="optional subsection focus")
    ap.add_argument("--model", default="anthropic/claude-fable-5")
    ap.add_argument("--src-dir", default=str(Path(__file__).with_name("sources")))
    ap.add_argument("--out-dir", default=str(Path(__file__).with_name("drafts_v4")))
    ap.add_argument("--words", type=int, default=3500)
    ap.add_argument("--max-sources", type=int, default=80)
    args = ap.parse_args()

    completion = load_router()
    spec = json.load(open(Path(args.src_dir) / f"{args.chapter}.json"))
    allowed = sources_block(spec["sources"], args.max_sources)
    focus = f"\n\nFocus this section on: {args.section_title}" if args.section_title else ""

    user = (f"Chapter: {spec['title']}\n"
            f"Target length: about {args.words} words.{focus}\n\n"
            f"ALLOWED SOURCES (cite only from this list):\n{allowed}\n\n"
            f"Write the section now.")

    resp = completion(
        model=args.model,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": user}],
        max_tokens=16000,
    )
    text = resp.choices[0].message.content

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    stem = args.chapter + ("__" + args.section_title.replace(" ", "_") if args.section_title else "")
    (out / f"{stem}.md").write_text(text)
    print(f"wrote {out / (stem + '.md')} ({len(text.split())} words, model={args.model})")


if __name__ == "__main__":
    main()
