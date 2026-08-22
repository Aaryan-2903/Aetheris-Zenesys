# ProcuraIQ — Implementation Plan

**Version:** 0.1 — Hackathon Draft  
**Last Updated:** 2026-08-22  
**Status:** Draft — Not yet started

---

## 1. Overview

Total build time: **~8 hours** (12-hour hackathon, 4 hours reserved for evaluation/presentation)

**Dependency order:**

```
Database Schema → Data Generation → ML Training → Backend → Frontend → Integration → Deploy
```

Each phase depends on the previous. Do not start a phase before its dependencies are complete.

---

## 2. Phase 0 — Environment Setup (Est. 20 min)

### Tasks

- [ ] Create Python virtual environment (`backend/venv`)
- [ ] Install backend dependencies: FastAPI, uvicorn, pandas, numpy, scikit-learn, joblib, supabase-py, psycopg2-binary, python-dotenv
- [ ] Scaffold frontend with `npx create-vite@latest frontend --template react`
- [ ] Install frontend dependencies: `axios`
- [ ] Create `.env` file with Supabase credentials (never commit this file)
- [ ] Ensure `.gitignore` covers: `venv/`, `node_modules/`, `.env`, `*.joblib`, `__pycache__/`
- [ ] Initialize `backend/requirements.txt`
- [ ] Verify Supabase project is created and credentials are available

### Deliverable

Working dev environment for both frontend and backend.

---

## 3. Phase 1 — Database Setup (Est. 30 min)

### Dependencies

- Phase 0 complete
- Supabase project created

### Tasks

- [ ] Run all SQL from `schema.md` in Supabase SQL editor
- [ ] Verify all 6 tables created successfully
- [ ] Verify indexes created
- [ ] Verify CHECK constraint on `procurement_requests.weight_*`
- [ ] Insert 5–10 seed vendors manually for early testing
- [ ] Test basic Supabase client connection from backend (`db/supabase_client.py`)

### Deliverable

All tables created in Supabase. Connection verified from Python.

---

## 4. Phase 2 — Synthetic Data Generation (Est. 45 min)

### Dependencies

- Phase 1 complete (vendor seeds must exist to reference)
- `backend/ml/generate_data.py`

### Design Principles

- Data must contain **real relationships** — not independent random columns
- Outcome (`outcome = 1`) must be significantly more likely when:
  - `on_time_delivery_rate` is high
  - `quality_score` is high
  - `lead_time` is not exceeded
  - `defect_rate` is low
- Outcome must be less likely when:
  - `advance_payment_pct` is very high with a new vendor
  - `order_complexity` is high and vendor has low experience
- ~50,000 rows total
- Realistic category distribution: IT Equipment, Stationery, Office Supplies, Raw Materials, Equipment, Consumables, Furniture

### Tasks

- [ ] Write `generate_data.py`
- [ ] Generate vendor master data (20–30 vendors, varied by category)
- [ ] Generate 50,000 transaction rows with realistic correlations
- [ ] Save to `backend/ml/procurement_data.csv`
- [ ] Aggregate into `vendor_performance` per vendor per category
- [ ] Insert vendors and vendor_performance into Supabase
- [ ] Spot-check: verify outcome correlation with delivery rate and quality score
- [ ] Verify no data leakage patterns (no target-derived features)

### Deliverable

`procurement_data.csv` with 50,000 rows. Supabase populated with vendor data.

---

## 5. Phase 3 — ML Model Training (Est. 45 min)

### Dependencies

- Phase 2 complete (`procurement_data.csv` exists)
- `backend/ml/train.py`

### Tasks

- [ ] Write `train.py`
- [ ] Load `procurement_data.csv`
- [ ] Define feature columns (see `techspec.md` — Section 3.3)
- [ ] Encode categorical features (vendor, category) — use label encoding or ordinal encoding
- [ ] Perform 80/20 train/test split using `train_test_split` with `random_state` fixed
- [ ] Train Random Forest Classifier (`n_estimators=100`, `random_state=42`)
- [ ] Evaluate on test set: Accuracy, Precision, Recall, F1
- [ ] Print and log all 4 metrics — do NOT fabricate or manually adjust
- [ ] Save model: `joblib.dump(model, 'backend/ml/model.joblib')`
- [ ] Save feature column list: `backend/ml/feature_columns.json` (for inference consistency)

### Deliverable

`model.joblib` trained and saved. All 4 metrics logged. Feature columns documented.

---

## 6. Phase 4 — Backend API (Est. 2.5 hours)

### Dependencies

- Phase 1 complete (Supabase)
- Phase 3 complete (`model.joblib`)

### 6.1 Foundation

- [ ] Create `backend/main.py` — FastAPI app with CORS, router registration, health check
- [ ] Create `backend/db/supabase_client.py` — Supabase client wrapper with helper functions
- [ ] Create `backend/models/schemas.py` — all Pydantic request/response models

### 6.2 Vendor Router (`routers/vendors.py`)

- [ ] `GET /api/vendors` — list active vendors with category filter
- [ ] `GET /api/vendors/{id}` — vendor detail with performance data

### 6.3 ML Service + Prediction Router

- [ ] `services/procurement_prediction_service.py` — load `model.joblib`, load `feature_columns.json`, inference function
- [ ] `routers/predict.py` — `POST /api/predict` — takes vendor+order params, returns predictions

### 6.4 Scoring Service + Router

- [ ] `services/scoring_service.py` — deterministic scoring formula (see `techspec.md` Section 4.4)
- [ ] `routers/procurement.py` — `POST /api/score` — returns composite scores per vendor

### 6.5 Risk Service + Router

- [ ] `services/risk_service.py` — risk calculation per vendor using performance data
  - Delivery Risk Score
  - Quality Risk Score
  - Supplier Concentration Risk
  - Payment/Advance Risk
  - Supplier Health Score (aggregate)
  - Risk level thresholds: Low < 0.33, Medium 0.33–0.66, High > 0.66
- [ ] `routers/risk.py` — `POST /api/risk`

### 6.6 Financial Exposure Service + Router

- [ ] `services/financial_service.py` — deterministic formulas for all 5 risk components
  - All formulas reference actual inputs — no hardcoded exposure values
  - Protection actions calculated based on component exposure levels
- [ ] `routers/financial.py` — `POST /api/financial-exposure`

### 6.7 Decision Router

- [ ] `routers/procurement.py` — `POST /api/decide` — combines ML + scoring + risk + financial to produce final recommendation
- [ ] Persist decision and financial exposure to Supabase

### 6.8 Validation

- [ ] Test all endpoints with curl / Postman
- [ ] Verify no endpoint returns hardcoded mock data
- [ ] Verify Supabase reads/writes working

### Deliverable

All 8 API endpoints working. No mock/hardcoded data.

---

## 7. Phase 5 — Frontend (Est. 2 hours)

### Dependencies

- Phase 4 complete (backend running locally)

### 7.1 Foundation

- [ ] Configure `vite.config.js` with proxy to backend (for local dev)
- [ ] Create `src/api/client.js` — axios instance with base URL from env
- [ ] Apply global CSS from `design.md` — typography, colors, layout shell

### 7.2 Application Shell

- [ ] `App.jsx` — router setup, sidebar, layout
- [ ] Sidebar navigation with 4 links: Dashboard, New Request, Vendor Database, History

### 7.3 Pages (in priority order)

- [ ] `ProcurementRequest.jsx` — requirement form (Step 1)
- [ ] `VendorComparison.jsx` — sortable vendor table with scores and ML predictions (Step 2)
- [ ] `RiskAssessment.jsx` — risk breakdown table for selected vendor (Step 3)
- [ ] `FinancialExposure.jsx` — Money At Risk table + protection actions (Step 4)
- [ ] `Decision.jsx` — final decision card with rationale (Step 5)
- [ ] `Dashboard.jsx` — summary stats + recent decisions table

### 7.4 Components

- [ ] `VendorTable.jsx`
- [ ] `RiskIndicator.jsx`
- [ ] `ScoreBar.jsx`
- [ ] `ExposureBreakdown.jsx`
- [ ] `DecisionCard.jsx`

### 7.5 Design Validation

- [ ] Verify: no emojis in UI
- [ ] Verify: no neon/glow effects
- [ ] Verify: no decorative AI graphics
- [ ] Verify: all tables sortable where specified
- [ ] Verify: risk colors are functional (Low/Medium/High)
- [ ] Verify: font is Inter, not a decorative font

### Deliverable

All 5 decision-flow pages working. Data flowing from backend API to frontend display.

---

## 8. Phase 6 — Integration Testing (Est. 45 min)

### Tasks

- [ ] Run full end-to-end flow: define requirement → see vendors → see risk → see exposure → see decision
- [ ] Verify all Money At Risk numbers trace to actual inputs (no hardcoded values)
- [ ] Verify ML predictions are live from model, not mocked
- [ ] Verify explanation text references actual calculated values
- [ ] Test edge cases: vendor with no history, high-risk vendor, very high advance payment
- [ ] Check browser console for errors

### Deliverable

Complete end-to-end flow working without errors.

---

## 9. Phase 7 — Deployment (Est. 30 min)

### 9.1 Backend (Railway)

- [ ] Create `Procfile` or `railway.toml` with startup command
- [ ] Push backend to Railway
- [ ] Set environment variables in Railway: `SUPABASE_URL`, `SUPABASE_KEY`
- [ ] Verify `/api/health` returns 200 from Railway URL

### 9.2 Frontend (Vercel)

- [ ] Connect GitHub repo to Vercel
- [ ] Set `VITE_API_BASE_URL` to Railway backend URL
- [ ] Deploy and verify frontend loads
- [ ] Verify all API calls reach Railway backend

### Deliverable

Frontend live on Vercel. Backend live on Railway. Full flow accessible from public URL.

---

## 10. Phase 8 — Polish and Demo Prep (Remaining time)

### Tasks

- [ ] Check all pages for visual consistency against `design.md`
- [ ] Ensure no placeholder text remains in UI
- [ ] Prepare demo scenario: specific category, vendors, order — rehearse full flow
- [ ] Confirm GitHub repository is clean and README is present

### Deliverable

Demo-ready application. Clean GitHub repository.

---

## 11. Dependency Graph

```
Phase 0 (Environment)
    └── Phase 1 (Database)
            └── Phase 2 (Data Generation)
                    └── Phase 3 (ML Training)
                            └── Phase 4 (Backend) ──┐
                                                     └── Phase 5 (Frontend)
                                                              └── Phase 6 (Integration)
                                                                       └── Phase 7 (Deploy)
                                                                                └── Phase 8 (Polish)
```

---

## 12. Risk and Contingency

| Risk | Mitigation |
|---|---|
| Supabase setup takes too long | Pre-create tables before hackathon if possible |
| ML model accuracy too low | Adjust data generation relationships; do not fabricate metrics |
| Railway deployment fails | Have localhost demo as fallback for judging |
| Frontend styling takes too long | Use a clean minimal CSS rather than over-designing |
| Feature creep | Refer to `prd.md` — anything not in scope is not built |

---

*This document is the source of truth for the build sequence and dependencies.*
