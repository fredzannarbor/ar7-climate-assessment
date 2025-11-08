#!/usr/bin/env python3
"""
test_api_keys.py

Test that all API providers are properly configured and accessible.
"""

import sys
from pathlib import Path

# Load environment
from load_env import load_parent_env
load_parent_env()

try:
    import litellm
    litellm.drop_params = True  # Auto-drop unsupported params
except ImportError:
    print("ERROR: litellm not available")
    sys.exit(1)


MODELS_TO_TEST = {
    "OpenAI GPT-5 Mini": "openai/gpt-5-mini",
    "Anthropic Haiku 4.5": "anthropic/claude-haiku-4-5-20251001",
    "Google Gemini Flash": "gemini/gemini-2.5-flash",
    "xAI Grok 3": "xai/grok-3-latest",
    "DeepSeek 7B": "huggingface/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "Mistral 7B": "deepinfra/mistralai/Mistral-7B-Instruct-v0.3",
    "Qwen 2.5-7B": "deepinfra/Qwen/Qwen2.5-7B-Instruct"
}

TEST_PROMPT = "Write a single sentence about climate change."


def test_model(model_name: str, model_id: str) -> dict:
    """Test if a model is accessible and working"""

    print(f"\n{'='*60}")
    print(f"Testing: {model_name}")
    print(f"Model ID: {model_id}")
    print(f"{'='*60}")

    try:
        response = litellm.completion(
            model=model_id,
            messages=[{"role": "user", "content": TEST_PROMPT}],
            max_tokens=50,
            timeout=30
        )

        content = response.choices[0].message.content
        word_count = len(content.split())

        print(f"✅ SUCCESS")
        print(f"   Response: {content[:100]}...")
        print(f"   Words: {word_count}")

        return {
            "model_name": model_name,
            "model_id": model_id,
            "status": "success",
            "response_length": word_count,
            "error": None
        }

    except Exception as e:
        error_str = str(e)
        print(f"❌ FAILED")
        print(f"   Error: {error_str[:200]}")

        # Categorize error
        if "401" in error_str or "Authentication" in error_str or "API key" in error_str:
            error_type = "Authentication/API Key"
        elif "temperature" in error_str or "UnsupportedParams" in error_str:
            error_type = "Parameter Restriction"
        elif "timeout" in error_str.lower():
            error_type = "Timeout"
        else:
            error_type = "Unknown"

        return {
            "model_name": model_name,
            "model_id": model_id,
            "status": "failed",
            "error": error_str[:200],
            "error_type": error_type
        }


def main():
    print(f"\n{'='*60}")
    print(f"AR7 MODEL PROVIDER API KEY VERIFICATION TEST")
    print(f"{'='*60}")
    print(f"Testing {len(MODELS_TO_TEST)} models...\n")

    results = []

    for model_name, model_id in MODELS_TO_TEST.items():
        result = test_model(model_name, model_id)
        results.append(result)

    # Summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}\n")

    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "failed"]

    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    print()

    if successful:
        print("Working Models:")
        for r in successful:
            print(f"  ✅ {r['model_name']}")
        print()

    if failed:
        print("Failed Models:")
        for r in failed:
            print(f"  ❌ {r['model_name']}: {r['error_type']}")
        print()

        # Group by error type
        by_error = {}
        for r in failed:
            error_type = r['error_type']
            if error_type not in by_error:
                by_error[error_type] = []
            by_error[error_type].append(r['model_name'])

        print("Error Types:")
        for error_type, models in by_error.items():
            print(f"  {error_type}:")
            for model in models:
                print(f"    - {model}")
        print()

    # Recommendations
    print("="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    print()

    if len(successful) >= 2:
        print(f"✅ {len(successful)} models working - sufficient for production")
        print(f"   Recommended: {successful[0]['model_name']}")
    else:
        print(f"⚠️  Only {len(successful)} model(s) working")

    for r in failed:
        if r['error_type'] == "Authentication/API Key":
            print(f"⚠️  {r['model_name']}: Check API key configuration")
        elif r['error_type'] == "Parameter Restriction":
            print(f"⚠️  {r['model_name']}: Use litellm.drop_params = True")

    print()
    print("="*60)

    # Save results
    import json
    from datetime import datetime

    Path("output").mkdir(exist_ok=True)

    with open("output/api_key_test_results.json", 'w') as f:
        json.dump({
            "tested_at": datetime.now().isoformat(),
            "total_models": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "results": results
        }, f, indent=2)

    print(f"Results saved to: output/api_key_test_results.json")
    print("="*60)
    print()

    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
