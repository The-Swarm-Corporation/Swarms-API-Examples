"""
Catering Quote Agent
====================

A single agent that turns an event brief into a structured catering plan and
quote.

Run:
    python catering_quote_agent.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv
from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

load_dotenv()

console = Console()

SYSTEM_PROMPT = """
You are Caterly — a professional event catering discovery assistant. Your task is to find, evaluate, and recommend caterers that best match a user's event requirements. Always prioritize accuracy, transparency, and user-safety.

Behavior rules:
1. Ask only necessary clarifying questions (if absolutely needed) — otherwise assume missing common defaults (guest_count=50, budget_per_person=$30, date=flexible).
2. When search_enabled is true, perform web lookups and verify vendor contact and availability information; include citation for each vendor where possible.
3. For each recommended caterer, provide: name, short description, service types, price per person or range, contact info, menu highlights, dietary accommodations, travel/fee considerations, and a confidence rating with explanation.
4. Quote prices clearly and compute total estimated event cost = guest_count * price_per_person + service/travel fees.
5. Provide a "next steps" checklist and a ready-to-send caterer outreach message.
6. If asked to make bookings, provide only a booking proposal — never execute payments or contact vendors unless a tool is explicitly connected.
7. Never invent contact data — mark unverifiable items explicitly as "unverified".
8. If a vendor is unavailable, offer alternatives or timeline adjustments.
9. Output structured JSON followed by a short human summary.
"""


def create_agent_payload(task: str, search_enabled: bool = True) -> Dict[str, Any]:
    """Create the agent completion payload."""
    return {
        "agent_config": {
            "agent_name": "Caterly - Event Catering Discovery Assistant",
            "description": "Professional event catering discovery assistant that finds, evaluates, and recommends caterers matching your event requirements. Provides detailed vendor information including pricing, dietary accommodations, contact details, menu highlights, and ready-to-send outreach messages. Performs web searches to verify vendor availability and contact information when enabled.",
            "system_prompt": SYSTEM_PROMPT,
            "model_name": "gpt-4.1",
            "max_tokens": 3000,
            "temperature": 0.5,
            "role": "worker",
            "max_loops": 1,
            "search_enabled": search_enabled,
            "tool_call_summary": True,
            "dynamic_temperature_enabled": True,
        },
        "task": task,
        "search_enabled": search_enabled,
    }


def make_api_request(
    payload: Dict[str, Any], api_key: Optional[str]
) -> requests.Response:
    """Make API request to Swarms agent completions endpoint."""
    # url = "https://api.swarms.world/v1/agent/completions"
    url = (
        os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
        + "/v1/agent/completions"
    )
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    return response


def extract_content_from_outputs(outputs: Any) -> str:
    """Extract text content from various output structures."""
    if outputs is None:
        return ""

    if isinstance(outputs, str):
        return outputs

    if isinstance(outputs, list):
        content_parts = []
        for item in outputs:
            if isinstance(item, dict):
                content = item.get("content") or item.get("text") or item.get("message")
                if content:
                    content_parts.append(str(content))
                else:
                    for key, value in item.items():
                        if isinstance(value, str) and value.strip():
                            content_parts.append(f"{key}: {value}")
            elif isinstance(item, str):
                content_parts.append(item)
        return "\n\n".join(content_parts) if content_parts else str(outputs)

    if isinstance(outputs, dict):
        content = (
            outputs.get("content")
            or outputs.get("text")
            or outputs.get("message")
            or outputs.get("output")
        )
        if content:
            return str(content)
        string_values = [
            v for v in outputs.values() if isinstance(v, str) and len(v) > 50
        ]
        if string_values:
            return max(string_values, key=len)
        return json.dumps(outputs, indent=2)

    return str(outputs)


def display_success_response(response_data: Dict[str, Any]) -> None:
    """Display successful agent response with metadata."""
    outputs = response_data.get("outputs", "")
    content = extract_content_from_outputs(outputs)
    markdown_content = Markdown(content)

    console.print("\n")
    console.print(
        Panel(
            markdown_content,
            title="[bold cyan]Agent Response[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )

    metadata = {
        "Agent Name": response_data.get("name", "N/A"),
        "Job ID": response_data.get("job_id", "N/A"),
        "Success": response_data.get("success", False),
        "Temperature": response_data.get("temperature", "N/A"),
    }

    usage = response_data.get("usage", {})
    if usage:
        metadata["Usage"] = (
            f"Input: {usage.get('input_tokens', 'N/A')} | "
            f"Output: {usage.get('output_tokens', 'N/A')} | "
            f"Total: {usage.get('total_tokens', 'N/A')}"
        )
        if usage.get("total_cost"):
            metadata["Cost"] = f"${usage.get('total_cost', 0):.4f}"

    metadata_text = "\n".join([f"[bold]{k}:[/bold] {v}" for k, v in metadata.items()])
    console.print(
        Panel(
            metadata_text,
            title="[bold green]Response Metadata[/bold green]",
            border_style="green",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )


def display_error_response(response_data: Dict[str, Any]) -> None:
    """Display error response."""
    error_content = json.dumps(response_data, indent=2)
    console.print("\n")
    console.print(
        Panel(
            error_content,
            title="[bold red]Error Response[/bold red]",
            border_style="red",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )


def main() -> None:
    """Main function to run the catering agent."""
    task = "Find 5 caterers for a 70 person event in Mission San Francisco, find a pizza caterer that can deliver to the event location, provide their name, address, phone number, email, website, and a brief description of their services."

    payload = create_agent_payload(task, search_enabled=True)
    response = make_api_request(payload, os.getenv("SWARMS_API_KEY"))
    response_data = response.json()

    if response.status_code == 200:
        display_success_response(response_data)
    else:
        display_error_response(response_data)


if __name__ == "__main__":
    main()
