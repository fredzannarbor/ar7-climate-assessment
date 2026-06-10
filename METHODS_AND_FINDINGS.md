# Methods & Findings — Multi-Model LLM Climate-Assessment Experiment

**Experiment conducted:** November 2025 · **Write-up revised:** June 2026
**Status:** Open methods experiment — feedback-seeking. **Not** a production system, **not** affiliated with or endorsed by the IPCC.

This document consolidates and supersedes the ten working reports from the original run (now in `reports/archive/`). Where those reports used aspirational framing ("production-ready", cost comparisons against the IPCC process), this version states only what the experiment actually measured.

---

## 1. Question

If you hand a frontier LLM the published IPCC AR7 Working Group II author outline and ask it to draft assessment-style text, **what happens, and how do models differ from one another** under identical prompts and an identical evaluation rubric?

This is a *measurement* question about model behavior on a hard, long-form, high-stakes synthesis task. It is **not** a proposal to automate climate assessment. The IPCC process is deliberative, expert-governed, and accountable; nothing here substitutes for it. Unvalidated synthesis has, if anything, negative value in a policy setting — the expensive and irreplaceable step is expert validation, which AI does not provide.

> **On the "IPCC author" voice.** Prompted with the author outline, some models adopt a first-person *"As a Coordinating Lead Author for the IPCC…"* voice. This is a **prompt artifact**, not a claim of any role or affiliation. All "AR7 / Working Group II" usage names the *target format the models imitate*, nothing more.

---

## 2. Method

- **Task.** Generate chapters in the style of the IPCC AR7 WGII report (Summary for Policymakers, Technical Summary, and assessment chapters) from a shared, published-in-repo prompt set (`prompts/`).
- **Models (Nov-2025 versions).** Two tiers were run:
  - *Premium tier* — 7 models × 3 chapters: OpenAI GPT-5, Google Gemini 2.5 Pro, xAI Grok 3, Anthropic Claude Sonnet 4, Mistral Mixtral 8x7B, Qwen QwQ-32B, DeepSeek (32B).
  - *Flash/lite tier* — 3 models × 29 chapters (full body): Gemini 2.5 Flash, Claude Haiku 4.5, GPT-4o-mini.
- **Identical prompts** across models within each run; exact model IDs recorded in metadata.
- **Evaluation.** An LLM judge (Gemini 2.5 Pro) applied (a) a multi-dimensional 1–7 Likert quality rubric (accuracy, IPCC-style fidelity, uncertainty-language calibration, synthesis, comprehensiveness, citation quality) and (b) a fact-check pass categorizing issues as critical / major / minor.
- **Prompt variants.** V1 (no citation requirement) and V2 (mandatory literature search + in-text citations + reference list) — V2 is published for a follow-up run but the headline findings below are from V1.

---

## 3. Findings (November 2025 snapshot)

### 3.1 Headline: longer output did not mean better output

On the full 29-chapter run, scored on matched chapters:

| Model | Words | Quality (1–7) | Fact-check issues | Critical issues |
|---|---|---|---|---|
| Gemini 2.5 Flash | ~141K | **6.02** | **23** | 2 |
| Claude Haiku 4.5 | ~160K | 5.81 | **64** | 10 |
| GPT-4o-mini | ~29K | 3.19 | 16 (too short to err) | 3 |

The most verbose model (Haiku, +13% words over Flash) drew **~2.8× more fact-check issues** and more critical issues, while scoring slightly lower overall. A plausible reading is a **"specificity paradox"**: more detailed prose creates more surface area for unsupported specific claims (dates, quantities). The shortest model failed for the opposite reason — insufficient substance. This points away from word-count or length-reward as a quality proxy for scientific synthesis.

### 3.2 Citation behavior was the universal weak point

Under V1 prompts, citation-quality scores were low across *every* model (≈3.86–4.57/7) — models produced fluent, well-structured, IPCC-styled prose largely **untethered to verifiable references**. This is the single most policy-relevant failure mode and is exactly what the V2 (mandatory-citation) prompts are designed to probe in a follow-up.

### 3.3 Premium tier

In the 3-chapter premium run the evaluator ranked Gemini 2.5 Pro highest (7.00/7), with GPT-5 and Grok 3 close behind; smaller open models (Qwen, Mixtral) produced outlines or thin prose. Two models (Sonnet 4, DeepSeek) timed out / failed on the long Technical Summary chapter — itself a finding about long-context reliability under these settings.

---

## 4. Threats to validity (read before citing anything)

1. **Single LLM judge.** Scores come from one model (Gemini 2.5 Pro) acting as judge. LLM-as-judge is known to carry self-preference and verbosity biases. Scores here are a **relative, reproducible signal — not ground truth.**
2. **No human expert validation.** No climate scientist reviewed any output. Quality and fact-check labels are model-assigned.
3. **Snapshot.** All results are Nov-2025 model versions; they would change with current models.
4. **Small premium n.** The premium tier is 3 chapters per model — directional, not statistically robust.
5. **Prompt sensitivity.** Results may shift substantially with different prompts; ours are published so others can test that.

---

## 5. What we are / are not claiming

**We claim:** a reproducible harness exists; under it, on Nov-2025 models, verbosity correlated with *more* factual errors, and citation grounding was uniformly weak.

**We do not claim:** that AI can or should write climate assessments; that any output is accurate; that the evaluator scores are authoritative; or any IPCC affiliation, endorsement, or equivalence.

---

## 6. Reproduce / extend

See `REPRODUCE.md`. Prompts (V1 + V2), scoring scripts, and summary statistics are in the repo; raw generated chapters and PDFs are intentionally not committed (they regenerate from the prompts). Critiques, alternative evaluators, and human-expert spot-checks are explicitly welcomed — that is the point of releasing it.

---

*AI Lab for Book-Lovers · Nimble Books LLC · MIT License. Feedback: see repository issues.*
