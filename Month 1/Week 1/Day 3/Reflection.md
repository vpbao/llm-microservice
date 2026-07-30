# Reflection — Day 3

**Ngày:** 3 · **Thời lượng thực tế:** 3 h · **Confidence (1–5):** 5

## 3 điều học được hôm nay
1. dùng pydantic cho dữ liệu biên, dataclass cho dữ liệu nội bộ, đã tin tưởng
2. pydantic setting cho quản lý environment variables. set env trực tiếp thắng .env vì ở CI CD hay prod sẽ ko có .env file.
3. apply vào cách gọi API 

## Điều còn mơ hồ / cần hỏi mentor
- 

## Production-mindset seed hôm nay
- Correctness/robustness: nếu client gửi request rác hoặc provider trả body lỗi, lỗi nổ *tại cửa* hay lan
  vào business logic? Pydantic tại biên đã dời lỗi về đúng chỗ chưa? → tại cửa, đã đúng
- Config: nếu thiếu một biến env quan trọng, app fail lúc *boot* hay chết giữa request? → boot

## Deliverable đã xong?
- [x] Đọc Lesson (dataclass · Pydantic v2 · settings · cầu nối FastAPI)
- [x] Notes: cheat-sheet + bảng chọn dataclass/Pydantic + 8-Q Pydantic + 8-Q Settings
- [x] ex1 dataclass — frozen/slots/default_factory/__post_init__ — mypy sạch
- [x] ex2 pydantic models — Field constraints + field_validator + model_validator — parse dict bẩn
- [x] ex3 settings — đọc .env, SecretStr, fail-fast lúc khởi động
- [x] ex4 typed client — nhận Settings, trả ChatResponse/Usage (Pydantic), validate response phòng thủ
- [x] mypy --strict + ruff sạch trên cả 4
- [x] 1 commit
- [x] Architecture.md điền xong

## Gõ `Day 3 completed` khi tất cả ô trên đã tick.
