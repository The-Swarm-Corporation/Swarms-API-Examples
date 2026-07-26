"""
Fan-Out / Fan-In Graph
======================

One agent fans work out to several parallel agents, then a final agent fans
the results back in. The standard map/reduce shape for graph workflows.

Run:
    python parallel_fan_out_fan_in.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os
from dotenv import load_dotenv
from requests import post
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

load_dotenv()

console = Console()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}

# Define agents for the workflow
agents = [
    {
        "agent_name": "DataCollector",
        "description": "Collects and aggregates data from multiple sources",
        "system_prompt": "You are a data collection expert. Gather comprehensive data from various sources.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "TechnicalAnalyst",
        "description": "Performs technical analysis",
        "system_prompt": "You are a technical analyst. Analyze data from a technical perspective.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "FundamentalAnalyst",
        "description": "Performs fundamental analysis",
        "system_prompt": "You are a fundamental analyst. Analyze data from a fundamental perspective.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "SentimentAnalyst",
        "description": "Performs sentiment analysis",
        "system_prompt": "You are a sentiment analyst. Analyze data from a sentiment and market psychology perspective.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "SynthesisAgent",
        "description": "Synthesizes multiple analyses into a comprehensive report",
        "system_prompt": "You are a synthesis expert. Combine multiple analyses into a comprehensive, actionable report.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
]

# Define edges with fan-out and fan-in patterns
# Fan-out: DataCollector feeds all analysts
# Fan-in: All analysts feed SynthesisAgent
edges = [
    # Fan-out pattern: DataCollector -> TechnicalAnalyst
    {"source": "DataCollector", "target": "TechnicalAnalyst"},
    # Fan-out pattern: DataCollector -> FundamentalAnalyst
    {"source": "DataCollector", "target": "FundamentalAnalyst"},
    # Fan-out pattern: DataCollector -> SentimentAnalyst
    {"source": "DataCollector", "target": "SentimentAnalyst"},
    # Fan-in pattern: TechnicalAnalyst -> SynthesisAgent
    {"source": "TechnicalAnalyst", "target": "SynthesisAgent"},
    # Fan-in pattern: FundamentalAnalyst -> SynthesisAgent
    {"source": "FundamentalAnalyst", "target": "SynthesisAgent"},
    # Fan-in pattern: SentimentAnalyst -> SynthesisAgent
    {"source": "SentimentAnalyst", "target": "SynthesisAgent"},
]

# Create the graph workflow request
workflow_input = {
    "name": "Market-Analysis-Parallel-Workflow",
    "description": "Parallel market analysis workflow with fan-out and fan-in patterns",
    "agents": agents,
    "edges": edges,
    "entry_points": ["DataCollector"],
    "end_points": ["SynthesisAgent"],
    "max_loops": 1,
    "task": "Analyze Bitcoin market trends including technical, fundamental, and sentiment perspectives",
    "auto_compile": True,
    "verbose": False,
}

console.print(
    Panel.fit(
        f"[bold]Workflow:[/bold] {workflow_input['name']}\n"
        f"[bold]Task:[/bold] {workflow_input['task']}\n"
        f"[bold]Agents:[/bold] {len(agents)} | [bold]Edges:[/bold] {len(edges)}",
        title="Sending GraphWorkflow Request",
        border_style="cyan",
    )
)

response = post(
    f"{BASE_URL}/v1/graph-workflow/completions",
    headers=headers,
    json=workflow_input,
)

if response.status_code == 200:
    result = response.json()

    console.print("\n[bold green]Workflow completed successfully![/bold green]")
    console.print(f"[dim]Job ID:[/dim] {result.get('job_id')}")
    console.print(f"[dim]Status:[/dim] {result.get('status')}\n")

    outputs = result.get("outputs", {})

    agent_order = [
        "DataCollector",
        "TechnicalAnalyst",
        "FundamentalAnalyst",
        "SentimentAnalyst",
        "SynthesisAgent",
    ]

    colors = {
        "DataCollector": "blue",
        "TechnicalAnalyst": "yellow",
        "FundamentalAnalyst": "green",
        "SentimentAnalyst": "magenta",
        "SynthesisAgent": "cyan",
    }

    for agent_name in agent_order:
        if agent_name in outputs:
            output = str(outputs[agent_name])
            color = colors.get(agent_name, "white")
            console.print(
                Panel(
                    Markdown(output),
                    title=f"[bold]{agent_name}[/bold]",
                    border_style=color,
                    padding=(1, 2),
                )
            )
            console.print()

    usage = result.get("usage", {})
    console.print(
        Panel.fit(
            f"[bold]Input tokens:[/bold] {usage.get('input_tokens', 0):,}\n"
            f"[bold]Output tokens:[/bold] {usage.get('output_tokens', 0):,}\n"
            f"[bold]Total tokens:[/bold] {usage.get('total_tokens', 0):,}\n"
            f"[bold]Token cost:[/bold] ${usage.get('token_cost', 0):.4f}\n"
            f"[bold]Cost per agent:[/bold] ${usage.get('cost_per_agent', 0):.4f}",
            title="Usage Statistics",
            border_style="green",
        )
    )
else:
    console.print(f"[bold red]Error: {response.status_code}[/bold red]")
    console.print(response.text)
