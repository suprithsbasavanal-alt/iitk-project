import os
import pytest
from backend.app.services.prediction_service import prediction_service

def test_ml_artifacts_exist():
    assert os.path.exists("ml/heart_model.pkl"), "heart_model.pkl must exist"
    assert os.path.exists("ml/scaler.pkl"), "scaler.pkl must exist"

def test_prediction_service_loaded():
    assert prediction_service.model is not None, "Model should be loaded"
    assert prediction_service.scaler is not None, "Scaler should be loaded"

def test_prediction_low_risk():
    # Patient with healthy parameters
    data = {
        "age": 35,
        "sex": 0,
        "cp": 1,
        "trestbps": 110,
        "chol": 170,
        "fbs": 0,
        "restecg": 0,
        "thalach": 175,
        "exang": 0,
        "oldpeak": 0.0,
        "slope": 1,
        "ca": 0,
        "thal": 3
    }
    result = prediction_service.predict(data)
    assert result["prediction_status"] in ["LOW RISK", "MEDIUM RISK", "HIGH RISK"]
    assert 0.0 <= result["risk_percentage"] <= 100.0
    assert 0.0 <= result["prediction_confidence"] <= 100.0
    assert len(result["recommendation"]) > 0

def test_prediction_high_risk():
    # Patient with severe cardiac indicators
    data = {
        "age": 65,
        "sex": 1,
        "cp": 4,
        "trestbps": 170,
        "chol": 310,
        "fbs": 1,
        "restecg": 2,
        "thalach": 110,
        "exang": 1,
        "oldpeak": 3.0,
        "slope": 3,
        "ca": 3,
        "thal": 7
    }
    result = prediction_service.predict(data)
    assert result["prediction_status"] == "HIGH RISK"
    assert result["risk_percentage"] > 50.0
    assert len(result["recommendation"]) > 0
