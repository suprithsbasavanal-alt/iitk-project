# HeartCare AI – Heart Disease Prediction System

HeartCare AI is a complete, production-ready software system designed to help clinicians assess patient cardiovascular health risk using machine learning. 

This application consists of a **FastAPI backend** utilizing a **Random Forest classifier** trained on the UCI Cleveland Heart Disease dataset, a **ReportLab PDF report generator**, and a responsive **React frontend** styled with **Tailwind CSS** (designed using Stitch MCP).

---

## Features

1. **Role-Based Access Control (RBAC):**
   - **Admin:** Management of doctor credentials, view patients directory, database backup/export, and global telemetry.
   - **Doctor:** Register patient files, enter clinical metric indicators, execute ML diagnostics prediction, view history, and export PDF reports.
   - **Patient (Optional):** Self-sign in using Patient ID as both username and passcode to view personal clinical diagnostics history and download reports.

2. **AI Diagnostics Engine:**
   - Pre-processes the 13 clinical factors (imputing missing values using dataset medians).
   - Random Forest Classifier (Multi-class: Low, Medium, High Risk).
   - Generates confidence score and weighted Risk Percentage ($P(Med) \times 0.5 + P(High) \times 1.0$).
   - Returns risk-specific clinical recommendations.

3. **PDF Clinical Reports:**
   - Generated dynamically with ReportLab in Python.
   - Includes full patient details, clinical metrics table, risk assessment indicators, physician recommendation text, and signature blocks.
   - Automatically archives reports on the server and streams the PDF for client download.

4. **Analytics Telemetry:**
   - Interactive charts built on Chart.js:
     - Male vs Female demographics.
     - Risk level distribution.
     - Patient age-group histogram.
     - Monthly prediction scans timeline.

---

## Folder Structure

```
iitk-project/
├── backend/
│   ├── app/
│   │   ├── auth/          # JWT tokens & bcrypt password hashing
│   │   ├── database/      # SQLite connection & database models
│   │   ├── models/        # Pydantic schemas for request validation
│   │   ├── routes/        # API Routers (auth, patients, predictions, reports, analytics)
│   │   └── services/      # AI engine predictor & ReportLab PDF generator
│   └── main.py            # FastAPI main entrypoint (initializes DB tables & seeds users)
├── ml/
│   ├── dataset/           # Cleveland dataset storage directory
│   ├── train_model.py     # Download, pre-processing, training & evaluation script
│   ├── heart_model.pkl    # Serialized Random Forest model
│   └── scaler.pkl         # Serialized standard scaler
├── reports/               # Hardcopy PDF clinical report archives
├── frontend/              # Vite React SPA + Tailwind CSS
├── requirements.txt       # Python dependencies list
└── README.md              # Document guide
```

---

## Installation & Running

### Prerequisites
- Python 3.12+ (tested on Python 3.14)
- Node.js 20+ & npm

### 1. Backend Setup

First, activate the virtual environment and install the dependencies:
```bash
# Create virtual environment
python3 -m venv .venv

# Install python requirements
.venv/bin/pip install -r requirements.txt

# Run the ML pipeline to download data and train the classifier
.venv/bin/python ml/train_model.py

# Launch the FastAPI dev server (running on port 8000)
.venv/bin/python -m uvicorn backend.main:app --port 8000 --reload
```

> **API Documentation:** Once the server is running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger API documentation.

### 2. Frontend Setup

In a new terminal window, compile and run the React app:
```bash
# Navigate to frontend folder
cd frontend

# Install package dependencies
npm install

# Run the local Vite server (running on port 5173)
npm run dev
```

Visit [http://localhost:5173/](http://localhost:5173/) to launch the HeartCare AI application in your browser.

---

## Default Login Credentials (Seeded on Boot)

| Role | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` |
| **Doctor** | `doctor` | `doctor123` |
| **Patient** | *Registered Patient ID* | *Patient ID* (e.g. `PAT-001`) or `patient123` |
