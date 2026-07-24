# Part 9 — Weeks 29–32 · Month 8: Capstone Finish, Portfolio Polish & Interview Readiness

> **Dates:** Mon 8 Feb 2027 → Sun 7 Mar 2027
> **Month goal:** Finish the capstone, bring all repos to hiring-committee quality, achieve system-design fluency, run a full interview loop, and get applications out the door for **Production AI / AI Platform / Senior GenAI Engineer** roles ($4k–$6k/mo).
> **Month project (Project 8 — finish):** *Enterprise AI Copilot (Capstone) v1.0* — RAG + agents + LLMOps + AWS deploy + SLOs + cost budget + observability + guardrails, fully documented with a case study.
> **Ratio this month flips slightly:** more polish/communication/interview reps, still heavily hands-on. Governed by Part 0.

> **Professional Development Track:** ADR-008 (capstone retrospective — the 3 decisions you'd defend hardest) · **System Design #7: full timed mock** · **Article #8:** "What I learned building production GenAI in 8 months" + capstone case study · Month-8 reading · **Mock #8 — full loop** (Week 32). This month operationalizes everything from Part 0 into an interview-ready package.

**Daily rhythm:** standard, but weekday block C and Sunday drills shift toward interview practice. Example — Mon 8 Feb: 19:00 capstone bug-bash; 20:00 write capstone README/case study; 21:00 rehearse the project walkthrough out loud.

---

# WEEK 29 · 8–14 Feb 2027 — Capstone finish & hardening

**1. Objectives.** Ship capstone v1.0: all production concerns green, deployed on AWS, load-tested to SLO, fully observed and guarded.

**2–5. Focus (build-heavy, minimal new theory).** Close all capstone gaps: evals-in-CI passing with real thresholds; tracing + metrics + dashboards + alerts live; guardrails + runbook; caching + routing + autoscaling; deployed to ECS/Fargate; secrets in Secrets Manager; IAM least-privilege. Reading: revisit the one paper + two docs most central to the capstone and critique your own choices.

**6. Hands-on project.** Capstone → **v1.0**: end-to-end demo, deployed, load-tested, documented. Record a 3–5 min demo video/GIF for the README.

**7. Deliverables.** Capstone v1.0 tagged + deployed; demo recording; dashboards/trace screenshots in README.

**8. GitHub milestones.** `release: capstone v1.0`; `docs: demo + dashboards + architecture`.

**9. Interview prep.** *Questions:* Walk me through your capstone architecture and the 3 hardest decisions. *Follow-ups:* "What breaks at 100×?" "Where does it cost the most and how would you cut it?" "How do you know it works?" (evals). *Scenario:* Live-debug a described capstone failure. *Common mistakes:* demo-only (no deploy/evals/observability), can't defend decisions. *Whiteboard:* your capstone architecture from memory.

**10. Common mistakes.** Leaving the capstone as a notebook demo; no deploy; weak README.

**11. Production best practices + mindset Q.** The capstone must pass all 13 production-mindset concerns or explicitly justify exceptions. *Mindset:* "Would I be comfortable putting this in front of real users on Monday?"

**12. Review.** Standard.

---

# WEEK 30 · 15–21 Feb 2027 — Portfolio polish (all 8 repos to hiring-committee grade)

**1. Objectives.** Every repo passes the Part 0 GitHub checklist and reads like a senior engineer wrote it; a portfolio landing page ties them together.

**2–5. Focus.** For each of the 8 projects: README (11-point), architecture diagram, ADR(s), evals with numbers, deploy guide, monitoring notes, "future improvements," clean commit history, tagged release, `.env.example`, secret scan (no leaks). Build a simple **portfolio index** (a repo/README or one-page site) linking projects, articles, ADRs, and design docs. Update your resume/LinkedIn with quantified outcomes.

**6. Hands-on project.** Portfolio finalization pass across all repos + portfolio index page.

**7. Deliverables.** 7–8 hiring-grade repos; portfolio index; updated resume + LinkedIn; all 8 articles published.

**8. GitHub milestones.** `docs: portfolio index`; per-repo `docs: README/diagram/ADR polish`.

**9. Interview prep.** *Questions:* Which project are you proudest of and why? Which decision would you now make differently? *Follow-ups:* per-project deep dives. *Scenario:* "Pick any repo — I'll ask about scaling/cost/failure." *Common mistakes:* inconsistent quality across repos, missing diagrams/evals, no through-line story. *Whiteboard:* your portfolio narrative arc (backend → production GenAI).

**10. Common mistakes.** One great repo + several weak ones; no unifying story; stale resume.

**11. Production best practices + mindset Q.** Consistency signals seniority. *Mindset:* "Does each repo prove I can build, operate, and decide — not just call an API?"

**12. Review.** Standard.

---

# WEEK 31 · 22–28 Feb 2027 — System design fluency & behavioral prep

**1. Objectives.** Design any of the target systems on a whiteboard in 40 min under questioning; tell crisp behavioral/story answers.

**2–5. Focus.** Drill the 7-part design method on all six prior exercises + new prompts (AI note-taker, customer-support copilot, code assistant, doc-intelligence platform). Behavioral: career-change narrative, "hardest bug," "a trade-off you made," "a time you were wrong," using STAR. Reading: two senior-interview / LLM-system-design prep posts; study one repo similar to your capstone and note what they did better.

**6. Hands-on project.** Produce a **system-design cheat-sheet** (`design/00-cheatsheet.md`): the 7-part method, latency/cost/failure checklists, reusable reference architectures (RAG, agent, multi-agent, platform).

**7. Deliverables.** Design cheat-sheet; a bank of ~10 rehearsed behavioral stories; 6+ timed design runs recorded.

**8. GitHub milestones.** `docs: system-design cheat-sheet`.

**9. Interview prep.** Full question banks from every month + follow-ups; timed whiteboard design; behavioral rehearsal. *Scenario:* Cold system-design prompt you haven't seen. *Common mistakes:* jumping to architecture before requirements/NFRs; no cost/failure analysis; rambling stories.

**10. Common mistakes.** Skipping requirements clarification; ignoring failure/cost; unstructured stories.

**11. Production best practices + mindset Q.** Always start with functional + non-functional requirements, end with failure + cost. *Mindset:* "Can I defend every box on the diagram and every number?"

**12. Review.** Standard.

---

# WEEK 32 · 1–7 Mar 2027 · 🔵 FINALE — Mock #8 (full loop), ADR-008, applications out

**Hands-on / activities:**
- **ADR-008** (`docs/adr/ADR-008.md`): capstone retrospective — the 3 decisions you'd defend hardest, what you'd change, and the triggers that would make you revisit them.
- **Article #8:** "What I learned building production GenAI systems in 8 months" + capstone case study (your best hiring-signal piece).
- **System Design #7:** a full **timed mock** on a fresh prompt (record + self-critique against the cheat-sheet).
- **Mock Interview #8 — full loop (~3–4h across the weekend):** behavioral + a Python/async coding round + a technical deep-dive (RAG/agents/LLMOps) + a system-design round + your capstone walkthrough. Have a peer or record and self-score.
- **Applications:** finalize resume + LinkedIn + portfolio index; ship the **Job Application Checklist** from the Finale doc — target list, tailored applications, outreach messages, and a tracking sheet.

**Reading set logged.** Complete the 8-month `reading-log.md`.

### End of Month 8 — Assessment (graduation)
- [ ] **Capstone v1.0** deployed, load-tested, observed, guarded, documented + demo.
- [ ] **7–8 hiring-grade repos**, all 8 **articles** published, all **ADRs** and **design docs** complete.
- [ ] **8 mock interviews** done (incl. a full loop); system-design fluency demonstrated.
- [ ] Resume/LinkedIn/portfolio index live; **applications submitted** and tracked.
- [ ] Skill matrix (Part 1) re-scored: core items at 🔵 production-ready.
- [ ] **Portfolio: 8/8.** You can design, build, deploy, monitor, optimize, secure, and maintain enterprise GenAI systems — and prove it.

*End of Part 9. See the Finale doc for the final portfolio review, mock-interview roadmap, system-design roadmap, production-readiness checklist, and job-application checklist.*
