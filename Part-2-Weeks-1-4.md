# Part 2 — Weeks 1–4 · Month 1: Foundations
### Python/FastAPI for AI Engineers + LLM Mental Model

> **Dates:** Mon 27 Jul 2026 → Sun 23 Aug 2026
> **Month goal:** Stand up a production-shaped, typed, async AI microservice and be able to explain an LLM request lifecycle end to end.
> **Month project:** *Streaming LLM Microservice* — a typed async FastAPI service that streams completions, enforces structured output, logs tokens/cost, and is tested + containerized.
> **Assumption:** You already know REST, MVC, DI, DB design, caching, queues, auth, Docker, architecture. We are **not** teaching programming — we're teaching Python idioms + the AI layer.

---

## How this month is structured

- **Week 1** — Modern Python for engineers who already code (typing, idioms, tooling) + LLM mental model & first API calls.
- **Week 2** — Async Python + FastAPI + Pydantic v2; build the service skeleton with streaming.
- **Week 3** — Structured output, function calling, cost/token accounting, SQLAlchemy/Alembic logging, pytest.
- **Week 4** — **Consolidation week:** harden, containerize, document, test, and drill interviews. No new theory.

Each week follows the same 12-part template (now including the Part 0 interview-prep block and production-mindset question). Daily blocks are concrete; adapt times ±30 min as life requires. Never skip the Sunday 16:00–17:00 review.

> **Professional Development Track (Part 0) for Month 1:** Project 1 is built to the 11-point portfolio spec + repo checklist · **ADR-001** after Project 1 · **Article:** "Building my first streaming LLM API" · **Reading set** logged · **Mock interview #1** in Week 4 · production-mindset seeded (cost/token logging Wk1, streaming/latency Wk2, request logging/observability Wk3, secrets/security Wk1, CI/CD + deployment Wk4). *System-design track begins Month 2.*

---
---

# WEEK 1 · 27 Jul → 2 Aug 2026
### Modern Python for AI engineers + LLM mental model

### 1. Learning objectives
By Sunday you can: (a) write idiomatic, fully type-hinted modern Python and run `uv`, `ruff`, `mypy`; (b) explain what an LLM is at inference time — tokens, context window, sampling, why it's stateless; (c) make your first OpenAI + Anthropic API calls and reason about tokens and cost.

### 2. Theory
- **Python-for-a-backend-dev delta:** type hints (`list[str]`, `dict`, `Optional`, `|`), dataclasses vs Pydantic, comprehensions, generators/iterators, context managers, `with`, decorators, packaging with `pyproject.toml`, virtual envs, the import system. Map each to a PHP/Laravel equivalent so you learn the *difference*, not the basics.
- **LLM mental model (first principles):** a transformer LLM is a function `tokens → probability distribution over next token`. Everything else — chat, RAG, agents — is scaffolding around repeated next-token prediction. Key concepts: **tokenization** (subword, BPE), **context window** (the model sees only what you send — it has no memory between calls), **sampling** (temperature, top-p, greedy), **logprobs**, **system/user/assistant roles**, **why the model is stateless** (you resend history every turn), and **cost = f(input tokens + output tokens)**.

### 3. Official documentation (primary sources — read these, not blog rehashes)
- Python typing: docs.python.org `typing` module; `mypy` docs.
- `uv` (Astral) docs; `ruff` docs.
- OpenAI API reference — Chat Completions & Responses API; "Text generation" guide; tokenizer explainer (tiktoken).
- Anthropic docs — Messages API; "Get started"; prompt basics.

### 4. Reading materials
- *Fluent Python* (Ramalho), ch. 1–2, 5 (data model, functions as objects) — skim, you're not a beginner.
- Anthropic "Building effective agents" (read intro now, revisit Month 4).
- Andrej Karpathy "Let's build the GPT tokenizer" (video) — watch for tokenization intuition.
- OpenAI cookbook: "How to count tokens with tiktoken".

### 5. Coding exercises
1. Convert a small PHP/Laravel class you know into idiomatic typed Python (dataclass + methods). Run `mypy --strict`.
2. Write a generator that streams lines from a file; write a context manager for a timer.
3. `tiktoken` exercise: count tokens for 5 sample texts; verify cost math by hand against the model's price sheet.
4. Hit the OpenAI Chat Completions endpoint with raw `httpx` (no SDK) once, then with the SDK — compare.

### 6. Hands-on project (kickoff)
Create the repo `llm-microservice`. `uv init`, add `ruff`, `mypy`, `pytest`, `pre-commit`. Write a throwaway script `scripts/hello_llm.py` that sends a prompt to OpenAI and Anthropic and prints the response + token usage. This proves your environment and keys work.

### 7. Deliverables
- Repo scaffolded with tooling and `pyproject.toml`.
- `hello_llm.py` printing responses + token counts from both providers.
- Notes file answering the 8-question test for "tokens" and "context window".

### 8. GitHub milestones
- `chore: scaffold project (uv, ruff, mypy, pytest, pre-commit)`
- `feat: first LLM calls (OpenAI + Anthropic) with token accounting`

### 9. Interview questions
- What is a token? Why does token count (not character count) drive cost and latency?
- What is a context window and what happens when you exceed it?
- Why are LLMs described as stateless? How does a chat "remember" earlier turns?
- Temperature vs top-p — what do they control and when do you set temperature to 0?
- What are logprobs and one production use for them?

**Follow-ups:** "You send a 50-page doc every turn — what's the cost and latency impact, and how would you fix it?" · "Temperature 0 doesn't fully guarantee determinism — why not?"
**Practical scenario:** A teammate says "the model forgot what I told it earlier." Diagnose and explain what's really happening.
**Whiteboard topic:** Sketch the lifecycle of one chat request from HTTP in → tokens → model → tokens out → cost logged.

### 10. Common mistakes
Confusing characters with tokens; assuming the model remembers previous requests; leaving temperature at default for tasks needing determinism; hardcoding API keys (use env + Secrets Manager later); using `requests` (sync) instead of async clients in an async service.

### 11. Production best practices
Keys in environment variables now, AWS Secrets Manager later — never in code. Log token usage on every call from day one. Pin dependencies. Enable `ruff` + `mypy` in pre-commit so quality is enforced automatically.

### 12. End-of-week review (Sun 16:00–17:00)
Can you explain, without notes, the lifecycle of one chat request? Did you commit working code? Fill the review checklist (end of Part 2). Set Week 2's top 3 goals.

---

# WEEK 2 · 3 Aug → 9 Aug 2026
### Async Python + FastAPI + Pydantic v2 → streaming service skeleton

### 1. Learning objectives
Explain the async event loop and when async helps (I/O-bound, like LLM calls) vs when it doesn't (CPU-bound). Build a FastAPI service with Pydantic v2 request/response models and a **streaming** endpoint (SSE) that proxies an LLM.

### 2. Theory
- **asyncio:** event loop, coroutines, `async`/`await`, `asyncio.gather`, `TaskGroup`, cancellation, timeouts, `async with`, `async for`. **Why it matters for AI:** LLM calls are long, I/O-bound network waits; async lets one worker handle many concurrent streams. Contrast with Laravel's mostly-sync request model + queues.
- **FastAPI:** path/query/body params, dependency injection via `Depends`, lifespan events, background tasks, middleware, exception handlers, `StreamingResponse` / SSE. Laravel→FastAPI map: FormRequest→Pydantic, service container→`Depends`, middleware→middleware, resource→response_model.
- **Pydantic v2:** models, validators, `Field`, settings management (`pydantic-settings`), serialization; why Pydantic is the lingua franca of AI code (structured output, tool schemas, config).
- **Streaming:** server-sent events, chunked transfer, backpressure, why streaming improves perceived latency (time-to-first-token).

### 3. Official documentation
- FastAPI docs (whole "Tutorial - User Guide", plus "Advanced" → streaming, lifespan, dependencies).
- Pydantic v2 docs (Models, Validators, Settings).
- Python `asyncio` docs (high-level API).
- OpenAI/Anthropic streaming guides.
- Uvicorn docs.

### 4. Reading materials
- FastAPI author's talks/notes on async; "async vs sync in FastAPI" section.
- *Architecture Patterns with Python* (Percival & Gregory) — ch. on service layer & DI (skim; maps to what you know from Laravel).
- Real Python: "Async IO in Python" primer.

### 5. Coding exercises
1. Write an async function that fans out 10 LLM calls with `asyncio.gather` and one with `TaskGroup`; add a per-call timeout.
2. Build a `/health` and `/echo` FastAPI endpoint with Pydantic models; add a dependency that injects a settings object.
3. Implement an SSE endpoint that streams a hardcoded token list with delays; then wire it to a real streamed LLM response.

### 6. Hands-on project
Turn the scaffold into a real service: `POST /v1/chat` (non-streaming) and `POST /v1/chat/stream` (SSE). Config via `pydantic-settings` (provider, model, keys). Dependency-injected provider client. Clean architecture: `api/` (routers), `domain/` (models, interfaces), `services/` (LLM client abstraction), `core/` (config, logging). One provider interface, OpenAI implementation first.

### 7. Deliverables
- Running FastAPI service with streaming + non-streaming chat endpoints.
- Provider abstraction (interface + OpenAI impl) — swappable by config.
- `curl` and README examples showing streaming works.

### 8. GitHub milestones
- `feat: FastAPI skeleton with clean architecture + settings`
- `feat: streaming chat endpoint (SSE) over provider abstraction`

### 9. Interview questions
- When does async improve throughput and when does it do nothing? Why are LLM calls the ideal async workload?
- What problem does streaming (SSE) solve for LLM UX? What is time-to-first-token?
- How does FastAPI dependency injection work, and how would you inject a mock LLM client in tests?
- Why Pydantic over plain dataclasses in an AI service?
- What happens if a client disconnects mid-stream — how do you handle cancellation?

**Follow-ups:** "One route does a heavy sync JSON parse — what happens to your other concurrent streams?" · "How many concurrent LLM streams can one Uvicorn worker realistically handle, and what limits it?"
**Practical scenario:** Under load, p95 latency spikes and some requests hang forever. Where do you look first?
**Whiteboard topic:** Draw the FastAPI service layers (api/domain/services/core) and show where the provider interface is injected.

### 10. Common mistakes
Blocking the event loop with sync SDK calls or CPU work inside async routes; forgetting to handle client disconnects; putting business logic in routers; not setting timeouts; using Pydantic v1 patterns in v2.

### 11. Production best practices
One provider interface so OpenAI/Anthropic/Bedrock are swappable. Structured JSON logging with a request/correlation ID. Timeouts + graceful cancellation on every LLM call. Lifespan-managed HTTP client (reuse connections). Separate settings per environment.

### 12. End-of-week review (Sun 16:00–17:00)
Demo your streaming endpoint. Explain async trade-offs aloud. Checklist + next-week goals.

---

# WEEK 3 · 10 Aug → 16 Aug 2026
### Structured output, function calling, cost accounting, persistence, testing

### 1. Learning objectives
Force models to return schema-valid JSON (Pydantic) reliably; understand function/tool calling mechanics; persist every request with token/cost accounting via async SQLAlchemy + Alembic; write real tests for AI code (including mocking the LLM).

### 2. Theory
- **Structured output:** JSON mode vs strict schema / tool-calling for structured data; why free-text parsing is fragile; validation + retry-on-invalid loops; Pydantic as the schema source of truth.
- **Function / tool calling:** how the model is given tool schemas, emits a tool-call request, you execute, and feed results back; this is the seed of agents (Month 4). Understand it now at the API level.
- **Cost & token accounting:** input vs output token pricing, why output is usually pricier, prompt-caching basics, per-request cost computation, budgets/limits.
- **Persistence:** async SQLAlchemy 2.0 sessions, models, Alembic migrations. Laravel→map: Eloquent→SQLAlchemy, migrations→Alembic. Store: request, model, tokens, cost, latency, status.
- **Testing AI code:** deterministic tests by mocking the provider; contract tests for the provider interface; testing streaming; `pytest` fixtures, `pytest-asyncio`, `httpx.AsyncClient` for endpoint tests; recorded/VCR-style fixtures.

### 3. Official documentation
- OpenAI "Structured Outputs" + "Function calling" guides; Anthropic "Tool use".
- Pydantic validators & JSON schema generation.
- SQLAlchemy 2.0 async ORM docs; Alembic docs.
- pytest + pytest-asyncio docs; HTTPX testing.

### 4. Reading materials
- Instructor library docs (Pydantic-based structured output) — read to see the pattern; you'll hand-roll it first.
- OpenAI cookbook: structured outputs & function calling examples.
- "Testing FastAPI applications" (FastAPI docs section).

### 5. Coding exercises
1. Define a Pydantic `ExtractionResult`; get the model to return it via strict/tool calling; add a retry loop that re-prompts on validation failure.
2. Implement one tool (`get_current_time` or a fake `search`) and run a full tool-call round trip manually.
3. Compute per-request cost from usage + a price table; assert it in a test.
4. Add an async SQLAlchemy `RequestLog` model + Alembic migration; write a repository with a fake for tests.

### 6. Hands-on project
Add to the service: (a) `POST /v1/extract` returning schema-validated JSON with retry-on-invalid; (b) a demo tool-calling endpoint; (c) persist every call to Postgres with tokens, cost, latency, status via a repository; (d) test suite mocking the LLM (unit) + endpoint tests (integration) reaching ~70%+ coverage on core logic.

### 7. Deliverables
- Structured-output endpoint with validation + retry.
- Tool-calling demo endpoint.
- Postgres logging of every request (tokens/cost/latency) via Alembic-migrated schema.
- Passing pytest suite with mocked provider.

### 8. GitHub milestones
- `feat: structured output with schema validation + retry`
- `feat: request logging (tokens/cost/latency) via async SQLAlchemy + Alembic`
- `test: unit + integration tests with mocked LLM`

### 9. Interview questions
- How do you get reliable JSON from an LLM? Compare JSON mode vs strict/tool-based structured output.
- Walk through a function-calling round trip. How is it different from an "agent"?
- Why is output token cost usually higher than input, and how do you budget a request?
- How do you unit-test code that calls a non-deterministic LLM?
- What's prompt caching and when does it save real money?

**Follow-ups:** "The model returns valid JSON but with a hallucinated enum value — how do you catch it?" · "Your retry loop occasionally loops forever — how do you bound it and what do you log?"
**Practical scenario:** Finance asks why last month's LLM bill tripled. You have per-request token/cost logs — how do you find the cause?
**Whiteboard topic:** Sketch the structured-output flow: prompt + schema → model → validate → (repair/retry) → persist usage.

### 10. Common mistakes
Parsing free-text with regex instead of using structured output; no retry/repair on invalid JSON; not recording token usage (flying blind on cost); tests that hit the real API (slow, flaky, expensive); mixing sync and async DB sessions.

### 11. Production best practices
Schema-validate every model output before it leaves your service. Record tokens/cost/latency/status for every call (foundation for observability in Month 6). Mock the LLM in CI; never call real APIs in unit tests. Migrations version-controlled via Alembic. Add per-request and per-day cost guards.

### 12. End-of-week review (Sun 16:00–17:00)
Show the extract endpoint returning valid JSON and the DB rows with cost. Explain function calling aloud. Checklist + goals.

---

# WEEK 4 · 17 Aug → 23 Aug 2026  ·  🔵 CONSOLIDATION WEEK
### Harden, containerize, document, test, interview-drill (no new theory)

### 1. Learning objectives
Ship Project 1 as a portfolio-grade artifact: containerized, documented, CI-tested, with a clear README and architecture diagram. Consolidate Month 1 and rehearse interviews.

### 2–5. Focus (consolidation, so lighter theory)
- **Containerize:** multi-stage Dockerfile, `docker-compose` with Postgres + the app; `.env.example`; healthcheck.
- **CI/CD:** GitHub Actions running ruff + mypy + pytest on push; build the image.
- **Docs:** README with architecture, setup, API examples, design decisions; a diagram (Excalidraw/Mermaid) of the request flow.
- **Refactor:** apply SOLID/clean-architecture pass; remove dead code; tighten types to `mypy --strict`.
- **Reading:** re-read your Month-1 notes; skim the two weakest topics from the 8-question test and fix gaps.

### 6. Hands-on project (finalize Project 1)
**Streaming LLM Microservice — v1.0.** Endpoints: chat (stream + non-stream), extract (structured), tool-call demo. Provider abstraction (OpenAI now, Bedrock-ready interface). Postgres request logging with cost. Tests + CI green. Dockerized. README + diagram.

### 7. Deliverables
- Tagged `v1.0` release on GitHub (passing the Part 0 **GitHub repository checklist**).
- Green CI badge; Dockerized; one-command `docker compose up`.
- README + architecture diagram + design-decisions section (Part 0 **11-point portfolio spec**).
- **ADR-001 written** (`docs/adr/ADR-001.md`): Why FastAPI (not Django/Flask)? Why AsyncIO? Why Pydantic + a provider abstraction? End with "how I'd defend this in an interview."
- **Technical article published:** "Building my first streaming LLM API (FastAPI + SSE + cost logging)."
- **Month-1 reading set logged** in `reading-log.md` (see Part 0, Month 1 list).
- **Mock interview #1 done** (Sunday of Week 4; see below).

### 8. GitHub milestones
- `ci: GitHub Actions (lint, type, test, build)`
- `docs: README + architecture diagram`
- `chore: dockerize + compose (app + postgres)`
- `release: v1.0`

### 9. Interview prep — Mock Interview #1 (Sunday, ~90 min)
Run a full mock (per Part 0, Track 6): **20 min behavioral** (tell your career-change story; why GenAI; walk through Project 1) · **30 min technical** (rapid-fire all Week 1–3 questions + their follow-ups) · **40 min system design — warm-up:** *Design a minimal multi-provider LLM proxy/gateway service.* Cover: layers/clean architecture, swappable providers, streaming (SSE, TTFT), timeouts & cancellation, cost/token accounting, request logging, failure handling & fallbacks, and how you'd add rate limits and caching. Record yourself; save answers to your interview answer bank. **Follow-ups to expect:** "What breaks under 10× traffic?" "Where does cost leak?" "How do you make this observable?" "How would you A/B two models safely?"

### 10. Common mistakes
Skipping the README/diagram (recruiters read these first); no CI; secrets committed; giant single-file app; no cost logging. Fix all before tagging v1.0.

### 11. Production best practices
Reproducible builds; healthchecks; env-based config; CI gates; a documented rollback (`git tag` + image tag). This is the baseline every later project inherits.

### 12. End-of-month review
Complete the Month 1 milestone checklist below.

---
---

## Daily schedule (repeats each week; Week 4 swaps "new theory" for hardening)

**Weekdays (Mon–Fri) — 19:00–22:00**
| Time | Block | Activity |
|---|---|---|
| 19:00–20:00 | A · Theory | Read the day's official docs / watch a focused video; take notes against the 8-question test |
| 20:00–21:00 | B · Hands-on | Coding exercises + project work for the current week |
| 21:00–22:00 | C · Practice & notes | Refactor, write tests, commit, and log what you learned |

**Saturday**
| Time | Activity |
|---|---|
| 09:00–12:00 | Deep project work (biggest feature of the week) |
| 14:00–16:00 | Project work continued |
| 16:00–18:00 | Reading (books/papers) + answer this week's interview questions in writing |

**Sunday**
| Time | Activity |
|---|---|
| 09:00–12:00 | Project hardening / stretch topic / catch-up |
| 14:00–16:00 | Interview drills (say answers out loud; whiteboard the design) |
| 16:00–17:00 | **Weekly review + plan next week (no new material)** |

### Concrete example — Monday 27 Jul 2026
- 19:00–20:00 — Read Python `typing` docs + `uv`/`ruff` quickstart; note 5 PHP→Python differences.
- 20:00–21:00 — `uv init` the repo; add tooling; write the first typed module.
- 21:00–22:00 — Commit scaffold; jot notes on "what is a token".

---

## Resources for Month 1 (consolidated)
**Curated reading set (Part 0 format — complete all and log in `reading-log.md`):**
- **1 paper:** *Attention Is All You Need* (Vaswani et al., 2017).
- **2 doc deep dives:** FastAPI (async, dependencies, streaming) · Pydantic v2 (models, validators, settings).
- **2 eng blogs:** an async-vs-sync FastAPI performance write-up · OpenAI "Structured Outputs" guide.
- **1 repo to study:** `fastapi/full-stack-fastapi-template`.
- **1 case study:** an LLM-gateway/proxy engineering post (fronting providers behind one API).

**Supporting docs (reference as needed):** Python asyncio, SQLAlchemy 2.0, Alembic, pytest, OpenAI API, Anthropic API, uv, ruff, Uvicorn.
**Books:** *Fluent Python* (selected chapters), *Architecture Patterns with Python* (service layer/DI chapters).
**Videos:** Karpathy "Let's build the GPT tokenizer"; one solid FastAPI async crash course (pick one, don't hop).
**Do NOT** start LangChain/LlamaIndex yet — frameworks come after you've built by hand.

---

## Weekly review checklist (use every Sunday 16:00–17:00)
- [ ] Did I hit this week's 3 top goals? If not, why?
- [ ] Can I answer all of this week's interview questions out loud, unaided?
- [ ] Did I commit working code every study day?
- [ ] For each new concept, can I answer the 8-question test?
- [ ] What are my 2 biggest knowledge gaps right now?
- [ ] What are next week's top 3 goals?
- [ ] Am I on pace, ahead, or behind? Do I need to use a buffer slot?
- [ ] **Production-mindset question (Part 0):** if what I built this week served real traffic tonight, what breaks, what costs too much, and what can't I see?
- [ ] Energy/burnout check: sustainable? Adjust if not.

---
---

## END OF MONTH 1 — Assessment

### Milestone checklist
- [ ] Idiomatic, fully typed modern Python; `uv`/`ruff`/`mypy --strict` clean.
- [ ] Explain LLM inference: tokens, context window, statelessness, sampling, cost.
- [ ] Async FastAPI service with streaming (SSE) + non-streaming chat.
- [ ] Reliable structured output (Pydantic) with validation + retry.
- [ ] Function/tool calling round trip understood and demoed.
- [ ] Every request logged with tokens/cost/latency to Postgres (Alembic).
- [ ] Provider abstraction (OpenAI now, Bedrock-ready).
- [ ] Tests (mocked LLM) + green CI + Docker + README + diagram.
- [ ] **Project 1 (Streaming LLM Microservice) tagged v1.0** (passes Part 0 repo checklist).

**Professional Development Track — Month 1 (Part 0):**
- [ ] **ADR-001** written (FastAPI / AsyncIO / Pydantic + provider abstraction) with interview-defense paragraph.
- [ ] **Technical article published:** "Building my first streaming LLM API."
- [ ] **Reading set** (paper + 2 docs + 2 blogs + 1 repo + 1 case study) completed and logged.
- [ ] **Mock interview #1** completed and answers banked.
- [ ] **Production-mindset status** stated for Project 1 (which of the 13 concerns are covered vs deferred, and why).
- [ ] Note: **System Design track starts Month 2** — no design exercise required this month.

### Skill assessment (rate yourself 1–5; target ≥4 to advance comfortably)
Modern Python & typing · asyncio · FastAPI · Pydantic v2 · SQLAlchemy/Alembic · pytest/mocking AI · LLM mental model · structured output · function calling · cost/token accounting · Docker/CI. If any core item is <3, use a Week-4 buffer slot or a Sunday morning to shore it up before Month 2.

### Portfolio progress
**1 of 8 complete.** Project 1 demonstrates: production service shape, streaming, structured output, cost logging, tests, CI, containerization. This is your "I can build real services" proof and the base every later project extends.

### Suggested improvements (optional stretch if ahead)
- Add Anthropic + a stub Bedrock implementation behind the same interface.
- Add a simple per-API-key rate limit and a daily cost cap.
- Add request/response JSON logging with correlation IDs (pre-work for Month 6 observability).
- Add a `/metrics`-style token/cost counter (pre-work for Prometheus later).

---

*End of Part 2. Reply "Part 3" for Weeks 5–8 (Month 2: prompting, tool calling depth, and your first hand-built RAG — "chat-with-your-PDF" from scratch).*
