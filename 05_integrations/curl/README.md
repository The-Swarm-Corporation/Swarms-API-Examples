# cURL

No dependencies, and the clearest possible view of the actual request body. Useful for
debugging, for shell pipelines, and for translating the API into a language with no SDK.

## Running them

```bash
export SWARMS_API_KEY="your-api-key"
bash swarm_completion.sh
```

Every script reads `SWARMS_API_KEY` from the environment and exits immediately if it
isn't set. Override the host with `SWARMS_API_BASE_URL`.

## Scripts

| File | Endpoint | What it runs |
|---|---|---|
| [`swarm_completion.sh`](swarm_completion.sh) | `POST /v1/swarm/completions` | A two-agent `SequentialWorkflow` |
| [`graph_workflow.sh`](graph_workflow.sh) | `POST /v1/graph-workflow/completions` | A two-node graph, researcher → analyzer |
| [`batched_grid_workflow.sh`](batched_grid_workflow.sh) | `POST /v1/batched-grid-workflow/completions` | Two agents crossed with two tasks |
| [`icd10_coding_swarm.sh`](icd10_coding_swarm.sh) | `POST /v1/swarm/completions` | A three-agent `ConcurrentWorkflow` for clinical coding |

A single-agent request is in
[`../../01_getting_started/hello_agent.sh`](../../01_getting_started/hello_agent.sh).

## Request anatomy

Every call is the same three headers plus a JSON body:

```bash
curl -X POST "${BASE_URL}/v1/swarm/completions" \
  -H "x-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{ "swarm_type": "SequentialWorkflow", "agents": [...], "task": "..." }'
```

`x-api-key` — not `Authorization: Bearer` — is the auth header.

## Tips

- **`batched_grid_workflow.sh` pipes through `jq`.** Install it (`brew install jq`) or
  delete the `| jq '.'` at the end.
- **Add `--max-time`** for swarm types that run long; the default curl timeout will cut
  a heavy swarm off mid-run.
- **Reading the response** is much easier through `jq`: `... | jq '.output'`.
- **Never paste a key into these files.** They read the environment for a reason — a
  key committed to git is a key that needs rotating.
