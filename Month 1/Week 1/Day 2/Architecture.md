# Architecture note — Day 2 (mini-ADR: retry & timeout ở tầng client)

> Chưa phải ADR-001 chính thức (viết cuối Project 1, tuần 4). Đây là ghi chú thiết kế nhỏ
> để tập tư duy "vì sao đặt ở đây".

## Bối cảnh
Service sẽ gọi LLM provider qua mạng — chậm, I/O-bound, và **không đáng tin** (429, 5xx,
mạng chập chờn). Cần quyết định đặt logic timeout + retry + phân loại lỗi ở đâu.

## Quyết định
Đặt timeout + retry + error-taxonomy ở **tầng client/adapter của provider**, KHÔNG rải rác
trong router hay business logic.

## Vì sao
- **Một chỗ duy nhất** biết cách nói chuyện với provider → đổi provider (OpenAI→Bedrock, tuần 2)
  không phải sửa retry ở khắp nơi.
- Router/handler chỉ nên lo HTTP-in/HTTP-out; nghiệp vụ chỉ lo nghiệp vụ. Retry/timeout là
  **cross-cutting concern** → hợp với decorator (`@retry`, `@timed`, `@log_usage`).
- Dễ test: mock client, giả lập 429 rồi 200, kiểm retry hoạt động — không cần mạng thật.

## Hệ quả / đánh đổi
- Phải phân biệt lỗi *retryable* vs *permanent* rõ ràng (xem bảng taxonomy trong `Notes.md`),
  nếu không sẽ retry cả lỗi 400 (vô ích, tốn tiền).
- Retry ẩn đi độ trễ thật → **phải log `attempts` + `latency` tổng** để không "mù" khi p95 vọt.
- Với thao tác có side-effect, retry cần **idempotency key** (chưa cần hôm nay, ghi nhớ cho sau).

## Cách tôi sẽ bảo vệ trong phỏng vấn (1 câu)
"Timeout và retry là thuộc tính của *cách gọi provider*, nên tôi gói chúng trong tầng client
sau một interface — nghiệp vụ không cần biết, và khi thêm provider mới tôi được kế thừa miễn phí."
