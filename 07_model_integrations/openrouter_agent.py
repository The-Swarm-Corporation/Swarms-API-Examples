import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

# Swap this for any name that `list_supported_models.py openrouter` prints.
MODEL_NAME = "openrouter/deepseek/deepseek-chat"

payload = {
    "agent_config": {
        "agent_name": "Open Model Evaluator",
        "description": "Answers a fixed prompt so open-weight models can be compared head to head.",
        "system_prompt": (
            "You are a careful technical explainer. Answer in plain language, lead with "
            "the direct answer, and keep the whole response under 200 words. If a "
            "question has a common misconception attached to it, name the misconception "
            "explicitly."
        ),
        "model_name": MODEL_NAME,
        "max_loops": 1,
        "max_tokens": 4096,
        "temperature": 0.4,
    },
    "task": "Why does quantizing a model to 4 bits cost less quality than you would expect?",
}

response = requests.post(
    f"{BASE_URL}/v1/agent/completions",
    headers=headers,
    json=payload,
    timeout=1000,
)

if response.status_code == 400:
    # The most common failure here is a model name OpenRouter has retired.
    print(f"Request rejected for model '{MODEL_NAME}':")
    print(response.text)
    print("\nRun `python list_supported_models.py openrouter` to see current names.")
    raise SystemExit(1)

response.raise_for_status()
print(json.dumps(response.json(), indent=4))
