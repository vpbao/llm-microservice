# Production Generative AI Engineer — 8-Month Roadmap
## Part 1: Overall Roadmap, Philosophy, Technology Stack, Skill Matrix

> **Candidate:** Backend Developer (PHP / Laravel, ~5 yrs) → **Target:** Production Generative AI Engineer / AI Backend Engineer
> **Duration:** 32 weeks · **Start:** Monday, 27 July 2026 · **End:** Sunday, 7 March 2027
> **Study budget:** Mon–Fri 19:00–22:00 (15h) + Sat 09:00–12:00 & 14:00–18:00 (7h) + Sun 09:00–12:00 & 14:00–17:00 (6h) = **~28h/week**
> **Primary cloud:** AWS · **Primary language:** Python 3.13+ · **Salary target:** $4k–$6k/mo

---

## 0. How to read this program

This is **Part 1 of 9**. It gives you the map. The later parts drill into 4-week blocks with day-by-day schedules, projects, and interview drills.

> **Read `Part-0-Professional-Development-Track.md` alongside this.** Part 0 is the senior-engineering overlay that runs through all 8 months — Portfolio, ADRs, AI System Design, Technical Writing, curated Reading, Interview Prep, and a continuous Production Mindset, at a ~20% theory / 80% implementation ratio. Every week and month below is governed by that overlay.

```
Part 0  →  Professional Development Track overlay (portfolio, ADR, system design, writing, reading, interview, prod mindset)
Part 1  →  Overall roadmap, philosophy, tech stack, skill matrix, month-by-month   ← YOU ARE HERE
Part 2  →  Weeks 1–4    (Month 1: Python/FastAPI foundations + LLM basics)
Part 3  →  Weeks 5–8    (Month 2: Prompting, structured output, first RAG)
Part 4  →  Weeks 9–12   (Month 3: Production RAG + vector DBs + evaluation)
Part 5  →  Weeks 13–16  (Month 4: Agents + LangGraph + tool use)
Part 6  →  Weeks 17–20  (Month 5: Multi-agent + AI search + Bedrock production)
Part 7  →  Weeks 21–24  (Month 6: LLMOps, observability, guardrails, security)
Part 8  →  Weeks 25–28  (Month 7: Scaling, cost/latency optimization, capstone build)
Part 9  →  Weeks 29–32  (Month 8: Capstone finish, portfolio polish, interview prep)
Finale  →  Portfolio review, mock-interview roadmap, system-design roadmap,
           production-readiness checklist, job-application checklist
```

**Confirm Part 1 and I'll generate Part 2.**

---

## 1. Learning Philosophy

You already know software engineering. That is your unfair advantage. Most people entering GenAI come from data science and struggle with production; you come from production and need to learn the AI layer. This roadmap is built around that asymmetry.

**Five operating principles**

1. **First principles over frameworks.** You will implement retrieval, chunking, and a mini agent loop *by hand* before touching LlamaIndex or LangGraph. When you later use a framework, you will know exactly what it hides — which is the difference between a $2k/mo prompt-plumber and a $6k/mo engineer.

2. **Every topic passes the 8-question test.** For each concept you learn, you must be able to answer: (1) Why do we need it? (2) What problem does it solve? (3) How does it work internally? (4) When to use it? (5) When *not* to use it? (6) Common interview questions? (7) Beginner mistakes? (8) How is it used in production? If you can't answer all eight, you haven't learned it. Later parts embed these prompts per week.

3. **Build, don't collect.** No tutorial is "done" until you've shipped a running artifact — a container, an endpoint, a deployed service, or a documented repo. Reading counts only as input to building.

4. **Production is the product.** A RAG that works in a notebook is a demo. A RAG with tracing, evals, cost caps, guardrails, caching, CI/CD, and a rollback plan is an engineering deliverable. We optimize for the second from Month 3 onward.

5. **Leverage the transfer.** You already understand REST, MVC, DI, DB design, caching, queues, auth, Docker, and CI/CD. We map every new AI concept onto something you know (e.g. "an embedding index is a specialized read-optimized store; treat it like a search replica"). Throughout, I flag **Laravel → FastAPI** analogues so you move fast.

**Anti-patterns we explicitly avoid:** YouTube hopping, course collecting, "learning LangChain" as a goal, memorizing API signatures, and building toy chatbots with no evaluation or observability.

**The 20/80 rule (from Part 0).** Roughly 20% of your hours are theory and reading; ~80% are hands-on building. A concept is only "learned" once it exists as running code, an ADR, a design doc, or a shipped project. Theory earns its place by unblocking a build — never as an end in itself.

**The parallel Professional Development Track (Part 0).** From Week 1, every project is a production portfolio project (11-point spec + repo checklist); after each major project you write an **ADR**; from Month 2 you do one **AI System Design** exercise per month; every month you publish one **technical article** and complete a **curated reading set** (1 paper, 2 doc deep dives, 2 eng blogs, 1 repo, 1 case study); every week has an **interview-prep block** and every month a **mock senior interview**; and a 13-point **production mindset** (cost, latency, observability, evaluation, security, guardrails, prompt/model versioning, experiment tracking, CI/CD, deployment, monitoring, incident response) is threaded throughout. This is what turns "can build AI" into "can be hired as a Production/Senior/Platform GenAI Engineer."

---

## 2. What "Production Generative AI Engineer" actually means

The job is **80% software/platform engineering, 20% ML intuition**. You are not training models. You are building reliable, observable, cost-bounded systems *around* models. Concretely, the market expects you to:

- Design and ship **Enterprise RAG** and **AI search** that survive real corpora (messy PDFs, tables, permissions, multi-tenant).
- Build **agents** and **multi-agent workflows** with tool use, memory, and human-in-the-loop.
- Run **LLMOps**: prompt/model versioning, evaluation pipelines, CI/CD for AI, canary/rollback.
- Own **observability**: tracing (spans per LLM/tool call), metrics (latency, tokens, cost, quality), dashboards, alerting.
- Enforce **guardrails & security**: prompt-injection defense, PII handling, output validation, access control, jailbreak resistance.
- Optimize **cost and latency**: caching, batching, routing, model selection, streaming, quantized/open-source fallbacks.
- Deploy on **AWS**: Bedrock, ECS/Fargate, Lambda, API Gateway, S3, CloudWatch, IAM, Secrets Manager, SQS/SNS/EventBridge.

That is the target profile. Every phase below builds one slice of it.

---

## 3. High-Level Roadmap (the 8-phase arc)

| Phase | Weeks | Theme | You can build by the end |
|------|-------|-------|--------------------------|
| **P1 Foundations** | 1–4 | Python/FastAPI for AI engineers, async, Pydantic, clean architecture; LLM mental model | A typed, async FastAPI service that streams LLM completions with structured output |
| **P2 LLM Craft** | 5–8 | Prompting, structured output, function/tool calling, tokenization, context, cost; naive RAG from scratch | A "chat-with-your-PDF" service — but hand-built retrieval, so you understand every step |
| **P3 Production RAG** | 9–12 | Chunking strategies, embeddings, vector DBs (Qdrant), hybrid search (BM25+vector), reranking, RAG evaluation (RAGAS) | Enterprise RAG with hybrid retrieval, reranking, and an automated eval suite |
| **P4 Agents** | 13–16 | Agent loop internals, LangGraph, tool use, state, memory, human-in-the-loop, retries | A LangGraph agent that plans, calls tools, self-corrects, and is fully traced |
| **P5 Multi-Agent & AI Search** | 17–20 | Orchestration patterns, supervisor/worker, AI search platform, Bedrock in production | A multi-agent research/copilot system running on Bedrock |
| **P6 LLMOps & Observability** | 21–24 | Tracing (LangSmith/Phoenix/OTel), metrics (Prometheus/Grafana), guardrails, security, prompt/model versioning | A fully instrumented AI platform: dashboards, evals-in-CI, guardrails, alerting |
| **P7 Scale & Optimize** | 25–28 | Latency/cost optimization, caching, routing, load, K8s basics, open-source model serving; capstone build | A cost- and latency-optimized system with a documented SLO and load test |
| **P8 Portfolio & Interview** | 29–32 | Capstone finish, portfolio polish, system design, mock interviews, job applications | 8-project portfolio + interview-ready + applications out |

**Cadence built in to prevent burnout:** every 4th week (Weeks 4, 8, 12, 16, 20, 24, 28, 32) is a lighter **consolidation week** — project hardening, review, buffer for catch-up, and interview drilling rather than new theory. Sunday evenings (16:00–17:00) are always review + planning, never new material.

---

## 4. Technology Roadmap — trade-offs & learning order

For each category: the **learning order**, the **primary** to master, and the **why**. You asked for trade-offs and a recommended sequence — this is the decision layer of the roadmap.

### 4.1 Language & backend
Python 3.13+, `asyncio`, FastAPI, Pydantic v2, SQLAlchemy 2.0 (async), Alembic, pytest, Redis, PostgreSQL. **Learn in this order:** modern Python idioms & typing → Pydantic → async → FastAPI → SQLAlchemy/Alembic → pytest.

**Laravel → Python map (quick reference):**

| Laravel / PHP | Python / FastAPI | Notes |
|---|---|---|
| Composer | uv / pip + pyproject | `uv` is the modern, fast choice — use it |
| Artisan | Typer / custom CLI | |
| Eloquent ORM | SQLAlchemy 2.0 | More explicit; you control sessions |
| Migrations | Alembic | Autogenerate from models |
| Form Request validation | Pydantic models | Pydantic is *everywhere* in AI code |
| Service container / DI | FastAPI `Depends` | Constructor-style DI via callables |
| Queues (Horizon) | Celery / ARQ / SQS workers | ARQ pairs well with async |
| Middleware | FastAPI middleware / dependencies | |
| PHPUnit | pytest | Fixtures replace setUp/tearDown |

### 4.2 LLM providers — learning order & when to use each
1. **OpenAI API** (learn first) — cleanest SDK, best docs, fastest feedback loop for learning prompting, function calling, structured outputs.
2. **Anthropic Claude API** — strong tool use, long context, great for agents; learn the differences vs OpenAI.
3. **AWS Bedrock** (**production focus**) — this is where you'll deploy for enterprise. Unified access to Claude, Llama, Titan, etc., with IAM, VPC, private networking, and CloudWatch integration.
4. **Open-source (Llama, Qwen, Mistral, Gemma)** — for cost control, data residency, and self-hosting; you'll serve one with vLLM in Phase 7.

**Trade-off / recommendation:** *Learn on OpenAI, ship on Bedrock.* OpenAI gives the tightest learning loop; Bedrock is what enterprises on AWS actually run. Treat provider choice as a config concern — build a thin abstraction so you can swap.

### 4.3 AI frameworks — learning order
1. **OpenAI SDK / raw HTTP first** — no framework. Implement retrieval and an agent loop by hand.
2. **PydanticAI** — typed, minimal, production-friendly; great bridge from raw SDK to structured agents.
3. **LangGraph** (**primary agent framework**) — graph-based, explicit state, durable, supports human-in-the-loop and cycles.
4. **LlamaIndex** (**primary RAG framework**) — best-in-class ingestion, indexing, and retrieval abstractions.
5. **LangChain** — learn *only enough* to read others' code and understand the ecosystem; not a primary tool.

**Trade-off — LangChain vs LangGraph:** LangChain's chain abstraction hides control flow and is hard to debug in production; LangGraph makes state and transitions explicit (like a state machine you can trace, checkpoint, and resume). **Recommendation: skip building on core LangChain; go raw → PydanticAI → LangGraph.** Interviewers increasingly ask *why LangGraph over LangChain* — you'll have a real answer.

### 4.4 Vector databases — learning order
1. **Qdrant** (**primary**) — Rust-based, excellent filtering, hybrid search, easy Docker local dev, generous OSS, scales to managed cloud.
2. **Milvus** — heavier, high-scale, GPU options; learn the architecture (segments, indexes).
3. **FAISS** — library, not a DB; learn it to understand ANN indexes (IVF, HNSW, PQ) from first principles.
4. **pgvector** — Postgres extension; you already know Postgres — great "when do I *not* need a dedicated vector DB" answer.
5. **Pinecone** — comparison only; fully managed, simple, but proprietary and pricier.

**Trade-off / recommendation:** **Start with Qdrant.** Understand ANN via FAISS. Know pgvector as the pragmatic default for small/medium corpora already in Postgres. Interview answer for "when NOT to use a vector DB": small corpora, exact-match needs, or when pgvector suffices and you want one fewer system.

### 4.5 Embeddings, reranking, evaluation, observability, deployment
- **Embeddings — learn order:** OpenAI `text-embedding-3` → BGE / E5 (open-source, self-host) → Voyage AI (retrieval-tuned) → Amazon Titan (Bedrock-native for production). Key concept: dimensionality, normalization, domain fit, cost.
- **Reranking:** BGE Reranker (open-source cross-encoder) → Cohere Rerank (managed). Concept: bi-encoder retrieval + cross-encoder rerank = the standard production recipe.
- **Evaluation:** RAGAS (RAG metrics: faithfulness, context precision/recall, answer relevancy) → DeepEval (unit-test style, CI-friendly) → LangSmith (traces + datasets + eval) → TruLens. You will make evals a first-class deliverable from Phase 3.
- **Observability:** LangSmith (LLM-native tracing) + Phoenix/Arize (OSS tracing & eval) + OpenTelemetry (vendor-neutral spans) → Prometheus (metrics) + Grafana (dashboards). Concept: a trace = a tree of spans across LLM/retrieval/tool calls.
- **Deployment (AWS):** Docker & Compose → ECR (registry) → ECS/Fargate (primary runtime) → API Gateway + Lambda (event/low-traffic) → Kubernetes (fundamentals only, EKS awareness). Supporting: S3, CloudWatch, IAM, Secrets Manager, SQS/SNS/EventBridge.

### 4.6 The "golden path" stack you'll converge on
> **FastAPI + Pydantic** service → **LlamaIndex** ingestion → **Qdrant** hybrid retrieval → **BGE/Cohere** rerank → **Bedrock (Claude/Titan)** generation → **LangGraph** agents → **LangSmith/Phoenix + OTel/Prometheus/Grafana** observability → **RAGAS/DeepEval** in CI → **ECS/Fargate** deploy, **CloudWatch** ops.

---

## 5. Month-by-Month Roadmap (with real dates)

Each month = 4 weeks. Dates below anchor the whole program.

### Month 1 — Foundations · 27 Jul → 23 Aug 2026 (Weeks 1–4)
**Focus:** Python-for-AI-engineers, async, Pydantic, FastAPI clean architecture; LLM mental model, tokens, first API calls, streaming, structured output.
**Project:** *Streaming LLM microservice* — typed async FastAPI service with structured outputs, cost logging, and tests.
**Milestone:** You can stand up a production-shaped AI service and explain the request lifecycle end to end.

### Month 2 — LLM Craft & Naive RAG · 24 Aug → 20 Sep 2026 (Weeks 5–8)
**Focus:** Prompt engineering, function/tool calling, context management, tokenization deep-dive, cost/latency basics; **build retrieval by hand** (no framework).
**Project:** *Chat-with-your-PDF (from scratch)* — manual chunking, embeddings, cosine search, prompt assembly, citations.
**Milestone:** You understand every moving part of RAG because you built it without a framework.

### Month 3 — Production RAG · 21 Sep → 18 Oct 2026 (Weeks 9–12)
**Focus:** Chunking strategies (fixed, recursive, semantic), embeddings selection, **Qdrant**, **hybrid search (BM25 + vector)**, **reranking**, RAG evaluation with **RAGAS**, LlamaIndex.
**Project:** *Enterprise RAG* — hybrid retrieval + rerank + eval suite + metadata filtering + multi-tenant awareness.
**Milestone:** You can design a RAG that survives a messy real corpus and prove its quality with numbers.

### Month 4 — Agents · 19 Oct → 15 Nov 2026 (Weeks 13–16)
**Focus:** Agent loop internals (ReAct, plan-execute), tool use, state & memory, retries/error handling, human-in-the-loop; **LangGraph** and **PydanticAI**.
**Project:** *Tool-using agent* — a LangGraph agent that plans, calls tools (search, DB, calculator, your RAG), self-corrects, and is fully traced.
**Milestone:** You can build a reliable, debuggable agent and explain why LangGraph over LangChain.

### Month 5 — Multi-Agent, AI Search & Bedrock · 16 Nov → 13 Dec 2026 (Weeks 17–20)
**Focus:** Orchestration patterns (supervisor/worker, router, hierarchical), multi-agent trade-offs, AI search platform design; **AWS Bedrock** in production (IAM, guardrails, knowledge bases, provisioned throughput).
**Project:** *Multi-agent research copilot on Bedrock* — supervisor delegates to specialist agents; deployed on AWS.
**Milestone:** You can decide *when multi-agent helps vs hurts* and ship on Bedrock.

### Month 6 — LLMOps, Observability, Guardrails & Security · 14 Dec 2026 → 10 Jan 2027 (Weeks 21–24)
**Focus:** Tracing (LangSmith/Phoenix/OTel), metrics (Prometheus/Grafana), prompt & model versioning, evals-in-CI, guardrails, prompt-injection & jailbreak defense, PII/secret handling, access control.
**Project:** *AI platform instrumentation* — turn a prior project into a fully observed, guarded, CI-evaluated service.
**Milestone:** You can operate an AI system: see it, measure it, protect it, and roll it back.
> *Note: this month spans the holidays — Weeks 21–22 are intentionally lighter; catch up or rest.*

### Month 7 — Scale, Cost & Latency + Capstone Build · 11 Jan → 7 Feb 2027 (Weeks 25–28)
**Focus:** Latency optimization (streaming, parallel tool calls, speculative retrieval), cost optimization (caching, routing, model selection), semantic caching, load testing, K8s fundamentals, serving open-source models with vLLM; **start capstone**.
**Project:** *Capstone (build)* — your flagship system, designed for SLOs and cost caps, load-tested.
**Milestone:** You can take a system from "works" to "works at scale, on budget."

### Month 8 — Portfolio, System Design & Interviews · 8 Feb → 7 Mar 2027 (Weeks 29–32)
**Focus:** Finish capstone, polish all 8 repos (READMEs, architecture diagrams, deploy, monitoring, evals), AI system-design drills, mock interviews, resume, and applications.
**Project:** *Portfolio finalization* + applications submitted.
**Milestone:** Interview-ready with a portfolio that demonstrates production capability; applying to $4k–$6k/mo roles.

---

## 6. Portfolio Overview (8 projects, increasing difficulty)

Full specs (architecture, folder structure, stack, deployment, monitoring, evaluation, README, extensions) arrive with each phase. Preview:

1. **Streaming LLM Microservice** (P1) — typed async FastAPI, structured output, cost logging.
2. **Chat-with-your-PDF, hand-built** (P2) — RAG from scratch, citations.
3. **Enterprise RAG** (P3) — hybrid + rerank + RAGAS evals + multi-tenant.
4. **Tool-Using Agent** (P4) — LangGraph, traced, self-correcting.
5. **Multi-Agent Research Copilot** (P5) — supervisor/worker on Bedrock.
6. **AI Search Platform** (P5/6) — hybrid search service with ranking + analytics.
7. **Observed & Guarded AI Platform** (P6) — tracing, metrics, guardrails, evals-in-CI.
8. **Capstone: Enterprise AI Copilot** (P7/8) — the flagship combining RAG + agents + LLMOps + AWS deploy + SLOs.

---

## 7. Skill Matrix

Legend: ⬜ none · 🟡 aware · 🟢 working · 🔵 production-ready. Target column is where you should be by Week 32.

### 7.1 Software & backend (leverage your existing strength)
| Skill | Start | Target | Reaches target by |
|---|---|---|---|
| Modern Python (typing, idioms) | 🟡 | 🔵 | Month 1 |
| Async / asyncio | ⬜ | 🔵 | Month 1 |
| FastAPI + Pydantic | ⬜ | 🔵 | Month 1 |
| SQLAlchemy 2.0 + Alembic | ⬜ | 🟢 | Month 2 |
| pytest / testing AI code | 🟡 | 🔵 | Month 3 |
| Clean architecture / DI / SOLID in Python | 🟢 | 🔵 | Month 2 |
| Docker / Compose | 🟢 | 🔵 | Month 1 |

### 7.2 LLM & GenAI core
| Skill | Start | Target | Reaches target by |
|---|---|---|---|
| LLM mental model, tokens, context | ⬜ | 🔵 | Month 1 |
| Prompt engineering | ⬜ | 🔵 | Month 2 |
| Structured output / function calling | ⬜ | 🔵 | Month 2 |
| Embeddings & similarity | ⬜ | 🔵 | Month 3 |
| Chunking strategies | ⬜ | 🔵 | Month 3 |
| Hybrid search (BM25 + vector) | ⬜ | 🔵 | Month 3 |
| Reranking | ⬜ | 🔵 | Month 3 |
| RAG evaluation (RAGAS/DeepEval) | ⬜ | 🔵 | Month 3 |

### 7.3 Agents & orchestration
| Skill | Start | Target | Reaches target by |
|---|---|---|---|
| Agent loop internals (ReAct) | ⬜ | 🔵 | Month 4 |
| Tool use / function calling in agents | ⬜ | 🔵 | Month 4 |
| LangGraph (state, cycles, HITL) | ⬜ | 🔵 | Month 4 |
| Memory & state management | ⬜ | 🟢 | Month 4 |
| Multi-agent orchestration | ⬜ | 🔵 | Month 5 |
| AI search platform design | ⬜ | 🟢 | Month 5 |

### 7.4 LLMOps, observability & production
| Skill | Start | Target | Reaches target by |
|---|---|---|---|
| Tracing (LangSmith/Phoenix/OTel) | ⬜ | 🔵 | Month 6 |
| Metrics (Prometheus/Grafana) | 🟡 | 🔵 | Month 6 |
| Prompt & model versioning | ⬜ | 🔵 | Month 6 |
| Evals in CI/CD | ⬜ | 🔵 | Month 6 |
| Guardrails & output validation | ⬜ | 🔵 | Month 6 |
| Security (prompt injection, PII, access) | 🟡 | 🔵 | Month 6 |
| Cost optimization (caching, routing) | ⬜ | 🔵 | Month 7 |
| Latency optimization | ⬜ | 🔵 | Month 7 |
| Load testing & SLOs | 🟡 | 🟢 | Month 7 |

### 7.5 AWS & cloud
| Skill | Start | Target | Reaches target by |
|---|---|---|---|
| Bedrock (models, guardrails, KB) | ⬜ | 🔵 | Month 5 |
| ECS/Fargate + ECR | 🟡 | 🔵 | Month 5 |
| Lambda + API Gateway | 🟡 | 🟢 | Month 6 |
| S3 / CloudWatch / IAM / Secrets Mgr | 🟡 | 🔵 | Month 6 |
| SQS/SNS/EventBridge | 🟡 | 🟢 | Month 6 |
| Kubernetes/EKS (fundamentals) | ⬜ | 🟡 | Month 7 |
| Serving OSS models (vLLM) | ⬜ | 🟢 | Month 7 |

### 7.6 Career
| Skill | Start | Target | Reaches target by |
|---|---|---|---|
| AI system design interviews | ⬜ | 🔵 | Month 8 |
| Portfolio & READMEs | 🟢 | 🔵 | Month 8 |
| Behavioral / storytelling | 🟡 | 🟢 | Month 8 |
| Job applications & outreach | 🟡 | 🟢 | Month 8 |

---

## 8. Weekly Rhythm (the template every week follows)

Full daily timetables come per-phase, but the shape is constant:

- **Mon–Fri 19:00–22:00** — block A theory (19:00–20:00), block B hands-on (20:00–21:00), block C practice/notes (21:00–22:00).
- **Sat 09:00–12:00** — deep project work; **14:00–18:00** — project + reading.
- **Sun 09:00–12:00** — project hardening / stretch topic; **14:00–16:00** — interview drills; **16:00–17:00** — weekly review + plan next week (never new material).
- **Every 4th week** — consolidation: no new theory, harden projects, catch up, drill interviews.

Each week's deliverables always include: running code committed to GitHub, notes answering the 8-question test, and the week's **interview-prep block** (questions + follow-ups + a practical scenario + common mistakes + a whiteboard topic — per Part 0).

**Monthly deliverables (per Part 0 overlay), in addition to the phase project:**
- One **ADR** after the month's major project (`docs/adr/ADR-00X.md`) ending with "how I'd defend this in an interview."
- From Month 2: one **AI System Design** exercise (`design/`, 7-part spec).
- One **published technical article** derived from the month's work.
- The month's **curated reading set** completed and logged in `reading-log.md`.
- One **mock senior AI-engineer interview** on the consolidation-week Sunday.
- Repo(s) advanced against the **GitHub repository checklist**; production-mindset status stated per project.

---

*End of Part 1. Reply "continue" or "Part 2" and I'll generate Weeks 1–4 in full detail (daily schedule, resources, project spec, interview questions, common mistakes, production best practices, and the end-of-week review).*
