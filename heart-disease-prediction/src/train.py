"""
Model Training and Central Registry Module for Heart Disease Prediction.

This module provides the central baseline model registry (7 classifiers), pipeline construction,
and Stratified 5-Fold Cross-Validation functions operating on raw training data without data leakage.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Union, Any
import numpy as np
import pandas as pd
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.preprocessing import build_preprocessor, get_feature_groups


def get_baseline_models() -> Dict[str, Any]:
    """
    Central Baseline Model Registry returning 7 un-tuned classification algorithms.

    Returns:
        Dict[str, Any]: Dictionary mapping model names to classifier instances.
    """
    models = {
        "Logistic Regression": LogisticRegression(max_iter=2000, random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42),
        "Support Vector Machine": SVC(probability=True, random_state=42),
        "Gaussian Naive Bayes": GaussianNB(),
        "XGBoost": XGBClassifier(random_state=42, eval_metric="logloss"),
    }
    return models


def get_file_safe_name(model_name: str) -> str:
    """
    Convert human-readable model name to filesystem-safe string.

    Args:
        model_name (str): Human-readable model name (e.g., "Logistic Regression").

    Returns:
        str: Filesystem-safe name (e.g., "logistic_regression").
    """
    return model_name.lower().replace(" ", "_").replace("-", "_")


def build_baseline_pipeline(classifier: Any) -> Pipeline:
    """
    Construct an end-to-end scikit-learn Pipeline with preprocessor and classifier.

    Args:
        classifier (Any): Scikit-learn or XGBoost classifier object.

    Returns:
        Pipeline: End-to-end processing and prediction pipeline.
    """
    num_features, cat_features = get_feature_groups()
    preprocessor = build_preprocessor(num_features, cat_features)

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", classifier)
    ])

    return pipeline


def evaluate_cv_baseline(
    models_dict: Dict[str, Any],
    X_train_raw: pd.DataFrame,
    y_train: pd.Series,
    n_splits: int = 5,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Perform 5-Fold Stratified Cross-Validation on raw training data using full pipelines.

    Args:
        models_dict: Map of model_name -> classifier.
        X_train_raw: Raw training features DataFrame (242 rows).
        y_train: Binary training target Series.
        n_splits: Number of CV folds. Defaults to 5.
        random_state: Seed for StratifiedKFold. Defaults to 42.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: (cv_summary_df, cv_fold_details_df)
    """
    cv_strategy = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]

    summary_rows = []
    fold_rows = []

    for model_name, classifier in models_dict.items():
        # Build fresh pipeline for each model CV run
        pipeline = build_baseline_pipeline(classifier)

        # Run cross_validate
        scores = cross_validate(
            pipeline,
            X_train_raw,
            y_train,
            cv=cv_strategy,
            scoring=scoring,
            return_train_score=False,
        )

        # Record fold-level metrics (5 folds per model = 35 total rows)
        for fold_idx in range(n_splits):
            fold_rows.append({
                "model": model_name,
                "fold": fold_idx + 1,
                "accuracy": float(scores["test_accuracy"][fold_idx]),
                "precision": float(scores["test_precision"][fold_idx]),
                "recall": float(scores["test_recall"][fold_idx]),
                "f1": float(scores["test_f1"][fold_idx]),
                "roc_auc": float(scores["test_roc_auc"][fold_idx]),
            })

        # Record mean ± std metrics summary
        summary_rows.append({
            "Model": model_name,
            "CV_Accuracy_Mean": float(scores["test_accuracy"].mean()),
            "CV_Accuracy_Std": float(scores["test_accuracy"].std()),
            "CV_Precision_Mean": float(scores["test_precision"].mean()),
            "CV_Precision_Std": float(scores["test_precision"].std()),
            "CV_Recall_Mean": float(scores["test_recall"].mean()),
            "CV_Recall_Std": float(scores["test_recall"].std()),
            "CV_F1_Mean": float(scores["test_f1"].mean()),
            "CV_F1_Std": float(scores["test_f1"].std()),
            "CV_ROC_AUC_Mean": float(scores["test_roc_auc"].mean()),
            "CV_ROC_AUC_Std": float(scores["test_roc_auc"].std()),
        })

    cv_summary_df = pd.DataFrame(summary_rows)
    cv_fold_details_df = pd.DataFrame(fold_rows)

    return cv_summary_df, cv_fold_details_df
