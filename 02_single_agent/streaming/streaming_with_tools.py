"""
Streaming With Tools
====================

Streams an agent that also has tools available. Lists the tools the API
exposes via `GET /v1/tools/available` before running.

Run:
    python streaming_with_tools.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
# Accept encoding for lz4
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
    "Accept-Encoding": "lz4",
}


def check_available_tools():
    response = requests.get(f"{BASE_URL}/v1/tools/available", headers=headers)
    return response.json()


def run_single_agent_streaming():
    """Run a single agent with streaming enabled"""
    payload = {
        "agent_config": {
            "agent_name": "Research Analyst",
            "description": "An expert in analyzing and synthesizing research data",
            "system_prompt": (
                "You are a Research Analyst with expertise in data analysis and synthesis. "
                "Your role is to analyze provided information, identify key insights, "
                "and present findings in a clear, structured format. "
                "Focus on accuracy, clarity, and actionable recommendations."
            ),
            "model_name": "claude-sonnet-4-20250514",
            "role": "worker",
            "max_loops": 2,
            "max_tokens": 8192,
            "temperature": 1,
            "auto_generate_prompt": False,
            "tools_list_dictionary": None,
            "streaming_on": True,
            "dynamic_temperature_enabled": True,
            # "mcp_url": "http://localhost:11434/sse",
        },
        "task": "What are the best ways to find samples of diabetes from blood samples?",
        # "tools_enabled": ["exa_search"],
    }

    print("🚀 Starting streaming agent request...")

    response = requests.post(
        f"{BASE_URL}/v1/agent/completions",
        headers=headers,
        json=payload,
        stream=True,
        timeout=60,
    )

    if response.status_code != 200:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return

    print("📡 Streaming response:")
    print("-" * 60)

    full_content = ""
    current_event = None

    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8")

            # Handle event lines
            if line.startswith("event: "):
                current_event = line[7:]  # Remove 'event: ' prefix
                continue

            # Handle data lines
            elif line.startswith("data: "):
                try:
                    data = json.loads(line[6:])  # Remove 'data: ' prefix

                    if current_event == "metadata" or data.get("type") == "metadata":
                        print(f"📋 Job ID: {data.get('job_id')}")
                        print(f"🤖 Agent: {data.get('name')}")
                        print(f"🌡️  Temperature: {data.get('temperature')}")
                        print("-" * 60)

                    elif current_event == "start":
                        print("🚀 Agent processing started...")

                    elif current_event == "chunk":
                        content = data.get("content", "")
                        full_content += content
                        print(content, end="", flush=True)

                    elif current_event == "usage":
                        print(f"\n📊 Usage: {data}")

                    elif current_event == "end":
                        print("\n✅ Completion finished!")

                    elif current_event == "done":
                        print("🎉 Processing complete!")

                    elif current_event == "error":
                        print(f"\n❌ Error: {data.get('error')}")

                except json.JSONDecodeError:
                    continue

    print(f"\n\n📝 Total content length: {len(full_content)} characters")
    return full_content


if __name__ == "__main__":

    # Demonstrate both streaming and non-streaming
    # print("\n🎬 DEMONSTRATION 1: Streaming Response")
    # print("=" * 80)
    streaming_result = run_single_agent_streaming()
