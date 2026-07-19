import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import DB configurations
from backend.app.database.db import engine, Base, SessionLocal, User, Patient, Prediction
from backend.app.auth.auth_service import get_password_hash

# Import routes
from backend.app.routes.auth import router as auth_router
from backend.app.routes.patients import router as patients_router
from backend.app.routes.predictions import router as predictions_router
from backend.app.routes.reports import router as reports_router
from backend.app.routes.analytics import router as analytics_router

# Ensure directory is treated as package and model is loaded
from backend.app.services.prediction_service import prediction_service

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HeartCare AI API",
    description="Backend prediction and reporting system for heart disease risk classification.",
    version="1.0.0"
)

# CORS setup for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed Database
def seed_database():
    db = SessionLocal()
    try:
        # Check if Admin already exists
        admin_exists = db.query(User).filter(User.username == "admin").first()
        if not admin_exists:
            hashed_pw = get_password_hash("admin123")
            admin_user = User(
                username="admin",
                hashed_password=hashed_pw,
                role="admin",
                name="System Administrator",
                email="admin@heartcare.ai"
            )
            db.add(admin_user)
            print("Database seeded: default admin user created.")
            
        # Check if Doctor already exists
        doctor_exists = db.query(User).filter(User.username == "doctor").first()
        if not doctor_exists:
            hashed_pw = get_password_hash("doctor123")
            doctor_user = User(
                username="doctor",
                hashed_password=hashed_pw,
                role="doctor",
                name="Dr. Julian Vance",
                email="julian.vance@heartcare.ai",
                phone="555-0192"
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
    return {"message": "Welcome to HeartCare AI - Heart Disease Prediction API"}
