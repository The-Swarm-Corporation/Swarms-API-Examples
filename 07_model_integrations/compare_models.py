import os
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

MODELS = [
    "openai/gpt-5",
    "anthropic/claude-opus-5",
    "anthropic/claude-sonnet-5",
    "gemini/gemini-2.5-pro",
    "deepseek/deepseek-reasoner",
    "groq/llama-3.3-70b-versatile",
    "openrouter/qwen/qwen-2.5-72b-instruct",
]

SYSTEM_PROMPT = (
    "You are a careful analyst. Answer directly, support each claim with a reason, "
    "and keep the response under 250 words."
)

TASK = (
    "A team wants to cache LLM responses to cut cost. What are the three failure "
    "modes they are most likely to hit, and what would you do about each?"
)


def run(model_name: str) -> dict:
    """Send the identical agent and task to one model; never raise, so one bad model
    name does not sink the whole comparison."""
    payload = {
        "agent_config": {
            "agent_name": "Analyst",
            "system_prompt": SYSTEM_PROMPT,
            "model_name": model_name,
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.3,
        },
        "task": TASK,
    }

    start = time.time()
    try:
        response = requests.post(
            f"{BASE_URL}/v1/agent/completions",
            headers=headers,
            json=payload,
            timeout=1000,
        )
        elapsed = time.time() - start
        if response.status_code != 200:
            return {
                "model": model_name,
                "error": f"HTTP {response.status_code}: {response.text[:200]}",
            }
        return {"model": model_name, "elapsed": elapsed, "body": response.json()}
    except Exception as exc:
        return {"model": model_name, "error": str(exc)}


def extract_text(body) -> str:
    """Pull the assistant text out of the response without assuming one exact shape."""
    if isinstance(body, str):
        return body
    if isinstance(body, list):
        return extract_text(body[-1]) if body else ""
    if isinstance(body, dict):
        for key in ("outputs", "output", "content", "result", "response"):
            if key in body:
                return extract_text(body[key])
    return str(body)


if __name__ == "__main__":
    print(f"Task: {TASK}\n")
    print(f"Running {len(MODELS)} models concurrently...\n")

    with ThreadPoolExecutor(max_workers=len(MODELS)) as pool:
        results = list(pool.map(run, MODELS))

    for result in results:
        print("=" * 78)
        if "error" in result:
            print(f"{result['model']}  —  FAILED")
            print(f"  {result['error']}")
            continue

        usage = (
            result["body"].get("usage", {}) if isinstance(result["body"], dict) else {}
        )
        print(f"{result['model']}  —  {result['elapsed']:.1f}s", end="")
        if usage:
            print(
                f"  |  in {usage.get('input_tokens', 0)} / out {usage.get('output_tokens', 0)}"
                f"  |  ${usage.get('token_cost', 0):.4f}"
            )
        else:
            print()
        print()
        print(extract_text(result["body"])[:1200])
        print()

    ok = [r for r in results if "error" not in r]
    if ok:
        fastest = min(ok, key=lambda r: r["elapsed"])
        print("=" * 78)
        print(f"Fastest: {fastest['model']} at {fastest['elapsed']:.1f}s")
    if len(ok) < len(results):
        print(
            f"{len(results) - len(ok)} model(s) failed — check the names with list_supported_models.py"
        )
