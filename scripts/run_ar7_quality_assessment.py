#!/usr/bin/env python3
"""
run_ar7_quality_assessment.py

Quality assessment phase for AR7 model comparison.
Runs AFTER generation and fact-checking to score each model's output.

Usage:
    # Assess specific chapter across all models
    uv run python run_ar7_quality_assessment.py \
      --chapter summary_for_policymakers \
      --model-outputs output/ar7_model_comparison \
      --fact-check-results output/ar7_fact_checking

    # Assess all chapters
    uv run python run_ar7_quality_assessment.py \
      --all-chapters \
      --model-outputs output/ar7_model_comparison \
      --fact-check-results output/ar7_fact_checking
"""

import argparse
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from codexes.modules.ar7_quality_assessment import AR7QualityAssessor, QualityScores, ChapterAssessment


QUALITY_ASSESSMENT_PROMPT = """You are an expert climate scientist and IPCC assessment reviewer with 20+ years experience.

You will evaluate AR7 chapter outputs from different AI models using strict 1-7 Likert scales.

CHAPTER: {chapter_key}
MODEL: {model_id}

ORIGINAL TEXT:
{chapter_text}

FACT-CHECKING RESULTS:
Errors found: {errors_found}
Error rate: {error_rate:.1%}
Details: {fact_check_summary}

RATING SCALES:

**ACCURACY (1-7):**
1 = Numerous factual errors, misrepresentations of published research
2 = Many errors undermining reliability
3 = Several errors but mostly accurate on major findings
4 = Few errors, generally reliable
5 = Minor errors only, highly accurate and verifiable
6 = Exceptionally accurate, near-perfect citation and fact representation
7 = Flawless, every claim verifiable from peer-reviewed sources

**STYLE (1-7):**
1 = Does not follow IPCC conventions, inappropriate tone/structure
2 = Poor adherence to IPCC style
3 = Partial adherence, some formatting and language issues
4 = Decent IPCC style with noticeable deviations
5 = Good IPCC style with minor convention deviations
6 = Excellent IPCC style, very few issues
7 = Perfect IPCC style: calibrated language, structure, tone, formatting

**INTELLIGENCE (1-7):**
1 = Superficial, misses key concepts and connections
2 = Below basic competence
3 = Basic competence, covers standard material adequately
4 = Good understanding, some sophisticated analysis
5 = NATIONAL-LEVEL EXPERT - comprehensive, nuanced, sophisticated analysis
6 = WORLD-CLASS EXPERT (top 1% of climate scientists) - exceptional synthesis, deep insights
7 = SUPERHUMAN - insights, connections, or analyses demonstrably beyond human expert capability

**SUB-METRICS (1-7 each):**
- Citation quality (accuracy, appropriateness, completeness)
- Coverage completeness (addresses all required topics)
- Uncertainty language (proper IPCC calibrated language use)
- Synthesis quality (integrates across literature effectively)
- Regional/sectoral balance (appropriate global coverage)

**QUALITATIVE ASSESSMENT:**
- Top 3 strengths
- Top 3 weaknesses
- Notable errors (if any)

**COMPARATIVE CONTEXT:**
Other models' word counts for this chapter: {comparison_word_counts}
(This helps calibrate expectations - some models may be more concise vs verbose)

PROVIDE YOUR ASSESSMENT AS JSON:
{{
  "accuracy": <1-7>,
  "accuracy_justification": "...",
  "style": <1-7>,
  "style_justification": "...",
  "intelligence": <1-7>,
  "intelligence_justification": "...",
  "citation_quality": <1-7>,
  "coverage_completeness": <1-7>,
  "uncertainty_language": <1-7>,
  "synthesis_quality": <1-7>,
  "regional_balance": <1-7>,
  "strengths": ["...", "...", "..."],
  "weaknesses": ["...", "...", "..."],
  "notable_errors": ["..."],
  "overall_assessment": "Brief 2-3 sentence summary"
}}
"""


def main():
    parser = argparse.ArgumentParser(
        description="AR7 Quality Assessment - Score model outputs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--chapter",
        help="Specific chapter to assess"
    )
    parser.add_argument(
        "--all-chapters",
        action="store_true",
        help="Assess all chapters"
    )
    parser.add_argument(
        "--model-outputs",
        default="output/ar7_model_comparison",
        help="Directory with model outputs"
    )
    parser.add_argument(
        "--fact-check-results",
        default="output/ar7_fact_checking",
        help="Directory with fact-checking results"
    )
    parser.add_argument(
        "--output",
        default="output/ar7_quality_assessment",
        help="Output directory for assessments"
    )
    parser.add_argument(
        "--assessor-model",
        default="gemini/gemini-2.5-pro",
        help="LLM model to use for quality assessment"
    )

    args = parser.parse_args()

    if not args.chapter and not args.all_chapters:
        parser.error("Must specify --chapter or --all-chapters")

    # Initialize assessor
    assessor = AR7QualityAssessor(llm_model=args.assessor_model)

    # Display assessment plan
    print("="*80)
    print("AR7 QUALITY ASSESSMENT")
    print("="*80)
    print(f"Assessor model: {args.assessor_model}")
    print(f"Model outputs: {args.model_outputs}")
    print(f"Fact-check results: {args.fact_check_results}")
    print(f"Output: {args.output}")
    print("="*80)
    print()

    # TODO: Implementation
    print("Quality assessment framework created.")
    print("Integration with llm_caller needed for actual scoring.")
    print()
    print("NEXT STEPS:")
    print("1. Run fact-checking on all model outputs")
    print("2. Use this script to score each chapter from each model")
    print("3. Generate comparative reports")
    print("4. Create final rankings and insights")
    print()
    print("See src/codexes/modules/ar7_quality_assessment.py for framework")

    return 0


if __name__ == "__main__":
    sys.exit(main())
