"""
Claude Opus 4.8 Agent (httpx)
=============================

The same request without the SDK, using `httpx` directly. Shows the raw JSON
body the SDK builds for you.

Run:
    python claude_opus_4_8_httpx.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os

from dotenv import load_dotenv
import httpx

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
ENDPOINT = "/v1/agent/completions"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}

payload = {
    "agent_config": {
        "agent_name": "Bloodwork Diagnosis Expert",
        "description": "An expert doctor specializing in interpreting and diagnosing blood work results.",
        "system_prompt": (
            "You are an expert medical doctor specializing in the interpretation and diagnosis of blood work. "
            "Your expertise includes analyzing laboratory results, identifying abnormal values, "
            "explaining their clinical significance, and recommending next diagnostic or treatment steps. "
            "Provide clear, evidence-based explanations and consider differential diagnoses based on blood test findings."
            "Your name is Bloodwork Diagnosis Expert"
        ),
        "model_name": "anthropic/claude-opus-4-8",
        "max_loops": 1,
        "max_tokens": 8192,
        "dynamic_temperature_enabled": False,
        "temperature": None,
    },
    "task": "what is your name?",
}

with httpx.Client(base_url=BASE_URL, timeout=1000.0) as client:
    response = client.post(
        ENDPOINT,
        headers=headers,
        json=payload,
    )
    response.raise_for_status()
    result = response.json()

print(json.dumps(result, indent=4))
