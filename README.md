# Testing LLM Contributions to Climate Assessment Reviews

A reproducible framework for generating and evaluating draft climate-assessment text using multiple Large Language Models (LLMs), as a transparent **experiment** in measuring AI-assisted scientific synthesis.

> **Snapshot note (models & dates):** The experiment described here was **conducted in November 2025**; this write-up was **revised June 2026**. All model versions, quality scores, and cost figures are a **November-2025 snapshot**. Frontier models move quickly — these numbers describe how *those* models behaved on *that* date, not the current state of the art. Reproducing the experiment with current models would be expected to change the results.

## Overview

These scripts generate complete drafts written **in the style of** an IPCC AR7 Working Group II climate-assessment report (29 chapters, ~330K words) using seven different AI models, then carry out a fact-checking loop, quality scoring, and multi-model comparison. Model parameters and prompts are fully documented and customizable.

**What this is**: an open, reproducible methods experiment for *measuring* how a panel of LLMs performs at long-form scientific synthesis under identical prompts, and for comparing models against one another. It is a measurement and comparison harness — **not** a production assessment system and **not** a substitute for the IPCC process.

> **On the "IPCC author" voice:** When prompted with the AR7 author outline, some models adopt a first-person voice such as *"As a Coordinating Lead Author for the IPCC…"*. This is a **stylistic artifact of the prompt, not a claim of any affiliation, authority, or role.** No output here was produced by, reviewed by, or endorsed by the IPCC or any of its authors.

**Not in Scope**:

- This project does not aim to replace human expertise in climate science, nor the IPCC assessment process.
- This project does not carry out direct analysis of data or models.
- This project does not create images, tables, charts, or visualizations.

**Disclaimer**:

This project is **not affiliated with the IPCC**, is not endorsed by it, and does not represent actual IPCC assessment work. "AR7" and "Working Group II" are used only to name the *target format* the models were asked to imitate. It is an experiment characterizing AI behavior on a hard synthesis task. **All AI-generated content is unvalidated** and must not be used in policy or decision-making contexts without expert review.

---

## 🌍 Why run this experiment?

The point is **measurement**, not deployment. Open, reproducible benchmarking of LLM behavior on a genuinely hard, high-stakes synthesis task is useful regardless of whether AI ever belongs anywhere near a real assessment. We make no claim that AI should write climate assessments — we ask only: *if a model is given this task, what actually happens, and how do models differ?*

**What the experiment can contribute:**

- **A transparent comparison harness.** Identical prompts across seven models make strengths and failure modes directly comparable, with all prompts, scoring criteria, and model IDs published.
- **Documented failure modes.** Fact-checking and quality scoring surface *where* and *how* these models go wrong on scientific synthesis (e.g. fabricated specifics, weak citation behavior, calibration of uncertainty language) — useful evidence for anyone studying LLM reliability.
- **An empirical, slightly counter-intuitive finding** (see Results): under these conditions, **longer output did not mean better output** — the more verbose model produced markedly more factual errors than a more concise one. This is the kind of measurable behavior worth sharing with the AI-for-science community.

**What it explicitly does NOT contribute** (and we want to be loud about this):

- It is **not** a path to "democratizing" or "accelerating" climate assessment. The IPCC process is deliberative, expert-governed, and accountable; nothing here substitutes for that.
- The cost of running these models is trivial (single-digit dollars), but **cheap to generate is not the same as cheap to trust.** The expensive, irreplaceable part — expert validation — is exactly what AI does not provide.
- None of the output is validated, and unvalidated synthesis has *negative* value in a policy context.

### Transparency the experiment does provide

- **Open evaluation framework** — exactly how content is generated and scored is public (see `prompts/`).
- **Multi-model comparison** — strengths/weaknesses are reported side by side, including the models that failed.
- **Fact-checking results** — errors are documented rather than hidden.
- **Reproducible pipeline** — same prompts, same model IDs, same scoring rubric.

---

## 🎯 Transparency Principles

### 1. Open Methodology
- **All prompts publicly available** (see `prompts/`)
- **Evaluation criteria documented** (7-point Likert scales with justifications)
- **Model configurations transparent** (exact model IDs and parameters)

### 2. Rigorous Evaluation
- **Fact-checking**: Every model output evaluated for errors
- **Quality scoring**: Multi-dimensional assessment (accuracy, style, intelligence)
- **Comparative analysis**: Models ranked objectively on performance

### 3. Limitations Acknowledged
- **AI hallucinations documented**: Fact-check reports show specific errors
- **Quality variations noted**: Some models fail to meet standards
- **Human validation required**: AI is tool for acceleration, not replacement

### 4. Reproducibility
- **All code open source**
- **Exact prompts preserved**
- **Results fully documented** with statistics and examples

---

## 📊 Methods

### Prompts

The prompts used for each model are available in the `prompts/` directory. The prompts were based on the actual outline provided to AR7 authors with enhancements to improve the models' substantive and stylistic accuracy.  Each model used the same prompts.  The prompts could and should be reviewed and edited by AR7 authors to improve the model's responsiveness to author goals.

### Premium Models used

  1. **OpenAI GPT-5** (`openai/gpt-5`)
     - Provider: USA - OpenAI
     - Chapters: 3/3 (100%)
     - Words: 15,099
     - Quality: 6.43/7

  2. **Google Gemini 2.5 Pro** (`gemini/gemini-2.5-pro`)
     - Provider: USA - Google
     - Chapters: 3/3 (100%)
     - Words: 10,740
     - Quality: 7.00/7 🏆 (Perfect)

  3. **xAI Grok 3** (`xai/grok-3-latest`)
     - Provider: USA - xAI (Elon Musk)
     - Chapters: 3/3 (100%)
     - Words: 5,245
     - Quality: 6.60/7

  4. **Anthropic Claude Sonnet 4**
  (`anthropic/claude-sonnet-4-20250514`)
     - Provider: USA - Anthropic
     - Chapters: 2/3 (67% - Tech Summary timeout)
     - Words: 9,898
     - Quality: Not scored (incomplete)

  5. **Mistral Mixtral 8x7B**
  (`deepinfra/mistralai/Mixtral-8x7B-Instruct-v0.1`)
     - Provider: Europe - Mistral (France)
     - Chapters: 3/3 (100%)
     - Words: 2,530
     - Quality: 4.29/7

  6. **Qwen QwQ-32B** (`deepinfra/Qwen/QwQ-32B-Preview`)
     - Provider: China - Qwen (Alibaba)
     - Chapters: 3/3 (100%)
     - Words: 3,980
     - Quality: 1.86/7 (Generated outline, not prose)


### Results (November 2025 snapshot)

**Premium-tier run** (7 models × 3 chapters: Summary for Policymakers, Technical Summary, Chapter 2):
- 18 chapters generated successfully across 7 models
- 48,354 words
- Best per the automated evaluator: **Google Gemini 2.5 Pro, 7.00/7**

**Earlier flash/lite-tier run** (3 models × 29 chapters) produced the full ~330K-word body and is where the headline empirical finding comes from:

- **Longer ≠ better.** The most verbose model (Claude Haiku 4.5, ~160K words) was flagged with **~2.8× more fact-check issues** (64 vs 23) than a more concise, higher-scoring model (Gemini Flash, ~141K words, 6.02/7) on the same chapters.
- **Citation behavior was the universal weak point** across all models under the V1 prompts (3.86–4.57/7); the V2 prompts add mandatory-citation requirements as a follow-up to test.

**Two caveats on these numbers:**

1. Scores come from a **single LLM judge** (Gemini 2.5 Pro). LLM-as-judge is known to be biased; it is used here as a *relative, reproducible* signal, not ground truth. No human expert validated any output.
2. These are **November-2025 model versions**; results would differ with current models.

**All Tests**: ✅ Complete

> **Note on artifacts in this repo:** code, prompts, scoring rubrics, and summary statistics are included. The **raw generated chapters and PDFs are intentionally not committed** (see `.gitignore`) — we publish the *method and the measurements*, not unvalidated AI drafts that could be mistaken for real assessment text. They are regenerable from the prompts and scripts; see `REPRODUCE.md`.

For the consolidated write-up, see **`METHODS_AND_FINDINGS.md`**. Superseded prior reports are kept in `reports/archive/`.


### 📖 Sample Output Comparison

To illustrate the differences between models, here is the opening of the Summary for Policymakers from two top-performing models:

> ⚠️ **Read these as model behavior, not as climate statements.** The excerpts below are *unvalidated AI output* reproduced to show stylistic differences between models. The "Coordinating Lead Author" framing in the first excerpt is a **prompt artifact** (the model role-playing the assigned outline), **not** a claim of any IPCC role. Do not cite these passages as fact.

### Google Gemini Pro (7.00/7 evaluator score)

> Of course. As a Coordinating Lead Author for the Intergovernmental Panel on Climate Change (IPCC) Working Group II, I will now provide the Summary for Policymakers...  *(← prompt-induced role-play voice; not an actual IPCC role)*
>
> **A. Observed Impacts and Projected Risks**
>
> A.1. Climate change has caused widespread adverse impacts and related losses and damages to nature and people. Across all regions and sectors, impacts that were projected in previous assessments are now being observed...

### OpenAI GPT-5 (6.43/7 evaluator score)

> **Summary for Policymakers: Climate Change 202X: Impacts, Adaptation and Vulnerability**
>
> **A. Current State and Observed Impacts**
>
> A.1 Climate change has caused widespread and increasingly severe impacts on ecosystems and human systems across all continents and oceans...

**Note**: Both models imitate IPCC-style formatting and calibrated uncertainty language, but vary in structure, depth, and framing. Raw chapters are not committed (see the artifacts note above) but regenerate deterministically from `prompts/` per `REPRODUCE.md`.

---

---

## 📁 Output Structure

```
output/production_release/
├── openai_gpt5/
│   ├── summary_for_policymakers.txt
│   ├── technical_summary.txt
│   ├── chapter_2_vulnerabilities_impacts_risks.txt
│   ├── *_metadata.json (3 files with generation stats)
│   ├── generation_summary.json
│   └── AR7_PRODUCTION_OPENAI_GPT5.md (compiled book)
├── google_gemini_pro/
│   ├── [same structure as above]
├── xai_grok3/
│   ├── [same structure]
├── anthropic_sonnet4/
│   ├── [2 chapters - technical_summary timed out]
├── mistral_mixtral/
│   ├── [same structure]
├── qwen_32b/
│   ├── [same structure]
├── deepseek_32b/
│   ├── [2 chapters - technical_summary failed]
├── pdfs/
│   ├── AR7_PRODUCTION_OPENAI_GPT5.pdf
│   ├── AR7_PRODUCTION_GOOGLE_GEMINI_PRO.pdf
│   ├── AR7_PRODUCTION_XAI_GROK3.pdf
│   ├── AR7_PRODUCTION_ANTHROPIC_SONNET4.pdf
│   ├── AR7_PRODUCTION_MISTRAL_MIXTRAL.pdf
│   ├── AR7_PRODUCTION_QWEN_32B.pdf
│   └── AR7_PRODUCTION_DEEPSEEK_32B.pdf
└── PRODUCTION_SUMMARY.json (master statistics)
```

(The `*.txt`/`*.pdf` leaves above are produced by a run but are gitignored; this layout documents what a reproduction will create locally.)

---

## Reproducibility & dependencies

See **`REPRODUCE.md`** for exact commands, required API keys, and what is/isn't committed.

> **Note on `litellm`:** the generation scripts in this repo call models through `litellm` **as the experiment was run in November 2025**. This is preserved *as-run* for reproducibility and is **not a current recommendation** — Nimble Books' own stack has since moved off `litellm` to native provider SDKs. Treat the dependency list here as a historical snapshot, and pin/verify any package before installing.

---

## 👥 About

### Project Lead

**Fred Zimmerman** began working on climate change in 1992 as a member of the founding team at the SocioEconomic Data Applications Center (SEDAC) for NASA's Mission to Planet Earth.  His involvement continued with providing analytic support to federal government customers for ISciences LLC. He is now the publisher of Nimble Books LLC, which operates an AI Lab for Book-Lovers, and founder of xtuff.ai.

### AI Lab for Book-Lovers

This project is developed by the **AI Lab for Book-Lovers**, exploring innovative applications of AI in scientific communication and knowledge synthesis.

🔗 **Visit**: [codexes.xtuff.ai](https://codexes.xtuff.ai)
📧 **Subscribe**: [AI Lab Substack](https://fredzannarbor.substack.com/)

### Variant Earths

Some future outputs from this project will be published in book form by Variant Earths, an imprint of Nimble Books LLC dba Big Five Killers.  Of course, no third party content will be included without permission.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
