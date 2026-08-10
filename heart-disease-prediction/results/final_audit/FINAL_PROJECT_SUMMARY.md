# Final Capstone Project Summary (Part 12)

**Project Title**: Heart Disease Prediction Using Machine Learning and Deep Learning Techniques  
**Team Members**: Shreyas, Uday, Suprith, Sahitya  
**Department**: Computer Science & Engineering  

### Key Specifications & Outcomes
- **Dataset**: UCI Heart Disease Dataset (Cleveland Subset, 303 observations, 13 predictors).
- **Train/Test Split**: 242 train rows (80%), 61 held-out test rows (20%), random_state=42.
- **Preprocessing**: Leakage-free median/mode imputation, `StandardScaler`, and `OneHotEncoder` (28 features).
- **Winning ML Model**: Tuned Random Forest (Test Accuracy: **90.16%**, Recall: **96.43%**, F1: **90.00%**, ROC-AUC: **0.9567**, FN=1).
- **Final DL Model**: Keras ANN-3 (Test Accuracy: **85.25%**, Recall: **96.43%**, F1: **87.10%**, ROC-AUC: **0.9253**, FN=1).
- **ML vs DL Conclusion**: Tuned Random Forest achieved higher overall accuracy and specificity on tabular data, while both models achieved identical top sensitivity (96.43% recall).
- **Literature Survey**: 16 peer-reviewed papers (8 ML, 8 DL) verified with official DOIs.
- **Web Application**: Streamlit app (`app.py`) featuring dual ML/DL engines, input validation, risk scoring, and disclaimers.
