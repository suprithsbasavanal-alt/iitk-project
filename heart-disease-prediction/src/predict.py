"""
Prediction and Inference Module for Heart Disease Prediction (Part 7).

This module provides robust, end-to-end inference routines using the frozen final model pipeline
(`models/final/final_model.joblib`). It accepts raw feature data (DataFrame or Dictionary),
performs schema and input validation, and returns structured risk predictions without using
medical diagnosis terminology.
"""

from pathlib import Path
from typing import Any, Dict, List, Union
import joblib
import numpy as np
import pandas as pd

# Define mandatory 13 predictor feature names
REQUIRED_FEATURES: List[str] = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]

# Project root path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FINAL_MODEL_PATH = PROJECT_ROOT / "models" / "final" / "final_model.joblib"


def load_final_model(model_path: Union[str, Path] = FINAL_MODEL_PATH) -> Any:
    """
    Load the serialized final model pipeline artifact from disk.

    Args:
        model_path (Union[str, Path]): Path to the joblib model artifact.

    Returns:
        Any: Scikit-learn Pipeline object combining preprocessor and classifier.
    """
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Final model artifact not found at: {path.resolve()}")
    
    model = joblib.load(path)
    return model


def validate_input_data(input_data: Union[pd.DataFrame, Dict[str, Any]]) -> pd.DataFrame:
    """
    Validate raw input data against expected feature names, data types, and value constraints.

    Args:
        input_data (Union[pd.DataFrame, Dict[str, Any]]): Input data sample(s).

    Returns:
        pd.DataFrame: Validated DataFrame with correct column ordering.

    Raises:
        ValueError: If required features are missing or invalid data types are supplied.
        TypeError: If input_data format is unsupported.
    """
    if isinstance(input_data, dict):
        df = pd.DataFrame([input_data])
    elif isinstance(input_data, pd.DataFrame):
        df = input_data.copy()
    else:
        raise TypeError(f"Unsupported input_data type: {type(input_data)}. Must be pandas DataFrame or dict.")

    # Check missing features
    missing_cols = [col for col in REQUIRED_FEATURES if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Input data is missing required feature(s): {missing_cols}")

    # Reorder columns strictly to match training schema
    df = df[REQUIRED_FEATURES]

    # Validate numeric types
    for col in df.columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            # Try coercion
            try:
                df[col] = pd.to_numeric(df[col])
            except Exception as e:
                raise ValueError(f"Feature '{col}' contains non-numeric values that could not be converted: {df[col].tolist()}") from e

    # Check for empty input
    if df.empty:
        raise ValueError("Input dataset contains 0 rows.")

    return df


def predict_heart_disease(
    input_data: Union[pd.DataFrame, Dict[str, Any]],
    model_path: Union[str, Path] = FINAL_MODEL_PATH
) -> Dict[str, Any]:
    """
    Generate heart disease risk predictions for raw clinical patient features using the final pipeline.

    Args:
        input_data (Union[pd.DataFrame, Dict[str, Any]]): Raw patient feature data.
        model_path (Union[str, Path]): Path to final model pipeline joblib.

    Returns:
        Dict[str, Any]: Structured prediction output dictionary containing:
            - 'predicted_class': List[int] (0 = No Disease, 1 = Disease Present)
            - 'predicted_label': List[str]
            - 'probability_no_disease': List[float]
            - 'probability_disease': List[float]
            - 'prediction_message': List[str]
    """
    # Step 1: Validate input format & schema
    validated_df = validate_input_data(input_data)

    # Step 2: Load final pipeline model
    pipeline = load_final_model(model_path)

    # Step 3: Compute class predictions and class probabilities
    raw_preds = pipeline.predict(validated_df)
    
    if hasattr(pipeline, "predict_proba"):
        probs = pipeline.predict_proba(validated_df)
        prob_no_disease = probs[:, 0].tolist()
        prob_disease = probs[:, 1].tolist()
    else:
        # Fallback if probability calculation unavailable
        prob_disease = raw_preds.astype(float).tolist()
        prob_no_disease = (1.0 - raw_preds.astype(float)).tolist()

    # Step 4: Format human-readable output without medical diagnosis language
    predicted_labels = ["Heart Disease Present" if p == 1 else "No Heart Disease" for p in raw_preds]
    prediction_messages = [f"Model prediction: {label} (Probability: {prob:.4f})" for label, prob in zip(predicted_labels, prob_disease)]

    result = {
        "predicted_class": raw_preds.tolist(),
        "predicted_label": predicted_labels,
        "probability_no_disease": prob_no_disease,
        "probability_disease": prob_disease,
        "prediction_message": prediction_messages,
    }

    return result
