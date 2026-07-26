#!/bin/bash
# Hello, Agent (cURL)
# The same request as hello_agent.py, with no dependencies but curl.
#
# Usage:
#   export SWARMS_API_KEY="your-api-key"
#   bash hello_agent.sh

set -euo pipefail

API_KEY="${SWARMS_API_KEY:?SWARMS_API_KEY is not set}"
BASE_URL="${SWARMS_API_BASE_URL:-https://api.swarms.world}"

curl -X POST "${BASE_URL}/v1/agent/completions" \
  -H "x-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_config": {
      "agent_name": "Research Analyst",
      "description": "Analyzes information and reports the key takeaways",
      "system_prompt": "You are a research analyst. Read the question, identify what actually matters, and answer in clear, structured prose.",
      "model_name": "gpt-4.1",
      "max_loops": 1,
      "max_tokens": 8192,
      "temperature": 0.5
    },
    "task": "What are the main tradeoffs between vector search and keyword search?"
  }'
