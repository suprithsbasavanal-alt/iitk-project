from pydantic import BaseModel, EmailStr
from typing import Optional, List
import datetime

# User Schemas
class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # 'admin', 'doctor', 'patient'
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    name: str
    username: str
    id: int

# Patient Schemas
class PatientCreate(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str  # 'Male', 'Female'
    phone: Optional[str] = None
    email: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None

class PatientResponse(BaseModel):
    patient_id: str
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
    age: int
    sex: int  # 1 = Male, 0 = Female
    cp: int   # 1, 2, 3, 4
    trestbps: int
    chol: int
    fbs: int  # 1 = Yes, 0 = No
    restecg: int # 0, 1, 2
    thalach: int
    exang: int # 1 = Yes, 0 = No
    oldpeak: float
    slope: int # 1, 2, 3
    ca: int    # 0, 1, 2, 3
    thal: int  # 3 = normal, 6 = fixed, 7 = reversible
    doctor_recommendation: Optional[str] = None

class PredictionResponse(BaseModel):
    id: int
    patient_id: str
    doctor_id: Optional[int] = None
    date: str
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
    prediction_status: str
    prediction_confidence: float
    risk_percentage: float
    doctor_recommendation: Optional[str] = None

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
