from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from database.db import get_db, Patient, Prediction, Doctor
from backend.app.models.schemas import PredictionResponse
from backend.app.auth.auth_service import get_current_user, get_current_doctor_or_admin
from backend.app.services.prediction_service import prediction_service
import datetime
import json

router = APIRouter(prefix="/api/predictions", tags=["Predictions"])

# Health form payload structure — 13 clinical features from Cleveland dataset
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

    # 2. Check model is ready
    if prediction_service.model is None or prediction_service.scaler is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI model is not loaded. Please run ml/train_model.py first."
        )

    # 3. Run real AI prediction
    clinical_inputs = {
        "age": prediction_in.age,
        "sex": prediction_in.sex,
        "cp": prediction_in.cp,
        "trestbps": prediction_in.trestbps,
        "chol": prediction_in.chol,
        "fbs": prediction_in.fbs,
        "restecg": prediction_in.restecg,
        "thalach": prediction_in.thalach,
        "exang": prediction_in.exang,
        "oldpeak": prediction_in.oldpeak,
        "slope": prediction_in.slope,
        "ca": prediction_in.ca,
        "thal": prediction_in.thal
    }

    try:
        result = prediction_service.predict(clinical_inputs)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction engine error: {str(e)}"
        )

    # Use doctor override recommendation if provided, else use AI-generated one
    final_recommendation = prediction_in.doctor_recommendation or result["recommendation"]

    # 4. Save prediction result into SQLite Database (including raw clinical inputs)
    db_prediction = Prediction(
        patient_id=prediction_in.patient_id,
        prediction=result["prediction_status"],
        risk_percentage=result["risk_percentage"],
        confidence=result["prediction_confidence"],
        date=datetime.datetime.now().isoformat(),
        clinical_data=json.dumps(clinical_inputs),
        recommendation=final_recommendation
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
        predictions = db.query(Prediction).filter(
            Prediction.patient_id == current_user.email
        ).order_by(Prediction.date.desc()).all()
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
