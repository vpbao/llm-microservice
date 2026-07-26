"""Exercise 1 — Comprehensions (thay array_map / array_filter của PHP).

Mục tiêu: lên phản xạ 4 dạng comprehension và biết KHI NÀO KHÔNG dùng.
Bạn TỰ viết phần thân — chỗ có `TODO` và `raise NotImplementedError`.

Acceptance:
- Không dùng vòng `for ... append(...)` ở 4 hàm đầu — phải là comprehension.
- `count_tokens_total` dùng GENERATOR EXPRESSION (không dựng list trung gian).
- Tất cả có type hint đầy đủ; `mypy --strict` sạch; `ruff check` sạch.
- Chạy `python ex1_comprehensions.py` in ra kết quả mẫu, không lỗi.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable


def clean_lines(lines: Iterable[str]) -> list[str]:
    """(list comp) strip mỗi dòng và LOẠI dòng rỗng.

    PHP: array_filter(array_map('trim', $lines)).
    """
    return [line.strip() for line in lines if line.strip()]


def to_token_map(
    texts: dict[str, str], counter: Callable[[str], int]
) -> dict[str, int]:
    """(dict comp) map {name -> số token} từ {name -> text}."""
    return {name: counter(text) for name, text in texts.items()}


def unique_words(text: str) -> set[str]:
    """(set comp) tập từ duy nhất, chữ thường. Gợi ý: text.lower().split()."""
    return {word for word in text.lower().split()}


def count_tokens_total(texts: Iterable[str], counter: Callable[[str], int]) -> int:
    """(generator expr) tổng token — KHÔNG được dựng list trung gian.

    Gợi ý: sum(counter(t) for t in texts)  ← generator expr nằm trong sum().
    """
    return sum(counter(text) for text in texts)


# --- Câu hỏi nhỏ (trả lời trong Notes.md, không cần code): -------------------
# Q: Khi nào KHÔNG nên dùng comprehension mà quay lại for-loop bình thường?
#    (gợi ý: side-effect / lồng quá sâu / khó đọc trong 1 hơi)


def _fake_counter(s: str) -> int:
    """Đếm token giả (~4 ký tự/token) để chạy demo mà không cần tiktoken."""
    return max(1, len(s) // 4)


if __name__ == "__main__":
    fake_counter: Callable[[str], int] = _fake_counter

    print(clean_lines(["  hi  ", "", "  world"]))  # ['hi', 'world']
    print(to_token_map({"a": "hello", "b": "hi there"}, fake_counter))
    print(sorted(unique_words("the cat the CAT sat")))  # ['cat', 'sat', 'the']
    print(count_tokens_total(["hello", "a longer piece of text"], fake_counter))
