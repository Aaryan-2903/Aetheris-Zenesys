# ProcuraIQ — Project Tracker

**Version:** 0.1  
**Last Updated:** 2026-08-22  
**Status:** Documentation Phase Complete — Implementation Not Yet Started

---

## Current Phase: Documentation ✓

---

## Phase 0 — Documentation Foundation

- [x] Create `docs/` directory
- [x] `prd.md` — Product Requirements Document
- [x] `techspec.md` — Technical Specification
- [x] `app-flow.md` — Application Flow
- [x] `design.md` — Design Specification
- [x] `schema.md` — Database Schema
- [x] `implementation-plan.md` — Implementation Plan
- [x] `tracker.md` — This file
- [x] `rules.md` — Project Constraints and Rules
- [x] `skill.md` — AI Agent Instructions

---

## Phase 1 — Environment Setup

- [ ] Python virtual environment created
- [ ] Backend dependencies installed
- [ ] `requirements.txt` initialized
- [ ] Frontend scaffolded with Vite + React
- [ ] Frontend dependencies installed
- [ ] `.env` file created (not committed)
- [ ] `.gitignore` configured
- [ ] Supabase project created and credentials available

---

## Phase 2 — Database Setup

- [ ] All 6 tables created in Supabase
- [ ] Indexes created
- [ ] CHECK constraints verified
- [ ] Seed vendors inserted
- [ ] Supabase client connection verified from Python

---

## Phase 3 — Synthetic Data Generation

- [ ] `generate_data.py` written
- [ ] Vendor master data generated (20–30 vendors)
- [ ] 50,000 transaction rows generated with realistic correlations
- [ ] Data saved to `procurement_data.csv`
- [ ] `vendor_performance` aggregated and inserted to Supabase
- [ ] Correlation spot-check passed
- [ ] No data leakage verified

---

## Phase 4 — ML Model Training

- [ ] `train.py` written
- [ ] Feature columns defined and consistent with `techspec.md`
- [ ] 80/20 train/test split applied
- [ ] Random Forest trained
- [ ] Accuracy logged
- [ ] Precision logged
- [ ] Recall logged
- [ ] F1 logged
- [ ] `model.joblib` saved
- [ ] `feature_columns.json` saved

---

## Phase 5 — Backend API

- [ ] `main.py` — FastAPI app, CORS, health check
- [ ] `db/supabase_client.py` — connection and query helpers
- [ ] `models/schemas.py` — Pydantic schemas
- [ ] `GET /api/vendors` — working
- [ ] `GET /api/vendors/{id}` — working
- [ ] `POST /api/predict` — ML inference working
- [ ] `POST /api/score` — deterministic scoring working
- [ ] `POST /api/risk` — risk assessment working
- [ ] `POST /api/financial-exposure` — financial exposure working
- [ ] `POST /api/decide` — final decision working
- [ ] All endpoints tested (no mock data)
- [ ] Supabase reads/writes verified

---

## Phase 6 — Frontend

- [ ] Vite config with backend proxy
- [ ] `api/client.js` configured
- [ ] Global CSS applied (Inter font, color palette, layout shell)
- [ ] Sidebar navigation working
- [ ] `ProcurementRequest.jsx` — working
- [ ] `VendorComparison.jsx` — working
- [ ] `RiskAssessment.jsx` — working
- [ ] `FinancialExposure.jsx` — working
- [ ] `Decision.jsx` — working
- [ ] `Dashboard.jsx` — working
- [ ] All 5 components built
- [ ] Design validation checklist passed (no emojis, no neon, no AI graphics)

---

## Phase 7 — Integration Testing

- [ ] Full end-to-end flow tested
- [ ] Money At Risk numbers verified against inputs
- [ ] ML predictions verified as live (not mocked)
- [ ] Explanation text references actual values
- [ ] Edge cases tested
- [ ] No browser console errors

---

## Phase 8 — Deployment

- [ ] Backend deployed to Railway
- [ ] Railway environment variables set
- [ ] `/api/health` returning 200 from Railway URL
- [ ] Frontend deployed to Vercel
- [ ] `VITE_API_BASE_URL` set to Railway URL
- [ ] Full flow working from Vercel URL

---

## Phase 9 — Polish and Demo

- [ ] Visual consistency check passed
- [ ] No placeholder text in UI
- [ ] Demo scenario prepared and rehearsed
- [ ] GitHub repository clean
- [ ] README updated

---

## Open Items / Blockers

| Item | Status | Owner |
|---|---|---|
| Zenesys Enterprise Constraint | **PENDING — TO BE CONFIRMED FROM ORGANIZERS** | Member 2 (Business & Research) |
| What-If Simulation as innovation feature | **PENDING — depends on Enterprise Constraint** | Member 1 + Member 3 |
| Currency for financial exposure (default: INR ₹) | Assumed INR — confirm before demo | Member 3 |
| Supabase project credentials | Not yet created | Member 1 |
| Railway account | Not yet set up | Member 1 |
| Vercel account | Not yet set up | Member 1 |

---

## Notes

- Do not begin Phase 1 (Environment Setup) until this documentation review is complete.
- Do not add features not listed in `prd.md` without team agreement.
- All financial exposure numbers must be derivable from inputs. Any unexplained number is a bug.

---

*Update this file after completing each task.*
