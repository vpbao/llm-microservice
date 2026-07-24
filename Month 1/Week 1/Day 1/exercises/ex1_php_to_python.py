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
from enum import StrEnum


class Currency(StrEnum):
    USD = "USD"
    VND = "VND"


@dataclass(frozen=True)
class Money:
    amount_cents: int
    currency: Currency = Currency.USD

    def add(self, other: Money) -> Money:
        if other.currency != self.currency:
            raise ValueError("Cannot add different currencies.")

        return Money(self.amount_cents + other.amount_cents, self.currency)

    def format(self) -> str:
        return f"${self.amount_cents / 100:.2f}"


if __name__ == "__main__":
    usd = Money(100, Currency.USD)
    other_usd = Money(200, Currency.USD)

    print(usd.add(other_usd).format())

    vnd = Money(50000, Currency.VND)
    print(vnd.format())  # $500.00 (format chưa phân biệt ký hiệu tiền tệ)

    # thử nhánh raise: cộng USD với VND -> ValueError
    try:
        usd.add(vnd)
    except ValueError as e:
        print(f"raised: {e}")  # raised: Cannot add different currencies.
