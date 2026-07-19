from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database.db import get_db, Patient, Prediction, User
from backend.app.models.schemas import PatientCreate, PatientResponse, PredictionResponse
from backend.app.auth.auth_service import get_current_user, get_current_doctor_or_admin

router = APIRouter(prefix="/api/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse)
def register_patient(patient_in: PatientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_doctor_or_admin)):
    existing = db.query(Patient).filter(Patient.patient_id == patient_in.patient_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient ID already exists"
        )
    
    db_patient = Patient(
        patient_id=patient_in.patient_id,
        name=patient_in.name,
        age=patient_in.age,
        gender=patient_in.gender,
        phone=patient_in.phone,
        email=patient_in.email,
        height=patient_in.height,
        weight=patient_in.weight
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/", response_model=List[PatientResponse])
def list_patients(db: Session = Depends(get_db), current_user: User = Depends(get_current_doctor_or_admin)):
    patients = db.query(Patient).all()
    return patients

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check permissions: patients can only access their own profile
    if current_user.role == "patient" and current_user.username != patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only view your own profile."
        )
        
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    return patient

@router.get("/{patient_id}/predictions", response_model=List[PredictionResponse])
def get_patient_predictions(patient_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check permissions
    if current_user.role == "patient" and current_user.username != patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only view your own predictions."
        )
        
    predictions = db.query(Prediction).filter(Prediction.patient_id == patient_id).order_by(Prediction.date.desc()).all()
    return predictions
