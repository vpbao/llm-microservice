"""Exercise 4 — Gọi Chat Completions bằng raw httpx, rồi bằng SDK, so sánh.

Mục tiêu: thấy SDK che giấu cái gì (auth header, endpoint, JSON shape, usage).
KEY để trong biến môi trường (OPENAI_API_KEY / ANTHROPIC_API_KEY) — KHÔNG hardcode.

Bước:
1. `uv add httpx openai anthropic`
2. Hàm `via_httpx(prompt)`: tự dựng POST tới endpoint, tự set header Authorization,
   tự parse JSON -> text + usage (prompt_tokens, completion_tokens).
3. Hàm `via_sdk(prompt)`: dùng SDK chính thức, lấy .usage.
4. In cả hai output + token usage cạnh nhau.

Ghi chú: hôm nay dùng client ĐỒNG BỘ cũng được để học; tuần 2 ta chuyển sang async.

Acceptance:
- Chạy được, in ra text + input/output tokens từ cả 2 cách.
- Không có key nào nằm trong code.
"""

from __future__ import annotations

import os

import httpx
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # đọc file .env vào biến môi trường

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
PROMPT = "Giải thích 'token' trong LLM bằng đúng 1 câu."


def via_httpx(prompt: str) -> tuple[str, dict[str, int]]:
    """Gọi 'trần' — tự dựng URL, header, body, tự bóc JSON."""
    api_key = os.environ["OPENROUTER_API_KEY"]
    resp = httpx.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )
    if resp.status_code != 200:
        print(f"[debug] status={resp.status_code}")
        print(f"[debug] body={resp.text}")
    resp.raise_for_status()
    data = resp.json()
    text = data["choices"][0]["message"]["content"]
    usage = data["usage"]
    return text, {
        "input": usage["prompt_tokens"],
        "output": usage["completion_tokens"],
    }


def via_sdk(prompt: str) -> tuple[str, dict[str, int]]:
    """Cùng việc đó, nhưng SDK lo header/endpoint/parse hộ."""
    client = OpenAI(api_key=os.environ["OPENROUTER_API_KEY"], base_url=BASE_URL)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.choices[0].message.content or ""
    usage = resp.usage
    assert usage is not None
    return text, {"input": usage.prompt_tokens, "output": usage.completion_tokens}


if __name__ == "__main__":
    for name, fn in [("httpx", via_httpx), ("sdk", via_sdk)]:
        text, tokens = fn(PROMPT)
        print(f"\n=== via {name} ===")
        print(text)
        print(f"tokens: input={tokens['input']} output={tokens['output']}")
