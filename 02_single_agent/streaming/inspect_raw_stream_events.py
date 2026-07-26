"""
Inspect Raw Stream Events
=========================

Prints every raw SSE line without parsing it. Reach for this when you need to
see the exact event shape the API emits, or to debug a stream that stalls.

Debug script to test streaming - shows exactly what's happening

Run:
    python inspect_raw_stream_events.py

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


def debug_streaming():
    """Debug streaming to see what's happening"""
    print("🔍 DEBUGGING Streaming")
    print("=" * 50)

    payload = {
        "agent_config": {
            "agent_name": "Debug Writer",
            "description": "A debug writer",
            "system_prompt": "You are a helpful assistant. Write clearly.",
            "model_name": "gpt-4.1",
            "max_loops": 1,
            "temperature": 0.7,
        },
        "task": "Write exactly 2 sentences about debugging.",
        "stream": True,
    }

    print("🚀 Starting request...")
    print("📡 Monitoring response...")
    print("-" * 50)

    try:
        response = requests.post(
            f"{BASE_URL}/v1/agent/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=30,
        )

        if response.status_code == 200:
            event_count = 0
            chunk_count = 0
            start_time = time.time()

            for line in response.iter_lines(decode_unicode=True):
                if line:
                    event_count += 1
                    current_time = time.time() - start_time

                    # Show every line for debugging
                    print(f"[{current_time:.2f}s] Line {event_count}: {line[:100]}...")

                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            if "content" in data:
                                chunk = data["content"]
                                chunk_count += 1
                                print(f"  -> CHUNK {chunk_count}: '{chunk}'")

                        except json.JSONDecodeError:
                            print(f"  -> JSON ERROR: {line[6:]}")

            print("\n📊 Summary:")
            print(f"  - Total events: {event_count}")
            print(f"  - Total chunks: {chunk_count}")
            print(f"  - Total time: {time.time() - start_time:.2f}s")
            return True

        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = debug_streaming()

    if success:
        print("\n✅ Debug completed!")
    else:
        print("\n❌ Debug failed")
