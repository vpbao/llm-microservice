# Part 7 — Weeks 21–24 · Month 6: LLMOps, Observability, Guardrails & Security

> **Dates:** Mon 14 Dec 2026 → Sun 10 Jan 2027
> **Month goal:** Make an AI system **operable**: full tracing + metrics + dashboards + alerting, prompt/model versioning, evals-in-CI as deploy gates, guardrails, and a real security posture (prompt injection, PII, access control, incident response).
> **Month project (Project 7):** *Observed & Guarded AI Platform* — take a prior project (Enterprise RAG or the agent) and instrument it end to end: LangSmith/Phoenix + OpenTelemetry tracing, Prometheus + Grafana metrics/dashboards, alerting, guardrails, prompt & model registry, evals-in-CI, and a runbook.
> **Ratio:** ~20% theory / 80% build. Governed by Part 0.

> **Professional Development Track:** ADR-006 (observability stack choice; guardrails approach) · **System Design #5: AI Copilot** · **Article #6:** "LLM evaluation & observability in production" · Month-6 reading · **Mock #6** (Week 24). **Production-mindset:** observability, evaluation, security, guardrails, prompt/model versioning, experiment tracking, incident response — nearly all become first-class this month.

> ⚠️ **Holiday pacing:** Weeks 21–22 span the holidays and are intentionally lighter. Protect rest; use them as buffer/catch-up. Front-load Week 21, treat Week 22 as flex, and hit Weeks 23–24 fresh.

**Daily rhythm:** standard (relax Weeks 21–22 as needed). Example — Mon 14 Dec: 19:00 read OpenTelemetry GenAI semantic conventions; 20:00 add OTel spans to the RAG service; 21:00 commit + 8-question test "trace vs span vs metric."

---

# WEEK 21 · 14–20 Dec 2026 — Tracing & observability (LangSmith / Phoenix / OpenTelemetry)

**1. Objectives.** Instrument an AI app so every request is a readable trace (spans across retrieval/LLM/tool calls) with token, cost, and latency attributes; know when to use LLM-native tooling vs vendor-neutral OTel.

**2. Theory (~20%).** Observability pillars (traces, metrics, logs) for LLM apps; a trace = tree of spans; span attributes (model, tokens, cost, latency, prompt/version); LangSmith (LLM-native traces + datasets + evals) vs Phoenix/Arize (OSS traces + eval) vs OpenTelemetry (vendor-neutral, exports anywhere); correlation IDs; sampling; PII in traces (redaction).

**3. Official docs.** LangSmith tracing; Arize Phoenix; OpenTelemetry GenAI semantic conventions.

**4. Reading.** RAGAS/Self-RAG (Month-6 paper); Hamel Husain on evals; a production LLM observability post.

**5. Coding exercises.** (a) Add OTel spans across retrieval→rerank→LLM in the RAG service; (b) mirror into LangSmith or Phoenix and read a full trace; (c) add cost/token/latency span attributes + a correlation ID.

**6. Hands-on project.** Start `ai-platform-ops`: wrap a prior project with tracing (OTel + LangSmith/Phoenix). Every request fully traced with cost/latency/model attributes and a correlation ID.

**7. Deliverables.** Fully traced service; screenshot of a trace in README.

**8. GitHub milestones.** `feat: OpenTelemetry tracing (spans + attributes + correlation IDs)`; `feat: LangSmith/Phoenix trace export`.

**9. Interview prep.** *Questions:* How do you make an LLM app observable? Trace vs span vs metric? LangSmith vs OTel — when each? *Follow-ups:* "A request is slow 5% of the time — how do traces help you find why?" "How do you keep PII out of traces?" *Scenario:* Users report intermittent bad answers — use traces to localize retrieval vs generation. *Common mistakes:* logging only inputs/outputs, no span tree, PII leaking into traces, no correlation ID. *Whiteboard:* draw a request trace with spans + attributes.

**10. Common mistakes.** No tracing; flat logs; PII in traces; no sampling strategy.

**11. Production best practices + mindset Q.** Trace every request; standardized span attributes; redact PII; correlation IDs everywhere. *Mindset (observability):* "Given a user's complaint and a timestamp, can I pull the exact trace in under a minute?"

**12. Review.** Standard (lighter — holiday week).

---

# WEEK 22 · 21–27 Dec 2026 — Metrics, dashboards, alerting + prompt/model versioning (LIGHT/BUFFER week)

**1. Objectives.** Add Prometheus metrics + Grafana dashboards + alerts; put prompts and model choices under version control with a registry and change discipline. *(Lighter week — spread across available time; use as catch-up if behind.)*

**2. Theory.** RED/USE metrics adapted for LLM apps (requests, errors, duration + tokens/cost/quality); SLIs/SLOs (p95 latency, error rate, cost/request, eval score); alerting thresholds & fatigue; **prompt versioning** (prompts in repo/registry, diffable, tested, tied to eval runs); **model versioning** (pin model IDs, changelog, eval-before-switch, canary); experiment tracking of prompt/model variants.

**3. Official docs.** Prometheus + Grafana docs; a prompt-registry pattern (LangSmith prompts or in-repo registry).

**4. Reading.** An SLO-for-LLM-apps post; a prompt/model versioning write-up.

**5. Coding exercises.** (a) Expose `/metrics` (tokens, cost, latency histograms, error counters); (b) build a Grafana dashboard + one alert; (c) move prompts into a versioned registry and tie each to an eval run.

**6. Hands-on project.** Add metrics + dashboards + alerting to `ai-platform-ops`; implement a prompt/model registry with change-tracking and eval-gated switches.

**7. Deliverables.** Grafana dashboard (screenshot in README); at least one alert; prompt/model registry with versions + changelog.

**8. GitHub milestones.** `feat: Prometheus metrics + Grafana dashboard + alert`; `feat: prompt & model registry (versioned, eval-gated)`.

**9. Interview prep.** *Questions:* What SLOs for an LLM service? How do you version prompts and models safely? What/when to alert? *Follow-ups:* "You want to switch model versions — safe rollout plan?" "How do you avoid alert fatigue?" *Scenario:* A new model version quietly drops answer quality — how does your process catch it before users do? *Common mistakes:* no SLOs, prompts un-versioned, swapping models without evals, noisy alerts. *Whiteboard:* draw the metrics→dashboard→alert pipeline + a canary model rollout.

**10. Common mistakes.** No SLOs/alerts; unversioned prompts; blind model upgrades.

**11. Production best practices + mindset Q.** SLOs defined + dashboarded; prompts/models versioned + eval-gated; canary rollouts. *Mindset (model/prompt versioning):* "Can I roll back a bad prompt or model change in one commit/deploy?"

**12. Review.** Standard (light — holiday).

---

# WEEK 23 · 28 Dec 2026–3 Jan 2027 — Guardrails, security & incident response

**1. Objectives.** Build layered guardrails and a real security posture; write a runbook and practice incident response for AI-specific failures.

**2. Theory.** Guardrails (input validation, prompt-injection & jailbreak defense, output validation/schema, PII detection/redaction, toxicity/topic filters, grounding checks); OWASP LLM Top-10; defense-in-depth (untrusted content isolation, least-privilege tools, allow-lists, human approval); secrets & access control (IAM, Secrets Manager, per-tenant isolation); incident response (runbooks, fallbacks, kill-switch, rollback, post-mortems); cost anomalies as incidents.

**3. Official docs.** Bedrock Guardrails; an OWASP LLM Top-10 reference; a guardrails library (e.g., Guardrails AI / NeMo Guardrails) overview.

**4. Reading.** A prompt-injection deep dive; a production LLM incident post-mortem (Month-6 case study).

**5. Coding exercises.** (a) Red-team your agent with injection payloads via retrieved docs + user input; add layered defenses and re-test; (b) add PII redaction on inputs/outputs/traces; (c) add a cost-spike alert + kill-switch.

**6. Hands-on project.** Complete Project 7: guardrails (input/output/PII/injection), access control, a documented **runbook** (failure modes, fallbacks, rollback, kill-switch), and a red-team report.

**7. Deliverables.** Guarded, secured platform + runbook + red-team report in `docs/`.

**8. GitHub milestones.** `feat: layered guardrails (injection/PII/output validation)`; `docs: security posture + incident runbook`.

**9. Interview prep.** *Questions:* OWASP LLM Top-10? How do you defend against prompt injection in RAG/agents? What's in an AI incident runbook? *Follow-ups:* "A jailbreak got through — how do you respond in the next 30 minutes?" "How do you prevent a runaway cost incident?" *Scenario:* Prod agent leaked a snippet of another tenant's data — contain, fix, prevent. *Common mistakes:* single-layer defense, trusting model self-policing, no runbook, no kill-switch. *Whiteboard:* draw defense-in-depth layers + the incident response flow.

**10. Common mistakes.** One guardrail and done; no tenant isolation; no incident plan.

**11. Production best practices + mindset Q.** Defense-in-depth; least privilege; runbooks + kill-switch + rollback; treat cost spikes as incidents. *Mindset (incident response):* "If this breaks at 2am, what's the fallback and who/what stops the bleeding?"

**12. Review.** Standard.

---

# WEEK 24 · 4–10 Jan 2027 · 🔵 CONSOLIDATION — ship Project 7, ADR-006, System Design #5, Article #6, Mock #6

**Hands-on (finalize Project 7 v1.0):** everything green — tracing + metrics + dashboards + alerts + guardrails + evals-in-CI + runbook; README (11-point) with dashboard/trace screenshots; tagged release.

**ADR-006** (`docs/adr/ADR-006.md`): *Which observability stack (LangSmith vs Phoenix vs OTel) and why?* · *Guardrails approach (managed Bedrock Guardrails vs library vs custom)?* Interview-defense paragraph.

**System Design #5 — AI Copilot** (`design/05-ai-copilot.md`, 7-part): functional (in-product assistant: chat + actions + citations, per-user context/permissions), non-functional (latency, quality SLOs, safety, auditability), architecture (RAG + agent + guardrails + observability + prompt/model registry), trade-offs (safety vs latency, managed vs custom guardrails), scaling (concurrent users, caching, rate limits), cost (per-session budget, caching, model tiering), failures (injection, bad actions, outages, quality regressions — with detection + rollback).

**Article #6:** "LLM evaluation & observability in production: traces, metrics, and evals-in-CI."

**Mock Interview #6 (Sunday):** behavioral · technical (Weeks 21–23 + follow-ups) · system design (AI Copilot).

### End of Month 6 — Assessment
- [ ] Full observability (traces/metrics/dashboards/alerts); prompt/model versioning; evals-in-CI as gates; guardrails; security posture + runbook.
- [ ] **Project 7 (Observed & Guarded AI Platform)** shipped v1.0.
- [ ] **ADR-006**, **System Design #5**, **Article #6**, **reading set**, **Mock #6** complete.
- [ ] Skill self-assessment (≥4/5): tracing, metrics/SLOs, prompt/model versioning, guardrails, security, incident response.
- [ ] **Portfolio: 7/8.** Production-mindset: observability/eval/security/versioning/incident response now first-class.
- [ ] *Suggested stretch:* add automated red-team tests to CI; add a cost-anomaly detector.

*End of Part 7. Next: Part 8 — Weeks 25–28, scaling, cost/latency optimization, and the capstone build.*
