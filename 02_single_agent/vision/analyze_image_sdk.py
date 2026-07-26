"""
Vision via the SDK
==================

The same image workflow through `swarms_client`, plus `marketplace_prompt_id`
to reuse a published system prompt instead of writing your own.

Run:
    python analyze_image_sdk.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import base64
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


def encode_image_to_base64(image_path: str) -> str:
    """Encode an image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


image_path = "img.jpg"
image_base64 = encode_image_to_base64(image_path)


agent_config = {
    "model_name": "gpt-4.1",
    "dynamic_temperature_enabled": True,
    "max_loops": 1,
    "marketplace_prompt_id": "72021048-6f31-48b6-b624-7732e6f93437",
}

out = client.agent.run(
    agent_config=agent_config, task="What city is this image of?", img=image_base64
)

print(json.dumps(out, indent=4))
