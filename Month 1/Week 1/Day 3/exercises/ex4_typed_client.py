"""Exercise 4 — CẦU NỐI: hardened client Day 2 giờ nhận Settings + trả Pydantic model.

Gộp cả ngày: client KHÔNG còn đọc os.environ, KHÔNG còn trả dict thô. Nó:
  - nhận `Settings` (ex3) qua constructor  -> config tập trung
  - build `ChatRequest` (ex2)               -> input đã validate
  - gọi provider (tái dùng httpx.Client + timeout + retry taxonomy của Day 2)
  - validate response provider bằng Pydantic -> ĐÓNG bug Day 2 (HTTP 200 + body lỗi)
  - trả `ChatResponse` có kiểu (Usage + cost) -> không còn dict.get("usage") mù mờ

Bạn TỰ viết phần thân ở chỗ `TODO`. Tái dùng @retry/@timed/@log_usage từ Day 2 nếu muốn.

Acceptance:
- `ProviderClient.__init__` nhận `settings: Settings`; tạo httpx.Client dùng base_url + timeout từ settings.
- `ProviderResponse.model_validate` phân xử body provider: thiếu `usage` HOẶC có `error` -> ValidationError.
- `chat()` trả `ChatResponse` (chứa Usage + cost_usd), KHÔNG trả dict.
- Lỗi validate response -> ném lỗi phân loại được (nối vào taxonomy Transient/Permanent Day 2).
- Không log key thô (Settings dùng SecretStr).
- Type hint đầy đủ; `mypy --strict` sạch; `ruff check` sạch.

GHI CHÚ: import từ ex2/ex3 để tái dùng model + settings (đừng copy-paste định nghĩa).
"""

from __future__ import annotations

import httpx
from pydantic import BaseModel, Field, ValidationError, model_validator

# Tái dùng từ hôm nay (điều chỉnh import nếu bạn để package khác):
from ex2_pydantic_models import ChatRequest, Usage
from ex3_settings import Settings, get_settings

# Giá tham khảo (USD / 1K token) — điền theo price sheet model bạn dùng:
PRICE_PER_1K_INPUT = 0.00015
PRICE_PER_1K_OUTPUT = 0.0006


class ProviderResponse(BaseModel):
    """Hình dạng response THÔ của provider — validate phòng thủ tại biên network.

    Bug Day 2: OpenRouter đôi khi trả HTTP 200 nhưng body là {"error": {...}} và THIẾU usage.
    Cho Pydantic phân xử: nếu có `error` hoặc thiếu `usage` -> ValidationError = tín hiệu rõ ràng.
    """

    id: str | None = None
    error: dict[str, object] | None = None
    usage: Usage | None = None
    # (giản lược: bỏ qua choices/text ở bài này — trọng tâm là usage + error taxonomy)

    @model_validator(mode="after")
    def reject_error_body(self) -> ProviderResponse:
        if self.error is not None:
            raise ValueError(f"provider error body: {self.error}")
        if self.usage is None:
            raise ValueError("response thiếu 'usage'")
        return self


class ChatResponse(BaseModel):
    """Kết quả ĐÃ tin, có kiểu — thứ business logic nhận được."""

    model: str
    usage: Usage
    cost_usd: float = Field(ge=0)


class TransientError(Exception):
    """Lỗi tạm — retry được (429/5xx/network). Nối vào taxonomy Day 2."""


class PermanentError(Exception):
    """Lỗi vĩnh viễn — KHÔNG retry (4xx, hoặc body không hợp lệ)."""


class ProviderClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = httpx.Client(
            base_url=settings.base_url,
            timeout=httpx.Timeout(
                connect=5.0, read=settings.request_timeout_s, write=10.0, pool=5.0
            ),
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key.get_secret_value()}"
            },
        )

    def close(self) -> None:
        self._client.close()

    def _compute_cost(self, usage: Usage) -> float:
        return (usage.prompt_tokens / 1000) * PRICE_PER_1K_INPUT + (
            usage.completion_tokens / 1000
        ) * PRICE_PER_1K_OUTPUT

    def chat(self, req: ChatRequest) -> ChatResponse:
        """Gọi provider, validate response, trả ChatResponse có kiểu.

        Luồng: POST /chat/completions -> classify(status) -> parse body qua ProviderResponse
        -> map sang ChatResponse (usage + cost). Lỗi -> TransientError/PermanentError.
        """
        try:
            resp = self._client.post("/chat/completions", json=req.model_dump())
        except httpx.HTTPError as e:
            raise TransientError(f"lỗi mạng: {e}") from e

        if resp.status_code == 429 or resp.status_code >= 500:
            raise TransientError(f"status tạm thời {resp.status_code}")
        if resp.status_code >= 400:
            raise PermanentError(f"status {resp.status_code}: {resp.text}")

        try:
            pr = ProviderResponse.model_validate(resp.json())
        except ValidationError as e:
            raise PermanentError(f"body không hợp lệ: {e}") from e
        assert pr.usage is not None
        return ChatResponse(
            model=self._settings.model,
            usage=pr.usage,
            cost_usd=self._compute_cost(pr.usage),
        )


def main() -> None:
    settings = get_settings()
    client = ProviderClient(settings)
    try:
        req = ChatRequest(
            model=settings.model,
            messages=[{"role": "user", "content": "Giải thích 'timeout' trong 1 câu."}],  # type: ignore[list-item]
        )
        out = client.chat(req)
        print(out.model_dump_json())
    except (TransientError, PermanentError, ValidationError) as e:
        print("handled:", type(e).__name__, e)
    finally:
        client.close()


if __name__ == "__main__":
    main()
