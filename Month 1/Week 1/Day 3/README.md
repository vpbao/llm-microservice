# Day 3 — Dataclass vs **Pydantic v2** + config/settings (`pydantic-settings`) → cầu nối FastAPI

**Date:** Wed 29 Jul 2026 · **Week 1 / Month 1** · **Project:** `llm-microservice`
**Mode:** Mentor + tự code (bạn tự viết code trong stub, mentor giảng + review)

> Day 1–2 bạn có: idioms (comprehension/generator/decorator) + một **hardened client** trả về
> `dict` thô. Vấn đề: `dict` không có kiểu, không tự kiểm tra, và cấu hình (key/model/base_url)
> đang nằm rải rác qua `os.environ`. Hôm nay ta đóng hai lỗ hổng đó:
> **(1) mô hình dữ liệu có kiểu tại biên** (Pydantic v2) và **(2) cấu hình tập trung, được validate**
> (`pydantic-settings`). Đây chính là *hai viên gạch* mà FastAPI (tuần 2) đứng lên trên:
> FormRequest→Pydantic model, `env` config→Settings. Hết ngày, hardened client của bạn sẽ
> **nhận `Settings` và trả về Pydantic model**, không còn `dict` mù kiểu.

## Mục tiêu cuối ngày (Definition of Done)
- [ ] Đọc `Lesson.md` (P1 dataclass · P2 Pydantic v2 · P3 pydantic-settings · P4 cầu nối FastAPI).
- [ ] Điền cheat-sheet **dataclass vs Pydantic vs Laravel (DTO/FormRequest/Eloquent)** trong `Notes.md`.
- [ ] Trả lời **8-question test** cho `PYDANTIC` và `SETTINGS/CONFIG` trong `Notes.md`.
- [ ] `exercises/ex1_dataclass.py` — chuyển một class PHP/Laravel → `@dataclass` (frozen, `slots`, `default_factory`, `__post_init__`); mypy sạch.
- [ ] `exercises/ex2_pydantic_models.py` — `ChatMessage` / `ChatRequest` / `Usage` với `Field` constraints + `field_validator` / `model_validator`; parse dict "bẩn" từ ngoài; `model_dump_json`.
- [ ] `exercises/ex3_settings.py` — `Settings` đọc từ `.env`/env, `SecretStr`, nested settings, validate lúc khởi động (fail-fast).
- [ ] `exercises/ex4_typed_client.py` — refactor client Day 2: **nhận `Settings`**, **trả `ChatResponse`/`Usage`** (Pydantic), validate response phòng thủ (bug Day 2: HTTP 200 + body lỗi).
- [ ] Điền bảng **"khi nào dataclass, khi nào Pydantic"** trong `Notes.md`.
- [ ] `mypy --strict` sạch trên cả 4 exercises; `ruff check` sạch.
- [ ] 1 git commit (xem `GitCommit.md`).
- [ ] Điền `Architecture.md` (mini-ADR: validate-at-the-boundary + centralized settings) và `Reflection.md`.

## Cấu trúc thư mục ngày
- `Lesson.md` — lý thuyết (P1 dataclass · P2 Pydantic v2 · P3 settings · P4 vì sao Pydantic là *lingua franca* của AI code).
- `Notes.md` — cheat-sheet + 8-Q test (Pydantic, Settings) + bảng chọn dataclass/Pydantic (bạn điền).
- `exercises/` — 4 bài stub có `TODO` — **bạn tự hoàn thành**.
- `.env.example` — mẫu biến môi trường cho `ex3`/`ex4` (copy sang `.env`, KHÔNG commit `.env`).
- `Interview.md` — câu hỏi phỏng vấn + chỗ trả lời.
- `Resources.md` — link tài liệu gốc (Pydantic v2, dataclasses, pydantic-settings).
- `Architecture.md` — mini-ADR: vì sao validate tại biên + settings tập trung.
- `Reflection.md` — nhật ký cuối ngày.
- `GitCommit.md` — hướng dẫn commit.

## Chuẩn bị môi trường (một lần)
Trong repo `llm-microservice`, thêm deps:
```bash
uv add pydantic pydantic-settings
```
Copy env mẫu: `cp exercises/../.env.example .env` rồi điền `OPENROUTER_API_KEY`.
(`.env` đã nằm trong `.gitignore` từ Day 1 — kiểm tra lại.)

## Quy tắc
Ngày chỉ hoàn thành khi bạn gõ **`Day 3 completed`**. Không mở khoá ngày sau sớm. Không skip.
