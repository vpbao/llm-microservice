# Part 4 — Weeks 9–12 · Month 3: Production RAG

> **Dates:** Mon 21 Sep 2026 → Sun 18 Oct 2026
> **Month goal:** Turn hand-built RAG into a **production RAG** that survives a messy real corpus: proper chunking, Qdrant, hybrid search (BM25 + vector), reranking, and — critically — an **automated evaluation suite** so quality is a number, not a vibe.
> **Month project (Project 3):** *Enterprise RAG* — LlamaIndex ingestion + Qdrant hybrid retrieval + reranking + metadata filtering + multi-tenant awareness + RAGAS evals in CI.
> **Ratio:** ~20% theory / 80% build. Governed by Part 0.

> **Professional Development Track this month:** ADR-003 (Qdrant vs Pinecone/pgvector; hybrid vs pure vector; why reranking) · **System Design #2: AI Search Platform** · **Article #3:** "Hybrid retrieval explained" · Month-3 reading · **Mock #3** (Week 12). **Production-mindset becomes first-class for evaluation, experiment tracking, and monitoring this month.**

**Daily rhythm:** standard Part-2 schedule. Example — Mon 21 Sep: 19:00 read Qdrant collection/filtering docs; 20:00 stand up Qdrant in Docker + ingest; 21:00 commit + note "HNSW vs IVF" 8-question test.

---

# WEEK 9 · 21–27 Sep 2026 — Chunking strategies + Qdrant + ANN internals

**1. Objectives.** Choose chunking deliberately (fixed / recursive / semantic / structure-aware) and justify it; run Qdrant with proper collections, payload filtering, and understand ANN indexes (HNSW) from first principles.

**2. Theory (~20%).** Chunk size vs overlap trade-offs; token-aware vs char-based; semantic and layout-aware chunking; why chunking dominates RAG quality; ANN: HNSW (graph), IVF, PQ, recall vs latency vs memory; Qdrant architecture (collections, payloads, filters, quantization); metadata as first-class (tenant_id, source, timestamps, ACLs).

**3. Official docs.** Qdrant docs (collections, payload filtering, hybrid, quantization); LlamaIndex node parsers / ingestion; HNSW paper (Malkov & Yashunin) for internals.

**4. Reading.** *Dense Passage Retrieval* (Karpukhin et al., 2020) — Month-3 paper option A; a Qdrant/Pinecone "learn" piece on chunking.

**5. Coding exercises.** (a) Implement 3 chunkers and compare retrieval hit-rate on your golden set; (b) load vectors into Qdrant with tenant + source payload; (c) run filtered searches (by tenant/source) and measure latency.

**6. Hands-on project.** Start `enterprise-rag` repo. Migrate Month-2 ingestion to **LlamaIndex** ingestion + a recursive/structure-aware chunker; index into **Qdrant** with rich metadata; retriever with payload filtering (multi-tenant isolation).

**7. Deliverables.** Qdrant-backed retriever with metadata filtering; chunking comparison note (numbers).

**8. GitHub milestones.** `feat: LlamaIndex ingestion + structure-aware chunking`; `feat: Qdrant index with metadata filtering (multi-tenant)`.

**9. Interview prep.** *Questions:* How do you choose chunk size? What is HNSW and its recall/latency trade-off? When do you NOT need a vector DB? *Follow-ups:* "Recall dropped after enabling quantization — why?" "How do you isolate tenants in one collection vs many?" *Scenario:* Retrieval misses answers that span two chunks — fix the chunking. *Common mistakes:* fixed 512-char chunks everywhere, no overlap, no metadata, one collection with no tenant isolation. *Whiteboard:* draw HNSW search and where recall/latency trade off.

**10. Common mistakes.** Chunking as an afterthought; ignoring document structure; no tenant isolation; blind quantization.

**11. Production best practices + mindset Q.** Metadata-rich payloads; tenant isolation by design; store embedding model version. *Mindset (monitoring):* "What retrieval metrics would I put on a dashboard?"

**12. Review.** Standard.

---

# WEEK 10 · 28 Sep–4 Oct 2026 — Hybrid search (BM25 + vector) + reranking

**1. Objectives.** Explain why pure vector search underperforms on keywords/rare terms, implement hybrid retrieval (sparse + dense) with fusion, and add a cross-encoder reranker.

**2. Theory.** Lexical (BM25/sparse) vs semantic (dense) retrieval; failure modes of each; fusion (RRF — reciprocal rank fusion, weighted); bi-encoder retrieve → cross-encoder rerank (the standard production recipe); why rerankers are slower but precise; reranking top-N selection and latency budget.

**3. Official docs.** Qdrant hybrid/sparse vectors; BGE Reranker model card; Cohere Rerank docs.

**4. Reading.** *Lost in the Middle* (Liu et al., 2023) — Month-3 paper option B; a hybrid-search + reranking engineering post.

**5. Coding exercises.** (a) Add BM25 (or Qdrant sparse) and fuse with dense via RRF; (b) add BGE reranker over top-50 → top-5; (c) A/B pure-vector vs hybrid vs hybrid+rerank on your golden set and record metrics.

**6. Hands-on project.** Add hybrid retrieval + reranking to `enterprise-rag`; make retrieval config-driven (dense / hybrid / hybrid+rerank) so you can benchmark and defend the choice.

**7. Deliverables.** Hybrid + rerank retriever; benchmark table (pure vs hybrid vs +rerank) with hit-rate/precision.

**8. GitHub milestones.** `feat: hybrid retrieval (BM25 + vector, RRF)`; `feat: cross-encoder reranking`.

**9. Interview prep.** *Questions:* Why BM25 + vector instead of just vector? How does reranking work? What is RRF? *Follow-ups:* "Reranking added 400ms p95 — how do you claw it back?" "When is a reranker not worth it?" *Scenario:* Vector search fails on exact product codes / acronyms — explain and fix with hybrid. *Common mistakes:* pure vector only, reranking too many candidates, no latency budget. *Whiteboard:* draw bi-encoder retrieve → cross-encoder rerank with the latency budget annotated.

**10. Common mistakes.** Ignoring lexical signal; reranking 200 candidates; no measurement.

**11. Production best practices + mindset Q.** Config-driven retrieval; measure every change; cap rerank candidates for latency. *Mindset (latency):* "What's my retrieval latency budget within the p95 target, and where does it go?"

**12. Review.** Standard.

---

# WEEK 11 · 5–11 Oct 2026 — RAG evaluation (RAGAS) + experiment tracking

**1. Objectives.** Make quality measurable: build an eval dataset and compute faithfulness, answer relevancy, context precision/recall; wire evals into CI; track experiments over time.

**2. Theory.** Why "it looks good" is not acceptable; RAG failure taxonomy (retrieval vs generation faults); RAGAS metrics; LLM-as-judge (uses, biases, mitigations); building/maintaining eval datasets (golden set + synthetic); regression testing; **experiment tracking** (compare retrieval/model/prompt variants over time).

**3. Official docs.** RAGAS docs; DeepEval docs; LangSmith datasets & evaluations.

**4. Reading.** RAGAS paper (Month-3 eval reading); Hamel Husain on building LLM evals.

**5. Coding exercises.** (a) Build a 50-item eval set; (b) compute RAGAS metrics for your 3 retrieval configs; (c) add a DeepEval test that fails CI if faithfulness drops below a threshold.

**6. Hands-on project.** Add an **eval suite** to `enterprise-rag`: dataset, RAGAS + DeepEval metrics, a CLI to run evals, and a GitHub Actions job that runs them (evals-in-CI). Record results per config in an experiment log.

**7. Deliverables.** Automated eval suite; evals-in-CI; experiment log comparing configs with numbers.

**8. GitHub milestones.** `feat: RAG eval suite (RAGAS + DeepEval)`; `ci: evals-in-CI gate`.

**9. Interview prep.** *Questions:* How do you evaluate a RAG system? What is faithfulness vs answer relevancy vs context precision/recall? What are LLM-as-judge pitfalls? *Follow-ups:* "Your judge scores are inconsistent run-to-run — why and how to stabilize?" "How do you separate a retrieval bug from a generation bug via metrics?" *Scenario:* A prompt change improved eyeball quality but dropped faithfulness — what do you ship? *Common mistakes:* no eval set, only anecdotal testing, trusting a single judge run, no CI gate. *Whiteboard:* sketch the eval pipeline + CI gate.

**10. Common mistakes.** Shipping without evals; conflating retrieval and generation failures; tiny/biased eval sets.

**11. Production best practices + mindset Q.** Evals gate deploys; experiments logged and comparable; thresholds enforced in CI. *Mindset (evaluation/experiment tracking):* "How do I know a change is a real improvement and not noise?"

**12. Review.** Standard.

---

# WEEK 12 · 12–18 Oct 2026 · 🔵 CONSOLIDATION — ship Project 3, ADR-003, System Design #2, Article #3, Mock #3

**Hands-on (finalize Project 3 v1.0):** deploy path (Docker Compose local; **ECS/Fargate** notes for AWS), monitoring hooks (retrieval metrics, latency, cost), README (11-point spec), architecture diagram, tagged release. Confirm evals-in-CI green.

**ADR-003** (`docs/adr/ADR-003.md`): *Why Qdrant (not Pinecone/pgvector)?* · *Why hybrid (BM25+vector) over pure vector?* · *Why add reranking despite latency cost?* Include the pgvector "when a dedicated vector DB is overkill" reasoning. Interview-defense paragraph.

**System Design #2 — AI Search Platform** (`design/02-ai-search-platform.md`, 7-part): functional (search across large multi-source corpus, ranking, filters, snippets/citations), non-functional (p95, QPS, freshness, relevance targets), architecture (ingestion, hybrid index, reranker, query understanding, caching, API), trade-offs (managed vs self-hosted vectors, rerank placement), scaling (sharding, replicas, cache tiers, embedding pipeline throughput), cost (embedding/rerank/generation, cache hit-rate), failures (index staleness, hot shards, reranker overload, poisoned docs).

**Article #3:** "Hybrid retrieval explained: BM25 + vectors + reranking, and why pure vector search underperforms."

**Mock Interview #3 (Sunday):** behavioral (Project 3 walk) · technical (Weeks 9–11 + follow-ups) · system design (defend AI Search Platform).

### End of Month 3 — Assessment
- [ ] Chunking, Qdrant/ANN, hybrid search, reranking, and RAG evaluation mastered.
- [ ] **Project 3 (Enterprise RAG)** shipped v1.0 with **evals-in-CI**.
- [ ] **ADR-003**, **System Design #2**, **Article #3**, **reading set**, **Mock #3** complete.
- [ ] Skill self-assessment (≥4/5): chunking, vector DB/ANN, hybrid, reranking, RAG eval, experiment tracking.
- [ ] **Portfolio: 3/8.** Production-mindset: evaluation + monitoring now first-class.
- [ ] *Suggested stretch:* add query rewriting / HyDE; add a small synthetic eval-set generator.

*End of Part 4. Next: Part 5 — Weeks 13–16, Agents & LangGraph.*
