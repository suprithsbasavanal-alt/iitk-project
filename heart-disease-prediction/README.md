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
The current phase of this project encompasses **Part 1 (Project Setup)** and **Part 2 (Dataset Selection, Acquisition, Inspection and Integration)**.
- The official UCI Heart Disease dataset (ID 45) has been acquired and saved as an immutable raw dataset (`data/raw/heart_disease_uci.csv`).
- Dataset inspection, data quality reporting, metadata documentation, and data loading routines have been established.
- No model training, preprocessing transformations, SMOTE, or feature scaling have been performed yet.

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

## 7. Project Structure
```text
heart-disease-prediction/
│
├── data/
│   ├── raw/                # Immutable raw dataset (heart_disease_uci.csv)
│   └── processed/          # Cleaned and preprocessed datasets placeholder
│
├── notebooks/
│   └── 01_eda.ipynb        # Exploratory Data Analysis notebook
│
├── src/
│   ├── __init__.py         # Package initializer
│   ├── download_data.py    # Automated dataset acquisition script from UCI
│   ├── data_loader.py      # Data loading & validation utilities
│   ├── preprocessing.py    # Data cleaning & feature engineering routines
│   ├── train.py            # Model training & persistence logic
│   ├── evaluate.py         # Performance evaluation & metric reporting
│   └── predict.py          # Inference routines for trained models
│
├── scripts/
│   └── verify_dataset.py   # Dataset verification script
│
├── models/                 # Saved model binaries and artifacts
│
├── results/
│   ├── dataset_metadata.txt    # UCI dataset metadata documentation
│   ├── dataset_dictionary.csv  # Detailed feature data dictionary
│   ├── data_quality_report.txt # Comprehensive data quality inspection report
│   ├── figures/                # Generated plots and visualization artifacts
│   └── metrics/                # Evaluation metrics reports and logs
│
├── tests/                  # Unit and integration test suites
│
├── main.py                 # Application entry point script
├── requirements.txt        # Project dependencies (including ucimlrepo)
├── .gitignore              # Git ignore configuration
└── README.md               # Project documentation
```

## 8. Installation

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

## 9. Running the Project

### Acquisition & Verification Commands

1. Programmatically acquire the raw dataset from UCI:
   ```bash
   python src/download_data.py
   ```

2. Verify raw dataset integrity:
   ```bash
   python scripts/verify_dataset.py
   ```

3. Run main project entry point:
   ```bash
   python main.py
   ```

## 10. Dataset
This project uses the official **Heart Disease Dataset** from the **UCI Machine Learning Repository**:

- **Dataset Name**: UCI Heart Disease Dataset (Cleveland Subset)
- **Dataset ID**: 45
- **Official URL**: [https://archive.ics.uci.edu/dataset/45/heart+disease](https://archive.ics.uci.edu/dataset/45/heart+disease)
- **Instances**: 303 patient records
- **Features**: 13 clinical attributes (age, sex, chest pain type, blood pressure, cholesterol, fasting blood sugar, rest ECG, max heart rate, exercise angina, ST depression, ST slope, fluoroscopy major vessels, thalassemia status)
- **Raw Target (`num`)**: Integer values 0 to 4 (0 = absence of disease; 1, 2, 3, 4 = disease presence & severity levels).

*Target Transformation Note*: The raw dataset preserves the original UCI target column `num`. During the future preprocessing stage, values 1-4 will be converted to a binary classification target (`0` = No Heart Disease, `1` = Heart Disease Present).

## 11. Future Deep Learning Module
After the machine learning module is fully built, benchmarked, and tuned, the project will expand to include a **Deep Learning Module**. This will explore Multi-Layer Perceptrons (MLPs) and Neural Network architectures to compare against traditional ML algorithms.

## 12. Disclaimer
This project is conducted strictly for educational and academic research purposes as part of a college capstone project. The predictions generated by models built within this repository are not medical diagnoses and must not be used for medical decision-making or real-world clinical evaluation.
