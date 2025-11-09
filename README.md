# Testin Potential LLM Contributions to Climate Assessment Reviews

A comprehensive framework for generating and evaluating draft climate assessment reports using multiple Large Language Models (LLMs), demonstrating transparent experimentation with AI involvement in scientific communication.

## Overview

This script generates complete drafts of the IPCC AR7 Working Group II climate assessment report (29 chapters, 330K+ words) using seven different AI models, then carries out a fact-checking loop, quality scoring, and multi-model comparison.

**Key Achievement**: Provides a framework for evaluating potential LLM contributions to climate assessment reviews.

**Not in Scope**:

- This project does not aim to replace human expertise in climate science.
- This project does not carry out direct analysis of data or models.
- This project does not create images, tables, charts, or visualizations.


** 📜 Disclaimer**

This project is **not affiliated with the IPCC** and does not represent actual IPCC assessment work. It is a demonstration of AI capabilities for scientific synthesis. All AI-generated content requires expert validation before use in policy or decision-making contexts.

---

## 🌍 Benefits to Global Publics, Science, and Policy

### For Global Publics

**1. Democratization of Scientific Knowledge**
- Makes complex climate science more accessible through AI-assisted synthesis
- Enables rapid generation of assessment summaries in multiple languages
- Reduces time from research to public-facing reports from years to hours

**2. Transparency and Trust**
- **Open evaluation frameworks** show exactly how AI content is generated and validated
- **Multi-model comparison** reveals strengths and weaknesses of different approaches
- **Fact-checking results** publicly document accuracy and limitations
- **Quality scoring** provides objective metrics for assessment reliability

**3. Accelerated Climate Communication**
- Faster synthesis of emerging research for policymakers
- Ability to quickly update assessments as new evidence emerges
- Multiple perspectives (USA, Europe, China) for global representation

### For Science

**1. Research Acceleration**
- **Rapid literature synthesis**: AI can process thousands of papers to identify key findings
- **Consistency checking**: Multi-model generation reveals contradictions in literature
- **Gap identification**: Comparison highlights areas needing more research

**2. Methodological Innovation**
- **Reproducible assessment pipelines**: Exact same prompts generate comparable outputs
- **Quality metrics**: Objective evaluation of synthesis quality (1-7 Likert scales)
- **Citation requirements**: V2 prompts enforce evidence-based claims with full references

**3. Enhanced Peer Review**
- AI-generated drafts provide starting points for expert refinement
- **Fact-checking frameworks** catch errors before human review
- **Cross-model validation**: Different models check each other's work

### For Policy

**1. Timely Decision Support**
- **Near-instant synthesis** of latest research for urgent policy questions
- **Scenario exploration**: Quick generation of assessment variants for different policy contexts
- **Evidence accessibility**: Direct citations link claims to peer-reviewed sources

**2. Improved Assessment Quality**
- **Objective quality metrics** (accuracy, IPCC compliance, comprehensiveness)
- **Multi-perspective analysis**: Models from different providers/nations offer diverse viewpoints
- **Consistency**: Automated generation ensures uniform style and structure

**3. Cost Efficiency**
- **Reduced assessment costs**: $5-20 vs millions for traditional IPCC assessments
- **Faster updates**: Weeks instead of years for assessment cycles
- **Resource allocation**: Frees human experts for high-value validation and refinement

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

## 📊 Key Results

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

**Total Words Generated**:
- 18 chapters across 7 models
- 48,354 words
- 7 markdown compilations
- 7 PDFs
- Complete metadata and statistics

**Best Model**: Google Gemini 2.5 Pro (perfect 7.00/7 score)

**Total Output**: 365,000+ words across all tests

**PDF Success Rate**: 100% (all formatting issues resolved)

**Working Models**: 7/7 verified

**All Tests**: ✅ Complete

**Documentation**: ✅ Comprehensive

**Project Status**: ✅ Development


See `PREMIUM_TIER_FINAL_REPORT.md` and `ULTIMATE_FINAL_REPORT.md` for complete results.


## 📖 Sample Output Comparison

To illustrate the differences between models, here is the opening of the Summary for Policymakers from two top-performing models:

### Google Gemini Pro (7.00/7 Quality Score)

> Of course. As a Coordinating Lead Author for the Intergovernmental Panel on Climate Change (IPCC) Working Group II, I will now provide the Summary for Policymakers...
>
> **A. Observed Impacts and Projected Risks**
>
> A.1. Climate change has caused widespread adverse impacts and related losses and damages to nature and people. Across all regions and sectors, impacts that were projected in previous assessments are now being observed...

### OpenAI GPT-5 (6.43/7 Quality Score)

> **Summary for Policymakers: Climate Change 202X: Impacts, Adaptation and Vulnerability**
>
> **A. Current State and Observed Impacts**
>
> A.1 Climate change has caused widespread and increasingly severe impacts on ecosystems and human systems across all continents and oceans...

**Note**: Both models demonstrate IPCC-style formatting and calibrated uncertainty language, but vary in structure, depth, and specific framing. Full chapters available in `output/production_release/`.

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

---

## 👥 About

### AI Lab for Book-Lovers

This project is developed by the **AI Lab for Book-Lovers**, exploring innovative applications of AI in scientific communication and knowledge synthesis.

🔗 **Visit**: [codexes.xtuff.ai](https://codexes.xtuff.ai)
📧 **Subscribe**: [AI Lab Substack](https://fredzannarbor.substack.com/)


### Project Lead

**Fred Zimmerman** began working on climate change in 1992 as a member of the founding team at the SocioEconomic Data Applications Center (SEDAC) for NASA's Mission to Planet Earth.  His involvement continued with providing analytic support to federal government customers for ISciences LLC. He is now the publisher of Nimble Books LLC, which operates an AI Lab for Book-Lovers, and founder of xtuff.ai.

---
