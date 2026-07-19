# HeartCare AI — API Reference

Base URL: `http://localhost:8000`  
Interactive Docs: `http://localhost:8000/docs`  
Authentication: **Bearer JWT Token** (obtain from `/api/auth/token`)

---

## Authentication

### POST `/api/auth/token`
Log in and receive a JWT access token.

**Request (form-data):**
| Field | Type | Description |
| :--- | :--- | :--- |
| `username` | string | Doctor email or Patient ID |
| `password` | string | Password |

**Response:**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "role": "doctor",
  "name": "Dr. Smith"
}
```

---

## Patients

### GET `/api/patients/`
Returns all patient profiles.  
**Auth:** Required (Doctor / Admin)

### POST `/api/patients/`
Register a new patient.  
**Auth:** Required (Doctor / Admin)

**Body:**
```json
{
  "id": "PAT-001",
  "name": "John Doe",
  "age": 58,
  "gender": "Male",
  "phone": "9876543210",
  "email": "john@example.com",
  "height": 172.0,
  "weight": 80.0
}
```

---

## Predictions

### POST `/api/predictions/predict`
Submit clinical inputs and receive an AI heart disease risk prediction.  
**Auth:** Required (Doctor / Admin)

**Body (13 clinical features):**
```json
{
  "patient_id": "PAT-001",
  "age": 58,
  "sex": 1,
  "cp": 4,
  "trestbps": 150,
  "chol": 260,
  "fbs": 0,
  "restecg": 0,
  "thalach": 140,
  "exang": 0,
  "oldpeak": 1.5,
  "slope": 2,
  "ca": 2,
  "thal": 7,
  "doctor_recommendation": null
}
```

**Response:**
```json
{
  "id": 1,
  "patient_id": "PAT-001",
  "prediction": "HIGH RISK",
  "risk_percentage": 73.0,
  "confidence": 51.3,
  "date": "2026-07-19T20:24:17",
  "recommendation": "1. Schedule an immediate consultation with a cardiologist.\n2. Perform diagnostic ECG..."
}
```

**Feature Encodings:**

| Feature | Values |
| :--- | :--- |
| `sex` | `1` = Male, `0` = Female |
| `cp` (Chest Pain) | `1`=Typical Angina, `2`=Atypical, `3`=Non-anginal, `4`=Asymptomatic |
| `fbs` (Fasting Blood Sugar) | `1` = >120 mg/dL, `0` = Normal |
| `restecg` | `0`=Normal, `1`=ST-T Abnormality, `2`=LV Hypertrophy |
| `exang` | `1` = Yes, `0` = No |
| `slope` | `1`=Upsloping, `2`=Flat, `3`=Downsloping |
| `ca` | Number of major vessels colored (0–3) |
| `thal` | `3`=Normal, `6`=Fixed Defect, `7`=Reversible Defect |

### GET `/api/predictions/history`
Returns all prediction records. Doctors see all; patients see their own.  
**Auth:** Required

### GET `/api/predictions/{prediction_id}`
Returns a single prediction record.  
**Auth:** Required

---

## Reports

### GET `/api/reports/{prediction_id}/pdf`
Downloads a professionally formatted PDF clinical report for the prediction.  
**Auth:** Required  
**Response:** `application/pdf` stream

---

## Analytics

### GET `/api/analytics/summary`
Returns live dashboard statistics.  
**Auth:** Required

**Response:**
```json
{
  "total_patients": 42,
  "predictions_made": 87,
  "high_risk_patients": 18,
  "medium_risk_patients": 31,
  "low_risk_patients": 38,
  "prediction_accuracy": 67.2,
  "recent_predictions": [...]
}
```

### GET `/api/analytics/charts-data`
Returns Chart.js-formatted datasets for the Analytics tab.  
**Auth:** Required  
**Response:** `gender_distribution`, `risk_distribution`, `age_distribution`, `monthly_predictions`

---

## Settings

### POST `/api/auth/register-doctor`
Create a new doctor account. **Admin only.**

**Body:**
```json
{
  "email": "newdoctor@heartcare.ai",
  "password": "securepass",
  "name": "Dr. Jane Smith"
}
```
