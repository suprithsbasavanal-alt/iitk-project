# Heart Disease Prediction Using Machine Learning and Deep Learning Techniques

## 1. Project Overview
This repository contains a college capstone project focused on predicting heart disease using clinical and diagnostic data. The goal of the project is to build an end-to-end analytical pipeline that compares traditional Machine Learning (ML) classifiers and advanced Deep Learning (DL) architectures for early detection and risk assessment of cardiovascular diseases.

## 2. Problem Statement
The objective is to develop and compare machine-learning and deep-learning techniques for predicting the presence of heart disease using patient clinical attributes. Early and accurate detection of heart disease can assist healthcare professionals in preventative decision-making and patient care management.

## 3. Objectives
- Establish a modular and reproducible Python machine learning codebase.
- Perform thorough Exploratory Data Analysis (EDA) on patient clinical features.
- Implement data preprocessing, cleaning, scaling, and categorical encoding workflows.
- Train, evaluate, and benchmark multiple machine learning classification models.
- Apply cross-validation and hyperparameter tuning techniques for model optimization.
- Execute transparent multi-criteria model selection and freeze the final machine learning pipeline artifact.
- Develop, evaluate, and benchmark an Artificial Neural Network (ANN) Deep Learning model.
- Deploy an interactive web application (Streamlit) supporting both ML and DL inference engines.

## 4. Current Scope
The project encompasses **Part 1** through **Part 10 (Deep Learning Integration & Benchmarking)**:
- The official UCI Heart Disease dataset (ID 45) is preserved as an immutable raw CSV (`data/raw/heart_disease_uci.csv`).
- Target binary mapping (0 -> 0, 1-4 -> 1) and 80/20 stratified split (242 train / 61 test) are maintained.
- **Tuned Random Forest (ML)** was selected as the primary winning model (**0.9016 Test Accuracy**, **0.9643 Test Recall**, **0.9000 Test F1**, **0.9567 Test ROC-AUC**, **FN=1**).
- **Final ANN (DL)** was trained and evaluated as a secondary benchmark architecture (**0.8525 Test Accuracy**, **0.9643 Test Recall**, **0.8710 Test F1**, **0.9253 Test ROC-AUC**, **FN=1**).
- Complete final scikit-learn pipeline is frozen at `models/final/final_model.joblib`, and final Keras ANN model is frozen at `models/deep_learning/final_ann.keras`.
- An interactive web application built with Streamlit (`app.py`) provides dual-engine ML and DL inference, risk scoring, schema validation, and benchmark comparison.

## 5. Machine Learning Models Evaluated
- Logistic Regression
- K-Nearest Neighbors (KNN)
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- Gaussian Naive Bayes
- XGBoost

## 6. Deep Learning Architecture (Part 10)
- **Framework**: Keras (v3.15+) with PyTorch backend
- **Winning Candidate Architecture**: **ANN-3** (`28 -> 64 (ReLU, Dropout 0.3) -> 32 (ReLU, Dropout 0.2) -> 16 (ReLU, Dropout 0.1) -> 1 (Sigmoid)`)
- **Validation Strategy**: 80/20 internal validation split on 242 training rows (~193 train / ~49 validation). Held-out 61-row test set remained completely locked during architecture selection.
- **Callbacks**: `EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)`, `ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=7)`
- **Frozen Model Artifact**: `models/deep_learning/final_ann.keras`

## 7. Machine Learning vs Deep Learning Test Performance Comparison

| Model Category | Model Name | Test Accuracy | Test Precision | Test Recall | Test Specificity | Test F1 | Test ROC-AUC | False Negatives (FN) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Machine Learning** | **Tuned Random Forest** | **0.9016** | **0.8438** | **0.9643** | **0.8485** | **0.9000** | **0.9567** | **1** |
| **Deep Learning** | **Final ANN (ANN-3)** | 0.8525 | 0.7941 | 0.9643 | 0.7576 | 0.8710 | 0.9253 | 1 |

## 8. Project Structure
```text
heart-disease-prediction/
│
├── app.py                          # Streamlit web application entry point
├── data/
│   ├── raw/                        # Immutable raw dataset (heart_disease_uci.csv)
│   └── processed/                  # Split CSV datasets (X_train_raw, X_test_raw, y_train, y_test)
│
├── notebooks/
│   ├── 01_eda.ipynb                # Executed EDA notebook
│   ├── 02_baseline_models.ipynb    # Executed Baseline Models notebook
│   ├── 03_hyperparameter_tuning.ipynb # Executed Hyperparameter Tuning notebook
│   ├── 04_final_ml_model.ipynb     # Executed Final Machine Learning Model notebook
│   └── 05_deep_learning_ann.ipynb  # Executed Deep Learning ANN notebook
│
├── src/
│   ├── __init__.py                 # Package initializer
│   ├── download_data.py            # Dataset acquisition script
│   ├── data_loader.py              # Data loading & validation utilities
│   ├── preprocessing.py            # Preprocessing & split functions
│   ├── eda.py                      # EDA engine & plot generator
│   ├── train.py                    # Baseline registry & tuning search spaces
│   ├── evaluate.py                 # Evaluation metrics & visualization routines
│   ├── predict.py                  # Final ML inference routines & input schema validation
│   └── deep_learning.py            # Deep Learning ANN construction, training & inference module
│
├── scripts/
│   ├── verify_dataset.py           # Dataset verification script
│   ├── verify_preprocessing.py     # Preprocessing verification script
│   ├── generate_eda.py             # EDA figure generator script
│   ├── verify_eda.py               # EDA verification script
│   ├── train_baseline_models.py    # Master baseline execution script
│   ├── verify_baseline_models.py   # Baseline verification suite
│   ├── tune_models.py              # Master tuning execution script
│   ├── verify_tuning.py            # Tuning verification suite
│   ├── select_final_model.py       # Master final model selection & freezing script
│   ├── test_final_prediction.py    # Prediction function & model reload test script
│   ├── verify_final_model.py       # 20-point final model verification suite
│   ├── test_app.py                 # Streamlit app integration test script
│   ├── verify_application.py       # 15-point master web application verification suite
│   ├── verify_documentation.py    # 17-point master documentation verification suite
│   ├── train_deep_learning.py     # Master Deep Learning execution & comparison script
│   └── verify_deep_learning.py    # 25-point master Deep Learning verification suite
│
├── models/
│   ├── preprocessor.joblib         # Fitted preprocessor transformer
│   ├── baseline/                   # 7 Persisted baseline pipeline joblib files
│   ├── tuned/                      # 5 Persisted tuned pipeline joblib files
│   ├── final/                      # Frozen final ML model pipeline & metadata (final_model.joblib)
│   └── deep_learning/              # Frozen final Deep Learning model (final_ann.keras)
│
├── reports/
│   ├── Heart_Disease_Capstone_Final_Report.docx # Final academic capstone report
│   ├── Heart_Disease_Capstone_Presentation.pptx # Final presentation slides
│   ├── Viva_Questions_and_Answers.md            # Viva examination Q&A
│   ├── Demo_Guide.md                            # Live presentation demonstration guide
│   └── Submission_Checklist.md                  # Comprehensive final submission checklist
│
├── results/
│   ├── eda_*.csv                   # Summary CSV files from EDA phase
│   ├── eda_report.txt
│   ├── baseline_model_report.txt   # Comprehensive baseline experiment report
│   ├── hyperparameter_tuning_report.txt # Comprehensive tuning experiment report
│   ├── final_model_report.txt      # Comprehensive final ML model report
│   ├── application_report.txt      # Comprehensive web application report
│   ├── deep_learning_report.txt    # Comprehensive Deep Learning technical report
│   ├── literature_survey_template.csv # Literature survey template (11 columns)
│   ├── references.md               # Verified project citations & dataset URL
│   ├── final_feature_importance.csv# Transformed feature importances
│   ├── figures/
│   │   ├── 01_*.png to 21_*.png    # 21 EDA figures
│   │   ├── models/                 # Baseline confusion matrices & ROC curves
│   │   ├── tuning/                 # Tuned confusion matrices & ROC curves
│   │   ├── deep_learning/          # Training curves, confusion matrix, ROC, PR & ML vs DL plots
│   │   ├── final_model_confusion_matrix.png
│   │   ├── final_model_roc_curve.png
│   │   ├── final_model_comparison.png
│   │   └── final_feature_importance.png
│   └── metrics/
│       ├── baseline_*.csv          # Baseline CV and test metrics CSVs
│       ├── tuning/                 # Tuning search results & test CSVs
│       ├── deep_learning/          # Architecture comparison, training history & ANN test metrics CSVs
│       ├── ml_vs_dl_comparison.csv # Machine Learning vs Deep Learning comparison table
│       └── model_selection_comparison.csv # 12-model benchmark comparison table
│
├── tests/
│   ├── test_preprocessing.py       # Unit test suite for Part 3
│   ├── test_train.py               # Unit test suite for Part 5 train module
│   ├── test_evaluate.py            # Unit test suite for Part 5 evaluate module
│   ├── test_tuning.py              # Unit test suite for Part 6 tuning module
│   ├── test_final_model.py         # Unit test suite for Part 7 final model module
│   ├── test_application.py         # Unit test suite for Part 8 web application module
│   └── test_deep_learning.py       # Unit test suite for Part 10 Deep Learning module
│
├── main.py                         # Application entry point script
├── requirements.txt                # Project dependencies
├── .gitignore                      # Git ignore configuration
└── README.md                       # Project documentation
```

## 9. Installation & Running the Application

### Setup Instructions

1. Activate virtual environment and install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Execute Deep Learning pipeline (training, architecture selection, model freezing, test evaluation & figures):
   ```bash
   python scripts/train_deep_learning.py
   ```

3. Run master Deep Learning verification suite:
   ```bash
   python scripts/verify_deep_learning.py
   ```

4. Launch Streamlit web application:
   ```bash
   streamlit run app.py
   ```

5. Run complete unit test suite (31 tests across all modules):
   ```bash
   python -m unittest discover tests
   ```

## 10. Disclaimer
This project is conducted strictly for educational and academic research purposes as part of a college capstone project. The predictions generated by models built within this repository are statistical model outputs and do not constitute medical diagnosis or clinical advice.
