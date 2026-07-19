from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any, List
import datetime
from backend.app.database.db import get_db, Patient, Prediction, User
from backend.app.auth.auth_service import get_current_doctor_or_admin

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_doctor_or_admin)):
    """
    Returns general stats for the clinician dashboard.
    """
    total_patients = db.query(Patient).count()
    predictions_made = db.query(Prediction).count()
    
    high_risk_patients = db.query(Prediction).filter(Prediction.prediction_status == "HIGH RISK").count()
    medium_risk = db.query(Prediction).filter(Prediction.prediction_status == "MEDIUM RISK").count()
    low_risk_patients = db.query(Prediction).filter(Prediction.prediction_status == "LOW RISK").count()

    # Get recent predictions with patient names
    recent_predictions_raw = db.query(Prediction).order_by(Prediction.date.desc()).limit(10).all()
    
    recent_predictions = []
    for pred in recent_predictions_raw:
        patient = db.query(Patient).filter(Patient.patient_id == pred.patient_id).first()
        recent_predictions.append({
            "id": pred.id,
            "patient_id": pred.patient_id,
            "patient_name": patient.name if patient else "Unknown",
            "date": pred.date,
            "prediction_status": pred.prediction_status,
            "prediction_confidence": pred.prediction_confidence,
            "risk_percentage": pred.risk_percentage,
            "age": pred.age,
            "sex": pred.sex
        })

    # Fixed base accuracy for this trained model
    accuracy = 67.2

    return {
        "total_patients": total_patients,
        "predictions_made": predictions_made,
        "high_risk_patients": high_risk_patients,
        "medium_risk_patients": medium_risk,
        "low_risk_patients": low_risk_patients,
        "prediction_accuracy": accuracy,
        "recent_predictions": recent_predictions
    }

@router.get("/charts-data")
def get_charts_data(db: Session = Depends(get_db), current_user: User = Depends(get_current_doctor_or_admin)):
    """
    Returns grouped data for frontend chart visualizers.
    """
    # 1. Male vs Female distribution
    male_count = db.query(Patient).filter(Patient.gender == "Male").count()
    female_count = db.query(Patient).filter(Patient.gender == "Female").count()

    # 2. Risk classification distribution
    low_risk = db.query(Prediction).filter(Prediction.prediction_status == "LOW RISK").count()
    med_risk = db.query(Prediction).filter(Prediction.prediction_status == "MEDIUM RISK").count()
    high_risk = db.query(Prediction).filter(Prediction.prediction_status == "HIGH RISK").count()

    # 3. Age Distribution
    # Under 40, 40-49, 50-59, 60-69, 70+
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

    # 4. Predictions by month (Last 6 months)
    # Since we use SQLite, we can parse ISO dates to get months
    predictions = db.query(Prediction.date).all()
    monthly_data = {}
    
    # Pre-populate past 6 months
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
