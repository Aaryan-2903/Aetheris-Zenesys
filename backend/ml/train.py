"""
ProcuraIQ — ML Training Script (Baseline Random Forest)
========================================================
Version: 1.0

Trains a Random Forest Classifier on the validated synthetic procurement
dataset and saves the serialised pipeline + feature column list for inference.

Rules compliance:
  - docs/rules.md  Section 2 (ML Integrity)
  - docs/techspec.md Section 3 (ML Architecture)
  - docs/skill.md  Section 4 (ML Conventions)

IMPORTANT:
  - Do NOT modify this script to optimise for a specific accuracy target.
  - Report all four metrics as computed from the actual held-out test set.
  - Never hardcode, fabricate, or cherry-pick any evaluation result.
  - All preprocessing is fit ONLY on the training split.
"""

import json
import os
import sys
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

# ---------------------------------------------------------------------------
# PATHS  (relative to this file)
# ---------------------------------------------------------------------------

_HERE = os.path.dirname(os.path.abspath(__file__))

DATA_PATH            = os.path.join(_HERE, "data", "procurement_transactions.csv")
MODEL_PATH           = os.path.join(_HERE, "model.joblib")
FEATURE_COLUMNS_PATH = os.path.join(_HERE, "feature_columns.json")

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

RANDOM_SEED = 42
TEST_SIZE   = 0.20   # 80/20 split — documented in techspec.md Section 3.2

# Approved predictive features (from techspec.md Section 3.3 and task spec).
# Forbidden: transaction_id, vendor_id, transaction_date, outcome.
CATEGORICAL_FEATURES = [
    "category",
]

NUMERIC_FEATURES = [
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
]

ALL_FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES   # order is preserved for inference

TARGET = "outcome"

# Columns that must NEVER appear in the feature matrix
FORBIDDEN_FEATURES = {"transaction_id", "vendor_id", "transaction_date", TARGET}

# Random Forest parameters — sized for hackathon deployment.
# n_estimators=100 and max_depth=20 give a valid, stable baseline while keeping
# the serialised artifact well below GitHub's 100 MiB single-file limit.
# These are not chosen to hit a specific accuracy; they represent a reasonable
# trade-off between model capacity and serialisation size.
RF_PARAMS = {
    "n_estimators": 100,       # reduced from 200 to shrink serialised tree storage
    "max_depth": 20,           # depth cap: bounds node count per tree significantly
    "min_samples_split": 10,   # mild regularisation to avoid single-sample splits
    "min_samples_leaf": 5,     # mild regularisation on leaf size
    "max_features": "sqrt",    # standard classification default
    "class_weight": "balanced",# accounts for ~65/35 outcome imbalance honestly
    "random_state": RANDOM_SEED,
    "n_jobs": -1,              # use all available cores
}

# ---------------------------------------------------------------------------
# STEP 0: LOAD DATA
# ---------------------------------------------------------------------------

def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        print(f"ERROR: Dataset not found at {path}")
        print("Run generate_data.py first, then validate_data.py.")
        sys.exit(1)
    df = pd.read_csv(path)
    print(f"Loaded {len(df):,} rows, {len(df.columns)} columns.")
    return df


# ---------------------------------------------------------------------------
# STEP 1: GUARD — VERIFY NO FORBIDDEN FEATURES LEAK IN
# ---------------------------------------------------------------------------

def verify_feature_safety(df: pd.DataFrame) -> None:
    """Hard stop if any forbidden column would appear in the feature matrix."""
    leaked = FORBIDDEN_FEATURES & set(ALL_FEATURES)
    if leaked:
        print(f"FATAL: Forbidden features in ALL_FEATURES list: {leaked}")
        sys.exit(1)
    print(f"Feature safety check: OK  (forbidden={FORBIDDEN_FEATURES})")


# ---------------------------------------------------------------------------
# STEP 2: BUILD PIPELINE
# ---------------------------------------------------------------------------

def build_pipeline() -> Pipeline:
    """
    Preprocessing:
      - OrdinalEncoder for `category` — maps each category string to an integer.
        This is appropriate for a tree-based model that does not assume ordinality
        but simply needs numeric inputs.
      - Numeric features are passed through unchanged; Random Forests are scale-
        invariant, so no normalisation is needed or applied.

    The full pipeline (preprocessor + classifier) is fitted only on training data
    and saved as a single joblib artifact for inference.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OrdinalEncoder(
                    handle_unknown="use_encoded_value",
                    unknown_value=-1,         # unseen categories at inference → -1
                ),
                CATEGORICAL_FEATURES,
            ),
            (
                "num",
                "passthrough",               # tree models are scale-invariant
                NUMERIC_FEATURES,
            ),
        ],
        remainder="drop",                    # silently drop any unlisted columns
    )

    clf = RandomForestClassifier(**RF_PARAMS)

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf),
        ]
    )
    return pipeline


# ---------------------------------------------------------------------------
# STEP 3: TRAIN / EVALUATE
# ---------------------------------------------------------------------------

def train_and_evaluate(df: pd.DataFrame) -> dict:
    X = df[ALL_FEATURES].copy()
    y = df[TARGET].copy()

    # Sanity: confirm target is present and binary
    assert set(y.unique()).issubset({0, 1}), "Target column has unexpected values."

    # 80/20 stratified split — stratify preserves class ratio in both splits
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=y,
    )

    print(f"\nSplit:  train={len(X_train):,}  test={len(X_test):,}")
    print(f"Train outcome distribution: {dict(y_train.value_counts().sort_index())}")
    print(f"Test  outcome distribution: {dict(y_test.value_counts().sort_index())}")

    # Build and fit pipeline — preprocessing fitted on TRAIN only
    pipeline = build_pipeline()
    print("\nFitting pipeline...")
    pipeline.fit(X_train, y_train)
    print("Training complete.")

    # Evaluate on held-out TEST set — no peeking during training
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]   # P(outcome=1)

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec  = recall_score(y_test, y_pred, zero_division=0)
    f1   = f1_score(y_test, y_pred, zero_division=0)
    cm   = confusion_matrix(y_test, y_pred)

    return {
        "pipeline": pipeline,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "confusion_matrix": cm,
        "y_test": y_test,
        "y_pred": y_pred,
        "y_prob": y_prob,
    }


# ---------------------------------------------------------------------------
# STEP 4: SAVE ARTIFACTS
# ---------------------------------------------------------------------------

def save_artifacts(pipeline: Pipeline) -> None:
    """
    Saves:
      model.joblib            — full fitted pipeline (preprocessor + classifier),
                                serialised with zlib compression level 3 to reduce
                                file size without affecting inference correctness.
      feature_columns.json    — ordered list of input feature names expected at inference

    At inference time the backend must:
      1. Load model.joblib
      2. Load feature_columns.json
      3. Construct a DataFrame with exactly those columns in that order
      4. Call pipeline.predict() / pipeline.predict_proba()
    """
    # compress=3: zlib level 3 — good size reduction, fast enough for a deploy artifact
    joblib.dump(pipeline, MODEL_PATH, compress=3)
    size_bytes = os.path.getsize(MODEL_PATH)
    size_mib = size_bytes / (1024 * 1024)
    print(f"\nModel saved   -> {MODEL_PATH}")
    print(f"Model size    -> {size_bytes:,} bytes  ({size_mib:.2f} MiB)")

    with open(FEATURE_COLUMNS_PATH, "w", encoding="utf-8") as f:
        json.dump(ALL_FEATURES, f, indent=2)
    print(f"Features saved -> {FEATURE_COLUMNS_PATH}")


# ---------------------------------------------------------------------------
# STEP 5: INFERENCE SMOKE TEST
# ---------------------------------------------------------------------------

def inference_smoke_test() -> None:
    """
    Loads the saved artifacts in a clean context and verifies end-to-end
    inference on a single synthetic (but realistic) input row.
    This validates that the model artifact is self-contained and inference-ready.
    """
    print("\n--- Inference Smoke Test ---")

    # Load artifacts
    loaded_pipeline = joblib.load(MODEL_PATH)
    with open(FEATURE_COLUMNS_PATH, "r", encoding="utf-8") as f:
        loaded_columns = json.load(f)

    print(f"Loaded model:    {MODEL_PATH}")
    print(f"Loaded features: {len(loaded_columns)} columns")

    # Construct one realistic test row (not from training data — just a plausible order)
    test_row = {
        "category":                "IT Equipment",
        "unit_price":              45_000.0,
        "quantity":                10,
        "total_order_value":       450_000.0,   # = unit_price × quantity
        "lead_time_days":          21,
        "historical_on_time_rate": 0.82,
        "historical_quality_score":0.88,
        "payment_terms_days":      45,
        "advance_payment_pct":     0.10,
        "order_complexity":        0.60,
        "vendor_transaction_count":50,
        "vendor_defect_rate":      0.04,
    }

    # Verify all expected columns are present
    missing = set(loaded_columns) - set(test_row.keys())
    assert not missing, f"Smoke test row missing columns: {missing}"

    df_test = pd.DataFrame([test_row])[loaded_columns]   # enforce column order

    pred_class = loaded_pipeline.predict(df_test)[0]
    pred_proba = loaded_pipeline.predict_proba(df_test)[0]   # [P(0), P(1)]
    confidence = pred_proba[1]

    print(f"\n  Input row:         IT Equipment, INR 4,50,000, 21-day lead, 82% historical OTR")
    print(f"  predicted_outcome: {pred_class}  (1=success, 0=failure)")
    print(f"  confidence_score:  {confidence:.4f}  (P(outcome=1))")
    print(f"  P(outcome=0):      {pred_proba[0]:.4f}")

    # Assertions — these must all pass for the model to be inference-ready
    assert pred_class in (0, 1),            "Predicted class must be 0 or 1"
    assert 0.0 <= confidence <= 1.0,        "Confidence must be in [0, 1]"
    assert abs(sum(pred_proba) - 1.0) < 1e-6, "Probabilities must sum to 1"
    assert len(loaded_columns) == len(ALL_FEATURES), "Feature count mismatch"
    assert TARGET not in loaded_columns,    f"Target '{TARGET}' must not be in feature list"
    for forbidden in FORBIDDEN_FEATURES:
        assert forbidden not in loaded_columns, f"Forbidden feature '{forbidden}' in artifact"

    print("\n  [PASS] All smoke-test assertions passed. Model is inference-ready.")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def print_section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


if __name__ == "__main__":
    print_section("ProcuraIQ — ML Training (Baseline Random Forest)")

    # 0. Load
    print_section("STEP 0: Load Dataset")
    df = load_data(DATA_PATH)

    # 1. Safety check
    print_section("STEP 1: Feature Safety Check")
    verify_feature_safety(df)
    print(f"Features to be used ({len(ALL_FEATURES)}):")
    for f in ALL_FEATURES:
        kind = "categorical" if f in CATEGORICAL_FEATURES else "numeric"
        print(f"  {f:<32} [{kind}]")

    # 2–3. Train + evaluate
    print_section("STEP 2–3: Train / Evaluate")
    results = train_and_evaluate(df)

    # 4. Save artifacts
    print_section("STEP 4: Save Artifacts")
    save_artifacts(results["pipeline"])

    # 5. Print evaluation report
    print_section("EVALUATION REPORT")
    cm = results["confusion_matrix"]
    print(f"""
  Training rows : {results['n_train']:,}
  Test rows     : {results['n_test']:,}

  --- Metrics (computed on held-out test set) ---
  Accuracy  : {results['accuracy']:.4f}  ({results['accuracy']:.2%})
  Precision : {results['precision']:.4f}  ({results['precision']:.2%})
  Recall    : {results['recall']:.4f}  ({results['recall']:.2%})
  F1 Score  : {results['f1']:.4f}  ({results['f1']:.2%})

  --- Confusion Matrix ---
  (rows=actual, cols=predicted; labels: 0=failure, 1=success)

              Pred 0   Pred 1
  Actual 0   {cm[0,0]:>6}   {cm[0,1]:>6}
  Actual 1   {cm[1,0]:>6}   {cm[1,1]:>6}

  True Negatives  (TN): {cm[0,0]:>6}  — correctly predicted failures
  False Positives (FP): {cm[0,1]:>6}  — predicted success, actually failed
  False Negatives (FN): {cm[1,0]:>6}  — predicted failure, actually succeeded
  True Positives  (TP): {cm[1,1]:>6}  — correctly predicted successes

  --- Random Forest Parameters ---""")
    for k, v in RF_PARAMS.items():
        print(f"  {k:<24}: {v}")
    print(f"""
  --- Artifacts ---
  model.joblib         : {MODEL_PATH}
  feature_columns.json : {FEATURE_COLUMNS_PATH}
""")

    # 6. Smoke test
    print_section("STEP 5: Inference Smoke Test")
    inference_smoke_test()

    print_section("COMPLETE")
    print("""
  Baseline training and validation complete.

  NEXT STEPS (wait for explicit instruction before proceeding):
  - Do NOT modify the dataset to improve metrics.
  - Do NOT adjust model parameters to hit an artificial target.
  - Report metrics above honestly to the team.
  - Proceed to backend API implementation when instructed.
""")
