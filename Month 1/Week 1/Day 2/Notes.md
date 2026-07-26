# Notes — Day 2

## Cheat-sheet idioms PHP/Laravel → Python (tự viết bằng lời của bạn)
| Việc | PHP / Laravel | Python | Ghi chú của bạn |
|---|---|---|---|
| map | `array_map(fn, $xs)` | `[f(x) for x in xs]` | gọi f(x) từ x lặp qua xs |
| filter | `array_filter($xs, fn)` | `[x for x in xs if cond]` | lấy x từ xs nếu cond |
| map+filter | lồng 2 hàm | 1 comprehension |gọi f(x) từ x lặp qua xs nếu cond |
| dict từ 2 mảng | `array_combine` | `{k: v for k, v in zip(...)}` | kết hợp 2 mảng |
| lazy / tiết kiệm RAM | Generator (`yield`) | generator expr `( ... )` / `def ... yield` | tạm dừng, ko load tất cả vào ram |
| cross-cutting (auth/log) | middleware / attribute | **decorator** | hàm bao bọc hàm chính, ko làm thay đổi hành vi của hàm chính |
| memoize | `Cache::remember` | `@functools.lru_cache` | |

> Q (từ ex1): Khi nào KHÔNG dùng comprehension? →

---

## 8-question test — "GENERATOR"
> Chưa trả lời được cả 8 = chưa học xong.

1. **Vì sao cần nó?** → để ko ngốn ram
2. **Giải quyết vấn đề gì?** (gợi ý: lazy, RAM, streaming) → lazy load, ko bị ngốn ram, phục vụ cho steaming
3. **Hoạt động bên trong ra sao?** (gợi ý: `yield` đóng băng trạng thái, `next()`, `StopIteration`) → yield tạm dừng hàm, **giữ nguyên trạng thái biến**; lần gọi (`next()`) sau chạy tiếp đúng chỗ dừng, tới khi cạn thì bắn `StopIteration`
4. **Khi nào dùng?** → streaming dữ liệu.
5. **Khi nào KHÔNG?** (gợi ý: cần dùng lại nhiều lần / cần random access) → khi một phần tử cần dùng lại thì ko nên dùng, thay vào đó dùng list
6. **Câu phỏng vấn hay gặp?** → generator là gì? vì sao cần thiết, cơ chế hoạt động ntn? 
7. **Lỗi người mới hay mắc?** (gợi ý: generator cạn 1 lần; lỗi bắn *muộn* lúc tiêu thụ) → generator cạn 1 lần; lỗi bắn *muộn* lúc tiêu thụ
8. **Dùng trong production thế nào?** (gợi ý: stream token SSE, xử lý file lớn) → stream token SSE, xử lý data lớn

---

## 8-question test — "DECORATOR"
1. **Vì sao cần nó?** → để làm các việc biên ngoài business logic chính
2. **Giải quyết vấn đề gì?** (gợi ý: tách cross-cutting concern khỏi nghiệp vụ) → tách cross-cutting concern khỏi nghiệp 
3. **Hoạt động bên trong ra sao?** (gợi ý: hàm nhận hàm trả hàm; decorator có tham số = 3 tầng) → hàm nhận hàm và trả về hàm mới đã bọc.
4. **Khi nào dùng?** → khi cần log, timed, làm các việc bao quanh công việc chính
5. **Khi nào KHÔNG?** → không cần làm gì ngoài business chính
6. **Câu phỏng vấn hay gặp?** (gợi ý: `functools.wraps` để làm gì? thứ tự khi xếp chồng?) → `functools.wraps` để copy tên/metadata của hàm gốc sang wrapper (không mất `__name__`). Xếp chồng: **đọc từ dưới lên** — decorator sát hàm nhất bọc trước, trên cùng bọc ngoài cùng (bằng chứng ở ex2: 3 dòng `noisy: ...ms` từ @timed, rồi 1 dòng `status=ok` từ @log_usage).
7. **Lỗi người mới hay mắc?** (gợi ý: quên `wraps` → mất `__name__`; nuốt exception) → quên `wraps` → mất `__name__`; nuốt exception
8. **Dùng trong production thế nào?** (gợi ý: `@retry`, `@timed`, `@log_usage`, `@app.get`) → dùng retry, timed log_usage hay app.get

---

## Error taxonomy — retry được vs KHÔNG (điền cột "Xử lý của bạn")
| Loại | HTTP | Retry? | Xử lý của bạn |
|---|---|---|---|
| Network / timeout | connect reset, read timeout | ✅ backoff | retry |
| Rate limit | `429` | ✅ + tôn trọng `Retry-After` | retry |
| Server error | `500 502 503 504` | ✅ backoff | retry |
| Bad request | `400 422` | ❌ | không |
| Auth | `401 403` | ❌ | không |
| Not found | `404` | ❌ | không |

**Câu vàng để nhớ:** *4xx (trừ 429) = lỗi của mình, sửa đầu vào; 5xx + network + 429 = lỗi tạm, retry có backoff + jitter + giới hạn số lần.*

---

## Retry / backoff — ghi chú
- **Exponential backoff:** chờ `base * 2**attempt` (0.5s → 1s → 2s…). Vì sao không retry ngay lập tức? → để dàn tải
- **Jitter:** cộng ngẫu nhiên để tránh "thundering herd". Vì sao cần? → để ko bị tràn vào server cùng 1 lúc, 
- **max_attempts:** vì sao retry vô hạn là nguy hiểm? → vì nếu vô hạn sẽ dẫn đến quá tải server, tránh ddos
- **Idempotency:** thao tác nào retry an toàn, thao tác nào cần idempotency key? → retry an toàn khi thao tác *lặp lại không đổi kết quả*. Đọc/hoàn thành LLM thường an toàn; thao tác có side-effect (tạo bản ghi, gửi mail) cần **idempotency key**.

## Timeout — ghi chú
- connect vs read timeout khác nhau thế nào, và vì sao với LLM read phải dài hơn? → connect là kết nối đến tcp -> nhanh, read timeout là đọc kết quả từ llm nên có thể lâu hơn có thể khoảng 60s 
- Điều gì xảy ra nếu gọi mạng KHÔNG timeout? → nếu server bên kia chết thì request bị treo và hệ thống của mình sẽ chết theo

## Số liệu chạy thật (điền sau khi làm ex4)
| Prompt | input tok | output tok | cost $ | latency ms | attempts |
|---|---|---|---|---|---|
| Giải thích 'timeout' trong 1 câu. | 27 | 61 | 0.000041 | 2024 | 1 |
