# Python SDK

```bash
pip install swarms-client
```

`SwarmsClient` handles auth headers, retries, timeouts, and response parsing. Prefer it
for application code — the raw-HTTP examples elsewhere in this repo exist to show the
wire format, not because HTTP is the better way to call the API.

## Setup

```python
import os
from swarms_client import SwarmsClient

client = SwarmsClient(
    api_key=os.getenv("SWARMS_API_KEY"),
    base_url=os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world"),
    timeout=300,
)
```

## Methods

| Call | Equivalent endpoint |
|---|---|
| `client.agent.run(agent_config=..., task=...)` | `POST /v1/agent/completions` |
| `client.swarms.run(name=..., swarm_type=..., agents=[...], task=...)` | `POST /v1/swarm/completions` |
| `client.models.list_available()` | `GET /v1/models/available` |

The `agent_config` and `agents` values are the same dicts you would send over HTTP, so
examples translate between the two forms directly.

## Examples

| File | What it shows |
|---|---|
| [`run_swarm_with_sdk.py`](run_swarm_with_sdk.py) | Running a swarm through `SwarmsClient` |

Other SDK examples across the repo:

| File | What it shows |
|---|---|
| [`../../01_getting_started/hello_agent_sdk.py`](../../01_getting_started/hello_agent_sdk.py) | The minimal agent call |
| [`../../02_single_agent/models/claude_opus_5.py`](../../02_single_agent/models/claude_opus_5.py) | Frontier model with `reasoning_effort` |
| [`../../02_single_agent/vision/analyze_image_sdk.py`](../../02_single_agent/vision/analyze_image_sdk.py) | Image input plus a marketplace prompt |
| [`../../06_platform_utilities/list_models.py`](../../06_platform_utilities/list_models.py) | Listing available models |

## SDK vs. raw HTTP

| Use the SDK when | Use raw HTTP when |
|---|---|
| Writing application code | Learning the request shape |
| You want retries and timeouts handled | Debugging what's actually on the wire |
| Python | Any other language, or shell |

Side-by-side comparison: [`../../02_single_agent/models/claude_opus_4_8.py`](../../02_single_agent/models/claude_opus_4_8.py)
(SDK) and [`../../02_single_agent/models/claude_opus_4_8_httpx.py`](../../02_single_agent/models/claude_opus_4_8_httpx.py)
(raw) send the same request.

## Tips

- **Raise `timeout` for swarms.** The default is tuned for single agents; heavy swarms
  and large graphs run for minutes.
- **`base_url` is optional** — omit it unless you're pointing at a non-production
  deployment.
