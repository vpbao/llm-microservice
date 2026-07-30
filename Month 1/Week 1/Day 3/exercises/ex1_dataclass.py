"""Exercise 1 — dataclass: struct có kiểu cho dữ liệu ĐÃ TIN (nội bộ).

Mục tiêu: lên phản xạ `@dataclass` và hiểu GIỚI HẠN của nó (không validate runtime),
để sang ex2 bạn thấy rõ vì sao cần Pydantic ở biên.

Bối cảnh PHP/Laravel: đây là DTO / value object bạn tự viết constructor + getter.

Bạn TỰ viết phần thân ở chỗ `TODO` / `raise NotImplementedError`.

Acceptance:
- `Money` là frozen + slots; `as_decimal()` trả amount_cents/100.
- `ChatMessage` dùng `frozen=True` (một message trong lịch sử là bất biến).
- `Conversation.messages` dùng `field(default_factory=list)` — KHÔNG `= []`.
- `__post_init__` của `ChatMessage` assert role thuộc {system,user,assistant}.
- Chứng minh giới hạn: `demo_no_runtime_validation()` cho thấy dataclass KHÔNG ép kiểu.
- Type hint đầy đủ; `mypy --strict` sạch; `ruff check` sạch; chạy in ra không lỗi.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Money:
    amount_cents: int
    currency: str = "USD"

    def as_decimal(self) -> float:
        """Trả về số tiền dạng thập phân (cents/100)."""
        return self.amount_cents / 100


@dataclass(frozen=True, slots=True)
class ChatMessage:
    role: str
    content: str

    def __post_init__(self) -> None:
        if self.role not in {"system", "user", "assistant"}:
            raise ValueError(f"role không hợp lệ: {self.role!r}")


@dataclass(slots=True)
class Conversation:
    model: str
    messages: list[ChatMessage] = field(default_factory=list)

    def add(self, msg: ChatMessage) -> None:
        """Thêm một message vào cuối hội thoại."""
        self.messages.append(msg)

    def last_user_content(self) -> str | None:
        """Nội dung message user gần nhất, hoặc None nếu chưa có."""
        for message in reversed(self.messages):
            if message.role == "user":
                return message.content
        return None


def demo_no_runtime_validation() -> None:
    """CHỨNG MINH giới hạn: dataclass KHÔNG ép kiểu / KHÔNG validate type lúc runtime.

    Type hint `amount_cents: int` chỉ để mypy đọc TĨNH. Lúc chạy, truyền str vẫn 'tạo được'
    object rác — đây chính là lý do ta cần Pydantic ở biên (ex2).
    """
    bad = Money(amount_cents="oops")  # type: ignore[arg-type]
    print("mypy nói int, runtime thực ra là:", type(bad.amount_cents).__name__)
    print("gọi as_decimal() sẽ NỔ ở đây, không phải lúc tạo:", end=" ")
    try:
        bad.as_decimal()  # str / 100 -> TypeError, bắn Ở ĐÂY
    except TypeError as e:
        print("NỔ (muộn):", e)


def main() -> None:
    conv = Conversation(model="openai/gpt-4o-mini")
    conv.add(ChatMessage(role="system", content="Bạn là trợ lý."))
    conv.add(ChatMessage(role="user", content="Xin chào"))
    print("last user:", conv.last_user_content())
    print(
        "price:",
        Money(amount_cents=1999).as_decimal(),
        Money(amount_cents=1999).currency,
    )
    demo_no_runtime_validation()


if __name__ == "__main__":
    main()
