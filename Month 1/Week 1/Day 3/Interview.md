# Interview — Day 3 (trả lời bằng lời của bạn, nói to được là đạt)

## Dataclass vs Pydantic
1. **`dataclass` khác Pydantic `BaseModel` ở đâu? Cái nào validate lúc runtime, cái nào không?**
   >

2. **Khi nào bạn chọn `dataclass`, khi nào Pydantic? Cho một ví dụ mỗi loại từ AI service.**
   >

3. **Vì sao `messages: list = []` trong dataclass là bug? Fix thế nào?**
   >

## Pydantic v2
4. **Vì sao Pydantic là "lingua franca" của AI code? (request/response, structured output, tool schema, config)**
   >

5. **`field_validator` khác `model_validator` thế nào? Cho một rule cần mỗi loại.**
   >

6. **Bạn đang ở Pydantic v2. Ba API bạn KHÔNG được viết theo v1 là gì (và v2 tương ứng)?**
   >

7. **`ValidationError` xảy ra khi nào, và ở FastAPI nó map sang HTTP status nào? Vì sao status đó?**
   >

## Settings / config
8. **Vì sao dồn config vào một `Settings` thay vì đọc `os.environ` rải rác? "Fail-fast" nghĩa là gì ở đây?**
   >

9. **Thứ tự ưu tiên nguồn config (arg / env / `.env` / default) ra sao? Vì sao env thắng `.env`?**
   >

10. **`SecretStr` giải quyết vấn đề gì? Bạn lấy giá trị thật lúc nào và tránh làm gì?**
   >

## Follow-ups (khó hơn)
- Provider trả **HTTP 200 nhưng body là object lỗi** (bug thật Day 2). Dùng Pydantic bạn đóng lỗ này thế nào?
  >
- Client gửi field thừa `{"temperatur": 0.5}` (typo). Với `extra="forbid"` vs `extra="ignore"`, điều gì xảy ra và bạn chọn cái nào ở biên API?
  >
- Vì sao `extra="ignore"` có thể hợp lý khi *đọc response provider* nhưng nguy hiểm khi *nhận request user*?
  >

## Practical scenario
Service của bạn thỉnh thoảng nổ `KeyError: 'usage'` sâu trong business logic, chỉ trên production, khó tái hiện.
Bạn nghi ngờ gì, và Pydantic tại biên (request + response provider) giúp *dời* lỗi này về đâu để dễ bắt hơn?
>

## Whiteboard
Vẽ đường đi của dữ liệu qua các biên (boundary) của service và đánh dấu chỗ nào là dataclass, chỗ nào Pydantic:
HTTP body → [?] → service → provider client(Settings) → provider 200 → [?] → Usage/cost.
> (mô tả hoặc dán ảnh sketch)
