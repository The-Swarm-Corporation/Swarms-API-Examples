"""
Simple Medical Swarm
====================

The shortest clinical example in this folder — a good starting point before
the enterprise version.

Run:
    python simple_medical_swarm.py

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
# Standard headers for all requests
headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def run_swarm(swarm_config):
    """Execute a swarm with the provided configuration."""
    response = requests.post(
        f"{BASE_URL}/v1/swarm/completions", headers=headers, json=swarm_config
    )
    return response.json()


def create_simple_medical_swarm(patient_symptoms):
    """
    Create a simple medical diagnosis swarm.

    Args:
        patient_symptoms (str): Patient symptoms and medical history

    Returns:
        dict: The swarm execution result containing diagnosis and recommendations.
    """

    # Configure a simple 2-agent medical swarm
    swarm_config = {
        "name": "Simple Medical Assistant",
        "description": "A basic medical diagnosis and treatment recommendation system",
        "agents": [
            {
                "agent_name": "Diagnostician",
                "description": "Analyzes symptoms and provides initial diagnosis",
                "system_prompt": """You are a medical diagnostician. Analyze the patient's symptoms and provide:
                1. A likely diagnosis
                2. Key symptoms that support this diagnosis
                3. Any red flags that require immediate attention

                Keep your response clear and professional.""",
                "model_name": "claude-sonnet-4-20250514",
                "role": "worker",
                "max_loops": 1,
                "max_tokens": 2048,
                "temperature": 0.3,
            },
            {
                "agent_name": "Treatment Advisor",
                "description": "Provides treatment recommendations based on diagnosis",
                "system_prompt": """You are a treatment advisor. Based on the diagnosis provided, suggest:
1. Recommended treatments or medications
2. Lifestyle modifications
3. When to seek immediate medical care
4. Follow-up recommendations

Focus on practical, actionable advice.""",
                "model_name": "groq/llama3-70b-8192",
                "role": "worker",
                "max_loops": 1,
                "max_tokens": 2048,
                "temperature": 0.4,
            },
        ],
        "max_loops": 1,
        "swarm_type": "SequentialWorkflow",
        "task": f"""
        Analyze the following patient symptoms and provide a medical assessment:

        Patient Symptoms:
        {patient_symptoms}

        Please provide:
        1. A likely diagnosis
        2. Treatment recommendations
        3. Any urgent concerns
        """,
    }

    # Execute the swarm
    result = run_swarm(swarm_config)
    return result


def run_simple_medical_example():
    """Run a simple medical diagnosis example."""

    # Simple patient case
    patient_symptoms = """
    Patient: 45-year-old female
    Chief Complaint: Chest pain and shortness of breath for 2 days
    
    Symptoms:
    - Sharp chest pain that worsens with deep breathing
    - Shortness of breath, especially when lying down
    - Mild fever (100.2°F)
    - Dry cough
    - Fatigue
    
    Medical History:
    - No significant medical history
    - Non-smoker
    - No recent travel or surgery
    """

    # Run the medical swarm
    result = create_simple_medical_swarm(patient_symptoms)

    # Print the result
    print("=== Simple Medical Diagnosis Example ===\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    run_simple_medical_example()
