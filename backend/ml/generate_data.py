"""
ProcuraIQ — Synthetic Procurement Dataset Generator
====================================================
Version: 1.1 (fixes: lead-time condition ordering, complexity condition ordering,
         explicit same-date sequence key for point-in-time integrity)

Generates ~50,000 synthetic procurement transactions with:
  - Point-in-time historical features (no future leakage)
  - Realistic relationships between variables and outcome
  - Deterministic chronological ordering (date + intra-day sequence key)
  - Reproducible output via fixed random seed

Output: backend/ml/data/procurement_transactions.csv

Rules compliance:
  - docs/rules.md  — Data Integrity section
  - docs/techspec.md — Section 3.2 (leakage prevention + point-in-time integrity)
  - docs/skill.md  — Section 4.1 (data generation conventions)

IMPORTANT: Do NOT modify this script to improve post-hoc ML accuracy.
If relationships look wrong, fix the generation logic here.
"""

import csv
import math
import os
import random
import uuid
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

RANDOM_SEED = 42
TARGET_ROWS = 50_000
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "procurement_transactions.csv")

# Simulation time window
START_DATE = date(2020, 1, 1)
END_DATE = date(2025, 6, 30)
TOTAL_DAYS = (END_DATE - START_DATE).days  # ~2007 days

random.seed(RANDOM_SEED)

# ---------------------------------------------------------------------------
# CATEGORY DEFINITIONS
# Each category has realistic price range, quantity range, typical lead time,
# order complexity tendency, and quality expectations.
# ---------------------------------------------------------------------------

CATEGORIES = {
    "IT Equipment": {
        "price_min": 8_000,   "price_max": 120_000,
        "qty_min": 1,         "qty_max": 50,
        "lead_min": 7,        "lead_max": 45,
        "complexity_mean": 0.65, "complexity_std": 0.15,
        "quality_expect": 0.85,
        "payment_terms_pool": [30, 45, 60],
        "advance_pool": [0.0, 0.10, 0.20, 0.30],
        "weight": 0.12,
    },
    "Electronics": {
        "price_min": 500,     "price_max": 30_000,
        "qty_min": 2,         "qty_max": 200,
        "lead_min": 5,        "lead_max": 30,
        "complexity_mean": 0.55, "complexity_std": 0.12,
        "quality_expect": 0.82,
        "payment_terms_pool": [30, 45, 60],
        "advance_pool": [0.0, 0.10, 0.20],
        "weight": 0.10,
    },
    "Raw Materials": {
        "price_min": 200,     "price_max": 8_000,
        "qty_min": 50,        "qty_max": 5_000,
        "lead_min": 10,       "lead_max": 60,
        "complexity_mean": 0.40, "complexity_std": 0.15,
        "quality_expect": 0.75,
        "payment_terms_pool": [30, 60, 90],
        "advance_pool": [0.0, 0.10, 0.15, 0.25],
        "weight": 0.12,
    },
    "Equipment": {
        "price_min": 20_000,  "price_max": 500_000,
        "qty_min": 1,         "qty_max": 10,
        "lead_min": 20,       "lead_max": 90,
        "complexity_mean": 0.75, "complexity_std": 0.12,
        "quality_expect": 0.88,
        "payment_terms_pool": [30, 45, 60, 90],
        "advance_pool": [0.10, 0.20, 0.30, 0.40],
        "weight": 0.08,
    },
    "Furniture": {
        "price_min": 3_000,   "price_max": 40_000,
        "qty_min": 1,         "qty_max": 100,
        "lead_min": 14,       "lead_max": 60,
        "complexity_mean": 0.45, "complexity_std": 0.15,
        "quality_expect": 0.78,
        "payment_terms_pool": [30, 45, 60],
        "advance_pool": [0.0, 0.10, 0.20],
        "weight": 0.07,
    },
    "Stationery": {
        "price_min": 10,      "price_max": 500,
        "qty_min": 50,        "qty_max": 5_000,
        "lead_min": 3,        "lead_max": 14,
        "complexity_mean": 0.20, "complexity_std": 0.08,
        "quality_expect": 0.80,
        "payment_terms_pool": [15, 30, 45],
        "advance_pool": [0.0, 0.0, 0.05],
        "weight": 0.10,
    },
    "Office Supplies": {
        "price_min": 50,      "price_max": 2_000,
        "qty_min": 10,        "qty_max": 1_000,
        "lead_min": 3,        "lead_max": 14,
        "complexity_mean": 0.22, "complexity_std": 0.08,
        "quality_expect": 0.80,
        "payment_terms_pool": [15, 30, 45],
        "advance_pool": [0.0, 0.0, 0.05],
        "weight": 0.10,
    },
    "Packaging Materials": {
        "price_min": 5,       "price_max": 500,
        "qty_min": 100,       "qty_max": 20_000,
        "lead_min": 5,        "lead_max": 21,
        "complexity_mean": 0.30, "complexity_std": 0.10,
        "quality_expect": 0.76,
        "payment_terms_pool": [30, 45, 60],
        "advance_pool": [0.0, 0.05, 0.10],
        "weight": 0.09,
    },
    "Maintenance Supplies": {
        "price_min": 100,     "price_max": 5_000,
        "qty_min": 5,         "qty_max": 500,
        "lead_min": 5,        "lead_max": 21,
        "complexity_mean": 0.35, "complexity_std": 0.12,
        "quality_expect": 0.77,
        "payment_terms_pool": [30, 45],
        "advance_pool": [0.0, 0.05, 0.10],
        "weight": 0.11,
    },
    "Safety Equipment": {
        "price_min": 500,     "price_max": 25_000,
        "qty_min": 2,         "qty_max": 200,
        "lead_min": 7,        "lead_max": 35,
        "complexity_mean": 0.50, "complexity_std": 0.12,
        "quality_expect": 0.90,
        "payment_terms_pool": [30, 45, 60],
        "advance_pool": [0.0, 0.10, 0.20],
        "weight": 0.11,
    },
}

CATEGORY_NAMES = list(CATEGORIES.keys())
CATEGORY_WEIGHTS = [CATEGORIES[c]["weight"] for c in CATEGORY_NAMES]


# ---------------------------------------------------------------------------
# VENDOR DEFINITIONS
# 30 vendors with persistent hidden characteristics.
# "true_reliability" and "true_quality" are latent variables used ONLY
# to drive data generation — they are NEVER included as ML features.
# ---------------------------------------------------------------------------

@dataclass
class Vendor:
    vendor_id: str
    name: str
    categories: List[str]           # categories this vendor serves
    true_reliability: float         # latent: base P(on-time) [0.5–0.98]; NOT a feature
    true_quality: float             # latent: base quality level [0.55–0.99]; NOT a feature
    true_defect_rate: float         # latent: base defect rate [0.01–0.15]; NOT a feature
    typical_lead_factor: float      # multiplier on category lead time [0.8–1.4]
    payment_terms_bias: int         # offset on category payment terms [-15, +30]
    advance_tendency: float         # base advance payment fraction [0.0–0.35]
    price_factor: float             # multiplier on category price [0.85–1.20]


def _make_vendors() -> List[Vendor]:
    """Define 30 vendors with realistic persistent characteristics."""
    rng = random.Random(RANDOM_SEED + 1)

    vendor_configs = [
        # (name, categories, reliability, quality, defect, lead_f, pay_bias, adv, price_f)
        ("TechSource Global",      ["IT Equipment", "Electronics"],        0.92, 0.93, 0.03, 0.90, +15, 0.10, 1.05),
        ("Nexus Supplies Co.",     ["IT Equipment", "Office Supplies"],     0.85, 0.86, 0.06, 1.00, +0,  0.05, 0.95),
        ("InfraCore Systems",      ["IT Equipment", "Equipment"],           0.88, 0.90, 0.04, 1.05, +15, 0.20, 1.10),
        ("Digi Components Ltd.",   ["Electronics", "IT Equipment"],         0.78, 0.80, 0.09, 1.10, +0,  0.10, 0.92),
        ("PrimeElectro Pvt.",      ["Electronics", "Safety Equipment"],     0.82, 0.84, 0.07, 1.00, +0,  0.05, 1.00),
        ("RawMat Industries",      ["Raw Materials", "Packaging Materials"],0.75, 0.76, 0.11, 1.15, +30, 0.15, 0.90),
        ("SteelCore Traders",      ["Raw Materials", "Equipment"],          0.80, 0.78, 0.09, 1.10, +30, 0.20, 0.95),
        ("Precision Parts Inc.",   ["Raw Materials", "Maintenance Supplies"],0.86, 0.85, 0.06, 1.00, +15, 0.10, 1.05),
        ("HeavyGear Solutions",    ["Equipment", "Maintenance Supplies"],   0.72, 0.80, 0.10, 1.20, +30, 0.30, 1.08),
        ("MachinePro Ltd.",        ["Equipment", "Raw Materials"],          0.84, 0.87, 0.06, 1.05, +15, 0.25, 1.12),
        ("WorkSpace Furnishings",  ["Furniture", "Office Supplies"],        0.87, 0.83, 0.07, 1.05, +0,  0.05, 0.97),
        ("ErgoDesign Co.",         ["Furniture", "Office Supplies"],        0.90, 0.88, 0.05, 0.95, +0,  0.10, 1.05),
        ("QuickWrite Stationery",  ["Stationery", "Office Supplies"],       0.93, 0.88, 0.04, 0.85, -15, 0.0,  0.93),
        ("OfficePro Supplies",     ["Office Supplies", "Stationery"],       0.91, 0.89, 0.04, 0.90, -15, 0.0,  0.96),
        ("PackagePlus Ltd.",       ["Packaging Materials", "Raw Materials"],0.83, 0.80, 0.08, 1.00, +15, 0.10, 0.94),
        ("WrapRight Industries",   ["Packaging Materials", "Stationery"],   0.79, 0.77, 0.10, 1.10, +15, 0.05, 0.91),
        ("MaintenEx Supplies",     ["Maintenance Supplies", "Safety Equipment"],0.85, 0.83, 0.07, 1.00, +0,  0.05, 1.00),
        ("SafeGuard Systems",      ["Safety Equipment", "Maintenance Supplies"],0.90, 0.91, 0.04, 0.95, +0,  0.10, 1.08),
        ("ProSafe Traders",        ["Safety Equipment", "Equipment"],       0.82, 0.87, 0.06, 1.05, +15, 0.15, 1.03),
        ("ValueSource Corp.",      ["Office Supplies", "Stationery", "Packaging Materials"], 0.76, 0.74, 0.12, 1.15, +0, 0.0, 0.88),
        ("GlobalTech Imports",     ["IT Equipment", "Electronics", "Equipment"], 0.80, 0.81, 0.08, 1.10, +30, 0.25, 1.02),
        ("SwiftDeliver Co.",       ["Stationery", "Office Supplies", "Packaging Materials"], 0.94, 0.90, 0.03, 0.80, -15, 0.0, 1.00),
        ("RobustMat Suppliers",    ["Raw Materials", "Packaging Materials", "Maintenance Supplies"], 0.77, 0.75, 0.11, 1.15, +30, 0.15, 0.92),
        ("EliteEquip Ltd.",        ["Equipment", "Safety Equipment"],       0.89, 0.92, 0.04, 1.00, +15, 0.30, 1.15),
        ("TechEdge Solutions",     ["IT Equipment", "Electronics"],         0.95, 0.94, 0.02, 0.88, +15, 0.15, 1.12),
        ("BudgetBuy Traders",      ["Office Supplies", "Stationery", "Furniture"], 0.70, 0.70, 0.15, 1.25, -15, 0.0, 0.82),
        ("QualityFirst Pvt.",      ["IT Equipment", "Equipment", "Electronics"], 0.91, 0.93, 0.03, 0.95, +30, 0.20, 1.10),
        ("AgroMat Suppliers",      ["Raw Materials", "Packaging Materials"], 0.74, 0.72, 0.13, 1.20, +30, 0.20, 0.88),
        ("FurnishWell Inc.",       ["Furniture", "Office Supplies"],        0.83, 0.81, 0.08, 1.10, +0,  0.05, 0.98),
        ("MaintainRight Co.",      ["Maintenance Supplies", "Safety Equipment", "Raw Materials"], 0.86, 0.84, 0.06, 1.00, +0, 0.10, 1.01),
    ]

    vendors = []
    for i, cfg in enumerate(vendor_configs):
        name, cats, rel, qual, defect, lead_f, pay_bias, adv, price_f = cfg
        # Add slight noise so each run's latent variables are consistent but not perfectly round
        vendors.append(Vendor(
            vendor_id=f"V{i+1:03d}",
            name=name,
            categories=cats,
            true_reliability=min(0.98, max(0.50, rel + rng.uniform(-0.02, 0.02))),
            true_quality=min(0.99, max(0.55, qual + rng.uniform(-0.02, 0.02))),
            true_defect_rate=min(0.20, max(0.01, defect + rng.uniform(-0.01, 0.01))),
            typical_lead_factor=lead_f,
            payment_terms_bias=pay_bias,
            advance_tendency=adv,
            price_factor=price_f,
        ))
    return vendors


VENDORS = _make_vendors()
VENDOR_MAP: Dict[str, Vendor] = {v.vendor_id: v for v in VENDORS}


# ---------------------------------------------------------------------------
# HISTORICAL STATE TRACKER
# Tracks rolling aggregates per vendor — updated AFTER each transaction.
# This enforces point-in-time integrity: features for row N only use rows 0..(N-1).
# ---------------------------------------------------------------------------

@dataclass
class VendorHistory:
    transaction_count: int = 0
    on_time_count: int = 0
    quality_sum: float = 0.0
    defect_count: int = 0

    # cold-start defaults (used when transaction_count == 0)
    COLD_START_ON_TIME_RATE: float = 0.75
    COLD_START_QUALITY_SCORE: float = 0.75
    COLD_START_DEFECT_RATE: float = 0.08

    def on_time_rate(self) -> float:
        if self.transaction_count == 0:
            return self.COLD_START_ON_TIME_RATE
        return self.on_time_count / self.transaction_count

    def quality_score(self) -> float:
        if self.transaction_count == 0:
            return self.COLD_START_QUALITY_SCORE
        return self.quality_sum / self.transaction_count

    def defect_rate(self) -> float:
        if self.transaction_count == 0:
            return self.COLD_START_DEFECT_RATE
        return self.defect_count / self.transaction_count

    def update(self, outcome: int, quality: float, had_defect: int) -> None:
        """Call this AFTER the transaction is recorded."""
        self.transaction_count += 1
        self.on_time_count += outcome
        self.quality_sum += quality
        self.defect_count += had_defect


# ---------------------------------------------------------------------------
# OUTCOME PROBABILITY
# Probabilistic — no single feature fully determines outcome.
# Latent vendor characteristics feed the probability but are not features.
# ---------------------------------------------------------------------------

def compute_outcome_probability(
    vendor: Vendor,
    hist: VendorHistory,
    lead_time_days: int,
    category_lead_max: int,
    order_complexity: float,
    advance_payment_pct: float,
) -> float:
    """
    Compute P(outcome=1) from multiple factors.
    None of the inputs are the current transaction's outcome.
    Latent vendor true_reliability is used here but is never stored as a feature.
    """
    # Base: vendor's true (latent) reliability, not observable as a feature
    p = vendor.true_reliability

    # Historical on-time rate pulls p toward observed past performance
    hist_otr = hist.on_time_rate()
    p = 0.50 * p + 0.50 * hist_otr  # blend latent + observable history

    # Lead time pressure: the longer relative to category max, the more risky.
    # FIX: check >1.0 (stronger penalty) BEFORE >0.80 (normal penalty) so the
    # more-specific branch is reachable.
    lead_ratio = lead_time_days / max(category_lead_max, 1)
    if lead_ratio > 1.0:     # promised lead time exceeds category maximum (unusual order)
        p *= 0.82
    elif lead_ratio > 0.80:  # within category max but in the high-pressure zone
        p *= 0.90

    # Order complexity increases failure risk.
    # FIX: check very-high complexity (>0.85) BEFORE moderate-high (>0.70) so the
    # more-specific branch is reachable.
    if order_complexity > 0.85:
        p *= 0.84            # strong penalty for very high complexity
    elif order_complexity > 0.70:
        # Graduated penalty: scales from 0% at 0.70 to ~12% at 1.0
        p *= (1.0 - 0.12 * ((order_complexity - 0.70) / 0.30))

    # High advance payment signals financial strain / new relationship risk
    if advance_payment_pct > 0.30:
        p *= 0.93
    elif advance_payment_pct > 0.20:
        p *= 0.97

    # Historical defect rate penalises probability
    dr = hist.defect_rate()
    p *= (1.0 - 0.6 * dr)

    # Historical quality score positively adjusts
    qs = hist.quality_score()
    p += 0.05 * (qs - 0.75)  # small boost/penalty relative to 0.75 baseline

    return min(0.98, max(0.05, p))


def generate_quality_score(vendor: Vendor, hist: VendorHistory, outcome: int) -> float:
    """
    Quality score for the transaction (observed after delivery).
    Depends on vendor's latent quality and history.
    Used to UPDATE history after outcome — never as an input feature.
    """
    base = 0.70 * vendor.true_quality + 0.30 * hist.quality_score()
    noise = random.gauss(0, 0.04)
    score = base + noise
    if outcome == 0:
        score -= random.uniform(0.05, 0.20)  # failed deliveries tend to score lower
    return round(min(1.0, max(0.20, score)), 4)


def had_defect(vendor: Vendor, outcome: int) -> int:
    """Whether this delivery had a defect/rejection (binary)."""
    base_prob = vendor.true_defect_rate
    if outcome == 0:
        base_prob = min(0.60, base_prob * 3.5)  # failed deliveries far more likely to have defects
    return 1 if random.random() < base_prob else 0


# ---------------------------------------------------------------------------
# TRANSACTION GENERATION — single row
# ---------------------------------------------------------------------------

def generate_transaction(
    txn_id: str,
    txn_date: date,
    vendor: Vendor,
    category: str,
    hist: VendorHistory,
) -> dict:
    """
    Generate one transaction. Historical features are read from hist BEFORE
    the outcome is generated. hist is updated by the caller AFTER this returns.
    """
    cat = CATEGORIES[category]

    # --- Order parameters (observable inputs) ---
    unit_price = round(
        random.uniform(cat["price_min"], cat["price_max"]) * vendor.price_factor, 2
    )
    quantity = random.randint(cat["qty_min"], cat["qty_max"])
    total_order_value = round(unit_price * quantity, 2)   # MUST equal price × qty

    lead_time_base = random.randint(cat["lead_min"], cat["lead_max"])
    lead_time_days = max(1, round(lead_time_base * vendor.typical_lead_factor))

    payment_terms_base = random.choice(cat["payment_terms_pool"])
    payment_terms_days = max(0, payment_terms_base + vendor.payment_terms_bias)

    adv_pool = cat["advance_pool"]
    advance_payment_pct = round(
        random.choice(adv_pool) + random.gauss(vendor.advance_tendency, 0.04), 4
    )
    advance_payment_pct = round(min(0.60, max(0.0, advance_payment_pct)), 4)

    complexity_raw = random.gauss(cat["complexity_mean"], cat["complexity_std"])
    order_complexity = round(min(1.0, max(0.05, complexity_raw)), 4)

    # --- Historical features (point-in-time: from prior transactions only) ---
    historical_on_time_rate = round(hist.on_time_rate(), 4)
    historical_quality_score = round(hist.quality_score(), 4)
    vendor_defect_rate = round(hist.defect_rate(), 4)
    vendor_transaction_count = hist.transaction_count  # integer count of prior txns

    # --- Outcome generation (probabilistic) ---
    p_success = compute_outcome_probability(
        vendor=vendor,
        hist=hist,
        lead_time_days=lead_time_days,
        category_lead_max=cat["lead_max"],
        order_complexity=order_complexity,
        advance_payment_pct=advance_payment_pct,
    )
    outcome = 1 if random.random() < p_success else 0

    return {
        "transaction_id": txn_id,
        "transaction_date": txn_date.isoformat(),
        "vendor_id": vendor.vendor_id,
        "category": category,
        "unit_price": unit_price,
        "quantity": quantity,
        "total_order_value": total_order_value,
        "lead_time_days": lead_time_days,
        "historical_on_time_rate": historical_on_time_rate,
        "historical_quality_score": historical_quality_score,
        "payment_terms_days": payment_terms_days,
        "advance_payment_pct": advance_payment_pct,
        "order_complexity": order_complexity,
        "vendor_transaction_count": vendor_transaction_count,
        "vendor_defect_rate": vendor_defect_rate,
        "outcome": outcome,
        # --- Internal fields used to update history (not ML features) ---
        "_quality_score_actual": None,   # filled below
        "_had_defect": None,             # filled below
    }, outcome


# ---------------------------------------------------------------------------
# MAIN GENERATION LOOP
# ---------------------------------------------------------------------------

def generate_dataset(n_rows: int = TARGET_ROWS) -> List[dict]:
    """
    Generate n_rows transactions in chronological order.
    Historical features are always derived from prior transactions only.

    Same-date ordering:
    Each transaction is assigned (date, sequence_key). sequence_key is a
    random integer drawn before sorting, which provides a stable, deterministic
    sub-order within any given date. Transactions are sorted by (date, key).
    This ensures that two transactions on the same date always process in the
    same order across re-runs, preserving point-in-time integrity.
    """
    print(f"Generating {n_rows:,} transactions (seed={RANDOM_SEED})...")

    # Initialise per-vendor history trackers
    vendor_histories: Dict[str, VendorHistory] = {
        v.vendor_id: VendorHistory() for v in VENDORS
    }

    rows: List[dict] = []

    # Pre-assign each transaction a (date, intra-day sequence key) then sort.
    # The sequence key is drawn from the seeded RNG so the order is reproducible.
    # Using a large int range keeps collisions negligible.
    date_keys = sorted(
        (START_DATE + timedelta(days=random.randint(0, TOTAL_DAYS)),
         random.randint(0, 10_000_000))    # intra-day tiebreaker
        for _ in range(n_rows)
    )  # sort is stable on (date, key) — fully deterministic

    txn_counter = 0
    for txn_date, _seq_key in date_keys:
        txn_counter += 1
        txn_id = f"TXN-{txn_counter:06d}"

        # Pick category, then a vendor that serves that category
        category = random.choices(CATEGORY_NAMES, weights=CATEGORY_WEIGHTS, k=1)[0]
        eligible_vendors = [v for v in VENDORS if category in v.categories]
        vendor = random.choice(eligible_vendors)

        hist = vendor_histories[vendor.vendor_id]

        row, outcome = generate_transaction(
            txn_id=txn_id,
            txn_date=txn_date,
            vendor=vendor,
            category=category,
            hist=hist,
        )

        # Generate post-delivery quality and defect (used to update history only)
        quality_actual = generate_quality_score(vendor, hist, outcome)
        defect = had_defect(vendor, outcome)
        row["_quality_score_actual"] = quality_actual
        row["_had_defect"] = defect

        # Append row
        rows.append(row)

        # Update history AFTER recording the row (point-in-time integrity)
        hist.update(outcome=outcome, quality=quality_actual, had_defect=defect)

        if txn_counter % 10_000 == 0:
            print(f"  ... {txn_counter:,} rows generated")

    print(f"Done. Total rows: {len(rows):,}")
    return rows


# ---------------------------------------------------------------------------
# CSV WRITER
# ---------------------------------------------------------------------------

# Columns written to CSV (internal _* columns are excluded from output)
OUTPUT_COLUMNS = [
    "transaction_id",
    "transaction_date",
    "vendor_id",
    "category",
    "unit_price",
    "quantity",
    "total_order_value",
    "lead_time_days",
    "historical_on_time_rate",
    "historical_quality_score",
    "payment_terms_days",
    "advance_payment_pct",
    "order_complexity",
    "vendor_transaction_count",
    "vendor_defect_rate",
    "outcome",
]


def write_csv(rows: List[dict], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Dataset written to: {path}")


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    rows = generate_dataset(TARGET_ROWS)
    write_csv(rows, OUTPUT_PATH)
    print("\nDataset generation complete.")
    print(f"  Rows: {len(rows):,}")
    print(f"  Vendors: {len(VENDORS)}")
    print(f"  Categories: {len(CATEGORIES)}")
    outcome_1 = sum(r["outcome"] for r in rows)
    outcome_0 = len(rows) - outcome_1
    print(f"  Outcome distribution: 1={outcome_1:,} ({outcome_1/len(rows):.1%}), "
          f"0={outcome_0:,} ({outcome_0/len(rows):.1%})")
    print("\nNext step: run validate_data.py")
