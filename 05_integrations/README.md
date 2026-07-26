# 05 · Integrations

Ways to reach the Swarms API other than `requests`.

## Python SDK

`pip install swarms-client`

The SDK handles auth, retries, timeouts, and response parsing. Prefer it for
application code; the raw-HTTP examples elsewhere in this repo exist to show the
wire format.

| File | What it shows |
|---|---|
| [`sdk/run_swarm_with_sdk.py`](sdk/run_swarm_with_sdk.py) | Running a swarm through `SwarmsClient` |

Also using the SDK: [`../01_getting_started/hello_agent_sdk.py`](../01_getting_started/hello_agent_sdk.py),
[`../02_single_agent/models/`](../02_single_agent/models/),
[`../02_single_agent/vision/analyze_image_sdk.py`](../02_single_agent/vision/analyze_image_sdk.py),
[`../06_platform_utilities/list_models.py`](../06_platform_utilities/list_models.py).

## MCP

`pip install fastmcp`

Exposes the Swarms API as [Model Context Protocol](https://modelcontextprotocol.io)
tools, so any MCP client — Claude Code, Claude Desktop, Cursor — can run swarms
directly.

| File | What it shows |
|---|---|
| [`mcp/swarms_api_mcp_server.py`](mcp/swarms_api_mcp_server.py) | The MCP server |
| [`mcp/mcp_client_test.py`](mcp/mcp_client_test.py) | A client that connects and calls a tool — use it to verify the server |

```bash
export SWARMS_API_KEY="your-api-key"
python mcp/swarms_api_mcp_server.py        # terminal 1
python mcp/mcp_client_test.py              # terminal 2
```

The client connects to `http://localhost:8000/sse` by default — change the transport
URL in the client if you run the server elsewhere.

## cURL

No dependencies, and the clearest view of the actual request body. Every script
reads `SWARMS_API_KEY` from the environment and exits if it isn't set.

| File | Endpoint |
|---|---|
| [`curl/swarm_completion.sh`](curl/swarm_completion.sh) | `POST /v1/swarm/completions` — a sequential swarm |
| [`curl/graph_workflow.sh`](curl/graph_workflow.sh) | `POST /v1/graph-workflow/completions` |
| [`curl/batched_grid_workflow.sh`](curl/batched_grid_workflow.sh) | `POST /v1/batched-grid-workflow/completions` |
| [`curl/icd10_coding_swarm.sh`](curl/icd10_coding_swarm.sh) | A concurrent clinical-coding swarm |

```bash
export SWARMS_API_KEY="your-api-key"
bash curl/swarm_completion.sh
```

A single-agent cURL request is in
[`../01_getting_started/hello_agent.sh`](../01_getting_started/hello_agent.sh).
`batched_grid_workflow.sh` pipes through `jq` — install it or drop the pipe.
