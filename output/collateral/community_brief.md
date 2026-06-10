# Community brief — one page

**Multi-Model LLM Climate-Assessment Experiment**
*Open methods · feedback-seeking · Nov 2025 snapshot · not affiliated with the IPCC*

---

### In one sentence
We measured how seven LLMs behave when asked to draft assessment-style scientific text,
and found that the wordiest model was the least factually reliable.

### What we ran
- **Task:** draft chapters *in the style of* an IPCC AR7 Working Group II report from a
  fixed, published author outline. ("AR7" names the target format only.)
- **Models (Nov 2025):** GPT-5, Gemini 2.5 Pro, Grok 3, Claude Sonnet 4, Mixtral 8x7B,
  Qwen QwQ-32B, DeepSeek (premium tier, 3 chapters each); Gemini Flash, Claude Haiku,
  GPT-4o-mini (flash tier, full 29-chapter body, ~330k words).
- **Evaluation:** one LLM judge (Gemini 2.5 Pro) — 1–7 Likert quality rubric + categorized
  fact-check pass.

### What we found
| | Gemini Flash | Claude Haiku | GPT-4o-mini |
|---|---|---|---|
| Words | ~141k | ~160k | ~29k |
| Quality (1–7) | 6.02 | 5.81 | 3.19 |
| Fact-check issues | 23 | **64** | 16 (too short) |

1. **Length hurt reliability.** +13% words → ~2.8× more flagged issues, slightly lower
   quality. A "specificity paradox": more concrete claims = more chances to be wrong.
2. **Citation grounding was uniformly weak** unless prompts forced it — fluent,
   authoritative-sounding prose untethered to verifiable references.

### What we are NOT claiming
- Not that AI should write climate assessments. Not an IPCC substitute or affiliate.
- Output is unvalidated; no climate scientist reviewed it.
- Scores come from a single (biased) LLM judge — relative signal, not truth.
- Results are a Nov-2025 snapshot and won't replicate on current models.

### What we're asking the community for
- Critique of the method and rubric.
- Alternative evaluators (other judges, human raters).
- A **domain-expert spot-check** of sample output — the missing ingredient.
- Pointers to related work on length/verbosity vs. factuality in long-form synthesis.

### Resources
- Repo (prompts, code, rubric): https://github.com/fredzannarbor/ar7-climate-assessment
- Canonical write-up: `METHODS_AND_FINDINGS.md`
- arXiv methods note (citations verified, gate-passed): `output/arxiv_methods_note/`

*Contact: Fred Zimmerman, AI Lab for Book-Lovers, Nimble Books LLC — wfz@nimblebooks.com*
