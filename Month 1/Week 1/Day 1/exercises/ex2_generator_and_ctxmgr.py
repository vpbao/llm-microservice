"""Exercise 2 — Generator + Context manager.

(a) Viết generator stream từng dòng của một file (lazy, không đọc hết vào RAM).
(b) Viết context manager `timer()` đo thời gian một block code.

Đây là nền tảng cho STREAMING (tuần 2) và cho việc đo latency (production mindset).

Acceptance:
- `read_lines` là generator (dùng `yield`), có type hint `Iterator[str]`.
- `timer` dùng `@contextmanager`, in ra elapsed ms khi thoát block.
- mypy --strict sạch.
"""

from __future__ import annotations

from collections.abc import Generator, Iterator
from contextlib import contextmanager
from time import perf_counter


def read_lines(path: str) -> Iterator[str]:
    with open(path, encoding='utf-8') as f:
        for line in f:
            yield line.rstrip('\n')

@contextmanager
def timer(label: str) -> Generator[None]:
    t0 = perf_counter()
    yield
    ms =  (perf_counter() - t0) * 1000
    print(f"{label}: {ms:.1f} ms")


if __name__ == "__main__":
    with timer("read file"):
        n = sum(1 for _ in read_lines(__file__))
    print(f"{n} dòng")
