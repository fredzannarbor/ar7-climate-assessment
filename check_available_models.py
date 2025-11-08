#!/usr/bin/env python3
"""
check_available_models.py

Check available models from litellm for Falcon, Mistral, and DeepSeek.
Queries litellm's model list to find the latest available models.

Usage:
    uv run python check_available_models.py
"""

import json
from typing import Dict, List
import litellm

def get_models_by_provider(provider_filter: str) -> List[Dict]:
    """Get all models matching a provider filter"""
    try:
        # Get all available models from litellm
        all_models = litellm.model_list

        matching_models = []
        for model in all_models:
            model_str = str(model).lower()
            if provider_filter.lower() in model_str:
                matching_models.append({
                    "model": str(model),
                    "provider": provider_filter
                })

        return matching_models
    except Exception as e:
        print(f"Error getting models for {provider_filter}: {e}")
        return []


def check_model_availability(model_name: str) -> Dict:
    """Check if a specific model is available and get its info"""
    try:
        # Try to get model info
        info = litellm.get_supported_openai_params(model_name)
        return {
            "model": model_name,
            "available": True,
            "supported_params": info if info else "Unknown"
        }
    except Exception as e:
        return {
            "model": model_name,
            "available": False,
            "error": str(e)
        }


def main():
    print("="*80)
    print("LITELLM MODEL AVAILABILITY CHECK")
    print("="*80)
    print()

    # Models to check
    providers = {
        "DeepSeek": [
            "deepseek/deepseek-chat",
            "deepseek/deepseek-reasoner",
            "deepseek/deepseek-coder",
            "huggingface/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
            "huggingface/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
        ],
        "Mistral": [
            "mistral/mistral-small-latest",
            "mistral/mistral-medium-latest",
            "mistral/mistral-large-latest",
            "mistral/open-mistral-7b",
            "mistral/open-mixtral-8x7b",
            "huggingface/mistralai/Mistral-7B-Instruct-v0.3",
        ],
        "Falcon": [
            "together_ai/togethercomputer/falcon-7b-instruct",
            "together_ai/togethercomputer/falcon-40b-instruct",
            "together_ai/togethercomputer/falcon-180B",
            "huggingface/tiiuae/falcon-7b-instruct",
            "huggingface/tiiuae/falcon-40b-instruct",
        ]
    }

    # Check each provider
    for provider, models in providers.items():
        print(f"\n{'='*80}")
        print(f"{provider} MODELS")
        print(f"{'='*80}\n")

        for model in models:
            result = check_model_availability(model)

            if result["available"]:
                print(f"✅ {model}")
                if result["supported_params"] != "Unknown":
                    print(f"   Supported params: {result['supported_params']}")
            else:
                print(f"❌ {model}")
                print(f"   Error: {result['error']}")
            print()

    # Print recommendations
    print(f"\n{'='*80}")
    print("RECOMMENDATIONS FOR AR7 PROJECT")
    print(f"{'='*80}\n")

    print("Flash/Lite Tier:")
    print("  DeepSeek:  deepseek/deepseek-chat")
    print("  Mistral:   mistral/mistral-small-latest")
    print("  Falcon:    together_ai/togethercomputer/falcon-7b-instruct")
    print()

    print("Premium Tier:")
    print("  DeepSeek:  deepseek/deepseek-reasoner")
    print("  Mistral:   mistral/mistral-large-latest")
    print("  Falcon:    together_ai/togethercomputer/falcon-180B")
    print()

    print("API Keys Required:")
    print("  DEEPSEEK_API_KEY     - For deepseek/* models")
    print("  MISTRAL_API_KEY      - For mistral/* models")
    print("  TOGETHER_API_KEY     - For together_ai/* models (Falcon)")
    print("  HUGGINGFACE_API_KEY  - For huggingface/* models (fallback)")
    print()

    # Try to check what's actually available through litellm
    print(f"\n{'='*80}")
    print("QUERYING LITELLM MODEL LIST")
    print(f"{'='*80}\n")

    try:
        # Check if litellm has a model list
        if hasattr(litellm, 'model_list'):
            print(f"Total models in litellm.model_list: {len(litellm.model_list)}")

            # Search for our providers
            deepseek_models = [m for m in litellm.model_list if 'deepseek' in str(m).lower()]
            mistral_models = [m for m in litellm.model_list if 'mistral' in str(m).lower()]
            falcon_models = [m for m in litellm.model_list if 'falcon' in str(m).lower()]

            if deepseek_models:
                print(f"\nDeepSeek models found: {len(deepseek_models)}")
                for m in deepseek_models[:5]:
                    print(f"  - {m}")
                if len(deepseek_models) > 5:
                    print(f"  ... and {len(deepseek_models) - 5} more")

            if mistral_models:
                print(f"\nMistral models found: {len(mistral_models)}")
                for m in mistral_models[:5]:
                    print(f"  - {m}")
                if len(mistral_models) > 5:
                    print(f"  ... and {len(mistral_models) - 5} more")

            if falcon_models:
                print(f"\nFalcon models found: {len(falcon_models)}")
                for m in falcon_models[:5]:
                    print(f"  - {m}")
                if len(falcon_models) > 5:
                    print(f"  ... and {len(falcon_models) - 5} more")
        else:
            print("litellm.model_list not available")

    except Exception as e:
        print(f"Error querying litellm model list: {e}")

    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    main()
