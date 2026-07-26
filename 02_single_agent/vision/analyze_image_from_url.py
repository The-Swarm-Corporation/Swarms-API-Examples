"""
Vision: Image From a URL
========================

Downloads an image, base64-encodes it into a data URL, and passes it to an
agent through the `img` field of an agent completion.

Run:
    python analyze_image_from_url.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import base64
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

# Constants
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
# Environment variables
API_KEY = os.getenv("SWARMS_API_KEY")

HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def fetch_image_as_base64(url: str) -> str:
    """Fetch an image from a URL and return it as a base64 encoded string."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return base64.b64encode(response.content).decode("utf-8")


def test_agent_completion_with_single_image_base64() -> Dict[str, Any]:
    """Test agent completion with a single base64 encoded image using the img field"""
    try:
        # Fetch a real image and convert to base64 (tiger image from Wikimedia Commons)
        image_url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/Walking_tiger_female.jpg"
        base64_image = fetch_image_as_base64(image_url)
        image_data_url = f"data:image/jpeg;base64,{base64_image}"

        payload = {
            "agent_config": {
                "agent_name": "Vision Assistant",
                "description": "An assistant that can analyze images",
                "system_prompt": "You are a helpful assistant that can analyze and describe images. When given an image, describe what you see.",
                "model_name": "gpt-4.1",
                "role": "worker",
                "max_loops": 1,
                "temperature": 0.7,
            },
            "task": "Describe what you see in this image.",
            "img": image_data_url,
        }

        response = requests.post(
            f"{BASE_URL}/v1/agent/completions", headers=HEADERS, json=payload
        )
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"

        response_data = response.json()

        # Validate response structure
        assert response_data.get("success") is True or response_data.get(
            "outputs"
        ), "Response should indicate success or contain outputs"

        return {
            "test_name": "Agent Completion Single Image Base64 Test",
            "status": "passed",
            "response": response_data,
            "error": None,
        }
    except Exception as e:
        return {
            "test_name": "Agent Completion Single Image Base64 Test",
            "status": "failed",
            "error": str(e),
        }


if __name__ == "__main__":
    result = test_agent_completion_with_single_image_base64()
    print(result)
