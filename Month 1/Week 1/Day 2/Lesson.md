# Lesson — Day 2

> Bạn là backend dev ~5 năm (PHP/Laravel). Bài này KHÔNG dạy lập trình. Nó dạy
> (1) *3 idiom Python* bạn sẽ gõ hàng ngày cho tới mức phản xạ — và cái *khác* so với PHP,
> và (2) *cách làm cứng một lời gọi mạng* tới LLM cho ra dáng production.
> Idiom hôm nay không phải trang trí: **generator = nền của streaming (tuần 2)**,
> **decorator = nơi gắn retry/timing/logging**, **comprehension = ngôn ngữ biến đổi dữ liệu**.

---

## PHẦN 1 — Ba idiom cốt lõi (đào sâu)

### 1.1. Comprehension — ngôn ngữ biến đổi dữ liệu

PHP bạn viết `array_map` / `array_filter` + closure. Python gộp cả hai vào một biểu thức đọc
xuôi như tiếng Anh: *"lấy X từ Y nếu Z"*.

| PHP / Laravel | Python |
|---|---|
| `array_map(fn($t) => trim($t), $lines)` | `[t.strip() for t in lines]` |
| `array_filter($xs, fn($x) => $x > 0)` | `[x for x in xs if x > 0]` |
| `array_map` + `array_filter` lồng nhau | `[f(x) for x in xs if cond(x)]` (một dòng) |
| `array_combine($keys, $vals)` | `{k: v for k, v in zip(keys, vals)}` (dict comp) |
| tập hợp duy nhất | `{x for x in xs}` (set comp) |
| `collect($xs)->map(...)->filter(...)` | comprehension hoặc generator expression |

Bốn dạng:
- **list**: `[expr for x in it if cond]` → trả về `list`, dựng ngay toàn bộ trong RAM.
- **dict**: `{k: v for ...}`.
- **set**: `{expr for ...}` — tự khử trùng lặp.
- **generator expression**: `(expr for ...)` — **lazy**, không dựng list; truyền thẳng vào
  `sum(...)`, `any(...)`, `max(...)` để không tốn RAM.

```python
# đếm token của nhiều đoạn mà KHÔNG dựng list trung gian:
total = sum(len(enc.encode(t)) for t in texts)  # generator expr, O(1) bộ nhớ phụ
```

**Quy tắc nghề:** comprehension cho biến đổi *đơn giản, đọc được trong 1 hơi*. Nếu nó bắt đầu
lồng 3 tầng hoặc có side-effect (in, ghi file) → **quay lại `for` loop bình thường**.
Comprehension là để *tạo giá trị*, không phải để *chạy hành động*.

### 1.2. Generator & iterator — lazy, và là xương sống của streaming

- **Iterator protocol:** một object có `__iter__` và `__next__`. `for` chỉ là đường cú pháp
  gọi `next()` cho tới khi `StopIteration`. (PHP: `Iterator` interface — khá giống.)
- **Generator:** hàm có `yield`. Gọi nó **không chạy thân hàm ngay** — trả về một generator
  object. Mỗi lần `next()` chạy tới `yield` kế rồi *đóng băng* trạng thái. Đây là "hàm tạm
  dừng được". PHP 5.5+ cũng có `yield` — ý niệm gần như y hệt, nên bạn đã có sẵn trực giác.
- **`yield from sub()`**: uỷ quyền cho một iterable con (nối generator).
- **Vì sao quan trọng cho AI:** LLM trả lời theo *dòng token*. Server đẩy từng chunk; bạn
  `for chunk in stream:` và `yield` tiếp ra ngoài. Không có generator thì không có streaming
  đúng nghĩa (bạn sẽ buộc phải buffer hết → mất lợi ích time-to-first-token).

```python
def stream_tokens(resp) -> Iterator[str]:
    for chunk in resp:  # lazy: nhận tới đâu xử lý tới đó
        if (piece := chunk.delta) is not None:
            yield piece  # đẩy ra ngoài ngay, không buffer
```

**Bẫy #1 — generator dùng một lần:** cạn rồi là hết. `list(g)` lần hai ra rỗng.
**Bẫy #2 — lazy nghĩa là lỗi/nổ *muộn*:** exception chỉ bắn khi bạn *tiêu thụ*, không phải khi
*tạo* generator. Đừng ngạc nhiên khi try/except quanh chỗ tạo generator không bắt được gì.

### 1.3. Decorator — nơi gắn cross-cutting concern

Decorator = **hàm nhận một hàm, trả về một hàm** (thường bọc thêm hành vi). PHP gần nhất là
**attributes + middleware** — logic "vòng ngoài" (auth, log, cache) tách khỏi logic nghiệp vụ.

```python
import functools


def timed(fn):
    @functools.wraps(fn)  # giữ __name__/__doc__ của fn gốc (BẮT BUỘC)
    def wrapper(*args, **kwargs):
        t0 = perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            print(f"{fn.__name__}: {(perf_counter() - t0) * 1000:.1f} ms")

    return wrapper


@timed
def call_llm(prompt: str) -> str: ...


# `@timed` chỉ là đường cú pháp cho: call_llm = timed(call_llm)
```

- **`functools.wraps` không phải tuỳ chọn.** Thiếu nó, `call_llm.__name__` biến thành
  `"wrapper"` → hỏng log, hỏng introspection, hỏng vài framework (FastAPI đọc metadata hàm).
- **Decorator có tham số** = *ba tầng*: `retry(max=3)` trả về decorator, decorator trả về
  wrapper. Nhớ mẫu này — bạn sẽ viết `@retry(max_attempts=3)` ở exercise 2.
- **Xếp chồng** đọc từ **dưới lên**: hàm gần định nghĩa nhất bọc trước.

```python
@log_usage          # (3) ngoài cùng
@retry(max=3)       # (2)
@timed              # (1) sát hàm nhất → bọc đầu tiên
def call_llm(...): ...
```

- `functools.lru_cache` = decorator sẵn có để **memoize** (Laravel: `Cache::remember`). Đừng
  dùng cache cho lời gọi LLM non-deterministic trừ khi bạn cố ý muốn cache theo prompt.

---

## PHẦN 2 — Làm cứng lời gọi API (từ "chạy được" → "production")

Day 1 lời gọi httpx của bạn là *happy path*: mạng luôn ngon, server luôn 200. Production
không như vậy. Bốn thứ phải thêm, theo thứ tự ưu tiên:

### 2.1. Timeout — thứ #1, không bao giờ bỏ
Một lời gọi mạng **không có timeout** có thể treo *vĩnh viễn*, giữ chết một worker/connection.
Với LLM (phản hồi lâu) điều này càng nguy hiểm.
- `httpx.Timeout(connect=..., read=..., write=..., pool=...)` — tách **connect timeout**
  (bắt tay TCP, nên ngắn) khỏi **read timeout** (chờ dữ liệu, với LLM stream phải dài hơn).
- Quy tắc: *mọi* lời gọi ra ngoài đều có timeout tường minh. Mặc định "vô hạn" là bug chờ nổ.

### 2.2. Retry + exponential backoff + jitter
Lỗi *tạm thời* (transient) thì **thử lại**; lỗi *vĩnh viễn* thì **đừng**.
- **Backoff:** đợi `base * 2**attempt` giây (1s, 2s, 4s…) để không dội bom server đang ốm.
- **Jitter:** cộng ngẫu nhiên một chút → tránh "thundering herd" khi nhiều client cùng retry đồng loạt.
- **Giới hạn:** luôn có `max_attempts`. Retry vô hạn = tự DDoS mình + đốt tiền.
- **Idempotency:** retry an toàn khi thao tác *lặp lại không đổi kết quả*. Đọc/hoàn thành LLM
  thường an toàn; thao tác có side-effect (tạo bản ghi, gửi mail) cần **idempotency key**.

### 2.3. Error taxonomy — phân loại trước khi xử lý
| Loại | Ví dụ HTTP | Retry? | Lý do |
|---|---|---|---|
| Network / timeout | connect reset, read timeout | ✅ có (backoff) | thường tạm thời |
| Rate limit | `429` | ✅ có — **tôn trọng header `Retry-After`** nếu có | server bảo "chờ" |
| Server error | `500 502 503 504` | ✅ có (backoff) | sự cố phía server |
| Bad request | `400 422` | ❌ không | prompt/schema sai — retry cũng sai y vậy |
| Auth | `401 403` | ❌ không | key sai/hết quyền — retry vô ích |
| Not found | `404` | ❌ không | sai endpoint/model |

Nguyên tắc: **4xx (trừ 429) = lỗi của bạn, sửa code/đầu vào; 5xx + network + 429 = lỗi tạm, retry.**

### 2.4. Tái dùng connection + đưa hardening lên decorator
- Tạo **một** `httpx.Client` (hoặc `AsyncClient` ở tuần 2) và dùng lại → tái dùng TCP/TLS
  handshake (connection pooling). Đừng tạo client mới mỗi request.
- **Nối Phần 1 vào Phần 2:** timeout là tham số client; **retry + timing + usage-logging gói
  gọn thành decorator** (`@retry`, `@timed`, `@log_usage`) để logic gọi LLM ở giữa sạch sẽ.
  Đây chính là lý do hôm nay học decorator *ngay trước* khi harden.

### 2.5. Log token/cost — seed observability (nối tiếp Day 1)
Mỗi lời gọi: log `model`, `input_tokens`, `output_tokens`, `cost`, `latency_ms`, `status`,
`attempts`. Từ ngày 1 ta đã nói "log token mỗi request"; hôm nay ta biến nó thành một
**decorator** dùng lại được — nền cho persistence (tuần 3) và observability (Month 6).

---

## Cầu nối sang hôm nay
Đọc xong Phần 1 → làm `ex1` (comprehension) & `ex2` (decorator) để lên phản xạ →
đọc Phần 2 → làm `ex3` (generator pipeline, mô phỏng stream) & `ex4` (bọc httpx của Day 1
bằng timeout + retry + taxonomy + usage log). Điền `Notes.md` (8-Q generator/decorator +
bảng taxonomy). Xem `Architecture.md` để hiểu *vì sao* đặt retry/timeout ở tầng client.
