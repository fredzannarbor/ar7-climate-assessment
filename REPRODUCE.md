# Reproducing the experiment

This repo publishes the **method and the measurements**, not the raw AI-generated drafts.
The generated chapters (`output/**/*.txt`) and compiled PDFs are intentionally **gitignored** —
they are unvalidated AI output that should not be mistaken for real assessment text, and they
regenerate deterministically from the prompts and scripts below.

> **Snapshot caveat.** The experiment was run in **November 2025**. Model IDs in the scripts
> point at Nov-2025 versions; some will have been deprecated or upgraded. Reproducing today
> will produce *different* numbers — that is expected and is part of the point.

## 1. What you need

- Python 3.12+ and [`uv`](https://docs.astral.sh/uv/).
- API keys for the providers you want to run (any subset works):
  OpenAI, Anthropic, Google (Gemini), xAI, DeepInfra (for Mixtral / Qwen), DeepSeek.
- For PDF compilation: `pandoc` + a LaTeX engine (XeLaTeX or pdfLaTeX).

Copy `.env.example` to `.env` and fill in the keys you have.

> **Dependency note.** The scripts call models via `litellm` **as run in Nov 2025**. This is
> preserved as-run for reproducibility and is **not a current recommendation**. Pin and verify
> any package before installing (supply-chain hygiene).

## 2. Install

```bash
uv sync
```

## 3. Run a generation

```bash
# Full multi-model comparison (edit the model list inside the script / via flags)
uv run python scripts/run_ar7_direct_test.py \
  --models "gemini_flash,anthropic_haiku" \
  --prompt-file prompts/ar7_model_comparison_prompts.json \
  --output-dir output/my_run \
  --compile-books

# V2 (mandatory-citation) prompts
uv run python scripts/run_ar7_direct_test.py \
  --models "gemini_flash" \
  --prompt-file prompts/ar7_model_comparison_prompts_v2_full_cited.json \
  --output-dir output/my_v2_run \
  --compile-books
```

## 4. Evaluate

```bash
uv run python scripts/run_ar7_quality_assessment.py --output-dir output/my_run
uv run python scripts/run_ar7_fact_checking.py     --output-dir output/my_run
uv run python scripts/generate_final_report.py     --output-dir output/my_run
```

## 5. What gets produced

- `output/my_run/<model>/*.txt` — per-chapter drafts (gitignored)
- `output/my_run/<model>/*_metadata.json` — per-chapter generation stats
- `output/my_run/quality_scoring/`, `fact_checking/` — evaluator outputs
- `output/my_run/pdfs/*.pdf` — compiled books (gitignored)
- summary `*.json` files (committed)

## 6. Caveats on results

The evaluator is a single LLM (Gemini 2.5 Pro). Treat scores as a relative, reproducible
signal, not ground truth. No human expert validated any output. See `METHODS_AND_FINDINGS.md`
§4 (Threats to validity) before citing any number.
