"""
Software Development Swarm
==========================

A tech-lead agent decomposing a feature and delegating to architecture, backend
and QA specialists.

Hierarchical Swarm Example - Software Development Planning

Demonstrates a HiearchicalSwarm for software development planning with a
tech lead coordinating backend, frontend, and DevOps specialists.

Run:
    python software_dev_swarm.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

payload = {
    "name": "Software Development Hierarchical Swarm",
    "description": "A hierarchical swarm for comprehensive software development planning",
    "swarm_type": "HiearchicalSwarm",
    "task": """
    Design the technical architecture for a real-time collaborative document editing 
    platform similar to Google Docs, targeting enterprise customers.
    
    Requirements:
    1. Support for 100+ concurrent editors per document
    2. Real-time synchronization with conflict resolution
    3. Enterprise-grade security and compliance
    4. Mobile and desktop application support
    """,
    "max_loops": 1,
    "agents": [
        {
            "agent_name": "Tech Lead",
            "description": "Senior technical leader coordinating architecture and development strategy",
            "system_prompt": """You are a Senior Tech Lead with 15+ years of experience in software architecture.

Your role is to:
1. Define overall system architecture and technical direction
2. Coordinate between frontend, backend, and DevOps teams
3. Ensure code quality, scalability, and maintainability
4. Identify technical risks and mitigation strategies

Synthesize team inputs into a cohesive technical strategy with clear deliverables.""",
            "model_name": "gpt-4.1",
            "role": "coordinator",
            "max_loops": 1,
            "max_tokens": 8192,
            "temperature": 0.3,
        },
        {
            "agent_name": "Backend Developer",
            "description": "Expert in server-side development, APIs, and database design",
            "system_prompt": """You are a Senior Backend Developer specializing in scalable server-side systems.

Your expertise includes:
1. API design and RESTful/GraphQL architecture
2. Database design and optimization
3. Microservices and distributed systems
4. Authentication, authorization, and security

Provide technical recommendations with specific technology choices and implementation patterns.""",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.4,
        },
        {
            "agent_name": "Frontend Developer",
            "description": "Specialist in UI/UX implementation and client-side architecture",
            "system_prompt": """You are a Senior Frontend Developer with expertise in modern web applications.

Your focus areas include:
1. Frontend framework selection and architecture
2. UI component design and state management
3. Performance optimization and bundle size
4. Accessibility and responsive design

Provide detailed frontend implementation recommendations with best practices.""",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.4,
        },
        {
            "agent_name": "DevOps Engineer",
            "description": "Expert in CI/CD, infrastructure, and deployment automation",
            "system_prompt": """You are a Senior DevOps Engineer specializing in cloud infrastructure.

Your expertise covers:
1. CI/CD pipeline design and implementation
2. Container orchestration and Kubernetes
3. Infrastructure as Code (IaC)
4. Monitoring, logging, and observability

Provide infrastructure recommendations that ensure reliability, scalability, and security.""",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.4,
        },
    ],
}

response = requests.post(
    f"{BASE_URL}/v1/swarm/completions",
    headers=headers,
    json=payload,
    timeout=300,
)

print(json.dumps(response.json(), indent=2))
