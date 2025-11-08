#!/usr/bin/env python3
"""
run_7model_test.py

Test all 7 models with 3 sample chapters through complete pipeline including PDF generation.
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Load parent environment FIRST
from load_env import load_parent_env
load_parent_env()

sys.path.insert(0, str(Path(__file__).parent / "nimble" / "codexes-factory" / "src"))

try:
    from nimble_llm_caller import llm_call_with_structured_output
except ImportError:
    import litellm
    def llm_call_with_structured_output(messages, model, **kwargs):
        response = litellm.completion(model=model, messages=messages, **kwargs)
        return response.choices[0].message.content

# All 7 models (lite/flash tier)
MODELS = {
    "openai_gpt5_mini": "openai/gpt-5-mini",
    "anthropic_haiku": "anthropic/claude-haiku-4-5-20251001",
    "xai_grok3": "xai/grok-3-latest",
    "google_gemini_flash": "gemini/gemini-2.5-flash",
    "deepseek_7b": "huggingface/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "mistral_7b": "deepinfra/mistralai/Mistral-7B-Instruct-v0.3",
    "qwen_7b": "deepinfra/Qwen/Qwen2.5-7B-Instruct"
}

DEFAULT_CHAPTERS = [
    "summary_for_policymakers",
    "chapter_2_vulnerabilities_impacts_risks",
    "chapter_7_africa"
]


def generate_chapter(chapter_key: str, prompt_data: Dict, model_name: str, output_dir: Path) -> Dict:
    """Generate a single chapter"""
    print(f"    📝 {chapter_key[:40]}...")

    messages = prompt_data.get("messages", [])
    params = prompt_data.get("params", {})

    if not messages:
        return {"success": False, "error": "No messages"}

    start_time = time.time()
    try:
        response = llm_call_with_structured_output(
            messages=messages,
            model=model_name,
            temperature=params.get("temperature", 0.3),
            max_tokens=min(params.get("max_tokens", 12000), 16000)  # Limit for compatibility
        )

        duration = time.time() - start_time
        word_count = len(response.split())

        # Save
        output_file = output_dir / f"{chapter_key}.txt"
        output_file.write_text(response, encoding='utf-8')

        metadata_file = output_dir / f"{chapter_key}_metadata.json"
        metadata = {
            "chapter_key": chapter_key,
            "model": model_name,
            "generated_at": datetime.now().isoformat(),
            "duration_seconds": duration,
            "word_count": word_count,
            "params": params
        }
        metadata_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

        print(f"       ✅ {word_count} words in {duration:.1f}s")

        return {
            "success": True,
            "chapter_key": chapter_key,
            "word_count": word_count,
            "duration": duration,
            "output_file": str(output_file)
        }

    except Exception as e:
        print(f"       ❌ ERROR: {e}")
        return {
            "success": False,
            "chapter_key": chapter_key,
            "error": str(e)
        }


def generate_model(model_id: str, model_name: str, prompts_data: Dict,
                  output_dir: Path, chapters: List[str]) -> Dict:
    """Generate chapters for one model"""

    print(f"\n{'='*80}")
    print(f"MODEL: {model_id} ({model_name})")
    print(f"{'='*80}")

    model_output_dir = output_dir / model_id
    model_output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for chapter_key in chapters:
        if chapter_key not in prompts_data:
            print(f"    ⚠️  Skipping {chapter_key} - not in prompts")
            continue

        result = generate_chapter(chapter_key, prompts_data[chapter_key], model_name, model_output_dir)
        results.append(result)
        time.sleep(1)  # Rate limiting

    # Summary
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    total_words = sum(r.get("word_count", 0) for r in successful)
    total_time = sum(r.get("duration", 0) for r in successful)

    summary = {
        "model_id": model_id,
        "model_name": model_name,
        "total_chapters": len(results),
        "successful": len(successful),
        "failed": len(failed),
        "total_words": total_words,
        "total_time": total_time,
        "avg_words": total_words / len(successful) if successful else 0,
        "results": results
    }

    summary_file = model_output_dir / "generation_summary.json"
    summary_file.write_text(json.dumps(summary, indent=2), encoding='utf-8')

    print(f"  ✅ {len(successful)}/{len(results)} successful, {total_words:,} words")

    return summary


def compile_markdown_book(model_id: str, model_dir: Path, chapters: List[str]) -> str:
    """Compile chapters into markdown book"""

    print(f"  📚 Compiling markdown book for {model_id}...")

    book_md = f"# AR7 Working Group II - 7-Model Test\n\n"
    book_md += f"**Model**: {model_id}\n"
    book_md += f"**Generated**: {datetime.now().isoformat()}\n\n"
    book_md += "---\n\n"

    for chapter_key in chapters:
        chapter_file = model_dir / f"{chapter_key}.txt"
        if not chapter_file.exists():
            continue

        chapter_title = chapter_key.replace("_", " ").title()
        book_md += f"# {chapter_title}\n\n"
        book_md += chapter_file.read_text(encoding='utf-8')
        book_md += "\n\n---\n\n"

    book_file = model_dir / f"AR7_7MODEL_TEST_{model_id.upper()}.md"
    book_file.write_text(book_md, encoding='utf-8')

    return str(book_file)


def generate_pdf(markdown_file: Path, pdf_dir: Path) -> bool:
    """Convert markdown to PDF using pandoc"""

    pdf_file = pdf_dir / markdown_file.with_suffix('.pdf').name

    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except:
        print(f"    ⚠️  Pandoc not available - skipping PDF")
        return False

    cmd = [
        "pandoc", str(markdown_file), "-o", str(pdf_file),
        "--pdf-engine=pdflatex",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
        "--toc"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, timeout=120)
        if result.returncode == 0:
            print(f"    ✅ PDF: {pdf_file.name}")
            return True
        else:
            print(f"    ❌ PDF failed: {result.stderr.decode()[:100]}")
            return False
    except:
        return False


def main():
    parser = argparse.ArgumentParser(description="7-Model AR7 Test")
    parser.add_argument("--chapters", default="summary_for_policymakers,chapter_2_vulnerabilities_impacts_risks,chapter_7_africa")
    parser.add_argument("--output-dir", default="output/ar7_7model_test")
    parser.add_argument("--prompts-file", default="prompts/ar7_model_comparison_prompts.json")

    args = parser.parse_args()

    # Load prompts
    with open(args.prompts_file) as f:
        prompts_data = json.load(f)

    chapters = [c.strip() for c in args.chapters.split(',')]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*80}")
    print(f"AR7 7-MODEL COMPREHENSIVE TEST")
    print(f"{'='*80}")
    print(f"Models: {len(MODELS)}")
    print(f"Chapters: {len(chapters)}")
    print(f"Total outputs: {len(MODELS) * len(chapters)}")
    print(f"Chapters: {', '.join(chapters)}")
    print(f"{'='*80}\n")

    # PHASE 1: Generate all models
    all_summaries = []
    for model_id, model_name in MODELS.items():
        summary = generate_model(model_id, model_name, prompts_data, output_dir, chapters)
        all_summaries.append(summary)

    # PHASE 2: Compile markdown books
    print(f"\n{'='*80}")
    print("PHASE 2: COMPILING MARKDOWN BOOKS")
    print(f"{'='*80}")

    for summary in all_summaries:
        model_dir = output_dir / summary["model_id"]
        if model_dir.exists():
            compile_markdown_book(summary["model_id"], model_dir, chapters)

    # PHASE 3: Generate PDFs
    print(f"\n{'='*80}")
    print("PHASE 3: GENERATING PDFS")
    print(f"{'='*80}")

    pdf_dir = output_dir / "pdfs"
    pdf_dir.mkdir(exist_ok=True)

    for summary in all_summaries:
        model_dir = output_dir / summary["model_id"]
        book_file = model_dir / f"AR7_7MODEL_TEST_{summary['model_id'].upper()}.md"
        if book_file.exists():
            print(f"\n  {summary['model_id']}:")
            generate_pdf(book_file, pdf_dir)

    # PHASE 4: Final report
    print(f"\n{'='*80}")
    print("FINAL REPORT - 7 MODEL TEST")
    print(f"{'='*80}\n")

    for summary in all_summaries:
        status = "✅" if summary["failed"] == 0 else "⚠️"
        print(f"{status} {summary['model_id']:<25} {summary['successful']}/{summary['total_chapters']} chapters, {summary['total_words']:,} words")

    # Save master summary
    master_summary = {
        "generated_at": datetime.now().isoformat(),
        "test_type": "7_model_3_chapter_complete_pipeline",
        "chapters": chapters,
        "models": all_summaries,
        "total_models": len(all_summaries),
        "total_chapters": sum(s["total_chapters"] for s in all_summaries),
        "total_words": sum(s["total_words"] for s in all_summaries)
    }

    master_file = output_dir / "7MODEL_TEST_SUMMARY.json"
    master_file.write_text(json.dumps(master_summary, indent=2), encoding='utf-8')

    print(f"\n📊 Summary: {master_file}")
    print(f"📁 PDFs: {pdf_dir}/")
    print(f"{'='*80}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
