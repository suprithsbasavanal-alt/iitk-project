# Literature-to-Project Mapping Document

This document maps findings from the 16 reviewed literature survey papers to the specific design, implementation, and evaluation choices executed in our Heart Disease Prediction Capstone Project.

---

## 1. Project Implementation Mapping Matrix

| Capstone Implementation Choice | Supporting Literature Evidence | Synthesis & Rationale |
| :--- | :--- | :--- |
| **Dataset Selection**<br>`UCI Cleveland Heart Disease` (303 rows, 13 features) | Detrano et al. (1989), Palaniappan & Awang (2008), Anooj (2012), Haq et al. (2018), Mohan et al. (2019), Alotaibi (2019) | The UCI Cleveland Heart Disease dataset is established in the literature as the premier benchmark for cardiovascular disease prediction, offering clinically validated diagnostic targets and features. |
| **Data Preprocessing & Scaling**<br>`StandardScaler` & `OneHotEncoder` | Haq et al. (2018), Gokulnath & Shantharajah (2019), Dissanayake & Johar (2021) | Literature demonstrates that scaling continuous physiological features (e.g., blood pressure, cholesterol, max heart rate) and encoding categorical variables prevents gradient dominance and improves convergence across distance-based and neural classifiers. |
| **Exploratory Data Analysis (EDA)**<br>Distribution & Correlation Analysis | Detrano et al. (1989), Palaniappan & Awang (2008) | Early literature identifies chest pain type (`cp`), maximum heart rate (`thalach`), ST depression (`oldpeak`), and major vessels (`ca`) as pivotal diagnostic markers, validating our EDA bivariate and multivariate findings. |
| **Logistic Regression Classifier** | Detrano et al. (1989), Haq et al. (2018), Dissanayake & Johar (2021) | Literature shows Logistic Regression serves as a strong linear probabilistic baseline for binary medical diagnosis, providing calibrated probability estimates. |
| **Random Forest Classifier**<br>(Selected Final ML Model) | Mohan et al. (2019), Latha & Jeeva (2019), Haq et al. (2018) | Studies consistently prove that Random Forest ensembling outperforms single decision trees and linear models on tabular medical data by mitigating variance and handling feature interaction non-linearities. |
| **Support Vector Machine (SVM)** | Gokulnath & Shantharajah (2019), Haq et al. (2018) | Literature highlights SVM's effectiveness in finding optimal high-dimensional decision hyperplanes for small sample sizes, justifying its inclusion in our baseline and hyperparameter tuning stages. |
| **K-Nearest Neighbors (KNN)** | Palaniappan & Awang (2008), Dissanayake & Johar (2021) | Studies demonstrate KNN's utility as an intuitive instance-based baseline classifier for clinical similarity matching. |
| **XGBoost Classifier** | Latha & Jeeva (2019), Sarra et al. (2022) | Literature confirms gradient boosting techniques (XGBoost) provide robust regularized decision trees for tabular classification. |
| **Artificial Neural Network (ANN)**<br>(Part 10 Deep Learning) | Mienye et al. (2020), Alotaibi (2019), Pan et al. (2020), Sarra et al. (2022) | Research demonstrates that multi-layer perceptrons (ANNs) capture complex non-linear feature interactions without explicit feature engineering, motivating our Part 10 Keras ANN architecture. |
| **Evaluation Metrics**<br>`Recall (Sensitivity)` & `ROC-AUC` | Dissanayake & Johar (2021), Mohan et al. (2019), Ali et al. (2020) | Medical diagnostic literature emphasizes that minimizing False Negatives (maximizing Recall) and evaluating threshold-invariant discrimination (ROC-AUC) are vital for patient safety in cardiovascular risk prediction. |
| **Feature Importance Analysis** | Mohan et al. (2019), Haq et al. (2018), Gokulnath & Shantharajah (2019) | Published studies highlight that ranking feature importance provides clinical interpretability, verifying that our model's top predictors align with established medical knowledge. |
| **ML vs DL Benchmark Comparison** | Alotaibi (2019), Dissanayake & Johar (2021), Sarra et al. (2022) | Comparative studies show that while ANNs achieve high diagnostic recall, ensemble tree models (Random Forest) maintain equal or superior accuracy on small tabular medical datasets (~300 rows). |
| **Streamlit Web Application** | Palaniappan & Awang (2008), Ali et al. (2020) | Literature supports deploying predictive decision support systems into accessible web interfaces to facilitate clinical interaction and real-time risk assessment. |

---

## 2. Conclusion

The 16 reviewed publications directly justify every stage of our capstone project pipeline. The literature confirms that our data preprocessor design, multi-model evaluation, hyperparameter tuning grid, Random Forest selection, Part 10 ANN architecture, recall-oriented evaluation metrics, and Streamlit deployment reflect state-of-the-art methodology in machine learning and deep learning for heart disease prediction.
