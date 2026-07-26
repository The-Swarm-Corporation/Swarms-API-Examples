"""
Medical Coding Swarm
====================

Medical coding assistant built on a sequential workflow, with tool access for
lookups.

Run:
    python medical_coding_swarm.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

# tools - search, code executor, create api

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
MED_SYS_PROMPT = """
You are an Advanced Clinical Research Specialist with extensive expertise in medical research methodology, clinical trial analysis, and evidence-based medicine. 
Your primary responsibilities include:

1. LITERATURE ANALYSIS: Conduct comprehensive reviews of peer-reviewed medical literature, clinical trial data, and research publications. 
Critically evaluate study methodologies, statistical significance, sample sizes, and potential biases.

2. TREATMENT EVALUATION: Analyze the efficacy, safety, and comparative effectiveness of medical treatments and interventions. 
Assess patient outcomes, adverse events, and long-term implications of therapeutic approaches.

3. CLINICAL TRIAL ASSESSMENT: Review and interpret clinical trial results, including Phase I-IV studies, randomized controlled trials, 
meta-analyses, and systematic reviews. Identify strengths, limitations, and clinical applicability of research findings.

4. EVIDENCE SYNTHESIS: Synthesize complex medical data from multiple sources to provide clear, actionable insights. 
Distinguish between correlation and causation, and evaluate the quality and reliability of evidence.

5. RECOMMENDATION FORMULATION: Develop evidence-based recommendations for clinical practice, considering patient populations, 
comorbidities, contraindications, and real-world applicability.

6. RESEARCH GAP IDENTIFICATION: Identify areas requiring further investigation and suggest directions for future research.

Your analysis must be rigorous, objective, and grounded in scientific evidence. Present findings in a structured format that includes: 
executive summary, methodology assessment, key findings, statistical analysis, clinical implications, limitations, and recommendations. 
Maintain scientific accuracy while ensuring accessibility for both medical professionals and stakeholders. 
Always cite sources appropriately and acknowledge the limitations of available evidence.
"""

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def run_health_check():
    response = requests.get(f"{BASE_URL}/health", headers=headers)
    return response.json()


def run_single_swarm():
    payload = {
        "name": "Advanced Medical Analysis Swarm",
        "description": "A highly specialized swarm designed for in-depth medical data analysis and research.",
        "agents": [
            {
                "agent_name": "Clinical Data Analyst",
                "description": "An expert in analyzing clinical data, patient outcomes, and treatment efficacy. This agent synthesizes complex datasets to derive actionable insights.",
                "system_prompt": (
                    "You are a highly skilled Clinical Data Analyst with extensive experience in evaluating clinical trials and patient data. "
                    "Your task is to analyze the provided clinical data, identify trends, and generate comprehensive reports that highlight key findings. "
                    "Consider factors such as patient demographics, treatment protocols, and outcomes. "
                    "Your analysis should be thorough, data-driven, and presented in a way that is accessible to both medical professionals and laypersons. "
                    "Provide recommendations based on your findings and suggest potential areas for further research."
                ),
                "model_name": "gpt-4.1",
                "role": "worker",
                "max_loops": 1,
                "max_tokens": 8192,
                "temperature": 0.5,
                "auto_generate_prompt": False,
                # "tools_dictionary": None,
            },
            {
                "agent_name": "Medical Researcher",
                "description": "A specialist in medical research, focusing on the latest advancements in treatments and therapies. This agent explores innovative solutions and their implications.",
                "system_prompt": MED_SYS_PROMPT,
                "model_name": "gpt-4.1",
                "role": "worker",
                "max_loops": 1,
                "max_tokens": 8192,
                "temperature": 0.5,
                "auto_generate_prompt": False,
                # "tools_dictionary": None,
            },
        ],
        "max_loops": 1,
        "swarm_type": "SequentialWorkflow",
        "task": "Investigate and report on the latest advancements in cancer treatment, focusing on innovative therapies and their clinical implications.",
    }

    response = requests.post(
        f"{BASE_URL}/v1/swarm/completions",
        headers=headers,
        json=payload,
    )

    print(response)
    print(response.status_code)
    output = response.json()

    return json.dumps(output, indent=4)


if __name__ == "__main__":
    result = run_single_swarm()
    print("Swarm Result:")
    print(result)
