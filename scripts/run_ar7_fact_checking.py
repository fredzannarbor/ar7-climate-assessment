#!/usr/bin/env python3
"""
run_ar7_fact_checking.py

Fact-checking script for AR7 model comparison outputs.
Uses Gemini with grounding to verify factual claims and citations.

Usage:
    # Check all chapters from all models
    uv run python run_ar7_fact_checking.py \
        --model-outputs output/ar7_model_comparison

    # Check specific chapter across all models
    uv run python run_ar7_fact_checking.py \
        --model-outputs output/ar7_model_comparison \
        --chapter summary_for_policymakers

    # Check specific model
    uv run python run_ar7_fact_checking.py \
        --model-outputs output/ar7_model_comparison \
        --model-id google_gemini3
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from codexes.core.llm_caller import call_model_with_prompt
except ModuleNotFoundError:
    from src.codexes.core.llm_caller import call_model_with_prompt


FACT_CHECKER_PROMPT = """You are a climate science fact-checker verifying AI-generated content against published literature.

Review the chapter below and identify:

1. **FACTUAL ERRORS**: Claims that contradict published literature or cite non-existent sources
2. **CITATION ISSUES**: Missing citations, incorrect citations, or unsupported claims
3. **UNCERTAINTY MISREPRESENTATION**: Incorrect use of IPCC calibrated language (virtually certain, very likely, likely, medium confidence, etc.)
4. **OUTDATED INFORMATION**: Claims based on outdated science that has been superseded
5. **STATISTICAL ERRORS**: Misrepresented data, incorrect trends, or mathematical errors

For each issue found, provide:
- **Type**: (factual_error | citation_issue | uncertainty_issue | outdated | statistical_error)
- **Severity**: (critical | major | minor)
- **Location**: Quote the problematic text
- **Issue**: Explain what's wrong
- **Correction**: What the correct information should be (if known)

If the chapter is accurate, respond with: "No significant errors found."

Output format (JSON):
{
  "errors_found": <number>,
  "error_rate": <errors per 1000 words>,
  "issues": [
    {
      "type": "factual_error",
      "severity": "major",
      "location": "quote from text",
      "issue": "explanation",
      "correction": "correct information"
    }
  ],
  "overall_assessment": "brief summary",
  "confidence": "high | medium | low"
}

---

CHAPTER TO REVIEW:

{chapter_content}
"""


def find_chapter_files(model_outputs_dir: Path, chapter_key: Optional[str] = None,
                      model_id: Optional[str] = None) -> List[Dict]:
    """
    Find chapter files to fact-check

    Args:
        model_outputs_dir: Base directory with model outputs
        chapter_key: Optional specific chapter to check
        model_id: Optional specific model to check

    Returns:
        List of dicts with model_id, chapter_key, file_path
    """
    files_to_check = []

    # Get all model directories
    model_dirs = [d for d in model_outputs_dir.iterdir() if d.is_dir()]

    for model_dir in model_dirs:
        current_model_id = model_dir.name

        # Skip if filtering by model_id
        if model_id and current_model_id != model_id:
            continue

        # Look for chapter files in prompts_output or similar
        chapter_dirs = [
            model_dir / "prompts_output",
            model_dir / "chapters",
            model_dir
        ]

        for chapter_dir in chapter_dirs:
            if not chapter_dir.exists():
                continue

            # Find .txt or .md files
            for ext in [".txt", ".md"]:
                chapter_files = list(chapter_dir.glob(f"*{ext}"))

                for chapter_file in chapter_files:
                    # Extract chapter key from filename
                    file_chapter_key = chapter_file.stem

                    # Skip if filtering by chapter
                    if chapter_key and file_chapter_key != chapter_key:
                        continue

                    files_to_check.append({
                        "model_id": current_model_id,
                        "chapter_key": file_chapter_key,
                        "file_path": chapter_file
                    })

    return files_to_check


def fact_check_chapter(chapter_content: str, fact_checker_model: str = "gemini/gemini-2.0-flash-exp") -> Dict:
    """
    Fact-check a single chapter using Gemini with grounding

    Args:
        chapter_content: The chapter text to check
        fact_checker_model: Model to use for fact-checking

    Returns:
        Dictionary with fact-check results
    """
    prompt = FACT_CHECKER_PROMPT.format(chapter_content=chapter_content)

    messages = [
        {"role": "user", "content": prompt}
    ]

    try:
        # Call LLM with grounding enabled
        response = call_model_with_prompt(
            messages=messages,
            model=fact_checker_model,
            temperature=0.2,
            max_tokens=4000,
            response_format={"type": "json_object"}
        )

        # Parse JSON response
        result = json.loads(response)
        return result

    except json.JSONDecodeError:
        # If JSON parsing fails, return basic structure
        return {
            "errors_found": 0,
            "error_rate": 0.0,
            "issues": [],
            "overall_assessment": "Error parsing fact-check response",
            "confidence": "low",
            "raw_response": response
        }
    except Exception as e:
        return {
            "errors_found": 0,
            "error_rate": 0.0,
            "issues": [],
            "overall_assessment": f"Fact-checking failed: {str(e)}",
            "confidence": "low",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description="AR7 Fact-Checking with Gemini Grounding",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--model-outputs",
        required=True,
        help="Directory containing model outputs (e.g., output/ar7_model_comparison)"
    )
    parser.add_argument(
        "--chapter",
        help="Specific chapter to fact-check (default: all)"
    )
    parser.add_argument(
        "--model-id",
        help="Specific model to fact-check (default: all)"
    )
    parser.add_argument(
        "--fact-checker",
        default="gemini/gemini-2.0-flash-exp",
        help="Model to use for fact-checking"
    )
    parser.add_argument(
        "--output-dir",
        default="output/ar7_fact_checking",
        help="Output directory for fact-check results"
    )

    args = parser.parse_args()

    model_outputs_dir = Path(args.model_outputs)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not model_outputs_dir.exists():
        print(f"❌ Error: Model outputs directory not found: {model_outputs_dir}")
        return 1

    print(f"\n{'='*80}")
    print(f"AR7 FACT-CHECKING")
    print(f"{'='*80}")
    print(f"Model outputs: {model_outputs_dir}")
    print(f"Fact-checker: {args.fact_checker}")
    print(f"Output: {output_dir}")
    print(f"{'='*80}\n")

    # Find files to check
    files_to_check = find_chapter_files(
        model_outputs_dir,
        chapter_key=args.chapter,
        model_id=args.model_id
    )

    if not files_to_check:
        print("❌ No chapter files found to fact-check")
        return 1

    print(f"Found {len(files_to_check)} chapters to fact-check\n")

    # Process each chapter
    results = []
    for i, file_info in enumerate(files_to_check, 1):
        model_id = file_info["model_id"]
        chapter_key = file_info["chapter_key"]
        file_path = file_info["file_path"]

        print(f"[{i}/{len(files_to_check)}] Checking {model_id}/{chapter_key}...", end=" ", flush=True)

        # Read chapter content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                chapter_content = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            continue

        # Skip empty or very short chapters
        if len(chapter_content.strip()) < 100:
            print("⚠️  Skipped (too short)")
            continue

        # Fact-check
        fact_check_result = fact_check_chapter(chapter_content, args.fact_checker)

        # Add metadata
        fact_check_result.update({
            "model_id": model_id,
            "chapter_key": chapter_key,
            "file_path": str(file_path),
            "word_count": len(chapter_content.split()),
            "checked_at": datetime.now().isoformat()
        })

        results.append(fact_check_result)

        # Print summary
        errors = fact_check_result.get("errors_found", 0)
        if errors == 0:
            print("✅ No errors")
        else:
            error_rate = fact_check_result.get("error_rate", 0)
            print(f"⚠️  {errors} issues ({error_rate:.2f} per 1000 words)")

        # Save individual result
        result_file = output_dir / f"{model_id}_{chapter_key}_factcheck.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(fact_check_result, f, indent=2)

    # Save summary
    summary_file = output_dir / "fact_check_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "fact_checker_model": args.fact_checker,
            "total_chapters_checked": len(results),
            "results": results
        }, f, indent=2)

    # Print summary statistics
    print(f"\n{'='*80}")
    print(f"FACT-CHECKING COMPLETE")
    print(f"{'='*80}\n")

    total_errors = sum(r.get("errors_found", 0) for r in results)
    chapters_with_errors = sum(1 for r in results if r.get("errors_found", 0) > 0)

    print(f"Chapters checked: {len(results)}")
    print(f"Chapters with errors: {chapters_with_errors} ({chapters_with_errors/len(results)*100:.1f}%)")
    print(f"Total errors found: {total_errors}")
    print(f"Average errors per chapter: {total_errors/len(results):.2f}")
    print(f"\nResults saved to: {summary_file}")
    print(f"{'='*80}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
