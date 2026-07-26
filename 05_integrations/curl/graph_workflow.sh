#!/bin/bash
# Graph Workflow (cURL)
# Run a two-node directed graph (researcher -> analyzer).
#
# Usage:
#   export SWARMS_API_KEY="your-api-key"
#   bash graph_workflow.sh

set -euo pipefail

API_KEY="${SWARMS_API_KEY:?SWARMS_API_KEY is not set}"
BASE_URL="${SWARMS_API_BASE_URL:-https://api.swarms.world}"

curl -s "${BASE_URL}/v1/graph-workflow/completions" \
  -H "x-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Quick Sequential",
    "task": "What are the latest AI breakthroughs as of November 2025?",
    "entry_points": ["Researcher"],
    "end_points": ["Analyzer"],
    "agents": [
      {
        "agent_name": "Researcher",
        "system_prompt": "You are an expert researcher. Be accurate and up-to-date.",
        "model_name": "gpt-4o",
        "temperature": 0.3,
        "max_tokens": 6000
      },
      {
        "agent_name": "Analyzer",
        "system_prompt": "You are a sharp analyst. Summarize clearly and highlight key insights.",
        "model_name": "gpt-4o",
        "temperature": 0.4,
        "max_tokens": 5000
      }
    ],
    "edges": [{"source": "Researcher", "target": "Analyzer"}]
  }'