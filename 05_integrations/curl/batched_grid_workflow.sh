#!/bin/bash
# Batched Grid Workflow (cURL)
# Run a grid of agents across a list of tasks in one request.
#
# Usage:
#   export SWARMS_API_KEY="your-api-key"
#   bash batched_grid_workflow.sh

set -euo pipefail

API_KEY="${SWARMS_API_KEY:?SWARMS_API_KEY is not set}"
BASE_URL="${SWARMS_API_BASE_URL:-https://api.swarms.world}"

# Create the JSON payload
read -r -d '' PAYLOAD << 'EOF'
{
  "name": "Content-Analysis-Grid",
  "description": "Multi-agent content analysis workflow",
  "agent_completions": [
    {
      "agent_name": "Content-Analyzer",
      "system_prompt": "You are an expert content analyst who evaluates text for quality, clarity, and effectiveness.",
      "model_name": "gpt-4.1",
      "max_tokens": 2000,
      "temperature": 0.4,
      "max_loops": 1
    },
    {
      "agent_name": "SEO-Specialist",
      "system_prompt": "You are an SEO expert who analyzes content for search engine optimization opportunities.",
      "model_name": "gpt-4.1",
      "max_tokens": 2000,
      "temperature": 0.4,
      "max_loops": 1
    }
  ],
  "tasks": [
    "Analyze this blog post topic: 'The Future of AI in Healthcare'",
    "Evaluate this content idea: 'How Multi-Agent Systems Transform Business Operations'"
  ],
  "max_loops": 1,
  "imgs": []
}
EOF

echo "Submitting batched grid workflow request..."
echo "=========================================="

# Make the API request
curl -X POST "${BASE_URL}/v1/batched-grid-workflow/completions" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d "${PAYLOAD}" \
  --max-time 300 \
  | jq '.'

echo ""
echo "Request completed."

