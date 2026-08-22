# ProcuraIQ — Product Requirements Document (PRD)

**Version:** 0.1 — Hackathon Draft  
**Last Updated:** 2026-08-22  
**Status:** Draft — Pending Enterprise Constraint Confirmation

---

## 1. Problem Statement

Procurement decisions in enterprise environments suffer from several structural weaknesses:

- Vendor comparison is often static, manual, and based on incomplete information.
- Risk is hidden or distributed across disconnected systems.
- Financial exposure from a procurement decision is rarely quantified before commitment.
- Decision rationale is opaque — teams cannot explain why a vendor was chosen.
- Prioritization does not account for current business requirements and constraints.

Procurement teams make significant financial commitments without a clear, data-grounded, explainable view of risk and outcome likelihood.

---

## 2. Target Users

| User | Role | Primary Need |
|---|---|---|
| Procurement Manager | Approves vendor selection | Clear decision rationale and financial risk summary |
| Procurement Analyst | Compares vendors and prepares decisions | Ranked vendor list with risk scores and ML predictions |
| Finance Controller | Validates financial commitment | Money At Risk breakdown before approval |
| Category Manager | Manages vendor relationships per category | Category-level risk and performance visibility |

---

## 3. Product Goal

ProcuraIQ is a focused, lightweight procurement decision-support layer.

It is not an ERP replacement. It addresses one specific gap:

> **Turning vendor comparison into a predictive, priority-aware, and explainable procurement decision.**

---

## 4. Unique Selling Proposition (USP)

> "ProcuraIQ turns vendor comparison into a predictive, priority-aware and explainable procurement decision."

Core decision flow:

```
Predict → Prioritize → Assess Risk → Explain → Decide
```

The product makes procurement decisions:
- **Faster** — single workflow from vendor list to final recommendation
- **Clearer** — explainable scoring grounded in actual calculated factors
- **Risk-aware** — visible procurement and financial risk before commitment
- **Financially informed** — Money At Risk quantified before approval

---

## 5. Scope

### 5.1 In Scope (MVP)

1. **Predict** — ML-based procurement outcome prediction per vendor
2. **Prioritize** — Requirement-aware, deterministic business scoring
3. **Assess Risk** — Vendor and procurement risk assessment
4. **Explain** — Grounded explanation of vendor recommendation
5. **Decide** — Final procurement recommendation with rationale
6. **Money At Risk / Financial Exposure Engine** — Quantified financial risk before commitment

### 5.2 Out of Scope (MVP)

- Live market pricing integrations
- AI Negotiation Copilot
- Protection-plan or warranty marketplaces
- Full ERP workflow integration
- Contract lifecycle management
- Supplier onboarding workflow
- Mobile application
- Multi-tenant enterprise authentication
- What-If Decision Simulator *(status: PENDING — TO BE CONFIRMED FROM ORGANIZERS)*

---

## 6. Feature Requirements

### Feature 1 — Predict

**Goal:** Predict procurement outcome (on-time delivery probability) using an ML model.

**Requirements:**
- Train a Random Forest classifier on synthetic procurement data (~50,000 records).
- Prediction target: procurement outcome / on-time delivery (binary classification).
- Model must learn real relationships between procurement variables (not random noise).
- Model is saved as `model.joblib`.
- Predictions are surfaced per vendor in the UI with a confidence score.
- No fabrication of predictions — all values come from the trained model.

**Inputs:** vendor attributes, category, price, quantity, lead time, historical performance, payment terms, order complexity.

**Outputs:** predicted outcome (success/failure), prediction confidence.

### Feature 2 — Prioritize

**Goal:** Rank vendors based on business requirements using deterministic scoring.

**Requirements:**
- Scoring must be requirement-aware (accounts for what the buyer needs for this order).
- Scoring must be explainable — each score component is visible.
- No simple priority dropdown masquerading as innovation.
- Score components: delivery reliability, quality rating, price competitiveness, lead time, payment terms.
- Weights are configurable and documented.
- Final rank is deterministic — same inputs always produce same rank.

### Feature 3 — Assess Risk

**Goal:** Identify and quantify procurement and vendor risk.

**Requirements:**
- Risk assessment uses historical transaction data per vendor.
- Risk categories: delivery risk, quality risk, supplier concentration risk, payment risk.
- Each risk category has a calculated score.
- Risk level (Low / Medium / High) is derived from thresholds, not heuristics.
- Supplier Health Score is an aggregate across risk categories.

### Feature 4 — Explain

**Goal:** Provide grounded, transparent explanations for vendor recommendations.

**Requirements:**
- Explanations reference actual calculated factors (scores, risks, predictions).
- No LLM-invented reasoning.
- Explanations cover: why this vendor is preferred, why others are not preferred.
- If AI (LLM) is used for natural-language explanation, it receives only actual computed values as context — it does not invent metrics.

### Feature 5 — Decide

**Goal:** Produce a final procurement decision recommendation.

**Requirements:**
- Final recommendation combines: ML prediction score + deterministic business score + risk assessment.
- Combination formula is documented and transparent.
- Output: recommended vendor, rationale, confidence, risk summary.
- Decision is not a "black box" — all contributing factors are visible.

### Feature 6 — Money At Risk / Financial Exposure Engine

**Goal:** Quantify financial exposure before procurement commitment.

**Requirements:**
- Calculate total Money At Risk from five risk components:
  - **Price Risk** — exposure from price volatility or unfavorable terms
  - **Supplier Risk** — exposure from vendor reliability/concentration
  - **Payment / Advance Risk** — exposure from advance payment or unfavorable payment terms
  - **Delivery Risk** — exposure from late delivery (operational cost, penalties)
  - **Quality Risk** — exposure from defective or non-conforming goods

- All exposure values are derived from transparent deterministic formulas — never hardcoded or fabricated.
- Show total Money At Risk.
- Show risk component breakdown.
- Recommend protection actions where relevant.
- Recalculate exposure after protection actions are applied.
- Show potential Money Protected.

**Calculation principle:** All values must be traceable to inputs (purchase value, vendor scores, historical data). No invented numbers.

---

## 7. Success Criteria

| Criterion | Measure |
|---|---|
| ML model trained and functional | Accuracy, precision, recall and F1 reported; performance evaluated against a defined baseline |
| Financial Exposure Engine working | All 5 risk components calculated, no hardcoded values |
| End-to-end decision flow works | User can go from vendor list to final decision in one session |
| Explanations are grounded | Every explanation references a calculated value |
| Documentation complete | All 9 docs present, accurate, and consistent |
| Deployed and accessible | Frontend on Vercel, backend on Railway |
| Demo-ready | Full flow demonstrable within 5 minutes |

---

## 8. Enterprise Constraint

**STATUS: PENDING — TO BE CONFIRMED FROM ORGANIZERS**

The Zenesys Enterprise Constraint will determine whether additional capabilities (e.g., What-If Decision Simulation) are elevated as the primary innovation feature. No assumption about the final innovation is made in this document.

---

## 9. Out of Scope — Explicit List

The following are explicitly out of scope for the hackathon MVP:

- Replacing SAP, Oracle, or any ERP
- Live market pricing or supplier API integration
- AI Negotiation Copilot
- Protection-plan / warranty marketplace
- Multi-tenant SaaS features
- Mobile application
- Contract lifecycle management
- Supplier onboarding workflows
- What-If Simulation *(pending Enterprise Constraint confirmation)*

---

*This document is the source of truth for WHAT ProcuraIQ does and WHY.*
