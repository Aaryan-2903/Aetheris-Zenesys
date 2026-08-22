# ProcuraIQ — Design Specification

**Version:** 0.1 — Hackathon Draft  
**Last Updated:** 2026-08-22  
**Status:** Draft

---

## 1. Design Philosophy

ProcuraIQ is **enterprise procurement software**, not a consumer app or an AI SaaS product.

The design must reflect:

- **Professional credibility** — users making significant financial decisions need to trust the UI
- **Information density** — procurement decisions require comparing many data points simultaneously
- **Clarity over decoration** — every element earns its place by serving a functional purpose
- **Readability at a glance** — risk levels and key figures must be visible without hunting

The design must NOT look like:

- A generic AI-generated SaaS landing page
- A futuristic AI dashboard with neon glow effects
- A consumer productivity app

---

## 2. Anti-Pattern Rules (AI Slop Killer — UI)

The following design elements are **explicitly prohibited**:

| Prohibited Element | Reason |
|---|---|
| Neon / glowing effects | Looks like a generic AI template, not enterprise software |
| Glassmorphism | Impairs readability; associated with trendy AI dashboards |
| Robot / brain / sparkle graphics | Decorative AI clichés; no functional purpose |
| Excessive gradients | Distracts from data |
| Huge hero sections | Not a marketing page; this is a workflow tool |
| Rounded pill badges everywhere | Over-designed; reduces information density |
| Futuristic / AI-looking fonts | Should be readable and professional |
| "AI-powered" text repeated throughout UI | Hollow marketing copy |
| Decorative animations | Distracts from procurement data |
| Emojis anywhere in the product UI | Unprofessional for enterprise procurement software |
| Generic dashboard card layouts | Prioritize tables and structured data |

---

## 3. Visual Language

### 3.1 Typography

- **Primary font:** Inter (Google Fonts) — clean, readable, widely used in enterprise SaaS
- **Fallback:** system-ui, -apple-system, sans-serif
- **Font sizes:**
  - Body text: 14px
  - Table content: 13px
  - Labels / captions: 12px
  - Section headings: 16px–20px
  - Page titles: 24px
- **Font weight:** Regular (400) for body, Medium (500) for labels, SemiBold (600) for headings
- **Line height:** 1.5 for body, 1.3 for headings

### 3.2 Color Palette

**Background system:**
- Primary background: `#F8F9FA` (near-white, off-white)
- Surface / card background: `#FFFFFF`
- Sidebar background: `#1E2330` (dark navy)
- Sidebar active item: `#2D3448`

**Text:**
- Primary text: `#1A1D23`
- Secondary text: `#5A6070`
- Muted text: `#8A92A0`
- Sidebar text: `#C8CDD8`
- Sidebar active text: `#FFFFFF`

**Accent (functional, not decorative):**
- Primary action: `#2563EB` (blue — used for primary buttons and links only)
- Positive / success: `#16A34A` (green)
- Warning: `#D97706` (amber)
- Danger / High Risk: `#DC2626` (red)
- Neutral: `#6B7280` (gray)

**Risk level colors (functional indicators only):**
- Low Risk: `#16A34A` background-light, text `#166534`
- Medium Risk: `#D97706` background-light, text `#92400E`
- High Risk: `#DC2626` background-light, text `#991B1B`

**Borders:**
- Default border: `#E5E7EB`
- Focused border: `#2563EB`
- Table row border: `#F3F4F6`

### 3.3 Spacing

- Base unit: 4px
- Component padding: 16px / 24px
- Table row height: 40px–44px
- Section gap: 24px
- Page container max-width: 1280px

### 3.4 Elevation / Depth

- Cards: `box-shadow: 0 1px 3px rgba(0,0,0,0.08)`
- No dramatic drop shadows
- No layered floating cards

---

## 4. Layout

### 4.1 Application Shell

```
┌─────────────────────────────────────────────────┐
│  [Sidebar Nav — fixed left, 240px wide]         │
│  ┌───────────────────────────────────────────┐  │
│  │  Logo + Product Name                      │  │
│  │  ─────────────────────                    │  │
│  │  Dashboard                                │  │
│  │  New Procurement Request                  │  │
│  │  Vendor Database                          │  │
│  │  Procurement History                      │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  [Main Content Area — flexible right]           │
│  ┌───────────────────────────────────────────┐  │
│  │  Page Header (title + breadcrumb)         │  │
│  │  ─────────────────────                    │  │
│  │  Page Content                             │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### 4.2 Page Header

- Page title (h1)
- Breadcrumb navigation
- Context actions (e.g., "New Request" button) — right-aligned
- Thin bottom border separating header from content

---

## 5. Pages and Screens

### 5.1 Dashboard

**Purpose:** Summary of procurement activity and recent decisions.

**Content:**
- Summary stats row: Active Requests | Pending Decisions | High-Risk Orders | Decisions This Month
- Recent Procurement Decisions table (last 10)
- No decorative charts for aesthetics — only if showing genuinely useful distribution data

**Table columns:** Request ID | Category | Recommended Vendor | Score | Risk Level | Decision Date | Status

### 5.2 New Procurement Request (Step 1)

**Purpose:** User defines their procurement requirement.

**Content:**
- Form — clean, left-aligned labels, full-width inputs
- Fields: Category, Quantity, Required Lead Time (days), Budget Per Unit, Min Quality Score, Priority Weights
- Weight inputs: delivery / quality / price / lead time / payment (must sum to 1.0, validated)
- Submit → proceeds to Vendor Comparison

**No decorative elements. Form is the only content.**

### 5.3 Vendor Comparison (Step 2)

**Purpose:** Compare all candidate vendors for the requirement.

**Primary component: Vendor Comparison Table**

| Column | Description |
|---|---|
| Vendor Name | Clickable → vendor detail |
| Composite Score | 0.00–1.00, bar indicator |
| ML Prediction | Success / Failure + confidence % |
| Delivery Score | 0.00–1.00 |
| Quality Score | 0.00–1.00 |
| Price Score | 0.00–1.00 |
| Lead Time Score | 0.00–1.00 |
| Risk Level | Low / Medium / High badge (functional color) |
| Action | [Select] button |

- Sortable by any column (default: Composite Score descending)
- Top-ranked row: subtle left border highlight in primary blue
- No extra decoration

### 5.4 Risk Assessment (Step 3)

**Purpose:** Detailed risk breakdown for selected vendor.

**Content:**

Risk Component Table:

| Risk Category | Score | Level | Key Factor |
|---|---|---|---|
| Delivery Risk | 0.72 | Medium | 78% on-time rate (last 24 months) |
| Quality Risk | 0.15 | Low | 1.2% defect rate |
| Supplier Concentration | 0.60 | Medium | 34% of category spend |
| Payment / Advance Risk | 0.30 | Low | 20% advance, net-30 |

- Supplier Health Score: single number prominently displayed (not animated, not glowing)
- Key factor column always references an actual data point

### 5.5 Financial Exposure (Step 4)

**Purpose:** Quantify Money At Risk from this procurement decision.

**Content:**

Financial Exposure Table:

| Risk Type | Exposure Amount | % of Purchase Value | Basis |
|---|---|---|---|
| Price Risk | ₹ X | X% | Price volatility × order value |
| Supplier Risk | ₹ X | X% | Health score gap × order value |
| Payment Risk | ₹ X | X% | Advance amount × advance risk factor |
| Delivery Risk | ₹ X | X% | Late delivery probability × impact factor |
| Quality Risk | ₹ X | X% | Defect rate × rejection impact |
| **Total Money At Risk** | **₹ X** | **X%** | |

Protection Actions section:
- List of recommended actions with expected exposure reduction
- Post-protection exposure total
- Money Protected = Total MAR − Post-Protection

**Currency:** Use ₹ (INR) for MVP (can be made configurable later).

### 5.6 Decision (Step 5)

**Purpose:** Final procurement recommendation with full rationale.

**Content:**

Decision Card:
- Recommended Vendor name and composite score
- Confidence level: High / Medium / Low (derived from ML confidence + score gap to next vendor)
- Risk level badge
- Total Money At Risk figure
- Decision rationale: bulleted list of grounded reasons

Comparison Summary (secondary):
- Brief table showing top 3 vendors across all dimensions

Alternative Vendor note (if applicable):
- Shown when top vendor risk is High and an alternative has lower risk

---

## 6. Components

### 6.1 VendorTable

- Sortable columns
- Row hover: very light background shift (no animation)
- Top-ranked row: subtle left border `3px solid #2563EB`
- Risk level badge: small pill with functional color, no glow

### 6.2 RiskIndicator

- Text badge: "Low" / "Medium" / "High"
- Functional background color (not decorative)
- Font: 12px medium

### 6.3 ScoreBar

- Horizontal bar, 100px wide, 8px height
- Fill color: blue for high, amber for medium, red for low
- Score number shown next to bar
- No animation

### 6.4 ExposureBreakdown

- Table with row totaling
- Optional: simple bar chart showing relative component size (no pie chart — harder to read precisely)

### 6.5 DecisionCard

- Clean bordered card
- No decorative icons
- Vendor name in large text
- Score and confidence in medium text
- Rationale in body text size

---

## 7. Charts and Visualizations

**Permitted charts:**
- Horizontal bar chart — for score comparisons
- Simple bar chart — for financial exposure breakdown by component
- Line chart — for vendor historical performance trend (if time allows)

**Prohibited chart uses:**
- Pie charts for risk distribution (use table instead)
- Donut charts as decoration
- Animated charts
- 3D visualizations

All chart labels must be precise numbers, not ranges.

---

## 8. Responsive Behavior

MVP targets desktop-first (1280px+). Tables must be horizontally scrollable on smaller viewports.

No specific mobile optimization required for hackathon MVP.

---

*This document is the source of truth for ProcuraIQ UI/UX decisions.*
