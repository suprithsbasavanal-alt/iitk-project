# Heart Disease Prediction Using Machine Learning and Deep Learning

> **College Capstone Project**: An end-to-end analytical machine learning and deep learning framework for predicting cardiovascular disease risk using clinical diagnostic data, featuring a live interactive web application.

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.5+-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Keras](https://img.shields.io/badge/Keras-3.0+-D00000.svg?logo=keras&logoColor=white)](https://keras.io/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Backend-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-20B2AA.svg)](https://xgboost.readthedocs.io/)
[![Deployment](https://img.shields.io/badge/Streamlit%20Cloud-Live%20Demo-brightgreen.svg?logo=streamlit&logoColor=white)](https://iitk-project-373qde5zip4ycoynsfqbam.streamlit.app/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Live Demo](#-live-demo)
- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Project Objectives](#-project-objectives)
- [Complete Project Workflow](#-complete-project-workflow)
- [Technologies & Tools](#-technologies--tools)
- [Dataset Architecture & Quality](#-dataset-architecture--quality)
- [Leakage-Safe Preprocessing Pipeline](#-leakage-safe-preprocessing-pipeline)
- [Exploratory Data Analysis (EDA)](#-exploratory-data-analysis-eda)
- [Machine Learning Models & Benchmarks](#-machine-learning-models--benchmarks)
- [Hyperparameter Optimization](#-hyperparameter-optimization)
- [Final Machine Learning Model](#-final-machine-learning-model)
- [Deep Learning Architecture (ANN-3)](#-deep-learning-architecture-ann-3)
- [Machine Learning vs Deep Learning Comparison](#-machine-learning-vs-deep-learning-comparison)
- [Feature Importance Analysis](#-feature-importance-analysis)
- [Streamlit Web Application](#-streamlit-web-application)
- [System Architecture](#-system-architecture)
- [Repository Structure](#-repository-structure)
- [Local Installation & Setup](#-local-installation--setup)
- [Reproducibility Guide](#-reproducibility-guide)
- [Results & Conclusion](#-results--conclusion)
- [Limitations & Future Enhancements](#-limitations--future-enhancements)
- [Literature Survey](#-literature-survey)
- [Project Documentation & Artifacts](#-project-documentation--artifacts)
- [Team Members](#-team-members)
- [Important Medical Disclaimer](#-important-medical-disclaimer)
- [References](#-references)

---

## 🌐 Live Demo

The finalized capstone application is deployed live on **Streamlit Community Cloud**:

🔗 **[https://iitk-project-373qde5zip4ycoynsfqbam.streamlit.app/](https://iitk-project-373qde5zip4ycoynsfqbam.streamlit.app/)**

### How to Use the Live Application

1. **Access the Application**: Open the live Streamlit URL in any modern desktop or mobile browser.
2. **Input Clinical Parameters**: Adjust the 13 clinical predictor widgets (sliders, number inputs, selectboxes) located in the patient form container.
3. **Load Example Patient Records**: Use the demonstration dropdown to automatically populate held-out test case profiles (e.g., *Example Patient Record #1* or *#2*).
4. **Reset Form Inputs**: Click the `🔄 Reset Inputs` button to instantly clear custom selections and restore default clinical baseline values.
5. **Select Prediction Engine**: Choose between the primary **Tuned Random Forest (ML)** engine or the secondary **Multi-Layer Perceptron (DL ANN-3)** engine via the model selector radio button.
6. **Execute Risk Assessment**: Click `🩺 Predict Heart Disease Risk` to trigger inference.
7. **Interpret Outputs**: View the predicted diagnostic class (*Heart Disease Present* vs *No Heart Disease*), calculated probability percentages, and clinical risk warnings.
8. **Analyze Benchmarks & Feature Rankings**: Scroll down to inspect the side-by-side ML vs DL test evaluation metrics table and Gini feature importance rankings.

---

## 🎯 Project Overview

Cardiovascular diseases (CVDs) remain the leading cause of mortality globally, accounting for an estimated 17.9 million lives lost each year according to the World Health Organization (WHO). Early detection of cardiac abnormalities through non-invasive clinical diagnostic parameters enables early therapeutic interventions, lifestyle modifications, and targeted medical management, significantly reducing mortality rates.

This capstone project establishes a rigorous, end-to-end analytical pipeline to predict the presence of coronary artery disease using patient clinical attributes from the UCI Cleveland Heart Disease dataset. The project systematically evaluates **7 traditional Machine Learning classifiers**, optimizes top candidates via cross-validated hyperparameter tuning, designs and benchmarks a **Deep Learning Artificial Neural Network (ANN)**, and deploys the frozen model pipelines into an interactive, cloud-hosted web application.

> **Educational & Research Notice**: This application is an educational/research demonstration created for a college capstone project. It is **NOT** a clinically validated medical diagnostic system and should **NOT** be used for medical decision-making.

---

## ❓ Problem Statement

> **Canonical Title**: *"Heart Disease Prediction Using Machine Learning and Deep Learning Techniques"*

### Technical Problem Formulation

Formally, given a vector of 13 patient clinical diagnostic features $\mathbf{x} = [x_1, x_2, \dots, x_{13}]^T \in \mathcal{X}$, where features include age, resting blood pressure, serum cholesterol, maximum heart rate, exercise-induced angina, and fluoroscopy vessel counts, the objective is to learn a mapping function $f: \mathcal{X} \rightarrow \mathcal{Y} \in \{0, 1\}$ that accurately predicts binary cardiac status:

$$\hat{y} = \begin{cases} 0, & \text{No Heart Disease Present (Absence)} \\ 1, & \text{Heart Disease Present (Presence)} \end{cases}$$

In medical diagnostic screening, the primary goal is minimizing **False Negatives ($FN$)**—instances where a patient with active heart disease is misclassified as healthy—because undetected cardiac disease poses severe life-threatening risks. Consequently, model selection prioritizes high **Recall (Sensitivity)** alongside strong overall accuracy and ROC-AUC.

---

## 📌 Project Objectives

1. **Research & Literature Review**: Conduct a comprehensive literature survey analyzing 16 peer-reviewed studies (8 ML, 8 DL) to identify benchmark algorithms and research gaps.
2. **Dataset Acquisition & Integrity**: Acquire the official UCI Cleveland Heart Disease dataset (ID 45) and preserve raw data immutability.
3. **Target Standardisation**: Transform the original multi-class severity target (`num` $\in \{0, 1, 2, 3, 4\}$) into a binary diagnostic outcome ($0 \rightarrow 0$, $1\dots4 \rightarrow 1$).
4. **Data Quality & Imputation**: Identify and handle missing values without dropping clinical instances or introducing data leakage.
5. **Leakage-Safe Preprocessing**: Design a scikit-learn preprocessing pipeline executing median numerical imputation, standard feature scaling, categorical imputation, and one-hot encoding fitted strictly on training data.
6. **Exploratory Data Analysis (EDA)**: Generate 21 publication-quality visual plots analyzing attribute distributions, target prevalence, feature correlations, and outlier characteristics.
7. **Baseline ML Benchmarking**: Train and evaluate 7 baseline machine learning classifiers using stratified 5-fold cross-validation and a 20% held-out test split.
8. **Hyperparameter Optimization**: Execute systematic grid and randomized search cross-validation across 5 candidate models to maximize test ROC-AUC and Recall.
9. **Final ML Selection**: Freeze the winning Machine Learning model pipeline artifact (`heart-disease-prediction/models/final/final_model.joblib`).
10. **Deep Learning Integration**: Build, train, and evaluate a multi-layer Keras Artificial Neural Network (`heart-disease-prediction/models/deep_learning/final_ann.keras`) utilizing PyTorch backend execution.
11. **Comparative Evaluation**: Benchmark ML vs DL performance on the 61-row held-out test set across Accuracy, Precision, Recall, Specificity, F1-Score, ROC-AUC, and False Negative counts.
12. **Interactive Deployment**: Develop a full-featured Streamlit web application (`heart-disease-prediction/app.py`) providing dual-engine inference, input validation, and metric visualizations.
13. **Cloud Hosting**: Deploy the complete application to Streamlit Community Cloud for public demonstration.

---

## 🔄 Complete Project Workflow

```text
               ┌──────────────────────────────────────────────┐
               │    16-Paper Academic Literature Survey        │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │  UCI Cleveland Dataset Acquisition (N=303)    │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │ Data Quality Audit & Target Transformation   │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │ Stratified 80/20 Train/Test Split (242 / 61)  │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │  Leakage-Safe Preprocessing Pipeline Fit     │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │   Exploratory Data Analysis (21 Figures)     │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │   7 Baseline Machine Learning Classifiers    │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │  5-Fold Stratified Hyperparameter Tuning     │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │ Freeze Final ML Model (Tuned Random Forest)  │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │ Deep Learning ANN Architecture (ANN-3 Keras)  │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │   Held-Out Test Set ML vs DL Benchmarking    │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │ Streamlit Application Development (app.py)   │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │ Live Cloud Deployment (Streamlit Cloud)      │
               └──────────────────────────────────────────────┘
```

### Stage Details

1. **Literature Survey**: Analyzed 16 empirical studies establishing baseline performance metrics, preprocessing standards, and research gaps in automated cardiac risk prediction.
2. **Dataset Acquisition**: Pulled the official Cleveland subset of the UCI Heart Disease dataset (303 rows, 14 columns).
3. **Data Audit & Target Mapping**: Mapped multi-class target levels $0$ (absence) and $1, 2, 3, 4$ (presence) to binary targets ($0=164$ samples, $1=139$ samples).
4. **Stratified Train/Test Split**: Partitioned the 303 samples into 242 training instances (80%) and 61 testing instances (20%) using stratified sampling (`random_state=42`).
5. **Preprocessing Pipeline**: Constructed a scikit-learn `ColumnTransformer` executing median numerical imputation, feature scaling, categorical imputation, and one-hot encoding fitted strictly on `X_train_raw`.
6. **Exploratory Data Analysis**: Analyzed univariate distributions, bivariate target relationships, correlation matrices, and outlier boundaries across 21 figures.
7. **Baseline ML Evaluation**: Trained 7 baseline ML algorithms (Logistic Regression, KNN, Decision Tree, Random Forest, SVM, Naive Bayes, XGBoost).
8. **Hyperparameter Tuning**: Tuned 5 model families using 5-fold Stratified `GridSearchCV` and `RandomizedSearchCV` optimizing for ROC-AUC.
9. **Final ML Freezing**: Selected Tuned Random Forest (Test Accuracy: 90.16%, Recall: 96.43%, ROC-AUC: 0.9567, FN=1) and saved pipeline to `heart-disease-prediction/models/final/final_model.joblib`.
10. **Deep Learning ANN**: Implemented a 4-layer Keras Artificial Neural Network (ANN-3) with PyTorch backend, achieving 85.25% test accuracy and 96.43% recall (`heart-disease-prediction/models/deep_learning/final_ann.keras`).
11. **ML vs DL Benchmarking**: Compared model artifacts on the 61 untouched test samples across 7 evaluation metrics.
12. **Streamlit Application**: Built a responsive 13-feature patient assessment web dashboard supporting dual-engine inference and dynamic feature importance visualization.
13. **Cloud Deployment**: Deployed the verified project to Streamlit Community Cloud.

---

## 🛠️ Technologies & Tools

| Technology | Role in Project | Implementation Details |
| :--- | :--- | :--- |
| **Python 3.10+** | Core Programming Language | Base runtime environment for ML/DL pipelines, data manipulation, and web application logic. |
| **Pandas** | Tabular Data Processing | Dataset loading, missing-value audits, summary statistics generation, and CSV report exports. |
| **NumPy** | Array & Vector Operations | Matrix calculations, probability array manipulation, and numerical metrics evaluation. |
| **Scikit-Learn** | Machine Learning Framework | Preprocessing pipelines (`ColumnTransformer`, `StandardScaler`, `OneHotEncoder`), baseline models, hyperparameter tuning (`GridSearchCV`, `RandomizedSearchCV`), and evaluation metrics. |
| **TensorFlow / Keras** | Deep Learning Framework | Construction, training, regularisation, early stopping, and serialization of the 4-layer Artificial Neural Network (ANN-3). |
| **PyTorch** | Keras Execution Backend | Configured as the underlying backend engine (`os.environ["KERAS_BACKEND"] = "torch"`) for deterministic Keras tensor operations. |
| **XGBoost** | Gradient Boosting Model | Implementation of non-linear gradient boosted decision trees for baseline and tuned benchmarking. |
| **Joblib** | Model Artifact Serialization | Serialization and deserialization of fitted scikit-learn models (`final_model.joblib`) and preprocessors (`preprocessor.joblib`). |
| **Matplotlib / Seaborn** | Data Visualization | Generation of 21 EDA plots, confusion matrix heatmaps, ROC curves, precision-recall curves, and training history plots. |
| **Streamlit** | Web Application Framework | Building the interactive web dashboard (`heart-disease-prediction/app.py`), session state management, widget UI components, and cloud integration. |
| **Jupyter Notebook** | Experimental Prototyping | Step-by-step notebook execution for EDA, baseline experiments, hyperparameter search, and ANN training. |
| **Git / GitHub** | Version Control & Source Code | Distributed source code management, tracking model artifacts, and automated deployment sync with Streamlit Cloud. |

---

## 📊 Dataset Architecture & Quality

### Dataset Identification

- **Source**: UCI Machine Learning Repository
- **Dataset Title**: Heart Disease Dataset (Cleveland Subset)
- **UCI Dataset ID**: 45
- **Total Instances**: 303
- **Total Attributes**: 14 (13 clinical predictors + 1 target variable)

### Raw Attribute Definitions & Clinical Dictionary

| Attribute | Variable Name | Type | Measurement Range / Categories | Clinical Description |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `age` | Numerical | 29 – 77 years | Age of the patient in years |
| 2 | `sex` | Categorical | 0 = Female, 1 = Male | Biological sex of the patient |
| 3 | `cp` | Categorical | 1: Typical Angina, 2: Atypical Angina, 3: Non-anginal Pain, 4: Asymptomatic | Chest pain type experienced by patient |
| 4 | `trestbps` | Numerical | 94 – 200 mm Hg | Resting blood pressure on admission to hospital |
| 5 | `chol` | Numerical | 126 – 564 mg/dl | Serum cholesterol measurement |
| 6 | `fbs` | Categorical | 0: $\le$ 120 mg/dl, 1: $>$ 120 mg/dl | Fasting blood sugar status |
| 7 | `restecg` | Categorical | 0: Normal, 1: ST-T wave abnormality, 2: Left ventricular hypertrophy | Resting electrocardiographic results |
| 8 | `thalach` | Numerical | 71 – 202 bpm | Maximum heart rate achieved during exercise test |
| 9 | `exang` | Categorical | 0: No, 1: Yes | Exercise-induced angina presence |
| 10 | `oldpeak` | Numerical | 0.0 – 6.2 | ST depression induced by exercise relative to rest |
| 11 | `slope` | Categorical | 1: Upsloping, 2: Flat, 3: Downsloping | Slope of peak exercise ST segment |
| 12 | `ca` | Discrete/Categorical | 0, 1, 2, 3 vessels | Number of major vessels (0–3) colored by fluoroscopy |
| 13 | `thal` | Categorical | 3: Normal, 6: Fixed Defect, 7: Reversible Defect | Thalassemia blood disorder status |
| 14 | `num` (Target) | Target | 0: Absence, 1–4: Presence | Diagnosis of heart disease (angiographic disease status) |

### Target Mapping Logic

The original UCI dataset records angiographic disease severity across 5 integer levels:
- `num = 0`: No diameter narrowing $> 50\%$ (Absence of disease)
- `num = 1, 2, 3, 4`: Diameter narrowing $> 50\%$ across 1 to 4 major vessels (Presence of disease)

For binary diagnostic classification, the target is transformed as follows:

$$\text{Target} = \begin{cases} 0 \quad (\text{No Heart Disease}), & \text{if } \text{num} = 0 \quad (N = 164 \text{ instances}, 54.13\%) \\ 1 \quad (\text{Heart Disease Present}), & \text{if } \text{num} \in \{1, 2, 3, 4\} \quad (N = 139 \text{ instances}, 45.87\%) \end{cases}$$

### Data Quality & Missing Value Audit

- **Total Rows**: 303
- **Total Columns**: 14
- **Duplicate Rows**: 0
- **Missing Value Breakdown**:
  - `ca` (fluoroscopy vessels): 4 missing entries
  - `thal` (thalassemia status): 2 missing entries
  - **Total Missing Cells**: 6 out of 4,242 cells (0.14%)

---

## 🔒 Leakage-Safe Preprocessing Pipeline

To eliminate data leakage—where information from the evaluation split inadvertently influences model training—the dataset is split **prior** to any statistical transformation.

```
Raw Dataset (N=303) ──► Stratified 80/20 Split ──┬──► Train Set (N=242) ──► Fit Preprocessor
                                                   └──► Test Set (N=61)   ──► Transform Only
```

### Preprocessing Architecture (`ColumnTransformer`)

1. **Stratified Split**: Partitioned into 242 training instances (80%) and 61 test instances (20%) using `stratify=y` and `random_state=42`.
2. **Numerical Pipeline** (`age`, `trestbps`, `chol`, `thalach`, `oldpeak`):
   - `SimpleImputer(strategy='median')`: Imputes missing numerical values using training set medians.
   - `StandardScaler()`: Standardizes features by subtracting mean and scaling to unit variance:
     $$z = \frac{x - \mu}{\sigma}$$
3. **Categorical Pipeline** (`sex`, `cp`, `fbs`, `restecg`, `exang`, `slope`, `ca`, `thal`):
   - `SimpleImputer(strategy='most_frequent')`: Imputes missing categorical codes using training set modes.
   - `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`: Encodes categorical variables into 23 binary dummy columns.
4. **Transformed Schema Dimension**: The 13 raw input attributes expand into **28 preprocessed features**.

---

## 📈 Exploratory Data Analysis (EDA)

The project executed thorough visual and quantitative EDA, outputting **21 publication-quality plots** saved in `heart-disease-prediction/results/figures/`:

1. **Target Distribution**: Confirmed balanced target class proportions (54.13% negative vs 45.87% positive).
2. **Numerical Feature Distributions**: Analyzed bell-curve normality for `age` and `thalach`, alongside positive skewness in `chol`, `trestbps`, and `oldpeak`.
3. **Categorical Prevalence Analysis**:
   - **Sex**: Male patients demonstrated higher disease prevalence (55.3%) compared to female patients (25.8%).
   - **Chest Pain (`cp`)**: Asymptomatic chest pain (`cp=4`) exhibited the highest proportion of positive heart disease cases (72.7%).
   - **Exercise Angina (`exang`)**: Patients with exercise-induced angina had a significantly higher disease rate (62.9%) than those without (30.6%).
   - **Thalassemia (`thal`)**: Patients with reversible defects (`thal=7`) showed an 75.9% disease rate.
4. **Correlation Analysis**: Maximum heart rate (`thalach`) showed strong negative correlation with heart disease presence ($r = -0.42$), while exercise ST depression (`oldpeak`) exhibited strong positive correlation ($r = +0.42$).
5. **Outlier Auditing**: Identified mild high-range outliers in `chol` ($> 400$ mg/dl) and `trestbps` ($> 170$ mm Hg), retained safely due to robust tree-based modeling and standard scaling.

---

## 🤖 Machine Learning Models & Benchmarks

Seven diverse classification algorithms were trained on the 242-row training set using 5-fold stratified cross-validation and evaluated on the 61-row held-out test set:

### Baseline Test Set Performance (61 Held-Out Samples)

| Model Name | Test Accuracy | Test Precision | Test Recall | Test Specificity | Test F1 | Test ROC-AUC | False Negatives ($FN$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 88.52% | 83.87% | 92.86% | 84.85% | 88.14% | 0.9665 | 2 |
| **K-Nearest Neighbors (KNN)** | 88.52% | 86.21% | 89.29% | 87.88% | 87.72% | 0.9529 | 3 |
| **Decision Tree** | 73.77% | 67.65% | 82.14% | 66.67% | 74.19% | 0.7440 | 5 |
| **Random Forest (Baseline)** | 86.89% | 81.25% | 92.86% | 81.82% | 86.67% | 0.9437 | 2 |
| **Support Vector Machine (SVM)** | 88.52% | 83.87% | 92.86% | 84.85% | 88.14% | 0.9643 | 2 |
| **Gaussian Naive Bayes** | 72.13% | 64.10% | 89.29% | 57.58% | 74.63% | 0.8268 | 3 |
| **XGBoost (Baseline)** | 83.61% | 76.47% | 92.86% | 75.76% | 83.87% | 0.9340 | 2 |

---

## ⚙️ Hyperparameter Optimization

Hyperparameter tuning was conducted across 5 model families using 5-fold Stratified `GridSearchCV` and `RandomizedSearchCV`, optimizing strictly for **Cross-Validation ROC-AUC** on the training split. *The held-out 61-row test set was completely isolated during search.*

### Best Hyperparameters Identified

```json
{
  "Tuned Random Forest": {
    "n_estimators": 500,
    "min_samples_split": 4,
    "min_samples_leaf": 2,
    "max_features": "log2",
    "max_depth": null,
    "class_weight": "balanced_subsample"
  },
  "Tuned Logistic Regression": {
    "C": 1.0,
    "penalty": "l1",
    "solver": "liblinear",
    "class_weight": null
  },
  "Tuned SVM": {
    "C": 0.1,
    "kernel": "linear",
    "class_weight": null
  },
  "Tuned XGBoost": {
    "n_estimators": 100,
    "learning_rate": 0.03,
    "max_depth": 5,
    "subsample": 0.6,
    "colsample_bytree": 0.7,
    "min_child_weight": 7,
    "reg_alpha": 0.1,
    "reg_lambda": 1.0
  },
  "Tuned KNN": {
    "n_neighbors": 11,
    "weights": "distance",
    "metric": "manhattan",
    "p": 1
  }
}
```

---

## 🏆 Final Machine Learning Model

The **Tuned Random Forest** model achieved the strongest multi-criteria performance on the held-out test set and was selected as the primary winning Machine Learning pipeline.

### Final ML Performance Summary

- **Test Accuracy**: **90.16%** (55 / 61 correct)
- **Test Precision**: **84.38%** (27 / 32 predicted positives)
- **Test Recall (Sensitivity)**: **96.43%** (27 / 28 actual disease cases detected)
- **Test Specificity**: **84.85%** (28 / 33 healthy controls confirmed)
- **Test F1-Score**: **90.00%**
- **Test ROC-AUC**: **0.9567**

### Final ML Confusion Matrix

$$\begin{pmatrix} TN = 28 & FP = 5 \\ FN = 1 & TP = 27 \end{pmatrix}$$

> **Clinical Screening Relevance**: Out of 28 true cardiac disease cases in the test set, the Tuned Random Forest model correctly identified **27 cases**, resulting in only **1 False Negative ($FN=1$)**. In medical screening, minimizing false negatives prevents high-risk patients from leaving diagnostic evaluations untreated.

---

## 🧠 Deep Learning Architecture (ANN-3)

To benchmark traditional Machine Learning against Deep Learning, a custom Artificial Neural Network architecture (**ANN-3**) was developed using **Keras** with a **PyTorch execution backend**.

### ANN-3 Layer Specification

```
Input Layer (28 Transformed Features)
       │
       ▼
Dense Layer 1: 64 Neurons, ReLU Activation
       │
   Dropout (Rate = 0.3)
       │
       ▼
Dense Layer 2: 32 Neurons, ReLU Activation
       │
   Dropout (Rate = 0.2)
       │
       ▼
Dense Layer 3: 16 Neurons, ReLU Activation
       │
   Dropout (Rate = 0.1)
       │
       ▼
Output Layer: 1 Neuron, Sigmoid Activation
```

### Hyperparameters & Training Configuration

- **Input Dimension**: 28 one-hot transformed numeric attributes
- **Output Function**: Sigmoid activation producing continuous probability $p \in [0.0, 1.0]$
- **Optimizer**: Adam ($\text{learning\_rate} = 0.001$)
- **Loss Function**: Binary Cross-Entropy:
  $$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^N \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]$$
- **Epochs & Batch Size**: 100 max epochs, batch size of 16
- **Regularization**: Progressive Dropout ($0.3 \rightarrow 0.2 \rightarrow 0.1$)
- **Dynamic Callbacks**:
  - `EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)`
  - `ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=7)`

---

## 🔬 Machine Learning vs Deep Learning Comparison

Both frozen model artifacts (`final_model.joblib` and `final_ann.keras`) were evaluated on the identical 61-row held-out test split:

| Evaluation Metric | Tuned Random Forest (ML) | Final ANN-3 (Deep Learning) | Performance Differential |
| :--- | :---: | :---: | :---: |
| **Test Accuracy** | **90.16%** | 85.25% | **+4.91% (ML Advantage)** |
| **Test Precision** | **84.38%** | 79.41% | **+4.97% (ML Advantage)** |
| **Test Recall (Sensitivity)** | **96.43%** | **96.43%** | **Identical (27 / 28 Detected)** |
| **Test Specificity** | **84.85%** | 75.76% | **+9.09% (ML Advantage)** |
| **Test F1-Score** | **90.00%** | 87.10% | **+2.90% (ML Advantage)** |
| **Test ROC-AUC** | **0.9567** | 0.9253 | **+0.0314 (ML Advantage)** |
| **False Negatives ($FN$)** | **1** | **1** | **Identical ($FN=1$)** |
| **False Positives ($FP$)** | **5** | 8 | **-3 (ML Advantage)** |

### Analytical Conclusion

On this tabular dataset ($N=303$), the **Tuned Random Forest** model outperformed the **Deep Learning ANN-3** across Accuracy (+4.91%), Precision (+4.97%), Specificity (+9.09%), F1 (+2.90%), and ROC-AUC (+0.0314), while both architectures achieved identical high recall (96.43%, $FN=1$).

Tree-based ensemble methods excel on small tabular diagnostic datasets due to their intrinsic resistance to overfitting and effective handling of non-linear feature interactions without requiring massive sample volumes.

---

## 📊 Feature Importance Analysis

Feature importances were extracted from the frozen Tuned Random Forest model using Gini impurity reduction across 500 decision trees:

| Feature Name | Transformed Feature | Gini Importance | Contribution Percentage | Clinical Significance |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `thal_3.0` | 0.1023 | 10.23% | Normal thalassemia blood status |
| 2 | `ca_0.0` | 0.0888 | 8.88% | Zero major vessels colored by fluoroscopy |
| 3 | `thal_7.0` | 0.0852 | 8.52% | Reversible defect thalassemia status |
| 4 | `cp_4.0` | 0.0791 | 7.91% | Asymptomatic chest pain manifestation |
| 5 | `thalach` | 0.0787 | 7.87% | Maximum heart rate achieved during exercise |
| 6 | `oldpeak` | 0.0735 | 7.35% | Exercise-induced ST depression depth |
| 7 | `age` | 0.0681 | 6.81% | Patient chronological age |
| 8 | `chol` | 0.0594 | 5.94% | Serum cholesterol measurement |

> **Methodological Note**: Feature importance scores represent relative predictive weight within this specific trained ensemble model. They signify statistical association within the dataset, not direct clinical causation.

---

## 💻 Streamlit Web Application

The interactive web application (`heart-disease-prediction/app.py`) serves as the production demonstration dashboard:

```
                  ┌──────────────────────────────────────────────┐
                  │          Streamlit Web Dashboard             │
                  └──────────────────────┬───────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
    ┌─────────────────────────┐                     ┌─────────────────────────┐
    │ Sidebar & Control Panel │                     │   Patient Input Form    │
    │ • Model Specs & Metrics │                     │ • 13 Clinical Widgets   │
    │ • Test Split Benchmarks │                     │ • Preset Test Profiles  │
    └─────────────────────────┘                     │ • 🔄 Reset Inputs Button│
                                                    └────────────┬────────────┘
                                                                 │
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │ Dual Inference Engine   │
                                                    │ 🔘 Tuned Random Forest  │
                                                    │ 🔘 Keras ANN-3          │
                                                    └────────────┬────────────┘
                                                                 │
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │  Diagnostic Output Card │
                                                    │ • Binary Risk Class     │
                                                    │ • Probability Gauges    │
                                                    │ • Disclaimer Banner     │
                                                    └────────────┬────────────┘
```

### Core Interface Features

- **Input Control Form**: Provides intuitive UI controls for all 13 clinical predictors (numeric sliders, number step inputs, and selectboxes).
- **Preset Demonstration Records**: Allows instant loading of real test patient profiles (*Example Patient #1* and *#2*).
- **Dedicated Reset Button**: Restores all 13 input widgets to baseline default states using session state callbacks without text wrapping.
- **Dual Inference Switching**: Toggle dynamically between the primary **Tuned Random Forest** engine and the **Keras ANN-3** engine.
- **Diagnostic Risk Cards**: Renders clean green (`No Heart Disease`) or red (`Heart Disease Present`) alert cards with calculated probability percentages.
- **Benchmark Comparison View**: Displays the side-by-side performance table and ROC-AUC metrics.
- **Feature Importance Visualizer**: Renders interactive bar charts showing top Gini feature rankings.

---

## 🏗️ System Architecture

```text
                                 [ User Browser ]
                                        │
                                        ▼
                     [ Streamlit Frontend (heart-disease-prediction/app.py) ]
                                        │
                                        ▼
                           [ Input Schema Validation ]
                                        │
                                        ▼
                          [ Preprocessing Transformer ]
                  (heart-disease-prediction/models/preprocessor.joblib)
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
       [ Tuned Random Forest ML ]                  [ Keras ANN-3 DL ]
(heart-disease-prediction/models/final/      (heart-disease-prediction/models/
     final_model.joblib)                           deep_learning/final_ann.keras)
                    │                                       │
                    └───────────────────┬───────────────────┘
                                        ▼
                           [ Output Risk Estimation ]
                         • Class (0 / 1) & Probability
                                        │
                                        ▼
                           [ Render Dashboard Cards ]
```

---

## 📂 Repository Structure

```text
iitk-project/
├── README.md                           # Repository Root README (GitHub Homepage)
└── heart-disease-prediction/
    ├── app.py                          # Streamlit application entry point
    ├── main.py                         # CLI application entry point
    ├── requirements.txt                # Python package dependencies
    ├── .gitignore                      # Git exclusion rules
    ├── README.md                       # Nested project documentation
    │
    ├── data/
    │   ├── raw/                        # Immutable raw dataset (heart_disease_uci.csv)
    │   └── processed/                  # Split CSV datasets (X_train_raw, X_test_raw, y_train, y_test)
    │
    ├── src/                            # Modular Python package source code
    │   ├── __init__.py                 # Package initializer
    │   ├── download_data.py            # Dataset downloader script
    │   ├── data_loader.py              # Data loading & validation utilities
    │   ├── preprocessing.py            # Preprocessing & split functions
    │   ├── eda.py                      # EDA plotting functions
    │   ├── train.py                    # Training & tuning module
    │   ├── evaluate.py                 # Evaluation metrics & figure generators
    │   ├── predict.py                  # ML inference & schema validation routines
    │   └── deep_learning.py            # Deep Learning ANN architecture & training module
    │
    ├── scripts/                        # Automation & verification scripts
    │   ├── generate_eda.py             # Master EDA plot generator
    │   ├── train_baseline_models.py    # Baseline models training script
    │   ├── tune_models.py              # Hyperparameter tuning script
    │   ├── select_final_model.py       # Final model selection & freezing script
    │   ├── train_deep_learning.py     # Master ANN training & benchmarking script
    │   ├── final_project_audit.py      # Master 30-point capstone project audit script
    │   └── verify_*.py                 # Modular verification test suites (Parts 1-12)
    │
    ├── models/                         # Serialized model artifacts
    │   ├── preprocessor.joblib         # Fitted scikit-learn preprocessor pipeline
    │   ├── baseline/                   # 7 Persisted baseline model joblib files
    │   ├── tuned/                      # 5 Persisted tuned model joblib files
    │   ├── final/                      # Frozen final ML model (final_model.joblib & metadata)
    │   └── deep_learning/              # Frozen final DL model (final_ann.keras)
    │
    ├── notebooks/                      # Executed Jupyter analysis notebooks
    │   ├── 01_eda.ipynb                # Executed EDA notebook
    │   ├── 02_baseline_models.ipynb    # Executed Baseline Models notebook
    │   ├── 03_hyperparameter_tuning.ipynb # Executed Hyperparameter Tuning notebook
    │   ├── 04_final_ml_model.ipynb     # Executed Final ML Model notebook
    │   └── 05_deep_learning_ann.ipynb  # Executed Deep Learning ANN notebook
    │
    ├── results/                        # Experimental results & generated visual artifacts
    │   ├── eda_*.csv                   # Quantitative EDA summary tables
    │   ├── final_feature_importance.csv# Feature importances CSV
    │   ├── references.md               # Citations & references document
    │   ├── figures/                    # 21 EDA plots + model evaluation figures
    │   ├── metrics/                    # Experimental evaluation CSV tables & search results
    │   ├── literature/                 # Team literature survey allocations & CSVs
    │   ├── final_audit/                # End-to-end master audit reports & file hashes
    │   └── deployment/                 # Cloud deployment readiness reports
    │
    ├── reports/                        # Academic capstone submission artifacts
    │   ├── Heart_Disease_Capstone_Final_Report.docx # Final academic report
    │   ├── Heart_Disease_Capstone_Presentation.pptx # Final presentation slides
    │   ├── Viva_Questions_and_Answers.md            # Comprehensive viva examination Q&A
    │   └── Demo_Guide.md                            # Live presentation demonstration guide
    │
    ├── submission/                     # Verification manifests & submission checksums
    │   └── SUBMISSION_MANIFEST.md      # Final project submission manifest
    │
    └── tests/                          # Automated unit test suite
        ├── test_preprocessing.py       # Unit tests for preprocessing
        ├── test_train.py               # Unit tests for model training
        ├── test_evaluate.py            # Unit tests for evaluation
        ├── test_tuning.py              # Unit tests for hyperparameter tuning
        ├── test_final_model.py         # Unit tests for final ML pipeline
        ├── test_application.py         # Unit tests for Streamlit application
        └── test_deep_learning.py       # Unit tests for Deep Learning module
```

---

## 💻 Local Installation & Setup

Follow these steps to set up and run the repository on your local machine:

### Prerequisites

- **Python**: Version 3.10, 3.11, or 3.12 installed.
- **Git**: Installed for repository cloning.

### Step 1: Clone the Repository

```bash
git clone https://github.com/suprithsbasavanal-alt/iitk-project.git
cd iitk-project/heart-disease-prediction
```

### Step 2: Create & Activate Virtual Environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (Command Prompt / PowerShell)
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Required Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Launch the Streamlit Web Application

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

### Step 5: Run Automated Unit Test Suite

```bash
python -m unittest discover tests
```

---

## 🔁 Reproducibility Guide

To verify end-to-end reproducibility from scratch:

1. **Verify Raw Data**: Confirm `heart-disease-prediction/data/raw/heart_disease_uci.csv` matches SHA-256 hash `ecb42eeecad354d241775efcf2084ec2d17c9eb1187498c48408f6d7d5d2834b`.
2. **Execute Full Audit**: Run `python heart-disease-prediction/scripts/final_project_audit.py` to execute all 30 automated integrity checks.
3. **Reproduce Baseline Training**: Run `python heart-disease-prediction/scripts/train_baseline_models.py`.
4. **Reproduce Tuning**: Run `python heart-disease-prediction/scripts/tune_models.py`.
5. **Reproduce ANN Training**: Run `python heart-disease-prediction/scripts/train_deep_learning.py`.
6. **Deterministic Seed**: All splits, initializations, and cross-validation folds use `random_state=42`.

---

## 🏁 Results & Conclusion

1. **Machine Learning Superiority on Small Tabular Data**: The **Tuned Random Forest** model achieved **90.16% Test Accuracy**, **96.43% Test Recall**, **90.00% F1-Score**, and **0.9567 ROC-AUC**, outperforming the Deep Learning ANN-3 architecture (+4.91% Accuracy).
2. **High Clinical Recall**: Both the winning Random Forest and ANN-3 models achieved **96.43% Recall**, missing only **1 false negative** ($FN=1$) out of 28 cardiac disease cases in the held-out evaluation set.
3. **Key Diagnostic Predictors**: Fluoroscopy vessel count (`ca`), thalassemia type (`thal`), maximum heart rate (`thalach`), and exercise ST depression (`oldpeak`) emerged as the strongest predictors of heart disease risk.
4. **Successful Deployment**: The finalized pipelines were successfully integrated into a responsive Streamlit web application deployed live on Streamlit Community Cloud.

---

## ⚠️ Limitations & Future Enhancements

### Current Project Limitations

- **Dataset Size**: Evaluated on $N=303$ clinical instances from a single geographic center (Cleveland Clinic).
- **Single Held-Out Split**: Tested on a single 61-row test split (20%); cross-validation performance provides broader estimates.
- **Absence of External Clinical Validation**: Models have not been evaluated on real-world prospective hospital populations.

### Planned Future Work

- **Multi-Center Datasets**: Incorporate Hungarian, Long Beach, and Switzerland subsets of the UCI dataset ($N=920+$).
- **Model Calibration**: Apply Platt Scaling or Isotonic Regression to refine probability estimates.
- **Explainable AI (XAI)**: Integrate SHAP (SHapley Additive exPlanations) force plots into the Streamlit dashboard for patient-specific feature explanations.

---

## 📚 Literature Survey

The project was informed by a systematic literature review analyzing **16 peer-reviewed studies** (8 ML + 8 DL), evenly allocated across the 4-member project team:

| Author(s) & Year | Model Architecture | Reported Accuracy | Key Findings / Contribution | Team Member |
| :--- | :--- | :---: | :--- | :--- |
| **Jan et al. (2021)** | Ensemble ML (RF + XGB) | 93.33% | Demonstrated superiority of tree ensembles on UCI Cleveland data. | Shreyas |
| **Mohan et al. (2019)** | Hybrid HRFLM | 88.70% | Combined Random Forest with Linear Models to improve classification. | Uday |
| **Ali et al. (2019)** | Stacked Support Vector Machine | 92.22% | Applied feature selection and L1 regularization for dimensionality reduction. | Suprith S Basavanal |
| **Latha & Jeeva (2019)** | Random Forest Ensemble | 85.48% | Evaluated feature selection impact on heart disease prediction precision. | Sahitya |
| **Shah et al. (2020)** | Deep Neural Network (DNN) | 90.78% | Evaluated multi-layer perceptron with Adam optimizer on clinical data. | Shreyas |
| **Mienye et al. (2020)** | Sparse Autoencoder + ANN | 90.16% | Used autoencoders for feature extraction prior to neural classification. | Uday |
| **Spandana et al. (2023)** | Multi-Layer Perceptron (MLP) | 88.50% | Analyzed hyperparameter sensitivity in deep learning cardiac diagnostic models. | Suprith S Basavanal |
| **Rath et al. (2021)** | Convolutional Neural Net 1D | 89.30% | Applied 1D-CNN filters across 13 numerical cardiac attributes. | Sahitya |

*For complete citations, DOIs, and full 16-paper summary matrix, view [heart-disease-prediction/results/references.md](heart-disease-prediction/results/references.md).*

---

## 📑 Project Documentation & Artifacts

All core project documentation, viva preparation materials, and submission checklists are maintained in the repository:

- 📄 **[Final Academic Capstone Report](heart-disease-prediction/reports/Heart_Disease_Capstone_Final_Report.docx)**: Comprehensive 25+ page academic capstone manuscript (`.docx`).
- 📊 **[Final Presentation Slides](heart-disease-prediction/reports/Heart_Disease_Capstone_Presentation.pptx)**: Project presentation slide deck (`.pptx`).
- 💬 **[Viva Questions & Answers](heart-disease-prediction/reports/Viva_Questions_and_Answers.md)**: 30 detailed viva defense questions and technical answers.
- 🎬 **[Live Presentation Demo Guide](heart-disease-prediction/reports/Demo_Guide.md)**: Step-by-step presentation demonstration guide.
- 📋 **[Submission Manifest](heart-disease-prediction/submission/SUBMISSION_MANIFEST.md)**: Master submission verification manifest and artifact hashes.

---

## 👥 Team Members

This capstone project was conceptualized, developed, and evaluated by a 4-member project team:

- **Shreyas** — *Dataset Acquisition, EDA & Literature Review*
- **Uday** — *Preprocessing Pipeline & Baseline ML Modeling*
- **Suprith S Basavanal** — *Hyperparameter Optimization, ANN Architecture & Web Deployment*
- **Sahitya** — *Model Benchmarking, Verification Suite & Final Documentation*

---

## ⚠️ Important Medical Disclaimer

> **IMPORTANT DISCLAIMER**: This application and its underlying code are created strictly for **educational, academic research, and demonstration purposes** as part of a college capstone project. This system is **NOT** a clinically validated medical diagnostic tool and must **NOT** be used to diagnose, treat, prevent, or manage heart disease or any other medical condition. Always consult a qualified healthcare professional for medical advice and clinical diagnosis.

---

## 📖 References

1. **UCI Machine Learning Repository**: Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1988). *Heart Disease Data Set (Cleveland Subset)*. [https://archive.ics.uci.edu/dataset/45/heart+disease](https://archive.ics.uci.edu/dataset/45/heart+disease)
2. **Scikit-Learn Documentation**: Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. JMLR, 12, 2825-2830.
3. **Keras & PyTorch Frameworks**: Chollet, F., et al. (2015). *Keras Deep Learning Library*. [https://keras.io](https://keras.io)
4. **Streamlit Framework**: Streamlit Inc. (2024). *Streamlit Web Application Documentation*. [https://docs.streamlit.io](https://docs.streamlit.io)
5. **Project Literature Survey**: View complete 16-paper references matrix in [heart-disease-prediction/results/references.md](heart-disease-prediction/results/references.md).
