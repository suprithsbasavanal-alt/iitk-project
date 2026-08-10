# Capstone Viva Examination: Questions and Answers (Part 9)

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
- $	ext{TN} = 28$, $	ext{FP} = 5$, $	ext{FN} = 1$, $	ext{TP} = 27$.

### Q19: What is the clinical significance of a low False Negative (FN) count?
**Answer**: In medical risk screening, a False Negative represents a patient with heart disease who is incorrectly flagged as healthy. Minimizing FN (only 1 out of 28 in our test set) ensures high sensitivity and minimizes dangerous missed diagnoses.

### Q20: What is ROC-AUC, and what was the ROC-AUC score of our final model?
**Answer**: Receiver Operating Characteristic Area Under Curve (ROC-AUC) measures the model's ability to discriminate between positive and negative classes across all classification thresholds. Our final model achieved a Test ROC-AUC of **0.9567**.

### Q21: Which model had the highest Test ROC-AUC, and why wasn't it selected based on ROC-AUC alone?
**Answer**: Tuned KNN had a slightly higher Test ROC-AUC (0.9621 vs 0.9567), but Tuned Random Forest was selected because it achieved higher Test Accuracy (90.16% vs 88.52%), higher Test Recall (96.43% vs 89.29%), higher F1-Score (0.9000 vs 0.8772), and fewer False Negatives (1 vs 3).

---

## Section 6: Feature Importance & Interpretability

### Q22: How is feature importance calculated in Random Forest?
**Answer**: It is calculated using Gini Importance (mean decrease in impurity), which measures how much each feature split reduces node impurity across all 500 decision trees.

### Q23: What were the top 5 clinical feature drivers in our final model?
**Answer**: 
1. `thalach` (Maximum Heart Rate Achieved): 11.97%
2. `oldpeak` (ST Depression): 10.98%
3. `cp_4.0` (Asymptomatic Chest Pain): 9.84%
4. `ca_0.0` (Zero Major Vessels Colored): 8.12%
5. `thal_7.0` (Reversible Defect Thalassemia): 7.65%

### Q24: Does high feature importance imply medical causation?
**Answer**: No. Feature importance measures how heavily the mathematical decision tree ensemble relies on a variable for statistical prediction; it does not prove medical causation.

---

## Section 7: Web Application & Deployment (Streamlit)

### Q25: What framework was used to build the web application, and how is it executed?
**Answer**: Streamlit (`app.py`). It is launched locally using `streamlit run app.py`.

### Q26: Does the Streamlit application perform any model training when launched?
**Answer**: No. The app loads the pre-fitted frozen pipeline (`final_model.joblib`) using `@st.cache_resource` for instant, zero-training inference.

### Q27: How does the application handle input validation and error prevention?
**Answer**: It enforces input schema checks via `src.predict.validate_input_data()`, restricts categorical fields to valid UCI categories via selectboxes, and displays user-friendly warning messages instead of Python tracebacks.

### Q28: What disclaimer is displayed on the application?
**Answer**: "This application is an educational/research demonstration created for a college capstone project. It is not a clinically validated medical diagnostic system and should not be used for medical decision-making."

---

## Section 8: Limitations & Future Scope

### Q29: What are the primary dataset limitations of this project?
**Answer**: Small sample size (303 total rows, 61 test rows), single-center geographic collection (Cleveland subset), and historical collection timeframe (1988).

### Q30: What is the status of Deep Learning in this repository?
**Answer**: Parts 1–8 established the complete Machine Learning baseline and web application. Deep Learning (ANN/MLP) models are documented as future scope and have not yet been trained.

### Q31: What future enhancements are proposed for this capstone project?
**Answer**: External validation on multi-center datasets, probability calibration, threshold optimization, SHAP/LIME explainability, fairness audits, and Deep Learning neural network benchmarks.

---

## Section 9: General Engineering & Coding Best Practices

### Q32: Why did we persist the complete pipeline (`preprocessor + classifier`) rather than saving them separately?
**Answer**: Saving the unified `Pipeline` object guarantees that raw user inputs undergo identical transformation steps during inference without risking manual feature misalignment or data leakage.

### Q33: How were unit tests used to verify code quality?
**Answer**: We wrote unit tests in `tests/` covering preprocessing, training, evaluation, tuning, final model selection, and app integration. All 26 unit tests pass 100%.

### Q34: What is the purpose of `verify_application.py` and other verification scripts?
**Answer**: Verification scripts perform automated sanity checks on dataset rows, file sizes, metric ranges, artifact immutability, and reproducibility.

### Q35: What is Stratified K-Fold Cross-Validation, and why is it essential for small datasets?
**Answer**: Stratified K-Fold ensures that each fold maintains the same target class proportions as the overall training set, preventing class distribution distortion in small samples.

### Q36: What is the difference between Precision and Recall?
**Answer**: Precision measures the percentage of positive predictions that are actually positive ($TP / [TP + FP]$). Recall measures the percentage of actual positive cases correctly identified ($TP / [TP + FN]$).

### Q37: Why is F1-Score useful when evaluating classifiers?
**Answer**: F1-Score is the harmonic mean of Precision and Recall ($2 \cdot rac{P \cdot R}{P + R}$), providing a single score that penalizes extreme trade-offs between precision and recall.

### Q38: What does `random_state=42` ensure across the codebase?
**Answer**: Setting a fixed random seed ensures 100% deterministic reproducibility across train/test splits, cross-validation folds, randomized searches, and random forest tree generation.

### Q39: What is one-hot encoding, and why is `handle_unknown="ignore"` used?
**Answer**: One-hot encoding creates binary indicator columns for categorical variables. `handle_unknown="ignore"` ensures that if an unseen category is encountered during inference, the pipeline sets all indicators to zero without crashing.

### Q40: What is the function of `StandardScaler`?
**Answer**: It standardizes features by subtracting the mean and scaling to unit variance ($z = rac{x - \mu}{\sigma}$), ensuring features with large numerical scales (e.g., cholesterol) do not dominate distance-based algorithms like KNN or SVM.

### Q41: Why did we choose `balanced_subsample` for `class_weight` in Random Forest?
**Answer**: It automatically adjusts tree weights inversely proportional to class frequencies in the bootstrap sample of each tree, helping the ensemble handle mild target imbalance and boosting recall for the positive class.

### Q42: Can this model be deployed directly in a hospital setting?
**Answer**: No. It is an academic capstone demonstration. Clinical deployment requires rigorous multi-center clinical trials, regulatory approvals (e.g., FDA/CE clearance), and integration with Electronic Health Record (EHR) infrastructure.
