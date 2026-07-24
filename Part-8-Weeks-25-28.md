# Part 8 — Weeks 25–28 · Month 7: Scale, Cost & Latency + Capstone Build

> **Dates:** Mon 11 Jan 2027 → Sun 7 Feb 2027
> **Month goal:** Take systems from "works" to "works at scale, on budget, fast" — latency and cost optimization, caching, model routing, load testing, K8s fundamentals, and self-hosting open-source models with vLLM. Then **start the capstone**.
> **Month project (Project 8 — begins):** *Enterprise AI Copilot (Capstone)* — the flagship that combines RAG + agents + LLMOps + AWS deploy, designed to an explicit SLO and cost budget, and load-tested. Built this month, finished in Month 8.
> **Ratio:** ~20% theory / 80% build. Governed by Part 0.

> **Professional Development Track:** ADR-007 (caching/routing strategy; vLLM vs managed) · **System Design #6: Enterprise AI Platform** · **Article #7:** "Cutting LLM cost and latency" · Month-7 reading · **Mock #7** (Week 28). **Production-mindset:** cost + latency optimization become first-class; incident response deepened with load/failure testing.

**Daily rhythm:** standard. Example — Mon 11 Jan: 19:00 read semantic-caching + prompt-caching material; 20:00 add a semantic cache to the RAG service; 21:00 commit + 8-question test "semantic cache invalidation."

---

# WEEK 25 · 11–17 Jan 2027 — Latency optimization

**1. Objectives.** Hit a latency SLO: reduce time-to-first-token and p95 end-to-end via streaming, parallelism, retrieval/generation overlap, model selection, and payload discipline.

**2. Theory (~20%).** Latency budget decomposition (network, retrieval, rerank, LLM prefill/decode, post-processing); TTFT vs total; streaming; parallel tool calls / concurrent retrieval; speculative/parallel retrieval; smaller/faster models for sub-tasks; prompt-length reduction; batching; keep-alive/connection reuse; where async actually helps.

**3. Official docs.** Provider streaming + latency guidance; vLLM performance concepts (prefill/decode, continuous batching).

**4. Reading.** *PagedAttention / vLLM* paper (Month-7 paper); a latency-optimization case study.

**5. Coding exercises.** (a) Instrument and break down p50/p95 latency by stage; (b) parallelize retrieval + rerank; (c) swap a smaller model for a sub-step and measure quality/latency trade-off.

**6. Hands-on project.** Start `enterprise-copilot` (Capstone). Set an explicit **latency SLO** (e.g., TTFT < 800ms, p95 < 4s) and instrument stage-level latency from day one.

**7. Deliverables.** Latency breakdown dashboard; documented SLO; before/after optimization numbers.

**8. GitHub milestones.** `feat: stage-level latency instrumentation`; `perf: parallel retrieval + streaming (TTFT/p95 improvements)`.

**9. Interview prep.** *Questions:* How do you reduce LLM app latency? What is TTFT and why optimize it? Where does latency go in a RAG request? *Follow-ups:* "p95 is 3× p50 — what causes the tail and how do you fix it?" *Scenario:* A copilot feels sluggish — produce a prioritized latency-cut plan. *Common mistakes:* optimizing averages not tails, no streaming, oversized prompts, serial calls. *Whiteboard:* draw the latency budget across stages with targets.

**10. Common mistakes.** Ignoring the tail; no streaming; giant prompts; serial where parallel is possible.

**11. Production best practices + mindset Q.** SLO-driven; measure per stage; stream; parallelize. *Mindset (latency):* "Which single stage owns my p95 and what's the cheapest way to halve it?"

**12. Review.** Standard.

---

# WEEK 26 · 18–24 Jan 2027 — Cost optimization: caching, routing, model tiering

**1. Objectives.** Cut cost without hurting quality: prompt caching, semantic caching, model routing/tiering, retrieval-cost control, and budget guardrails.

**2. Theory.** Cost model (input/output tokens, context size, calls-per-request in agents); prompt caching; **semantic caching** (embedding-keyed response cache, invalidation, staleness risk); model routing (cheap model first, escalate on low confidence); model tiering by task; reducing context/chunks; batching; budget caps + per-tenant quotas; cost/quality Pareto thinking.

**3. Official docs.** Provider prompt-caching docs; a semantic-cache library (e.g., GPTCache) overview; Bedrock pricing/throughput.

**4. Reading.** An LLM cost-optimization case ("how we cut cost by N%"); a semantic-caching write-up.

**5. Coding exercises.** (a) Add prompt caching + measure savings; (b) add a semantic cache with invalidation; (c) implement a router (small→large on low confidence) and measure cost/quality.

**6. Hands-on project.** Add caching + routing + budget guardrails to the capstone; produce a cost-per-request dashboard and a cost/quality trade-off table.

**7. Deliverables.** Caching + routing live; cost-per-request dashboard; documented savings with quality held constant.

**8. GitHub milestones.** `feat: semantic + prompt caching`; `feat: model routing/tiering + budget guardrails`.

**9. Interview prep.** *Questions:* How do you cut LLM cost without hurting quality? What is semantic caching and its risks? When to route to a cheaper model? *Follow-ups:* "Semantic cache returns a stale/wrong hit — how do you prevent it?" "How do you cap spend per tenant?" *Scenario:* Bill doubled after a launch — find and stop the leak. *Common mistakes:* caching without invalidation, routing that tanks quality, no budget caps, ignoring agent multi-call cost. *Whiteboard:* draw the caching + routing decision flow with budget guardrails.

**10. Common mistakes.** Unsafe cache hits; quality regressions from routing; no per-tenant budgets.

**11. Production best practices + mindset Q.** Cache with invalidation; route with a confidence signal; enforce budgets; always re-measure quality after a cost change. *Mindset (cost):* "What's my cost per request and per tenant, and where's the biggest safe cut?"

**12. Review.** Standard.

---

# WEEK 27 · 25–31 Jan 2027 — Scaling, load testing, K8s basics & self-hosting (vLLM)

**1. Objectives.** Reason about horizontal scale, load-test to your SLO, know K8s fundamentals (and when EKS/ECS), and self-host an open-source model with vLLM to compare vs managed.

**2. Theory.** Stateless services + horizontal scaling; autoscaling (ECS/Fargate, K8s HPA); queues for spiky load (SQS); connection/concurrency limits; load testing (Locust/k6) against SLOs; K8s fundamentals (pods, deployments, services, HPA) and ECS-vs-EKS trade-off; self-hosting with **vLLM** (continuous batching, throughput, GPU cost) vs managed (Bedrock) — cost/control/latency/ops trade-offs.

**3. Official docs.** vLLM docs; AWS ECS/Fargate autoscaling + CloudWatch; Kubernetes basics; Locust or k6 docs.

**4. Reading.** vLLM paper (revisit); a "managed vs self-hosted inference" cost analysis.

**5. Coding exercises.** (a) Load-test the capstone with Locust/k6 to find the breaking point vs SLO; (b) add autoscaling config; (c) serve an open-source model (Llama/Qwen/Mistral) with vLLM locally and benchmark throughput/latency vs Bedrock.

**6. Hands-on project.** Make the capstone horizontally scalable (stateless, autoscaling, queue for spikes); document a load test to SLO; add a vLLM self-hosting option behind the provider interface with a cost/latency comparison.

**7. Deliverables.** Load-test report (breaking point + SLO adherence); autoscaling config; vLLM-vs-Bedrock benchmark.

**8. GitHub milestones.** `feat: autoscaling + queue for spiky load`; `perf: load test to SLO`; `feat: vLLM self-hosted provider option`.

**9. Interview prep.** *Questions:* How do you scale an LLM service? ECS vs EKS? When self-host vs managed inference? How do you load-test to an SLO? *Follow-ups:* "Traffic 10×'d overnight — what breaks first and how does the system absorb it?" "GPU costs for self-hosting vs Bedrock at your volume?" *Scenario:* Design scaling for a copilot going from 100 to 100k users. *Common mistakes:* stateful services, no load test, self-hosting without a cost case, no queue for spikes. *Whiteboard:* draw the scaled architecture (LB, autoscaling, queue, cache, vector DB, inference).

**10. Common mistakes.** Assuming vertical scale; no load test; self-hosting for prestige not economics.

**11. Production best practices + mindset Q.** Stateless + autoscale + queue; load-test to SLO; justify self-hosting with numbers. *Mindset (scale/incident):* "At 10× traffic, what's my failure mode and my graceful-degradation plan?"

**12. Review.** Standard.

---

# WEEK 28 · 1–7 Feb 2027 · 🔵 CONSOLIDATION — capstone checkpoint, ADR-007, System Design #6, Article #7, Mock #7

**Hands-on (capstone checkpoint):** capstone runs end to end with SLOs, caching, routing, autoscaling, full observability, and guardrails carried over from prior projects. Not "finished" (that's Month 8) but demoable and load-tested. README draft (11-point), architecture diagram, tagged `v0.9`.

**ADR-007** (`docs/adr/ADR-007.md`): *Caching + model-routing strategy?* · *Self-hosted vLLM vs managed Bedrock inference — the decision and the numbers.* Interview-defense paragraph.

**System Design #6 — Enterprise AI Platform** (`design/06-enterprise-ai-platform.md`, 7-part): functional (multi-tenant platform hosting RAG/agents/search for many teams, self-serve, governance), non-functional (SLOs, cost budgets/chargeback, security/compliance, availability), architecture (gateway, provider abstraction, shared retrieval + vector store, agent runtime, prompt/model registry, observability, guardrails, IAM), trade-offs (shared vs isolated tenancy, managed vs self-hosted, build vs buy), scaling (per-tenant limits, autoscaling, caching tiers), cost (chargeback, routing, caching, provisioned throughput), failures (noisy neighbor, provider outage, cost runaway, injection — with isolation + fallback).

**Article #7:** "Cutting LLM cost and latency: caching, routing, and self-hosting trade-offs."

**Mock Interview #7 (Sunday):** behavioral · technical (Weeks 25–27 + follow-ups) · system design (Enterprise AI Platform — your hardest design yet).

### End of Month 7 — Assessment
- [ ] Latency + cost optimization; scaling + load testing; K8s basics; vLLM self-hosting; capstone at v0.9.
- [ ] **Project 8 (Capstone)** building; **ADR-007**, **System Design #6**, **Article #7**, **reading set**, **Mock #7** complete.
- [ ] Skill self-assessment (≥4/5): latency opt, cost opt, caching, routing, scaling/load testing, self-hosting judgment.
- [ ] **Portfolio: 7/8 done + capstone at v0.9.** Production-mindset: cost + latency now first-class; full 13-point coverage across portfolio.
- [ ] *Suggested stretch:* add cost chargeback per tenant; add chaos/failure injection to the load test.

*End of Part 8. Next: Part 9 — Weeks 29–32, capstone finish, portfolio polish, system design & interview readiness.*
