#!/usr/bin/env python3
"""
run_fact_checking.py

Fact-check sample chapters from AR7 model comparison.
Uses an evaluator model to verify scientific claims.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Try to import LiteLLM
try:
    import litellm
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    print("WARNING: litellm not available. Fact-checking will be simulated.")


FACT_CHECK_PROMPT = """You are an expert climate scientist and fact-checker reviewing AI-generated climate assessment content for the IPCC AR7 report.

Your task is to identify any factual errors, misrepresentations, or unsupported claims in the following chapter.

CHAPTER: {chapter_name}
MODEL: {model_name}

CONTENT:
{content}

Please analyze this content and identify:

1. **Factual Errors**: Specific claims that are demonstrably incorrect based on current climate science literature
2. **Misrepresentations**: Claims that oversimplify, exaggerate, or mischaracterize scientific findings
3. **Unsupported Claims**: Statements lacking scientific evidence or proper attribution
4. **Uncertainty Language Issues**: Improper use of IPCC calibrated language (e.g., "virtually certain" used incorrectly)
5. **Outdated Information**: References to superseded findings or old data

For each issue found, provide:
- Location (approximate line/paragraph)
- Issue type
- Description of the problem
- Correct information (if applicable)
- Severity (Critical, Major, Minor)

Respond in JSON format:
{{
  "total_issues": <number>,
  "critical_issues": <number>,
  "major_issues": <number>,
  "minor_issues": <number>,
  "issues": [
    {{
      "location": "...",
      "type": "...",
      "severity": "...",
      "description": "...",
      "correction": "..."
    }}
  ],
  "overall_assessment": "...",
  "confidence_score": <0-100>
}}

If no significant issues are found, return an empty issues array.
"""


def fact_check_chapter(chapter_file: Path, model_name: str,
                       evaluator_model: str = "gemini/gemini-2.5-pro") -> Dict:
    """Fact-check a single chapter"""

    print(f"  🔍 Fact-checking: {chapter_file.name}")

    # Read chapter content
    try:
        content = chapter_file.read_text(encoding='utf-8')
        word_count = len(content.split())

        # Limit content for fact-checking (first 5000 words)
        if word_count > 5000:
            words = content.split()[:5000]
            content = ' '.join(words) + "\n\n[Content truncated for fact-checking...]"
            print(f"    ⚠️  Truncated to 5000 words for evaluation")

    except Exception as e:
        print(f"    ❌ Error reading file: {e}")
        return {
            "success": False,
            "error": str(e)
        }

    chapter_name = chapter_file.stem.replace('_', ' ').title()

    if not LITELLM_AVAILABLE:
        # Simulated fact-checking results
        return {
            "success": True,
            "chapter": chapter_name,
            "model": model_name,
            "word_count": word_count,
            "simulated": True,
            "total_issues": 0,
            "critical_issues": 0,
            "major_issues": 0,
            "minor_issues": 0,
            "issues": [],
            "overall_assessment": "Fact-checking simulated (litellm not available)",
            "confidence_score": 0
        }

    # Perform actual fact-checking
    try:
        prompt = FACT_CHECK_PROMPT.format(
            chapter_name=chapter_name,
            model_name=model_name,
            content=content
        )

        response = litellm.completion(
            model=evaluator_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        print(f"    ✅ Issues found: {result.get('total_issues', 0)}")
        if result.get('critical_issues', 0) > 0:
            print(f"       🔴 Critical: {result['critical_issues']}")
        if result.get('major_issues', 0) > 0:
            print(f"       🟡 Major: {result['major_issues']}")
        if result.get('minor_issues', 0) > 0:
            print(f"       🟢 Minor: {result['minor_issues']}")

        return {
            "success": True,
            "chapter": chapter_name,
            "model": model_name,
            "word_count": word_count,
            "simulated": False,
            **result
        }

    except Exception as e:
        print(f"    ❌ Error during fact-checking: {e}")
        return {
            "success": False,
            "chapter": chapter_name,
            "model": model_name,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description="Fact-check AR7 sample chapters")
    parser.add_argument("--output-dir", default="output/ar7_complete_run_final")
    parser.add_argument("--samples", type=int, default=3,
                       help="Number of sample chapters to check per model")
    parser.add_argument("--evaluator", default="gemini/gemini-2.5-pro",
                       help="Model to use for fact-checking")
    parser.add_argument("--chapters",
                       help="Specific chapters to check (comma-separated)")

    args = parser.parse_args()

    output_dir = Path(args.output_dir)

    if not output_dir.exists():
        print(f"ERROR: Output directory not found: {output_dir}")
        return 1

    print(f"\n{'='*80}")
    print(f"AR7 FACT-CHECKING - SAMPLE CHAPTERS")
    print(f"{'='*80}")
    print(f"Evaluator Model: {args.evaluator}")
    print(f"Samples per Model: {args.samples}")
    print(f"{'='*80}\n")

    # Select chapters to fact-check
    if args.chapters:
        target_chapters = [c.strip() for c in args.chapters.split(',')]
    else:
        # Default sample chapters (diverse selection)
        target_chapters = [
            "summary_for_policymakers",
            "technical_summary",
            "chapter_2_vulnerabilities_impacts_risks",
            "chapter_7_africa",
            "chapter_16_water"
        ][:args.samples]

    print(f"Target chapters: {', '.join(target_chapters)}\n")

    # Fact-check each model
    all_results = {}

    for model_dir in output_dir.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['pdfs', '__pycache__']:
            continue

        model_name = model_dir.name
        print(f"\n{'='*80}")
        print(f"MODEL: {model_name}")
        print(f"{'='*80}")

        model_results = []

        for chapter_key in target_chapters:
            chapter_file = model_dir / f"{chapter_key}.txt"

            if not chapter_file.exists():
                print(f"  ⚠️  Skipping {chapter_key} - file not found")
                continue

            result = fact_check_chapter(chapter_file, model_name, args.evaluator)
            model_results.append(result)

        all_results[model_name] = model_results

        # Summary for this model
        successful = [r for r in model_results if r.get("success")]
        total_issues = sum(r.get("total_issues", 0) for r in successful)
        critical = sum(r.get("critical_issues", 0) for r in successful)

        print(f"\n  Summary for {model_name}:")
        print(f"    Chapters checked: {len(successful)}")
        print(f"    Total issues: {total_issues}")
        print(f"    Critical issues: {critical}")

    # Save results
    fact_check_dir = output_dir / "fact_checking"
    fact_check_dir.mkdir(exist_ok=True)

    results_file = fact_check_dir / "fact_check_results.json"

    full_results = {
        "generated_at": datetime.now().isoformat(),
        "evaluator_model": args.evaluator,
        "chapters_checked": target_chapters,
        "models": all_results
    }

    with open(results_file, 'w') as f:
        json.dump(full_results, f, indent=2)

    print(f"\n{'='*80}")
    print(f"FACT-CHECKING COMPLETE")
    print(f"{'='*80}")
    print(f"Results saved to: {results_file}")

    # Generate summary report
    report_file = fact_check_dir / "fact_check_report.md"

    report = f"""# AR7 Fact-Checking Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Evaluator Model**: {args.evaluator}
**Chapters Checked**: {len(target_chapters)}

## Summary by Model

"""

    for model_name, results in all_results.items():
        successful = [r for r in results if r.get("success")]
        total_issues = sum(r.get("total_issues", 0) for r in successful)
        critical = sum(r.get("critical_issues", 0) for r in successful)
        major = sum(r.get("major_issues", 0) for r in successful)
        minor = sum(r.get("minor_issues", 0) for r in successful)

        report += f"### {model_name}\n\n"
        report += f"- Chapters checked: {len(successful)}\n"
        report += f"- Total issues: {total_issues}\n"
        report += f"- Critical: {critical} 🔴\n"
        report += f"- Major: {major} 🟡\n"
        report += f"- Minor: {minor} 🟢\n\n"

        if total_issues > 0:
            report += "**Issues by Chapter:**\n\n"
            for result in successful:
                if result.get("total_issues", 0) > 0:
                    report += f"- {result['chapter']}: {result['total_issues']} issues\n"
            report += "\n"

    report += f"\n## Detailed Results\n\nSee `fact_check_results.json` for complete details.\n"

    report_file.write_text(report)
    print(f"Report saved to: {report_file}")
    print(f"{'='*80}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
