# Part 0 — Professional Development Track (Overlay)
### The senior-engineering layer that runs through all 8 months

> **Read this once, then apply it every week.** This overlay does not replace anything in Parts 1–9. It upgrades the standard week/month templates so that *every* week produces portfolio value, and by Month 8 you have the artifacts a hiring committee for a **Production AI / AI Platform / Senior GenAI Engineer** role actually looks for: production-grade repos, ADRs, system-design fluency, public technical writing, and interview reps.
>
> **Core ratio: ~20% theory / 80% implementation.** A concept is not "done" until it exists as running code, an ADR, a design doc, or a shipped project. Theory earns its place only by unblocking a build.

---

## Why this overlay exists (mentor's note)

Learning the AI stack gets you to "can build." What gets you *hired at $4–6k/mo and past a senior loop* is proving you can **decide, operate, and communicate**: justify architecture choices (ADRs), reason about systems you haven't built yet (system design), run things in production (the production-mindset checklist), and explain your work publicly (technical writing). Those are separable skills from framework knowledge, and most self-taught engineers skip them. This track makes them non-optional and spreads them across the 8 months so they compound.

---

## The 7 tracks at a glance

| # | Track | Cadence | Primary artifact | Interview payoff |
|---|-------|---------|------------------|------------------|
| 1 | **Portfolio** | Every project | Production-grade repo (11-point spec) | "Show me something you built" |
| 2 | **ADR** | After each major project | `docs/adr/ADR-00X.md` | Senior "why did you choose X over Y" |
| 3 | **AI System Design** | 1 per month, from Month 2 | `design/` doc (7-part spec) | System-design interview round |
| 4 | **Technical Writing** | 1 article per month | Public post (blog/dev.to/LinkedIn) | Signal of depth + communication |
| 5 | **Reading** | Curated set per month | Reading log + notes | Depth in follow-up questions |
| 6 | **Interview Prep** | Weekly + monthly mock | Answer bank + mock recordings | The loop itself |
| 7 | **Production Mindset** | Continuous, every week | Checklist applied to each project | "How would this run in prod?" |

---

## Track 1 — Portfolio (every project is production-grade)

Every project in this program is treated as a **production portfolio project**, not an exercise. Each one ships with this 11-point spec (delivered in the project's README + `docs/`):

1. **Project goals** — the problem, the user, the success criteria (measurable).
2. **Architecture diagram** — components + data flow (Mermaid in-repo, or Excalidraw PNG committed).
3. **Folder structure** — clean architecture; documented in README.
4. **Design decisions** — the key choices and why (links to the ADRs).
5. **Technology trade-offs** — alternatives considered and rejected, with reasoning.
6. **Deployment guide** — reproducible steps; local (Docker Compose) + AWS (ECS/Fargate or Lambda) where applicable.
7. **Monitoring strategy** — what you log/trace/measure; dashboards; alerts.
8. **Evaluation strategy** — how you prove it works (metrics, datasets, eval-in-CI from Month 3 on).
9. **README requirements** — see checklist below.
10. **Future improvements** — honest "what I'd do next / at scale."
11. **GitHub repository checklist** — see below.

### README requirements (every repo)
Title + one-line pitch · problem & goals · architecture diagram · tech stack + trade-offs · quickstart (one command) · configuration/env · API examples (curl/screenshots) · testing & how to run · evaluation results (numbers) · monitoring/observability notes · deployment guide · design decisions (link ADRs) · future improvements · license.

### GitHub repository checklist (per project)
- [ ] Clear README (all items above)
- [ ] `docs/adr/` with the project's ADR(s)
- [ ] `design/` doc if the project maps to that month's system-design exercise
- [ ] Architecture diagram committed (Mermaid/PNG)
- [ ] `.env.example`; **no secrets committed** (verify with a secret scanner)
- [ ] Dockerfile + `docker-compose.yml`
- [ ] Tests + CI (GitHub Actions: lint, type, test; evals-in-CI from Month 3)
- [ ] Conventional commits + meaningful history
- [ ] Tagged release (`vX.Y`)
- [ ] `LICENSE`, `.gitignore`, `pyproject.toml` pinned deps
- [ ] Issues/roadmap section for "future improvements"
- [ ] (Month 6+) observability wired: traces + metrics + dashboard screenshot in README

**Target by Week 32: 7–8 repos that each pass this checklist.** Two smaller projects (P5+P6 in Month 5) may be combined or kept separate; aim for 7 strong repos minimum, 8 ideal.

---

## Track 2 — Architecture Decision Records (ADRs)

After each major project you write at least one ADR. Format is short and standardized (this is how real senior teams work). Template:

```markdown
# ADR-00X: <decision title>
Date: YYYY-MM-DD · Status: Accepted | Superseded by ADR-00Y

## Context
The forces at play: requirements, constraints, what problem forced a decision.

## Options considered
- Option A — pros / cons
- Option B — pros / cons
- Option C — pros / cons

## Decision
What we chose and the single most important reason.

## Consequences
What becomes easier, what becomes harder, what we now accept as a cost,
and what would make us revisit this (the "trigger to supersede").
```

**ADR schedule (one line each — you write the full doc):**

| ADR | Month | Core question(s) |
|-----|-------|------------------|
| ADR-001 | 1 | Why FastAPI (not Django/Flask)? Why AsyncIO? Why Pydantic + a provider abstraction? |
| ADR-002 | 2 | Why build RAG from scratch before a framework? Which embedding model and why? |
| ADR-003 | 3 | Why Qdrant (not Pinecone/pgvector)? Why hybrid (BM25+vector)? Why add reranking? |
| ADR-004 | 4 | Why LangGraph (not LangChain)? Why PydanticAI for typed agents? |
| ADR-005 | 5 | Why AWS Bedrock (not direct OpenAI)? When multi-agent (not a single agent)? |
| ADR-006 | 6 | Which observability stack (LangSmith vs Phoenix vs OTel) and why? Guardrails approach? |
| ADR-007 | 7 | Caching + model-routing strategy? Self-hosted vLLM vs managed inference? |
| ADR-008 | 8 | Capstone-wide retrospective ADR: the 3 decisions you'd defend hardest in a loop. |

Each ADR must end with a **"how I'd defend this in an interview"** paragraph. That's the whole point.

---

## Track 3 — AI System Design (one per month, from Month 2)

One design exercise per month, written as a `design/` doc, using this 7-part spec (the same structure senior system-design interviews expect):

1. **Functional requirements** — what it must do (user stories, scope, out-of-scope).
2. **Non-functional requirements** — latency targets (p50/p95, time-to-first-token), throughput/QPS, availability, accuracy/quality bar, data freshness, tenancy, compliance.
3. **Architecture** — components, data flow, storage, retrieval/generation path, sync vs async, queues, caches.
4. **Trade-offs** — the 3–4 pivotal decisions and alternatives.
5. **Scaling strategy** — how it grows 10×/100× (retrieval, embeddings, LLM concurrency, DB sharding, caching layers).
6. **Cost considerations** — token cost model, caching savings, model routing, where money leaks, budget guardrails.
7. **Failure scenarios** — LLM timeout/outage, provider rate limits, bad retrieval, hallucination, poison inputs, prompt injection; degradation and fallback strategy.

**System-design schedule:**

| Month | Exercise |
|-------|----------|
| 2 | Enterprise PDF RAG |
| 3 | AI Search Platform |
| 4 | Internal Knowledge Assistant (RAG + agent) |
| 5 | Multi-Agent Workflow / research copilot |
| 6 | AI Copilot (with guardrails, evals, observability) |
| 7 | Enterprise AI Platform (multi-tenant, LLMOps) |
| 8 | Full mock system-design (pick one, whiteboard end-to-end under time) |

Do each one **before** you finish that month's project when possible — designing then building cements the reasoning.

---

## Track 4 — Technical Writing (one article per month)

Publish one article/month (dev.to, Medium, LinkedIn, or a personal blog — pick one and stick to it). Length 800–1,500 words, code + a diagram, written for a mid-level engineer. Each article is derived from that month's project + ADR + reading, so it costs little extra time and doubles as interview storytelling prep.

| Month | Working title |
|-------|---------------|
| 1 | Building my first streaming LLM API (FastAPI + SSE + cost logging) |
| 2 | I built RAG from scratch (no framework) — here's what actually happens |
| 3 | Hybrid retrieval explained: BM25 + vectors + reranking, and why pure vector search underperforms |
| 4 | AI agent architecture: the loop, LangGraph, and why not LangChain |
| 5 | When multi-agent helps (and when it just adds latency and cost) |
| 6 | LLM evaluation & observability in production: traces, metrics, and evals-in-CI |
| 7 | Cutting LLM cost and latency: caching, routing, and self-hosting trade-offs |
| 8 | What I learned building production GenAI systems in 8 months (+ capstone case study) |

**Rule:** if you can't explain it in an article, you don't understand it well enough to be asked about it in an interview.

---

## Track 5 — Reading (curated, not random)

Each month: **1 research paper · 2 official-doc deep dives · 2 engineering blog posts · 1 GitHub repo to study · 1 production case study.** Keep a `reading-log.md` with a 3–5 sentence takeaway per item. Prioritize primary sources over tutorials.

**Month 1 — Foundations**
- Paper: *Attention Is All You Need* (Vaswani et al., 2017) — build the transformer intuition.
- Docs deep dive: FastAPI (async, dependencies, streaming) · Pydantic v2 (models, validators, settings).
- Blogs: an async-vs-sync FastAPI performance write-up · OpenAI "Structured Outputs" guide/blog.
- Repo: `fastapi/full-stack-fastapi-template` (production project shape).
- Case study: an LLM-gateway/proxy engineering post (how a team fronts LLM providers behind one API).

**Month 2 — LLM craft & naive RAG**
- Paper: *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (Lewis et al., 2020).
- Docs: OpenAI text-generation + embeddings guides · Anthropic Messages & tool-use.
- Blogs: Chip Huyen "Building LLM applications for production" · Eugene Yan on patterns for LLM systems.
- Repo: `openai/openai-cookbook` (embeddings + RAG notebooks).
- Case study: a "chat with your docs" production write-up (chunking/citation lessons).

**Month 3 — Production RAG**
- Paper: *Dense Passage Retrieval* (Karpukhin et al., 2020) **or** *Lost in the Middle* (Liu et al., 2023).
- Docs: Qdrant (collections, filtering, hybrid) · LlamaIndex (ingestion, indexes, retrievers).
- Blogs: Pinecone/Qdrant "learn" pieces on hybrid search & reranking · a RAGAS/eval walkthrough.
- Repo: `qdrant/qdrant` + `run-llama/llama_index` (read retrieval internals).
- Case study: an enterprise RAG post-mortem (why naive RAG failed on real data).

**Month 4 — Agents**
- Paper: *ReAct: Synergizing Reasoning and Acting in LLMs* (Yao et al., 2022).
- Docs: LangGraph (state, cycles, checkpoints, human-in-the-loop) · PydanticAI.
- Blogs: Anthropic "Building effective agents" · a LangGraph-vs-LangChain teardown.
- Repo: `langchain-ai/langgraph` (examples) .
- Case study: a production agent write-up (tool use, retries, guardrails, cost).

**Month 5 — Multi-agent, AI search, Bedrock**
- Paper: a multi-agent collaboration paper (e.g., *AutoGen* or *Self-Refine*).
- Docs: AWS Bedrock (models, guardrails, knowledge bases, provisioned throughput) · Bedrock Agents.
- Blogs: an "AI search at scale" post (e.g., Vespa/hybrid ranking) · a multi-agent orchestration write-up.
- Repo: a supervisor/worker multi-agent example repo.
- Case study: an enterprise copilot/search launch (LinkedIn "Musings on building a GenAI product").

**Month 6 — LLMOps, observability, guardrails, security**
- Paper: a RAG/agent **evaluation** paper (e.g., *RAGAS* or *Self-RAG*).
- Docs: LangSmith (tracing, datasets, evals) · OpenTelemetry GenAI semantic conventions.
- Blogs: Hamel Husain on LLM evals · an OWASP LLM Top-10 / prompt-injection write-up.
- Repo: `Arize-ai/phoenix` (OSS tracing + eval).
- Case study: a production incident/observability post for an LLM system.

**Month 7 — Scale, cost, latency**
- Paper: *Efficient Memory Management for LLM Serving with PagedAttention* (vLLM).
- Docs: vLLM · AWS (ECS/Fargate autoscaling, CloudWatch, cost) .
- Blogs: a semantic-caching write-up · an LLM cost-optimization case (routing/model-tiering).
- Repo: `vllm-project/vllm`.
- Case study: a company's "how we cut LLM cost/latency by N%" post.

**Month 8 — Consolidation & interview**
- Paper: re-read your single most relevant paper for the capstone and critique it.
- Docs: revisit the 2 docs most central to your capstone.
- Blogs: 2 senior-interview / system-design-for-LLM prep posts.
- Repo: study one repo similar to your capstone; note what they did better.
- Case study: a hiring/interview retrospective from a GenAI engineer.

---

## Track 6 — Interview Preparation (weekly + monthly)

**Every week** (already in the per-week template) now explicitly includes:
- **Interview questions** — core concept checks.
- **Follow-up questions** — the "and why / what if" second layer that separates senior from mid.
- **Practical scenarios** — "your RAG returns wrong answers 20% of the time — debug it."
- **Common mistakes** — what beginners get wrong (and what you'll be probed on).
- **Whiteboard discussion topics** — 1–2 things to sketch and explain out loud.

**Every month:** one **mock senior AI-engineer interview** (Sunday of the consolidation week, ~90 min): 20 min behavioral/story, 30 min deep technical on the month's topics, 40 min system design (that month's exercise). Record yourself or do it with a peer. Keep an answer bank you refine each month. Month 8 runs a **full loop** (behavioral + coding + technical + system design + your project walkthrough).

---

## Track 7 — Production Mindset (continuous)

These 13 concerns are threaded through every week from now on. Each project must state where it stands on each (even "not applicable yet, here's why"). The month column shows where each becomes a **first-class deliverable**, but awareness starts Week 1.

| Concern | Seeded | First-class | How it shows up |
|---|---|---|---|
| Cost optimization | Wk1 (token/cost logging) | Month 7 | per-request cost, caching, routing, budgets |
| Latency optimization | Wk2 (streaming) | Month 7 | TTFT, streaming, parallel tools, p95 targets |
| Observability | Wk3 (request logging) | Month 6 | traces (spans), metrics, dashboards, alerts |
| Evaluation | Month 3 | Month 6 | RAGAS/DeepEval, datasets, evals-in-CI |
| Security | Wk1 (secrets) | Month 6 | secrets mgmt, PII, access control |
| Guardrails | Month 4 | Month 6 | input/output validation, injection defense |
| Prompt versioning | Month 2 | Month 6 | prompts in code/registry, diffable, tested |
| Model versioning | Month 5 | Month 6 | pinned models, changelog, eval before switch |
| Experiment tracking | Month 3 | Month 6 | eval runs, datasets, comparisons over time |
| CI/CD | Month 1 | Month 6 | lint/type/test + evals as gates |
| Production deployment | Month 1 | Month 5 | Docker → ECS/Fargate/Lambda on AWS |
| Monitoring | Month 3 | Month 6 | CloudWatch/Prometheus/Grafana, SLOs, alerts |
| Incident response | Month 6 | Month 7 | runbooks, fallbacks, rollback, post-mortems |

**Weekly habit:** end each week by asking of whatever you built — *"If this were serving real traffic tonight, what breaks, what costs too much, and what can't I see?"* Write the answer in your review.

---

## Upgraded WEEKLY template (applies to Parts 3–9; retrofitted to 1–2)

Every week now contains, in this order:
1. Learning objectives · 2. Theory (~20%) · 3. Official documentation · 4. Reading (this week's slice of the monthly set) · 5. Coding exercises · 6. Hands-on project (~80%) · 7. Deliverables · 8. GitHub milestones · 9. **Interview prep block** (questions + follow-ups + practical scenario + common mistakes + whiteboard topic) · 10. Common mistakes · 11. Production best practices (+ the weekly production-mindset question) · 12. End-of-week review.

## Upgraded MONTHLY template
Milestone checklist · skill assessment · portfolio progress (repo checklist status) · **ADR written** · **system-design exercise delivered** (Months 2–8) · **technical article published** · **reading set completed + logged** · **mock interview done** · suggested improvements.

---

*This overlay governs Parts 3–9. Parts 1 and 2 have been retrofitted to match. Keep `reading-log.md`, `docs/adr/`, `design/`, and your article drafts in the same **Production Generative AI Engineer** folder so the portfolio assembles itself.*
