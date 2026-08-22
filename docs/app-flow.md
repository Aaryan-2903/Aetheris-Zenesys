# ProcuraIQ — Application Flow

**Version:** 0.1 — Hackathon Draft  
**Last Updated:** 2026-08-22  
**Status:** Draft

---

## 1. Core Decision Flow

```
[1] Define Procurement Requirement
         ↓
[2] Retrieve Matching Vendors
         ↓
[3] ML Prediction (per vendor)
         ↓
[4] Deterministic Business Scoring & Ranking
         ↓
[5] Risk Assessment
         ↓
[6] Money At Risk / Financial Exposure
         ↓
[7] Explanation
         ↓
[8] Final Procurement Decision
```

Each step is sequential. No step is skipped. All results from earlier steps feed later steps.

---

## 2. Step-by-Step Flow

---

### Step 1 — Define Procurement Requirement

**Page:** Procurement Request

**User Actions:**
- Enter item/category being procured
- Enter required quantity
- Enter required delivery date / acceptable lead time
- Enter budget / target price per unit
- Optionally specify: minimum quality score, payment term preference, priority weighting

**System Actions:**
- Validate inputs
- Normalize requirement into a structured requirement object
- Pass requirement to vendor retrieval

**Output:**
```json
{
  "category": "IT Equipment",
  "quantity": 500,
  "required_lead_time_days": 14,
  "budget_per_unit": 1200,
  "min_quality_score": 0.75,
  "weights": {
    "delivery": 0.35,
    "quality": 0.25,
    "price": 0.20,
    "lead_time": 0.10,
    "payment": 0.10
  }
}
```

---

### Step 2 — Retrieve Matching Vendors

**System Actions:**
- Query Supabase `vendors` table for vendors in the specified category
- Retrieve each vendor's historical performance data from `vendor_transactions`
- Filter vendors by minimum quality threshold if specified
- Return list of candidate vendors with their attributes

**Output:** List of vendors with attributes populated from database.

---

### Step 3 — ML Prediction

**System Actions:**
- For each candidate vendor, construct the feature vector from vendor attributes and order parameters
- Call Prediction model (`model.joblib`) via `procurement_prediction_service.py`
- Receive `predicted_outcome` (1=success, 0=failure) and `confidence_score` per vendor

**API Call:**
```
POST /api/predict
Body: { vendors: [...], order_params: {...} }
Response: [{ vendor_id, predicted_outcome, confidence_score }, ...]
```

**Display:**
- Prediction result and confidence shown in vendor comparison table
- Not used in isolation — feeds into final decision

---

### Step 4 — Deterministic Business Scoring and Ranking

**System Actions:**
- For each vendor, calculate the business score using the weighted scoring formula
- Score components: delivery reliability, quality, price competitiveness, lead time, payment terms
- Apply requirement weights defined in Step 1
- Rank vendors by composite score (descending)

**API Call:**
```
POST /api/score
Body: { vendors: [...], requirement: {...} }
Response: [{ vendor_id, composite_score, score_breakdown }, ...]
```

**Display — Vendor Comparison Table:**
- Columns: Vendor Name | Composite Score | ML Prediction | Delivery Score | Quality Score | Price Score | Lead Time Score | Payment Score | Risk Level
- Sortable by any column
- Top-ranked vendor highlighted

---

### Step 5 — Risk Assessment

**User Actions:**
- View risk assessment for selected/top vendor(s)
- Optionally compare risk across vendors

**System Actions:**
- For each vendor, calculate risk scores per category:
  - Delivery Risk (derived from historical on-time rate and variability)
  - Quality Risk (derived from defect rate and quality score)
  - Supplier Concentration Risk (derived from spend concentration)
  - Payment / Advance Risk (derived from advance payment % and terms)
- Calculate Supplier Health Score (aggregate)
- Assign risk level: Low / Medium / High using defined thresholds

**API Call:**
```
POST /api/risk
Body: { vendor_id, order_params: {...} }
Response: { vendor_id, risk_components: {...}, supplier_health_score, overall_risk_level }
```

**Display:**
- Risk summary table: Category | Score | Level (Low/Medium/High)
- Supplier Health Score badge

---

### Step 6 — Money At Risk / Financial Exposure

**User Actions:**
- View financial exposure for the selected order and vendor combination

**System Actions:**
- Calculate each risk component's financial exposure:
  - **Price Risk:** `purchase_value × price_volatility_factor`
  - **Supplier Risk:** `purchase_value × (1 - supplier_health_score) × supplier_concentration_weight`
  - **Payment Risk:** `advance_amount × advance_risk_factor`
  - **Delivery Risk:** `purchase_value × late_delivery_probability × operational_impact_factor`
  - **Quality Risk:** `purchase_value × defect_rate × quality_impact_factor`
- Calculate **Total Money At Risk** = sum of above
- Recommend protection actions based on highest-exposure components
- Recalculate exposure after protection actions
- Calculate **Money Protected** = Total Money At Risk − Post-Protection Exposure

**API Call:**
```
POST /api/financial-exposure
Body: { vendor_id, order_params: {...} }
Response: {
  total_money_at_risk,
  components: { price, supplier, payment, delivery, quality },
  protection_actions: [...],
  post_protection_exposure,
  money_protected
}
```

**Display:**
- Financial Exposure table: Risk Type | Exposure Amount | % of Purchase Value
- Total Money At Risk prominently displayed
- Protection actions listed with expected impact
- Money Protected shown after actions applied

---

### Step 7 — Explanation

**System Actions:**
- Generate explanation for the top-ranked vendor:
  - Why this vendor is recommended: reference to highest-scoring components
  - Why other vendors ranked lower: reference to their score gaps
  - Key risk factors: drawn from risk assessment
  - Financial exposure summary: drawn from financial engine
- Explanation text uses actual computed values — no invented reasons
- If LLM is used for natural-language formatting, it receives only the computed data as structured input

**Display:**
- "Why Recommended" section: bulleted, factual, value-grounded
- "Why Others Ranked Lower" section: comparative, factual
- Risk flags highlighted
- All explanation points traceable to data

---

### Step 8 — Final Procurement Decision

**System Actions:**
- Combine all signals into final recommendation:
  - ML prediction confidence
  - Business composite score
  - Risk level
  - Financial exposure severity
- Apply decision rule (documented in `rules.md`)
- Output final recommended vendor with decision rationale

**API Call:**
```
POST /api/decide
Body: { vendors: [...], requirement: {...}, risk_data: {...}, financial_data: {...} }
Response: {
  recommended_vendor_id,
  decision_rationale,
  confidence_level,
  risk_summary,
  financial_exposure_summary,
  alternative_vendor_id (if applicable)
}
```

**Display — Decision Card:**
- Recommended Vendor with name and composite score
- Decision rationale (grounded in factors)
- Confidence level indicator
- Risk level badge
- Total Money At Risk figure
- Alternative vendor option if risk is borderline

---

## 3. Navigation Flow (UI)

```
[Dashboard / Home]
       ↓
[New Procurement Request] → [Step 1: Define Requirement]
                                      ↓
                            [Step 2: Vendor Comparison Table]
                                      ↓
                            [Step 3/4: Risk + Score Detail]
                                      ↓
                            [Step 5: Financial Exposure]
                                      ↓
                            [Step 6: Decision + Explanation]
                                      ↓
                            [Decision Saved to History]
```

---

## 4. Data Flow Summary

```
User Input (requirement)
  → Vendor Query (Supabase)
  → Feature Engineering (backend)
  → ML Prediction (model.joblib)
  → Business Scoring (scoring_service.py)
  → Risk Calculation (risk_service.py)
  → Financial Exposure (financial_service.py)
  → Explanation Construction (actual computed values)
  → Final Decision (decision rule)
  → Response to Frontend
```

---

*This document is the source of truth for the complete user and system workflow.*
