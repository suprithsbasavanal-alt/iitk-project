# Capstone Project Demonstration & Presentation Guide (Part 9)

**Project Title**: Heart Disease Prediction Using Machine Learning and Deep Learning Techniques  
**Team Members**: Shreyas, Uday, Suprith, Sahitya  

---

## Demonstration Workflow (Step-by-Step)

Follow this 12-step sequence during your capstone project live demonstration to external examiners and evaluators:

### Step 1: Open Project Repository & Structure
- Open the project workspace in VS Code or Terminal (`cd heart-disease-prediction`).
- Point out the clean modular project layout (`data/`, `src/`, `scripts/`, `models/`, `results/`, `reports/`, `tests/`, `app.py`).

### Step 2: Show Raw Dataset & Binary Target Transformation
- Display `data/raw/heart_disease_uci.csv` (303 rows, 14 columns).
- Explain the binary target conversion: `num = 0` (No Heart Disease: 164) vs `num > 0` (Heart Disease Present: 139).
- Highlight the 80/20 stratified split (242 training rows, 61 held-out test rows).

### Step 3: Demonstrate Exploratory Data Analysis (EDA)
- Open `results/figures/01_target_distribution.png` and `results/figures/09_correlation_matrix.png`.
- Highlight key correlations: `thalach` ($r = -0.42$), `oldpeak` ($r = +0.42$), `age` ($r = +0.23$).
- Show `results/eda_report.txt` and state that all 21 figures were generated automatically.

### Step 4: Show Baseline Model Benchmarking
- Open `results/metrics/baseline_test_results.csv` and `results/figures/models/baseline_model_comparison.png`.
- Show the 7 baseline classifiers evaluated (Logistic Regression, KNN, Decision Tree, Random Forest, SVM, Naive Bayes, XGBoost).

### Step 5: Demonstrate Hyperparameter Tuning Results
- Open `results/metrics/tuning/best_parameters.json` and `results/hyperparameter_tuning_report.txt`.
- Explain 5-Fold Stratified Cross-Validation on training folds to optimize ROC-AUC while protecting the held-out test set.

### Step 6: Present Final Model Selection & Freezing
- Open `models/final/final_model_metadata.json` and `results/final_model_report.txt`.
- Show the winning model: **Tuned Random Forest** (`models/final/final_model.joblib`).
- Explain selection criteria: Test Accuracy (90.16%), Test Recall (96.43%), Test F1 (90.00%), Test ROC-AUC (0.9567), and False Negatives (FN=1 out of 28 positive cases).

### Step 7: Launch Streamlit Web Application
- Open terminal and run:
  ```bash
  streamlit run app.py
  ```
- Access local URL in browser (`http://localhost:8501`).

### Step 8: Load Example Patient Record
- Select an example patient record from the dropdown menu ("Select an Example Patient Record from Held-Out Test Set").
- Point out how all 13 clinical form fields populate automatically with dataset values.

### Step 9: Execute Live Risk Prediction
- Click **"Predict Heart Disease Risk"**.
- Point out the prediction output container: `Model Prediction: No Heart Disease` or `Model Prediction: Heart Disease Present`.

### Step 10: Explain Predicted Probability Display
- Highlight the dual metric cards: `Heart Disease Probability (%)` and `No Disease Probability (%)`.
- Confirm that $P(\text{disease}) + P(\text{no disease}) = 100\%$.

### Step 11: Expand Feature Importance & Model Information
- Expand the **"Model Feature Importance Rankings"** section to display top clinical risk drivers (`thalach`, `oldpeak`, `cp_4.0`, etc.).
- Expand the **"About the Frozen Model"** section to review frozen hyperparameters and test metrics.

### Step 12: Emphasize Educational & Ethics Disclaimer
- Point out the yellow warning banner:
  > *"This application is an educational/research demonstration created for a college capstone project. It is not a clinically validated medical diagnostic system and should not be used for medical decision-making."*
