# HeartCare AI — Setup Guide

> **Project:** Applied Artificial Intelligence and Data Science Internship  
> **Institution:** IIIT Kottayam  
> **Stack:** React · FastAPI · SQLite · Scikit-learn

---

## Prerequisites

| Requirement | Version |
| :--- | :--- |
| Python | 3.10+ |
| Node.js | 18+ |
| pip | Latest |

---

## 1. Clone the Repository

```bash
git clone https://github.com/suprithsbasavanal-alt/iitk-project.git
cd iitk-project
```

---

## 2. Backend Setup

### 2a. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate.bat     # Windows
```

### 2b. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2c. Train the AI Model (One-time)
```bash
python ml/train_model.py
```
This downloads the UCI Cleveland Heart Disease dataset, trains a Random Forest classifier, and saves `ml/heart_model.pkl` and `ml/scaler.pkl`.

### 2d. Start the Backend Server
```bash
python -m uvicorn backend.main:app --port 8000 --reload
```
Backend runs at → **http://localhost:8000**  
Interactive API docs → **http://localhost:8000/docs**

---

## 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
Frontend runs at → **http://localhost:5173**

---

## 4. Default Login Credentials

| Role | Email / ID | Password |
| :--- | :--- | :--- |
| Admin | `admin@heartcare.ai` | `admin123` |
| Doctor | `doctor@heartcare.ai` | `doctor123` |

---

## 5. Application Workflow

```
Login (Admin / Doctor / Patient)
     │
     ▼
Dashboard  ─── View stats: patients, predictions, risk distribution
     │
     ├── Patients → Register Profile / Search / Filter by Gender
     │
     ├── Prediction → Select Patient → Enter 13 Clinical Features → Run AI
     │              → View: Risk Level · Risk % · Confidence · Recommendations
     │
     ├── History → View all past prediction records
     │
     ├── Reports → Download PDF clinical report per prediction
     │
     ├── Analytics → Chart.js charts: Risk Distribution, Age Group,
     │               Gender Split, Monthly Trends
     │
     └── Settings (Admin) → Create new Doctor accounts
```

---

## 6. Database Schema

**File:** `database/heartcare.db` (SQLite)

| Table | Description |
| :--- | :--- |
| `doctors` | Registered doctors and admin users |
| `patients` | Patient demographic profiles |
| `predictions` | AI prediction results with clinical inputs stored as JSON |

---

## 7. AI Model Details

| Property | Value |
| :--- | :--- |
| Dataset | UCI Cleveland Heart Disease (303 patients) |
| Features | 13 clinical parameters |
| Algorithm | Random Forest Classifier |
| Trees | 150 (balanced class weights) |
| Max Depth | 6 |
| Test Accuracy | **67.21%** (20% holdout, stratified) |
| Output Classes | `LOW RISK` · `MEDIUM RISK` · `HIGH RISK` |
