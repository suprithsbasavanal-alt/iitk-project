from pydantic import BaseModel, EmailStr
from typing import Optional, List

# User/Doctor Schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "doctor"  # 'doctor' or 'admin'

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    name: str
    email: str
    id: int

# Patient Schemas
class PatientCreate(BaseModel):
    id: str  # e.g., PAT-001
    name: str
    age: int
    gender: str
    phone: Optional[str] = None
    email: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None

class PatientResponse(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    phone: Optional[str] = None
    email: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None

    class Config:
        from_attributes = True

# Prediction Schemas
class PredictionCreate(BaseModel):
    patient_id: str
    prediction: str          # 'LOW RISK', 'MEDIUM RISK', 'HIGH RISK'
    risk_percentage: float
    confidence: float

class PredictionResponse(BaseModel):
    id: int
    patient_id: str
    prediction: str
    risk_percentage: float
    confidence: float
    date: str
    recommendation: Optional[str] = None   # AI-generated clinical recommendation

    class Config:
        from_attributes = True

# Dashboard Stats Schemas
class DashboardStats(BaseModel):
    total_patients: int
    predictions_made: int
    high_risk_patients: int
    low_risk_patients: int
    medium_risk_patients: int
    prediction_accuracy: float
    recent_predictions: List[PredictionResponse]
