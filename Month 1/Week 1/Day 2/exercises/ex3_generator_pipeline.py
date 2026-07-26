"""Exercise 3 — Generator pipeline (lazy) + mô phỏng stream token.

Ý tưởng: dữ liệu chảy qua nhiều generator nối nhau, mỗi phần tử xử lý tới đâu tiêu thụ tới đó
(không dựng list khổng lồ). Đây CHÍNH LÀ mô hình streaming LLM của tuần 2.

Pipeline:  read_lines → clean → chunk_words(n) → (tiêu thụ)

Bạn TỰ viết phần thân ở chỗ `TODO`.

Acceptance:
- Cả 3 hàm là GENERATOR (dùng `yield` / `yield from`), trả `Iterator[...]`.
- Không hàm nào gọi `list(...)` bên trong (giữ lazy).
- `stream_tokens` mô phỏng LLM đẩy từng token kèm delay nhỏ.
- mypy --strict sạch.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from time import sleep

# TODO(ex3): khi làm `stream_tokens` với delay>0, thêm `import time` và dùng time.sleep(delay)


def read_lines(text: str) -> Iterator[str]:
    """Yield từng dòng của một chuỗi nhiều dòng (mô phỏng đọc file lazy)."""
    yield from text.splitlines()


def clean(lines: Iterable[str]) -> Iterator[str]:
    """Yield mỗi dòng đã strip, BỎ QUA dòng rỗng. Giữ lazy (không dựng list)."""
    for line in lines:
        if line.strip():
            yield line.strip()


def chunk_words(lines: Iterable[str], n: int) -> Iterator[list[str]]:
    """Gộp toàn bộ từ trên các dòng, yield từng khối n từ.

    Ví dụ n=2, "a b c" -> ['a','b'], ['c'].
    Gợi ý: gom buffer, yield khi đủ n; cuối cùng yield phần dư nếu có.
    """
    buffer: list[str] = []
    for line in lines:
        for word in line.split():
            buffer.append(word)
            if len(buffer) == n:
                yield buffer
                buffer = []
        if buffer:
            yield buffer


def stream_tokens(chunks: Iterable[list[str]], delay: float = 0.0) -> Iterator[str]:
    """Mô phỏng LLM stream: yield từng token (từ), có thể sleep(delay) giữa các token.

    Đây là hình mẫu cho endpoint SSE ở tuần 2: nhận chunk -> yield ra ngoài NGAY.
    """
    # TODO: for chunk in chunks: for tok in chunk: (sleep nếu delay>0); yield tok
    for chunk in chunks:
        for token in chunk:
            yield token
            if delay:
                sleep(delay)


# --- Câu hỏi nhỏ (trả lời trong Notes.md): ----------------------------------
# Q1: Vì sao pipeline generator tiết kiệm RAM hơn là làm từng bước bằng list?
# Q2: Nếu clean() raise lỗi ở dòng thứ 100, lỗi bắn ra lúc TẠO generator hay lúc TIÊU THỤ?


if __name__ == "__main__":
    doc = "  the quick brown  \n\n fox jumps over \n the lazy dog  "
    pipeline = stream_tokens(chunk_words(clean(read_lines(doc)), n=3))
    got = list(pipeline)  # chỉ ở main ta mới "materialize" để in
    print(got)  # ['the','quick','brown','fox','jumps','over','the','lazy','dog']
    print("num tokens:", len(got))
