#!/bin/bash
# ICD-10 Coding Swarm (cURL)
# Extract, explain and validate ICD-10 codes with a ConcurrentWorkflow swarm.
#
# Usage:
#   export SWARMS_API_KEY="your-api-key"
#   bash icd10_coding_swarm.sh

set -euo pipefail

API_KEY="${SWARMS_API_KEY:?SWARMS_API_KEY is not set}"
BASE_URL="${SWARMS_API_BASE_URL:-https://api.swarms.world}"

curl -X POST "${BASE_URL}/v1/swarm/completions" \
  -H "x-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ICD-10 Coding Assistant",
    "description": "A specialized swarm for accurate ICD-10 coding with explanation and validation",
    "agents": [
      {
        "agent_name": "Code Extractor",
        "description": "Extracts ICD-10 codes from clinical documentation",
        "system_prompt": "Extract ICD-10 codes from clinical documentation. List codes by importance (principal diagnosis first), one per line. Use only explicitly documented codes, choose most specific codes, and follow proper sequencing.",
        "model_name": "gpt-4.1",
        "role": "worker",
        "max_loops": 1,
        "max_tokens": 8192,
        "temperature": 0.3,
        "auto_generate_prompt": false
      },
      {
        "agent_name": "Code Explainer",
        "description": "Explains the rationale for each ICD-10 code",
        "system_prompt": "Explain each ICD-10 code with: code meaning, selection rationale, supporting documentation, and relevant guidelines. Format as: Code, Description, Justification, Supporting Documentation, Guidelines.",
        "model_name": "gpt-4.1",
        "role": "worker",
        "max_loops": 1,
        "max_tokens": 8192,
        "temperature": 0.5,
        "auto_generate_prompt": false
      },
      {
        "agent_name": "Code Validator",
        "description": "Validates code assignments and explanations",
        "system_prompt": "Validate ICD-10 codes by checking: accuracy/specificity, documentation support, sequencing, guideline compliance, and missing codes. Format as: Code, Status, Issues, Recommendations, Gaps.",
        "model_name": "groq/deepseek-r1-distill-llama-70b",
        "role": "worker",
        "max_loops": 1,
        "max_tokens": 8192,
        "temperature": 0.3,
        "auto_generate_prompt": false
      }
    ],
    "max_loops": 1,
    "swarm_type": "ConcurrentWorkflow",
    "task": "Code this case:\n\n61M with CHF (EF 35%) admitted for SOB, chest pressure. NSTEMI (troponin 0.25), BNP 1250. PCI to LAD. Type 2 DM with nephropathy (GFR 42). HTN, HLD. Discharged on cardiac meds and insulin."
  }'
