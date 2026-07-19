from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json
from database.db import get_db, Prediction, Patient, Doctor
from backend.app.services.pdf_service import generate_pdf_report
from backend.app.auth.auth_service import get_current_user

router = APIRouter(prefix="/api/reports", tags=["Reports"])

# Default clinical baselines to use when a prediction has no stored clinical_data (legacy Step 1 records)
DEFAULT_CLINICAL = {
    "trestbps": 120, "chol": 210, "cp": 4, "fbs": 0,
    "restecg": 0, "thalach": 150, "exang": 0,
    "oldpeak": 0.0, "slope": 2, "ca": 0, "thal": 3
}

@router.get("/{prediction_id}/pdf")
def download_prediction_pdf(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: Doctor = Depends(get_current_user)
):
    # 1. Fetch prediction
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction record not found"
        )

    # Permission checks for patients
    if current_user.role == "patient" and prediction.patient_id != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )

    # 2. Fetch patient
    patient = db.query(Patient).filter(Patient.id == prediction.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated patient profile not found"
        )

    # 3. Determine doctor name from current user
    doctor_name = current_user.name if current_user.role != "patient" else "HeartCare AI System"

    # 4. Build data dicts for PDF
    try:
        patient_dict = {
            "patient_id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "phone": patient.phone,
            "email": patient.email,
            "height": patient.height,
            "weight": patient.weight
        }

        # Load stored clinical inputs (populated by /predict endpoint for real AI predictions)
        # Fall back to defaults for legacy Step 1 mock records
        if prediction.clinical_data:
            clinical = json.loads(prediction.clinical_data)
        else:
            clinical = DEFAULT_CLINICAL

        prediction_dict = {
            "id": prediction.id,
            "date": prediction.date,
            "trestbps": clinical.get("trestbps", 120),
            "chol": clinical.get("chol", 210),
            "cp": clinical.get("cp", 4),
            "fbs": clinical.get("fbs", 0),
            "restecg": clinical.get("restecg", 0),
            "thalach": clinical.get("thalach", 150),
            "exang": clinical.get("exang", 0),
            "oldpeak": clinical.get("oldpeak", 0.0),
            "slope": clinical.get("slope", 2),
            "ca": clinical.get("ca", 0),
            "thal": clinical.get("thal", 3),
            "prediction_status": prediction.prediction,
            "prediction_confidence": prediction.confidence,
            "risk_percentage": prediction.risk_percentage,
            "recommendation": prediction.recommendation or "No specific recommendations provided.",
            "doctor_recommendation": None
        }

        pdf_buffer = generate_pdf_report(patient_dict, prediction_dict, doctor_name)

        filename = f"HeartCare_Report_{patient.id}_{prediction.id}.pdf"
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating PDF report: {str(e)}"
        )
