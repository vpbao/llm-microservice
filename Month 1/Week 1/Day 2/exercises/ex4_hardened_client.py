"""Exercise 4 — Làm cứng lời gọi httpx của Day 1.

Lấy `via_httpx` của Day 1 và thêm 4 lớp production:
  (1) TIMEOUT tường minh (connect ngắn, read dài cho LLM).
  (2) RETRY + exponential backoff + jitter — CHỈ cho lỗi tạm thời.
  (3) ERROR TAXONOMY — phân loại lỗi retry được vs không (xem bảng trong Notes.md).
  (4) USAGE LOG — model, input/output tokens, cost, latency_ms, status, attempts.

KEY để trong biến môi trường (OPENROUTER_API_KEY) — KHÔNG hardcode.
Bạn TỰ viết phần thân ở chỗ `TODO`. Có thể tái dùng @retry từ ex2 nếu muốn.

Acceptance:
- Có `httpx.Timeout` tường minh (KHÔNG để mặc định vô hạn).
- Dùng MỘT `httpx.Client` tái dùng (context manager `with`).
- Phân loại: 429 + 5xx + lỗi mạng -> retry; 4xx khác -> raise ngay (PermanentError).
- Tôn trọng header `Retry-After` khi gặp 429 (nếu có).
- Trả về `CallResult` có text + usage + latency_ms + attempts; in một dòng usage log.
- mypy --strict sạch.
"""

from __future__ import annotations

import os
import random
import time
from dataclasses import dataclass

import httpx
from dotenv import load_dotenv

# TODO(ex4): khi làm backoff+jitter, thêm `import random` và dùng random.uniform(...)

load_dotenv()

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

# Giá ví dụ (USD / 1M token) — chỉnh theo bảng giá model thật khi tính cost.
PRICE_INPUT_PER_M = 0.15
PRICE_OUTPUT_PER_M = 0.60

# Lỗi tạm thời (retry được) vs vĩnh viễn (không retry).
RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})


class PermanentError(RuntimeError):
    """Lỗi KHÔNG nên retry (4xx trừ 429): sai prompt/schema/key/endpoint."""


class TransientError(RuntimeError):
    """Lỗi tạm thời (429/5xx/mạng): nên retry với backoff."""


@dataclass(slots=True)
class CallResult:
    text: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    attempts: int

    @property
    def cost_usd(self) -> float:
        return (self.input_tokens / 1e6) * PRICE_INPUT_PER_M + (
            self.output_tokens / 1e6
        ) * PRICE_OUTPUT_PER_M


def _classify(resp: httpx.Response) -> None:
    """Ném TransientError / PermanentError dựa trên status. 2xx -> return bình thường."""
    if resp.is_success:
        return
    if resp.status_code in RETRYABLE_STATUS:
        raise TransientError(f"transient {resp.status_code}")
    raise PermanentError(f"permanent {resp.status_code}")


def call_hardened(
    prompt: str, *, max_attempts: int = 3, base_delay: float = 0.5
) -> CallResult:
    """Gọi chat completion đã làm cứng. Tự retry lỗi tạm thời, không retry lỗi vĩnh viễn."""
    api_key = os.environ["OPENROUTER_API_KEY"]
    timeout = httpx.Timeout(connect=5.0, read=60.0, write=10.0, pool=5.0)

    t0 = time.perf_counter()
    last_exc: Exception | None = None

    with httpx.Client(base_url=BASE_URL, timeout=timeout) as client:
        for attempt in range(max_attempts):
            try:
                resp = client.post(
                    "/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                )
                _classify(resp)  # raise nếu lỗi
                data = resp.json()
                print("[debug] status:", resp.status_code)  # tạm
                print("[debug] data:", data)  # tạm
                usage = data["usage"]
                latency_ms = (time.perf_counter() - t0) * 1000
                result = CallResult(
                    text=data["choices"][0]["message"]["content"],
                    input_tokens=usage["prompt_tokens"],
                    output_tokens=usage["completion_tokens"],
                    latency_ms=latency_ms,
                    attempts=attempt + 1,
                )
                _log_usage(result, status="ok")
                return result

            except (httpx.TransportError, TransientError) as e:
                last_exc = e
                if attempt == max_attempts - 1:
                    break
                backoff = base_delay * 2**attempt + random.uniform(0, base_delay)
                time.sleep(backoff)

            except PermanentError:
                _log_usage(None, status="permanent_error")
                raise

    _log_usage(None, status="exhausted")
    raise TransientError(f"hết {max_attempts} lượt thử") from last_exc


def _log_usage(result: CallResult | None, *, status: str) -> None:
    """In MỘT dòng log có cấu trúc (seed cho observability tuần 3 / Month 6)."""
    if result is None:
        print(f"usage status={status}")
        return
    print(
        f"Model: {MODEL} - Input tokens: {result.input_tokens} - Output tokens: {result.output_tokens} - Cost_USD: {result.cost_usd:.6f} - Latency_MS: {result.latency_ms:.0f} - Attempts: {result.attempts} - Status: {status}"
    )


if __name__ == "__main__":
    r = call_hardened("Giải thích 'timeout' trong 1 câu.")
    print(r.text)
    print(f"cost=${r.cost_usd:.6f} latency={r.latency_ms:.0f}ms attempts={r.attempts}")
