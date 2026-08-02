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
The current phase encompasses **Part 1 (Setup)**, **Part 2 (Dataset Integration)**, and **Part 3 (Data Cleaning, Target Transformation, Train/Test Splitting, and Leakage-Safe Preprocessing Pipeline)**.
- The official UCI Heart Disease dataset (ID 45) is preserved as an immutable raw CSV (`data/raw/heart_disease_uci.csv`).
- Target binary mapping (0 -> 0, 1-4 -> 1) and 80/20 stratified split have been established.
- A scikit-learn `ColumnTransformer` preprocessing pipeline has been constructed and fitted **exclusively on the training split** to guarantee zero data leakage.
- Fitted preprocessor is persisted at `models/preprocessor.joblib`.
- **No machine learning prediction model has been trained yet.**

## 5. Planned Machine Learning Models
For the Machine Learning phase, we plan to investigate and compare the following classification algorithms:
- Logistic Regression
- K-Nearest Neighbors (KNN)
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- Naive Bayes
- XGBoost

## 6. Planned Evaluation Metrics
To comprehensively assess model performance, the following evaluation metrics will be used:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC (Receiver Operating Characteristic - Area Under Curve)
- Confusion Matrix

*Note: Cross-validation strategies (e.g., Stratified K-Fold) and systematic hyperparameter tuning (e.g., Grid Search / Random Search) will be incorporated during model development. No performance accuracy metrics are reported yet as models have not been trained.*

## 7. Data Preprocessing & Leakage Prevention (Part 3)

### Binary Target Transformation
- **Raw Target (`num`)**: Multiclass integer values 0, 1, 2, 3, 4.
- **Binary Target (`target`)**:
  - `0` (Absence of Heart Disease): 164 instances (54.13%)
  - `1` (Presence of Heart Disease): 139 instances (45.87%)

### Feature Grouping
- **Continuous Numerical Features (5)**: `age`, `trestbps`, `chol`, `thalach`, `oldpeak`
- **Categorical / Discrete Features (8)**: `sex`, `cp`, `fbs`, `restecg`, `exang`, `slope`, `ca`, `thal`
  * *Note on `ca`*: `ca` represents major vessels colored by fluoroscopy (0–3). Treated as discrete categorical.

### Preprocessing Pipelines
1. **Numerical Pipeline**:
   `SimpleImputer(strategy="median")` ➔ `StandardScaler()`
2. **Categorical Pipeline**:
   `SimpleImputer(strategy="most_frequent")` ➔ `OneHotEncoder(handle_unknown="ignore")`
3. **Combined ColumnTransformer**:
   Maps feature groups to respective pipelines, expanding 13 raw predictors to 28 transformed numeric features.

### Train / Test Split Parameters
- **Split Ratio**: 80% Training (242 instances) / 20% Testing (61 instances)
- **Random Seed**: `random_state=42`
- **Stratification**: `stratify=y` (preserves binary class balance across splits)

### Data Leakage Prevention Guarantee
- Imputer statistics (median, mode), scaler parameters ($\mu, \sigma$), and one-hot encoder categories were **fitted strictly on `X_train`**.
- The test set (`X_test`) was transformed using only parameters learned from `X_train`.

## 8. Project Structure
```text
heart-disease-prediction/
│
├── data/
│   ├── raw/                        # Immutable raw dataset (heart_disease_uci.csv)
│   └── processed/                  # Split CSV datasets (X_train_raw, X_test_raw, y_train, y_test, preprocessed)
│
├── notebooks/
│   └── 01_eda.ipynb                # Exploratory Data Analysis notebook
│
├── src/
│   ├── __init__.py                 # Package initializer
│   ├── download_data.py            # Automated dataset acquisition script from UCI
│   ├── data_loader.py              # Data loading & validation utilities
│   ├── preprocessing.py            # Target conversion, split & ColumnTransformer pipeline
│   ├── train.py                    # Model training & persistence logic skeleton
│   ├── evaluate.py                 # Performance evaluation & metric reporting skeleton
│   └── predict.py                  # Inference routines for trained models
│
├── scripts/
│   ├── verify_dataset.py           # Dataset verification script
│   └── verify_preprocessing.py     # 14-point preprocessing & leakage verification script
│
├── models/
│   ├── .gitkeep
│   └── preprocessor.joblib         # Fitted scikit-learn preprocessing transformer
│
├── results/
│   ├── dataset_metadata.txt        # UCI dataset metadata documentation
│   ├── dataset_dictionary.csv      # Detailed feature data dictionary
│   ├── data_quality_report.txt     # Data quality inspection report
│   ├── preprocessing_report.txt    # Detailed preprocessing & leakage audit report
│   ├── processed_feature_names.txt # List of 28 transformed feature names
│   ├── figures/                    # Visualization artifacts directory
│   └── metrics/                    # Evaluation metrics reports directory
│
├── tests/
│   └── test_preprocessing.py       # Unit test suite for target & preprocessing routines
│
├── main.py                         # Application entry point script
├── requirements.txt                # Project dependencies
├── .gitignore                      # Git ignore configuration
└── README.md                       # Project documentation
```

## 9. Installation

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

## 10. Running the Project

### Preprocessing & Verification Commands

1. Execute the leakage-safe preprocessing pipeline:
   ```bash
   python src/preprocessing.py
   ```

2. Run the 14-point preprocessing verification suite:
   ```bash
   python scripts/verify_preprocessing.py
   ```

3. Run unit test suite:
   ```bash
   python -m unittest discover tests
   ```

4. Run main project entry point:
   ```bash
   python main.py
   ```

## 11. Dataset
This project uses the official **Heart Disease Dataset** from the **UCI Machine Learning Repository** (Dataset ID: 45).
- **Official URL**: [https://archive.ics.uci.edu/dataset/45/heart+disease](https://archive.ics.uci.edu/dataset/45/heart+disease)
- **Instances**: 303 patient records
- **Features**: 13 clinical attributes
- **Target**: `num` (0 to 4) converted to binary classification target `target` (`0` = 164, `1` = 139).

## 12. Future Deep Learning Module
After the machine learning module is fully built, benchmarked, and tuned, the project will expand to include a **Deep Learning Module**.

## 13. Disclaimer
This project is conducted strictly for educational and academic research purposes as part of a college capstone project. The predictions generated by models built within this repository are not medical diagnoses.
