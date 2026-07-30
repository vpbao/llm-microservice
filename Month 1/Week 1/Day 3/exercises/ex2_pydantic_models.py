"""Exercise 2 — Pydantic v2: validate + ép kiểu + serialize tại BIÊN.

Đây là nơi dữ liệu KHÔNG tin được (HTTP body của user) bị chặn tại cửa. Laravel: FormRequest
(rules) + API Resource (serialize) gộp làm một. Bạn sẽ TÁI DÙNG các model này ở ex4.

Bạn TỰ viết phần thân ở chỗ `TODO`.

Acceptance (dùng API Pydantic v2, KHÔNG v1):
- `ChatMessage`: role khớp regex ^(system|user|assistant)$; content min_length=1, max_length=8000.
- `ChatRequest`: messages min_length=1; temperature default 0.7, ràng buộc 0.0..2.0.
- `@field_validator("messages")`: message CUỐI phải có role == "user" (nếu không -> ValueError).
- `@model_validator(mode="after")`: nếu stream=True thì n phải == 1.
- `model_config = ConfigDict(extra="forbid")` cho ChatRequest (từ chối field lạ ở biên user).
- `parse_untrusted()`: dùng `model_validate` trên dict "bẩn" (temperature là "0.5" -> ép về float).
- `demo_validation_error()`: bắt `ValidationError` và in ra (chứng minh lỗi nổ TẠI cửa).
- Type hint đầy đủ; `mypy --strict` sạch; `ruff check` sạch.
"""

from __future__ import annotations

from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)


class ChatMessage(BaseModel):
    role: str = Field(pattern=r"^(system|user|assistant)$")
    content: str = Field(min_length=1, max_length=8000)


class ChatRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )  # field lạ ở biên user -> lỗi, không im lặng

    model: str
    messages: list[ChatMessage] = Field(min_length=1)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    stream: bool = False
    n: int = Field(default=1, ge=1, le=8)

    @field_validator("messages")
    @classmethod
    def last_must_be_user(cls, v: list[ChatMessage]) -> list[ChatMessage]:
        if v[-1].role != "user":
            raise ValueError("message cuối phải là user")
        return v

    @model_validator(mode="after")
    def stream_implies_single(self) -> ChatRequest:
        if self.stream and self.n != 1:
            raise ValueError("stream=True cần n=1")
        return self


class Usage(BaseModel):
    """Số token do provider trả — sẽ dùng lại ở ex4 để tính cost."""

    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


def parse_untrusted(raw: dict[str, Any]) -> ChatRequest:
    """Parse một dict 'bẩn' từ ngoài (vd JSON body). Ép kiểu + validate tại đây.

    Ví dụ raw có temperature là chuỗi "0.5" -> Pydantic ép về 0.5 (float).
    """
    return ChatRequest.model_validate(raw)


def demo_validation_error() -> None:
    """Chứng minh: dữ liệu sai bị chặn TẠI cửa với ValidationError gom mọi lỗi một lần."""
    bad = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": ""}],  # content rỗng -> lỗi
        "temperature": 5,  # ngoài [0,2] -> lỗi
        "typo_field": 1,  # extra="forbid" -> lỗi
    }
    try:
        ChatRequest.model_validate(bad)
    except ValidationError as e:
        print(e)  # xem nó liệt kê CẢ 3 lỗi


def main() -> None:
    raw = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": "Xin chào"}],
        "temperature": "0.5",  # chuỗi -> sẽ bị ép về float
    }
    req = parse_untrusted(raw)
    print("parsed:", req.model_dump_json())
    print("temperature type:", type(req.temperature).__name__)  # -> float
    demo_validation_error()


if __name__ == "__main__":
    main()
