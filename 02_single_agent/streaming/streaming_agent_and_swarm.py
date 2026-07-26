"""
Streaming: Agent and Swarm
==========================

End-to-end streaming reference covering both the single-agent endpoint and
the swarm endpoint, with event parsing and error handling.

Run:
    python streaming_agent_and_swarm.py

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


def test_real_time_streaming():
    """Test real-time streaming with a long-form creative task"""
    print("🌊 Testing REAL-TIME Agent Streaming...")

    payload = {
        "agent_config": {
            "agent_name": "Creative Writer",
            "description": "A creative storyteller",
            "system_prompt": "You are a creative writer who tells detailed, engaging stories. Write slowly and descriptively, with rich details about characters, settings, and emotions.",
            "model_name": "gpt-4.1",
            "max_loops": 1,
            "max_tokens": 1000,
            "temperature": 0.8,
            "streaming_on": True,  # Force streaming at agent level
        },
        "task": "Write a detailed story about a young astronaut's first journey to Mars. Include vivid descriptions of the launch, the journey through space, and the first glimpse of the red planet. Make it at least 500 words long with rich emotional details.",
        "stream": True,  # Enable API streaming
    }

    print("🚀 Starting REAL-TIME streaming request...")
    print("📡 Content should appear word by word as it's generated:")
    print("=" * 80)

    start_time = time.time()

    response = requests.post(
        f"{BASE_URL}/v1/agent/completions",
        headers=headers,
        json=payload,
        stream=True,  # Critical for real-time streaming
        timeout=60,
    )

    if response.status_code == 200:
        chunk_count = 0
        total_content = ""

        for line in response.iter_lines(decode_unicode=True):
            if line:
                # Track timing for real-time verification
                current_time = time.time() - start_time

                # Handle event-based SSE format
                if line.startswith("event: start"):
                    print("🚀 Agent processing started...")
                    continue
                elif line.startswith("event: chunk"):
                    # Next line should contain the data
                    continue
                elif line.startswith("event: end"):
                    print(f"\n{'=' * 80}")
                    print(f"✅ Streaming completed in {current_time:.2f}s")
                    print(f"📊 Received {chunk_count} chunks")
                    print(f"📝 Total content: {len(total_content)} characters")
                    continue
                elif line.startswith("event: error"):
                    print("\n❌ Error event detected")
                    continue
                elif line.startswith("event: usage"):
                    continue
                elif line.startswith("event: metadata"):
                    continue
                elif line.startswith("event: done"):
                    break

                # Handle data lines
                elif line.startswith("data: "):
                    try:
                        data = json.loads(line[6:])

                        # Handle chunk content
                        if "content" in data:
                            chunk = data["content"]
                            if chunk:
                                chunk_count += 1
                                total_content += chunk

                                # Print with timestamp to verify real-time
                                print(f"{chunk}", end="", flush=True)

                                # Add timing info every 10 chunks
                                if chunk_count % 10 == 0:
                                    print(f" [{current_time:.1f}s]", end="", flush=True)

                        # Handle usage data
                        elif "total_tokens" in data:
                            print(f"\n📊 Usage: {data.get('total_tokens', 0)} tokens")

                        # Handle start/end messages
                        elif "message" in data:
                            if data["message"] == "Starting agent processing...":
                                print("🚀 Agent processing started...")
                            elif data["message"] == "Agent processing complete":
                                pass  # Already handled by event: end

                        # Handle errors
                        elif "error" in data:
                            print(f"\n❌ Error: {data['error']}")
                            break

                    except json.JSONDecodeError:
                        continue

        return total_content
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None


def test_swarm_streaming():
    """Test real-time swarm streaming"""
    print("\n🐝🌊 Testing REAL-TIME Swarm Streaming...")

    payload = {
        "name": "Story Creation Swarm",
        "description": "A team creating a collaborative story",
        "swarm_type": "SequentialWorkflow",
        "agents": [
            {
                "agent_name": "Plot Writer",
                "description": "Creates the story plot",
                "system_prompt": "You are a plot creator. Write detailed story outlines with rich descriptions. Take your time and be descriptive.",
                "model_name": "gpt-4.1",
                "max_loops": 1,
                "temperature": 0.8,
                "streaming_on": True,
            },
            {
                "agent_name": "Character Developer",
                "description": "Develops characters for the story",
                "system_prompt": "You are a character developer. Create detailed, complex characters with backstories and motivations. Be thorough and descriptive.",
                "model_name": "gpt-4.1",
                "max_loops": 1,
                "temperature": 0.7,
                "streaming_on": True,
            },
        ],
        "task": "Create an epic space adventure story with compelling characters and an exciting plot involving alien contact.",
        "max_loops": 1,
        "stream": True,
    }

    print("🚀 Starting REAL-TIME swarm streaming...")
    print("📡 Multi-agent content streaming:")
    print("=" * 80)

    start_time = time.time()

    response = requests.post(
        f"{BASE_URL}/v1/swarm/completions",
        headers=headers,
        json=payload,
        stream=True,
        timeout=120,
    )

    if response.status_code == 200:
        chunk_count = 0

        for line in response.iter_lines(decode_unicode=True):
            if line:
                current_time = time.time() - start_time

                # Handle event-based SSE format
                if line.startswith("event: start"):
                    print("🚀 Swarm processing started...")
                    continue
                elif line.startswith("event: chunk"):
                    continue
                elif line.startswith("event: end"):
                    print(f"\n{'=' * 80}")
                    print(f"✅ Swarm streaming completed in {current_time:.2f}s")
                    print(f"📊 Received {chunk_count} chunks from swarm")
                    continue
                elif line.startswith("event: error"):
                    print("\n❌ Swarm Error event detected")
                    continue
                elif line.startswith("event: usage"):
                    continue
                elif line.startswith("event: metadata"):
                    continue
                elif line.startswith("event: done"):
                    break

                # Handle data lines
                elif line.startswith("data: "):
                    try:
                        data = json.loads(line[6:])

                        # Handle chunk content
                        if "content" in data:
                            chunk = data["content"]
                            if chunk:
                                chunk_count += 1
                                print(f"{chunk}", end="", flush=True)

                                # Timing markers
                                if chunk_count % 15 == 0:
                                    print(f" [{current_time:.1f}s]", end="", flush=True)

                        # Handle errors
                        elif "error" in data:
                            print(f"\n❌ Swarm Error: {data['error']}")
                            break

                    except json.JSONDecodeError:
                        continue
    else:
        print(f"❌ Swarm Error: {response.status_code} - {response.text}")


if __name__ == "__main__":
    print("🧪 REAL-TIME Streaming Test")
    print("This test focuses ONLY on streaming functionality")
    print("You should see text appear gradually as it's generated!\n")

    try:
        # Test agent streaming
        print(test_real_time_streaming())

        # # Test swarm streaming
        # test_swarm_streaming()

        print("\n🎉 Real-time streaming tests completed!")

    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
