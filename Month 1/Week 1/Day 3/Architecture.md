# Architecture note — Day 3 (mini-ADR: validate-at-the-boundary + centralized settings)

> Chưa phải ADR-001 chính thức (viết cuối Project 1, tuần 4). Đây là ghi chú thiết kế nhỏ để tập
> tư duy "vì sao đặt ở đây". Kế thừa mini-ADR Day 2 (retry/timeout ở tầng client).

## Bối cảnh
Một AI service nhận dữ liệu **không đáng tin** từ nhiều biên: HTTP body của user, biến môi trường,
và response của provider (Day 2 đã chứng minh: HTTP 200 vẫn có thể là body lỗi). Nếu để dữ liệu rác
lọt vào business logic, lỗi nổ *muộn* và *xa* điểm gốc (`KeyError` sâu trong service, chỉ trên prod).

## Quyết định
1. **Validate tại biên.** Mọi dữ liệu băng qua biên hệ thống phải đi qua một Pydantic model *trước khi*
   chạm business logic: request (`ChatRequest`), response provider (`ChatResponse`/`Usage`).
2. **Config tập trung, fail-fast.** Một `Settings` (pydantic-settings) là **nguồn sự thật duy nhất** cho
   cấu hình; khởi tạo + validate **một lần lúc boot**; tiêm xuống client qua tham số (không đọc `os.environ` rải rác).
3. **`dataclass` cho dữ liệu nội bộ đã tin**; Pydantic chỉ dành cho biên.

## Vì sao
- **Dời lỗi về gần điểm gốc.** Dữ liệu sai bị chặn *tại cửa* với `ValidationError` mô tả rõ field nào sai,
  thay vì `KeyError` mù mờ ở tầng sâu. Dễ debug, dễ trả 422 cho client.
- **Business logic được tin dữ liệu.** Sau biên, code chỉ làm việc với object có kiểu, đúng shape → ít
  phòng thủ rải rác (`.get(...)` khắp nơi).
- **Đóng bug Day 2 đúng chỗ.** Cho `ChatResponse.model_validate` phân xử body provider: thiếu `usage`/có
  `error` → `ValidationError` = tín hiệu rõ để phân loại Transient/Permanent (nối vào taxonomy Day 2).
- **Config fail-fast** = lỗi cấu hình làm app *không start*, không phải chết giữa request lúc 2h sáng.
- **Một nguồn config** → đổi provider/model/timeout ở một chỗ; test dễ (override Settings, không đụng env thật).

## Hệ quả / đánh đổi
- Thêm một lớp model + chi phí validate mỗi request (rất nhỏ so với latency LLM — chấp nhận được).
- Phải chọn chính sách `extra`: **`forbid` ở input user** (bắt typo/field lạ sớm) nhưng cân nhắc **`ignore`
  khi đọc response provider** (provider thêm field mới không nên làm mình sập).
- `SecretStr` che secret khỏi log → phải nhớ `.get_secret_value()` đúng chỗ *dùng*, không log ra.
- Ép kiểu (coercion) tiện nhưng cần ý thức: `"0.5"`→`0.5`. Nơi cần nghiêm ngặt dùng Strict types.

## Cách tôi sẽ bảo vệ trong phỏng vấn (1 câu)
"Validate mọi dữ liệu từ bên ngoài vào bằng Pydantic để bắt lỗi sớm thay vì cho đi vào business logic. Các cấu hình sẽ được đưa vào một class Setting để quản lý chung, được validate lúc boot để fail-fast thay vì bị chết khi có request tới"
