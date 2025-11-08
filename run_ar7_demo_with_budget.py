#!/usr/bin/env python3
"""
run_ar7_demo_with_budget.py
Runs AR7 demo generation with $5 budget limit and cost tracking

Usage:
    uv run python run_ar7_demo_with_budget.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from codexes.core.token_usage_tracker import TokenUsageTracker
from codexes.core import llm_caller

# Import cost tracking utilities
try:
    import litellm
    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False
    print("Warning: litellm not available, cost tracking may be limited")

BUDGET_LIMIT = 5.00  # $5 USD
OUTPUT_DIR = Path("output/ar7_demo_optimistic_breakthrough")
SCHEDULE_FILE = "configs/ar7_demo_schedule.json"

def get_current_spend(tracker: TokenUsageTracker) -> float:
    """Calculate current spend from token tracker"""
    stats = tracker.get_total_statistics()
    return stats.get('total_cost', 0.0)

def should_continue(tracker: TokenUsageTracker, budget_limit: float = BUDGET_LIMIT) -> tuple[bool, float]:
    """Check if we should continue generation within budget"""
    current_spend = get_current_spend(tracker)
    remaining = budget_limit - current_spend

    if current_spend >= budget_limit:
        return False, current_spend

    # Stop if less than $0.10 remaining (safety buffer)
    if remaining < 0.10:
        return False, current_spend

    return True, current_spend

def generate_chapter_list():
    """Generate list of chapters to process in order"""
    return [
        {"key": "summary_for_policymakers", "title": "Summary for Policymakers", "model": "claude"},
        {"key": "technical_summary", "title": "Technical Summary", "model": "claude"},
        {"key": "chapter_01_framing", "title": "Chapter 1: Framing and Key Concepts", "model": "gemini"},
        {"key": "chapter_02_vulnerabilities", "title": "Chapter 2: Vulnerabilities, Impacts and Risks", "model": "gemini"},
        {"key": "chapter_03_adaptation_progress", "title": "Chapter 3: Current Adaptation Progress", "model": "gemini"},
        {"key": "chapter_04_adaptation_options", "title": "Chapter 4: Adaptation Options", "model": "gemini"},
        {"key": "chapter_05_loss_damage", "title": "Chapter 5: Responses to Losses and Damages", "model": "gemini"},
        {"key": "chapter_06_finance", "title": "Chapter 6: Finance", "model": "gemini"},
    ]

def main():
    """Main execution with budget tracking"""

    print("="*80)
    print("VARIANT EARTH AR7 DEMO GENERATION")
    print("Scenario: Optimistic Breakthrough")
    print("Budget Limit: $5.00")
    print("Model Strategy: Hybrid (Claude for SPM/TS, Gemini Flash for chapters)")
    print("="*80)
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize token tracker
    token_tracker = TokenUsageTracker()
    llm_caller.set_token_tracker(token_tracker)

    # Load schedule
    print(f"Loading schedule from {SCHEDULE_FILE}...")
    with open(SCHEDULE_FILE, 'r') as f:
        schedule = json.load(f)

    book_data = schedule['publishing_schedule'][0]['books'][0]
    variation_params = book_data['variation_parameters']

    print(f"✓ Loaded: {book_data['title']}")
    print(f"  Variation: {variation_params['variation_id']}")
    print(f"  Scenario: {variation_params['scenario_narrative'][:100]}...")
    print()

    # Track generation progress
    chapters_completed = []
    chapters_failed = []
    generation_log = {
        "started": datetime.now().isoformat(),
        "budget_limit": BUDGET_LIMIT,
        "variation_id": variation_params['variation_id'],
        "chapters": []
    }

    # Get chapter list
    chapters_to_generate = generate_chapter_list()

    print(f"Planning to generate {len(chapters_to_generate)} chapters:")
    for i, ch in enumerate(chapters_to_generate, 1):
        print(f"  {i}. {ch['title']} ({ch['model']})")
    print()

    # IMPORTANT: This is a demonstration/planning script
    # Actual generation requires integration with run_book_pipeline.py
    # For now, simulate what would happen

    print("="*80)
    print("COST TRACKING SIMULATION")
    print("="*80)
    print()
    print("This script demonstrates the budget tracking approach.")
    print("To actually generate content, we need to:")
    print()
    print("1. Modify run_book_pipeline.py to accept variation_parameters")
    print("2. Inject variation parameters into prompts before LLM calls")
    print("3. Use model_assignments to route chapters to appropriate models")
    print("4. Track costs after each chapter generation")
    print("5. Stop when budget limit reached")
    print()
    print("Estimated costs with hybrid approach:")
    print("  - SPM (Claude Sonnet): ~$2.00 (15k tokens output)")
    print("  - Tech Summary (Claude Sonnet): ~$2.50 (20k tokens output)")
    print("  - Chapter 1 (Gemini Flash): ~$0.15 (8k tokens output)")
    print("  - Chapter 2 (Gemini Flash): ~$0.15 (8k tokens output)")
    print("  - Chapter 3 (Gemini Flash): ~$0.15 (8k tokens output)")
    print("  ...")
    print()
    print("With $5 budget, we can likely complete:")
    print("  ✓ Summary for Policymakers (Claude)")
    print("  ✓ Technical Summary (Claude)")
    print("  ✓ Chapter 1-3 (Gemini Flash)")
    print()
    print("This provides:")
    print("  - High-quality policy/technical summaries")
    print("  - 3 full chapters demonstrating structure")
    print("  - Enough output to validate approach")
    print("  - Accurate cost data for remaining 22 chapters")
    print()

    # Simulate cost tracking
    simulated_costs = [
        {"chapter": "SPM", "model": "claude-sonnet", "cost": 2.00, "tokens": 15000},
        {"chapter": "Tech Summary", "model": "claude-sonnet", "cost": 2.50, "tokens": 20000},
        {"chapter": "Chapter 1", "model": "gemini-flash", "cost": 0.15, "tokens": 8000},
        {"chapter": "Chapter 2", "model": "gemini-flash", "cost": 0.15, "tokens": 8000},
        {"chapter": "Chapter 3", "model": "gemini-flash", "cost": 0.15, "tokens": 8000},
    ]

    cumulative = 0.0
    print("Simulated generation with cost tracking:")
    print()
    for entry in simulated_costs:
        cumulative += entry['cost']
        if cumulative <= BUDGET_LIMIT:
            status = "✓ Generated"
            print(f"  {status}: {entry['chapter']} ({entry['model']})")
            print(f"    Cost: ${entry['cost']:.2f} | Cumulative: ${cumulative:.2f} | Remaining: ${BUDGET_LIMIT - cumulative:.2f}")
        else:
            status = "⏸ Stopped"
            print(f"  {status}: Budget limit would be exceeded")
            break
        print()

    print("="*80)
    print("NEXT STEPS TO ENABLE ACTUAL GENERATION")
    print("="*80)
    print()
    print("1. Modify llm_get_book_data.py to accept and inject variation_parameters")
    print("2. Update prompt templates to use {{variation_parameters}} placeholder")
    print("3. Add model selection logic based on model_assignments in schedule")
    print("4. Integrate cost checking between chapter generations")
    print("5. Create checkpoint/resume functionality for budget-limited runs")
    print()
    print("Estimated implementation time: 2-3 hours")
    print("Would you like me to proceed with these modifications?")
    print()

    # Save progress log
    generation_log['completed'] = datetime.now().isoformat()
    generation_log['status'] = 'simulation_only'
    generation_log['simulated_spend'] = cumulative
    generation_log['chapters_simulated'] = simulated_costs

    log_file = OUTPUT_DIR / "generation_log.json"
    with open(log_file, 'w') as f:
        json.dump(generation_log, f, indent=2)

    print(f"Simulation log saved to: {log_file}")
    print()

if __name__ == "__main__":
    main()
