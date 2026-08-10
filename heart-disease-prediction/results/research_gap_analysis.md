# Comprehensive Research Gap Analysis

This document identifies recurring methodological gaps, limitations, and future research opportunities observed across the 16 reviewed literature survey papers in heart disease prediction using Machine Learning (ML) and Deep Learning (DL).

---

## 1. Observed Recurring Methodological Limitations in Literature

Based on our empirical analysis of the 16 reviewed publications (8 Machine Learning, 8 Deep Learning), the following key research gaps recur across published studies:

### 1.1 Limited Dataset Size & Sample Constraints
- **Observed Limitation**: A majority of published benchmark studies (e.g., Detrano et al. 1989, Alotaibi 2019, Mohan et al. 2019, Dissanayake & Johar 2021) rely exclusively on small tabular repositories such as the 303-patient UCI Cleveland dataset.
- **Impact**: Deep learning architectures (e.g., ANNs, 1D/2D-CNNs) require extensive sample sizes to learn hierarchical feature representations. When trained on fewer than 300 rows, deep models risk overfitting or failing to significantly outperform well-regularized tree ensembles (Random Forest).

### 1.2 Single-Dataset Evaluation & Lack of External Validation
- **Observed Limitation**: Studies such as Anooj (2012), Gokulnath & Shantharajah (2019), and Mehmood et al. (2021) evaluate their proposed pipelines on a single hospital dataset without external validation on independent patient cohorts (e.g., Hungarian, Switzerland, or Long Beach subsets).
- **Impact**: Reported accuracy metrics may reflect dataset-specific noise or local clinical practices, limiting cross-institution generalizability.

### 1.3 Lack of Direct Head-to-Head Comparison Between ML and DL
- **Observed Limitation**: Traditional machine learning papers (e.g., Latha & Jeeva 2019, Haq et al. 2018) evaluate only classical classifiers (SVM, Random Forest, KNN), whereas deep learning papers (e.g., Sarra et al. 2022, Pan et al. 2020) evaluate only neural architectures or baseline decision trees without strict leakage-free multi-model benchmarking.
- **Impact**: Researchers and clinicians lack clear empirical guidance on whether deep neural networks justify the added architectural complexity over classical tree ensembles for tabular clinical data.

### 1.4 Limited Explainability & Interpretability
- **Observed Limitation**: Complex deep learning models (e.g., SAE-ANN in Mienye et al. 2020, 2D-CNN in Mehmood et al. 2021, DBM in Al-Makhadmeh & Tolba 2019) function as black-box predictors without offering interpretable feature importance rankings or clinical decision rationale.
- **Impact**: Healthcare practitioners are hesitant to adopt opaque deep learning systems for high-stakes medical diagnosis without transparent risk factor attribution.

### 1.5 Absence of Deployed Interactive Applications
- **Observed Limitation**: Most literature focuses exclusively on offline training and static validation metrics in research papers, omitting practical software deployment or interactive web application interfaces (with the notable exception of early prototypes like Palaniappan & Awang 2008).
- **Impact**: Theoretical predictive models remain inaccessible to medical practitioners for real-time risk assessment or point-of-care demonstration.

---

## 2. Research Opportunities Addressed by Our Capstone Project

Our project directly addresses the identified research gaps through the following implementation choices:

| Identified Research Gap | How Our Capstone Project Addresses It |
| :--- | :--- |
| **Lack of Rigorous ML vs DL Head-to-Head Benchmark** | We conducted a strict, leak-free comparison between **Tuned Random Forest (ML)** and **Final ANN (DL)** on the exact same 61-row held-out test set (`X_test_preprocessed.csv`). |
| **Data Leakage & Test Set Over-Tuning** | We locked the 61-row test set during all hyperparameter tuning and candidate architecture selection, utilizing internal stratified 5-fold cross-validation for ML and internal 80/20 train/validation splits for DL. |
| **Lack of Model Interpretability** | We extracted and visualized transformed feature importance rankings (`results/final_feature_importance.csv`), identifying key diagnostic predictors such as `chest_pain_type_4`, `thalach`, `oldpeak`, and `ca`. |
| **Absence of Practical Deployment** | We built and deployed an interactive, user-friendly **Streamlit web application** (`app.py`) featuring real-time input schema validation, dual ML/DL model engines, risk probability scoring, and educational disclaimers. |
| **Clinical Metric Focus (Recall / Sensitivity)** | Rather than relying solely on accuracy, we prioritized **Recall (Sensitivity)** and **ROC-AUC** to minimize False Negatives in heart disease detection (achieving 96.43% test recall, FN=1). |

---

## 3. Summary & Conclusion

The literature survey confirms that while deep learning techniques offer advanced representation capabilities, classical ensemble machine learning algorithms (specifically Random Forest) remain highly competitive and superior for small tabular clinical datasets. By addressing leakage prevention, multi-model benchmarking, interpretability, and interactive deployment, our capstone project bridges the gap between theoretical algorithmic research and practical clinical application.
