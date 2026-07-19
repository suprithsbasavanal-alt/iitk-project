from database.db import engine, Base, SessionLocal, Doctor, Patient, Prediction, get_db

# Map Doctor to User for compatibility with backend models
User = Doctor
