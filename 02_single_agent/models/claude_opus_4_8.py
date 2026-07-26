"""
Claude Opus 4.8 Agent (SDK)
===========================

Same agent shape as the Opus 5 example, pinned to `anthropic/claude-opus-4-8`.
Useful for comparing model behaviour on an identical prompt.

Run:
    python claude_opus_4_8.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os

from dotenv import load_dotenv
from swarms_client import SwarmsClient

load_dotenv()

client = SwarmsClient(
    api_key=os.getenv("SWARMS_API_KEY"),
    base_url="https://api.swarms.world",
    timeout=1000,
)


result = client.agent.run(
    agent_config={
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
    },
    task="Hemoglobin 10.2 g/dL, MCV 72 fL, ferritin 8 ng/mL — what's your diagnosis and next step?",
)

print(json.dumps(result, indent=4))
