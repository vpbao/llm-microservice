# Reflection — Day 2

**Ngày:** 2 · **Thời lượng thực tế:** 4 h · **Confidence (1–5):** 4

## 3 điều học được hôm nay
1. decorator - bao bọc 1 hàm, truyền vào hàm và trả về hàm được bao, không thay đổi logic chính.
2. generator - giảm ngốn ram, streaming, xử lý dữ liệu lớn
3. không tin hoàn toàn vào status, phải check body. 
4. luôn có timeout khi call API, phân biết error code để retry (400 trừ 429 là ko retry)
5. phân biệt connection timeout và read timeout

## Điều còn mơ hồ / cần hỏi mentor
- `Retry-After`: chưa implement tôn trọng header khi gặp 429 (mới để `# TODO`). Cần phân biệt "có `resp`" (lỗi HTTP) vs "không có `resp`" (lỗi mạng) — quay lại sau.

## Production-mindset seed hôm nay
- Reliability: nếu client này chạy thật tối nay, lỗi tạm thời của provider có làm sập request của mình không? Timeout + retry đã đủ chưa? -> sẽ ko sập nếu biết cách retry và set timeout ổn.
- **Bài học từ bug thật (KeyError 'usage'):** OpenRouter đôi khi trả **HTTP 200 nhưng body là object lỗi** → không thể tin mỗi status code. Taxonomy/`_classify` nên soi cả **body** (kiểm `data.get("error")`), và parse response phòng thủ (`.get("usage")` thay vì `["usage"]`) thay vì tin mù cấu trúc từ bên ngoài. → thêm `# TODO: check body error` trong ex4.

## Deliverable đã xong?
- [x] Đọc Lesson (idioms + hardening)
- [x] Notes: cheat-sheet idioms + 8-Q generator + 8-Q decorator + bảng taxonomy
- [x] ex1 comprehensions — mypy sạch
- [x] ex2 decorators (@timed/@retry/@log_usage) — dùng functools.wraps
- [x] ex3 generator pipeline — chạy in đúng token list
- [x] ex4 hardened client — timeout + retry + taxonomy + usage log
- [x] 1 commit

## Gõ `Day 2 completed` khi tất cả ô trên đã tick.
