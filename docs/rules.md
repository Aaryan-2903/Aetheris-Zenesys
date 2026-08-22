# ProcuraIQ — Project Rules

**Version:** 0.2 — Hackathon Draft  
**Last Updated:** 2026-08-22  
**Status:** Active — Must be respected at all times

---

## 0. Purpose of This Document

This document defines hard constraints on what ProcuraIQ may and may not do — across ML, business logic, data, UI, and development practice. These rules exist to preserve the integrity of the product and prevent the introduction of fabricated, misleading, or invented outputs.

Every team member and every AI coding agent working on this project must read and follow this document.

---

## 1. The Five Calculation Layers — Strict Separation

ProcuraIQ uses five distinct calculation layers. Each has a defined role. They must NOT be conflated.

### Layer 1 — ML Prediction

**What it does:** Predicts the probability of a successful procurement outcome (on-time delivery) using a trained Random Forest model.

**What it does NOT do:**
- Calculate business scores
- Calculate risk
- Calculate financial exposure
- Explain decisions
- Generate any number not produced by the model

**Rules:**
- All predictions come from `model.joblib` via `procurement_prediction_service.py`
- The model is trained on real data with real relationships
- Prediction output: `predicted_outcome` (0/1) and `confidence_score` (0.0–1.0)
- Never hardcode, mock, or fabricate a prediction
- Never report a metric (accuracy, precision, recall, F1) that was not actually computed

### Layer 2 — Deterministic Business Scoring

**What it does:** Scores and ranks vendors using a weighted formula applied to actual vendor attributes.

**Formula:**
```
Composite Score = 
  (weight_delivery × on_time_delivery_rate)
  + (weight_quality × avg_quality_score)
  + (weight_price × price_competitiveness_score)
  + (weight_lead_time × lead_time_score)
  + (weight_payment × payment_terms_score)
```

Where:
- `price_competitiveness_score = min(budget_per_unit, vendor_price) / max(budget_per_unit, vendor_price)`
- `lead_time_score = 1.0 if actual_lead_time ≤ required_lead_time else required_lead_time / actual_lead_time`
- `payment_terms_score = min(payment_terms_days, 60) / 60` (higher terms = better score, capped at 60)

**Rules:**
- Scoring formula is fixed and documented here
- Weights are supplied by the user (default weights sum to 1.0)
- Same inputs always produce the same score — deterministic
- Never invent a score component
- Never allow an LLM to generate or modify a score

### Layer 3 — Risk Calculation

**What it does:** Calculates procurement and vendor risk scores from historical performance data.

**Risk Components and Formulas:**

| Component | Formula |
|---|---|
| Delivery Risk | `1.0 - on_time_delivery_rate` |
| Quality Risk | `defect_rate + (1.0 - avg_quality_score) × 0.5` (capped at 1.0) |
| Supplier Concentration Risk | `vendor_category_spend / total_category_spend` (see definition below) |
| Payment/Advance Risk | `advance_payment_pct × (1.0 - on_time_delivery_rate)` |
| Supplier Health Score | `1.0 - weighted_average(risk_components)` (see weights below) |

**Supplier Concentration Risk — Definition:**
- `vendor_category_spend` = total historical procurement spend attributed to this vendor within the relevant category
- `total_category_spend` = total historical procurement spend across all suppliers within that category
- Result is bounded between 0.0 and 1.0
- If insufficient historical spend data exists, flag as low-confidence — do NOT fabricate a value

**Supplier Health Score — Default Weights:**

| Risk Component | Weight |
|---|---|
| Delivery Risk | 0.30 |
| Quality Risk | 0.30 |
| Supplier Concentration Risk | 0.20 |
| Payment/Advance Risk | 0.20 |
| **Total** | **1.00** |

`Supplier Health Score = 1.0 - (0.30 × delivery_risk + 0.30 × quality_risk + 0.20 × concentration_risk + 0.20 × payment_risk)`

Default weights are deterministic and documented here. Any change to weights requires updating this file first.

**Risk Levels (Thresholds):**
- Low: risk score < 0.33
- Medium: risk score >= 0.33 AND < 0.67
- High: risk score >= 0.67

Thresholds apply to all individual risk components and to the Supplier Health Score inversion. There is no ambiguous boundary.

**Rules:**
- All risk scores derived from historical data in the database
- If a vendor has < 5 transactions, flag data as low-confidence but do not block
- Never invent a risk score
- Never allow an LLM to generate a risk score

### Layer 4 — Financial Exposure Calculation

**What it does:** Translates risk scores into monetary exposure (Money At Risk).

**Formulas:**

| Risk Component | Formula |
|---|---|
| Price Risk Exposure | `purchase_value × price_stddev_pct × 0.5` |
| Supplier Risk Exposure | `purchase_value × (1.0 - supplier_health_score) × 0.3` |
| Payment/Advance Risk Exposure | `(advance_payment_pct × purchase_value) × payment_risk_score` |
| Delivery Risk Exposure | `purchase_value × delivery_risk_score × 0.15` |
| Quality Risk Exposure | `purchase_value × quality_risk_score × 0.2` |
| **Total Money At Risk** | **Sum of all above** |

**Protection Actions (trigger thresholds):**

| Condition | Recommended Action | Expected Reduction |
|---|---|---|
| Delivery Risk > 0.50 | Request delivery penalty clause | Delivery Risk Exposure × 0.40 |
| Quality Risk > 0.40 | Require quality inspection at source | Quality Risk Exposure × 0.50 |
| Advance > 30% of order | Negotiate advance reduction or bank guarantee | Payment Risk Exposure × 0.60 |
| Supplier Concentration > 0.40 | Recommend dual-sourcing for next cycle | Supplier Risk Exposure × 0.30 |

**Money Protected = Total MAR − Post-Protection Exposure**

**Variable Definitions:**
- `price_stddev_pct` = historical vendor price standard deviation / historical vendor average price (for the relevant category)
  - If historical average price is zero or fewer than 5 historical transactions exist, set `price_stddev_pct = 0` and flag as low-confidence; do NOT invent a value
  - This is a dimensionless fraction — it is never a hardcoded currency amount

**Rules:**
- All values must be derivable from order inputs and vendor data
- All formula multipliers (0.15, 0.20, 0.30, etc.) are documented above — any change requires a doc update
- Never hardcode a currency amount
- Never fabricate an exposure figure
- `calculation_inputs` must be saved to `financial_exposures` for auditability
- Never allow an LLM to generate a financial figure

### Layer 5 — AI Explanation

**What it does:** Produces human-readable explanation text for procurement decisions.

**Rules:**
- AI/LLM explanation, if used, receives only structured computed values as input
- LLM prompt must include actual scores, risk levels, and exposure amounts
- LLM is not permitted to invent facts, fabricate vendor histories, or claim metrics not provided
- If LLM is not used, explanation is generated from templates using actual values
- Explanation always cites the data point behind each claim (e.g., "78% on-time delivery rate")

---

## 2. ML Integrity Rules

- No target (`outcome`) shall appear in the feature set for any order being predicted
- The current procurement order's actual outcome (whether it succeeded or failed) must NEVER be used as an input feature — it is known only after fulfillment
- Any information that becomes available only after order fulfillment must not be included in the prediction feature set
- Historical vendor performance features (e.g., `historical_on_time_rate`, `historical_quality_score`, `historical_defect_rate`) are permitted as features — they are aggregates of past orders, not the current order's outcome
- Historical aggregates must be constructed using data from orders prior to the current order whenever chronological ordering is applicable (no future leakage)
- Train/test split is performed before any feature engineering derived from labels
- `random_state=42` is used for reproducibility
- All four evaluation metrics (Accuracy, Precision, Recall, F1) must be computed and logged
- Never modify or cherry-pick evaluation output
- If model accuracy is unacceptably low, fix the data generation logic — not the metrics
- `model.joblib` is the only artifact used for inference
- Feature column list must be saved and loaded at inference time (no column mismatch)

---

## 3. Data Integrity Rules

- Synthetic data must contain realistic relationships between variables
- Do not generate independent random columns
- The probability of `outcome = 1` (successful delivery) must be meaningfully higher when:
  - `historical_on_time_rate` is high (these are historical aggregates, not the current outcome)
  - `historical_quality_score` is high
  - `historical_defect_rate` is low
  - `order_complexity` is within the vendor's demonstrated experience range
- Note: these are correlational rules for data generation only — they describe how the synthetic generator must construct relationships, not how any individual current order outcome is determined
- The current order's `outcome` column is the label; the historical performance columns are features — they must never be the same column or derived from the same order
- Outcome distribution must be realistic (not 50/50 random)
- Do not insert fabricated vendor histories
- All data inserted to Supabase must originate from the generation script, not manual invention

---

## 4. Financial Exposure Rules

- All Money At Risk values are calculated — never invented
- All formula coefficients are documented in this file
- Any change to formula coefficients requires updating this file first
- `calculation_inputs` field in `financial_exposures` must store the full audit trail
- Post-protection exposure must be ≤ Total MAR
- Money Protected must = Total MAR − Post-Protection (no rounding hacks)
- Never display a financial figure that cannot be re-derived from stored inputs

---

## 5. No Fabrication Rules

The following are strictly prohibited:

- Hardcoding any procurement metric, risk score, or financial exposure value in production code
- Claiming a vendor has "excellent history" when the database does not support this
- Displaying a prediction confidence not produced by the model
- Displaying ML metrics not computed from the actual test set
- Generating explanation text that cites a factor not included in the computed data

**Zero tolerance.** Any fabricated value is a product defect.

---

## 6. Architecture Integrity Rules

- Do not change `schema.md`-defined tables without updating `schema.md` first
- Do not add a new API endpoint without updating `techspec.md`
- Do not add a new page or screen without updating `design.md`
- Do not add a dependency to `requirements.txt` or `package.json` without documented justification
- Documentation is updated BEFORE code is changed for architectural decisions

---

## 7. Feature Scope Rules

- Any feature not listed in `prd.md` Section 5 (In Scope) is NOT to be built without team approval
- The following are explicitly out of scope: Live market pricing, AI Negotiation Copilot, Protection marketplace, Multi-tenant auth, Mobile app
- What-If Simulation: **PENDING Enterprise Constraint — do not implement without confirmation**
- If an AI agent suggests a new feature "to make it look more impressive," reject it

---

## 8. Enterprise Constraint Rules

**STATUS: PENDING — TO BE CONFIRMED FROM ORGANIZERS**

- Do not claim What-If Simulation as the primary innovation until the Enterprise Constraint is known
- Do not build any Enterprise Constraint-dependent feature until the constraint is received and reviewed by Member 2 (Business & Research) and Member 3 (Product & Research)
- When the constraint is received, update `prd.md`, `implementation-plan.md`, and `tracker.md` accordingly

---

## 9. Positioning Rules

Do NOT claim:
- "Better than SAP"
- "Better than Oracle"
- "Replaces ERP"
- "AI-powered" on every screen
- Any benchmark comparison not supported by evidence

DO claim:
- "A focused, lightweight procurement decision layer"
- "Predictive, priority-aware, and explainable procurement decisions"
- "Quantified financial exposure before commitment"

---

## 10. Documentation Synchronization Rules

| When you change... | You must also update... |
|---|---|
| Database schema | `schema.md` |
| API endpoints | `techspec.md` |
| ML features or model | `techspec.md`, `rules.md` (Section 1) |
| Financial formulas | `rules.md` (Section 1, Layer 4) |
| UI pages or components | `design.md` |
| Build sequence | `implementation-plan.md` |
| Task completion | `tracker.md` |

Documentation is the source of truth. Code follows documentation — not the other way around.

---

*These rules are mandatory. They are not suggestions.*
