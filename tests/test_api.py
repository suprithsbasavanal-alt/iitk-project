import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_doctor_login_success():
    response = client.post(
        "/api/auth/token",
        data={"username": "doctor@heartcare.ai", "password": "doctor123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "doctor"

def test_login_invalid_password():
    response = client.post(
        "/api/auth/token",
        data={"username": "doctor@heartcare.ai", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_patient_registration_and_prediction_flow():
    # 1. Login as Doctor
    login_res = client.post(
        "/api/auth/token",
        data={"username": "doctor@heartcare.ai", "password": "doctor123"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Register a Patient
    patient_data = {
        "id": "PAT-PYTEST-01",
        "name": "Pytest Patient",
        "age": 52,
        "gender": "Female",
        "phone": "5551234567",
        "email": "pytest@example.com",
        "height": 165.0,
        "weight": 68.0
    }
    reg_res = client.post("/api/patients/", json=patient_data, headers=headers)
    # 200 or 400 (if patient ID already exists from previous runs)
    assert reg_res.status_code in [200, 400]

    # 3. Submit Prediction
    pred_payload = {
        "patient_id": "PAT-PYTEST-01",
        "age": 52,
        "sex": 0,
        "cp": 2,
        "trestbps": 125,
        "chol": 215,
        "fbs": 0,
        "restecg": 0,
        "thalach": 158,
        "exang": 0,
        "oldpeak": 0.5,
        "slope": 1,
        "ca": 0,
        "thal": 3
    }
    pred_res = client.post("/api/predictions/predict", json=pred_payload, headers=headers)
    assert pred_res.status_code == 200
    pred_data = pred_res.json()
    assert "prediction" in pred_data
    assert "risk_percentage" in pred_data
    assert "confidence" in pred_data
    pred_id = pred_data["id"]

    # 4. Download PDF report
    pdf_res = client.get(f"/api/reports/{pred_id}/pdf", headers=headers)
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert len(pdf_res.content) > 0

def test_analytics_summary():
    login_res = client.post(
        "/api/auth/token",
        data={"username": "doctor@heartcare.ai", "password": "doctor123"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/analytics/summary", headers=headers)
    assert res.status_code == 200
    summary = res.json()
    assert "total_patients" in summary
    assert "predictions_made" in summary
    assert "high_risk_patients" in summary
