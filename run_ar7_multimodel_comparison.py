#!/usr/bin/env python3
"""
run_ar7_multimodel_comparison.py

Multi-model comparison script for AR7 climate assessment generation.
Tests 7 foundation models on identical factual assessment prompts.

Usage:
    # Validation run with all flash/lite models
    uv run python run_ar7_multimodel_comparison.py --validation-run

    # Full generation with all premium models
    uv run python run_ar7_multimodel_comparison.py --full-run

    # Single model test
    uv run python run_ar7_multimodel_comparison.py --model gemini/gemini-2.5-flash
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Model configurations
MODELS = {
    "openai_gpt5": {
        "full": "openai/gpt-5",
        "lite": "openai/gpt-5-mini",
        "provider": "USA - OpenAI",
        "notes": "GPT-5 and GPT-5 mini"
    },
    "anthropic_haiku45": {
        "full": "anthropic/claude-sonnet-4-20250514",
        "lite": "anthropic/claude-haiku-4-5-20251001",
        "provider": "USA - Anthropic",
        "notes": "Haiku 4.5 for flash, Sonnet 4 for premium"
    },
    "xai_grok3": {
        "full": "xai/grok-3-latest",
        "lite": "xai/grok-3-latest",
        "provider": "USA - xAI (Elon Musk)",
        "notes": "Grok 3 latest"
    },
    "google_gemini": {
        "full": "gemini/gemini-2.5-pro",
        "lite": "gemini/gemini-2.5-flash",
        "provider": "USA - Google",
        "notes": "Has web grounding capability"
    },
    "deepseek": {
        "full": "huggingface/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
        "lite": "huggingface/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "provider": "China - DeepSeek",
        "notes": "Chinese perspective via HuggingFace API"
    },
    "mistral": {
        "full": "deepinfra/mistralai/Mixtral-8x7B-Instruct-v0.1",
        "lite": "deepinfra/mistralai/Mistral-7B-Instruct-v0.3",
        "provider": "Europe - Mistral (France)",
        "notes": "European perspective via DeepInfra"
    },
    "qwen": {
        "full": "deepinfra/Qwen/QwQ-32B-Preview",
        "lite": "deepinfra/Qwen/Qwen2.5-7B-Instruct",
        "provider": "China - Qwen (Alibaba)",
        "notes": "Chinese/Asian perspective via DeepInfra - replaces unavailable Falcon"
    }
}

def run_model_generation(model_id: str, model_name: str, output_dir: Path,
                         prompt_file: str, schedule_file: str,
                         chapters: List[str] = None) -> Dict:
    """
    Run generation for a single model

    Args:
        model_id: Model identifier (e.g., 'openai_gpt5')
        model_name: Full model name for litellm (e.g., 'openai/gpt-4o')
        output_dir: Base output directory
        prompt_file: Path to prompts.json
        schedule_file: Path to schedule file
        chapters: List of chapter keys to generate (None = all)

    Returns:
        Dictionary with generation results
    """

    # Create model-specific output directory
    model_output_dir = output_dir / model_id
    model_output_dir.mkdir(parents=True, exist_ok=True)

    # Build command
    cmd = [
        "uv", "run", "python", "run_book_pipeline.py",
        "--imprint", "variant_earth",
        "--schedule-file", schedule_file,
        "--model", model_name,
        "--base-dir", str(model_output_dir),
        "--start-stage", "1",
        "--end-stage", "1",
        "--max-books", "1",
        "--skip-lsi",
        "--overwrite"
    ]

    # Add chapter filter if specified
    if chapters:
        cmd.extend(["--only-run-prompts", ",".join(chapters)])

    print(f"\n{'='*80}")
    print(f"GENERATING WITH: {model_id}")
    print(f"Model: {model_name}")
    print(f"Provider: {MODELS[model_id]['provider']}")
    if chapters:
        print(f"Chapters: {', '.join(chapters[:5])}{'...' if len(chapters) > 5 else ''}")
    else:
        print(f"Chapters: ALL (29 chapters)")
    print(f"Output: {model_output_dir}")
    print(f"{'='*80}\n")

    # Run generation
    start_time = datetime.now()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Parse output for success indicators
        success = "Successfully finished" in result.stdout
        prompts_ok = result.stdout.count("✅") if success else 0

        return {
            "model_id": model_id,
            "model_name": model_name,
            "success": success,
            "prompts_completed": prompts_ok,
            "duration_seconds": duration,
            "output_dir": str(model_output_dir),
            "stdout_sample": result.stdout[-500:] if result.stdout else "",
            "errors": result.stderr if result.returncode != 0 else None
        }
    except subprocess.TimeoutExpired:
        return {
            "model_id": model_id,
            "model_name": model_name,
            "success": False,
            "error": "Timeout after 1 hour",
            "output_dir": str(model_output_dir)
        }
    except Exception as e:
        return {
            "model_id": model_id,
            "model_name": model_name,
            "success": False,
            "error": str(e),
            "output_dir": str(model_output_dir)
        }


def main():
    parser = argparse.ArgumentParser(
        description="AR7 Multi-Model Comparison Generation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--validation-run",
        action="store_true",
        help="Run with all flash/lite models for validation"
    )
    parser.add_argument(
        "--full-run",
        action="store_true",
        help="Run with all premium models for final generation"
    )
    parser.add_argument(
        "--model",
        choices=list(MODELS.keys()),
        help="Generate with single model only"
    )
    parser.add_argument(
        "--chapters",
        help="Comma-separated list of chapter keys (default: all 29)"
    )
    parser.add_argument(
        "--output-dir",
        default="output/ar7_model_comparison",
        help="Base output directory for all model outputs"
    )
    parser.add_argument(
        "--schedule-file",
        default="configs/ar7_base_schedule.json",
        help="Schedule file with base AR7 data (no scenario framing)"
    )
    parser.add_argument(
        "--prompt-file",
        default="imprints/variant_earth/prompts_base_factual.json",
        help="Factual base prompts (no scenario framing)"
    )

    args = parser.parse_args()

    # Parse chapters if specified
    chapters = None
    if args.chapters:
        chapters = [c.strip() for c in args.chapters.split(',')]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine which models to run
    models_to_run = []

    if args.validation_run:
        print("\n🔬 VALIDATION RUN - Using lite/flash models")
        models_to_run = [(mid, MODELS[mid]["lite"]) for mid in MODELS.keys()]
    elif args.full_run:
        print("\n🚀 FULL RUN - Using premium models")
        models_to_run = [(mid, MODELS[mid]["full"]) for mid in MODELS.keys()]
    elif args.model:
        tier = "lite"  # Default to lite for single model test
        models_to_run = [(args.model, MODELS[args.model][tier])]
    else:
        parser.error("Must specify --validation-run, --full-run, or --model")

    # Display plan
    print(f"\n{'='*80}")
    print(f"AR7 MULTI-MODEL COMPARISON GENERATION")
    print(f"{'='*80}")
    print(f"Models to test: {len(models_to_run)}")
    print(f"Chapters per model: {len(chapters) if chapters else 29}")
    print(f"Total chapters: {len(models_to_run) * (len(chapters) if chapters else 29)}")
    print(f"Output directory: {output_dir}")
    print(f"{'='*80}\n")

    # List models
    for mid, mname in models_to_run:
        print(f"  • {mid:<25} {mname:<40} ({MODELS[mid]['provider']})")
    print()

    # Run generations
    results = []
    for model_id, model_name in models_to_run:
        result = run_model_generation(
            model_id=model_id,
            model_name=model_name,
            output_dir=output_dir,
            prompt_file=args.prompt_file,
            schedule_file=args.schedule_file,
            chapters=chapters
        )
        results.append(result)

        # Save intermediate results
        results_file = output_dir / "generation_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "mode": "validation" if args.validation_run else "full",
                "results": results
            }, f, indent=2)

    # Summary report
    print(f"\n{'='*80}")
    print(f"GENERATION COMPLETE")
    print(f"{'='*80}\n")

    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]

    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    print()

    if successful:
        print("Successful generations:")
        for r in successful:
            print(f"  ✅ {r['model_id']}: {r.get('prompts_completed', '?')} chapters in {r.get('duration_seconds', 0):.1f}s")

    if failed:
        print("\nFailed generations:")
        for r in failed:
            print(f"  ❌ {r['model_id']}: {r.get('error', 'Unknown error')}")

    print(f"\nResults saved to: {results_file}")
    print(f"{'='*80}\n")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
