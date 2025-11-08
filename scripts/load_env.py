#!/usr/bin/env python3
"""
load_env.py

Properly load environment variables from parent xcu_my_apps/.env
"""

import os
from pathlib import Path

def load_parent_env():
    """Load environment from /Users/fred/xcu_my_apps/.env"""

    parent_env = Path("/Users/fred/xcu_my_apps/.env")

    if not parent_env.exists():
        print(f"WARNING: Parent .env not found at {parent_env}")
        return

    print(f"Loading environment from: {parent_env}")

    with open(parent_env) as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                # Always set (last occurrence wins - allows overrides in .env)
                os.environ[key] = value

    # Verify critical keys
    required_keys = [
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY',
        'GEMINI_API_KEY',
        'XAI_API_KEY',
        'TOGETHER_AI_API_KEY',
        'DEEPINFRA_API_KEY',
        'HUGGINGFACE_API_KEY'
    ]

    loaded = []
    missing = []

    for key in required_keys:
        if os.environ.get(key):
            loaded.append(key)
        else:
            missing.append(key)

    print(f"✅ Loaded {len(loaded)}/{len(required_keys)} API keys")

    if missing:
        print(f"⚠️  Missing: {', '.join(missing)}")

    return len(loaded), len(missing)


if __name__ == "__main__":
    load_parent_env()
