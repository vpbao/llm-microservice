# Part 3 — Weeks 5–8 · Month 2: LLM Craft & Naive RAG (from scratch)

> **Dates:** Mon 24 Aug 2026 → Sun 20 Sep 2026
> **Month goal:** Master prompting, structured output, and tool calling at a deep level, then **build RAG by hand** (no framework) so you understand every moving part before Month 3 hands it to LlamaIndex/Qdrant.
> **Month project (Project 2):** *Chat-with-your-PDF, hand-built* — manual ingestion, chunking, embeddings, cosine search, prompt assembly, and grounded answers with citations.
> **Ratio:** ~20% theory / 80% build. Governed by `Part-0-Professional-Development-Track.md`.

> **Professional Development Track this month:** Project 2 to the 11-point spec + repo checklist · **ADR-002** (why build RAG from scratch; which embedding model) · **System Design #1: Enterprise PDF RAG** (7-part doc) · **Article #2:** "I built RAG from scratch (no framework)" · Month-2 **reading set** · **Mock interview #2** (Week 8). Production-mindset focus this month: prompt versioning (seeded), evaluation intuition, retrieval-quality thinking, cost of embeddings.

**Daily rhythm is the standard from Part 2** (Mon–Fri 19–22 in 3 blocks; Sat 09–12 & 14–18; Sun 09–12, 14–16 drills, 16–17 review). Concrete example — Mon 24 Aug: 19:00 read OpenAI prompting + Anthropic prompt docs; 20:00 refactor prompts into versioned templates; 21:00 commit + note the 8-question test for "few-shot prompting."

---

# WEEK 5 · 24–30 Aug 2026 — Prompt engineering & context management (deep)

**1. Learning objectives.** Write reliable prompts as *code* (versioned, testable); understand zero/few-shot, role prompting, chain-of-thought, decomposition; manage the context window deliberately (what to include, order effects, truncation).

**2. Theory (~20%).** System vs user vs assistant roles; instruction hierarchy; few-shot exemplar selection; CoT and when it helps/hurts; output formatting; context-window budgeting; the "lost in the middle" position-bias effect; prompt templating and **prompt versioning** (prompts live in the repo, are diffable, and are tested — treat like DB migrations).

**3. Official docs.** OpenAI prompt engineering guide + text-generation guide; Anthropic prompt engineering docs (system prompts, XML tags, prefills, long-context tips).

**4. Reading (this week's slice).** Chip Huyen "Building LLM applications for production"; skim *Lost in the Middle* (Liu et al., 2023).

**5. Coding exercises.** (a) Build a `PromptTemplate` abstraction with versioned templates + variables; (b) run the same task with zero-shot, few-shot, and CoT and log quality differences; (c) demonstrate position bias by moving the key fact to start/middle/end of context.

**6. Hands-on project.** Kick off `pdf-rag` repo (clean architecture, uv, ruff, mypy, tests, CI). Build the **prompt layer**: versioned answer/refusal/citation templates with variable injection. Add a golden-set of 15–20 Q/A pairs you'll use to eyeball quality all month.

**7. Deliverables.** Versioned prompt module + tests; a short experiment note comparing prompting strategies on your golden set.

**8. GitHub milestones.** `feat: versioned prompt templates`; `test: prompt rendering + strategy comparison`.

**9. Interview prep.** *Questions:* What is few-shot prompting and when does it beat fine-tuning? How does CoT change behavior and cost? What is the instruction hierarchy? *Follow-ups:* "Your few-shot examples leak into answers — fix it." "When does CoT hurt latency without helping accuracy?" *Scenario:* A prompt works in dev but degrades in prod on longer inputs — diagnose (context position/truncation). *Common mistakes:* prompts as scattered f-strings, no versioning, over-long few-shot blocks. *Whiteboard:* sketch how you'd version and test prompts in CI.

**10. Common mistakes.** Treating prompts as throwaway strings; ignoring token budget; stuffing context and hoping; no evaluation of prompt changes.

**11. Production best practices + mindset Q.** Prompts versioned in repo, rendered through one module, tested. *Mindset:* "If a prompt change ships tonight, how do I detect a quality regression?" (answer: golden set + evals — foreshadows Month 3/6).

**12. End-of-week review.** Standard checklist; can you defend each prompting choice aloud?

---

# WEEK 6 · 31 Aug–6 Sep 2026 — Embeddings & similarity from first principles

**1. Objectives.** Explain what embeddings are, how similarity search works, and the trade-offs across embedding models; generate and store embeddings and run cosine search **by hand** (numpy), no vector DB yet.

**2. Theory.** Vector representations; cosine vs dot vs Euclidean; normalization; dimensionality; embedding model families (OpenAI `text-embedding-3`, BGE, E5, Voyage, Titan) and how to choose (domain fit, cost, dimension, latency); chunk→embed→index→query flow; approximate vs exact nearest neighbor (why exact is fine at small scale, why ANN matters later).

**3. Official docs.** OpenAI embeddings guide; BGE / E5 model cards (HuggingFace); Amazon Titan Embeddings (Bedrock) overview.

**4. Reading.** OpenAI cookbook embeddings + semantic-search notebooks; a "choosing an embedding model" engineering post.

**5. Coding exercises.** (a) Embed 200 chunks, build a numpy cosine-search function, return top-k; (b) compare two embedding models on your golden set (retrieval hit-rate by eye); (c) show why un-normalized dot product misranks.

**6. Hands-on project.** Add ingestion + embedding to `pdf-rag`: PDF text extraction, a naive fixed-size chunker, embed with OpenAI (and one open-source model behind the same interface), store vectors + metadata in Postgres/JSON, and a hand-rolled cosine retriever.

**7. Deliverables.** Working ingest→embed→retrieve pipeline (no framework, no vector DB); embedding-model comparison note.

**8. GitHub milestones.** `feat: pdf ingestion + chunking`; `feat: embeddings + hand-rolled cosine retrieval`.

**9. Interview prep.** *Questions:* What is an embedding? Why cosine similarity? How do you pick an embedding model? *Follow-ups:* "Your retrieval returns semantically-close but wrong chunks — why, and what levers do you have?" "Why normalize embeddings?" *Scenario:* Retrieval quality is poor on tables/numbers — explain why embeddings struggle and what you'd do. *Common mistakes:* mismatched embedding models between index and query, no normalization, ignoring metadata. *Whiteboard:* draw the ingest→embed→index→retrieve→generate pipeline.

**10. Common mistakes.** Embedding query with a different model than the index; forgetting metadata; assuming bigger dimension = better.

**11. Production best practices + mindset Q.** Store the embedding model + version alongside every vector (you'll thank yourself when you re-embed). *Mindset:* "What does re-embedding the whole corpus cost, and how would I do it without downtime?"

**12. Review.** Standard.

---

# WEEK 7 · 7–13 Sep 2026 — Assemble naive RAG + tool calling depth

**1. Objectives.** Wire retrieval into generation with grounded, cited answers and honest refusals; understand tool/function calling deeply enough to see it as the seed of agents.

**2. Theory.** RAG anatomy (retrieve → augment → generate); context assembly and citation; grounding and refusal ("I don't know"); hallucination — what it is and why RAG reduces (not eliminates) it; tool calling round-trips, parallel tool calls, tool-choice control; the boundary between "RAG" and "agentic RAG."

**3. Official docs.** OpenAI function calling + Anthropic tool use (re-read at depth); RAG concept pages from the RAG paper's framing.

**4. Reading.** *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (Lewis et al., 2020) — the Month-2 paper; Eugene Yan on LLM patterns.

**5. Coding exercises.** (a) Assemble a grounded prompt from top-k chunks with inline citations; (b) implement a refusal path when retrieval confidence is low; (c) expose retrieval as a *tool* and let the model decide when to call it.

**6. Hands-on project.** Complete Project 2: `POST /chat` that retrieves, assembles context, generates a cited answer, and refuses when unsupported; streaming responses; request logging with tokens/cost/latency (reuse Month-1 patterns).

**7. Deliverables.** End-to-end hand-built RAG answering questions over your PDFs with citations + refusals.

**8. GitHub milestones.** `feat: grounded answers with citations`; `feat: retrieval-as-tool + refusal path`.

**9. Interview prep.** *Questions:* What is hallucination and how does RAG reduce it? Why can RAG still hallucinate? What's the difference between RAG and an agent? *Follow-ups:* "The model cites a chunk but the answer contradicts it — what's happening and how do you catch it?" *Scenario:* Users report confidently-wrong answers — walk your debugging from retrieval → prompt → generation. *Common mistakes:* no citations, no refusal path, dumping all chunks into context. *Whiteboard:* sketch grounded-RAG data flow + where hallucination can enter.

**10. Common mistakes.** Over-stuffing context; no grounding/citation; treating retrieval score as truth.

**11. Production best practices + mindset Q.** Always ground + cite; always have a refusal path; log which chunks were used (traceability). *Mindset:* "How would I prove to a stakeholder this answer is grounded?"

**12. Review.** Standard.

---

# WEEK 8 · 14–20 Sep 2026 · 🔵 CONSOLIDATION — harden, ADR-002, System Design #1, article, Mock #2

**Focus (no new theory):** ship Project 2 to portfolio grade; complete the month's Professional Development Track deliverables.

**Hands-on (finalize Project 2 v1.0):** Dockerize (+ Postgres), CI (lint/type/test), README with the 11-point spec, architecture diagram, `.env.example`, tagged release. Add a tiny eval: hit-rate + a manual faithfulness score on the golden set (foreshadows RAGAS in Month 3).

**ADR-002** (`docs/adr/ADR-002.md`): *Why build RAG from scratch before adopting a framework?* and *Which embedding model did I choose and why?* Include the strategy you'll flip to in Month 3 (LlamaIndex + Qdrant) and the trigger for that switch. End with the interview-defense paragraph.

**System Design #1 — Enterprise PDF RAG** (`design/01-enterprise-pdf-rag.md`, 7-part spec): functional (ingest heterogeneous PDFs incl. scans/tables, Q&A with citations, multi-tenant), non-functional (p95 < 3s, freshness, accuracy bar, tenancy isolation), architecture (ingestion pipeline, chunking, embeddings, index, retriever, generator, cache), trade-offs (chunking strategy, embedding model, exact vs ANN), scaling (corpus 10×/100×, re-embedding, sharding), cost (embedding + generation costs, caching), failures (bad OCR, empty retrieval, provider outage, injection via document content).

**Article #2:** "I built RAG from scratch (no framework) — here's what actually happens." Derived from Project 2 + ADR-002.

**Mock Interview #2 (Sunday):** 20 min behavioral (walk Project 2) · 30 min technical (Weeks 5–7 Q + follow-ups) · 40 min system design (present/defend Enterprise PDF RAG).

**Reading set logged** in `reading-log.md`.

### End of Month 2 — Assessment
- [ ] Prompting mastered (versioned, tested); embeddings + similarity understood from first principles.
- [ ] **Project 2** hand-built RAG shipped v1.0 (repo checklist passed).
- [ ] **ADR-002**, **System Design #1**, **Article #2**, **reading set**, **Mock #2** complete.
- [ ] Skill self-assessment (target ≥4/5): prompting, embeddings, similarity search, naive RAG, tool calling, citations/grounding.
- [ ] **Portfolio: 2/8.** Production-mindset status stated for Project 2.
- [ ] *Suggested stretch:* add a second embedding model comparison; add a naive BM25 keyword baseline to feel why hybrid matters next month.

*End of Part 3. Next: Part 4 — Weeks 9–12, Production RAG with Qdrant, hybrid search, reranking, and RAGAS evaluation.*
