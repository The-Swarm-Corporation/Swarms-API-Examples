"""
Advanced Research
=================

The full `POST /v1/advanced-research/completions` surface: research depth,
source handling and structured findings.

Simple example demonstrating how to use the Advanced Research endpoint
with httpx HTTP client library.

Run:
    python advanced_research.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def run_advanced_research_example():
    """
    Example of using the Advanced Research endpoint
    """

    # API configuration
    api_url = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
    api_key = os.getenv("SWARMS_API_KEY")

    # Advanced Research request payload
    payload = {
        "config": {
            "name": "Market Research Example",
            "description": "Research on AI market trends",
            "worker_model_name": "claude-3-7-sonnet-20250219",
            "director_model_name": "claude-3-7-sonnet-20250219",
            "max_loops": 1,
        },
        "task": "Research the current state of AI development and identify the top 3 emerging trends in 2024",
    }

    # Headers
    headers = {"Content-Type": "application/json", "x-api-key": api_key}

    try:
        async with httpx.AsyncClient(timeout=300.0) as client:  # 5 minute timeout
            # Make the request to the advanced research endpoint
            response = await client.post(
                f"{api_url}/v1/advanced-research/completions",
                json=payload,
                headers=headers,
            )

            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return {"error": response.status_code, "response": response.text}

    except httpx.TimeoutException:
        return {
            "error": "Request timed out. Advanced research can take several minutes."
        }
    except httpx.RequestError as e:
        return {"error": f"Network error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


if __name__ == "__main__":
    asyncio.run(run_advanced_research_example())
