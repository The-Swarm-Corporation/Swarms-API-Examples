# 02 · Single Agent

Everything one agent can do. A single agent is often the right answer — reach for a
swarm only when the work genuinely splits across specialists.

All of these hit `POST /v1/agent/completions` unless noted.

## Basics

Start here. `agent_completion.py` is the reference for every field an `agent_config`
accepts.

| File | What it shows |
|---|---|
| [`basics/agent_completion.py`](basics/agent_completion.py) | The full agent config surface: model, prompt, loops, tokens, temperature |
| [`basics/max_loops_auto.py`](basics/max_loops_auto.py) | `"max_loops": "auto"` — let the API decide how much reasoning the task needs |
| [`basics/conversation_history.py`](basics/conversation_history.py) | What the agent carries across loops, plus a health check |
| [`basics/batch_completions.py`](basics/batch_completions.py) | Many independent completions in one request |
| [`basics/agent_handoffs.py`](basics/agent_handoffs.py) | Give an agent specialists it can delegate to mid-task |

## Streaming

Set `"stream": true` and read server-sent events as tokens are produced.

| File | What it shows |
|---|---|
| [`streaming/stream_agent_response.py`](streaming/stream_agent_response.py) | The standard streaming client |
| [`streaming/minimal_streaming.py`](streaming/minimal_streaming.py) | The smallest streaming client that works |
| [`streaming/streaming_with_tools.py`](streaming/streaming_with_tools.py) | Streaming an agent that also has tools |
| [`streaming/streaming_agent_and_swarm.py`](streaming/streaming_agent_and_swarm.py) | Streaming both the agent and the swarm endpoints, with error handling |
| [`streaming/inspect_raw_stream_events.py`](streaming/inspect_raw_stream_events.py) | Raw, unparsed SSE lines — for debugging a stalled stream |

Streaming a whole swarm: [`../03_multi_agent/streaming/`](../03_multi_agent/streaming/).

## Vision

Pass an image through the `img` field. Base64 data URLs and local files both work.

| File | What it shows |
|---|---|
| [`vision/analyze_image_from_url.py`](vision/analyze_image_from_url.py) | Fetch a remote image, encode it, describe it |
| [`vision/analyze_local_image.py`](vision/analyze_local_image.py) | Read an image from disk |
| [`vision/analyze_image_sdk.py`](vision/analyze_image_sdk.py) | Vision through the SDK, with a marketplace prompt |

## Reasoning

| File | What it shows |
|---|---|
| [`reasoning/reasoning_agents.py`](reasoning/reasoning_agents.py) | The `AgentJudge` type — an agent that evaluates work rather than producing it |
| [`reasoning/reasoning_agent_types.py`](reasoning/reasoning_agent_types.py) | List the reasoning types available, then run `reasoning-duo` |

## Models

The same agent on different frontier models. Swap `model_name` to compare.

| File | Model |
|---|---|
| [`models/claude_opus_5.py`](models/claude_opus_5.py) | `anthropic/claude-opus-5` via the SDK, with `reasoning_effort` |
| [`models/claude_opus_4_8.py`](models/claude_opus_4_8.py) | `anthropic/claude-opus-4-8` via the SDK |
| [`models/claude_opus_4_8_httpx.py`](models/claude_opus_4_8_httpx.py) | The same request with `httpx`, no SDK |

See every model your account can route to with
[`../06_platform_utilities/list_models.py`](../06_platform_utilities/list_models.py).

## Next

When one agent isn't enough → [`../03_multi_agent/`](../03_multi_agent/)
