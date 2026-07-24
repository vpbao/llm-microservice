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

# TODO: import httpx và SDK tương ứng


def via_httpx(prompt: str) -> tuple[str, dict[str, int]]:
    api_key = os.environ["OPENAI_API_KEY"]  # đọc từ env
    # TODO: POST https://api.openai.com/v1/chat/completions
    #   headers={"Authorization": f"Bearer {api_key}"}
    #   json={"model": ..., "messages": [{"role":"user","content":prompt}]}
    # parse: choices[0].message.content, usage
    raise NotImplementedError


def via_sdk(prompt: str) -> tuple[str, dict[str, int]]:
    # TODO: client = OpenAI(); resp = client.chat.completions.create(...)
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: gọi cả hai với cùng prompt và in so sánh
    ...
