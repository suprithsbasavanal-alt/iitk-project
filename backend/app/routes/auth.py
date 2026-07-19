from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db, Doctor, Patient
from backend.app.models.schemas import UserCreate, UserResponse, Token
from backend.app.auth.auth_service import (
    create_access_token, 
    get_password_hash, 
    get_current_user,
    get_current_admin
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

def authenticate_user(db: Session, username: str, password_raw: str):
    """Verifies credentials of Doctor or Patient."""
    from backend.app.auth.auth_service import verify_password
    # Try doctor login first
    doctor = db.query(Doctor).filter(Doctor.email == username).first()
    if doctor:
        if verify_password(password_raw, doctor.password):
            return doctor
            
    # Try patient login (username is Patient ID)
    patient = db.query(Patient).filter(Patient.id == username).first()
    if patient:
        # Patients login with their Patient ID or 'patient123'
        if password_raw == username or password_raw == "patient123":
            return Doctor(id=-1, name=patient.name, email=patient.id, role="patient", password="")
            
    return None

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "name": user.name,
        "email": user.email,
        "id": user.id
    }

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: Doctor = Depends(get_current_user)):
    return current_user

# Admin doctor management routes
@router.post("/doctors", response_model=UserResponse)
def create_doctor(doctor_in: UserCreate, db: Session = Depends(get_db), current_admin: Doctor = Depends(get_current_admin)):
    existing = db.query(Doctor).filter(Doctor.email == doctor_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_pwd = get_password_hash(doctor_in.password)
    db_doctor = Doctor(
        email=doctor_in.email,
        password=hashed_pwd,
        role="doctor",
        name=doctor_in.name
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db), current_admin: Doctor = Depends(get_current_admin)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id, Doctor.role == "doctor").first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    db.delete(doctor)
    db.commit()
    return {"detail": "Doctor deleted successfully"}

@router.get("/doctors", response_model=List[UserResponse])
def list_doctors(db: Session = Depends(get_db), current_admin: Doctor = Depends(get_current_admin)):
    doctors = db.query(Doctor).filter(Doctor.role == "doctor").all()
    return doctors
