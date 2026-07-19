from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from database.db import get_db, Patient, Prediction, Doctor
from backend.app.models.schemas import PredictionResponse
from backend.app.auth.auth_service import get_current_user, get_current_doctor_or_admin
import datetime

router = APIRouter(prefix="/api/predictions", tags=["Predictions"])

# Health form payload structure for Step 1 mock predictions
class HealthDataInput(BaseModel):
    patient_id: str
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int
    doctor_recommendation: Optional[str] = None

@router.post("/predict", response_model=PredictionResponse)
def create_prediction(
    prediction_in: HealthDataInput, 
    db: Session = Depends(get_db), 
    current_user: Doctor = Depends(get_current_doctor_or_admin)
):
    # 1. Verify Patient exists
    patient = db.query(Patient).filter(Patient.id == prediction_in.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {prediction_in.patient_id} not registered."
        )

    # 2. Mock prediction engine logic (Step 1 placeholder)
    # Simple deterministic rules to make the prototype feel real:
    # High BP (>140) or High Cholesterol (>240) -> HIGH RISK
    # Otherwise, if Moderate -> MEDIUM RISK, otherwise LOW RISK
    risk_level = "LOW RISK"
    risk_pct = 24.5
    confidence = 91.2

    if prediction_in.chol > 240 or prediction_in.trestbps > 140 or prediction_in.ca > 1:
        risk_level = "HIGH RISK"
        risk_pct = 93.0
        confidence = 95.2
    elif prediction_in.chol > 200 or prediction_in.trestbps > 120 or prediction_in.thalach < 130:
        risk_level = "MEDIUM RISK"
        risk_pct = 54.0
        confidence = 88.6

    # 3. Save prediction into SQLite Database
    db_prediction = Prediction(
        patient_id=prediction_in.patient_id,
        prediction=risk_level,
        risk_percentage=risk_pct,
        confidence=confidence,
        date=datetime.datetime.now().isoformat()
    )

    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

@router.get("/history", response_model=List[PredictionResponse])
def get_prediction_history(
    db: Session = Depends(get_db), 
    current_user: Doctor = Depends(get_current_user)
):
    if current_user.role == "patient":
        predictions = db.query(Prediction).filter(Prediction.patient_id == current_user.email).order_by(Prediction.date.desc()).all()
    else:
        predictions = db.query(Prediction).order_by(Prediction.date.desc()).all()
    return predictions

@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(
    prediction_id: int, 
    db: Session = Depends(get_db), 
    current_user: Doctor = Depends(get_current_user)
):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction record not found"
        )
    
    if current_user.role == "patient" and prediction.patient_id != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )
        
    return prediction
