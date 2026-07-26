# 06 · Platform Utilities

Short scripts for inspecting your account and what the platform offers. Each one is a
single GET — run them when you need an answer, not as part of an application.

## Discovery

| File | Endpoint | Answers |
|---|---|---|
| [`list_models.py`](list_models.py) | `/v1/models/available` | Which models can I route to? |
| [`list_swarm_types.py`](list_swarm_types.py) | `/v1/swarms/available` | Which swarm types can I use? |
| [`list_agents.py`](list_agents.py) | `/v1/agents/list` | Which agents have I saved? |

## Quota and cost

| File | Endpoint | Answers |
|---|---|---|
| [`check_rate_limits.py`](check_rate_limits.py) | `/v1/rate/limits` | What are my limits, and what's left? |
| [`check_premium_rate_limits.py`](check_premium_rate_limits.py) | `/v1/rate/limits` | What do premium tiers get, and which models do they reach? |
| [`check_account_credits.py`](check_account_credits.py) | `/v1/account/credits` | What's my balance? |
| [`check_usage_costs.py`](check_usage_costs.py) | `/v1/usage/costs` | What have I spent, by request? |
| [`metrics_summary.py`](metrics_summary.py) | `/v1/metrics/summary` | Aggregate usage over time |

## Debugging

| File | Endpoint | Answers |
|---|---|---|
| [`fetch_swarm_logs.py`](fetch_swarm_logs.py) | `/v1/swarm/logs` | What actually happened in that run? |

## Usage

```bash
export SWARMS_API_KEY="your-api-key"
python list_models.py
```

`list_models.py` uses the `swarms-client` SDK (`pip install swarms-client`); the rest
use `requests` or `httpx`.

Hitting a 429? [`check_rate_limits.py`](check_rate_limits.py) tells you which limit
you hit and when it resets. A run that returned nothing useful?
[`fetch_swarm_logs.py`](fetch_swarm_logs.py) shows each agent's actual output.
