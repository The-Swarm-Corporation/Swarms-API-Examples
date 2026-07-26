# Single Agent — Vision

Pass an image alongside the task and a vision-capable model will read it.

**Endpoint:** `POST /v1/agent/completions`

## Configuration

| Field | Type | Notes |
|---|---|---|
| `img` | string | The image, as a base64 data URL or raw base64 |
| `agent_config.model_name` | string | Must be a vision-capable model (e.g. `gpt-4.1`) |
| `task` | string | What to do with the image |

## Shape

```python
import base64

with open("img.jpg", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "agent_config": {
        "agent_name": "Vision Assistant",
        "system_prompt": "You describe and analyze images.",
        "model_name": "gpt-4.1",
        "max_loops": 1,
    },
    "task": "Describe what you see in this image.",
    "img": f"data:image/jpeg;base64,{encoded}",
}

requests.post(f"{BASE_URL}/v1/agent/completions", headers=headers, json=payload)
```

## Examples

| File | What it shows |
|---|---|
| [`analyze_image_from_url.py`](analyze_image_from_url.py) | Fetch a remote image, encode it, describe it |
| [`analyze_local_image.py`](analyze_local_image.py) | Read an image from disk (uses [`img.jpg`](img.jpg)) |
| [`analyze_image_sdk.py`](analyze_image_sdk.py) | The same flow through the SDK, with `marketplace_prompt_id` |

[`img.jpg`](img.jpg) is the sample image these examples read. Swap in your own — the
examples take the file next to them.

## Tips

- **Base64 inflates payload size by ~33%.** Large images can hit request limits;
  downscale before encoding when you don't need full resolution.
- **The prefix matters.** Use `data:image/jpeg;base64,...` (or `image/png`) to match
  the actual file type.
- **Ask a specific question.** "Describe this image" gets a generic caption; naming
  what you care about gets a usable answer.
- **`marketplace_prompt_id`** ([`analyze_image_sdk.py`](analyze_image_sdk.py)) reuses a
  published system prompt instead of writing your own.
