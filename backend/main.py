import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import DB configurations
from backend.app.database.db import engine, Base, SessionLocal, Doctor, Patient, Prediction
from backend.app.auth.auth_service import get_password_hash

# Import routes
from backend.app.routes.auth import router as auth_router
from backend.app.routes.patients import router as patients_router
from backend.app.routes.predictions import router as predictions_router
from backend.app.routes.reports import router as reports_router
from backend.app.routes.analytics import router as analytics_router

# Ensure database directory exists
os.makedirs("database", exist_ok=True)

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HeartCare AI API",
    description="Backend diagnostics API for Step 1 project foundation.",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed Database
def seed_database():
    db = SessionLocal()
    try:
        # Check if Admin already exists
        admin_exists = db.query(Doctor).filter(Doctor.email == "admin@heartcare.ai").first()
        if not admin_exists:
            hashed_pw = get_password_hash("admin123")
            admin_user = Doctor(
                email="admin@heartcare.ai",
                password=hashed_pw,
                role="admin",
                name="System Administrator"
            )
            db.add(admin_user)
            print("Database seeded: default admin user created.")
            
        # Check if Doctor already exists
        doctor_exists = db.query(Doctor).filter(Doctor.email == "doctor@heartcare.ai").first()
        if not doctor_exists:
            hashed_pw = get_password_hash("doctor123")
            doctor_user = Doctor(
                email="doctor@heartcare.ai",
                password=hashed_pw,
                role="doctor",
                name="Dr. Julian Vance"
            )
            db.add(doctor_user)
            print("Database seeded: default doctor user created.")
            
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

seed_database()

# Register Routers
app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(predictions_router)
app.include_router(reports_router)
app.include_router(analytics_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to HeartCare AI - Step 1 Foundation API"}
