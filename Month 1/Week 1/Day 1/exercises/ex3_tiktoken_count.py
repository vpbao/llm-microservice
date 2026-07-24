"""Exercise 3 — Đếm token bằng tiktoken + kiểm chứng cost bằng tay.

Mục tiêu: cảm nhận trực giác "token != ký tự" và cost = f(tokens).

Bước:
1. `uv add tiktoken`
2. Encode 5 đoạn text mẫu (ngắn/dài, tiếng Anh/tiếng Việt/code) và in số token.
3. So sánh len(chars) vs n_tokens -> tính chars/token cho mỗi mẫu.
4. Lấy giá 1 model (vd từ price sheet OpenAI/Anthropic) và TỰ TAY tính cost cho
   một request giả định (vd 1200 input + 400 output tokens). Ghi kết quả vào Notes.md.

Acceptance:
- In bảng: text | chars | tokens | chars/token
- Có một assert kiểm tra: tiếng Anh ~ 3.5-4.5 chars/token (chỉ để tự thấy quy luật).
"""

from __future__ import annotations

import tiktoken

SAMPLES: list[str] = [
    "Hello world",
    "Tokenization splits text into subword units.",
    "Xin chào, đây là một câu tiếng Việt để so sánh số token.",
    "def add(a: int, b: int) -> int:\n    return a + b",
]

_ENC = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    return len(_ENC.encode(text))


def cost_usd(
    input_tokens: int, output_tokens: int, in_price: float, out_price: float
) -> float:
    return (input_tokens / 1e6) * in_price + (output_tokens / 1e6) * out_price


if __name__ == "__main__":
    print(f"{'chars':>6} {'tokens':>6} {'chars/tokens':>6} {'text'}")
    for s in SAMPLES:
        chars = len(s)
        tokens = count_tokens(s)
        ratio = chars / tokens
        print(f"{chars:>6} {tokens:>6} {ratio:>6.2f}  {s[:40]!r}")

    c = cost_usd(1200, 400, 0.15, 0.60)
    print(f"\nRequest: ${c:.6f}")
