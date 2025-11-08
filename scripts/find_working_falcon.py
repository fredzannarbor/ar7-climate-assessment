#!/usr/bin/env python3
"""
find_working_falcon.py

Test various Falcon model IDs to find working ones across different providers.
"""

from load_env import load_parent_env
load_parent_env()

import litellm
litellm.drop_params = True

FALCON_CANDIDATES = [
    # DeepInfra attempts
    ("deepinfra/tiiuae/falcon-7b-instruct", "DeepInfra - Old Falcon 7B Instruct"),
    ("deepinfra/tiiuae/Falcon3-7B-Instruct", "DeepInfra - Falcon 3 7B"),
    ("deepinfra/tiiuae/Falcon3-3B-Instruct", "DeepInfra - Falcon 3 3B"),

    # Together AI attempts
    ("together_ai/tiiuae/falcon-40b-instruct", "Together AI - Falcon 40B"),
    ("together_ai/tiiuae/Falcon3-10B-Instruct", "Together AI - Falcon 3 10B"),
    ("together_ai/Falcon-40B-Instruct", "Together AI - Falcon 40B alt"),

    # HuggingFace attempts (if inference API enabled)
    ("huggingface/tiiuae/falcon-7b-instruct", "HuggingFace - Falcon 7B"),
    ("huggingface/tiiuae/Falcon3-7B-Instruct", "HuggingFace - Falcon 3 7B"),
]

TEST_PROMPT = "Say hello"


def test_model(model_id: str, description: str) -> dict:
    """Test if a Falcon model works"""

    print(f"\nTesting: {description}")
    print(f"  Model ID: {model_id}")

    try:
        response = litellm.completion(
            model=model_id,
            messages=[{"role": "user", "content": TEST_PROMPT}],
            max_tokens=20,
            timeout=15
        )

        content = response.choices[0].message.content if response.choices[0].message.content else ""
        print(f"  ✅ SUCCESS! Response: {content[:50]}")

        return {
            "model_id": model_id,
            "description": description,
            "status": "working",
            "error": None
        }

    except Exception as e:
        error = str(e)[:150]
        print(f"  ❌ Failed: {error}")

        return {
            "model_id": model_id,
            "description": description,
            "status": "failed",
            "error": error
        }


def main():
    print("="*70)
    print("FINDING WORKING FALCON MODELS")
    print("="*70)

    results = []

    for model_id, description in FALCON_CANDIDATES:
        result = test_model(model_id, description)
        results.append(result)

    # Summary
    working = [r for r in results if r["status"] == "working"]
    failed = [r for r in results if r["status"] == "failed"]

    print(f"\n{'='*70}")
    print(f"RESULTS SUMMARY")
    print(f"{'='*70}\n")

    print(f"✅ Working: {len(working)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}\n")

    if working:
        print("WORKING FALCON MODELS:")
        for r in working:
            print(f"  ✅ {r['description']}")
            print(f"     Model ID: {r['model_id']}")
        print()
    else:
        print("⚠️  NO WORKING FALCON MODELS FOUND")
        print("\nRecommendation: Replace Falcon with alternative model:")
        print("  - Qwen (Chinese perspective)")
        print("  - Llama (Meta - multilingual)")
        print("  - Additional Mistral variant")
        print()

    if failed:
        print("Failed models:")
        for r in failed:
            print(f"  ❌ {r['description']}: {r['error'][:80]}")

    # Save results
    import json
    from pathlib import Path

    Path("output").mkdir(exist_ok=True)

    with open("output/falcon_search_results.json", 'w') as f:
        json.dump({
            "tested_candidates": len(results),
            "working": len(working),
            "failed": len(failed),
            "results": results,
            "recommendation": working[0]["model_id"] if working else "No Falcon model available - use alternative"
        }, f, indent=2)

    print(f"\n{'='*70}")
    print(f"Results saved to: output/falcon_search_results.json")
    print(f"{'='*70}\n")

    return 0 if working else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
