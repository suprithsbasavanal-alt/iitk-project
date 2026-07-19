from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import datetime
from database.db import get_db, Patient, Prediction, Doctor
from backend.app.auth.auth_service import get_current_doctor_or_admin

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db), current_user: Doctor = Depends(get_current_doctor_or_admin)):
    total_patients = db.query(Patient).count()
    predictions_made = db.query(Prediction).count()
    
    high_risk_patients = db.query(Prediction).filter(Prediction.prediction == "HIGH RISK").count()
    medium_risk = db.query(Prediction).filter(Prediction.prediction == "MEDIUM RISK").count()
    low_risk_patients = db.query(Prediction).filter(Prediction.prediction == "LOW RISK").count()

    recent_predictions_raw = db.query(Prediction).order_by(Prediction.date.desc()).limit(10).all()
    
    recent_predictions = []
    for pred in recent_predictions_raw:
        patient = db.query(Patient).filter(Patient.id == pred.patient_id).first()
        recent_predictions.append({
            "id": pred.id,
            "patient_id": pred.patient_id,
            "patient_name": patient.name if patient else "Unknown",
            "date": pred.date,
            "prediction_status": pred.prediction,
            "prediction_confidence": pred.confidence,
            "risk_percentage": pred.risk_percentage,
            "age": patient.age if patient else 50,
            "sex": 1 if patient and patient.gender == "Male" else 0
        })

    return {
        "total_patients": total_patients,
        "predictions_made": predictions_made,
        "high_risk_patients": high_risk_patients,
        "medium_risk_patients": medium_risk,
        "low_risk_patients": low_risk_patients,
        "prediction_accuracy": 67.2,
        "recent_predictions": recent_predictions
    }

@router.get("/charts-data")
def get_charts_data(db: Session = Depends(get_db), current_user: Doctor = Depends(get_current_doctor_or_admin)):
    male_count = db.query(Patient).filter(Patient.gender == "Male").count()
    female_count = db.query(Patient).filter(Patient.gender == "Female").count()

    low_risk = db.query(Prediction).filter(Prediction.prediction == "LOW RISK").count()
    med_risk = db.query(Prediction).filter(Prediction.prediction == "MEDIUM RISK").count()
    high_risk = db.query(Prediction).filter(Prediction.prediction == "HIGH RISK").count()

    patients = db.query(Patient.age).all()
    age_groups = {
        "Under 40": 0,
        "40-49": 0,
        "50-59": 0,
        "60-69": 0,
        "70+": 0
    }
    for p in patients:
        age = p.age
        if age < 40:
            age_groups["Under 40"] += 1
        elif age < 50:
            age_groups["40-49"] += 1
        elif age < 60:
            age_groups["50-59"] += 1
        elif age < 70:
            age_groups["60-69"] += 1
        else:
            age_groups["70+"] += 1

    predictions = db.query(Prediction.date).all()
    monthly_data = {}
    
    today = datetime.date.today()
    for i in range(5, -1, -1):
        d = today - datetime.timedelta(days=i*30)
        month_str = d.strftime("%b %Y")
        monthly_data[month_str] = 0

    for pred in predictions:
        try:
            pred_date = datetime.datetime.fromisoformat(pred.date)
            month_str = pred_date.strftime("%b %Y")
            if month_str in monthly_data:
                monthly_data[month_str] += 1
        except Exception:
            pass

    timeline_labels = list(monthly_data.keys())
    timeline_values = list(monthly_data.values())

    return {
        "gender_distribution": {
            "labels": ["Male", "Female"],
            "datasets": [male_count, female_count]
        },
        "risk_distribution": {
            "labels": ["Low Risk", "Medium Risk", "High Risk"],
            "datasets": [low_risk, med_risk, high_risk]
        },
        "age_distribution": {
            "labels": list(age_groups.keys()),
            "datasets": list(age_groups.values())
        },
        "monthly_predictions": {
            "labels": timeline_labels,
            "datasets": timeline_values
        }
    }
