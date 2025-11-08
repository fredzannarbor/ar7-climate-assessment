#!/bin/bash
#
# finalize_test.sh
# Automatically finalize the AR7 test once generation completes
#

set -e

OUTPUT_DIR="output/ar7_complete_run_final"

echo "========================================="
echo "FINALIZING AR7 COMPLETE TEST"
echo "========================================="
echo

# Wait for generation to complete
echo "Waiting for generation to complete..."
while ps aux | grep -q "[r]un_ar7_direct"; do
    sleep 10
done

echo "✅ Generation complete!"
echo

# Generate final comparison report
echo "Generating final comparison report..."
uv run python generate_final_report.py --output-dir "$OUTPUT_DIR"
echo

# Generate PDFs (if pandoc is available)
echo "Generating PDFs..."
if command -v pandoc &> /dev/null; then
    uv run python generate_pdfs.py --output-dir "$OUTPUT_DIR"
else
    echo "⚠️  Pandoc not found - skipping PDF generation"
    echo "   Install with: brew install pandoc"
fi
echo

# Show final statistics
echo "========================================="
echo "FINAL STATISTICS"
echo "========================================="
echo

find "$OUTPUT_DIR" -name "*.txt" | wc -l | xargs echo "Total chapter files:"
find "$OUTPUT_DIR" -name "generation_summary.json" | wc -l | xargs echo "Models completed:"
find "$OUTPUT_DIR" -name "AR7_COMPLETE_BOOK_*.md" | wc -l | xargs echo "Markdown books:"

echo
echo "========================================="
echo "OUTPUTS AVAILABLE"
echo "========================================="
echo

ls -lh "$OUTPUT_DIR"/*.md 2>/dev/null || echo "No top-level markdown files yet"
ls -lh "$OUTPUT_DIR"/pdfs/*.pdf 2>/dev/null || echo "No PDFs generated"

echo
echo "✅ TEST COMPLETE!"
echo
echo "View results:"
echo "  - Interim report: AR7_COMPLETE_TEST_INTERIM_REPORT.md"
echo "  - Final report: $OUTPUT_DIR/AR7_FINAL_COMPARISON_REPORT.md"
echo "  - Master index: $OUTPUT_DIR/INDEX.md"
echo "  - Individual chapters: $OUTPUT_DIR/<model>/*.txt"
echo "  - Markdown books: $OUTPUT_DIR/<model>/AR7_COMPLETE_BOOK_*.md"
echo "  - PDFs: $OUTPUT_DIR/pdfs/"
echo
echo "========================================="
