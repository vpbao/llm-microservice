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

SAMPLES: list[str] = [
    "Hello world",
    "Tokenization splits text into subword units.",
    "Xin chào, đây là một câu tiếng Việt để so sánh số token.",
    "def add(a: int, b: int) -> int:\n    return a + b",
    # TODO: thêm 1 đoạn dài (~1 đoạn văn)
]


def count_tokens(text: str) -> int:
    # TODO: dùng tiktoken encode và trả về len
    raise NotImplementedError


def cost_usd(input_tokens: int, output_tokens: int,
             in_price_per_m: float, out_price_per_m: float) -> float:
    # TODO: return (input_tokens/1e6)*in_price + (output_tokens/1e6)*out_price
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: in bảng cho SAMPLES, rồi in cost cho một request giả định
    ...
