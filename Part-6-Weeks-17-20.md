# Part 6 — Weeks 17–20 · Month 5: Multi-Agent, AI Search & AWS Bedrock

> **Dates:** Mon 16 Nov 2026 → Sun 13 Dec 2026
> **Month goal:** Learn multi-agent orchestration (and when it *hurts*), build an AI search platform, and move to **production on AWS Bedrock** (IAM, Guardrails, Knowledge Bases, provisioned throughput).
> **Month projects:** **Project 5** — *Multi-agent research copilot on Bedrock* (supervisor/worker). **Project 6** — *AI Search Platform* (productionize Month-3 retrieval as a standalone hybrid-search service with ranking + analytics). Keep both repos; if time-pressed, prioritize Project 5 and keep Project 6 lean.
> **Ratio:** ~20% theory / 80% build. Governed by Part 0.

> **Professional Development Track:** ADR-005 (Bedrock vs direct OpenAI; multi-agent vs single agent) · **System Design #4: Multi-Agent Workflow** · **Article #5:** "When multi-agent helps (and when it just adds latency and cost)" · Month-5 reading · **Mock #5** (Week 20). **Production-mindset:** production deployment first-class (AWS); model versioning; cost of multi-step/multi-agent.

**Daily rhythm:** standard. Example — Mon 16 Nov: 19:00 read Bedrock model access + IAM docs; 20:00 call Claude/Titan via Bedrock behind your Month-1 provider interface; 21:00 commit + 8-question test "Bedrock vs direct API."

---

# WEEK 17 · 16–22 Nov 2026 — AWS Bedrock in production

**1. Objectives.** Run models through Bedrock behind your existing provider abstraction; use IAM, Bedrock Guardrails, and Knowledge Bases; reason about provisioned vs on-demand throughput.

**2. Theory (~20%).** Bedrock model access & regions; Converse API; IAM least-privilege for model invocation; Bedrock **Guardrails** (content filters, denied topics, PII, word filters); Bedrock **Knowledge Bases** (managed RAG) vs your own stack; provisioned throughput vs on-demand (cost/latency/SLA); private networking (VPC endpoints); Bedrock vs direct OpenAI/Anthropic trade-offs (data residency, IAM, unified access, enterprise procurement vs latest-model access + simplest SDK).

**3. Official docs.** AWS Bedrock docs (models, Converse, Guardrails, Knowledge Bases, provisioned throughput); IAM for Bedrock; Titan Embeddings.

**4. Reading.** AWS Bedrock case study / reference architecture; Month-5 docs deep dive (Bedrock + Bedrock Agents).

**5. Coding exercises.** (a) Add a **Bedrock provider** implementing your Month-1 interface (Converse API, streaming); (b) attach a Bedrock Guardrail and test blocked cases; (c) stand up a Knowledge Base and compare answers vs your own Qdrant RAG.

**6. Hands-on project.** Add Bedrock as a first-class provider across your existing services; make model choice config-driven; document IAM policy + Guardrail config.

**7. Deliverables.** Bedrock provider (streaming) swappable by config; Guardrail demo; KB-vs-own-RAG comparison note.

**8. GitHub milestones.** `feat: AWS Bedrock provider (Converse + streaming)`; `feat: Bedrock Guardrails integration`.

**9. Interview prep.** *Questions:* Why Bedrock over direct OpenAI for an enterprise? What do Bedrock Guardrails give you? Managed Knowledge Base vs your own RAG — trade-offs? *Follow-ups:* "How do you keep data in-region and off third-party APIs?" "When is provisioned throughput worth the cost?" *Scenario:* Enterprise won't send data to OpenAI — design the migration to Bedrock. *Common mistakes:* over-broad IAM, ignoring region/data-residency, assuming managed KB always beats custom. *Whiteboard:* draw a Bedrock-based RAG with IAM + Guardrails + VPC endpoints.

**10. Common mistakes.** God-mode IAM; hardcoding model IDs; no guardrail; ignoring cost of provisioned throughput.

**11. Production best practices + mindset Q.** Least-privilege IAM; secrets in Secrets Manager; model IDs + versions config-driven and pinned. *Mindset (deployment/security):* "What's my blast radius if these IAM creds leak?"

**12. Review.** Standard.

---

# WEEK 18 · 23–29 Nov 2026 — Multi-agent orchestration patterns

**1. Objectives.** Know the orchestration patterns and, crucially, **when multi-agent is justified** vs a single agent or plain pipeline; build a supervisor/worker system in LangGraph.

**2. Theory.** Patterns: single-agent-with-tools, router, supervisor/worker, hierarchical, parallel map-reduce, debate/critique; coordination cost (latency, tokens, error compounding); when multi-agent genuinely helps (separable expertise, parallelizable subtasks, isolation) vs when it just multiplies cost/latency; shared vs isolated state; inter-agent communication.

**3. Official docs.** LangGraph multi-agent docs (supervisor, hierarchical); Bedrock Agents (multi-agent collaboration).

**4. Reading.** A multi-agent paper (AutoGen or Self-Refine) — Month-5 paper; a multi-agent orchestration write-up.

**5. Coding exercises.** (a) Build a supervisor that routes to specialist worker agents (researcher, RAG-expert, summarizer); (b) add parallel fan-out + aggregation; (c) measure latency/cost vs a single agent doing the same task.

**6. Hands-on project.** Start `research-copilot` (Project 5): LangGraph supervisor delegating to worker agents (web search, your RAG, analysis, synthesis) running on **Bedrock**, fully traced.

**7. Deliverables.** Working supervisor/worker multi-agent system; cost/latency comparison vs single-agent baseline.

**8. GitHub milestones.** `feat: supervisor/worker multi-agent graph on Bedrock`; `feat: parallel worker fan-out + aggregation`.

**9. Interview prep.** *Questions:* When is multi-agent worth it? Supervisor/worker vs hierarchical vs debate? How do errors compound across agents? *Follow-ups:* "Your 4-agent system is 3× slower and 5× costlier than one agent for the same quality — what do you do?" *Scenario:* Design a research copilot — justify agent count. *Common mistakes:* multi-agent as a default, unbounded delegation, no per-agent caps, ignored latency. *Whiteboard:* draw supervisor/worker with state flow + caps.

**10. Common mistakes.** Over-decomposition; error compounding; no global budget across agents.

**11. Production best practices + mindset Q.** Justify every agent; global step/cost budget; trace the whole tree. *Mindset (cost):* "What's the total token cost of one multi-agent request at p95 depth?"

**12. Review.** Standard.

---

# WEEK 19 · 30 Nov–6 Dec 2026 — AI Search Platform (productionize retrieval)

**1. Objectives.** Turn Month-3 retrieval into a standalone **AI search service**: query understanding, hybrid ranking, snippets/citations, and search analytics.

**2. Theory.** Search platform anatomy (query understanding → retrieval → ranking → presentation); query rewriting/expansion, HyDE; ranking signals beyond similarity (recency, authority, popularity, personalization); result diversification; search analytics (CTR, zero-result rate, latency, relevance feedback); caching layers.

**3. Official docs.** Qdrant (scaling, replication, quantization); a hybrid-ranking reference (e.g., Vespa concepts).

**4. Reading.** An "AI search at scale" engineering post; LinkedIn "Musings on building a GenAI product" — Month-5 case study.

**5. Coding exercises.** (a) Add query rewriting + HyDE and measure impact; (b) add a ranking layer blending similarity + recency/source authority; (c) add search analytics logging + a zero-result fallback.

**6. Hands-on project.** Build `ai-search` (Project 6): hybrid search API with query understanding, ranking, snippets/citations, caching, and an analytics endpoint/dashboard stub.

**7. Deliverables.** Deployable AI search service with ranking + analytics; before/after relevance numbers.

**8. GitHub milestones.** `feat: query understanding + ranking layer`; `feat: search analytics + caching`.

**9. Interview prep.** *Questions:* Design an AI search platform. What ranking signals beyond vector similarity? How do you measure search quality online? *Follow-ups:* "Zero-result rate is 15% — how do you investigate and reduce it?" *Scenario:* Users say 'search feels worse than keyword' — diagnose and fix. *Common mistakes:* similarity-only ranking, no analytics, no caching, no zero-result handling. *Whiteboard:* draw the full search platform with caching + analytics.

**10. Common mistakes.** Ignoring non-semantic signals; no online metrics; no cache.

**11. Production best practices + mindset Q.** Log search analytics from day one; cache aggressively; measure online relevance. *Mindset (monitoring):* "What search dashboard would tell me quality is degrading before users complain?"

**12. Review.** Standard.

---

# WEEK 20 · 7–13 Dec 2026 · 🔵 CONSOLIDATION — ship Projects 5 & 6, ADR-005, System Design #4, Article #5, Mock #5

**Hands-on (finalize):** Project 5 (research copilot on Bedrock) and Project 6 (AI search) to portfolio grade — Docker, CI, READMEs (11-point), diagrams, agent/search evals, **deploy Project 5 to ECS/Fargate on AWS** (real deployment milestone), tagged releases.

**ADR-005** (`docs/adr/ADR-005.md`): *Why AWS Bedrock (not direct OpenAI) for production?* · *When multi-agent (not a single agent)?* Interview-defense paragraph.

**System Design #4 — Multi-Agent Workflow** (`design/04-multi-agent-workflow.md`, 7-part): functional (multi-step research/automation with specialist agents + HITL), non-functional (latency budget across agents, cost ceiling, auditability), architecture (supervisor/workers, shared state, tool layer, Bedrock, tracing), trade-offs (agent count, parallel vs sequential), scaling (concurrency, per-agent rate limits, queueing), cost (compounding tokens, caps, model tiering), failures (one worker fails, loops, injection, provider throttling).

**Article #5:** "When multi-agent helps (and when it just adds latency and cost)."

**Mock Interview #5 (Sunday):** behavioral · technical (Weeks 17–19 + follow-ups) · system design (Multi-Agent Workflow).

### End of Month 5 — Assessment
- [ ] Bedrock production skills (IAM, Guardrails, KB, throughput); multi-agent orchestration + judgment; AI search platform.
- [ ] **Projects 5 & 6** shipped; Project 5 **deployed to AWS**.
- [ ] **ADR-005**, **System Design #4**, **Article #5**, **reading set**, **Mock #5** complete.
- [ ] Skill self-assessment (≥4/5): Bedrock, multi-agent, orchestration judgment, AI search, AWS deploy.
- [ ] **Portfolio: 6/8.** Production-mindset: production deployment + model versioning now first-class.
- [ ] *Suggested stretch:* add provisioned-throughput cost modeling; add personalization to search ranking.

*End of Part 6. Next: Part 7 — Weeks 21–24, LLMOps, observability, guardrails, and security (holiday-adjusted).*
