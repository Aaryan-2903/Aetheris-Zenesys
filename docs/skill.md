---
name: procuraiq-agent
description: >
  Instructions for Antigravity and all AI coding agents working on ProcuraIQ.
  Contains coding conventions, architecture rules, UI rules, data integrity rules,
  and the complete AI Slop Killer anti-pattern checklist.
  Every agent working on this project MUST read this file before writing any code.
---

# ProcuraIQ — Agent Skill File

**Version:** 0.2  
**Last Updated:** 2026-08-22  
**Applies To:** All AI coding agents (Antigravity, Copilot, etc.) working on ProcuraIQ

---

## MANDATORY: READ THIS BEFORE WRITING ANY CODE

This file contains binding instructions for every AI agent working on ProcuraIQ.  
Failure to follow these instructions produces incorrect, misleading, or low-quality output.

---

## 1. Project Context

ProcuraIQ is a **procurement decision-support system**.

- It is NOT a generic SaaS app.
- It is NOT a consumer product.
- It is NOT a marketing landing page.
- It is a focused, lightweight, enterprise procurement decision tool.

USP: *"ProcuraIQ turns vendor comparison into a predictive, priority-aware and explainable procurement decision."*

Core decision flow: **Predict → Prioritize → Assess Risk → Explain → Decide**

Before making ANY change, read the relevant documentation:

| Want to change... | Read... |
|---|---|
| What features to build | `docs/prd.md` |
| Architecture or API | `docs/techspec.md` |
| UI or design | `docs/design.md` |
| Database schema | `docs/schema.md` |
| Build sequence | `docs/implementation-plan.md` |
| Formulas or constraints | `docs/rules.md` |
| User workflow | `docs/app-flow.md` |
| Project status | `docs/tracker.md` |

**Documentation is the source of truth. Do not invent requirements.**

---

## 2. Architecture Rules

### 2.1 Layer Separation — CRITICAL

There are five distinct layers. Each has a defined role. Never conflate them.

| Layer | Role | Owner |
|---|---|---|
| Procurement Prediction | Predict procurement outcome independently | `procurement_prediction_service.py` + `model.joblib` |
| Deterministic Business Scoring | Score and rank vendors independently | `scoring_service.py` |
| Risk Calculation | Calculate risk scores independently | `risk_service.py` |
| Financial Exposure | Calculate Money At Risk | `financial_service.py` |
| AI Explanation | Explain computed values in natural language | Template or LLM with computed inputs only |

**Rules:**
- ML model does not calculate scores or risks
- Business scoring does not use ML output as a component — it is computed independently from vendor attributes
- Risk calculation does not depend on ML output — it is derived from historical performance data
- Financial exposure does not use LLM-generated numbers
- LLM/AI explanation only receives computed values as structured input — it does not generate metrics

**Final Decision Engine:**
The final procurement recommendation (`POST /api/decide`) is the ONLY layer that combines outputs from multiple layers. It may combine:
- ML predicted outcome and confidence (from ML Prediction layer)
- Composite vendor score (from Business Scoring layer)
- Risk level and Supplier Health Score (from Risk Calculation layer)

This combination happens in the decision layer only. The individual layers above remain independent of each other.

### 2.2 Do Not Invent

Do NOT invent:
- API endpoints not in `techspec.md`
- Database tables or columns not in `schema.md`
- ML features not in `techspec.md` Section 3.3
- Financial formulas not in `rules.md` Section 1 Layer 4
- Risk formulas not in `rules.md` Section 1 Layer 3
- UI pages not in `design.md`

If something is missing from the documentation, ask a human — do not invent it.

### 2.3 Do Not Add Dependencies Without Justification

Before adding to `requirements.txt` or `package.json`:
- State what the dependency does
- State why an existing library cannot do it
- State whether it is needed for MVP scope

Lightweight hackathon project — do not bloat dependencies.

---

## 3. Backend Coding Conventions

### 3.1 File and Module Structure

Always follow the module structure defined in `techspec.md` Section 4.2.

Do not create new service files without updating `techspec.md`.

### 3.2 FastAPI Conventions

- Use Pydantic models for all request/response bodies
- Define all schemas in `models/schemas.py`
- Use dependency injection for Supabase client if needed
- CORS must be configured in `main.py` — only allow the frontend domain
- Include `GET /api/health` for uptime monitoring

### 3.3 ML Inference Conventions

- Load `model.joblib` and `feature_columns.json` once during application startup — use FastAPI's modern lifespan pattern (`@asynccontextmanager` with `lifespan=` argument on the `FastAPI()` constructor) rather than the deprecated `@app.on_event("startup")` decorator
- Store the loaded model and feature columns in application state so they are accessible to route handlers without reloading
- Never reload the model per request
- Never reconstruct feature columns at inference time — always use the saved list
- Input data to the model must match training feature columns exactly (name and order)
- Inference returns `predicted_outcome` (int) and `confidence_score` (float 0–1)

### 3.4 Database Conventions

- All queries go through `db/supabase_client.py`
- No raw SQL in route handlers
- No credentials in source code — use environment variables via `python-dotenv`
- Use `.env` for local development, Railway environment variables for production
- Never commit `.env` to git

### 3.5 Financial Exposure Conventions

- All formula coefficients are in `rules.md` Section 1 Layer 4
- Do not change coefficients without updating `rules.md` first
- Save `calculation_inputs` to the `financial_exposures` table for every calculation
- Round currency values to 2 decimal places for display only; keep full precision internally

---

## 4. ML Conventions

### 4.1 Data Generation (`generate_data.py`)

- Generate ~50,000 rows
- Categories: IT Equipment, Stationery, Office Supplies, Raw Materials, Equipment, Consumables, Furniture
- Outcome must be correlated with delivery rate, quality score, defect rate, order complexity
- Do NOT generate independent random columns
- Save to `backend/ml/procurement_data.csv`

### 4.2 Training (`train.py`)

- Use `random_state=42` for reproducibility
- 80/20 split with `train_test_split(..., random_state=42, stratify=y)`
- Features: see `techspec.md` Section 3.3
- No target-derived features in the feature set
- Compute and print: Accuracy, Precision, Recall, F1
- Save: `model.joblib`, `feature_columns.json`
- Do NOT modify metrics output. Report whatever the model produces.

### 4.3 Model File

- `model.joblib` is the only inference artifact
- Feature columns from `feature_columns.json` must be used at inference time
- Both files must exist in `backend/ml/` before the backend can start

---

## 5. Frontend Coding Conventions

### 5.1 Stack

- React 18 + Vite
- CSS: plain CSS modules or a single global stylesheet
- HTTP: axios via `src/api/client.js`
- No CSS-in-JS libraries (styled-components, emotion) — not needed for MVP
- No Tailwind — not in scope

### 5.2 Component Conventions

- Each page has its own file in `src/pages/`
- Shared components in `src/components/`
- API calls only in `src/api/client.js` or custom hooks in `src/hooks/`
- No inline API calls inside components

### 5.3 State Management

- React `useState` and `useContext` only
- No Redux, Zustand, or Recoil for MVP
- Procurement session data flows top-down; lift state to `App.jsx` or a context provider if needed

---

## 6. AI Slop Killer — Anti-Pattern Checklist

**Before completing any UI change, verify the following list. Violations must be corrected.**

### 6.1 Typography

- [ ] Font is a professional enterprise or system UI font — see `design.md` Section 3.1 for the current approved choice; do not introduce a decorative, futuristic, novelty, or AI-template typeface
- [ ] Do not add a Google Fonts dependency solely for aesthetics; if a web font is used, it must be justified as more readable than the system font stack for this context
- [ ] Font size is 14px for body text, 13px for table cells, 24px for page titles
- [ ] No "AI-looking" display fonts
- [ ] Font rendering is readable at normal viewing distance
- [ ] The final font selection is owned by the frontend team and must comply with `design.md`

### 6.2 Color and Visual Effects

- [ ] No neon colors (electric blue, neon green, hot pink)
- [ ] No glowing/luminous effects (`text-shadow`, `box-shadow` glow variants)
- [ ] No glassmorphism (`backdrop-filter: blur` on primary surfaces)
- [ ] No gradient backgrounds used decoratively
- [ ] All colors are from the approved palette in `design.md` Section 3.2
- [ ] Risk level indicators use ONLY: green (#16A34A), amber (#D97706), red (#DC2626)

### 6.3 Layout and Structure

- [ ] No huge hero sections or marketing banners
- [ ] No decorative AI graphics (robots, brains, sparkles, circuit patterns)
- [ ] No excessive rounded corners (> 8px border-radius on data containers)
- [ ] No excessive pill shapes used as primary layout elements
- [ ] Primary data display is in TABLES, not cards

### 6.4 Animations and Motion

- [ ] No decorative animations (floating elements, pulse effects, continuous motion)
- [ ] Hover effects are subtle: background-color shift only
- [ ] No animated chart entrances
- [ ] No typewriter text effects
- [ ] Transitions: max 150ms, purpose is feedback not aesthetics

### 6.5 Content and Copy

- [ ] NO EMOJIS anywhere in the product UI
- [ ] "AI-powered" does not appear repeatedly in the UI
- [ ] No marketing copy masquerading as UI text
- [ ] All visible numbers on screen can be traced to actual calculated data
- [ ] No placeholder text (`Lorem ipsum`, `TBD`, `Coming soon`) in shipped UI

### 6.6 Functional Purpose Check

For every UI element, ask: **"Does this element serve a procurement function?"**

If the answer is NO → remove it.

---

## 7. Fabrication Kill Rules

These are absolute prohibitions. If you find yourself writing any of the following, STOP and reconsider.

**NEVER:**
- Hardcode a vendor score: `const score = 0.87`
- Hardcode a risk level: `const risk = "Low"`
- Hardcode a Money At Risk amount: `const mar = 45000`
- Fabricate ML metrics: `return { accuracy: 0.91, f1: 0.88 }`
- Write explanation text that doesn't reference actual computed values
- Return mock data from an API endpoint that should call real services
- Use `Math.random()` to generate risk scores or financial exposure
- Use dummy data in production API responses
- Claim a vendor has "3 years of excellent performance" without this being in the database

**If data is missing:** Return a clear `null` or `undefined` and display a "Insufficient Data" indicator in the UI. Do NOT invent replacement values.

---

## 8. Scope Enforcement

Before building any feature, check it against `prd.md` Section 5.1 (In Scope).

Features NOT in scope for MVP:

- Live market pricing
- AI Negotiation Copilot
- Protection marketplace
- Mobile app
- Multi-tenant authentication
- Contract lifecycle management
- Supplier onboarding
- What-If Simulation *(PENDING — not confirmed as innovation)*

If an idea seems good but isn't in scope: document it as a future consideration, not in tracker. Do not build it.

---

## 9. Enterprise Constraint Protocol

**STATUS: PENDING — TO BE CONFIRMED FROM ORGANIZERS**

**Approved MVP features may be implemented while the Enterprise Constraint is pending.** The constraint does not block core implementation work.

Only features that are intended to satisfy or depend on the Enterprise Constraint must wait for confirmation. Specifically:

- What-If Decision Simulation remains unimplemented until the constraint is confirmed and reviewed.
- Do NOT pre-implement any feature assumed to match the Enterprise Constraint.

When the Enterprise Constraint is received:

1. Member 2 reviews it
2. Member 3 assesses product impact
3. Team decides if/how to implement
4. Update `prd.md`, `implementation-plan.md`, `tracker.md`
5. Then and only then: begin implementing any constraint-dependent feature

---

## 10. Hackathon Discipline Rules

You are working in an 8-hour build window. Every decision has a time cost.

- Prefer simple, reliable implementation over clever complexity
- Prefer one working feature over two half-built features
- If a decision takes more than 2 minutes to evaluate, pick the simpler option and move on
- The demo matters: make the end-to-end flow work before polishing
- If you're adding something not in `tracker.md`, question whether it should be added at all
- Update `tracker.md` when completing tasks — it is the live project state

---

## 11. Post-documentation Gate

**Before beginning implementation, confirm all of the following:**

- [ ] All 9 documentation files have been reviewed by the team
- [ ] Enterprise Constraint is known or explicitly deferred
- [ ] Team agrees on the demo scenario
- [ ] Required credentials and secrets are secured before the work that needs them begins

**Credential prerequisite scope:**
- Supabase credentials must be secured before database setup and backend integration work.
- Supabase is NOT a prerequisite for: synthetic dataset generation, ML training, or ML evaluation. Those phases may proceed independently.
- Railway and Vercel credentials are only needed at deployment time.

Documentation must be complete and consistent before agents begin writing code.

---

*These instructions are binding for all AI agents on this project.*
