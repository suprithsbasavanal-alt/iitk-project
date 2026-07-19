from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database.db import get_db, Patient, Prediction, User
from backend.app.models.schemas import PredictionCreate, PredictionResponse
from backend.app.services.prediction_service import prediction_service
from backend.app.auth.auth_service import get_current_user, get_current_doctor_or_admin

router = APIRouter(prefix="/api/predictions", tags=["Predictions"])

@router.post("/predict", response_model=PredictionResponse)
def create_prediction(
    prediction_in: PredictionCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_doctor_or_admin)
):
    # 1. Verify Patient exists
    patient = db.query(Patient).filter(Patient.patient_id == prediction_in.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {prediction_in.patient_id} not registered. Please register the patient first."
        )

    # 2. Run AI Prediction
    # Map raw fields to dictionary expected by prediction service
    data_dict = prediction_in.model_dump()
    # Remove metadata
    data_dict.pop('patient_id')
    data_dict.pop('doctor_recommendation', None)

    try:
        prediction_result = prediction_service.predict(data_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Prediction Engine Error: {str(e)}"
        )

    # Override recommendation if doctor specified a custom one
    recommendation = prediction_in.doctor_recommendation or prediction_result['recommendation']

    # 3. Create prediction database entry
    db_prediction = Prediction(
        patient_id=prediction_in.patient_id,
        doctor_id=current_user.id if current_user.role != "admin" else None,
        age=prediction_in.age,
        sex=prediction_in.sex,
        cp=prediction_in.cp,
        trestbps=prediction_in.trestbps,
        chol=prediction_in.chol,
        fbs=prediction_in.fbs,
        restecg=prediction_in.restecg,
        thalach=prediction_in.thalach,
        exang=prediction_in.exang,
        oldpeak=prediction_in.oldpeak,
        slope=prediction_in.slope,
        ca=prediction_in.ca,
        thal=prediction_in.thal,
        prediction_status=prediction_result['prediction_status'],
        prediction_confidence=prediction_result['prediction_confidence'],
        risk_percentage=prediction_result['risk_percentage'],
        doctor_recommendation=recommendation
    )

    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

@router.get("/history", response_model=List[PredictionResponse])
def get_prediction_history(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # If the user is a patient, they can only get their own predictions
    if current_user.role == "patient":
        predictions = db.query(Prediction).filter(Prediction.patient_id == current_user.username).order_by(Prediction.date.desc()).all()
    else:
        # Doctors and Admins see all predictions
        predictions = db.query(Prediction).order_by(Prediction.date.desc()).all()
    return predictions

@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(
    prediction_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction record not found"
        )
    
    # Patient role checks
    if current_user.role == "patient" and prediction.patient_id != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only view your own predictions."
        )
        
    return prediction
