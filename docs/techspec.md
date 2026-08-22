# ProcuraIQ — Technical Specification

**Version:** 0.3 — Hackathon Draft  
**Last Updated:** 2026-08-22  
**Status:** Draft

---

## 1. Architecture Overview

ProcuraIQ follows a three-tier architecture:

```
[React/Vite Frontend]  ←→  [FastAPI Backend]  ←→  [Supabase/PostgreSQL]
                                  ↕
                          [ML Model (joblib)]
```

**Architectural Principle:**

- ML predicts outcomes.
- Deterministic business logic scores, ranks, and calculates financial exposure.
- AI (LLM), if used at all, explains computed values — it does NOT generate them.

---

## 2. Components

| Layer | Technology | Responsibility |
|---|---|---|
| Frontend | React + Vite | User interface, decision flow, data display |
| Backend | Python + FastAPI | API layer, business logic, ML inference, financial engine |
| ML Model | Scikit-learn (Random Forest) | Procurement outcome prediction |
| Database | Supabase (PostgreSQL) | Vendor data, transaction history, procurement requests |
| Deployment (FE) | Vercel | Frontend hosting |
| Deployment (BE) | Railway | Backend + ML model hosting |

---

## 3. ML Architecture

### 3.1 Model

- **Algorithm:** Random Forest Classifier
- **Library:** Scikit-learn
- **Serialization:** Joblib → `model.joblib`

### 3.2 Training Data

- **Size:** ~50,000 synthetic procurement transactions
- **Split:** 80% train / 20% test
- **Leakage prevention:** No target-derived features in inputs; split before any feature engineering derived from labels. Historical vendor performance features (e.g., `historical_on_time_rate`, `historical_quality_score`, `vendor_defect_rate`, `vendor_transaction_count`) must be constructed from data available **before** the current transaction's outcome — they must not include or be influenced by the current transaction's result. The target `outcome` is always the label and is never an input feature.
- **Point-in-time integrity:** The synthetic data-generation process must respect chronological order. Historical vendor/category aggregates for each generated transaction must be calculated only from transactions that precede it chronologically. The generator must NOT calculate historical aggregates using the full dataset first and then assign them to all rows — doing so would leak future outcomes into earlier rows. The intended generation flow is:

  ```
  prior transactions
  → calculate historical vendor/category features (from prior rows only)
  → generate current transaction features
  → generate current transaction outcome
  → move forward chronologically
  → update historical aggregates with the completed transaction
  ```

### 3.3 Features (Inputs)

| Feature | Description |
|---|---|
| `category` | Procurement category (encoded) |
| `unit_price` | Unit price of item |
| `quantity` | Order quantity |
| `total_order_value` | Calculated from price × quantity |
| `lead_time_days` | Promised delivery lead time |
| `historical_on_time_rate` | Vendor historical on-time delivery % — prior orders only ¹ |
| `historical_quality_score` | Vendor historical quality rating (0–1) — prior orders only ¹ |
| `payment_terms_days` | Net payment terms in days |
| `advance_payment_pct` | % of order paid in advance |
| `order_complexity` | Derived complexity score (items, customization) |
| `vendor_transaction_count` | Historical order volume with vendor — prior orders only ¹ |
| `vendor_defect_rate` | Historical defect/rejection rate — prior orders only ¹ |

> ¹ **Historical features** are aggregates of orders placed *before* the current transaction. They must not include the current transaction's outcome or any information available only after fulfillment. `vendor_id` is used for vendor lookup and historical aggregation but is not required as a direct predictive feature — the model should learn from measurable vendor and order characteristics rather than raw vendor identity.

### 3.4 Target Variable

- `outcome` — Binary: `1` (on-time, successful delivery) / `0` (late or failed delivery)

### 3.5 Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1 Score

All four metrics are reported. Fabricated metrics are prohibited.

### 3.6 Prediction API Contract

```
POST /api/predict
Input:  { vendor_attributes }
Output: { vendor_id, predicted_outcome, confidence_score }
```

---

## 4. Backend Architecture

### 4.1 Framework

FastAPI — Python 3.11+

### 4.2 Module Structure

```
backend/
├── main.py                  # FastAPI app entry point
├── routers/
│   ├── predict.py           # ML prediction endpoint
│   ├── vendors.py           # Vendor data CRUD
│   ├── procurement.py       # Procurement request and decision flow
│   ├── risk.py              # Risk assessment engine
│   └── financial.py         # Money At Risk / Financial Exposure engine
├── services/
│   ├── procurement_prediction_service.py        # Model loading and inference
│   ├── scoring_service.py   # Deterministic vendor scoring
│   ├── risk_service.py      # Risk calculation logic
│   └── financial_service.py # Financial exposure calculation
├── models/
│   └── schemas.py           # Pydantic request/response schemas
├── db/
│   └── supabase_client.py   # Supabase connection and queries
├── ml/
│   ├── train.py             # Model training script
│   ├── generate_data.py     # Synthetic data generation
│   └── model.joblib         # Trained model artifact
└── requirements.txt
```

### 4.3 API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/vendors` | List all vendors |
| GET | `/api/vendors/{id}` | Get vendor detail with history |
| POST | `/api/predict` | ML prediction for vendor(s) |
| POST | `/api/score` | Deterministic business scoring |
| POST | `/api/risk` | Risk assessment for vendor/order |
| POST | `/api/financial-exposure` | Money At Risk calculation |
| POST | `/api/decide` | Final procurement decision |
| GET | `/api/health` | Health check |

### 4.4 Business Scoring Formula

Vendor Score = weighted sum of:

```
(delivery_weight × on_time_rate)
+ (quality_weight × quality_score)
+ (price_weight × price_competitiveness)
+ (lead_time_weight × lead_time_score)
+ (payment_weight × payment_terms_score)
```

Default weights are documented in `rules.md`. Weights are configurable.

### 4.5 Financial Exposure Engine

Total Money At Risk =

```
Price Risk Exposure
+ Supplier Risk Exposure
+ Payment/Advance Risk Exposure
+ Delivery Risk Exposure
+ Quality Risk Exposure
```

Each component is calculated from deterministic formulas using actual order and vendor data. See `rules.md` for formula definitions.

---

## 5. Frontend Architecture

### 5.1 Framework

React 18 + Vite

### 5.2 Directory Structure

The structure below is a **reference example**. The final page and component breakdown is owned by the frontend team and must remain consistent with `prd.md`, `design.md`, `app-flow.md`, and the AI Slop Killer rules in `skill.md`. Do not treat filenames below as mandatory — the functional requirements of the decision flow take precedence.

```
frontend/
├── src/
│   ├── pages/          # One file per page/step in the decision flow
│   ├── components/     # Shared UI components (tables, indicators, charts)
│   ├── api/
│   │   └── client.js   # Axios instance; all API calls go here
│   ├── hooks/          # Custom hooks for data fetching and session state
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── vite.config.js
└── package.json
```

The frontend must implement the decision flow defined in `app-flow.md`. The mapping of those steps to pages and the decomposition into components is owned by the frontend team.

### 5.3 UI Design Principles

See `design.md` for the full UI specification. The design document is the source of truth for visual decisions.

Non-negotiable principles (from `skill.md` AI Slop Killer):
- Enterprise professional aesthetic — not an AI SaaS template
- Tables-first data display
- No decorative AI graphics
- No emojis in product UI
- Clear visual hierarchy
- Typography and color palette must comply with `design.md`

### 5.4 State Management

- React built-in state (useState, useContext)
- No additional state management library unless justified
- Procurement session data flows top-down through component tree

---

## 6. Database Interaction

- Backend connects to Supabase via the **Supabase Python client** (`supabase-py`). Direct psycopg2 connections are not used for MVP.
- All schema details in `schema.md`.
- No raw SQL in API route handlers — queries abstracted to `db/supabase_client.py`.
- Environment variables used for all credentials (never hardcoded).
- Data flow: Backend → Supabase Python client → Supabase/PostgreSQL.

---

## 7. Deployment Architecture

### 7.1 Frontend (Vercel)

- Build: `vite build`
- Environment variable: `VITE_API_BASE_URL` pointing to Railway backend

### 7.2 Backend (Railway)

- Startup: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- `model.joblib` included in repository and loaded at startup
- Environment variables for Supabase credentials set in Railway dashboard

### 7.3 Database (Supabase)

- Hosted Supabase project
- PostgreSQL instance managed by Supabase
- Row-level security policies set per table (basic for MVP)

---

## 8. Environment Variables

| Variable | Used By | Description |
|---|---|---|
| `SUPABASE_URL` | Backend | Supabase project URL |
| `SUPABASE_KEY` | Backend | Supabase service role key |
| `VITE_API_BASE_URL` | Frontend | Railway backend URL |

---

## 9. Security Considerations (MVP)

- No user authentication in MVP (out of scope for hackathon)
- The Supabase service-role key is used **server-side only** (FastAPI backend). It must never be exposed to or used by the frontend under any circumstances.
- Database access for the no-auth MVP is controlled entirely by backend application logic — the backend validates and mediates all requests before they reach Supabase.
- Row-level security (RLS) may be enabled on Supabase tables as a defense-in-depth measure, but RLS is **not** the MVP authorization mechanism. Because there is no user authentication, RLS cannot enforce per-user access rules — it is supplementary only.
- CORS configured in FastAPI to allow the frontend domain only
- No user-generated input passed to LLM without sanitization

---

*This document is the source of truth for HOW ProcuraIQ is built technically.*
