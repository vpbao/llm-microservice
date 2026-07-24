# Notes — Day 1

## 5 khác biệt PHP/Laravel → Python (tự viết bằng lời của bạn)
1. Khác naming convention (snake_case); **type hints không enforce lúc chạy** — `mypy --strict` mới là thứ bắt lỗi (như PHPStan), interpreter không ép kiểu.
2. Python **có** `None`, nhưng phải khai báo nullable **tường minh** (`str | None`) và mypy **bắt buộc** xử lý nhánh None (PHP `?string` lỏng hơn).
3. Không có `new`, không có `$this`; constructor là `__init__(self, ...)` và `self` phải viết tay ở tham số đầu mọi method.
4. Không autoload PSR-4 — import tường minh; package định nghĩa bằng `pyproject.toml`, không phải `composer.json`.
5. Duck typing / `Protocol` (structural) thay cho `interface` bắt buộc (nominal) của PHP.

---

## 8-question test — "TOKEN"
> Chưa trả lời được cả 8 câu = chưa học xong khái niệm.

1. **Vì sao cần nó?** Model không xử lý được ký tự/từ thô — nó chỉ làm việc trên các số (token ID). Token là đơn vị đầu vào của model.
2. **Giải quyết vấn đề gì?** Biến văn bản bất kỳ (mọi ngôn ngữ) thành một dãy số ID nằm trong một **bộ từ vựng cố định** để model xử lý đồng nhất.
3. **Hoạt động bên trong ra sao?** Tokenizer dùng **BPE** — gộp các cặp ký tự/byte hay đi cùng nhau thành subword. Vì thế từ tiếng Anh phổ biến → ít token; chữ có dấu tiếng Việt (nhiều byte UTF-8, hiếm gặp) bị tách nhỏ → nhiều token.
4. **Khi nào dùng?** Khi cần ước lượng/tính **cost và latency**, và khi kiểm soát độ dài để vừa context window.
5. **Khi nào KHÔNG?** Khi chỉ cần đếm ký tự cho hiển thị/UI — không liên quan model.
6. **Câu hỏi phỏng vấn thường gặp?** Token là gì? Vì sao token (không phải ký tự) chi phối cost & latency? Tiếng Anh vs tiếng Việt chi phí có khác không?
7. **Lỗi người mới hay mắc?** Tưởng 1 từ = 1 token; tưởng đếm ký tự là đủ để tính tiền.
8. **Dùng trong production thế nào?** Log token mỗi request để tính cost, đặt budget/limit, và ước lượng latency. (Ta seed điều này từ ngày 1.)

---

## 8-question test — "CONTEXT WINDOW"
1. **Vì sao cần nó?** Context window **KHÔNG phải bộ nhớ**. Nó là **giới hạn tối đa số token model xử lý trong MỘT lần gọi** (input + output). Cần nắm vì kiến trúc model có trần cố định.
2. **Giải quyết vấn đề gì?** Nó không "ghi nhớ" gì cả. **Model stateless** — không tự nhớ lần trước. Chat "nhớ" là do **client gửi lại toàn bộ lịch sử mỗi lượt**, và toàn bộ lịch sử đó phải **nhét vừa** trong context window.
3. **Hoạt động bên trong ra sao?** Tổng token = input (system + history + prompt) + output. Vượt trần → lỗi hoặc bị **truncate** (cắt bớt phần cũ).
4. **Khi nào dùng?** Là **ràng buộc ở MỌI lần gọi**, không phải "lúc bắt đầu session". Luôn phải tính: lịch sử + tài liệu + câu trả lời có vừa trần không.
5. **Khi nào KHÔNG (phải lo)?** Khi nội dung ngắn, còn xa giới hạn — chưa cần cắt bớt/summarize/RAG.
6. **Câu hỏi phỏng vấn thường gặp?** Context window là gì? Chuyện gì xảy ra khi vượt quá? Vì sao LLM stateless mà chat vẫn "nhớ"?
7. **Lỗi người mới hay mắc?** Tưởng context window là "bộ nhớ" của model; không quan tâm giới hạn nên bị truncate mất thông tin; gửi cả tài liệu khổng lồ mỗi lượt → cháy token.
8. **Dùng trong production thế nào?** Quản lý cửa sổ chủ động: cắt/summarize lịch sử, chỉ đưa phần liên quan (nền của **RAG**), và theo dõi token để không vượt trần + không phí tiền.

> **Câu vàng để nhớ:** LLM stateless → chat "nhớ" là do client resend history → history đó bị chặn bởi context window (trần token/lần gọi) → vượt thì lỗi hoặc truncate.

---

## Sampling — temperature / top-p & vì sao temp=0 vẫn không deterministic tuyệt đối
- **temperature**: làm phân phối xác suất "phẳng" (cao → sáng tạo/ngẫu nhiên) hay "nhọn" (thấp → an toàn). `temp=0` ≈ **argmax/greedy** (luôn chọn token xác suất cao nhất) → dùng khi cần ổn định (trích JSON, phân loại).
- **top-p (nucleus)**: chỉ lấy mẫu trong nhóm token nhỏ nhất có tổng xác suất ≥ p.

**Vì sao temp=0 vẫn KHÔNG deterministic 100%:** temp=0 chỉ bỏ ngẫu nhiên do *sampling*, không bỏ được ngẫu nhiên do *tính toán*:
1. **Floating-point non-associative:** GPU cộng song song theo thứ tự không cố định (parallel reduction) → logits lệch ở chữ số cuối.
2. **Batching động phía server:** request được gom vào batch với kích thước/thành phần thay đổi mỗi lần → kernel khác → lại lệch floating-point.
3. **Near-tie:** khi 2 token top xác suất sát nhau, một dao động cực nhỏ đủ để argmax lật token → cả câu đi hướng khác.
4. **MoE routing + GPU ops không xác định (atomic add) + khác kernel/phần cứng.**

**Production:** một số API có `seed` + `system_fingerprint` (best-effort, không đảm bảo tuyệt đối). ⇒ Không bao giờ giả định output LLM bit-for-bit giống nhau; test bằng **kiểm tra ngữ nghĩa/schema** (JSON hợp lệ, đúng enum), không so sánh chuỗi tuyệt đối.

---

## Số liệu tiktoken (điền từ Exercise 3, encoding cl100k_base)
| Text | Chars | Tokens | chars/token |
|---|---|---|---|
| Hello world | 11 | 2 | 5.50 |
| Tokenization splits text into subword units. | 44 | 9 | 4.89 |
| Xin chào, đây là một câu tiếng Việt... | 56 | 28 | 2.00 |
| def add(a: int, b: int) -> int: ... | 48 | 18 | 2.67 |

**Kết luận:** tiếng Việt ~2.00 chars/token, chỉ bằng ~40% tiếng Anh (~4.9) → cùng một lượng nội dung, tiếng Việt tốn **gấp ~2.5× token** → cost cao hơn, context window đầy nhanh hơn, latency lớn hơn. Đây là "bẫy cháy túi" của RAG tiếng Việt.

## Kiểm chứng cost bằng tay
- Giá ví dụ: input **$0.15 / 1M** token, output **$0.60 / 1M** token.
- Request giả định: 1200 input + 400 output token.
- Phép tính: `(1200/1e6)*0.15 + (400/1e6)*0.60 = 0.00018 + 0.00024 = $0.00042`.
- Ghi nhớ: **output thường đắt hơn input** (ở đây gấp 4× đơn giá).
