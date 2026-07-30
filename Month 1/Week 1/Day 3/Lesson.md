# Lesson — Day 3

> Bạn là backend dev ~5 năm (PHP/Laravel). Hôm nay KHÔNG học "cách khai báo class". Bạn học
> **ba tầng công cụ dữ liệu** trong Python và *chọn đúng tầng cho đúng việc*:
> - **`dataclass`** — struct có kiểu, *tin dữ liệu bên trong* (không validate).
> - **Pydantic v2** — *cổng biên* (boundary): validate + ép kiểu + serialize dữ liệu **không tin được** từ ngoài.
> - **`pydantic-settings`** — cấu hình tập trung, được validate lúc khởi động (fail-fast).
>
> Vì sao quan trọng: dữ liệu vào một AI service (request của user, response của provider, biến môi trường)
> đều **không đáng tin**. Day 2 bạn đã nếm điều đó: OpenRouter trả **HTTP 200 nhưng body là lỗi**.
> Pydantic là nơi ta *chặn dữ liệu rác ngay tại cửa* thay vì để nó lan vào business logic rồi nổ `KeyError`
> ở tận đâu đó. Và đây là ngôn ngữ chung mà **FastAPI, structured output, tool schema** (tuần 2–3) đều dùng.

---

## PHẦN 1 — `dataclass`: struct có kiểu (dữ liệu *đã tin*)

`dataclass` = decorator sinh sẵn `__init__`, `__repr__`, `__eq__` cho một class chỉ-chứa-dữ-liệu.
Laravel gần nhất: một **DTO** / value object viết tay (bạn tự gõ constructor + getter).

```python
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Money:
    amount_cents: int
    currency: str = "USD"

    def as_decimal(self) -> float:
        return self.amount_cents / 100
```

Bốn cờ (flag) đáng nhớ:
- **`frozen=True`** → immutable (như value object). Gán lại field ném `FrozenInstanceError`. Dùng cho
  giá trị *không nên đổi* (config đã load, một message trong lịch sử chat).
- **`slots=True`** → không có `__dict__` per-instance → **nhẹ RAM + nhanh hơn**. Quan trọng khi bạn giữ
  hàng nghìn object (ví dụ: token/message trong một stream dài).
- **`field(default_factory=list)`** → **BẮT BUỘC** cho default là `list`/`dict`. Viết `msgs: list = []`
  là bug kinh điển (mutable default *dùng chung* giữa mọi instance — y như bug PHP static array).
- **`__post_init__`** → chạy sau `__init__`, nơi bạn *derive* field hoặc *assert* điều kiện đơn giản.

**Giới hạn cốt lõi:** `dataclass` **KHÔNG validate và KHÔNG ép kiểu**. Type hint chỉ để `mypy` đọc lúc
*tĩnh*; lúc *chạy*, `Money(amount_cents="oops")` vẫn tạo được object rác. Vậy nên:

> **Quy tắc chọn:** dùng `dataclass` cho dữ liệu **bạn tự tạo và đã tin** bên trong hệ thống.
> Dùng **Pydantic** ở **biên** — nơi dữ liệu đến từ user, network, file, env.

---

## PHẦN 2 — Pydantic v2: validate + ép kiểu + serialize tại biên

Pydantic = "khai báo hình dạng dữ liệu, thư viện lo phần kiểm tra". Laravel map rất sát:
**FormRequest (validate input)** + **API Resource (serialize output)** gộp làm một, cho *mọi* dữ liệu.

```python
from pydantic import BaseModel, Field, field_validator


class ChatMessage(BaseModel):
    role: str = Field(pattern="^(system|user|assistant)$")
    content: str = Field(min_length=1, max_length=8000)


class ChatRequest(BaseModel):
    model: str
    messages: list[ChatMessage] = Field(min_length=1)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    @field_validator("messages")
    @classmethod
    def last_must_be_user(cls, v: list[ChatMessage]) -> list[ChatMessage]:
        if v[-1].role != "user":
            raise ValueError("message cuối phải có role=user")
        return v


# parse dữ liệu KHÔNG tin được (vd JSON từ HTTP body):
raw = {
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "hi"}],
    "temperature": "0.5",
}
req = ChatRequest.model_validate(raw)  # "0.5" (str) -> 0.5 (float): ép kiểu tự động
print(req.model_dump_json())  # serialize ra JSON
```

Những điểm phải nắm (và những cái *khác* Pydantic v1 — quan trọng cho phỏng vấn):

- **`Field(...)`** = ràng buộc + metadata: `ge/le/gt/lt` (số), `min_length/max_length`, `pattern` (regex),
  `default`, `default_factory`, `alias`. Đây là "rule" như FormRequest.
- **Validate lúc *khởi tạo*.** Khác `dataclass`: tạo object = đã validate. `ValidationError` gom **mọi** lỗi
  một lần (không dừng ở lỗi đầu) → thông điệp lỗi đẹp cho client.
- **Ép kiểu (coercion):** `"0.5"`→`0.5`, `"3"`→`3`. Có kiểm soát; nếu muốn nghiêm ngặt dùng `Strict` types.
- **v2 API mới (đừng viết kiểu v1):**
  - `model_validate(dict)` thay `parse_obj`; `model_validate_json(str)` thay `parse_raw`.
  - `model_dump()` / `model_dump_json()` thay `.dict()` / `.json()`.
  - `@field_validator` thay `@validator`; `@model_validator(mode="after")` thay `@root_validator`.
  - Config bằng `model_config = ConfigDict(...)` thay `class Config`.
- **`field_validator` (một field) vs `model_validator` (cross-field).** "Message cuối phải là user" cần nhìn
  cả list → `field_validator("messages")`. "Nếu `stream=True` thì `n` phải =1" cần nhiều field → `model_validator(mode="after")`.
- **`model_config = ConfigDict(extra="forbid")`** → field lạ trong input bị *từ chối* thay vì bị bỏ im lặng.
  Ở biên API, `forbid` giúp bắt lỗi client sớm. (Cân nhắc `ignore` khi đọc response provider có field thừa.)
- **`ValidationError`** là exception bạn sẽ map sang **HTTP 422** ở FastAPI (tuần 2 làm tự động).

**Vì sao Pydantic ở khắp nơi trong AI code:** request/response, **structured output** (bắt LLM trả JSON đúng
schema), **tool/function schema** (mô tả tham số cho model), config — tất cả đều là "dữ liệu có hình dạng cần
được đảm bảo". Học chắc hôm nay = đỡ 80% ma sát ở tuần 2–3.

---

## PHẦN 3 — `pydantic-settings`: cấu hình tập trung, fail-fast

Day 1–2 bạn đọc `os.environ["OPENROUTER_API_KEY"]` *ngay chỗ cần*. Ba vấn đề: (1) rải rác → khó biết service
cần những gì; (2) không validate → thiếu key thì nổ *muộn*, giữa request; (3) không kiểu → `TIMEOUT` là str.

`pydantic-settings` = một Pydantic model **tự đọc từ env/`.env`**, validate **một lần lúc khởi động**.
Laravel map: `config/*.php` + `.env` + `config()` helper — nhưng có kiểu và fail-fast.

```python
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="APP_", extra="ignore"
    )

    openrouter_api_key: SecretStr  # bắt buộc; thiếu -> fail lúc khởi động
    model: str = "openai/gpt-4o-mini"
    base_url: str = "https://openrouter.ai/api/v1"
    request_timeout_s: float = Field(default=60.0, gt=0)
    max_retries: int = Field(default=3, ge=0, le=10)


settings = (
    Settings()
)  # đọc .env + env vars, validate NGAY. Thiếu key -> ValidationError.
```

Điểm nghề:
- **`SecretStr`** — key/secret không lộ khi `print`/log (`repr` ra `**********`); lấy giá trị thật bằng
  `.get_secret_value()`. **Không bao giờ** log key thô.
- **Fail-fast:** khởi tạo `Settings()` lúc *boot*. Thiếu/config sai → app **không start**, thay vì chết giữa
  request lúc 2h sáng. Đây là "seed" cho lifespan startup của FastAPI tuần 2.
- **Thứ tự ưu tiên nguồn:** đối số truyền thẳng > **biến môi trường** > `.env` > default. Env thắng `.env`
  (đúng cho container/CI, nơi bạn set env chứ không có file `.env`).
- **`env_prefix`** tránh đụng tên biến env chung; **nested settings** (model con) cho nhóm config lớn.
- **Một instance dùng chung** (import `settings`), tiêm vào client qua tham số — KHÔNG đọc `os.environ`
  rải rác nữa. Tuần 2 cái này biến thành `Depends(get_settings)` của FastAPI.

---

## PHẦN 4 — Cầu nối: vì sao đây chính là bậc thang lên FastAPI

Ghép ba mảnh trên lại là *hình dạng* của một service thật:

```
HTTP body (JSON, không tin)  --ChatRequest.model_validate-->  object đã validate
        |                                                          |
     (422 nếu sai)                                          business/service
                                                                   |
env/.env (không tin)  --Settings()-->  config đã validate  --tiêm-->  ProviderClient
                                                                   |
provider HTTP 200 (vẫn không tin! bug Day 2)  --ChatResponse.model_validate-->  Usage/cost có kiểu
```

- **FormRequest → Pydantic model.** Tuần 2, FastAPI tự gọi `model_validate` cho body và tự trả 422 —
  bạn chỉ khai báo model. Hôm nay bạn làm *thủ công* để hiểu điều FastAPI làm dưới mui xe.
- **`.env`/config() → `Settings` + `Depends`.** `get_settings()` sẽ là một dependency; router nhận
  `settings` mà không biết nó từ env hay test-override.
- **API Resource → `response_model`.** Trả về Pydantic model = response được serialize + tài liệu OpenAPI tự sinh.
- **Đóng bug Day 2 đúng chỗ:** provider trả 200 + body lỗi → cho `ChatResponse.model_validate` *phân xử*.
  Nếu body không khớp schema (thiếu `usage`, có `error`) → `ValidationError` = tín hiệu rõ ràng để phân loại
  `Permanent`/`Transient`, thay vì `dict.get("usage")` mù mờ.

> **Câu chốt để nhớ cả ngày:** *`dataclass` cho dữ liệu tôi đã tin; **Pydantic cho mọi thứ băng qua biên**
> (user, network, env); config là dữ liệu-tại-biên nên nó cũng là Pydantic (settings), validate một lần lúc boot.*

---

### Bẫy thường gặp (đọc kỹ, sẽ gặp ở exercise)
1. **Mutable default** trong dataclass (`x: list = []`) → dùng `field(default_factory=list)`.
2. **Viết Pydantic v1 trong v2** (`.dict()`, `@validator`, `class Config`) → mypy/deprecation cảnh báo; dùng API v2.
3. **Nghĩ dataclass validate** — không. Type hint dataclass chỉ tĩnh; runtime không kiểm.
4. **Log `SecretStr` sai cách** — đừng `.get_secret_value()` rồi tống vào log. Chỉ lấy secret lúc *dùng*.
5. **Đọc `os.environ` rải rác** — dồn hết vào `Settings`, tiêm xuống. Một nguồn sự thật.
6. **`extra` mặc định** — ở input API cân nhắc `forbid` (bắt lỗi client); đọc response provider có thể `ignore`.
