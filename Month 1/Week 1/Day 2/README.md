# Day 2 — Idioms deep-dive (comprehensions · generators · decorators) + first API calls **hardened**

**Date:** Tue 28 Jul 2026 · **Week 1 / Month 1** · **Project:** `llm-microservice`
**Mode:** Mentor + tự code (bạn tự viết code trong stub, mentor giảng + review)

> Hôm qua bạn đã *chạm* vào comprehension/generator/decorator và gọi API lần đầu.
> Hôm nay ta **đào sâu 3 idiom đó** cho tới mức phản xạ, rồi **làm cứng (harden)** lời gọi
> API kiểu production: timeout, retry + backoff, phân loại lỗi, tái dùng connection, và
> log token/cost. Đây là bộ khung mọi ngày sau kế thừa.

## Mục tiêu cuối ngày (Definition of Done)
- [ ] Đọc `Lesson.md` (Phần 1 idioms + Phần 2 hardening), điền cheat-sheet PHP→Python vào `Notes.md`.
- [ ] Trả lời được **8-question test** cho `GENERATOR` và `DECORATOR` trong `Notes.md`.
- [ ] `exercises/ex1_comprehensions.py` — chuyển loop/`array_map`/`array_filter` → comprehension; mypy sạch.
- [ ] `exercises/ex2_decorators.py` — tự viết `@timed`, `@retry(...)`, `@log_usage`; dùng `functools.wraps`.
- [ ] `exercises/ex3_generator_pipeline.py` — pipeline lazy (read → clean → chunk) + mô phỏng stream token.
- [ ] `exercises/ex4_hardened_client.py` — bọc lời gọi httpx của Day 1 bằng timeout + retry + error taxonomy + usage log.
- [ ] Điền bảng **error taxonomy** (retry vs không retry) trong `Notes.md`.
- [ ] `mypy --strict` sạch trên cả 4 exercises; `ruff check` sạch.
- [ ] 1 git commit (xem `GitCommit.md`).
- [ ] Điền `Reflection.md`.

## Cấu trúc thư mục ngày
- `Lesson.md` — lý thuyết (Phần 1 idioms, Phần 2 hardening).
- `Notes.md` — cheat-sheet idioms + 8-Q test (generator, decorator) + error taxonomy (bạn điền).
- `exercises/` — 4 bài stub có `TODO` — **bạn tự hoàn thành**.
- `Interview.md` — câu hỏi phỏng vấn + chỗ trả lời.
- `Resources.md` — link tài liệu gốc.
- `Architecture.md` — ghi chú thiết kế: vì sao timeout + retry ở tầng client (mini-ADR).
- `Reflection.md` — nhật ký cuối ngày.
- `GitCommit.md` — hướng dẫn commit.

## Quy tắc
Ngày chỉ hoàn thành khi bạn gõ **`Day 2 completed`**. Không mở khoá ngày sau sớm.
