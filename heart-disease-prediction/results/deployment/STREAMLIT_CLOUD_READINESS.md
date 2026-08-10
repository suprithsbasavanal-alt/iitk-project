# STREAMLIT COMMUNITY CLOUD DEPLOYMENT READINESS REPORT

**Project Title**: Heart Disease Prediction Using Machine Learning and Deep Learning Techniques  
**Repository**: `suprithsbasavanal-alt/iitk-project`  
**Branch**: `main`  
**Streamlit Entrypoint**: `heart-disease-prediction/app.py`  

---

## 1. VERCEL 404 / NOT_FOUND ROOT CAUSE ANALYSIS

- **Root Cause**: The Vercel platform is built exclusively for stateless Serverless Functions (Next.js, Node.js, static HTML, or Python Flask/FastAPI serverless routes inside an `api/` directory). Vercel does **not** support persistent, stateful Python web application processes or WebSockets required by Streamlit (`streamlit run app.py`).
- **Effect**: When Vercel attempted to build the repository, it found zero static build outputs or serverless HTTP route handlers, resulting in a Vercel 404 / `NOT_FOUND` deployment error.
- **Resolution**: Streamlit applications must be deployed on a platform designed for long-running stateful Python web servers and WebSockets — specifically **Streamlit Community Cloud** ([share.streamlit.io](https://share.streamlit.io)).

---

## 2. REPOSITORY & ENTRYPOINT VERIFICATION

- **Application Script**: `heart-disease-prediction/app.py`
- **Execution Command**: `streamlit run app.py` (executed from the `heart-disease-prediction/` directory).
- **Portability Check**: All resource paths in `app.py` use relative, portable resolution:
  ```python
  PROJECT_ROOT = Path(__file__).resolve().parent
  model_path = PROJECT_ROOT / "models" / "final" / "final_model.joblib"
  dl_model_path = PROJECT_ROOT / "models" / "deep_learning" / "final_ann.keras"
  prep_path = PROJECT_ROOT / "models" / "preprocessor.joblib"
  ```
- **Absolute Path Search**: `0` hardcoded local paths (`/Users/...`, `C:\...`, `localhost/...`) exist in the application code.

---

## 3. REQUIRED DEPENDENCIES (`requirements.txt`)

All required Python libraries used by `app.py` and its underlying modules (`src/predict.py`, `src/deep_learning.py`, `src/preprocessing.py`) are specified in `requirements.txt`:

```text
pandas
numpy
matplotlib
scikit-learn
joblib
xgboost
ucimlrepo
streamlit
keras
torch
```

---

## 4. FROZEN MODEL ARTIFACT INTEGRITY & GIT TRACKING STATUS

| Model Artifact | Relative Path | File Size | Git Tracking Status | SHA-256 Hash |
| :--- | :--- | :---: | :---: | :--- |
| **Preprocessor Pipeline** | `models/preprocessor.joblib` | 3.8 KB | **TRACKED in Git** | `4df331ff3d3c8502f6ef3ef8734917a149c4faeefb4081c7e974e44b9dce6c64` |
| **Final ML Model (Random Forest)** | `models/final/final_model.joblib` | 2.9 MB | **TRACKED in Git** | `045e0d37e584fbe381ebfcecae6ce8a9dd2b4edfd9d7ad5f09630c7ef1e506d2` |
| **ML Model Metadata** | `models/final/final_model_metadata.json` | 1.3 KB | **TRACKED in Git** | `9dca3e30129759c2509b5ca817b2b64d1f2ef99e07f66a20d4ec4e3d368e7ceb` |
| **Final DL Model (ANN-3)** | `models/deep_learning/final_ann.keras` | 47 KB | **TRACKED in Git** | `bfd1872dfd31a5eb23b7b3b3cb2451f2fe967c13a233bde7cf1e95fa500e5720` |

*(Note: All model artifacts are tracked in the `main` branch of GitHub and are under 3 MB, well within GitHub's 100 MB single-file limit).*

---

## 5. GITIGNORE COMPATIBILITY CHECK

The repository `.gitignore` has been configured to un-ignore deployment artifacts while remaining clean:

```gitignore
!data/raw/heart_disease_uci.csv
!data/processed/*.csv
!models/preprocessor.joblib
!models/final/*
!models/deep_learning/*
!results/metrics/*.csv
```

Unnecessary items (`.venv/`, `__pycache__/`, `.DS_Store`) remain strictly ignored.

---

## 6. LOCAL REGRESSION & TEST SUITE RESULTS

- **Local Streamlit Launch**: `streamlit run app.py` $\rightarrow$ **PASS** (Running cleanly on port 8504).
- **Tuned Random Forest Loading**: **PASS** (Test Accuracy: 90.16%, Recall: 96.43%).
- **Final ANN-3 Loading**: **PASS** (Test Accuracy: 85.25%, Recall: 96.43%).
- **Example Patient #1 Loading**: **PASS** (Populates Record #1 attributes).
- **Example Patient #2 Loading**: **PASS** (Populates Record #2 attributes).
- **Reset Inputs Functionality**: **PASS** (Restores all 13 widget keys to normal default values on a single line `🔄 Reset Inputs`).
- **ML & DL Inference**: **PASS** (Generates correct risk probability scores and diagnostic alert blocks).
- **ML vs DL Comparison Table**: **PASS** (Renders side-by-side metric table and chart).
- **Feature Importance Rankings**: **PASS** (Renders feature importance dataframe).
- **Educational Disclaimer**: **PASS** (Visible at top and footer).
- **Master Project Audit (`scripts/final_project_audit.py`)**: **30 / 30 PASS**.
- **Unit Test Suite (`python -m unittest discover tests`)**: **38 / 38 PASS** (Time: 0.514s).

---

## 7. DEPLOYMENT RISKS & COMPATIBILITY ASSESSMENT

- **Python Version Compatibility**: The local project was built using Python 3.14 alpha, but all libraries in `requirements.txt` (`scikit-learn`, `pandas`, `xgboost`, `streamlit`, `keras`, `torch`) use standard APIs compatible with Python 3.10, 3.11, and 3.12 on Streamlit Community Cloud.
- **PyTorch/Keras Environment Variable**: `app.py` sets `os.environ["KERAS_BACKEND"] = "torch"` prior to importing Keras, ensuring PyTorch backend is selected deterministically on Linux Cloud instances.

---

## 8. EXACT STREAMLIT COMMUNITY CLOUD DEPLOYMENT SETTINGS

1. Log in to [https://share.streamlit.io](https://share.streamlit.io) via GitHub.
2. Click **Create App** $\rightarrow$ **I already have an app**.
3. Fill in deployment options:
   - **Repository**: `suprithsbasavanal-alt/iitk-project`
   - **Branch**: `main`
   - **Main file path**: `heart-disease-prediction/app.py`
4. Click **Deploy!**

---

## VERIFICATION VERDICT
```text
======================================================================
READY FOR STREAMLIT COMMUNITY CLOUD DEPLOYMENT
======================================================================
```
