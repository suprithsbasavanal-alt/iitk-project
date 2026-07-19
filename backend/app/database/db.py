from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# SQLite database file path in the backend directory
DATABASE_URL = "sqlite:///backend/heartcare.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'admin', 'doctor', 'patient'
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

    predictions = relationship("Prediction", back_populates="doctor")

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(String, primary_key=True, index=True)  # e.g., PAT-001
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)  # 'Male', 'Female'
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    height = Column(Float, nullable=True)  # in cm
    weight = Column(Float, nullable=True)  # in kg

    predictions = relationship("Prediction", back_populates="patient", cascade="all, delete-orphan")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Can be null if patient logs in or system prediction
    date = Column(String, default=lambda: datetime.datetime.now().isoformat())
    
    # Clinical input variables
    age = Column(Integer, nullable=False)
    sex = Column(Integer, nullable=False)  # 1 = Male, 0 = Female
    cp = Column(Integer, nullable=False)   # 1, 2, 3, 4
    trestbps = Column(Integer, nullable=False)
    chol = Column(Integer, nullable=False)
    fbs = Column(Integer, nullable=False)  # 1 = Yes, 0 = No
    restecg = Column(Integer, nullable=False) # 0, 1, 2
    thalach = Column(Integer, nullable=False)
    exang = Column(Integer, nullable=False) # 1 = Yes, 0 = No
    oldpeak = Column(Float, nullable=False)
    slope = Column(Integer, nullable=False) # 1, 2, 3
    ca = Column(Integer, nullable=False)    # 0, 1, 2, 3
    thal = Column(Integer, nullable=False)  # 3 = normal, 6 = fixed, 7 = reversible

    # AI prediction outputs
    prediction_status = Column(String, nullable=False)  # 'LOW RISK', 'MEDIUM RISK', 'HIGH RISK'
    prediction_confidence = Column(Float, nullable=False)
    risk_percentage = Column(Float, nullable=False)
    doctor_recommendation = Column(String, nullable=True)

    patient = relationship("Patient", back_populates="predictions")
    doctor = relationship("User", back_populates="predictions")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
