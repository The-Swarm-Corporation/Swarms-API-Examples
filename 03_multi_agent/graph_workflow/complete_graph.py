"""
Complete Graph Workflow
=======================

Every GraphWorkflow feature in one file, with error handling — the reference
to copy from when building a real graph.

Complete example demonstrating all GraphWorkflow features with error handling
and comprehensive output processing.

This example shows:
- Multiple agents with different configurations
- Complex edge patterns (fan-out, fan-in, parallel chains)
- Entry and end points configuration
- Usage tracking and cost calculation
- Error handling

Run:
    python complete_graph.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os
import json
from dotenv import load_dotenv
from requests import post, HTTPError

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")

if not API_KEY:
    raise ValueError("SWARMS_API_KEY environment variable is required")

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}


def create_market_research_workflow():
    """
    Creates a comprehensive market research workflow configuration.
    """
    # Define specialized agents
    agents = [
        {
            "agent_name": "DataCollector",
            "description": "Collects market data from multiple sources",
            "system_prompt": "You are a data collection expert. Gather comprehensive market data from various sources including financial reports, news articles, and market indicators.",
            "model_name": "gpt-4.1",
            "max_tokens": 4000,
            "temperature": 0.3,
            "max_loops": 1,
        },
        {
            "agent_name": "TechnicalAnalyst",
            "description": "Performs technical analysis on market data",
            "system_prompt": "You are a technical analyst. Analyze market data using technical indicators, charts, and patterns. Focus on price movements and trading signals.",
            "model_name": "gpt-4.1",
            "max_tokens": 4000,
            "temperature": 0.3,
            "max_loops": 1,
        },
        {
            "agent_name": "FundamentalAnalyst",
            "description": "Performs fundamental analysis on market data",
            "system_prompt": "You are a fundamental analyst. Analyze market data from a fundamental perspective including company financials, industry trends, and economic factors.",
            "model_name": "gpt-4.1",
            "max_tokens": 4000,
            "temperature": 0.3,
            "max_loops": 1,
        },
        {
            "agent_name": "SentimentAnalyst",
            "description": "Performs sentiment analysis on market data",
            "system_prompt": "You are a sentiment analyst. Analyze market sentiment, investor psychology, and market mood from news, social media, and market commentary.",
            "model_name": "gpt-4.1",
            "max_tokens": 4000,
            "temperature": 0.3,
            "max_loops": 1,
        },
        {
            "agent_name": "RiskAnalyst",
            "description": "Assesses market risks",
            "system_prompt": "You are a risk analyst. Identify and assess various types of market risks including volatility, liquidity, credit, and operational risks.",
            "model_name": "gpt-4.1",
            "max_tokens": 4000,
            "temperature": 0.3,
            "max_loops": 1,
        },
        {
            "agent_name": "SynthesisAgent",
            "description": "Synthesizes all analyses into a comprehensive report",
            "system_prompt": "You are a synthesis expert. Combine technical, fundamental, sentiment, and risk analyses into a comprehensive, actionable market research report with clear recommendations.",
            "model_name": "gpt-4.1",
            "max_tokens": 4000,
            "temperature": 0.3,
            "max_loops": 1,
        },
        {
            "agent_name": "Validator",
            "description": "Validates the final report",
            "system_prompt": "You are a validation expert. Review the synthesized report for accuracy, completeness, and clarity. Ensure all key points are properly addressed.",
            "model_name": "gpt-4.1",
            "max_tokens": 4000,
            "temperature": 0.2,
            "max_loops": 1,
        },
    ]

    # Define edges with fan-out and fan-in patterns
    edges = [
        # Fan-out: DataCollector feeds all analysts
        {"source": "DataCollector", "target": "TechnicalAnalyst"},
        {"source": "DataCollector", "target": "FundamentalAnalyst"},
        {"source": "DataCollector", "target": "SentimentAnalyst"},
        {"source": "DataCollector", "target": "RiskAnalyst"},
        # Fan-in: All analysts feed SynthesisAgent
        {"source": "TechnicalAnalyst", "target": "SynthesisAgent"},
        {"source": "FundamentalAnalyst", "target": "SynthesisAgent"},
        {"source": "SentimentAnalyst", "target": "SynthesisAgent"},
        {"source": "RiskAnalyst", "target": "SynthesisAgent"},
        # Final validation step
        {"source": "SynthesisAgent", "target": "Validator"},
    ]

    return {
        "name": "Complete-Market-Research-Workflow",
        "description": "Comprehensive market research workflow with data collection, multi-perspective analysis, synthesis, and validation",
        "agents": agents,
        "edges": edges,
        "entry_points": ["DataCollector"],
        "end_points": ["Validator"],
        "max_loops": 1,
        "task": "Conduct comprehensive market research on the cryptocurrency market, including technical analysis, fundamental analysis, sentiment analysis, and risk assessment. Synthesize all findings into a detailed report with actionable recommendations.",
        "auto_compile": True,
        "verbose": True,
    }


def print_workflow_summary(workflow_input):
    """Print a summary of the workflow configuration."""
    print("=" * 80)
    print("GraphWorkflow Configuration Summary")
    print("=" * 80)
    print(f"Name: {workflow_input['name']}")
    print(f"Description: {workflow_input['description']}")
    print(f"Task: {workflow_input['task']}")
    print(f"\nAgents ({len(workflow_input['agents'])}):")
    for agent in workflow_input["agents"]:
        print(f"  - {agent['agent_name']}: {agent['description']}")
    print(f"\nEdges ({len(workflow_input['edges'])}):")
    for edge in workflow_input["edges"]:
        print(f"  - {edge['source']} -> {edge['target']}")
    print(f"\nEntry Points: {workflow_input['entry_points']}")
    print(f"End Points: {workflow_input['end_points']}")
    print(f"Max Loops: {workflow_input['max_loops']}")
    print(f"Auto Compile: {workflow_input['auto_compile']}")
    print("=" * 80)
    print()


def print_results(result):
    """Print workflow execution results in a formatted way."""
    print("=" * 80)
    print("Workflow Execution Results")
    print("=" * 80)
    print(f"Job ID: {result.get('job_id')}")
    print(f"Status: {result.get('status')}")
    print(f"Timestamp: {result.get('timestamp')}")
    print("\nOutputs:")
    outputs = result.get("outputs", {})
    for agent_name in workflow_input["entry_points"] + [
        agent["agent_name"] for agent in workflow_input["agents"]
    ]:
        if agent_name in outputs:
            output = outputs[agent_name]
            output_str = str(output)
            if len(output_str) > 300:
                output_preview = output_str[:300] + "..."
            else:
                output_preview = output_str
            print(f"\n  {agent_name}:")
            print(f"    {output_preview}")
    print("\nUsage Statistics:")
    usage = result.get("usage", {})
    print(f"  Input tokens: {usage.get('input_tokens', 0):,}")
    print(f"  Output tokens: {usage.get('output_tokens', 0):,}")
    print(f"  Total tokens: {usage.get('total_tokens', 0):,}")
    print(f"  Token cost: ${usage.get('token_cost', 0):.4f}")
    print(f"  Cost per agent: ${usage.get('cost_per_agent', 0):.4f}")
    print("=" * 80)


def main():
    """Main function to execute the workflow."""
    global workflow_input
    workflow_input = create_market_research_workflow()

    print_workflow_summary(workflow_input)

    print("Sending GraphWorkflow request...")
    try:
        response = post(
            f"{BASE_URL}/v1/graph-workflow/completions",
            headers=headers,
            json=workflow_input,
            timeout=600,  # 10 minute timeout for complex workflows
        )

        response.raise_for_status()

        result = response.json()
        print_results(result)

        # Optionally save results to file
        output_file = f"workflow_result_{result.get('job_id')}.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nResults saved to: {output_file}")

    except HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
