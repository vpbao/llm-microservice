# Lesson — Day 1

> Bạn đã là backend dev ~5 năm (PHP/Laravel). Bài này KHÔNG dạy lập trình. Nó dạy
> (1) *Python idioms & typing* — cái khác so với PHP, và (2) *LLM mental model* —
> nền tảng để mọi thứ RAG/agent về sau không còn là ma thuật.

---

## PHẦN 1 — Modern Python typing cho AI engineer

### 1.1. Type hints: PHP → Python

Python type hints là **gradual typing** — giống PHP 7+/8 typed properties, nhưng runtime
KHÔNG ép kiểu. `mypy` (static checker) mới là thứ bắt lỗi, không phải interpreter.

| Ý niệm | PHP / Laravel | Python (3.10+) |
|---|---|---|
| Mảng danh sách | `string[]` (docblock) / `array` | `list[str]` |
| Map | `array<string,int>` | `dict[str, int]` |
| Nullable | `?string` | `str \| None` (hoặc `Optional[str]`) |
| Union | `int\|string` (PHP 8) | `int \| str` |
| Không kiểu | `mixed` | `Any` (tránh dùng — nó tắt mypy) |
| DTO/value object | class + typed props | `@dataclass` hoặc `pydantic.BaseModel` |
| Interface | `interface` | `typing.Protocol` (structural) hoặc ABC |
| Enum | `enum Foo: string` | `enum.Enum` / `StrEnum` |

**5 khác biệt cốt lõi cần ghi vào `Notes.md`:**
1. **Type hints là tuỳ chọn & không enforce lúc chạy.** `mypy --strict` là "compiler" của bạn. Bật nó trong pre-commit ngay từ ngày 1.
2. **`None` không phải `null` ngầm.** Bạn phải khai báo `str | None` rõ ràng; mypy sẽ ép bạn xử lý nhánh `None` (giống `??` nhưng bị kiểm tra tĩnh).
3. **Không có `new`, không có `$this`.** Constructor là `__init__(self, ...)`; `self` phải viết tay ở tham số đầu.
4. **Duck typing / Protocol thay cho interface bắt buộc.** `Protocol` = "nếu nó có method này thì hợp lệ" — structural typing, khác `implements` của PHP (nominal).
5. **Không autoload theo PSR-4.** Import tường minh (`from app.services import x`); package định nghĩa bằng `pyproject.toml`, không phải `composer.json`.

### 1.2. Dataclass vs Pydantic — khi nào dùng gì
- `@dataclass`: value object thuần, nội bộ, không cần validate input ngoài. Nhẹ, stdlib.
- `pydantic.BaseModel`: khi dữ liệu đến từ **ngoài** (HTTP body, LLM output, config). Nó
  *validate + parse + serialize*. Đây là **lingua franca của code AI** — request/response,
  structured output, tool schema, settings đều là Pydantic. (Laravel: `FormRequest` ≈ Pydantic model.)

### 1.3. Idioms sẽ dùng hàng ngày
- **Comprehension:** `[t.strip() for t in lines if t]` — thay `array_map`/`array_filter`.
- **Generator:** `def read(f): yield from f` — lazy, tiết kiệm RAM, nền tảng của **streaming** (tuần 2 dùng để stream token).
- **Context manager:** `with open(...) as f:` — như `try/finally` tự động. Tự viết bằng `contextlib.contextmanager` hoặc class có `__enter__/__exit__`. Dùng để đo thời gian, quản lý client HTTP.
- **Decorator:** `@lru_cache`, `@app.get(...)` — như PHP attributes/middleware.
- **f-string:** `f"cost={cost:.4f}"`.

### 1.4. Tooling (thay Composer/PHPCS/PHPStan)
| Việc | Laravel stack | Python stack |
|---|---|---|
| Package manager | Composer | **uv** (Astral — nhanh, thay pip/venv/poetry) |
| Linter/format | PHP-CS-Fixer / Pint | **ruff** (lint + format, cực nhanh) |
| Static analysis | PHPStan / Psalm | **mypy** (`--strict`) |
| Test | PHPUnit / Pest | **pytest** |
| Git hooks | husky/GrumPHP | **pre-commit** |
| Manifest | `composer.json` | `pyproject.toml` |

Nguyên tắc production ngay hôm nay: **pin dependencies, bật ruff + mypy trong pre-commit,
API key để trong env — không bao giờ hardcode.**

---

## PHẦN 2 — LLM mental model (first principles)

> **Một câu cốt lõi:** Một transformer LLM là một hàm
> `tokens → phân phối xác suất cho token kế tiếp`.
> Mọi thứ khác — chat, RAG, agent — chỉ là *scaffolding* quanh việc lặp lại dự đoán token kế tiếp.

### 2.1. Token là gì?
- Model KHÔNG thấy ký tự hay từ. Nó thấy **token** — mảnh subword do bộ tokenizer (BPE)
  tạo ra. Ví dụ `"tokenization"` có thể tách thành `token` + `ization`.
- Quy tắc ngón tay cái tiếng Anh: **~4 ký tự ≈ 1 token**, ~0.75 từ ≈ 1 token. Tiếng Việt
  và code thường tốn token hơn.
- **Vì sao quan trọng:** *cost và latency tính theo token, không theo ký tự.* Giá =
  `f(input_tokens + output_tokens)`, và **output thường đắt hơn input**.

### 2.2. Context window
- Là **giới hạn tổng số token** (input + output) model xử lý trong MỘT lần gọi.
- Model chỉ "thấy" đúng những gì bạn gửi trong request đó. Vượt quá → lỗi hoặc bị cắt (truncate).
- Đây là lý do bạn không thể "nhồi" cả cơ sở dữ liệu vào prompt → nền tảng cho **RAG** (chỉ lấy phần liên quan).

### 2.3. Vì sao LLM là stateless
- Mỗi lần gọi API là **độc lập**. Model không nhớ gì giữa các request.
- "Chat nhớ được câu trước" là ảo giác: **bạn (client) tự gửi lại toàn bộ lịch sử**
  (`system` + các cặp `user`/`assistant`) mỗi lượt. Đây là mấu chốt để chẩn đoán bug
  "model quên những gì tôi vừa nói".
- Hệ quả cost: hội thoại càng dài, input token mỗi lượt càng phình → tiền càng tăng.

### 2.4. Sampling — temperature vs top-p
- Model xuất **phân phối xác suất** trên toàn bộ vocab cho token kế tiếp.
- **temperature**: làm phân phối "phẳng" (cao → sáng tạo/ngẫu nhiên) hay "nhọn" (thấp → an toàn/lặp lại). `temperature=0` ≈ greedy (chọn token xác suất cao nhất) → dùng khi cần *ổn định/deterministic* (trích xuất JSON, phân loại).
- **top-p (nucleus)**: chỉ lấy mẫu trong nhóm token nhỏ nhất có tổng xác suất ≥ p.
- *Lưu ý interview:* `temperature=0` **không đảm bảo tuyệt đối deterministic** (floating-point, batching phía server, MoE routing... vẫn gây khác biệt nhỏ).

### 2.5. Roles & logprobs
- **system / user / assistant**: system = chỉ dẫn/hành vi; user = đầu vào người dùng; assistant = phản hồi model. Bạn xếp chúng thành list `messages`.
- **logprobs**: log xác suất của token model chọn. Ứng dụng production: đo **confidence**,
  phát hiện câu trả lời "mù mờ", hoặc chấm điểm phân loại.

### 2.6. Vòng đời một chat request (whiteboard — nhớ vẽ được)
```
HTTP in  →  build messages (system+history+user)  →  tokenize
        →  model: next-token loop (sampling)  →  detokenize
        →  stream/JSON out  →  log tokens+cost+latency
```
Bạn sẽ phải **vẽ và giải thích không cần nhìn note** vào cuối tuần.

---

## Cầu nối sang hôm nay
Block A (đọc trên) → Block B: dựng repo + module typed đầu tiên + 4 exercises →
Block C: commit + điền `Notes.md`. Xem `exercises/` và `GitCommit.md`.
