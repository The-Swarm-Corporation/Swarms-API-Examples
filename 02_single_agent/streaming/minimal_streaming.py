"""
Minimal Streaming
=================

The smallest possible streaming client — useful for confirming that tokens
really are arriving incrementally rather than in one buffered chunk.

Very simple streaming test to verify real-time character display

Run:
    python minimal_streaming.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
headers = {
    "x-api-key": os.getenv("SWARMS_API_KEY"),
    "Content-Type": "application/json",
}


def test_real_time_chars():
    """Test that characters appear in real-time"""
    print("🧪 Testing Real-Time Character Display...")

    payload = {
        "agent_config": {
            "agent_name": "Quick Writer",
            "description": "A quick writer",
            "system_prompt": "You are a helpful assistant. Write clearly.",
            "model_name": "gpt-4.1",
            "max_loops": 1,
            "temperature": 0.7,
        },
        "task": "Write a short story about a robot learning to paint. Make it about 5 sentences.",
        "stream": True,
    }

    print("🚀 Starting streaming...")
    print("📡 You should see characters appear one by one:")
    print("=" * 50)

    start_time = time.time()
    char_count = 0

    try:
        response = requests.post(
            f"{BASE_URL}/v1/agent/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=30,
        )

        if response.status_code == 200:
            for line in response.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    try:
                        data = json.loads(line[6:])
                        if "content" in data:
                            chunk = data["content"]
                            if chunk:
                                char_count += len(chunk)
                                print(f"{chunk}", end="", flush=True)

                                # Show progress every 10 characters
                                if char_count % 10 == 0:
                                    elapsed = time.time() - start_time
                                    print(f" [{elapsed:.1f}s]", end="", flush=True)

                    except json.JSONDecodeError:
                        continue

            print(f"\n\n✅ Test completed! Total characters: {char_count}")
            return True

        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Real-Time Character Test")
    print("This test verifies characters appear in real-time\n")

    success = test_real_time_chars()

    if success:
        print("\n✅ Real-time streaming is working!")
    else:
        print("\n❌ Real-time streaming needs debugging")
