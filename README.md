# ProcuraIQ

ProcuraIQ turns vendor comparison into a predictive, priority-aware, and explainable procurement decision.

## Problem
Procurement decisions are often based on simple price comparisons or gut feelings rather than data. Vendor performance history is ignored, risk is not quantified until something goes wrong, and financial exposure is hidden.

## Solution
ProcuraIQ is a Procurement Decision Intelligence Platform that leverages Machine Learning and deterministic risk/financial engines to evaluate vendors. It predicts delivery success, ranks vendors based on custom business priorities, assesses multi-dimensional risk, and calculates actual money at risk before any commitment is made.

## Why ProcuraIQ
Instead of just showing who is cheapest, ProcuraIQ shows who is most likely to deliver on time, calculates the true cost of risk, and provides explainable insights to justify procurement decisions. 

## Core Decision Flow
Predict → Prioritize → Assess Risk → Explain → Decide

## Key Features
- **ML Delivery Prediction**: Predicts the probability of a successful procurement outcome using a Random Forest model trained on historical transactions.
- **Requirement-Aware Scoring**: Deterministically ranks vendors based on customized weights (delivery, quality, price, lead time, payment terms).
- **Multi-Dimensional Risk Intelligence**: Analyzes delivery, quality, supplier concentration, and payment risks.
- **Money At Risk (In Progress)**: Translates abstract risk scores into quantified financial exposure.
- **Explainable Decisions (In Progress)**: Provides transparent reasoning for why a vendor is recommended or flagged.

## Current Implementation
The backend foundation is established and tested.

- **Completed**:
  - Comprehensive documentation foundation (9 documents)
  - 50,000 synthetic procurement transactions across 30 vendors and 10 categories
  - Dataset validation and historical feature leakage safeguards
  - Random Forest procurement outcome model (`model.joblib`)
  - FastAPI backend foundation
  - Supabase / PostgreSQL schema
  - ML prediction API endpoint
  - Requirement-aware deterministic vendor scoring engine
  - Deterministic risk assessment engine

- **Verified API Functionality**:
  - `GET /api/health`: HTTP 200 `{"status":"ok"}`
  - `POST /api/predict/`: HTTP 200 (Real model inference using `model.joblib`, verified confidence around 0.7863)
  - `POST /api/score/`: HTTP 200 (Returns ranked vendors, component scores, and deterministic final scores)
  - `POST /api/risk/`: HTTP 200 (Returns delivery, quality, supplier, payment, and overall risk, plus supplier health score and low-confidence indicator)

## Architecture
```text
React + Vite
        ↓
FastAPI
        ↓
Business Logic + ML
        ↓
Supabase / PostgreSQL
```

## ML Pipeline
- **Algorithm**: Random Forest Classifier (Scikit-learn, Joblib)
- **Dataset**: 50,000 synthetic procurement transactions
- **Target**: On-time/successful procurement outcome (0 or 1)
- **Features**: Historical vendor performance features derived strictly from prior transactions to prevent target leakage.

## Dataset
The generated 50,000-row dataset has passed rigorous validation, including structural, uniqueness, null, numeric-range, calculation-integrity, categorical, class-balance, chronological-order, and historical-feature consistency checks.

## Risk Intelligence
The deterministic risk engine evaluates:
- **Delivery Risk**: Based on historical on-time delivery rates.
- **Quality Risk**: Based on defect rates and average quality scores.
- **Supplier Concentration Risk**: Evaluates vendor spend vs total category spend.
- **Payment / Advance Risk**: Calculates risk based on advance payment percentage and historical reliability.

## Money At Risk
*Status: IN PROGRESS*
This engine will translate risk into financial exposure across five components:
- Price Risk
- Supplier Risk
- Payment / Advance Risk
- Delivery Risk
- Quality Risk

## Technology Stack
- **Frontend**: React, Vite (In Progress)
- **Backend**: FastAPI, Python
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Database**: Supabase / PostgreSQL

## Project Structure
```text
backend/
├── db/             # Database connection and queries
├── ml/             # ML models, training scripts, and dataset generation
├── models/         # Pydantic schemas for API validation
├── routers/        # FastAPI route definitions (predict, score, risk, etc.)
├── services/       # Core business logic and deterministic engines
└── main.py         # FastAPI application entry point
docs/               # Project specifications and rules
```

## API Endpoints
- `GET /api/health` - Health check
- `POST /api/predict/` - ML procurement outcome prediction
- `POST /api/score/` - Deterministic vendor scoring and ranking
- `POST /api/risk/` - Deterministic risk assessment

## Current Status
### COMPLETED
- Dataset generation and validation
- ML training pipeline and artifact creation
- FastAPI foundation
- ML prediction endpoint
- Scoring engine
- Risk engine
- Supabase schema

### IN PROGRESS
- Money At Risk / Financial Exposure Engine
- Final Decision Engine
- Supabase backend data integration
- Frontend (React + Vite)
- Frontend ↔ API integration
- Deployment
- End-to-end testing

## Roadmap
1. Procurement Requirement
2. Vendor Comparison
3. ML Prediction *(Completed)*
4. Requirement-Aware Scoring *(Completed)*
5. Risk Assessment *(Completed)*
6. Money At Risk *(In Progress)*
7. Protection Actions *(Planned)*
8. Explainable Final Decision *(Planned)*

## Demo / Screenshots
*(Planned for Frontend Completion)*

## Local Setup
1. Clone the repository.
2. Install dependencies: `pip install -r backend/requirements.txt`
3. Run the backend: `uvicorn backend.main:app --reload`
4. Run tests: `python test_risk.py` or `python test_score.py`

## Environment Variables
The project uses local environment variables for configuration. See `.env.example` for the required keys. Do not expose actual credentials.

## Security
- All sensitive credentials must remain in `.env` (not committed to version control).
- No actual enterprise data is currently used; all transactions are strictly synthetic.
- `model.joblib` does not contain sensitive customer information.

## Team / Credits
Built for the Hackathon.