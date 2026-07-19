from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from backend.app.database.db import get_db, User, Patient
from backend.app.models.schemas import UserCreate, UserResponse, Token
from backend.app.auth.auth_service import (
    create_access_token, 
    get_password_hash, 
    get_current_user,
    get_current_admin
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

def authenticate_user(db: Session, username: str, password_raw: str):
    """Verifies user credentials."""
    from backend.app.auth.auth_service import verify_password
    user = db.query(User).filter(User.username == username).first()
    if not user:
        # Check if username is a Patient ID (for patient login)
        patient = db.query(Patient).filter(Patient.patient_id == username).first()
        if patient:
            # Patients login with their Patient ID as password by default (or "patient123")
            if password_raw == username or password_raw == "patient123":
                # Create a temporary virtual user for patient
                return User(id=-1, username=patient.patient_id, role="patient", name=patient.name)
        return False
        
    if not verify_password(password_raw, user.hashed_password):
        return False
    return user

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "name": user.name,
        "username": user.username,
        "id": user.id
    }

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Admin doctor management routes
@router.post("/doctors", response_model=UserResponse)
def create_doctor(doctor_in: UserCreate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    existing = db.query(User).filter(User.username == doctor_in.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_pwd = get_password_hash(doctor_in.password)
    db_doctor = User(
        username=doctor_in.username,
        hashed_password=hashed_pwd,
        role="doctor",
        name=doctor_in.name,
        phone=doctor_in.phone,
        email=doctor_in.email
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    doctor = db.query(User).filter(User.id == doctor_id, User.role == "doctor").first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    db.delete(doctor)
    db.commit()
    return {"detail": "Doctor deleted successfully"}

@router.get("/doctors", response_model=List[UserResponse])
def list_doctors(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    doctors = db.query(User).filter(User.role == "doctor").all()
    return doctors
