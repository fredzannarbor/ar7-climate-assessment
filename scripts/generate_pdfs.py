#!/usr/bin/env python3
"""
generate_pdfs.py

Convert markdown books to PDF using pandoc.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


def markdown_to_pdf(markdown_file: Path, output_file: Path) -> bool:
    """Convert markdown to PDF using pandoc"""

    print(f"Converting {markdown_file.name} to PDF...")

    try:
        # Check if pandoc is available
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: pandoc not found. Install with: brew install pandoc")
        return False

    # Pandoc command with nice formatting
    cmd = [
        "pandoc",
        str(markdown_file),
        "-o", str(output_file),
        "--pdf-engine=xelatex",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
        "-V", "documentclass=report",
        "--toc",
        "--toc-depth=2",
        "-V", "linkcolor=blue",
        "-V", "urlcolor=blue"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            print(f"  ✅ Created: {output_file}")
            return True
        else:
            print(f"  ❌ Error: {result.stderr}")
            # Try without xelatex
            print("  Retrying with pdflatex...")
            cmd[3] = "--pdf-engine=pdflatex"
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                print(f"  ✅ Created: {output_file}")
                return True
            else:
                print(f"  ❌ Failed: {result.stderr}")
                return False

    except subprocess.TimeoutExpired:
        print(f"  ❌ Timeout converting {markdown_file.name}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate PDFs from markdown books")
    parser.add_argument("--output-dir", default="output/ar7_complete_run_final")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)

    if not output_dir.exists():
        print(f"ERROR: Output directory not found: {output_dir}")
        return 1

    print(f"\n{'='*80}")
    print(f"GENERATING PDFS")
    print(f"{'='*80}\n")

    # Find all markdown books
    markdown_books = list(output_dir.glob("*/AR7_COMPLETE_BOOK_*.md"))

    if not markdown_books:
        print("No markdown books found. Looking for compiled books...")
        markdown_books = list(output_dir.glob("**/AR7_*.md"))

    if not markdown_books:
        print("ERROR: No markdown books found")
        return 1

    print(f"Found {len(markdown_books)} markdown book(s)\n")

    # Convert each book
    pdf_dir = output_dir / "pdfs"
    pdf_dir.mkdir(exist_ok=True)

    successful = 0
    failed = 0

    for md_file in markdown_books:
        pdf_file = pdf_dir / md_file.with_suffix('.pdf').name

        if markdown_to_pdf(md_file, pdf_file):
            successful += 1
        else:
            failed += 1

    # Also convert the comparison report
    report_file = output_dir / "AR7_FINAL_COMPARISON_REPORT.md"
    if report_file.exists():
        pdf_file = pdf_dir / "AR7_FINAL_COMPARISON_REPORT.pdf"
        if markdown_to_pdf(report_file, pdf_file):
            successful += 1
        else:
            failed += 1

    print(f"\n{'='*80}")
    print(f"PDF GENERATION COMPLETE")
    print(f"{'='*80}\n")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"\nPDFs saved to: {pdf_dir}")
    print(f"{'='*80}\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
