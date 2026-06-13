# Requirements Specification

**Project:** Intelligent Healthcare Compliance & Safety Management System
**Group:** W — Abu Sufian · Xiao Liang · MSE800 Assessment 2
**GitHub:** https://github.com/liangxiaoisme/MSE800
**Methodology:** Agile Scrum — 3 Sprints × 2 weeks + 1 Release Week
**Companion documents:** [Agile Project Plan (README.md)](README.md) · [Auth module (Week10/Activity_1)](../../Week10/Activity_1/README.md)

---

## Introduction

The Intelligent Healthcare Compliance & Safety Management System is a full-stack web
platform that helps healthcare organisations keep their staff trained, their regulatory
requirements compliant, and their safety incidents tracked — supported by an AI chatbot
that answers safety questions from official policy documents using Retrieval-Augmented
Generation (RAG).

The system is built with a **Django + Django REST Framework** backend (modular 5-app
architecture), a **React + Vite** single-page frontend, a **PostgreSQL + pgvector**
database, and a RAG pipeline using **fastembed** for embeddings and **OpenRouter
(Llama 4 Maverick)** for answer generation. It is deployed at zero cost on Render
(API), Vercel (SPA), and Supabase (database).

This document lists the **functional** and **non-functional** requirements. Each
requirement has a brief description, the location where it is implemented or addressed,
and the sprint in which it was delivered.

| Sprint | Weeks | Theme |
|---|---|---|
| Sprint 1 | 1–2 | Foundation & Backend APIs |
| Sprint 2 | 3–4 | Frontend SPA + RAG Chatbot |
| Sprint 3 | 5–6 | Deployment, Testing & Polish |
| Release | 7 | Deploy, Train & Retrospect |

---

## 1. Functional Requirements

Functional requirements define **what the system does**. Each ID is traceable to a
sprint task in [README.md](README.md).

### 1.1 Accounts & Authentication

| ID | Requirement | Description | Where Implemented | Sprint |
|---|---|---|---|---|
| FR-01 | User registration | A new user can sign up with full name, date of birth, email, username, password, and role (STAFF/ADMIN). | `accounts/views.py` `register()`, `accounts/serializers.py` `RegisterSerializer`, `accounts/models.py` `User` | Sprint 1 (Task 1.2) |
| FR-02 | User login (JWT) | A registered user logs in with email + password and receives a JWT access + refresh token pair. | `accounts/views.py` `login()`, `accounts/services.py` `AuthService.generate_tokens()` | Sprint 1 (Task 1.7) |
| FR-03 | Token refresh | The client can exchange a valid refresh token for a new access token without re-login. | `/api/auth/token/refresh/` (Simple JWT), `accounts/urls.py` | Sprint 1 (Task 1.7) |
| FR-04 | View & edit profile | An authenticated user can view and update their full name, DOB, and username. | `accounts/views.py` `profile()` (GET/PUT), `UserProfileSerializer` | Sprint 1 (Task 1.7) |
| FR-05 | Change password | An authenticated user can change their password by supplying the current and new password. | `accounts/views.py` `change_password()`, `AuthService.change_password()` | Sprint 1 (Task 1.7) |
| FR-06 | Forgot password | A user can request a reset; a one-time, 30-minute reset link is emailed. Response is identical whether or not the email exists (anti-enumeration). | `accounts/views.py` `forgot_password()`, `PasswordResetService.send_reset_email()` | Sprint 1 (Task 1.7) |
| FR-07 | Reset password | A user sets a new password using a valid, unused, unexpired token; the token is consumed on use. | `accounts/views.py` `reset_password()`, `PasswordResetService.consume_token()`, `models.py` `PasswordResetToken` | Sprint 1 (Task 1.7) |
| FR-08 | Role-based access (RBAC) | STAFF and ADMIN roles gate sensitive actions (e.g. only ADMIN can resolve incidents). | `accounts/models.py` `User.Role` / `is_admin`, DRF `IsAuthenticated` permissions | Sprint 1 (Tasks 1.2, 1.10) |

### 1.2 Training

| ID | Requirement | Description | Where Implemented | Sprint |
|---|---|---|---|---|
| FR-09 | List training modules | Staff can view all available training modules. | `training` app API (module list), Dashboard/TrainingList page | Sprint 1 (Task 1.8) / Sprint 2 (Task 2.7) |
| FR-10 | View module & quiz | Staff can open a module and see its questions. | `training` app `Module`/`Question` models + detail API, `TrainingDetail` page | Sprint 1 (Task 1.8) / Sprint 2 (Task 2.7) |
| FR-11 | Submit quiz & grade | Staff submit quiz answers; the system grades and returns a score; enrollment is recorded. | `training` quiz submission endpoint (`/api/training/<id>/submit/`), `Enrollment` model | Sprint 1 (Task 1.8) |
| FR-12 | Enrollment tracking | The system tracks which staff have enrolled in / completed which modules. | `training` `Enrollment` model | Sprint 1 (Task 1.3) |

### 1.3 Compliance

| ID | Requirement | Description | Where Implemented | Sprint |
|---|---|---|---|---|
| FR-13 | List compliance requirements | View all regulatory requirements and their records. | `compliance` app `Requirement` / `ComplianceRecord` models + list API | Sprint 1 (Task 1.9) |
| FR-14 | Computed compliance status | On read, each record's status is computed as COMPLIANT / DUE / OVERDUE from due dates. | `compliance` API (computed status on read) | Sprint 1 (Task 1.9) |
| FR-15 | Status badges in UI | The frontend renders colour-coded status badges for each requirement. | `ComplianceList` page (status badges) | Sprint 2 (Task 2.8) |

### 1.4 Incidents

| ID | Requirement | Description | Where Implemented | Sprint |
|---|---|---|---|---|
| FR-16 | Report incident | Authenticated staff can create a safety incident with severity and description. | `incidents` app `Incident` model + create API, `IncidentForm` page | Sprint 1 (Task 1.10) / Sprint 2 (Task 2.9) |
| FR-17 | List incidents | Staff and admins can list incidents with severity/status. | `incidents` list API, `IncidentList` page | Sprint 1 (Task 1.10) |
| FR-18 | Resolve incident (admin) | An ADMIN can update an incident's status (e.g. mark RESOLVED). | `incidents` update API (admin-only), `Incident` status enum | Sprint 1 (Task 1.10) |

### 1.5 AI Chatbot (RAG)

| ID | Requirement | Description | Where Implemented | Sprint |
|---|---|---|---|---|
| FR-19 | Document ingestion | Policy documents are chunked (300 words, 50-word overlap), embedded, and stored as vectors. | `chatbot` `Document`/`Chunk` models, chunking + `ingest_docs` command | Sprint 2 (Tasks 2.10, 2.16) |
| FR-20 | Vector embedding | Text chunks and questions are embedded with fastembed (BAAI/bge-small-en, 384-dim). | fastembed integration in `chatbot` app | Sprint 2 (Task 2.11) |
| FR-21 | Semantic retrieval | A question retrieves the top-5 most similar chunks via pgvector L2 distance. | pgvector retrieval (`VectorField`, `L2Distance`) | Sprint 2 (Task 2.12) |
| FR-22 | AI answer generation | Retrieved chunks + question are sent to OpenRouter (Llama 4 Maverick) to generate a sourced answer. | OpenRouter chat call, RAG prompt template | Sprint 2 (Task 2.13) |
| FR-23 | Graceful fallback | If the API key is missing or the call fails, the system returns the raw retrieved chunks instead of erroring. | RAG fallback logic in `chatbot` app | Sprint 2 (Task 2.14) |
| FR-24 | Chat widget UI | A floating chat button opens a slide-out panel to ask questions and view answers. | `ChatWidget` React component | Sprint 2 (Task 2.15) |

### 1.6 Cross-cutting Frontend

| ID | Requirement | Description | Where Implemented | Sprint |
|---|---|---|---|---|
| FR-25 | Dashboard summary | A landing dashboard shows summary cards (training, compliance, incidents). | `Dashboard` page (3 API calls) | Sprint 2 (Task 2.6) |
| FR-26 | Auth-aware API client | The SPA auto-attaches the JWT to requests and redirects to login on 401. | Axios client with JWT interceptor, `AuthContext` | Sprint 2 (Tasks 2.2, 2.3) |
| FR-27 | Navigation layout | Persistent sidebar navigation and header across authenticated pages. | `Layout` component (sidebar, header, Outlet) | Sprint 2 (Task 2.5) |

---

## 2. Non-Functional Requirements

Non-functional requirements define **how well** the system behaves — quality
attributes and constraints.

| ID | Category | Requirement | Description | Where Addressed | Sprint |
|---|---|---|---|---|---|
| NFR-01 | Security | Password hashing | Passwords are stored only as Django/bcrypt hashes, never plaintext. | Django auth (`set_password`), `accounts/models.py` | Sprint 1 |
| NFR-02 | Security | Stateless JWT auth | Access tokens expire in 1 hour, refresh in 7 days; no server session store needed. | Simple JWT settings in `healthcare_auth/settings.py` | Sprint 1 |
| NFR-03 | Security | One-time reset tokens | Reset tokens are random (32-byte URL-safe), single-use, and expire in 30 minutes. | `PasswordResetToken` (`secrets.token_urlsafe`, `is_valid()`) | Sprint 1 |
| NFR-04 | Security | Anti-enumeration | Forgot-password always returns the same response regardless of email existence. | `PasswordResetService.send_reset_email()` | Sprint 1 |
| NFR-05 | Security | Role-based authorisation | Sensitive operations are restricted by role; protected endpoints require a valid JWT. | DRF permission classes, `User.is_admin` | Sprint 1 |
| NFR-06 | Security | Secret management | Secrets (DB URL, API keys, Django secret) are read from environment variables, never committed. | 12-factor settings, `.env.example` | Sprint 1 (1.1) / Sprint 3 (3.12) |
| NFR-07 | Maintainability | Layered architecture | Views are thin; all business logic lives in a service layer; models hold data only. | `accounts/views.py` ↔ `services.py` ↔ `models.py` separation | Sprint 1 |
| NFR-08 | Maintainability | Modular app structure | Backend is split into 5 cohesive apps (accounts, training, compliance, incidents, chatbot). | Django project layout | Sprint 1 (1.1–1.6) |
| NFR-09 | Usability | Responsive UI | Layout adapts to mobile and tablet breakpoints. | Responsive CSS polish | Sprint 3 (3.10) |
| NFR-10 | Usability | Loading & error states | Pages show loading indicators / error boundaries; chatbot shows a spinner and cold-start message. | Loading states & error boundaries on all pages | Sprint 3 (3.11) |
| NFR-11 | Reliability | Graceful degradation | The chatbot never hard-fails; missing AI key → returns raw source chunks. | RAG fallback (FR-23) | Sprint 2 (2.14) |
| NFR-12 | Performance | Lightweight embeddings | Embedding model (bge-small-en) fits within Render's 512 MB free-tier RAM. | fastembed model choice | Sprint 2 (2.11) |
| NFR-13 | Portability | Cloud deployability | The system deploys to free managed services via config files and a single git push. | `render.yaml`, `vercel.json`, Gunicorn | Sprint 3 (3.1, 3.2, 3.4, 3.5) |
| NFR-14 | Portability | Interoperability (CORS) | The SPA on Vercel can call the API on Render via configured CORS. | CORS config in `settings.py` | Sprint 1 (1.1) / Sprint 3 (3.9) |
| NFR-15 | Cost | Zero-cost operation | The entire stack runs on free tiers (Render, Vercel, Supabase, OpenRouter). | Deployment architecture | Sprint 3 |
| NFR-16 | Testability | Verifiable acceptance | Each sprint defines a Definition of Done and an end-to-end demo flow that is manually verified. | Sprint Reviews in [README.md](README.md) | Sprints 1–3 |
| NFR-17 | Documentation | Comprehensive docs | Spec, Agile plan, READMEs, requirements, and retrospectives are maintained in the repo. | This file, README.md, Week10 README | Release Week 7 |
| NFR-18 | Data integrity | Referential integrity | Reset tokens cascade-delete with their user; unique constraints on email/username/token. | Model `ForeignKey(on_delete=CASCADE)`, `unique=True` fields | Sprint 1 |

---

## 3. Traceability Summary

| Sprint | Functional Requirements | Non-Functional Requirements |
|---|---|---|
| Sprint 1 (Foundation & APIs) | FR-01–FR-14, FR-16–FR-18 | NFR-01–NFR-08, NFR-14, NFR-18 |
| Sprint 2 (Frontend + RAG) | FR-09–FR-11, FR-15–FR-17, FR-19–FR-27 | NFR-11, NFR-12 |
| Sprint 3 (Deploy & Polish) | (hardening of all above) | NFR-09, NFR-10, NFR-13, NFR-15 |
| Release Week 7 | — | NFR-16, NFR-17 |

> **Definition of Done (all sprints):** code committed, manually tested against
> acceptance criteria, no regressions — see [README.md](README.md).
</content>
</invoke>
