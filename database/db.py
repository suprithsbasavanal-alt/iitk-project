from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# SQLite database file path at the root database directory
DATABASE_URL = "sqlite:///database/heartcare.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # hashed password
    role = Column(String, default="doctor")    # 'doctor' or 'admin'

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True) # e.g. PAT-001
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)

    predictions = relationship("Prediction", back_populates="patient", cascade="all, delete-orphan")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    prediction = Column(String, nullable=False)  # 'LOW RISK', 'MEDIUM RISK', 'HIGH RISK'
    risk_percentage = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    date = Column(String, default=lambda: datetime.datetime.now().isoformat())

    patient = relationship("Patient", back_populates="predictions")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
