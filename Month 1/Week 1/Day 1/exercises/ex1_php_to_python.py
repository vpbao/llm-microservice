"""Exercise 1 — Chuyển một class PHP/Laravel bạn biết sang Python typed idiomatic.

Mục tiêu: dùng @dataclass + method, type hint đầy đủ. Chạy `mypy --strict` phải SẠCH.

Gợi ý: chọn một value object đơn giản bạn từng viết (vd Money, Money+Currency,
hoặc một Eloquent-ish "UserProfile"). KHÔNG dùng `Any`.

Acceptance:
- `uv run mypy --strict exercises/ex1_php_to_python.py`  -> Success
- `uv run ruff check exercises/ex1_php_to_python.py`      -> no errors
"""

from __future__ import annotations

from dataclasses import dataclass


# TODO: thay ví dụ mẫu dưới bằng class PHP của bạn, chuyển sang Python typed.
@dataclass(frozen=True)
class Money:
    amount_cents: int
    currency: str = "USD"

    def add(self, other: Money) -> Money:
        # TODO: raise nếu khác currency; trả về Money mới
        raise NotImplementedError

    def format(self) -> str:
        # TODO: trả về ví dụ "$12.34"
        raise NotImplementedError


if __name__ == "__main__":
    # TODO: in vài ví dụ để tự kiểm tra
    ...
