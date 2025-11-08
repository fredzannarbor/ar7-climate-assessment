#!/usr/bin/env python3
"""
run_ar7_full_comparison.py

Full end-to-end AR7 multi-model comparison with all 7 models.
Generates comprehensive comparison tables and performance metrics.

Usage:
    # Run with 2 test chapters (quick validation)
    uv run python run_ar7_full_comparison.py --test-chapters 2

    # Run with all 30 chapters (full generation)
    uv run python run_ar7_full_comparison.py --all-chapters

    # Run with custom chapter selection
    uv run python run_ar7_full_comparison.py \
        --chapters "summary_for_policymakers,technical_summary,chapter_1_point_of_departure"
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import time

# Model configurations
MODELS = {
    "openai_gpt5": {
        "lite": "openai/gpt-5-mini",
        "provider": "USA - OpenAI",
        "nation": "USA",
        "company": "OpenAI"
    },
    "anthropic_haiku45": {
        "lite": "anthropic/claude-haiku-4-5-20251001",
        "provider": "USA - Anthropic",
        "nation": "USA",
        "company": "Anthropic"
    },
    "xai_grok3": {
        "lite": "xai/grok-3-latest",
        "provider": "USA - xAI (Elon Musk)",
        "nation": "USA",
        "company": "xAI"
    },
    "google_gemini": {
        "lite": "gemini/gemini-2.5-flash",
        "provider": "USA - Google",
        "nation": "USA",
        "company": "Google"
    },
    "deepseek": {
        "lite": "huggingface/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "provider": "China - DeepSeek",
        "nation": "China",
        "company": "DeepSeek"
    },
    "mistral": {
        "lite": "deepinfra/mistralai/Mistral-7B-Instruct-v0.3",
        "provider": "Europe - Mistral (France)",
        "nation": "France",
        "company": "Mistral AI"
    },
    "qwen": {
        "lite": "deepinfra/Qwen/Qwen2.5-7B-Instruct",
        "provider": "China - Qwen (Alibaba)",
        "nation": "China",
        "company": "Alibaba"
    }
}

# Default test chapters (2 for quick validation)
DEFAULT_TEST_CHAPTERS = [
    "summary_for_policymakers",
    "technical_summary"
]

# Minimum word count threshold for success
MIN_WORDS_PER_CHAPTER = 500  # Anything less is considered a failure


def run_generation(output_dir: Path, chapters: List[str]) -> Dict:
    """Run generation phase for all models"""

    print(f"\n{'='*80}")
    print(f"PHASE 1: GENERATION")
    print(f"{'='*80}")
    print(f"Models: {len(MODELS)}")
    print(f"Chapters: {len(chapters)}")
    print(f"Total outputs: {len(MODELS) * len(chapters)}")
    print(f"Output dir: {output_dir}")
    print(f"{'='*80}\n")

    model_outputs_dir = output_dir / "model_outputs"

    cmd = [
        "uv", "run", "python", "run_ar7_multimodel_comparison.py",
        "--validation-run",
        "--chapters", ",".join(chapters),
        "--output-dir", str(model_outputs_dir)
    ]

    print(f"Running: {' '.join(cmd)}\n")

    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    duration = time.time() - start_time

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    return {
        "success": result.returncode == 0,
        "duration": duration,
        "command": " ".join(cmd),
        "returncode": result.returncode
    }


def analyze_generation_results(output_dir: Path, min_words: int = MIN_WORDS_PER_CHAPTER) -> Dict:
    """Analyze generation outputs and create performance metrics

    Args:
        output_dir: Directory containing model outputs
        min_words: Minimum words per chapter to consider successful
    """

    print(f"\n{'='*80}")
    print(f"ANALYZING GENERATION RESULTS")
    print(f"{'='*80}")
    print(f"Minimum words threshold: {min_words} per chapter\n")

    model_outputs_dir = output_dir / "model_outputs"
    results = {
        "models": {},
        "summary": {
            "total_models": len(MODELS),
            "successful_models": 0,
            "failed_models": 0,
            "total_chapters": 0,
            "total_words": 0,
            "min_words_threshold": min_words
        }
    }

    for model_id in MODELS.keys():
        model_dir = model_outputs_dir / model_id

        if not model_dir.exists():
            print(f"❌ {model_id}: No output directory found")
            results["models"][model_id] = {
                "status": "failed",
                "error": "No output directory",
                "failure_reason": "no_output_directory"
            }
            results["summary"]["failed_models"] += 1
            continue

        # Find generated chapters
        raw_json_dir = model_dir / "raw_json_responses"
        if not raw_json_dir.exists():
            print(f"❌ {model_id}: No raw_json_responses directory")
            results["models"][model_id] = {
                "status": "failed",
                "error": "No raw_json_responses directory",
                "failure_reason": "no_responses_directory"
            }
            results["summary"]["failed_models"] += 1
            continue

        chapter_files = list(raw_json_dir.glob("*.txt"))

        if not chapter_files:
            print(f"❌ {model_id}: No chapter files generated")
            results["models"][model_id] = {
                "status": "failed",
                "error": "No chapters generated",
                "failure_reason": "no_chapters_generated"
            }
            results["summary"]["failed_models"] += 1
            continue

        # Count words in each chapter
        total_words = 0
        chapters = {}
        chapters_below_threshold = 0

        for chapter_file in chapter_files:
            try:
                content = chapter_file.read_text(encoding='utf-8')
                word_count = len(content.split())
                total_words += word_count

                chapter_name = chapter_file.stem.split('_', 6)[-1] if '_' in chapter_file.stem else chapter_file.stem

                is_below_threshold = word_count < min_words
                if is_below_threshold:
                    chapters_below_threshold += 1

                chapters[chapter_name] = {
                    "file": str(chapter_file),
                    "words": word_count,
                    "below_threshold": is_below_threshold
                }
            except Exception as e:
                print(f"⚠️  {model_id}/{chapter_file.name}: Error reading - {e}")

        # Determine overall status
        avg_words = total_words / len(chapters) if chapters else 0

        # Consider it a failure if:
        # 1. Average words per chapter is below threshold
        # 2. More than half the chapters are below threshold
        if avg_words < min_words or chapters_below_threshold > len(chapters) / 2:
            status = "failed"
            results["summary"]["failed_models"] += 1
            failure_reason = f"avg_words_too_low ({avg_words:.0f} < {min_words})"
            print(f"❌ {model_id}: {len(chapters)} chapters, {total_words:,} words (FAILED - too short)")
        else:
            status = "success"
            results["summary"]["successful_models"] += 1
            results["summary"]["total_chapters"] += len(chapters)
            results["summary"]["total_words"] += total_words
            failure_reason = None
            print(f"✅ {model_id}: {len(chapters)} chapters, {total_words:,} words")

        results["models"][model_id] = {
            "status": status,
            "model_name": MODELS[model_id]["lite"],
            "provider": MODELS[model_id]["provider"],
            "nation": MODELS[model_id]["nation"],
            "company": MODELS[model_id]["company"],
            "chapters_generated": len(chapters),
            "chapters_below_threshold": chapters_below_threshold,
            "total_words": total_words,
            "avg_words_per_chapter": avg_words,
            "chapters": chapters,
            "failure_reason": failure_reason
        }

    return results


def generate_comparison_tables(results: Dict, output_dir: Path):
    """Generate markdown comparison tables"""

    print(f"\n{'='*80}")
    print(f"GENERATING COMPARISON TABLES")
    print(f"{'='*80}\n")

    tables_dir = output_dir / "comparison_tables"
    tables_dir.mkdir(exist_ok=True)

    min_words = results['summary']['min_words_threshold']

    # Table 1: Model Performance Summary
    performance_md = "# AR7 Model Performance Summary\n\n"
    performance_md += f"**Generated:** {datetime.now().isoformat()}\n"
    performance_md += f"**Minimum Words Threshold:** {min_words} per chapter\n\n"
    performance_md += "## Overall Summary\n\n"
    performance_md += f"- **Total Models:** {results['summary']['total_models']}\n"
    performance_md += f"- **Successful:** {results['summary']['successful_models']} ✅\n"
    performance_md += f"- **Failed:** {results['summary']['failed_models']} ❌\n"
    performance_md += f"- **Total Chapters (from successful models):** {results['summary']['total_chapters']}\n"
    performance_md += f"- **Total Words (from successful models):** {results['summary']['total_words']:,}\n\n"

    performance_md += "## Model Performance\n\n"
    performance_md += "| Model | Provider | Status | Chapters | Total Words | Avg Words/Chapter | Notes |\n"
    performance_md += "|-------|----------|--------|----------|-------------|-------------------|-------|\n"

    for model_id, model_data in sorted(results["models"].items()):
        if model_data["status"] == "success":
            performance_md += f"| {model_id} | {model_data['provider']} | ✅ Success | "
            performance_md += f"{model_data['chapters_generated']} | "
            performance_md += f"{model_data['total_words']:,} | "
            performance_md += f"{model_data['avg_words_per_chapter']:.0f} | - |\n"
        else:
            error_msg = model_data.get('failure_reason') or model_data.get('error', 'Unknown error')
            performance_md += f"| {model_id} | {MODELS[model_id]['provider']} | "
            performance_md += f"❌ Failed | "

            # Show what was generated even if failed
            if model_data.get('chapters_generated', 0) > 0:
                performance_md += f"{model_data['chapters_generated']} | "
                performance_md += f"{model_data['total_words']:,} | "
                performance_md += f"{model_data['avg_words_per_chapter']:.0f} | "
            else:
                performance_md += "- | - | - | "

            performance_md += f"{error_msg} |\n"

    performance_file = tables_dir / "model_performance.md"
    performance_file.write_text(performance_md)
    print(f"✅ Created: {performance_file}")

    # Table 2: Cross-Model Comparison by Nation (successful models only)
    nation_md = "# AR7 Model Comparison by Nation\n\n"
    nation_md += f"**Generated:** {datetime.now().isoformat()}\n"
    nation_md += f"**Note:** Only includes successful models (>{min_words} words/chapter average)\n\n"

    # Group by nation (successful only)
    by_nation = {}
    for model_id, model_data in results["models"].items():
        if model_data["status"] == "success":
            nation = model_data["nation"]
            if nation not in by_nation:
                by_nation[nation] = []
            by_nation[nation].append({
                "model_id": model_id,
                "company": model_data["company"],
                "chapters": model_data["chapters_generated"],
                "words": model_data["total_words"]
            })

    if by_nation:
        nation_md += "## Performance by Nation (Successful Models Only)\n\n"
        nation_md += "| Nation | Models | Total Chapters | Total Words | Avg Words/Model |\n"
        nation_md += "|--------|--------|----------------|-------------|------------------|\n"

        for nation in sorted(by_nation.keys()):
            models = by_nation[nation]
            total_chapters = sum(m["chapters"] for m in models)
            total_words = sum(m["words"] for m in models)
            avg_words = total_words / len(models)

            nation_md += f"| {nation} | {len(models)} | {total_chapters} | "
            nation_md += f"{total_words:,} | {avg_words:,.0f} |\n"

        nation_md += "\n## Detailed Breakdown\n\n"
        for nation in sorted(by_nation.keys()):
            nation_md += f"### {nation}\n\n"
            nation_md += "| Model | Company | Chapters | Words |\n"
            nation_md += "|-------|---------|----------|-------|\n"

            for model in by_nation[nation]:
                nation_md += f"| {model['model_id']} | {model['company']} | "
                nation_md += f"{model['chapters']} | {model['words']:,} |\n"

            nation_md += "\n"
    else:
        nation_md += "⚠️ No models met the success criteria.\n"

    nation_file = tables_dir / "nation_comparison.md"
    nation_file.write_text(nation_md)
    print(f"✅ Created: {nation_file}")

    # Table 3: Chapter-by-Chapter Comparison (successful models only)
    successful_models = [m for m in results["models"].values() if m["status"] == "success"]
    if successful_models and len(successful_models) > 0:
        # Get all unique chapters
        all_chapters = set()
        for model_data in successful_models:
            all_chapters.update(model_data["chapters"].keys())

        if all_chapters:
            chapter_md = "# AR7 Chapter-by-Chapter Comparison\n\n"
            chapter_md += f"**Generated:** {datetime.now().isoformat()}\n"
            chapter_md += f"**Note:** Only includes successful models (>{min_words} words/chapter average)\n\n"

            for chapter in sorted(all_chapters):
                chapter_md += f"## {chapter}\n\n"
                chapter_md += "| Model | Words | Provider | Status |\n"
                chapter_md += "|-------|-------|----------|--------|\n"

                chapter_words = []
                for model_id, model_data in sorted(results["models"].items()):
                    if model_data["status"] == "success" and chapter in model_data["chapters"]:
                        words = model_data["chapters"][chapter]["words"]
                        below_threshold = model_data["chapters"][chapter]["below_threshold"]
                        chapter_words.append((model_id, words, model_data["provider"], below_threshold))

                # Sort by word count descending
                for model_id, words, provider, below_threshold in sorted(chapter_words, key=lambda x: x[1], reverse=True):
                    status_icon = "⚠️ Short" if below_threshold else "✅ OK"
                    chapter_md += f"| {model_id} | {words:,} | {provider} | {status_icon} |\n"

                chapter_md += "\n"

            chapter_file = tables_dir / "chapter_comparison.md"
            chapter_file.write_text(chapter_md)
            print(f"✅ Created: {chapter_file}")
    else:
        print(f"⚠️  No successful models - skipping chapter comparison")

    # Save JSON results
    json_file = tables_dir / "results.json"
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✅ Created: {json_file}")

    return {
        "performance": performance_file,
        "nation": nation_file,
        "chapter": chapter_file if successful_models and all_chapters else None,
        "json": json_file
    }


def main():
    parser = argparse.ArgumentParser(
        description="AR7 Full Multi-Model Comparison with Analysis",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--test-chapters",
        type=int,
        help="Run quick test with N chapters (uses default 2: SPM + TS)"
    )
    parser.add_argument(
        "--all-chapters",
        action="store_true",
        help="Run all 30 chapters (full generation)"
    )
    parser.add_argument(
        "--chapters",
        help="Comma-separated list of specific chapters to generate"
    )
    parser.add_argument(
        "--output-dir",
        default="output/ar7_full_run",
        help="Working directory for all outputs"
    )
    parser.add_argument(
        "--skip-generation",
        action="store_true",
        help="Skip generation, only analyze existing results"
    )
    parser.add_argument(
        "--min-words",
        type=int,
        default=MIN_WORDS_PER_CHAPTER,
        help=f"Minimum words per chapter to consider successful (default: {MIN_WORDS_PER_CHAPTER})"
    )

    args = parser.parse_args()

    # Determine chapters to generate
    if args.chapters:
        chapters = [c.strip() for c in args.chapters.split(',')]
    elif args.test_chapters:
        chapters = DEFAULT_TEST_CHAPTERS[:args.test_chapters]
    elif args.all_chapters:
        # Would need to load all 30 from prompts file
        print("ERROR: --all-chapters not yet implemented. Use --chapters to specify.")
        return 1
    else:
        # Default to 2 test chapters
        chapters = DEFAULT_TEST_CHAPTERS

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*80}")
    print(f"AR7 FULL MULTI-MODEL COMPARISON")
    print(f"{'='*80}")
    print(f"Chapters: {len(chapters)}")
    print(f"Models: {len(MODELS)}")
    print(f"Total outputs expected: {len(chapters) * len(MODELS)}")
    print(f"Minimum words threshold: {args.min_words}")
    print(f"Output directory: {output_dir}")
    print(f"{'='*80}\n")

    # Phase 1: Generation
    if not args.skip_generation:
        gen_result = run_generation(output_dir, chapters)

        if not gen_result["success"]:
            print(f"\n❌ Generation failed with return code {gen_result['returncode']}")
            return 1

        print(f"\n✅ Generation completed in {gen_result['duration']:.1f}s")
    else:
        print("\n⏭️  Skipping generation (--skip-generation)")

    # Phase 2: Analysis
    results = analyze_generation_results(output_dir, min_words=args.min_words)

    # Phase 3: Generate Tables
    table_files = generate_comparison_tables(results, output_dir)

    # Final Summary
    print(f"\n{'='*80}")
    print(f"COMPARISON COMPLETE")
    print(f"{'='*80}\n")

    print(f"📊 Summary:")
    print(f"   Successful models: {results['summary']['successful_models']}/{results['summary']['total_models']}")
    print(f"   Failed models: {results['summary']['failed_models']}/{results['summary']['total_models']}")
    print(f"   Total chapters (successful): {results['summary']['total_chapters']}")
    print(f"   Total words (successful): {results['summary']['total_words']:,}")
    if results['summary']['successful_models'] > 0:
        print(f"   Average per successful model: {results['summary']['total_words'] / results['summary']['successful_models']:,.0f} words")

    print(f"\n📁 Comparison Tables:")
    print(f"   Performance: {table_files['performance']}")
    print(f"   By Nation: {table_files['nation']}")
    if table_files['chapter']:
        print(f"   By Chapter: {table_files['chapter']}")
    print(f"   JSON Results: {table_files['json']}")

    print(f"\n{'='*80}\n")

    return 0 if results['summary']['failed_models'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
