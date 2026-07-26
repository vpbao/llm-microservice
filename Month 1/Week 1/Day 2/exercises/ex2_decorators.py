"""Exercise 2 — Decorators: @timed, @retry(...), @log_usage.

Đây là nơi "cross-cutting concern" (đo giờ, thử lại, log cost) tách khỏi logic nghiệp vụ —
giống attributes/middleware của Laravel. Bạn sẽ TÁI DÙNG chính các decorator này ở ex4.

Bạn TỰ viết phần thân ở chỗ `TODO`.

Acceptance:
- Cả 3 decorator dùng `functools.wraps` (kiểm: `noisy.__name__ == "noisy"`).
- `retry` là decorator CÓ THAM SỐ (retry(max_attempts=3, base_delay=0.01)).
- `retry` chỉ thử lại các exception trong `retry_on`; hết lượt thì raise lỗi cuối.
- `retry` dùng exponential backoff: chờ base_delay * 2**attempt (có thể thêm jitter).
- Type hint đầy đủ; mypy --strict sạch.
"""

from __future__ import annotations

import functools
import random
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

# TODO(ex2): khi làm backoff+jitter trong `retry`, thêm `import random` và dùng random.uniform(...)

P = ParamSpec("P")
R = TypeVar("R")


def timed(fn: Callable[P, R]) -> Callable[P, R]:
    """In ra '<tên hàm>: X ms' kể cả khi hàm raise (dùng try/finally)."""

    @functools.wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        t0 = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            _ms = (time.perf_counter() - t0) * 1000
            print(f"{fn.__name__}: {_ms:.1f} ms")

    return wrapper


def retry(
    max_attempts: int = 3,
    base_delay: float = 0.01,
    retry_on: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator CÓ THAM SỐ → trả về một decorator.

    - Thử tối đa max_attempts lần.
    - Chỉ retry khi exception thuộc `retry_on`; lỗi khác raise ngay.
    - Backoff: sleep(base_delay * 2**attempt) + jitter nhỏ, trừ lần cuối.
    - Hết lượt: raise exception cuối cùng.
    """

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # TODO: vòng for attempt in range(max_attempts):
            #   try: return fn(...)
            #   except retry_on as e: nếu là lần cuối -> raise; else sleep backoff+jitter
            for attempt in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except retry_on:
                    if attempt == max_attempts - 1:
                        raise
                    delay = base_delay * 2**attempt + random.uniform(0, base_delay)
                    time.sleep(delay)

            raise RuntimeError("unreachable: retry loop không return/raise")

        return wrapper

    return decorator


def log_usage(fn: Callable[P, R]) -> Callable[P, R]:
    """In một dòng log sau khi gọi: tên hàm + trạng thái (ok/err).

    (Ở ex4 bạn sẽ mở rộng để log input/output tokens + cost + latency.)
    """

    @functools.wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            result = fn(*args, **kwargs)
            print(f"usage fn={fn.__name__} status=ok")
            return result
        except Exception:
            print(f"usage fn={fn.__name__} status=err")
            raise

    return wrapper


if __name__ == "__main__":
    attempts = {"n": 0}

    @log_usage
    @retry(max_attempts=3, base_delay=0.01, retry_on=(ValueError,))
    @timed
    def noisy(x: int) -> int:
        """Fail 2 lần đầu rồi thành công — để thấy retry hoạt động."""
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise ValueError("transient boom")
        return x * 2

    print("result =", noisy(21))  # kỳ vọng 42 sau 3 lần thử
    print("wraps ok:", noisy.__name__ == "noisy")
