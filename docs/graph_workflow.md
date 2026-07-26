# GraphWorkflow API Examples

This directory contains Python examples demonstrating how to use the GraphWorkflow endpoint with the `requests` library.

## Overview

The GraphWorkflow endpoint enables you to create and execute complex multi-agent workflows with directed graphs. Each workflow consists of:
- **Nodes**: Agents that process tasks
- **Edges**: Connections defining data flow between agents
- **Entry Points**: Starting nodes for the workflow
- **End Points**: Terminal nodes for the workflow

## Prerequisites

1. Install required dependencies:
```bash
pip install requests python-dotenv
```

2. Set up your environment variables:
```bash
export SWARMS_API_KEY="your-api-key-here"
export SWARMS_BASE_URL="https://api.swarms.world"  # Optional, defaults to this
```

Or create a `.env` file:
```
SWARMS_API_KEY=your-api-key-here
SWARMS_BASE_URL=https://api.swarms.world
```

## Example Files

### 1. Basic Sequential Workflow (`graph_workflow_basic_example.py`)

Demonstrates a simple two-agent sequential workflow:
- ResearchAgent → AnalysisAgent

**Key Features:**
- Simple sequential flow
- Basic edge definition
- Entry and end points configuration

**Run:**
```bash
python graph_workflow_basic_example.py
```

### 2. Parallel Processing Workflow (`graph_workflow_parallel_example.py`)

Demonstrates fan-out and fan-in patterns:
- DataCollector → [TechnicalAnalyst, FundamentalAnalyst, SentimentAnalyst] → SynthesisAgent

**Key Features:**
- Fan-out pattern (one source to multiple targets)
- Fan-in pattern (multiple sources to one target)
- Parallel agent execution

**Run:**
```bash
python graph_workflow_parallel_example.py
```

### 3. Complex Multi-Layer Workflow (`graph_workflow_complex_example.py`)

Demonstrates a three-layer workflow with parallel processing:
- Layer 1: Multiple data collectors
- Layer 2: Multiple analysts (parallel chain)
- Layer 3: Validators and synthesis

**Key Features:**
- Multiple workflow layers
- Parallel chain patterns
- Complex edge configurations

**Run:**
```bash
python graph_workflow_complex_example.py
```

### 4. Workflow with Metadata (`graph_workflow_with_metadata_example.py`)

Demonstrates adding custom metadata to edges:
- ResearchAgent → AnalysisAgent (with metadata)
- AnalysisAgent → ReportGenerator (with metadata)

**Key Features:**
- Edge metadata for additional context
- Custom configuration per edge

**Run:**
```bash
python graph_workflow_with_metadata_example.py
```

### 5. Edge Format Examples (`graph_workflow_edge_formats_example.py`)

Demonstrates different ways to define edges:
- Dictionary format (simple)
- Dictionary format with metadata
- Alternative formats

**Key Features:**
- Multiple edge definition formats
- Flexibility in edge specification

**Run:**
```bash
python graph_workflow_edge_formats_example.py
```

### 6. Complete Example (`graph_workflow_complete_example.py`)

Comprehensive example with all features:
- Multiple specialized agents
- Complex edge patterns
- Error handling
- Result processing and saving

**Key Features:**
- Full workflow configuration
- Error handling and timeouts
- Result formatting and saving
- Usage statistics

**Run:**
```bash
python graph_workflow_complete_example.py
```

## API Endpoint

**Endpoint:** `POST /v1/graph-workflow/completions`

**Headers:**
```
x-api-key: YOUR_API_KEY
Content-Type: application/json
```

## Request Schema

```python
{
    "name": "Workflow-Name",
    "description": "Workflow description",
    "agents": [
        {
            "agent_name": "Agent1",
            "description": "Agent description",
            "system_prompt": "System prompt",
            "model_name": "gpt-4.1",
            "max_tokens": 4000,
            "temperature": 0.3,
            "max_loops": 1
        }
    ],
    "edges": [
        {
            "source": "Agent1",
            "target": "Agent2",
            "metadata": {}  # Optional
        }
    ],
    "entry_points": ["Agent1"],
    "end_points": ["Agent2"],
    "max_loops": 1,
    "task": "Task description",
    "auto_compile": True,
    "verbose": False
}
```

## Response Schema

```python
{
    "job_id": "unique-job-id",
    "name": "Workflow-Name",
    "description": "Workflow description",
    "status": "success",
    "outputs": {
        "Agent1": "output from agent 1",
        "Agent2": "output from agent 2"
    },
    "usage": {
        "input_tokens": 1000,
        "output_tokens": 500,
        "total_tokens": 1500,
        "token_cost": 0.0125,
        "cost_per_agent": 0.02
    },
    "timestamp": "2024-01-01T00:00:00Z"
}
```

## Edge Patterns

### Sequential Flow
```python
edges = [
    {"source": "Agent1", "target": "Agent2"},
    {"source": "Agent2", "target": "Agent3"}
]
```

### Fan-Out Pattern
```python
edges = [
    {"source": "DataCollector", "target": "Analyst1"},
    {"source": "DataCollector", "target": "Analyst2"},
    {"source": "DataCollector", "target": "Analyst3"}
]
```

### Fan-In Pattern
```python
edges = [
    {"source": "Analyst1", "target": "SynthesisAgent"},
    {"source": "Analyst2", "target": "SynthesisAgent"},
    {"source": "Analyst3", "target": "SynthesisAgent"}
]
```

### Parallel Chain Pattern
```python
edges = [
    {"source": "Collector1", "target": "Analyst1"},
    {"source": "Collector1", "target": "Analyst2"},
    {"source": "Collector2", "target": "Analyst1"},
    {"source": "Collector2", "target": "Analyst2"}
]
```

## Best Practices

1. **Agent Naming**: Use descriptive, unique agent names
2. **Entry Points**: Always specify entry points for clarity
3. **End Points**: Specify end points to control workflow termination
4. **Auto Compile**: Enable `auto_compile` for better performance
5. **Error Handling**: Implement proper error handling and timeouts
6. **Usage Monitoring**: Monitor token usage and costs
7. **Metadata**: Use edge metadata for additional context when needed

## Error Handling

All examples include basic error handling. For production use, implement:
- Retry logic for transient failures
- Exponential backoff
- Comprehensive logging
- Monitoring and alerting

## Cost Considerations

The workflow cost includes:
- Agent cost: $0.01 per agent
- Input tokens: $4.00 per 1M tokens
- Output tokens: $12.50 per 1M tokens

Monitor usage statistics in the response to track costs.

## Support

For issues or questions:
- Check the API documentation: https://docs.swarms.ai
- Review the endpoint documentation in the API
- Contact support: https://cal.com/swarms

