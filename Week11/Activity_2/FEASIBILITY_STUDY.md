# Feasibility Study

**Project:** Intelligent Healthcare Compliance & Safety Management System
**Group:** W — Abu Sufian · Xiao Liang · MSE800 Assessment 2
**GitHub:** https://github.com/liangxiaoisme/MSE800
**Methodology:** Agile Scrum — 3 Sprints × 2 weeks + 1 Release Week
**Companion documents:** [Requirements Specification](../Activity_1/REQUIREMENTS.md) · [Agile Project Plan (Week9)](../../Week9/Activity_2/README.md) · [Auth module (Week10)](../../Week10/Activity_1/README.md)

---

## 1. Purpose

This feasibility study evaluates whether the Intelligent Healthcare Compliance &
Safety Management System is realistic and worth building before and during
implementation. It assesses the project across four dimensions — **technical,
operational, financial, and scheduling** — and concludes with an overall
justification of the proposed solution's viability.

Evidence is drawn from the already-delivered work in [Week9 (Agile plan)](../../Week9/Activity_2/README.md)
and [Week10 (working authentication module)](../../Week10/Activity_1/README.md), which
together demonstrate that the chosen approach is not only proposed but partially proven.

---

## 2. Project Summary

The system helps healthcare organisations keep staff **trained**, regulatory
requirements **compliant**, and safety **incidents** tracked, supported by an AI
chatbot that answers safety questions from official policy documents using
Retrieval-Augmented Generation (RAG).

**Proposed technology stack:**

| Layer | Technology |
|---|---|
| Backend | Django + Django REST Framework (modular 5-app architecture) |
| Frontend | React + Vite single-page application |
| Database | PostgreSQL + pgvector (vector search) |
| AI / RAG | fastembed (BAAI/bge-small-en, 384-dim) + OpenRouter (Llama 4 Maverick) |
| Auth | JWT (Simple JWT), role-based access (STAFF / ADMIN) |
| Hosting | Render (API), Vercel (SPA), Supabase (DB) — all free tiers |

---

## 3. Technical Feasibility

**Question: Can the team build it with the chosen technology?** — **Yes.**

| Factor | Assessment |
|---|---|
| **Proven core** | The authentication module (registration, JWT login, profile, change/forgot/reset password) is already implemented and working in [Week10/Activity_1](../../Week10/Activity_1/README.md). This de-risks the most security-sensitive part of the system. |
| **Mature frameworks** | Django + DRF and React + Vite are industry-standard, well-documented, and stable. No experimental or unsupported tooling is on the critical path. |
| **Walking-skeleton de-risking** | The Agile plan (Sprint 1) builds all 11 models and core APIs end-to-end first, so integration risks surface in Week 2, not at the end. The Sprint 1 retrospective confirms "pgvector integration worked on first attempt." |
| **AI/RAG novelty** | RAG (chunk → embed → retrieve → generate) is the least familiar component. This risk is mitigated by (a) a small, RAM-light embedding model that fits Render's 512 MB free tier, and (b) a **graceful fallback** (FR-23) that returns raw source chunks if the LLM key is missing or the call fails — so the feature degrades instead of breaking. |
| **Architecture quality** | Clean layered design (thin views → service layer → models) and a 5-app modular split keep the codebase maintainable as it grows. Demonstrated in the Week10 code. |
| **Skills fit** | A 2-person team has already produced a working Django module, evidencing the Python/Django skills needed for the remainder. |

**Conclusion:** Technically feasible. The hardest parts (auth, vector search) are
already proven; the remaining risk (LLM inference) has a working fallback.

---

## 4. Operational Feasibility

**Question: Will the system actually be used and fit real workflows?** — **Yes.**

| Factor | Assessment |
|---|---|
| **Clear user need** | Healthcare organisations have a genuine, ongoing obligation to track training, compliance, and incidents — a recurring administrative burden the system directly addresses. |
| **Defined roles** | Two roles (STAFF, ADMIN) map to real-world responsibilities: staff complete training and report incidents; admins resolve incidents and oversee compliance. RBAC is already implemented. |
| **Usability** | A React SPA with sidebar navigation, a summary dashboard, status badges (COMPLIANT/DUE/OVERDUE), responsive layout, and loading/error states (NFR-09, NFR-10) lowers the barrier to adoption. |
| **AI assistance** | The chatbot lets non-expert staff get sourced answers to safety questions instantly, instead of searching long policy PDFs — a concrete productivity gain. |
| **Low operational overhead** | Fully managed hosting (Render/Vercel/Supabase) means no servers to maintain; deployment is a single `git push`. |
| **Known limitation** | Render free-tier cold start (~30s on first request) is the main UX friction. Mitigated by a "Waking up server…" message and acknowledged honestly in documentation. |

**Conclusion:** Operationally feasible. The system fits real healthcare workflows,
serves clearly defined users, and is easy to adopt and run.

---

## 5. Financial Feasibility

**Question: Is it affordable to build and run?** — **Yes — effectively zero cost.**

| Cost item | Amount | Notes |
|---|---|---|
| Backend hosting (Render) | **$0** | Free tier, 512 MB RAM |
| Frontend hosting (Vercel) | **$0** | Free tier, SPA hosting |
| Database (Supabase PostgreSQL + pgvector) | **$0** | Free tier, 500 MB |
| LLM inference (OpenRouter, Llama 4 Maverick) | **$0** | Free model tier |
| Embeddings (fastembed) | **$0** | Runs locally in-process, no API |
| Development tools (Django, React, VS Code, Git) | **$0** | Open source / free |
| **Total cash cost** | **$0** | — |

**Cost–benefit:** The only real investment is the team's time across the 7-week
schedule. Against zero cash outlay, the system delivers a full-stack, AI-enabled
compliance platform. For a real deployment, the realistic upgrade costs are modest
and optional (e.g. a paid OpenRouter tier for faster inference, or a warm dyno to
remove cold starts) — these are improvements, not prerequisites.

**Conclusion:** Financially feasible. Zero build/run cost makes the project viable
with no budget risk; scaling costs are predictable and deferrable.

---

## 6. Scheduling Feasibility

**Question: Can it be delivered in the available time?** — **Yes.**

The project follows a **7-week Agile Scrum** schedule: 3 two-week sprints plus a
release week. Sprint scope and outcomes are documented in [Week9/Activity_2](../../Week9/Activity_2/README.md).

| Sprint | Weeks | Goal | Status (per plan) |
|---|---|---|---|
| Sprint 1 — Foundation & Backend APIs | 1–2 | Models, JWT auth, CRUD APIs, seed data | Tasks 1.1–1.12 **Done** |
| Sprint 2 — Frontend + RAG Chatbot | 3–4 | React SPA + full RAG pipeline | Tasks 2.1–2.17 **Done** |
| Sprint 3 — Deployment & Polish | 5–6 | Live deploy, E2E test, UI polish | Tasks 3.1–3.13 **Done** |
| Release Week | 7 | Deploy, train, demo, retrospect | Planned |

| Factor | Assessment |
|---|---|
| **Incremental delivery** | Working software every 2 weeks reduces the risk of a last-minute crunch; each sprint ends in a verified demo. |
| **Front-loaded risk** | The riskiest integration (full-stack skeleton, pgvector) is scheduled first, leaving later sprints for polish, not firefighting. |
| **Buffer** | Week 7 is reserved for deployment, documentation, and demo — a built-in buffer against slippage. |
| **Demonstrated progress** | The completed auth module and the marked-Done sprint task tables show the schedule is being met, not just planned. |
| **Small-team agility** | A 2-person team with async standups keeps coordination overhead low. |

**Conclusion:** Schedulable. The 3-sprint plan is realistic, front-loads risk, and
the evidence to date shows the timeline is being honoured.

---

## 7. Overall Viability & Justification

| Dimension | Verdict | Key justification |
|---|---|---|
| Technical | ✅ Feasible | Core auth + vector search already proven; RAG has a working fallback |
| Operational | ✅ Feasible | Real need, defined roles, usable UI, low maintenance |
| Financial | ✅ Feasible | $0 cash cost; optional, deferrable scaling costs |
| Scheduling | ✅ Feasible | Realistic 7-week sprint plan, risk front-loaded, progress evidenced |

**Overall conclusion:** The Intelligent Healthcare Compliance & Safety Management
System is **viable on all four dimensions**. It solves a genuine healthcare problem
with mature, well-understood technology; it serves clearly defined users through an
accessible interface; it costs nothing to build or run; and it fits comfortably
within a 7-week Agile schedule whose early sprints are already delivered and
verified. The biggest uncertainty — AI inference reliability — is contained by a
graceful-degradation fallback, so the project remains viable even in the
worst-case AI scenario.

**Recommendation: Proceed.** The proposed solution is justified and the project
should continue to delivery as planned.
</content>
