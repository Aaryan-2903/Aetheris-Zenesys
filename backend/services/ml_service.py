import os
import json
import joblib
import pandas as pd
import logging
from backend.models.schemas import PredictionRequest, PredictionResponse

logger = logging.getLogger(__name__)

# Paths relative to this file's location
_HERE = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.join(os.path.dirname(_HERE), "ml")
MODEL_PATH = os.path.join(ML_DIR, "model.joblib")
FEATURE_COLUMNS_PATH = os.path.join(ML_DIR, "feature_columns.json")

# Global variables to hold the loaded model and feature list
_pipeline = None
_feature_columns = None

def _load_model_artifacts():
    """Loads the model pipeline and feature columns if not already loaded."""
    global _pipeline, _feature_columns
    
    if _pipeline is not None and _feature_columns is not None:
        return
        
    try:
        logger.info(f"Loading ML model from {MODEL_PATH}")
        _pipeline = joblib.load(MODEL_PATH)
        
        logger.info(f"Loading feature columns from {FEATURE_COLUMNS_PATH}")
        with open(FEATURE_COLUMNS_PATH, "r", encoding="utf-8") as f:
            _feature_columns = json.load(f)
            
        logger.info("ML artifacts loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load ML artifacts: {e}")
        raise RuntimeError(f"ML artifacts could not be loaded: {e}")

def get_prediction(request: PredictionRequest) -> PredictionResponse:
    """
    Performs inference using the loaded model.
    """
    _load_model_artifacts()
    
    # Convert request to dict and then DataFrame to enforce column order
    input_data = request.model_dump()
    
    # Ensure all required features are present
    missing = set(_feature_columns) - set(input_data.keys())
    if missing:
        raise ValueError(f"Missing required features: {missing}")
        
    # Create DataFrame with the exact column order expected by the model
    df_input = pd.DataFrame([input_data])[_feature_columns]
    
    try:
        # Perform prediction
        pred_class = int(_pipeline.predict(df_input)[0])
        pred_proba = _pipeline.predict_proba(df_input)[0]
        confidence = float(pred_proba[1])  # P(outcome=1)
        
        return PredictionResponse(
            predicted_outcome=pred_class,
            confidence_score=confidence
        )
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise RuntimeError(f"Prediction failed: {e}")
