# Methods abstract (arXiv cs.CY; cross-list physics.ao-ph)

**Title:** Verbosity Without Veracity: A Reproducible Multi-Model Probe of Large
Language Models on Long-Form Scientific Synthesis

**Abstract (~230 words).**
We report a small, fully reproducible probe of how a panel of seven large language
models behaves when asked to draft long-form scientific-assessment text *in the style
of* an IPCC Working Group II report. Using one fixed prompt set, identical task
definitions, and a uniform LLM-judge rubric, we generated up to 29 chapters per model
(~330k words in the largest configuration) and scored each for quality and factual
issues. Our central observation is counter-intuitive and policy-relevant: output length
was *negatively* associated with factual reliability. The most verbose model produced
roughly 2.8× as many flagged fact-check issues as a more concise, higher-scoring model
on matched chapters, while scoring marginally lower overall. Separately, citation
grounding was uniformly weak across all models under non-citation-enforcing prompts —
fluent, official-sounding prose largely untethered to verifiable references. We frame
these results strictly as a measurement of model behavior, not as a proposal to
automate scientific assessment, and we discuss threats to validity — chiefly the
single-LLM-judge design — at length. All prompts, scoring code, and rubrics are released.
This is a negative-leaning, hygiene-oriented contribution intended to caution against
length-as-quality heuristics in AI-for-science pipelines. Not affiliated with or
endorsed by the IPCC; all model output is unvalidated.

**Suggested categories:** cs.CY (primary), cs.CL, physics.ao-ph (cross-list).
**Full source:** `output/arxiv_methods_note/ar7_methods_note.tex` (citations gate: PASS, 6/6 verified).
