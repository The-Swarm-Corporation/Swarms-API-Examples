# Single Agent — Models

The same agent, the same task, different models. Change `model_name` and nothing else
to compare behaviour, cost, and latency on your own workload.

**Endpoint:** `POST /v1/agent/completions`

## Naming

Models are addressed as `provider/model`:

```
anthropic/claude-opus-5
openai/gpt-4o
groq/deepseek-r1-distill-llama-70b
```

Some short names (`gpt-4.1`, `gpt-4o`) resolve without a prefix. List everything your
account can route to with
[`../../06_platform_utilities/list_models.py`](../../06_platform_utilities/list_models.py).

## Examples

| File | Model | Transport |
|---|---|---|
| [`claude_opus_5.py`](claude_opus_5.py) | `anthropic/claude-opus-5` | `swarms-client` SDK |
| [`claude_opus_4_8.py`](claude_opus_4_8.py) | `anthropic/claude-opus-4-8` | `swarms-client` SDK |
| [`claude_opus_4_8_httpx.py`](claude_opus_4_8_httpx.py) | `anthropic/claude-opus-4-8` | `httpx`, no SDK |

The two Opus 4.8 files send the same request — one through the SDK, one by hand — so
you can see exactly what the SDK builds for you.

For every other provider — GPT-5, Claude Sonnet 5, Gemini, Groq, DeepSeek, Grok,
OpenRouter — plus a side-by-side comparison script, see
[`../../07_model_integrations/`](../../07_model_integrations/).

## Reasoning effort

Frontier reasoning models accept a `reasoning_effort` field controlling how much
thinking they do before answering:

```python
agent_config = {
    "agent_name": "ETF Research Analyst",
    "model_name": "anthropic/claude-opus-5",
    "reasoning_effort": "low",   # low | medium | high
    "max_tokens": 16000,
}
```

Higher effort costs more tokens and takes longer. Start low and raise it only where
your evaluation shows it helps — see [`claude_opus_5.py`](claude_opus_5.py).

## Picking a model

| Priority | Approach |
|---|---|
| Quality on hard reasoning | A frontier model at higher `reasoning_effort` |
| Cost and latency at volume | A smaller model — most swarm agents don't need a frontier model |
| Mixed | Different `model_name` per agent inside one swarm; that is allowed and common |

Swarm agents each carry their own `model_name`, so a coordinator can run on a frontier
model while the workers run on something cheaper. See
[`../../03_multi_agent/hierarchical_swarm/`](../../03_multi_agent/hierarchical_swarm/).
