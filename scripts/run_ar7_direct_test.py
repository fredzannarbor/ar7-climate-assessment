#!/usr/bin/env python3
"""
run_ar7_direct_test.py

Direct end-to-end test that generates AR7 chapters for all models
without relying on external pipeline scripts.
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add nimble/codexes-factory/src to path
sys.path.insert(0, str(Path(__file__).parent / "nimble" / "codexes-factory" / "src"))

try:
    from nimble_llm_caller import llm_call_with_structured_output
except ImportError:
    print("ERROR: nimble-llm-caller not available. Using basic litellm...")
    import litellm
    def llm_call_with_structured_output(messages, model, **kwargs):
        response = litellm.completion(model=model, messages=messages, **kwargs)
        return response.choices[0].message.content

# Model configurations
MODELS = {
    "gemini_flash": "gemini/gemini-2.5-flash",
    "anthropic_haiku": "anthropic/claude-haiku-4-5-20251001",
    "openai_mini": "openai/gpt-5-mini",
}

def generate_chapter(chapter_key: str, prompt_data: Dict, model_name: str, output_dir: Path) -> Dict:
    """Generate a single chapter using specified model"""

    print(f"  📝 Generating: {chapter_key}")

    # Get messages from prompt
    messages = prompt_data.get("messages", [])
    params = prompt_data.get("params", {})

    if not messages:
        return {
            "success": False,
            "error": "No messages in prompt data"
        }

    # Generate
    start_time = time.time()
    try:
        response = llm_call_with_structured_output(
            messages=messages,
            model=model_name,
            temperature=params.get("temperature", 0.3),
            max_tokens=params.get("max_tokens", 12000)
        )

        duration = time.time() - start_time
        word_count = len(response.split())

        # Save response
        output_file = output_dir / f"{chapter_key}.txt"
        output_file.write_text(response, encoding='utf-8')

        # Save metadata
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

        print(f"    ✅ {word_count} words in {duration:.1f}s")

        return {
            "success": True,
            "chapter_key": chapter_key,
            "word_count": word_count,
            "duration": duration,
            "output_file": str(output_file)
        }

    except Exception as e:
        print(f"    ❌ ERROR: {e}")
        return {
            "success": False,
            "chapter_key": chapter_key,
            "error": str(e)
        }


def generate_all_chapters(model_id: str, model_name: str, prompts_data: Dict,
                         output_dir: Path, chapters: List[str] = None) -> Dict:
    """Generate all chapters for a single model"""

    print(f"\n{'='*80}")
    print(f"MODEL: {model_id} ({model_name})")
    print(f"{'='*80}")

    model_output_dir = output_dir / model_id
    model_output_dir.mkdir(parents=True, exist_ok=True)

    # Determine chapters to generate
    if chapters:
        chapter_keys = chapters
    else:
        chapter_keys = prompts_data.get("prompt_keys", [])

    print(f"Chapters to generate: {len(chapter_keys)}\n")

    results = []
    for chapter_key in chapter_keys:
        if chapter_key not in prompts_data:
            print(f"  ⚠️  Skipping {chapter_key} - not in prompts file")
            continue

        result = generate_chapter(
            chapter_key=chapter_key,
            prompt_data=prompts_data[chapter_key],
            model_name=model_name,
            output_dir=model_output_dir
        )
        results.append(result)

        # Brief pause to avoid rate limits
        time.sleep(1)

    # Calculate summary
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

    # Save summary
    summary_file = model_output_dir / "generation_summary.json"
    summary_file.write_text(json.dumps(summary, indent=2), encoding='utf-8')

    print(f"\n{'='*80}")
    print(f"SUMMARY: {model_id}")
    print(f"  ✅ Successful: {len(successful)}/{len(results)}")
    print(f"  ❌ Failed: {len(failed)}/{len(results)}")
    print(f"  📊 Total words: {total_words:,}")
    print(f"  ⏱️  Total time: {total_time:.1f}s")
    if successful:
        print(f"  📈 Avg words/chapter: {total_words / len(successful):.0f}")
    print(f"{'='*80}\n")

    return summary


def compile_markdown_book(model_id: str, model_dir: Path, prompts_data: Dict) -> str:
    """Compile all chapters into a single markdown book"""

    print(f"\n📚 Compiling markdown book for {model_id}...")

    book_md = f"# AR7 Working Group II Report\n"
    book_md += f"## Multi-Model Assessment\n\n"
    book_md += f"**Model:** {model_id}\n"
    book_md += f"**Generated:** {datetime.now().isoformat()}\n\n"
    book_md += "---\n\n"

    chapter_keys = prompts_data.get("prompt_keys", [])

    for chapter_key in chapter_keys:
        chapter_file = model_dir / f"{chapter_key}.txt"

        if not chapter_file.exists():
            continue

        # Add chapter heading
        chapter_title = chapter_key.replace("_", " ").title()
        book_md += f"# {chapter_title}\n\n"

        # Add content
        content = chapter_file.read_text(encoding='utf-8')
        book_md += content
        book_md += "\n\n---\n\n"

    # Save compiled book
    book_file = model_dir / f"AR7_COMPLETE_BOOK_{model_id.upper()}.md"
    book_file.write_text(book_md, encoding='utf-8')

    print(f"  ✅ Saved: {book_file}")
    return str(book_file)


def main():
    parser = argparse.ArgumentParser(description="Direct AR7 multi-model test")
    parser.add_argument("--chapters", help="Comma-separated chapter keys (default: all)")
    parser.add_argument("--models", help="Comma-separated model IDs (default: all)")
    parser.add_argument("--output-dir", default="output/ar7_direct_test")
    parser.add_argument("--prompts-file", default="prompts/ar7_model_comparison_prompts.json")
    parser.add_argument("--compile-books", action="store_true",
                       help="Compile markdown books after generation")

    args = parser.parse_args()

    # Load prompts
    prompts_file = Path(args.prompts_file)
    if not prompts_file.exists():
        print(f"ERROR: Prompts file not found: {prompts_file}")
        return 1

    with open(prompts_file) as f:
        prompts_data = json.load(f)

    # Determine models to run
    if args.models:
        model_ids = [m.strip() for m in args.models.split(',')]
        models_to_run = {mid: MODELS[mid] for mid in model_ids if mid in MODELS}
    else:
        models_to_run = MODELS

    # Determine chapters
    chapters = None
    if args.chapters:
        chapters = [c.strip() for c in args.chapters.split(',')]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*80}")
    print(f"AR7 DIRECT MULTI-MODEL TEST")
    print(f"{'='*80}")
    print(f"Models: {len(models_to_run)}")
    print(f"Chapters: {len(chapters) if chapters else len(prompts_data.get('prompt_keys', []))}")
    print(f"Output: {output_dir}")
    print(f"{'='*80}\n")

    # Generate for all models
    all_summaries = []
    for model_id, model_name in models_to_run.items():
        summary = generate_all_chapters(
            model_id=model_id,
            model_name=model_name,
            prompts_data=prompts_data,
            output_dir=output_dir,
            chapters=chapters
        )
        all_summaries.append(summary)

    # Compile markdown books if requested
    if args.compile_books:
        print(f"\n{'='*80}")
        print("COMPILING MARKDOWN BOOKS")
        print(f"{'='*80}")

        for summary in all_summaries:
            model_dir = output_dir / summary["model_id"]
            if model_dir.exists():
                compile_markdown_book(summary["model_id"], model_dir, prompts_data)

    # Final report
    print(f"\n{'='*80}")
    print("FINAL REPORT")
    print(f"{'='*80}\n")

    for summary in all_summaries:
        status = "✅" if summary["failed"] == 0 else "⚠️"
        print(f"{status} {summary['model_id']}: {summary['successful']}/{summary['total_chapters']} chapters, {summary['total_words']:,} words")

    # Save master summary
    master_summary = {
        "generated_at": datetime.now().isoformat(),
        "models": all_summaries,
        "total_models": len(all_summaries),
        "total_chapters": sum(s["total_chapters"] for s in all_summaries),
        "total_words": sum(s["total_words"] for s in all_summaries)
    }

    master_file = output_dir / "MASTER_SUMMARY.json"
    master_file.write_text(json.dumps(master_summary, indent=2), encoding='utf-8')

    print(f"\n📊 Master summary: {master_file}")
    print(f"{'='*80}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
