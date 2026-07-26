"""
ICD-10 Coding Swarm
===================

Extracts, explains and validates ICD-10 codes from clinical documentation —
one agent per step, run sequentially.

Run:
    python icd10_coding_swarm.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    "Accept-Encoding": "lz4",
}

# Clinical documentation
clinical_documentation = """
DISCHARGE SUMMARY

Patient: John Smith
MRN: 12345678
DOB: 01/15/1962
Admission Date: 06/10/2023
Discharge Date: 06/15/2023

FINAL DIAGNOSES:
1. Acute exacerbation of chronic systolic congestive heart failure
2. Non-ST elevation myocardial infarction
3. Type 2 diabetes mellitus with diabetic nephropathy, estimated GFR 42
4. Hypertension
5. Hyperlipidemia

HISTORY OF PRESENT ILLNESS:
The patient is a 61-year-old male with a history of congestive heart failure (EF 35% on prior echo 3 months ago) who presented to the emergency department with a 3-day history of worsening shortness of breath, orthopnea, and lower extremity edema. The patient reported chest pressure while walking to the bathroom. Initial troponin was elevated at 0.15 ng/mL, with subsequent rise to 0.25 ng/mL, consistent with NSTEMI. BNP was significantly elevated at 1,250 pg/mL.

HOSPITAL COURSE:
The patient was admitted to the cardiac care unit. He was treated with IV furosemide with good diuretic response, losing 3.5 liters of fluid during hospitalization. Cardiology was consulted and performed a left heart catheterization, which revealed 70% stenosis in the mid-LAD with PCI and drug-eluting stent placement. The patient's symptoms improved significantly with diuresis and coronary intervention.

His diabetes was managed with insulin during the hospitalization, with blood glucose ranging from 130-210 mg/dL. Nephrology was consulted regarding his diabetic nephropathy and recommended adjustment of medications appropriate for his renal function.

PROCEDURES:
1. Left heart catheterization with percutaneous coronary intervention and drug-eluting stent placement to mid-LAD (06/12/2023)

DISCHARGE MEDICATIONS:
1. Lisinopril 10 mg daily
2. Carvedilol 12.5 mg twice daily
3. Spironolactone 25 mg daily
4. Furosemide 40 mg twice daily
5. Atorvastatin 80 mg daily
6. Aspirin 81 mg daily
7. Clopidogrel 75 mg daily
8. Insulin glargine 20 units nightly
9. Insulin lispro sliding scale before meals

DISCHARGE PLAN:
1. Follow-up with cardiology in 2 weeks
2. Follow-up with primary care physician in 1 week
3. Follow-up with nephrology in 3 weeks
4. Daily weights, 2 gram sodium diet, fluid restriction to 1.5 liters daily
"""

# Swarm configuration
swarm_config = {
    "name": "ICD-10 Coding Assistant",
    "description": "A specialized swarm for accurate ICD-10 coding with explanation and validation",
    "agents": [
        {
            "agent_name": "Code Extractor",
            "description": "Extracts ICD-10 codes from clinical documentation",
            "system_prompt": "You are a precise ICD-10 code extractor. Extract ONLY the ICD-10 codes from clinical documentation. List them in order of importance (principal diagnosis first). Do not include explanations. Format as a clean list of codes.",
            "model_name": "claude-sonnet-4-20250514",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 8192,
            "temperature": 0.3,
            "auto_generate_prompt": False,
        },
        {
            "agent_name": "Code Explainer",
            "description": "Explains the rationale for each ICD-10 code",
            "system_prompt": "You are an expert ICD-10 code explainer. For each code, explain what it represents, why it was chosen, key documentation elements, and relevant coding guidelines.",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 8192,
            "temperature": 0.5,
            "auto_generate_prompt": False,
        },
        {
            "agent_name": "Code Validator",
            "description": "Validates code assignments and explanations",
            "system_prompt": "You are a thorough ICD-10 code validator. Verify code accuracy, documentation support, proper sequencing, compliance with guidelines, and identify missing codes.",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 8192,
            "temperature": 0.3,
            "auto_generate_prompt": False,
        },
    ],
    "max_loops": 1,
    "swarm_type": "SequentialWorkflow",
    "task": f"""
    Analyze the following clinical documentation and provide:
    1. A list of appropriate ICD-10-CM codes
    2. Detailed explanation for each code
    3. Validation of the code assignments

    Clinical Documentation:
    {clinical_documentation}
    """,
}

# Execute the swarm
response = requests.post(
    f"{BASE_URL}/v1/swarm/completions", headers=headers, json=swarm_config
)
result = response.json()

# Print the result
print(json.dumps(result, indent=4))
