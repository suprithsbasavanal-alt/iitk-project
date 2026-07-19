from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend.app.database.db import get_db, Prediction, Patient, User
from backend.app.services.pdf_service import generate_pdf_report
from backend.app.auth.auth_service import get_current_user

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/{prediction_id}/pdf")
def download_prediction_pdf(
    prediction_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # 1. Fetch prediction
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction record not found"
        )
    
    # Permission checks for patients
    if current_user.role == "patient" and prediction.patient_id != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only download your own reports."
        )

    # 2. Fetch patient
    patient = db.query(Patient).filter(Patient.patient_id == prediction.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated patient profile not found"
        )

    # 3. Fetch doctor name
    doctor_name = "System AI Engine"
    if prediction.doctor_id:
        doctor = db.query(User).filter(User.id == prediction.doctor_id).first()
        if doctor:
            doctor_name = doctor.name

    # 4. Generate report
    try:
        # Convert objects to dictionaries
        patient_dict = {
            "patient_id": patient.patient_id,
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "phone": patient.phone,
            "email": patient.email,
            "height": patient.height,
            "weight": patient.weight
        }

        prediction_dict = {
            "id": prediction.id,
            "date": prediction.date,
            "trestbps": prediction.trestbps,
            "chol": prediction.chol,
            "cp": prediction.cp,
            "fbs": prediction.fbs,
            "restecg": prediction.restecg,
            "thalach": prediction.thalach,
            "exang": prediction.exang,
            "oldpeak": prediction.oldpeak,
            "slope": prediction.slope,
            "ca": prediction.ca,
            "thal": prediction.thal,
            "prediction_status": prediction.prediction_status,
            "prediction_confidence": prediction.prediction_confidence,
            "risk_percentage": prediction.risk_percentage,
            "doctor_recommendation": prediction.doctor_recommendation
        }

        pdf_buffer = generate_pdf_report(patient_dict, prediction_dict, doctor_name)
        
        # Return response streaming the file
        filename = f"HeartCare_Report_{patient.patient_id}_{prediction.id}.pdf"
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
