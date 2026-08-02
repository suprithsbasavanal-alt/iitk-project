# Heart Disease Prediction Using Machine Learning and Deep Learning Techniques

## 1. Project Overview
This repository contains a college capstone project focused on predicting heart disease using clinical and diagnostic data. The goal of the project is to build an end-to-end analytical pipeline that compares traditional Machine Learning (ML) classifiers and advanced Deep Learning (DL) architectures for early detection and risk assessment of cardiovascular diseases.

## 2. Problem Statement
The objective is to develop and compare machine-learning and later deep-learning techniques for predicting the presence of heart disease using patient clinical attributes. Early and accurate detection of heart disease can assist healthcare professionals in preventative decision-making and patient care management.

## 3. Objectives
- Establish a modular and reproducible Python machine learning codebase.
- Perform thorough Exploratory Data Analysis (EDA) on patient clinical features.
- Implement data preprocessing, cleaning, scaling, and categorical encoding workflows.
- Train, evaluate, and benchmark multiple machine learning classification models.
- Apply cross-validation and hyperparameter tuning techniques for model optimization.
- Extend the framework to include Deep Learning models in a subsequent phase.

## 4. Current Scope
The current phase encompasses **Part 1 (Setup)**, **Part 2 (Dataset Integration)**, **Part 3 (Preprocessing Pipeline)**, **Part 4 (Exploratory Data Analysis)**, and **Part 5 (Baseline Machine Learning Model Training, Cross-Validation, Evaluation and Comparison)**.
- The official UCI Heart Disease dataset (ID 45) is preserved as an immutable raw CSV (`data/raw/heart_disease_uci.csv`).
- Target binary mapping (0 -> 0, 1-4 -> 1) and 80/20 stratified split (242 train / 61 test) have been established.
- 7 baseline classification algorithms have been benchmarked using 5-Fold Stratified Cross-Validation on the training set.
- Complete end-to-end scikit-learn pipelines (`preprocessor` + `classifier`) have been fitted and persisted under `models/baseline/*.joblib`.
- Evaluated on the untouched 61-row test set; confusion matrices, ROC curves, and performance comparison charts have been generated.

## 5. Planned Machine Learning Models
For the Machine Learning phase, we investigate and compare the following classification algorithms:
- Logistic Regression
- K-Nearest Neighbors (KNN)
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- Gaussian Naive Bayes
- XGBoost

## 6. Planned Evaluation Metrics
To comprehensively assess model performance, the following evaluation metrics are used:
- Accuracy
- Precision
- Recall (Sensitivity)
- Specificity ($TN / [TN + FP]$)
- F1-Score
- ROC-AUC (Receiver Operating Characteristic - Area Under Curve)
- Confusion Matrix (TN, FP, FN, TP)

## 7. Data Preprocessing & Leakage Prevention (Part 3)
- **Binary Target**: `target` (`0` = 164 No Heart Disease, `1` = 139 Heart Disease Present).
- **Continuous Features (5)**: `age`, `trestbps`, `chol`, `thalach`, `oldpeak` ➔ `SimpleImputer(strategy="median")` ➔ `StandardScaler()`
- **Categorical Features (8)**: `sex`, `cp`, `fbs`, `restecg`, `exang`, `slope`, `ca`, `thal` ➔ `SimpleImputer(strategy="most_frequent")` ➔ `OneHotEncoder(handle_unknown="ignore")`
- **Leakage Prevention**: Imputer, scaler, and one-hot encoder parameters were **fitted strictly on training folds** within complete scikit-learn pipelines.

## 8. Exploratory Data Analysis & Visualization (Part 4)
- **21 Report-Quality Figures**: Generated at 300 DPI in `results/figures/` (`01_target_distribution.png` to `21_missing_values.png`).
- **6 Analytical Summary CSVs**: Saved in `results/` covering numerical statistics, grouped means by target, categorical disease prevalence, IQR outlier exploration, and Pearson correlation matrices.

## 9. Baseline Machine Learning Models (Part 5)

### Modeling Architecture
Each baseline model is constructed as an end-to-end scikit-learn `Pipeline`:
```text
Raw Patient Features ➔ ColumnTransformer Preprocessor ➔ Classifier
```
This guarantees zero data leakage during cross-validation.

### Cross-Validation & Test Benchmarking
- **Cross-Validation**: 5-Fold Stratified Cross-Validation (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`) executed strictly on the 242-row training set (`X_train_raw.csv`).
- **Test Evaluation**: Final models were fitted on all 242 training rows and evaluated on the untouched 61-row test set (`X_test_raw.csv`).
- **Persisted Pipeline Artifacts**: Saved complete fitted pipelines in `models/baseline/` (`logistic_regression.joblib`, `knn.joblib`, `decision_tree.joblib`, `random_forest.joblib`, `svm.joblib`, `gaussian_naive_bayes.joblib`, `xgboost.joblib`).
- **Generated Metrics & Figures**:
  - `results/metrics/baseline_cv_results.csv` (Mean ± Std metrics across CV folds)
  - `results/metrics/baseline_test_results.csv` (Test Accuracy, Precision, Recall, Specificity, F1, ROC-AUC, TN, FP, FN, TP)
  - `results/metrics/cv_vs_test_comparison.csv` (CV vs Test comparison)
  - `results/figures/models/baseline_roc_curves.png` (Combined ROC curves for all 7 models)
  - `results/figures/models/baseline_model_comparison.png` (Bar chart model comparison)

*For detailed numerical performance tables, inspect [baseline_test_results.csv](file:///Users/suprith.s.basavanal/Documents/antigrativity%20/iitk-project/heart-disease-prediction/results/metrics/baseline_test_results.csv) and [baseline_model_report.txt](file:///Users/suprith.s.basavanal/Documents/antigrativity%20/iitk-project/heart-disease-prediction/results/baseline_model_report.txt).*

## 10. Project Structure
```text
heart-disease-prediction/
│
├── data/
│   ├── raw/                        # Immutable raw dataset (heart_disease_uci.csv)
│   └── processed/                  # Split CSV datasets (X_train_raw, X_test_raw, y_train, y_test)
│
├── notebooks/
│   ├── 01_eda.ipynb                # Executed EDA notebook with 14 sections & plots
│   └── 02_baseline_models.ipynb    # Executed Baseline Models notebook with CV & test results
│
├── src/
│   ├── __init__.py                 # Package initializer
│   ├── download_data.py            # Automated dataset acquisition script from UCI
│   ├── data_loader.py              # Data loading & validation utilities
│   ├── preprocessing.py            # Target conversion, split & ColumnTransformer pipeline
│   ├── eda.py                      # Reusable EDA engine & 21-figure Matplotlib generator
│   ├── train.py                    # Central baseline model registry & 5-fold CV engine
│   ├── evaluate.py                 # Performance metrics, classification reports & ROC plots
│   └── predict.py                  # Inference routines for trained models
│
├── scripts/
│   ├── verify_dataset.py           # Dataset verification script
│   ├── verify_preprocessing.py     # 14-point preprocessing & leakage verification script
│   ├── generate_eda.py             # Script reproducing all 21 EDA figures & 6 summary reports
│   ├── verify_eda.py               # 14-point EDA verification script
│   ├── train_baseline_models.py    # Master execution script training 7 baseline pipelines
│   └── verify_baseline_models.py   # 25-point baseline model verification suite
│
├── models/
│   ├── .gitkeep
│   ├── preprocessor.joblib         # Fitted preprocessor transformer
│   └── baseline/                   # 7 Persisted complete baseline pipeline joblib files
│
├── results/
│   ├── dataset_metadata.txt
│   ├── dataset_dictionary.csv
│   ├── data_quality_report.txt
│   ├── preprocessing_report.txt
│   ├── processed_feature_names.txt
│   ├── eda_*.csv                   # Summary CSV files from EDA phase
│   ├── eda_report.txt
│   ├── baseline_model_report.txt   # Comprehensive baseline experiment report
│   ├── figures/
│   │   ├── 01_*.png to 21_*.png    # 21 EDA figures
│   │   └── models/                 # 7 Confusion matrices, combined ROC, comparison plot
│   └── metrics/
│       ├── baseline_cv_results.csv # 5-Fold CV mean ± std metrics
│       ├── baseline_cv_fold_results.csv # 35 fold-level CV results
│       ├── baseline_test_results.csv    # Test set performance metrics
│       ├── cv_vs_test_comparison.csv    # CV vs Test comparison table
│       ├── baseline_test_predictions.csv# Row-level test predictions and probabilities
│       └── classification_reports/      # 7 Text classification reports
│
├── tests/
│   ├── test_preprocessing.py       # Unit test suite for Part 3
│   ├── test_train.py               # Unit test suite for Part 5 train module
│   └── test_evaluate.py            # Unit test suite for Part 5 evaluate module
│
├── main.py                         # Application entry point script
├── requirements.txt                # Project dependencies
├── .gitignore                      # Git ignore configuration
└── README.md                       # Project documentation
```

## 11. Installation

### Prerequisites
- Python 3.8+ installed on your system.

### Setup Instructions

1. Clone or navigate into the project directory:
   ```bash
   cd heart-disease-prediction
   ```

2. Create a virtual environment:
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     ```
   - **Windows:**
     ```cmd
     python -m venv .venv
     ```

3. Activate the virtual environment:
   - **macOS / Linux (bash/zsh):**
     ```bash
     source .venv/bin/activate
     ```
   - **Windows (Command Prompt):**
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **Windows (PowerShell):**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```

4. Upgrade `pip` and install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## 12. Running the Project

### Reproduce Baseline Training & Run Verifications

1. Train 7 baseline models, run 5-fold CV, evaluate test set, and generate figures/reports:
   ```bash
   python scripts/train_baseline_models.py
   ```

2. Run 25-point baseline model verification suite:
   ```bash
   python scripts/verify_baseline_models.py
   ```

3. Regenerate all 21 EDA figures and summary reports:
   ```bash
   python scripts/generate_eda.py
   ```

4. Run 14-point EDA verification suite:
   ```bash
   python scripts/verify_eda.py
   ```

5. Execute leakage-safe preprocessing pipeline:
   ```bash
   python src/preprocessing.py
   ```

6. Run 14-point preprocessing verification suite:
   ```bash
   python scripts/verify_preprocessing.py
   ```

7. Run unit test suite:
   ```bash
   python -m unittest discover tests
   ```

8. Run main project entry point:
   ```bash
   python main.py
   ```

## 13. Dataset
This project uses the official **Heart Disease Dataset** from the **UCI Machine Learning Repository** (Dataset ID: 45).
- **Official URL**: [https://archive.ics.uci.edu/dataset/45/heart+disease](https://archive.ics.uci.edu/dataset/45/heart+disease)
- **Instances**: 303 patient records
- **Features**: 13 clinical attributes
- **Target**: `num` (0 to 4) converted to binary classification target `target` (`0` = 164, `1` = 139).

## 14. Future Deep Learning Module
After the machine learning module is fully built, benchmarked, and tuned, the project will expand to include a **Deep Learning Module**.

## 15. Disclaimer
This project is conducted strictly for educational and academic research purposes as part of a college capstone project. The predictions generated by models built within this repository are not medical diagnoses.
