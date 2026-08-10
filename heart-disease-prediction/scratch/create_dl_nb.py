"""
Script to create and execute notebooks/05_deep_learning_ann.ipynb with 17 sections.
"""

from pathlib import Path
import json
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

repo_dir = Path("/Users/suprith.s.basavanal/Documents/antigrativity /iitk-project/heart-disease-prediction")
nb_path = repo_dir / "notebooks" / "05_deep_learning_ann.ipynb"

nb = nbf.v4.new_notebook()

cells = [
    # 1. Title & Objective
    nbf.v4.new_markdown_cell("""# Notebook 05: Deep Learning — Artificial Neural Network (ANN / MLP)

**Project Title**: Heart Disease Prediction Using Machine Learning and Deep Learning Techniques  
**Part 10**: Deep Learning Model Implementation, Architecture Selection, and ML vs DL Benchmarking  

### 1. Objective
The objective of this notebook is to implement, optimize, evaluate, and benchmark a genuine feed-forward Artificial Neural Network (ANN / Multi-Layer Perceptron) using Keras (with PyTorch backend) for predicting heart disease risk, and fairly compare its performance against the frozen Tuned Random Forest machine learning model on the exact same 61-row held-out test split.
"""),

    # 2. Imports & Setup
    nbf.v4.new_code_cell("""import os
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Enforce PyTorch backend for Keras 3.x
os.environ['KERAS_BACKEND'] = 'torch'
import keras
import torch

# Ensure project root is on sys.path
PROJECT_ROOT = Path('.').resolve().parent if Path('.').resolve().name == 'notebooks' else Path('.').resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.deep_learning import (
    build_ann_model,
    build_candidate_architectures,
    train_ann,
    evaluate_ann,
    save_ann_model,
    load_ann_model,
    predict_ann
)

print(f"Keras Version: {keras.__version__}")
print(f"PyTorch Version: {torch.__version__}")
"""),

    # 3. Dataset & Preprocessing Strategy
    nbf.v4.new_markdown_cell("""### 2. Dataset & Preprocessing Overview
We load the preprocessed training (242 rows) and testing (61 rows) datasets generated in Part 3. The 13 original predictor variables were transformed into 28 numeric features using median/mode imputation, `StandardScaler`, and `OneHotEncoder`.
"""),
    nbf.v4.new_code_cell("""X_train_df = pd.read_csv(PROJECT_ROOT / 'data' / 'processed' / 'X_train_preprocessed.csv')
X_test_df = pd.read_csv(PROJECT_ROOT / 'data' / 'processed' / 'X_test_preprocessed.csv')
y_train_df = pd.read_csv(PROJECT_ROOT / 'data' / 'processed' / 'y_train.csv')
y_test_df = pd.read_csv(PROJECT_ROOT / 'data' / 'processed' / 'y_test.csv')

X_train_full = X_train_df.values.astype(np.float32)
X_test_full = X_test_df.values.astype(np.float32)
y_train_full = y_train_df['target'].values.astype(int)
y_test_full = y_test_df['target'].values.astype(int)

print(f"Preprocessed Training Set: {X_train_full.shape}")
print(f"Preprocessed Held-Out Test Set: {X_test_full.shape}")
"""),

    # 4. Train / Validation / Test Strategy
    nbf.v4.new_markdown_cell("""### 3. Train / Validation / Test Strategy & Leakage Prevention
To prevent data leakage, the 61-row test set is **completely locked**. All model architecture choices, hyperparameter selections, and early stopping decisions are conducted strictly using an internal stratified validation split (80% train subset = 193 rows, 20% validation subset = 49 rows) derived from the 242 training rows.
"""),
    nbf.v4.new_code_cell("""from sklearn.model_selection import train_test_split

X_train_sub, X_val, y_train_sub, y_val = train_test_split(
    X_train_full,
    y_train_full,
    test_size=0.20,
    stratify=y_train_full,
    random_state=42
)

print(f"Training Subset: {X_train_sub.shape[0]} rows")
print(f"Validation Subset: {X_val.shape[0]} rows")
print("Test Set (61 rows): LOCKED")
"""),

    # 5. Candidate Architecture Search
    nbf.v4.new_markdown_cell("""### 4. Candidate Architecture Evaluation
We evaluate three candidate feed-forward ANN architectures on the validation subset:
- **ANN-1**: 28 -> 32 (ReLU, Dropout 0.2) -> 16 (ReLU, Dropout 0.1) -> 1 (Sigmoid)
- **ANN-2**: 28 -> 64 (ReLU, Dropout 0.3) -> 32 (ReLU, Dropout 0.2) -> 1 (Sigmoid)
- **ANN-3**: 28 -> 64 (ReLU, Dropout 0.3) -> 32 (ReLU, Dropout 0.2) -> 16 (ReLU, Dropout 0.1) -> 1 (Sigmoid)
"""),
    nbf.v4.new_code_cell("""cand_df = pd.read_csv(PROJECT_ROOT / 'results' / 'metrics' / 'deep_learning' / 'architecture_comparison.csv')
cand_df
"""),

    # 6. Architecture Selection & Freezing
    nbf.v4.new_markdown_cell("""### 5. Winning Architecture Selection & Configuration Freezing
Based on Validation ROC-AUC (0.9327), **ANN-3** was selected as the winning architecture. Its configuration was frozen into `frozen_ann_configuration.json` **before** inspecting test set metrics.
"""),
    nbf.v4.new_code_cell("""with open(PROJECT_ROOT / 'results' / 'metrics' / 'deep_learning' / 'frozen_ann_configuration.json', 'r') as f:
    config = json.load(f)

for k, v in config.items():
    print(f"{k}: {v}")
"""),

    # 7. Final ANN Training
    nbf.v4.new_markdown_cell("""### 6. Final ANN Model Training & History
We train the final frozen ANN-3 model on the training dataset using Adam (`lr=0.001`), `EarlyStopping(patience=15)`, and `ReduceLROnPlateau(patience=7)`.
"""),
    nbf.v4.new_code_cell("""hist_df = pd.read_csv(PROJECT_ROOT / 'results' / 'metrics' / 'deep_learning' / 'ann_training_history.csv')
hist_df.head(10)
"""),

    # 8. Training & Validation Loss/Accuracy Curves
    nbf.v4.new_markdown_cell("""### 7. Training and Validation Performance Curves
Below are the loss and accuracy curves plotted across training epochs.
"""),
    nbf.v4.new_code_cell("""fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(hist_df['epoch'], hist_df['loss'], label='Training Loss', color='#1B365D', lw=2)
ax1.plot(hist_df['epoch'], hist_df['val_loss'], label='Validation Loss', color='#D9534F', lw=2, linestyle='--')
ax1.set_title('ANN Loss Curves', fontsize=12, fontweight='bold')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Binary Cross-Entropy')
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend()

ax2.plot(hist_df['epoch'], hist_df['accuracy'], label='Training Accuracy', color='#1B365D', lw=2)
ax2.plot(hist_df['epoch'], hist_df['val_accuracy'], label='Validation Accuracy', color='#2E7D32', lw=2, linestyle='--')
ax2.set_title('ANN Accuracy Curves', fontsize=12, fontweight='bold')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy')
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend()

plt.tight_layout()
plt.show()
"""),

    # 9. Held-Out Test Evaluation
    nbf.v4.new_markdown_cell("""### 8. Final ANN Model Evaluation on Locked Test Set
Now that the configuration was frozen, we load `models/deep_learning/final_ann.keras` and evaluate its performance on the 61 held-out test rows.
"""),
    nbf.v4.new_code_cell("""ann_test_df = pd.read_csv(PROJECT_ROOT / 'results' / 'metrics' / 'deep_learning' / 'ann_test_results.csv')
ann_test_df
"""),

    # 10. Confusion Matrix
    nbf.v4.new_markdown_cell("""### 9. Test Confusion Matrix Analysis
The confusion matrix tabulates True Negatives (TN), False Positives (FP), False Negatives (FN), and True Positives (TP).
"""),
    nbf.v4.new_code_cell("""img_cm = plt.imread(PROJECT_ROOT / 'results' / 'figures' / 'deep_learning' / 'ann_confusion_matrix.png')
plt.figure(figsize=(6, 5))
plt.imshow(img_cm)
plt.axis('off')
plt.title('Final ANN Confusion Matrix (Test Set)', fontsize=12, fontweight='bold')
plt.show()
"""),

    # 11. ROC Curve
    nbf.v4.new_markdown_cell("""### 10. ROC Curve & AUC Score
The Receiver Operating Characteristic (ROC) curve evaluates class separation across all decision thresholds.
"""),
    nbf.v4.new_code_cell("""img_roc = plt.imread(PROJECT_ROOT / 'results' / 'figures' / 'deep_learning' / 'ann_roc_curve.png')
plt.figure(figsize=(7, 5))
plt.imshow(img_roc)
plt.axis('off')
plt.title('Final ANN ROC Curve (Test Set)', fontsize=12, fontweight='bold')
plt.show()
"""),

    # 12. Precision-Recall Curve
    nbf.v4.new_markdown_cell("""### 11. Precision-Recall Curve
The Precision-Recall curve illustrates the trade-off between precision and recall at different probability thresholds.
"""),
    nbf.v4.new_code_cell("""img_pr = plt.imread(PROJECT_ROOT / 'results' / 'figures' / 'deep_learning' / 'ann_precision_recall_curve.png')
plt.figure(figsize=(7, 5))
plt.imshow(img_pr)
plt.axis('off')
plt.title('Final ANN Precision-Recall Curve (Test Set)', fontsize=12, fontweight='bold')
plt.show()
"""),

    # 13. ML vs DL Benchmark Comparison
    nbf.v4.new_markdown_cell("""### 12. Machine Learning vs Deep Learning Benchmark Comparison
We benchmark the **Tuned Random Forest** (ML) against the **Final ANN** (DL) on the exact same 61-row test set.
"""),
    nbf.v4.new_code_cell("""ml_vs_dl_df = pd.read_csv(PROJECT_ROOT / 'results' / 'metrics' / 'ml_vs_dl_comparison.csv')
ml_vs_dl_df
"""),
    nbf.v4.new_code_cell("""img_comp = plt.imread(PROJECT_ROOT / 'results' / 'figures' / 'deep_learning' / 'ml_vs_dl_comparison.png')
plt.figure(figsize=(9, 5))
plt.imshow(img_comp)
plt.axis('off')
plt.title('Machine Learning vs Deep Learning Test Metric Comparison', fontsize=12, fontweight='bold')
plt.show()
"""),

    # 14. Discussion & Limitations
    nbf.v4.new_markdown_cell("""### 13. Discussion & Limitations
1. **Sample Size Constraints**: Deep neural networks typically require thousands of samples to learn complex representation hierarchies. With 303 total records (242 train), tree ensembles (Random Forest) maintain a inductive bias advantage.
2. **Performance Comparison**: Tuned Random Forest achieved higher Test Accuracy (90.16% vs 85.25%) and higher Test ROC-AUC (0.9567 vs 0.9253), while both models achieved identical high Test Recall (96.43%, detecting 27 out of 28 disease cases with only 1 False Negative).
3. **Interpretability**: Random Forest provides built-in feature importance scores, whereas ANNs function as black-box predictors requiring post-hoc explainability tools (e.g., SHAP).
"""),

    # 15. Conclusion
    nbf.v4.new_markdown_cell("""### 14. Conclusion
Part 10 successfully implemented, tuned, frozen, evaluated, and benchmarked a feed-forward Artificial Neural Network (ANN-3). While the ANN demonstrated strong diagnostic capability (85.25% Test Accuracy, 96.43% Test Recall), the Tuned Random Forest remains the overall winning machine learning pipeline for this tabular dataset.
""")
]

nb.cells = cells

with open(nb_path, "w") as f:
    nbf.write(nb, f)

print(f"Created notebook `{nb_path}`. Now executing...")

ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
with open(nb_path) as f:
    nb_to_run = nbf.read(f, as_version=4)

ep.preprocess(nb_to_run, {"metadata": {"path": str(repo_dir / "notebooks")}})

with open(nb_path, "w") as f:
    nbf.write(nb_to_run, f)

print(f"Successfully executed and saved `{nb_path}`.")
