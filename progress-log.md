# Progress Log — Production Generative AI Engineer

**Mentor:** Principal AI Engineer / Tech Lead
**Rule:** A day is complete only when you type `Day X completed`. No lesson is unlocked early. No day is skipped.

---

## Current position
- **Month:** 1 — Foundations (Python/FastAPI for AI + LLM mental model)
- **Week:** 1 (27 Jul → 2 Aug 2026)
- **Day:** Day 4 — NOT STARTED (next; Week 2 opener — async Python + FastAPI + Pydantic v2 → streaming service skeleton)
- **Current project:** Project 1 — Streaming LLM Microservice (`llm-microservice`)
- **Current milestone:** M1 — stand up a production-shaped AI service; explain the LLM request lifecycle end to end
- **Completed days:** 3
- **Remaining days in Month 1:** ~22 study days (Weeks 1–4)

---

## Day ledger
| Day | Date | Topic | Status | Confidence (1–5) | Deliverable |
|-----|------|-------|--------|------------------|-------------|
| 1 | Mon 27 Jul 2026 | Modern Python typing for AI engineers → LLM mental model | ✅ completed | 4 | Repo scaffolded (uv/ruff/mypy strict/pytest/pre-commit); 4 exercises; `hello_llm.py` (token usage via OpenRouter); Notes 8-Q test; 2 commits |
| 2 | Tue 28 Jul 2026 | Idioms deep-dive (comprehensions, generators, decorators) + first API calls hardened | ✅ completed | 4 | 4 exercises tự code, `mypy --strict` + `ruff` sạch: ex1 comprehensions (list/dict/set/genexpr), ex2 decorators (`@timed`/`@retry` backoff+jitter/`@log_usage`, `functools.wraps`, off-by-one, unreachable-raise), ex3 generator pipeline (`yield`/`yield from`, buffer aliasing), ex4 hardened httpx client (Timeout, reused Client, `_classify` taxonomy Transient/Permanent, retry loop, `cost_usd`, usage log). Notes 8-Q (generator+decorator) + taxonomy + run-data. Reflection ghi bug thật OpenRouter 200+error-body. 1 commit (`feat: harden LLM client`). |
| 3 | Wed 29 Jul 2026 | Dataclass vs Pydantic v2 + config/settings (pydantic-settings) — bridge to FastAPI | ✅ completed | — | 4 exercises tự code, `mypy --strict` + `ruff` sạch: ex1 dataclass (frozen/slots/default_factory/__post_init__ + demo chứng minh dataclass KHÔNG validate runtime → lỗi nổ muộn), ex2 Pydantic v2 models (ChatMessage/ChatRequest/Usage, Field constraints, `field_validator` vs `model_validator`, `extra="forbid"`, coercion "0.5"→float, ValidationError gom mọi lỗi), ex3 pydantic-settings (env_prefix, SecretStr, fail-fast, `@lru_cache` get_settings), ex4 typed client (DI Settings, trả ChatResponse có kiểu, validate provider body → ĐÓNG bug Day 2 200+error-body, nối taxonomy Transient/Permanent; gọi thật thành công). Notes: cheat-sheet + decision table + 2×8-Q + bảng v1→v2. Architecture mini-ADR (validate-at-boundary + centralized settings). Fix tooling: mypy/ruff vào đúng venv, pyright/LSP trỏ venv. 1 commit. |

*(Rows are added as each day is unlocked. Status: pending → in-progress → completed.)*

---

## Standing reminders
- Weekdays: 3h (19:00–22:00). Sat/Sun: longer blocks. Sunday = weekly review, not a normal lesson.
- Every day ends with a real deliverable: code + notes + git commit + README/ADR touch.
- 20% theory / 80% build.
- Folder per day: `Month X/Week X/Day X/` with README, Lesson, Notes, Exercise.py, MiniProject, Resources, Interview, Reflection, Architecture, GitCommit.
