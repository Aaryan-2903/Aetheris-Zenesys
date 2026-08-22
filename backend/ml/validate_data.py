"""
ProcuraIQ — Dataset Validation & Relationship Report
=====================================================
Version: 1.1

Validates procurement_transactions.csv against all data integrity rules
defined in docs/rules.md and docs/techspec.md.

Produces a concise pass/fail report and key relationship statistics.

Validation scope and limitations
---------------------------------
This script performs structural, numeric-range, chronological, and
logical-consistency checks that can be independently verified from the CSV.

Point-in-time integrity (historical features computed from prior transactions
only) is guaranteed by generate_data.py's chronological generation logic and
the per-vendor rolling accumulator pattern. The validator confirms observable
proxies for this property (vendor_transaction_count starts at 0 per vendor,
is non-decreasing per vendor, and the dataset is chronologically ordered) but
cannot re-derive what each row's historical values were from the CSV alone.
That guarantee must be audited in generate_data.py.

DO NOT manipulate the dataset based on these results to improve ML accuracy.
If relationships look wrong, fix generate_data.py and regenerate.
"""

import csv
import os
import sys
from collections import defaultdict
from typing import Dict, List

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "procurement_transactions.csv")

VALID_CATEGORIES = {
    "IT Equipment", "Electronics", "Raw Materials", "Equipment", "Furniture",
    "Stationery", "Office Supplies", "Packaging Materials",
    "Maintenance Supplies", "Safety Equipment",
}

REQUIRED_COLUMNS = {
    "transaction_id", "transaction_date", "vendor_id", "category",
    "unit_price", "quantity", "total_order_value", "lead_time_days",
    "historical_on_time_rate", "historical_quality_score",
    "payment_terms_days", "advance_payment_pct", "order_complexity",
    "vendor_transaction_count", "vendor_defect_rate", "outcome",
}

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def load_csv(path: str) -> List[dict]:
    if not os.path.exists(path):
        print(f"ERROR: Dataset not found at {path}")
        print("Run generate_data.py first.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pf(condition: bool, label: str, detail: str = "") -> bool:
    status = "PASS" if condition else "FAIL"
    extra = f" — {detail}" if detail else ""
    print(f"  [{status}] {label}{extra}")
    return condition


def section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ---------------------------------------------------------------------------
# VALIDATION CHECKS
# ---------------------------------------------------------------------------

def run_validation(rows: List[dict]) -> int:
    """Returns number of failures."""
    failures = 0

    section("1. STRUCTURE CHECKS")

    # Column presence
    if rows:
        missing = REQUIRED_COLUMNS - set(rows[0].keys())
        ok = not missing
        if not pf(ok, "All required columns present",
                  f"missing: {missing}" if not ok else ""):
            failures += 1
            return failures  # can't continue without columns

    # Row count — must be exactly 50,000
    n = len(rows)
    ok = (n == 50_000)
    if not pf(ok, "Row count is exactly 50,000", f"actual={n:,}"):
        failures += 1

    section("2. UNIQUENESS AND NULLS")

    # Duplicate transaction_ids
    ids = [r["transaction_id"] for r in rows]
    dups = n - len(set(ids))
    if not pf(dups == 0, "No duplicate transaction_ids", f"{dups} duplicates"):
        failures += 1

    # Missing values in required columns
    null_counts = defaultdict(int)
    for r in rows:
        for col in REQUIRED_COLUMNS:
            if r.get(col, "") in ("", None):
                null_counts[col] += 1
    total_nulls = sum(null_counts.values())
    if not pf(total_nulls == 0, "No missing values in required columns",
              dict(null_counts) if total_nulls else ""):
        failures += 1

    section("3. NUMERIC RANGE CHECKS")

    neg_price = neg_qty = neg_tov = 0
    bad_otr = bad_qs = bad_dr = bad_adv = bad_comp = bad_outcome = 0
    bad_lead = bad_pay_terms = 0

    for r in rows:
        try:
            up = float(r["unit_price"])
            qty = int(r["quantity"])
            tov = float(r["total_order_value"])
            lead = int(r["lead_time_days"])
            pay_terms = int(r["payment_terms_days"])
            otr = float(r["historical_on_time_rate"])
            qs = float(r["historical_quality_score"])
            dr = float(r["vendor_defect_rate"])
            adv = float(r["advance_payment_pct"])
            comp = float(r["order_complexity"])
            out = int(r["outcome"])
        except (ValueError, KeyError):
            continue

        if up <= 0:              neg_price += 1
        if qty <= 0:             neg_qty += 1
        if tov <= 0:             neg_tov += 1
        if lead <= 0:            bad_lead += 1
        if pay_terms < 0:        bad_pay_terms += 1
        if not 0.0 <= otr <= 1.0:  bad_otr += 1
        if not 0.0 <= qs <= 1.0:   bad_qs += 1
        if not 0.0 <= dr <= 1.0:   bad_dr += 1
        if not 0.0 <= adv <= 1.0:  bad_adv += 1
        if not 0.0 <= comp <= 1.0: bad_comp += 1
        if out not in (0, 1):      bad_outcome += 1

    if not pf(neg_price == 0, "All unit_prices > 0", f"{neg_price} violations"):
        failures += 1
    if not pf(neg_qty == 0, "All quantities > 0", f"{neg_qty} violations"):
        failures += 1
    if not pf(neg_tov == 0, "All total_order_values > 0", f"{neg_tov} violations"):
        failures += 1
    if not pf(bad_lead == 0, "lead_time_days > 0", f"{bad_lead} violations"):
        failures += 1
    if not pf(bad_pay_terms == 0, "payment_terms_days >= 0", f"{bad_pay_terms} violations"):
        failures += 1
    if not pf(bad_otr == 0, "historical_on_time_rate in [0,1]", f"{bad_otr} violations"):
        failures += 1
    if not pf(bad_qs == 0, "historical_quality_score in [0,1]", f"{bad_qs} violations"):
        failures += 1
    if not pf(bad_dr == 0, "vendor_defect_rate in [0,1]", f"{bad_dr} violations"):
        failures += 1
    if not pf(bad_adv == 0, "advance_payment_pct in [0,1]", f"{bad_adv} violations"):
        failures += 1
    if not pf(bad_comp == 0, "order_complexity in [0,1]", f"{bad_comp} violations"):
        failures += 1
    if not pf(bad_outcome == 0, "outcome is 0 or 1", f"{bad_outcome} violations"):
        failures += 1

    section("4. CALCULATION INTEGRITY")

    # total_order_value == unit_price × quantity (within floating point tolerance)
    tov_errors = 0
    for r in rows:
        try:
            computed = round(float(r["unit_price"]) * int(r["quantity"]), 2)
            recorded = round(float(r["total_order_value"]), 2)
            if abs(computed - recorded) > 0.02:
                tov_errors += 1
        except (ValueError, KeyError):
            tov_errors += 1

    if not pf(tov_errors == 0, "total_order_value == unit_price × quantity",
              f"{tov_errors} mismatches"):
        failures += 1

    section("5. CATEGORICAL VALIDITY")

    bad_cats = sum(1 for r in rows if r.get("category") not in VALID_CATEGORIES)
    if not pf(bad_cats == 0, "All categories are valid", f"{bad_cats} invalid rows"):
        failures += 1

    vendor_ids = {r["vendor_id"] for r in rows}
    if not pf(len(vendor_ids) == 30, "Exactly 30 unique vendor IDs",
              f"actual={len(vendor_ids)}"):
        failures += 1

    section("6. OUTCOME CLASS BALANCE")

    outcome_counts = defaultdict(int)
    for r in rows:
        outcome_counts[int(r["outcome"])] += 1

    has_both = 0 in outcome_counts and 1 in outcome_counts
    if not pf(has_both, "Both classes present (0 and 1)"):
        failures += 1

    if has_both:
        minority = min(outcome_counts[0], outcome_counts[1])
        majority = max(outcome_counts[0], outcome_counts[1])
        ratio = minority / majority
        reasonable = ratio > 0.15  # at least 15:85 split
        if not pf(reasonable, "Reasonable class balance (>15% minority)",
                  f"ratio={ratio:.3f}"):
            failures += 1

    section("7. CHRONOLOGICAL ORDER")

    dates = [r["transaction_date"] for r in rows]
    ordered = all(dates[i] <= dates[i+1] for i in range(len(dates)-1))
    if not pf(ordered, "Transactions in non-decreasing date order"):
        failures += 1

    section("8. HISTORICAL FEATURE CONSISTENCY")

    print()
    print("  Scope note: Point-in-time integrity (historical features computed from")
    print("  prior transactions only) is guaranteed by generate_data.py's chrono-")
    print("  logical generation logic. This section validates observable proxies:")
    print("  vendor_transaction_count monotonicity and cold-start value. Full leakage")
    print("  proof is not independently derivable from the exported CSV alone.")

    # vendor_transaction_count must be non-negative and non-decreasing per vendor,
    # in the order the rows appear (which is chronological order).
    vendor_txn_counts: Dict[str, int] = {}
    count_inconsistencies = 0
    negative_counts = 0
    for r in rows:
        vid = r["vendor_id"]
        try:
            cnt = int(r["vendor_transaction_count"])
        except (ValueError, KeyError):
            continue
        if cnt < 0:
            negative_counts += 1
        if vid in vendor_txn_counts:
            if cnt < vendor_txn_counts[vid]:
                count_inconsistencies += 1
        vendor_txn_counts[vid] = cnt

    if not pf(negative_counts == 0,
              "vendor_transaction_count is non-negative throughout",
              f"{negative_counts} violations"):
        failures += 1
    if not pf(count_inconsistencies == 0,
              "vendor_transaction_count is non-decreasing per vendor (chronological)",
              f"{count_inconsistencies} violations"):
        failures += 1

    # First transaction per vendor must have vendor_transaction_count == 0
    # (cold-start: no prior history exists for that vendor yet)
    first_seen: Dict[str, bool] = {}
    cold_start_errors = 0
    for r in rows:
        vid = r["vendor_id"]
        if vid not in first_seen:
            first_seen[vid] = True
            try:
                cnt = int(r["vendor_transaction_count"])
                if cnt != 0:
                    cold_start_errors += 1
            except (ValueError, KeyError):
                cold_start_errors += 1

    if not pf(cold_start_errors == 0,
              "First transaction per vendor has vendor_transaction_count=0 (cold-start)",
              f"{cold_start_errors} violations"):
        failures += 1

    # historical_on_time_rate and historical_quality_score must be in [0,1].
    # (Already checked in Section 3; confirmed here as a targeted re-assertion
    # in the historical-integrity context.)
    bad_hist_otr = sum(
        1 for r in rows
        if not (0.0 <= float(r.get("historical_on_time_rate", -1)) <= 1.0)
    )
    bad_hist_qs = sum(
        1 for r in rows
        if not (0.0 <= float(r.get("historical_quality_score", -1)) <= 1.0)
    )
    if not pf(bad_hist_otr == 0,
              "historical_on_time_rate in [0,1] (historical integrity re-check)",
              f"{bad_hist_otr} violations"):
        failures += 1
    if not pf(bad_hist_qs == 0,
              "historical_quality_score in [0,1] (historical integrity re-check)",
              f"{bad_hist_qs} violations"):
        failures += 1

    return failures


# ---------------------------------------------------------------------------
# RELATIONSHIP REPORT
# ---------------------------------------------------------------------------

def relationship_report(rows: List[dict]) -> None:
    section("RELATIONSHIP VALIDATION (informational — do not manipulate dataset)")
    n = len(rows)

    # Overall outcome rate
    outcomes = [int(r["outcome"]) for r in rows]
    overall_rate = sum(outcomes) / n
    print(f"\n  Overall outcome=1 rate: {overall_rate:.3f} ({overall_rate:.1%})")

    # Outcome rate by category
    cat_outcomes: Dict[str, List[int]] = defaultdict(list)
    for r in rows:
        cat_outcomes[r["category"]].append(int(r["outcome"]))

    print("\n  Outcome=1 rate by category:")
    for cat in sorted(cat_outcomes.keys()):
        vals = cat_outcomes[cat]
        rate = sum(vals) / len(vals)
        print(f"    {cat:<28} n={len(vals):>5,}  rate={rate:.3f}")

    # Outcome rate by vendor (top 10 and bottom 5 by count)
    vendor_outcomes: Dict[str, List[int]] = defaultdict(list)
    for r in rows:
        vendor_outcomes[r["vendor_id"]].append(int(r["outcome"]))

    print(f"\n  Outcome=1 rate by vendor (showing all {len(vendor_outcomes)}):")
    vendor_summary = sorted(
        [(vid, sum(v)/len(v), len(v)) for vid, v in vendor_outcomes.items()],
        key=lambda x: x[1], reverse=True
    )
    for vid, rate, cnt in vendor_summary:
        print(f"    {vid}  n={cnt:>4,}  rate={rate:.3f}")

    # Relationship between historical_on_time_rate and outcome (quartile bins)
    def bucket_relationship(col: str, label: str, n_buckets: int = 5) -> None:
        vals = []
        for r in rows:
            try:
                vals.append((float(r[col]), int(r["outcome"])))
            except (ValueError, KeyError):
                pass
        vals.sort(key=lambda x: x[0])
        bucket_size = len(vals) // n_buckets
        print(f"\n  {label} vs outcome=1 rate (quintile buckets):")
        for i in range(n_buckets):
            bucket = vals[i*bucket_size : (i+1)*bucket_size]
            if not bucket:
                continue
            lo = bucket[0][0]
            hi = bucket[-1][0]
            rate = sum(o for _, o in bucket) / len(bucket)
            print(f"    [{lo:.3f}–{hi:.3f}]  n={len(bucket):>5,}  outcome_rate={rate:.3f}")

    bucket_relationship("historical_on_time_rate",  "historical_on_time_rate")
    bucket_relationship("historical_quality_score", "historical_quality_score")
    bucket_relationship("vendor_defect_rate",       "vendor_defect_rate")
    bucket_relationship("lead_time_days",            "lead_time_days")
    bucket_relationship("order_complexity",          "order_complexity")

    # Order value distribution
    values = [float(r["total_order_value"]) for r in rows]
    values.sort()
    print("\n  Order value distribution:")
    print(f"    min={values[0]:,.2f}  "
          f"p25={values[n//4]:,.2f}  "
          f"median={values[n//2]:,.2f}  "
          f"p75={values[3*n//4]:,.2f}  "
          f"max={values[-1]:,.2f}")

    # Vendor transaction distribution
    vcounts = sorted(len(v) for v in vendor_outcomes.values())
    print("\n  Vendor transaction count distribution:")
    print(f"    min={vcounts[0]}  "
          f"median={vcounts[len(vcounts)//2]}  "
          f"max={vcounts[-1]}")


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"\nProcuraIQ — Dataset Validation")
    print(f"Dataset: {CSV_PATH}\n")

    rows = load_csv(CSV_PATH)
    print(f"Loaded {len(rows):,} rows.")

    failures = run_validation(rows)

    section("VALIDATION SUMMARY")
    if failures == 0:
        print("\n  ALL CHECKS PASSED. Dataset is validated and ready for ML evaluation.")
    else:
        print(f"\n  {failures} CHECK(S) FAILED. Fix generate_data.py and regenerate.")

    relationship_report(rows)

    section("NEXT STEP")
    if failures == 0:
        print("  Dataset validated. Do NOT train the ML model until instructed.")
    else:
        print("  Fix failures above before proceeding.")

    sys.exit(0 if failures == 0 else 1)
