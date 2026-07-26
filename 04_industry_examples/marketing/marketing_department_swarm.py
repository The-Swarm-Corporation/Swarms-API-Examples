"""
Marketing Department Swarm
==========================

Models a marketing department as a hierarchical swarm: a director delegating to
strategy, copy and channel specialists.

Run:
    python marketing_department_swarm.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
API_KEY = os.getenv("SWARMS_API_KEY")

TASK = (
    "Plan the launch campaign for 'FlowDeck', an AI-powered project management "
    "platform for software teams, launching next quarter with a $50k budget. "
    "Deliver: target audience definition, positioning and messaging, a content "
    "plan, a 4-week social calendar outline, SEO priorities, and the KPIs we "
    "will track with budget split across channels."
)

swarm = {
    "name": "Autonomous Marketing Department",
    "description": (
        "A hierarchical marketing team: a director plans and delegates, "
        "specialists execute their functions, and the director synthesizes "
        "everything into one coherent launch plan."
    ),
    "swarm_type": "HierarchicalSwarm",
    "task": TASK,
    "agents": [
        {
            "agent_name": "Marketing Director",
            "description": "Head of marketing; plans, delegates, and synthesizes",
            "system_prompt": (
                "You are the Marketing Director. Break the campaign brief into "
                "clear workstreams for your specialists, review their output, "
                "resolve conflicts between channel plans, and assemble the final "
                "launch plan with timeline and budget allocation. Be decisive "
                "and concrete."
            ),
            "model_name": "openrouter/tencent/hy3:free",
            "role": "coordinator",
            "max_loops": 1,
            "max_tokens": 4000,
        },
        {
            "agent_name": "Market Research Analyst",
            "description": "Audience, competitor, and positioning research",
            "system_prompt": (
                "You are a market research analyst. Define the ideal customer "
                "profiles and segments, map the competitive landscape, and "
                "recommend a differentiated positioning. Support every claim "
                "with reasoning."
            ),
            "model_name": "openrouter/tencent/hy3:free",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 3000,
        },
        {
            "agent_name": "Content Strategist",
            "description": "Messaging, copy, and content plan",
            "system_prompt": (
                "You are a content strategist and senior copywriter. Turn the "
                "positioning into a messaging hierarchy, headline options, and "
                "a content plan (blog, case studies, landing pages) mapped to "
                "the funnel."
            ),
            "model_name": "openrouter/tencent/hy3:free",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 3000,
        },
        {
            "agent_name": "Social Media Manager",
            "description": "Channel strategy and posting calendar",
            "system_prompt": (
                "You are a social media manager. Choose the right channels for "
                "a developer-focused B2B SaaS launch, and outline a 4-week "
                "posting calendar with formats, hooks, and cadence per channel."
            ),
            "model_name": "openrouter/tencent/hy3:free",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 3000,
        },
        {
            "agent_name": "SEO Specialist",
            "description": "Keyword strategy and on-page priorities",
            "system_prompt": (
                "You are an SEO specialist. Identify the highest-intent keyword "
                "clusters for the product category, recommend page structure "
                "and internal linking, and list quick technical wins for a new "
                "product site."
            ),
            "model_name": "openrouter/tencent/hy3:free",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 3000,
        },
        {
            "agent_name": "Performance Analyst",
            "description": "KPIs, measurement plan, and budget allocation",
            "system_prompt": (
                "You are a performance marketing analyst. Define the KPI tree "
                "(north star, channel KPIs, guardrails), a measurement plan, "
                "and a defensible split of the $50k budget across channels "
                "with expected CAC ranges."
            ),
            "model_name": "openrouter/tencent/hy3:free",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 3000,
        },
    ],
    "max_loops": 1,
    "director_model_name": "gpt-5.5",
}


try:
    response = httpx.post(
        f"{BASE_URL}/v1/swarm/completions",
        headers={"x-api-key": API_KEY, "Content-Type": "application/json"},
        json=swarm,
        timeout=600,
    )
    response.raise_for_status()
    print(json.dumps(response.json(), indent=4))
except httpx.HTTPStatusError as e:
    print(
        f"Request failed with status code {e.response.status_code}: {e.response.text}"
    )
except Exception as e:
    print(f"An error occurred: {str(e)}")
