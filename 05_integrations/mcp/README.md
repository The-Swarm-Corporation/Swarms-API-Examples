# MCP (Model Context Protocol)

Exposes the Swarms API as [MCP](https://modelcontextprotocol.io) tools, so any
MCP-compatible client — Claude Code, Claude Desktop, Cursor — can run swarms directly
as part of a conversation instead of you writing a script.

```bash
pip install fastmcp
```

## Files

| File | What it is |
|---|---|
| [`swarms_api_mcp_server.py`](swarms_api_mcp_server.py) | The MCP server — exposes swarm execution and model listing as tools |
| [`mcp_client_test.py`](mcp_client_test.py) | A `fastmcp` client that connects and calls a tool — use it to verify the server before wiring up a real client |

## Running it

```bash
export SWARMS_API_KEY="your-api-key"

python swarms_api_mcp_server.py     # terminal 1 — serves on http://localhost:8000/sse
python mcp_client_test.py           # terminal 2 — connects and calls a tool
```

The client's transport URL is set in [`mcp_client_test.py`](mcp_client_test.py); change
it there if you run the server on a different host or port.

## Connecting a real client

Point your MCP client at the running server's SSE endpoint (`http://localhost:8000/sse`
by default). The exact configuration depends on the client — consult its MCP docs for
where server definitions live.

Once connected, the client can invoke swarms as tools: it sends the agent roster and
task, the server calls the Swarms API, and the result comes back into the conversation.

## Tips

- **Verify with the test client first.** If [`mcp_client_test.py`](mcp_client_test.py)
  can't reach the server, no other MCP client will either — that isolates transport
  problems from client-configuration problems.
- **The server needs its own `SWARMS_API_KEY`.** It calls the Swarms API on the
  client's behalf; the MCP client never sees your key.
- **Swarm runs take minutes.** MCP clients with short tool timeouts may give up before
  a heavy swarm returns — prefer smaller swarm types for interactive use.
