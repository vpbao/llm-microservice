# Finale — Portfolio Review · Mock-Interview Roadmap · System-Design Roadmap · Production-Readiness · Job-Application Checklist

> Use this after Month 8 (or reference throughout). Everything here converts 8 months of building into offers.

---

## 1. Final Portfolio Review

**Target: 7–8 production-grade repos**, each passing the Part 0 GitHub checklist, telling one story: *a senior backend engineer who became a Production GenAI engineer.*

| # | Project | Proves | Must-have artifacts |
|---|---------|--------|---------------------|
| 1 | Streaming LLM Microservice | Production service shape, streaming, structured output, cost logging | README(11), tests, CI, Docker, ADR-001 |
| 2 | Chat-with-your-PDF (hand-built RAG) | RAG from first principles, citations | README(11), golden-set eval, ADR-002 |
| 3 | Enterprise RAG | Hybrid + rerank + **evals-in-CI**, multi-tenant | README(11), RAGAS numbers, ADR-003, design-02 |
| 4 | Tool-using Agent (LangGraph) | Agent loop, tools, memory, tracing, guardrails | README(11), agent-eval, ADR-004, design-03 |
| 5 | Multi-agent Research Copilot (Bedrock) | Orchestration + AWS production | README(11), deployed, ADR-005, design-04 |
| 6 | AI Search Platform | Query understanding, ranking, analytics | README(11), relevance numbers |
| 7 | Observed & Guarded AI Platform | Tracing, metrics, guardrails, security, runbook | README(11), dashboards, ADR-006, design-05 |
| 8 | **Capstone: Enterprise AI Copilot** | Everything, at scale, on budget, deployed | README(11)+case study+demo, SLOs, load test, ADR-007/008, design-06 |

**Portfolio index page** (repo or one-pager) links: each project (with a one-line pitch + architecture thumbnail), the 8 articles, the 8 ADRs, and the 6 design docs + cheat-sheet.

**Reviewer's rubric — each repo scores itself on:** clarity of README · architecture diagram present · decisions defensible (ADR) · quality proven with numbers (evals) · deployable (Docker + AWS) · observable (traces/metrics) · secure (no secrets, least privilege) · honest "future improvements." Any repo below bar gets a polish pass before you apply.

---

## 2. Mock-Interview Roadmap

You did **8 monthly mocks** (Months 1–8). This is the recurring loop to keep sharp while applying.

**Weekly during job search (2–3h):**
- 1 timed system-design (40 min) from the design bank + a fresh prompt.
- 1 technical deep-dive (30 min): rotate RAG / agents / LLMOps / cost-latency.
- 1 coding round (30–45 min): Python/async, data structures, a small LLM-integration task.
- 5 behavioral stories rehearsed (STAR), rotating.

**The full-loop simulation (do before real onsites):** behavioral (30) → coding (45) → LLM/GenAI technical (45) → system design (45) → project deep-dive (30). Record, self-score, note two fixes.

**Question banks:** pull from every Part's interview-prep blocks (each has questions + follow-ups + scenarios). Maintain a living **answer bank** — one crisp answer + one "here's how I did it in project X" per question.

**Behavioral core stories to have ready:** the career pivot (why GenAI, why now) · hardest technical problem you solved · a trade-off/decision you owned (cite an ADR) · a time you were wrong and corrected · shipping under ambiguity/pressure · working with non-technical stakeholders.

---

## 3. System-Design Roadmap

**Method (always, in order):** clarify **functional requirements** → pin **non-functional requirements** (p50/p95, TTFT, QPS, availability, accuracy bar, tenancy, compliance, budget) → sketch **architecture** (ingestion, retrieval, generation, agents, storage, cache, gateway) → call out **trade-offs** (3–4 pivotal) → **scaling** (10×/100×) → **cost** (token model, caching, routing, budgets) → **failure scenarios** (timeouts, outages, bad retrieval, hallucination, injection, cost runaway) + graceful degradation.

**Reference architectures to know cold** (from your design docs 1–6): Enterprise PDF RAG · AI Search Platform · Internal Knowledge Assistant (RAG+agent) · Multi-Agent Workflow · AI Copilot · Enterprise AI Platform (multi-tenant).

**Practice prompts to rotate:** customer-support copilot · doc-intelligence platform · code assistant · meeting-notes agent · semantic search over 100M docs · a RAG that must cite and never leak cross-tenant data · cost-capped agent platform for 100k users.

**Senior signals interviewers reward:** starting with requirements not boxes; naming the *one* metric that matters; explaining what you'd measure; discussing failure + cost unprompted; knowing when NOT to use an agent / vector DB / multi-agent; citing a real trade-off you made (ADR).

---

## 4. Production-Readiness Checklist (apply to any GenAI system)

**Functionality & quality**
- [ ] Automated eval suite (RAGAS/DeepEval) with thresholds; **evals gate deploys in CI**
- [ ] Golden + synthetic datasets, versioned; experiment tracking of prompt/model/retrieval variants
- [ ] Grounding + citations; refusal path for unsupported queries

**Observability**
- [ ] Tracing (spans across retrieval/LLM/tool) with token/cost/latency attributes + correlation IDs
- [ ] Metrics + dashboards (requests, errors, latency p50/p95, tokens, cost, quality)
- [ ] Alerts on SLO breaches, error spikes, **cost anomalies**

**Performance & cost**
- [ ] Documented SLOs (TTFT, p95, availability); load-tested to SLO
- [ ] Streaming; parallelized where possible
- [ ] Caching (prompt + semantic, with invalidation); model routing/tiering; per-tenant budgets/quotas

**Reliability & scale**
- [ ] Stateless services; autoscaling; queue for spikes; timeouts + retries + circuit breakers
- [ ] Graceful degradation + fallback model/provider; **kill-switch**
- [ ] Checkpointing/resumability for agents

**Security & governance**
- [ ] Layered guardrails (input/output validation, injection defense, PII redaction, topic filters)
- [ ] Secrets in Secrets Manager; least-privilege IAM; per-tenant isolation
- [ ] Prompt & model **versioning** (pinned, changelog, eval-before-switch, canary/rollback)
- [ ] Data residency/compliance considered

**Operations**
- [ ] Incident runbook (failure modes, fallbacks, rollback, contacts); post-mortem template
- [ ] CI/CD (lint, type, test, evals, build, deploy); reproducible infra; tagged releases + rollback path
- [ ] Deployed on AWS (ECS/Fargate or Lambda) with CloudWatch

---

## 5. Job-Application Checklist

**Positioning**
- [ ] Title yourself for the target: *Production/AI Platform/Senior GenAI Engineer* (not "learning AI")
- [ ] One-line pitch: "Backend engineer (5y) turned Production GenAI engineer — I build and operate RAG, agents, and LLMOps on AWS, with evals, observability, and cost control."
- [ ] Resume: quantified outcomes (latency cut %, cost cut %, eval scores, scale); link portfolio + top 3 repos
- [ ] LinkedIn matches resume; "Open to work"; headline = target title
- [ ] Portfolio index page live; capstone demo video linked

**Proof assets ready**
- [ ] 7–8 polished repos · 8 articles published · capstone case study · design docs + cheat-sheet · ADRs

**Targeting & pipeline**
- [ ] Build a target list (AI startups + enterprise AI teams; remote-friendly for the $4–6k/mo band)
- [ ] Tailor application to each JD (mirror their stack: RAG? agents? Bedrock? evals?)
- [ ] Warm outreach: short message referencing a specific article/repo relevant to them
- [ ] Tracking sheet: company, role, JD link, contact, status, next action, date
- [ ] Cadence: N applications/week + M outreach/week; review weekly (reuse your Sunday review)

**Interview logistics**
- [ ] Practice the project walkthrough (5 min) + be ready to screen-share a repo/dashboard
- [ ] Prepare questions for them (their eval strategy, observability, on-call, model governance) — senior signal
- [ ] Post-interview: send a concise follow-up; log feedback; feed gaps back into next week's mocks

**Salary**
- [ ] Know the band ($4–6k/mo target); anchor on value delivered (production systems, not tutorials)
- [ ] Have a walk-away number and a "why me" backed by the portfolio

---

## Program complete

Across 8 months you moved from PHP/Laravel backend to a Production GenAI engineer with a defensible portfolio, public writing, ADRs, system-design fluency, interview reps, and a production mindset threaded through everything. Keep the Sunday review habit during the search, keep shipping small improvements to the capstone, and let the portfolio do the talking.

*Files in this program: Part 0 (professional track overlay), Parts 1–9 (roadmap + 32 weeks), this Finale. All in the **Production Generative AI Engineer** folder.*
