# Interview — Day 2 (trả lời bằng lời của bạn, nói to được là đạt)

## Idioms
1. **Comprehension vs `array_map`/`array_filter`: khi nào dùng, khi nào KHÔNG (quay lại for-loop)?**
   >

2. **Generator là gì? Khác list ở đâu? Vì sao nó là nền của streaming LLM?**
   >

3. **Generator "cạn một lần" nghĩa là gì? Và tại sao exception trong generator bắn ra *muộn*?**
   >

4. **Decorator là gì (nói theo góc middleware/attribute của Laravel)? `functools.wraps` để làm gì?**
   >

5. **Xếp chồng decorator: `@a @b @c def f()` — thứ tự bọc và thứ tự chạy ra sao?**
   >

## Hardening
6. **Vì sao MỌI lời gọi mạng phải có timeout? connect timeout khác read timeout thế nào?**
   >

7. **Lỗi nào nên retry, lỗi nào KHÔNG? Vì sao 429 retry được nhưng 400/401 thì không?**
   >

8. **Exponential backoff + jitter giải quyết vấn đề gì? Vì sao phải giới hạn số lần thử?**
   >

## Follow-ups (khó hơn)
- Retry loop của bạn thỉnh thoảng chạy mãi không dừng — bound nó lại thế nào và log gì?
  >
- Bạn retry một lời gọi *tạo bản ghi* — rủi ro gì và fix bằng gì (idempotency key)?
  >
- Vì sao nên tái dùng một `httpx.Client` thay vì tạo mới mỗi request?
  >

## Practical scenario
Production báo p95 latency của endpoint chat thỉnh thoảng vọt lên vô hạn và "treo" worker.
Bạn nghi ngờ gì đầu tiên và sửa ở đâu?
>

## Whiteboard
Vẽ luồng một lời gọi đã harden: request → (timeout) → response → classify(status) →
[retryable? backoff+jitter, lặp lại | permanent? raise] → log(tokens, cost, latency, attempts).
> (mô tả hoặc dán ảnh sketch)
