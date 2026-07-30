# Notes — Day 3

## Cheat-sheet: dataclass vs Pydantic vs Laravel (tự viết bằng lời của bạn)
| Việc | Laravel / PHP | Python `dataclass` | Pydantic v2 | Ghi chú của bạn |
|---|---|---|---|---|
| struct dữ liệu đã tin | DTO viết tay | `@dataclass` | (được, nhưng thừa) | dành cho các class chỉ đọc |
| validate input từ ngoài | FormRequest `rules()` | ❌ không validate | `BaseModel` + `Field` | dành cho dữ liệu từ ngoài vào, chặn lúc runtime |
| ép kiểu `"3"`→`3` | thủ công | ❌ | tự động (coercion) | Field trong pydantic  |
| serialize ra JSON | API Resource | `asdict()` thủ công | `model_dump_json()` | thư viện pydantic  |
| immutable value object | readonly props | `frozen=True` | `model_config frozen=True` | dùng để đọc |
| cross-field rule | `rules()` phức tạp | `__post_init__` (assert) | `@model_validator` | __post_init__ phải tự validate, còn @model_validator thì define còn validate để thư viện làm |
| config tập trung | `config/*.php` + `.env` | ❌ | `pydantic-settings` | quản lý biến môi trường, có thứ tự đọc ưu tiên, có in ***** mấy cái secret |
| giấu secret khi log | — | ❌ | `SecretStr` | ưu điểm của `pydantic-settings` |

> Q (từ P1): dataclass KHÔNG làm được gì mà Pydantic làm được? → chặn lúc khởi tạo, còn pydantic là gom mọi lỗi rồi trả về ValidationError
> Q (từ P3): vì sao env thắng `.env` trong thứ tự ưu tiên? → khi deploy thật (container/CI/server) KHÔNG có file `.env`, mình set biến môi trường trực tiếp; `.env` chỉ tiện lúc dev. Nên env thật phải đè được lên default trong `.env`.

---

## Bảng quyết định — KHI NÀO dataclass, KHI NÀO Pydantic (điền cột "Chọn + vì sao")
| Tình huống | Chọn dataclass / Pydantic? | Vì sao |
|---|---|---|
| Parse HTTP request body của user | Pydantic | để gom hết lỗi rồi xử lý luôn 1 lần thay vì từng lỗi một tốn nhiều lần sửa |
| Một `Message` trong lịch sử chat tôi tự dựng trong code | dataclass | dữ liệu tự dựng, validate đơn giản được |
| Đọc response JSON của provider (không tin) | pydantic | dữ liệu bên ngoài |
| Config app (key, model, timeout) từ env | pydantic | bảo mật tốt hơn, thứ tự ưu tiên |
| Value object `Money` immutable dùng nội bộ | dataclass (`frozen=True`) | dữ liệu nội bộ đã tin, không băng qua biên → Pydantic là thừa (nặng/chậm hơn) |
| Schema cho structured output (bắt LLM trả JSON) | pydantic | ko tin dữ liệu từ bên ngoài |

**Câu vàng để nhớ:** *dataclass cho dữ liệu tôi đã tin (nội bộ); Pydantic cho MỌI thứ băng qua biên (user, network, env).*

---

## 8-question test — "PYDANTIC v2"
> Chưa trả lời được cả 8 = chưa học xong. Trả lời bằng lời của bạn.

1. **Vì sao cần nó?** → để validate dữ liệu từ bên ngoài vào hệ thống
2. **Giải quyết vấn đề gì?** (gợi ý: dữ liệu không tin ở biên; `KeyError` muộn) → dữ liệu không tin ở biên; `KeyError` muộn
3. **Hoạt động bên trong ra sao?** (gợi ý: validate + coerce lúc khởi tạo; `ValidationError` gom mọi lỗi) → validate lúc khởi tạo; `ValidationError` gom mọi lỗi
4. **Khi nào dùng (vs dataclass)?** → kiểm tra dữ liệu từ bên ngoài vào hệ thống, cần bắn lỗi sớm ở biên, tránh phải access vào hệ thống sâu rồi mới lỗi.
5. **Khi nào KHÔNG?** (gợi ý: dữ liệu nội bộ đã tin, cần cực nhẹ) → dữ liệu nội bộ đã tin, cần cực nhẹ
6. **Câu phỏng vấn hay gặp?** (gợi ý: khác gì v1? `field_validator` vs `model_validator`?) → có gì khác gì v1? `field_validator` vs `model_validator`? khi nào dùng đến?
7. **Lỗi người mới hay mắc?** (gợi ý: viết API v1 trong v2; tưởng dataclass validate) → viết API v1 trong v2; tưởng dataclass validate
8. **Dùng trong production thế nào?** (gợi ý: request/response FastAPI→422, structured output, tool schema) → request/response FastAPI→422, structured output, tool schema

---

## 8-question test — "SETTINGS / CONFIG (pydantic-settings)"
1. **Vì sao cần nó?** → để quản lý biến môi trường
2. **Giải quyết vấn đề gì?** (gợi ý: config rải rác, không validate, nổ muộn) → config rải rác, không validate, nổ muộn
3. **Hoạt động bên trong ra sao?** (gợi ý: đọc env/`.env`, validate 1 lần lúc khởi động) → đọc env/`.env`, validate 1 lần lúc khởi động
4. **Khi nào dùng?** → quản lý biến môi trường tập trung, nổ lỗi sớm nếu có
5. **Khi nào KHÔNG?** → khi thứ đó không phải config: dữ liệu thay đổi theo từng request, hoặc script nhỏ dùng một lần chẳng có gì để cấu hình.
6. **Câu phỏng vấn hay gặp?** (gợi ý: thứ tự ưu tiên nguồn? `SecretStr` để làm gì?) → thứ tự ưu tiên nguồn? `SecretStr` để làm gì?
7. **Lỗi người mới hay mắc?** (gợi ý: đọc `os.environ` rải rác; log secret thô) → đọc `os.environ` rải rác; log secret thô
8. **Dùng trong production thế nào?** (gợi ý: fail-fast lúc boot, `Depends(get_settings)`, config theo môi trường) → fail-fast lúc boot, `Depends(get_settings)`, config theo môi trường

---

## Pydantic v1 → v2 — bảng đổi API (để không viết nhầm)
| Ý định | v1 (ĐỪNG dùng) | v2 (dùng cái này) |
|---|---|---|
| parse dict | `Model.parse_obj(d)` | `Model.model_validate(d)` |
| parse json string | `Model.parse_raw(s)` | `Model.model_validate_json(s)` |
| ra dict | `m.dict()` | `m.model_dump()` |
| ra json | `m.json()` | `m.model_dump_json()` |
| validate 1 field | `@validator("x")` | `@field_validator("x")` |
| validate cross-field | `@root_validator` | `@model_validator(mode="after")` |
| config model | `class Config:` | `model_config = ConfigDict(...)` |

---

## Ghi chú `SecretStr`
- Vì sao cần? → (giấu secret khỏi log/`repr`/traceback) giấu secret khỏi log/`repr`/traceback
- Lấy giá trị thật thế nào, và chỉ nên lấy khi nào? → dùng `.get_secret_value()`, và CHỈ ngay tại chỗ dùng (vd gắn header `Authorization`), không gán ra biến, không log.

## Số liệu chạy thật (điền sau khi làm ex4 — client trả Pydantic model)
| Prompt | model | input tok | output tok | cost $ |
|---|---|---|---|---|
| Giải thích 'timeout' trong 1 câu | nvidia/nemotron-3-ultra-550b-a55b:free | 27 | 63 | ~0.0000418 |
