# Resources — Day 3 (primary sources, đọc bản gốc)

## Dataclasses
- Python docs — `dataclasses` (đọc: `field`, `default_factory`, `frozen`, `slots`, `__post_init__`).
- PEP 557 — Data Classes (đọc lướt để hiểu ý niệm/động cơ).
- *Fluent Python* (Ramalho) — ch. "Data Class Builders" (dataclass vs namedtuple vs attrs).

## Pydantic v2 (đọc bản v2, KHÔNG phải v1)
- Pydantic docs — **Models** (khai báo, `model_validate`, `model_dump`).
- Pydantic docs — **Fields** (`Field`, constraints `ge/le/min_length/pattern`, `alias`).
- Pydantic docs — **Validators** (`field_validator`, `model_validator`, `mode="before"/"after"`).
- Pydantic docs — **Migration guide v1→v2** (đọc để không viết nhầm API cũ).
- Pydantic docs — **Serialization** (`model_dump` / `model_dump_json`, `exclude`, `by_alias`).

## pydantic-settings
- pydantic-settings docs — **Settings management** (`BaseSettings`, `SettingsConfigDict`, `env_file`, `env_prefix`).
- pydantic-settings docs — **thứ tự ưu tiên nguồn** (init args > env > `.env` > secrets > default).
- Pydantic docs — `SecretStr` / `SecretBytes`.

## Cầu nối FastAPI (đọc trước 1 chút cho tuần 2)
- FastAPI docs — "Request Body" (cách FastAPI dùng Pydantic model + trả 422 tự động).
- FastAPI docs — "Settings and Environment Variables" (dùng `pydantic-settings` + `Depends`, `lru_cache`).

## Ghi chú
- Vẫn KHÔNG động vào LangChain/LlamaIndex. Build tay trước.
- Hôm nay là **cầu nối**: mọi thứ Pydantic/Settings làm thủ công hôm nay, tuần 2 FastAPI sẽ tự động hoá.
  Hiểu cơ chế trước, rồi mới để framework lo.
