# Capstone Viva Examination: Questions and Answers (Part 9 & Part 11)

**Project Title**: Heart Disease Prediction Using Machine Learning and Deep Learning Techniques  
**Team Members**: Shreyas, Uday, Suprith, Sahitya  
**Target Audience**: Second-Year Computer Science & Engineering Capstone Defense  

---

## Section 1: Dataset & Problem Formulation

### Q1: What is the main objective of this capstone project?
**Answer**: The main objective is to develop, evaluate, tune, and compare multiple machine learning algorithms for predicting the presence of heart disease based on patient clinical indicators from the UCI Heart Disease dataset, and deploy the frozen winning pipeline as an interactive web application.

### Q2: Which dataset is used, and what are its key dimensions?
**Answer**: We used the official UCI Heart Disease Dataset (Cleveland subset, Dataset ID 45). It contains 303 total patient observations and 13 clinical predictor attributes plus 1 target variable (`num`).

### Q3: How was the target variable processed from multiclass to binary?
**Answer**: The original UCI `num` target had values 0 (absence) and 1, 2, 3, 4 (varying degrees of heart disease). We mapped `0` to class `0` ("No Heart Disease", 164 cases) and `{1, 2, 3, 4}` to class `1` ("Heart Disease Present", 139 cases), creating a clean binary classification problem.

### Q4: Were there any missing values or duplicates in the raw dataset?
**Answer**: Yes, there were 6 missing values in total across two columns: `ca` (4 missing values) and `thal` (2 missing values). There were 0 duplicate rows in the dataset.

---

## Section 2: Data Preprocessing & Data Leakage Prevention

### Q5: What train/test split ratio was used, and why?
**Answer**: An 80/20 stratified train/test split was used with `random_state=42`. This allocated 242 patient rows for training and cross-validation, and held out 61 untouched patient rows strictly for final model evaluation.

### Q6: What is data leakage, and how did our pipeline prevent it?
**Answer**: Data leakage occurs when information from the test dataset unintentionally influences the training phase, leading to overly optimistic metrics. We prevented data leakage by fitting all missing value imputers (`SimpleImputer`), continuous scalers (`StandardScaler`), and categorical encoders (`OneHotEncoder`) strictly on the training fold (`X_train_raw`) within complete scikit-learn `Pipeline` objects.

### Q7: How were continuous vs categorical features preprocessed?
**Answer**: 
- **Continuous Features (5)** (`age`, `trestbps`, `chol`, `thalach`, `oldpeak`): Imputed using median strategy, then scaled using `StandardScaler`.
- **Categorical Features (8)** (`sex`, `cp`, `fbs`, `restecg`, `exang`, `slope`, `ca`, `thal`): Imputed using most-frequent strategy, then encoded using `OneHotEncoder(handle_unknown="ignore")`.

### Q8: What was the total feature count after one-hot encoding?
**Answer**: The original 13 predictor columns expanded to exactly 28 transformed numeric features after one-hot encoding categorical variables.

---

## Section 3: Exploratory Data Analysis (EDA)

### Q9: What were the top continuous feature correlations with the target variable?
**Answer**: 
- `thalach` (Maximum Heart Rate Achieved): Negative correlation ($r = -0.42$). Higher max heart rate is associated with absence of disease.
- `oldpeak` (ST Depression): Positive correlation ($r = +0.42$). Higher ST depression is associated with presence of disease.
- `age` (Age): Positive correlation ($r = +0.23$). Older age has a moderate association with heart disease.

### Q10: Why must we use cautious wording like "descriptive association" rather than "causation"?
**Answer**: Observational correlation analysis in EDA identifies statistical co-occurrence in data; it does not prove medical cause-and-effect mechanisms.

---

## Section 4: Machine Learning Baseline & Tuning Algorithms

### Q11: Which 7 baseline machine learning models were evaluated?
**Answer**: 
1. Logistic Regression
2. K-Nearest Neighbors (KNN)
3. Decision Tree
4. Random Forest
5. Support Vector Machine (SVM)
6. Gaussian Naive Bayes
7. XGBoost

### Q12: How was cross-validation structured during baseline and tuning stages?
**Answer**: We used 5-Fold Stratified Cross-Validation (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`) executed strictly on the 242 training rows. Test set rows (61 rows) were completely isolated.

### Q13: Why was hyperparameter tuning performed on 5 candidate models?
**Answer**: Tuning optimizes hyperparameters (like tree depth, regularization, or number of neighbors) to improve generalization and reduce bias/variance. We tuned Logistic Regression, SVM, Random Forest, XGBoost, and KNN using `GridSearchCV` or `RandomizedSearchCV`.

### Q14: What hyperparameter search space was defined for Random Forest?
**Answer**: `n_estimators` (100–500), `max_depth` (None, 5–20), `min_samples_split` (2–10), `min_samples_leaf` (1–4), `max_features` ("sqrt", "log2"), and `class_weight` ("balanced", "balanced_subsample").

---

## Section 5: Final Model Selection & Evaluation Metrics

### Q15: Which model was selected as the final winning pipeline, and why?
**Answer**: **Tuned Random Forest** was selected based on transparent multi-criteria evaluation. It achieved the highest Test Accuracy (90.16%), highest Test Recall (96.43%), highest Test F1 (90.00%), lowest False Negatives (FN=1), strong CV ROC-AUC (0.9041), and high interpretability.

### Q16: What are the exact frozen hyperparameters of the final model?
**Answer**: 
`n_estimators=500`, `min_samples_split=4`, `min_samples_leaf=2`, `max_features="log2"`, `max_depth=None`, `class_weight="balanced_subsample"`, `random_state=42`.

### Q17: What were the exact final performance metrics on the held-out test set?
**Answer**: 
- **Test Accuracy**: 0.9016 (55 / 61 correct)
- **Test Precision**: 0.8438 (27 / 32 predicted positive correct)
- **Test Recall (Sensitivity)**: 0.9643 (27 / 28 disease cases detected)
- **Test Specificity**: 0.8485 (28 / 33 healthy cases detected)
- **Test F1-Score**: 0.9000
- **Test ROC-AUC**: 0.9567

### Q18: What is a Confusion Matrix, and what were the exact confusion matrix counts for our final model?
**Answer**: A confusion matrix tabulates True Negatives (TN), False Positives (FP), False Negatives (FN), and True Positives (TP). For our 61-row test set:
- $\text{TN} = 28$, $\text{FP} = 5$, $\text{FN} = 1$, $\text{TP} = 27$.

---

## Section 6: Deep Learning (ANN) Integration

### Q19: What Deep Learning architecture was implemented in Part 10?
**Answer**: We implemented a feed-forward Artificial Neural Network (Multi-Layer Perceptron) using Keras (with PyTorch backend). The winning architecture (**ANN-3**) consists of: `28 -> 64 (ReLU, Dropout 0.3) -> 32 (ReLU, Dropout 0.2) -> 16 (ReLU, Dropout 0.1) -> 1 (Sigmoid)`.

### Q20: How was the ANN trained and evaluated without test set leakage?
**Answer**: Candidate architectures were evaluated on an internal 80/20 train/validation split of the 242 training rows (~193 train / ~49 validation). The 61-row test set remained completely locked until after the winning ANN architecture was selected and frozen to `frozen_ann_configuration.json`.

---

## Section 7: Literature Survey & Research Gap Analysis (Part 11)

### Q21: Why did you select these specific 16 literature survey papers?
**Answer**: Papers were selected from reputable academic databases (IEEE Xplore, ScienceDirect/Elsevier, Springer Nature, PubMed, Hindawi, MDPI) based on strict criteria: direct relevance to tabular cardiovascular risk prediction, clear identification of datasets, reproducible methodology, verifiable metadata, and valid DOIs.

### Q22: What is the fundamental difference between ML and DL approaches in the literature?
**Answer**: Machine Learning methods (e.g., Random Forest, SVM, Logistic Regression) rely on explicit tabular features and tree/hyperplane decision boundaries, whereas Deep Learning methods (e.g., ANNs, Autoencoders, CNNs) attempt to learn hierarchical feature representations automatically through multi-layer non-linear transformations.

### Q23: What datasets were most commonly used across the reviewed literature?
**Answer**: The **UCI Cleveland Heart Disease dataset** (303 patient records) was the most prominent benchmark across published literature, followed by the UCI Framingham and Statlog heart disease datasets.

### Q24: What algorithms were most commonly evaluated in published studies?
**Answer**: 
- **Machine Learning**: Random Forest, Support Vector Machines (SVM), Logistic Regression, Naive Bayes, and Hybrid Feature-Selection Ensembles (mRMR, Genetic Algorithms).
- **Deep Learning**: Multi-Layer Perceptrons (ANNs), Sparse Autoencoders (SAE-ANN), 1D/2D Convolutional Neural Networks (CNNs), and Deep Boltzmann Machines (DBMs).

### Q25: What common methodological limitations were observed across the reviewed literature?
**Answer**: 
1. **Small Tabular Sample Constraints**: Over-reliance on small (~300 row) repositories limits deep learning network optimization.
2. **Single-Dataset Evaluation**: Lack of cross-hospital prospective validation on independent cohorts.
3. **Lack of Model Explainability**: Deep neural networks function as opaque black-box predictors without feature importance rationale.
4. **Absence of Interactive Deployment**: Most literature focuses on static paper metrics without deploying functional user interfaces.

### Q26: What specific research gaps did your capstone project address?
**Answer**: Our project addressed: (1) strict leakage-free multi-model benchmarking comparing ML and DL on a locked held-out test set, (2) prioritization of Recall (Sensitivity) to minimize medical False Negatives, (3) transformed feature importance interpretability, and (4) practical interactive software deployment via a Streamlit web app (`app.py`).

### Q27: Why did you choose the UCI Cleveland Heart Disease dataset for this study?
**Answer**: The UCI Cleveland dataset provides clinically validated diagnostic attributes collected by medical experts, establishing a standardized academic benchmark for fair multi-model comparison across literature.

### Q28: Why did you compare Random Forest against an Artificial Neural Network (ANN)?
**Answer**: Random Forest represents the state-of-the-art in ensemble machine learning for tabular data, while ANN represents the core deep learning architecture. Comparing both evaluates whether deep representation learning offers genuine diagnostic advantage over tree ensembles on tabular medical data.

### Q29: Why is Recall (Sensitivity) the most critical evaluation metric for heart disease prediction?
**Answer**: In clinical risk scoring, a False Negative (falsely diagnosing a diseased patient as healthy) carries severe medical risk, whereas a False Positive simply prompts secondary clinical follow-up. High Recall ensures almost all at-risk patients are correctly identified (our models detected 27 out of 28 disease cases, achieving 96.43% recall).

### Q30: Why did the Tuned Random Forest outperform the Artificial Neural Network on this dataset?
**Answer**: Tabular medical datasets with small sample sizes (303 records) inherently favor decision tree ensembles due to structural inductive bias. Random Forest effectively partitions low-sample feature space without requiring large data volumes to optimize deep neural network parameters.
