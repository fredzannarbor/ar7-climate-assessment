#!/usr/bin/env python3
"""
run_ar7_test_validation.py

Run a complete validation test of the AR7 multi-model comparison pipeline:
1. Generate 2-3 chapters with all working models
2. Fact-check the generated chapters
3. Assess quality
4. Generate comparison report
5. Assemble test book for one model

Usage:
    # Full validation with all models
    uv run python run_ar7_test_validation.py

    # Quick test with just one model
    uv run python run_ar7_test_validation.py --quick --model google_gemini3
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List


def run_command(cmd: List[str], description: str, timeout: int = 600) -> Dict:
    """Run a command and return results"""
    print(f"\n{'='*80}")
    print(f"🔧 {description}")
    print(f"{'='*80}")
    print(f"Command: {' '.join(cmd)}\n")

    start_time = datetime.now()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return {
            "success": result.returncode == 0,
            "duration": duration,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Timeout after {timeout}s",
            "duration": timeout
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "duration": 0
        }


def main():
    parser = argparse.ArgumentParser(
        description="AR7 Complete Validation Test",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick test with just 2 chapters and 1 model"
    )
    parser.add_argument(
        "--model",
        default="google_gemini3",
        help="Model to use for quick test"
    )
    parser.add_argument(
        "--chapters",
        default="summary_for_policymakers,technical_summary",
        help="Comma-separated chapter keys for validation"
    )
    parser.add_argument(
        "--output-dir",
        default="output/ar7_validation_test",
        help="Output directory for validation test"
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Track results
    results = {
        "started_at": datetime.now().isoformat(),
        "mode": "quick" if args.quick else "full",
        "steps": []
    }

    print(f"\n{'='*80}")
    print(f"AR7 VALIDATION TEST")
    print(f"{'='*80}")
    print(f"Mode: {'QUICK (1 model, 2 chapters)' if args.quick else 'FULL (all models, 2 chapters)'}")
    print(f"Output: {output_dir}")
    print(f"{'='*80}\n")

    # Step 1: Generate chapters
    print("\n📝 STEP 1: GENERATE CHAPTERS")
    if args.quick:
        # Single model test
        gen_cmd = [
            "uv", "run", "python", "run_ar7_multimodel_comparison.py",
            "--model", args.model,
            "--chapters", args.chapters,
            "--output-dir", str(output_dir / "model_outputs")
        ]
    else:
        # All models validation run
        gen_cmd = [
            "uv", "run", "python", "run_ar7_multimodel_comparison.py",
            "--validation-run",
            "--chapters", args.chapters,
            "--output-dir", str(output_dir / "model_outputs")
        ]

    gen_result = run_command(gen_cmd, "Generating chapters", timeout=1200)
    results["steps"].append({"step": "generation", "result": gen_result})

    if not gen_result["success"]:
        print(f"\n❌ Generation failed: {gen_result.get('error', 'Unknown error')}")
        results["status"] = "FAILED_AT_GENERATION"
        results["completed_at"] = datetime.now().isoformat()

        # Save results
        with open(output_dir / "validation_results.json", 'w') as f:
            json.dump(results, f, indent=2)

        return 1

    # Step 2: Fact-check chapters
    print("\n🔍 STEP 2: FACT-CHECK CHAPTERS")
    fact_check_cmd = [
        "uv", "run", "python", "run_ar7_fact_checking.py",
        "--model-outputs", str(output_dir / "model_outputs"),
        "--output-dir", str(output_dir / "fact_checking")
    ]

    if args.quick:
        fact_check_cmd.extend(["--model-id", args.model])

    fact_result = run_command(fact_check_cmd, "Fact-checking chapters", timeout=900)
    results["steps"].append({"step": "fact_checking", "result": fact_result})

    # Step 3: Quality assessment
    print("\n⭐ STEP 3: QUALITY ASSESSMENT")
    quality_cmd = [
        "uv", "run", "python", "run_ar7_quality_assessment.py",
        "--model-outputs", str(output_dir / "model_outputs"),
        "--fact-check-results", str(output_dir / "fact_checking"),
        "--output", str(output_dir / "quality_assessment")
    ]

    if args.quick:
        quality_cmd.extend(["--chapter", args.chapters.split(',')[0]])

    quality_result = run_command(quality_cmd, "Assessing quality", timeout=900)
    results["steps"].append({"step": "quality_assessment", "result": quality_result})

    # Step 4: Generate comparison report
    print("\n📊 STEP 4: GENERATE COMPARISON REPORT")

    # Create a simple markdown report
    report_path = output_dir / "VALIDATION_REPORT.md"

    with open(report_path, 'w') as f:
        f.write(f"# AR7 Validation Test Report\n\n")
        f.write(f"**Date:** {datetime.now().isoformat()}\n")
        f.write(f"**Mode:** {'Quick (1 model)' if args.quick else 'Full (all models)'}\n")
        f.write(f"**Chapters:** {args.chapters}\n\n")

        f.write(f"## Test Results\n\n")

        for step in results["steps"]:
            step_name = step["step"].replace("_", " ").title()
            step_result = step["result"]
            status = "✅ PASSED" if step_result["success"] else "❌ FAILED"
            duration = step_result.get("duration", 0)

            f.write(f"### {step_name}\n")
            f.write(f"- **Status:** {status}\n")
            f.write(f"- **Duration:** {duration:.1f}s\n")

            if not step_result["success"]:
                f.write(f"- **Error:** {step_result.get('error', 'Unknown')}\n")

            f.write(f"\n")

        f.write(f"## Next Steps\n\n")
        f.write(f"1. Review generated chapters in `model_outputs/`\n")
        f.write(f"2. Check fact-checking results in `fact_checking/`\n")
        f.write(f"3. Review quality scores in `quality_assessment/`\n")
        f.write(f"4. If validation passes, run full generation\n")

    print(f"\n📄 Report generated: {report_path}")

    # Step 5: Copy to GitHub repo structure
    print("\n📦 STEP 5: ORGANIZE FOR GITHUB REPO")

    github_repo = Path("/Users/fred/xcu_my_apps/nimble/ar7-model-comparison")
    if github_repo.exists():
        print(f"Copying prompts to GitHub repo...")

        # Copy prompts
        import shutil
        prompts_src = Path("prompts/ar7_model_comparison_prompts.json")
        if prompts_src.exists():
            shutil.copy(prompts_src, github_repo / "prompts/")
            print(f"✅ Copied prompts")

        # Copy validation report
        shutil.copy(report_path, github_repo / "docs/VALIDATION_REPORT.md")
        print(f"✅ Copied validation report")

        print(f"\nGitHub repo ready at: {github_repo}")

    # Final summary
    results["completed_at"] = datetime.now().isoformat()
    results["status"] = "COMPLETED"

    all_success = all(step["result"]["success"] for step in results["steps"])

    print(f"\n{'='*80}")
    print(f"VALIDATION TEST {'✅ PASSED' if all_success else '⚠️ PARTIAL'}")
    print(f"{'='*80}\n")

    print(f"Steps completed: {sum(1 for s in results['steps'] if s['result']['success'])}/{len(results['steps'])}")
    print(f"Total duration: {(datetime.fromisoformat(results['completed_at']) - datetime.fromisoformat(results['started_at'])).total_seconds():.1f}s")
    print(f"\nFull results: {output_dir / 'validation_results.json'}")
    print(f"Report: {report_path}")
    print(f"\n{'='*80}\n")

    # Save final results
    with open(output_dir / "validation_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
