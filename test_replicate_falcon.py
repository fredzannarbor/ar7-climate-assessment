from load_env import load_parent_env
load_parent_env()

import litellm
litellm.drop_params = True

print("Testing Replicate Falcon-40B...")
try:
    response = litellm.completion(
        model="replicate/joehoover/falcon-40b-instruct",
        messages=[{"role": "user", "content": "Write one sentence about climate."}],
        max_tokens=50,
        timeout=60
    )
    print("✅ SUCCESS!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Failed: {e}")
