# HeartCare AI

## Description
HeartCare AI is a machine learning-based web application that predicts the risk of heart disease using patient health parameters. It provides patient management, prediction reports, analytics, and AI-powered decision support for healthcare professionals.

Developed for:
**Applied Artificial Intelligence and Data Science Internship**  
**IIIT Kottayam**

---

## Tech Stack (Step 1 Foundation)
- **Frontend:** React + Tailwind CSS
- **Backend:** FastAPI (Python)
- **Database:** SQLite
- **Authentication:** JWT
- **Machine Learning:** Scikit-learn (planned for Step 2)
- **Charts:** Chart.js
- **PDF Reports:** ReportLab

---

## Development Roadmap
- [x] **Step 1:** UI layout with Top Bar and Left Sidebar, SQLite database design (`Doctors`, `Patients`, `Predictions`), mockup FastAPI backend endpoints, and navigation layout.
- [ ] **Step 2:** AI Model Training, prediction API integration, dynamic analytics charts, and downloadable PDF clinical reports.

---

## Installation & Running

### Prerequisites
- Python 3.12+ (tested on Python 3.14)
- Node.js 20+ & npm

### 1. Backend Setup
```bash
# Create virtual environment
python3 -m venv .venv

# Install python requirements
.venv/bin/pip install -r requirements.txt

# Run the FastAPI server
.venv/bin/python -m uvicorn backend.main:app --port 8000 --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## Seed Accounts (Step 1)

| Account Type | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@heartcare.ai` | `admin123` |
| **Doctor** | `doctor@heartcare.ai` | `doctor123` |
| **Patient** | *Registered Patient ID* | *Patient ID* (e.g. `PAT-001`) or `patient123` |
