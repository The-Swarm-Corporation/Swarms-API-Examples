"""
Stream a Swarm Response
=======================

Streams a multi-agent swarm, printing each agent's output as it is produced
rather than waiting for the whole swarm to finish.

Run:
    python stream_swarm_response.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os

import requests
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
}


def check_available_swarm_types():
    """Check available swarm types"""
    try:
        response = requests.get(f"{BASE_URL}/v1/swarms/available", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error getting swarm types: {response.status_code}")
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return {"error": str(e)}
    except ValueError as e:
        print(f"❌ JSON decode error: {e}")
        return {
            "error": f"Invalid JSON response: {response.text if 'response' in locals() else 'No response'}"
        }


def run_swarm_streaming():
    """Run a swarm with streaming enabled"""
    payload = {
        "name": "Medical Research Swarm",
        "description": "A collaborative swarm of medical experts analyzing diabetes detection methods",
        "swarm_type": "SequentialWorkflow",
        "max_loops": 1,
        "stream": True,  # Enable streaming
        "service_tier": "standard",
        "task": "What are the most effective and accurate methods for detecting diabetes from blood samples? Include both traditional tests and emerging technologies.",
        "agents": [
            {
                "agent_name": "Clinical Diagnostician",
                "description": "Expert in clinical diagnostic procedures and laboratory testing",
                "system_prompt": (
                    "You are a Clinical Diagnostician with extensive experience in laboratory medicine and diabetes diagnosis. "
                    "Your expertise includes interpreting blood glucose tests, HbA1c levels, and other biomarkers. "
                    "Focus on established clinical protocols and evidence-based diagnostic criteria. "
                    "Provide accurate, clinical-grade information suitable for healthcare professionals."
                ),
                "model_name": "claude-sonnet-4-20250514",
                "role": "worker",
                "max_loops": 1,
                "max_tokens": 4096,
                "temperature": 0.2,
                "auto_generate_prompt": False,
                "dynamic_temperature_enabled": False,
            },
            {
                "agent_name": "Biomedical Researcher",
                "description": "Specialist in emerging biomarker research and advanced diagnostic technologies",
                "system_prompt": (
                    "You are a Biomedical Researcher specializing in diabetes biomarker discovery and innovative diagnostic technologies. "
                    "Your focus is on cutting-edge research, emerging biomarkers, novel detection methods, and future diagnostic possibilities. "
                    "Analyze the latest scientific literature and provide insights into promising research directions. "
                    "Complement clinical approaches with research-based innovations."
                ),
                "model_name": "claude-sonnet-4-20250514",
                "role": "worker",
                "max_loops": 1,
                "max_tokens": 4096,
                "temperature": 0.3,
                "auto_generate_prompt": False,
                "dynamic_temperature_enabled": False,
            },
            {
                "agent_name": "Medical Technology Analyst",
                "description": "Expert in medical devices, point-of-care testing, and diagnostic technology evaluation",
                "system_prompt": (
                    "You are a Medical Technology Analyst with expertise in diagnostic devices, point-of-care testing, and healthcare technology evaluation. "
                    "Focus on practical implementation, cost-effectiveness, accuracy metrics, and real-world deployment of diabetes testing technologies. "
                    "Evaluate both current market solutions and emerging technologies from a practical healthcare delivery perspective. "
                    "Consider factors like accessibility, user-friendliness, and healthcare system integration."
                ),
                "model_name": "claude-sonnet-4-20250514",
                "role": "worker",
                "max_loops": 1,
                "max_tokens": 4096,
                "temperature": 0.4,
                "auto_generate_prompt": False,
                "dynamic_temperature_enabled": False,
            },
        ],
    }

    print("🚀 Starting streaming swarm request...")
    print(f"🎯 Task: {payload['task']}")
    print(f"🏗️ Swarm Type: {payload['swarm_type']}")
    print(f"👥 Number of Agents: {len(payload['agents'])}")

    response = requests.post(
        f"{BASE_URL}/v1/swarm/completions",
        headers=headers,
        json=payload,
        stream=True,
        timeout=120,  # Longer timeout for swarm operations
    )

    if response.status_code != 200:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return

    print("📡 Streaming swarm response:")
    print("=" * 80)

    full_output = {}
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

                    if current_event == "metadata":
                        print(f"📋 Job ID: {data.get('job_id')}")
                        print(f"🏷️  Swarm Name: {data.get('swarm_name')}")
                        print(f"📝 Description: {data.get('description')}")
                        print(f"🔧 Swarm Type: {data.get('swarm_type')}")
                        print(f"👥 Number of Agents: {data.get('number_of_agents')}")
                        print(f"🎚️  Service Tier: {data.get('service_tier')}")
                        print(f"📊 Status: {data.get('status')}")
                        print("-" * 80)

                    elif current_event == "start":
                        print("🚀 Swarm processing started...")
                        print("🔄 Agents are collaborating...")

                    elif current_event == "status":
                        print(f"📊 Status Update: {data.get('message')}")
                        if data.get("input_tokens"):
                            print(f"🔤 Input Tokens: {data.get('input_tokens')}")

                    elif current_event == "chunk":
                        output = data.get("output", {})
                        if output:
                            print("\n🎯 Swarm Output:")
                            print("-" * 60)

                            # Handle different output formats
                            if isinstance(output, dict):
                                for agent_role, content in output.items():
                                    if agent_role != "User":  # Skip User entries
                                        print(f"\n🤖 {agent_role}:")
                                        print("─" * 40)
                                        if isinstance(content, list):
                                            for item in content:
                                                if isinstance(item, dict):
                                                    role = item.get("role", "Assistant")
                                                    text = item.get(
                                                        "content", str(item)
                                                    )
                                                    print(f"[{role}]: {text}")
                                                else:
                                                    print(str(item))
                                        else:
                                            print(str(content))
                                        print()

                            elif isinstance(output, list):
                                for item in output:
                                    if (
                                        isinstance(item, dict)
                                        and item.get("role") != "User"
                                    ):
                                        role = item.get("role", "Agent")
                                        content = item.get("content", str(item))
                                        print(f"\n🤖 {role}:")
                                        print("─" * 40)
                                        print(content)
                                        print()

                            full_output = output

                    elif current_event == "usage":
                        print("\n📊 Usage Statistics:")
                        print("─" * 40)
                        print(f"📥 Input Tokens: {data.get('input_tokens', 'N/A')}")
                        print(f"📤 Output Tokens: {data.get('output_tokens', 'N/A')}")
                        print(f"🔢 Total Tokens: {data.get('total_tokens', 'N/A')}")

                        billing_info = data.get("billing_info", {})
                        if billing_info:
                            cost_breakdown = billing_info.get("cost_breakdown", {})
                            print(
                                f"💰 Total Cost: ${billing_info.get('total_cost', 'N/A')}"
                            )
                            if cost_breakdown:
                                print(
                                    f"   Agent Cost: ${cost_breakdown.get('agent_cost', 'N/A')}"
                                )
                                print(
                                    f"   Input Token Cost: ${cost_breakdown.get('input_token_cost', 'N/A')}"
                                )
                                print(
                                    f"   Output Token Cost: ${cost_breakdown.get('output_token_cost', 'N/A')}"
                                )
                                print(
                                    f"   Service Tier: {cost_breakdown.get('service_tier', 'N/A')}"
                                )

                    elif current_event == "end":
                        print("\n✅ Swarm execution completed!")
                        execution_time = data.get("execution_time")
                        if execution_time:
                            print(f"⏱️  Execution Time: {execution_time:.2f} seconds")

                    elif current_event == "done":
                        print("🎉 Swarm processing complete!")

                    elif current_event == "error":
                        print(f"\n❌ Error: {data.get('error')}")

                except json.JSONDecodeError:
                    continue

    print("\n\n📝 Swarm execution summary completed")
    return full_output


if __name__ == "__main__":
    print("🛠️ Available swarm types:")
    available_swarms = check_available_swarm_types()
    if "error" in available_swarms:
        print(f"❌ Could not fetch swarm types: {available_swarms['error']}")
        print("⚠️  Continuing with examples anyway...")
    else:
        print(json.dumps(available_swarms, indent=2))
    print("\n" + "=" * 80)

    # Demonstrate single task swarm streaming
    print("\n🎬 DEMONSTRATION 1: Single Task Swarm Streaming")
    print("=" * 80)
    single_result = run_swarm_streaming()
