# 01 · Getting Started

Four ways to make your first Swarms API call. Each file is short, commented, and
runs on its own.

Start with `hello_agent.py`, then `hello_swarm.py`.

| File | What it shows |
|---|---|
| [`hello_agent.py`](hello_agent.py) | One agent, one task, one response — the smallest useful request |
| [`hello_swarm.py`](hello_swarm.py) | Three agents chained with `SequentialWorkflow` |
| [`hello_agent_sdk.py`](hello_agent_sdk.py) | The same agent request through the `swarms-client` SDK |
| [`hello_agent.sh`](hello_agent.sh) | The same agent request with nothing but `curl` |

## Setup

```bash
pip install requests python-dotenv
export SWARMS_API_KEY="your-api-key"
python hello_agent.py
```

Or put the key in a `.env` file at the repo root (`cp .env.example .env`) — every
example calls `load_dotenv()`.

## The two request shapes

Everything in this repo is one of these two calls.

**One agent** — `POST /v1/agent/completions`

```json
{
  "agent_config": { "agent_name": "...", "system_prompt": "...", "model_name": "..." },
  "task": "..."
}
```

**Many agents** — `POST /v1/swarm/completions`

```json
{
  "name": "...",
  "swarm_type": "SequentialWorkflow",
  "agents": [ { "agent_name": "...", "system_prompt": "...", "model_name": "..." } ],
  "task": "..."
}
```

The swarm request is the agent request with an `agents` list and a `swarm_type`.
Everything else — streaming, vision, tools, handoffs — is a field you add to one of
these two bodies.

## Next

- Every field an agent accepts → [`../02_single_agent/basics/agent_completion.py`](../02_single_agent/basics/agent_completion.py)
- Choosing a `swarm_type` → [`../03_multi_agent/`](../03_multi_agent/)
- A finished, real-world build → [`../04_industry_examples/`](../04_industry_examples/)
