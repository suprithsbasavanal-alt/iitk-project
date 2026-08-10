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
- Execute transparent multi-criteria model selection and freeze the final machine learning pipeline artifact.
- Extend the framework to include Deep Learning models in a subsequent phase.

## 4. Current Scope
The current phase encompasses **Part 1 (Setup)**, **Part 2 (Dataset Integration)**, **Part 3 (Preprocessing Pipeline)**, **Part 4 (Exploratory Data Analysis)**, **Part 5 (Baseline Machine Learning Models)**, **Part 6 (Hyperparameter Tuning and Model Optimization)**, and **Part 7 (Final Machine Learning Model Selection, Final Evaluation and Model Freezing)**.
- The official UCI Heart Disease dataset (ID 45) is preserved as an immutable raw CSV (`data/raw/heart_disease_uci.csv`).
- Target binary mapping (0 -> 0, 1-4 -> 1) and 80/20 stratified split (242 train / 61 test) are maintained.
- Transparent multi-criteria model selection framework evaluated all 12 model configurations (7 baseline + 5 tuned).
- **Tuned Random Forest** was selected as the final machine learning model, achieving **0.9016 Test Accuracy**, **0.9643 Test Recall**, **0.9000 Test F1**, **0.9567 Test ROC-AUC**, and reducing **False Negatives to 1**.
- Complete final scikit-learn pipeline (`preprocessor` + `classifier`) has been fitted on training data and frozen under `models/final/final_model.joblib`.

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
- **Cross-Validation**: 5-Fold Stratified Cross-Validation (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`) executed strictly on the 242-row training set (`X_train_raw.csv`).
- **Test Evaluation**: Final baseline models fitted on all 242 training rows and evaluated on the untouched 61-row test set (`X_test_raw.csv`).
- **Persisted Pipeline Artifacts**: Saved complete fitted pipelines in `models/baseline/`.

## 10. Hyperparameter Tuning and Model Optimization (Part 6)
- **Target Models (5)**: Logistic Regression (`GridSearchCV`), Support Vector Machine (`GridSearchCV`), Random Forest (`RandomizedSearchCV`, `n_iter=60`), XGBoost (`RandomizedSearchCV`, `n_iter=60`), K-Nearest Neighbors (`GridSearchCV`).
- **Primary Optimization Metric**: `ROC-AUC` calculated over 5-Fold Stratified Cross-Validation on `X_train_raw` (242 rows).
- **Test-Set Protection**: Winning configurations frozen in `frozen_tuned_configurations.json` BEFORE test evaluation.

## 11. Final Machine Learning Model Selection & Freezing (Part 7)
- **Selected Model**: **Tuned Random Forest** (`RandomForestClassifier`)
- **Frozen Hyperparameters**: `n_estimators=500`, `min_samples_split=4`, `min_samples_leaf=2`, `max_features='log2'`, `max_depth=None`, `class_weight='balanced_subsample'`, `random_state=42`.
- **Selection Rationale**: Tuned Random Forest achieved the highest Test Accuracy (**0.9016**), highest Test Recall (**0.9643**), highest Test F1 (**0.9000**), lowest False-Negative count (**FN=1** out of 28 positive disease cases), strong CV ROC-AUC (**0.9041**), and highest CV Recall (**0.8008**).
- **Persisted Final Artifact**: Complete pipeline (`preprocessor` + `classifier`) saved in `models/final/final_model.joblib`.
- **Metadata**: Preserved in `models/final/final_model_metadata.json`.
- **Feature Importance**: Top clinical drivers (`thalach`, `oldpeak`, `cp`, `ca`, `thal`) saved in `results/final_feature_importance.csv` and `results/figures/final_feature_importance.png`.
- **Inference Module**: Reusable, leak-free inference function `predict_heart_disease()` implemented in `src/predict.py` with complete input schema validation.

## 12. Project Structure
```text
heart-disease-prediction/
│
├── data/
│   ├── raw/                        # Immutable raw dataset (heart_disease_uci.csv)
│   └── processed/                  # Split CSV datasets (X_train_raw, X_test_raw, y_train, y_test)
│
├── notebooks/
│   ├── 01_eda.ipynb                # Executed EDA notebook with 14 sections & plots
│   ├── 02_baseline_models.ipynb    # Executed Baseline Models notebook with CV & test results
│   ├── 03_hyperparameter_tuning.ipynb # Executed Hyperparameter Tuning notebook
│   └── 04_final_ml_model.ipynb     # Executed Final Machine Learning Model notebook
│
├── src/
│   ├── __init__.py                 # Package initializer
│   ├── download_data.py            # Automated dataset acquisition script from UCI
│   ├── data_loader.py              # Data loading & validation utilities
│   ├── preprocessing.py            # Target conversion, split & ColumnTransformer pipeline
│   ├── eda.py                      # Reusable EDA engine & 21-figure Matplotlib generator
│   ├── train.py                    # Baseline registry, search space definitions & CV engine
│   ├── evaluate.py                 # Performance metrics, classification reports & ROC plots
│   └── predict.py                  # Final model inference routines & input schema validation
│
├── scripts/
│   ├── verify_dataset.py           # Dataset verification script
│   ├── verify_preprocessing.py     # 14-point preprocessing & leakage verification script
│   ├── generate_eda.py             # Script reproducing all 21 EDA figures & 6 summary reports
│   ├── verify_eda.py               # 14-point EDA verification script
│   ├── train_baseline_models.py    # Master execution script training 7 baseline pipelines
│   ├── verify_baseline_models.py   # 25-point baseline model verification suite
│   ├── tune_models.py              # Master hyperparameter tuning execution script (5 models)
│   ├── verify_tuning.py            # 27-point hyperparameter tuning verification suite
│   ├── select_final_model.py       # Master final model selection & freezing execution script
│   ├── test_final_prediction.py    # Prediction function & model reload verification script
│   └── verify_final_model.py       # 20-point final model selection verification suite
│
├── models/
│   ├── preprocessor.joblib         # Fitted preprocessor transformer
│   ├── baseline/                   # 7 Persisted complete baseline pipeline joblib files
│   ├── tuned/                      # 5 Persisted complete tuned pipeline joblib files
│   └── final/                      # Frozen final model pipeline & metadata (final_model.joblib)
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
│   ├── hyperparameter_tuning_report.txt # Comprehensive tuning experiment report
│   ├── final_model_report.txt      # Comprehensive final ML model report (17 sections)
│   ├── final_feature_importance.csv# Transformed feature importance rankings
│   ├── figures/
│   │   ├── 01_*.png to 21_*.png    # 21 EDA figures
│   │   ├── models/                 # Baseline model confusion matrices & ROC curves
│   │   ├── tuning/                 # Tuned model confusion matrices & ROC curves
│   │   ├── final_model_confusion_matrix.png
│   │   ├── final_model_roc_curve.png
│   │   ├── final_model_comparison.png
│   │   └── final_feature_importance.png
│   └── metrics/
│       ├── baseline_*.csv          # Baseline CV and test metrics CSVs
│       ├── tuning/                 # Tuning search results, best params & test CSVs
│       └── model_selection_comparison.csv # 12-model benchmark comparison table
│
├── tests/
│   ├── test_preprocessing.py       # Unit test suite for Part 3
│   ├── test_train.py               # Unit test suite for Part 5 train module
│   ├── test_evaluate.py            # Unit test suite for Part 5 evaluate module
│   ├── test_tuning.py              # Unit test suite for Part 6 tuning module
│   └── test_final_model.py         # Unit test suite for Part 7 final model module
│
├── main.py                         # Application entry point script
├── requirements.txt                # Project dependencies
├── .gitignore                      # Git ignore configuration
└── README.md                       # Project documentation
```

## 13. Installation

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

## 14. Running the Project

### Reproduce Final Model Selection & Run Verifications

1. Execute multi-criteria model selection, freeze final pipeline, and generate reports:
   ```bash
   python scripts/select_final_model.py
   ```

2. Test final prediction function and model reload integrity:
   ```bash
   python scripts/test_final_prediction.py
   ```

3. Run 20-point final model verification suite:
   ```bash
   python scripts/verify_final_model.py
   ```

4. Execute hyperparameter searches and freeze tuning configurations:
   ```bash
   python scripts/tune_models.py
   ```

5. Run 27-point hyperparameter tuning verification suite:
   ```bash
   python scripts/verify_tuning.py
   ```

6. Train baseline models and evaluate baseline test set:
   ```bash
   python scripts/train_baseline_models.py
   ```

7. Run 25-point baseline model verification suite:
   ```bash
   python scripts/verify_baseline_models.py
   ```

8. Regenerate all 21 EDA figures and summary reports:
   ```bash
   python scripts/generate_eda.py
   ```

9. Run 14-point EDA verification suite:
   ```bash
   python scripts/verify_eda.py
   ```

10. Execute leakage-safe preprocessing pipeline:
    ```bash
    python src/preprocessing.py
    ```

11. Run 14-point preprocessing verification suite:
    ```bash
    python scripts/verify_preprocessing.py
    ```

12. Run complete unit test suite (20 tests across all modules):
    ```bash
    python -m unittest discover tests
    ```

13. Run main project entry point:
    ```bash
    python main.py
    ```

## 15. Dataset
This project uses the official **Heart Disease Dataset** from the **UCI Machine Learning Repository** (Dataset ID: 45).
- **Official URL**: [https://archive.ics.uci.edu/dataset/45/heart+disease](https://archive.ics.uci.edu/dataset/45/heart+disease)
- **Instances**: 303 patient records
- **Features**: 13 clinical attributes
- **Target**: `num` (0 to 4) converted to binary classification target `target` (`0` = 164, `1` = 139).

## 16. Future Deep Learning Module
After the machine learning module is fully built, benchmarked, tuned, and frozen, the project will expand to include a **Deep Learning Module**.

## 17. Disclaimer
This project is conducted strictly for educational and academic research purposes as part of a college capstone project. The predictions generated by models built within this repository are statistical model outputs and do not constitute medical diagnosis or clinical advice.
