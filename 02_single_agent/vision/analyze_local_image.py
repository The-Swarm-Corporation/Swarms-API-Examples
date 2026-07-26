"""
Vision: Local Image File
========================

Reads an image from disk and sends it to a vision-capable agent.

Run:
    python analyze_local_image.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os
import requests
from dotenv import load_dotenv
import json
import base64

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def encode_image_to_base64(image_path: str) -> str:
    """Encode an image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


img = encode_image_to_base64("img.jpg")


def run_single_agent():
    """Run a single agent with the new AgentCompletion format"""
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
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 8192,
            "temperature": 1,
            "auto_generate_prompt": False,
            "dynamic_temperature_enabled": True,
        },
        "task": "what is in the image?",
        "img": img,
    }

    response = requests.post(
        f"{BASE_URL}/v1/agent/completions", headers=headers, json=payload, timeout=1000
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    try:
        agent_result = run_single_agent()
        print(json.dumps(agent_result, indent=4))
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
