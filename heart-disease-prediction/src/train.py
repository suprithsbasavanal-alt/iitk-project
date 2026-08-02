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
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold, cross_validate
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


def get_tuning_search_spaces() -> Dict[str, Tuple[Any, Any, str]]:
    """
    Define hyperparameter search spaces and methods for 5 target models.

    Returns:
        Dict[str, Tuple[Any, Any, str]]: Map of model_name -> (classifier_instance, param_space, search_method)
    """
    spaces = {}

    # 1. Logistic Regression (GridSearchCV)
    log_reg_cls = LogisticRegression(random_state=42)
    log_reg_param_grid = [
        {
            "classifier__penalty": ["l2"],
            "classifier__C": [0.001, 0.01, 0.1, 1, 10, 100],
            "classifier__solver": ["lbfgs"],
            "classifier__max_iter": [5000],
            "classifier__class_weight": [None, "balanced"],
        },
        {
            "classifier__penalty": ["l1", "l2"],
            "classifier__C": [0.001, 0.01, 0.1, 1, 10, 100],
            "classifier__solver": ["liblinear"],
            "classifier__class_weight": [None, "balanced"],
        },
    ]
    spaces["Logistic Regression"] = (log_reg_cls, log_reg_param_grid, "grid")

    # 2. Support Vector Machine (GridSearchCV)
    svm_cls = SVC(probability=True, random_state=42)
    svm_param_grid = [
        {
            "classifier__kernel": ["linear"],
            "classifier__C": [0.01, 0.1, 1, 10, 100],
            "classifier__class_weight": [None, "balanced"],
        },
        {
            "classifier__kernel": ["rbf"],
            "classifier__C": [0.01, 0.1, 1, 10, 100],
            "classifier__gamma": ["scale", "auto", 0.001, 0.01, 0.1, 1],
            "classifier__class_weight": [None, "balanced"],
        },
    ]
    spaces["Support Vector Machine"] = (svm_cls, svm_param_grid, "grid")

    # 3. Random Forest (RandomizedSearchCV)
    rf_cls = RandomForestClassifier(random_state=42)
    rf_param_dist = {
        "classifier__n_estimators": [100, 200, 300, 500, 700],
        "classifier__max_depth": [None, 3, 5, 7, 10, 15],
        "classifier__min_samples_split": [2, 4, 6, 8, 10],
        "classifier__min_samples_leaf": [1, 2, 3, 4, 5],
        "classifier__max_features": ["sqrt", "log2", None],
        "classifier__class_weight": [None, "balanced", "balanced_subsample"],
    }
    spaces["Random Forest"] = (rf_cls, rf_param_dist, "random")

    # 4. XGBoost (RandomizedSearchCV)
    xgb_cls = XGBClassifier(random_state=42, eval_metric="logloss")
    xgb_param_dist = {
        "classifier__n_estimators": [50, 100, 150, 200, 300, 500],
        "classifier__max_depth": [2, 3, 4, 5, 6],
        "classifier__learning_rate": [0.01, 0.03, 0.05, 0.1, 0.2],
        "classifier__subsample": [0.6, 0.7, 0.8, 0.9, 1.0],
        "classifier__colsample_bytree": [0.6, 0.7, 0.8, 0.9, 1.0],
        "classifier__min_child_weight": [1, 3, 5, 7],
        "classifier__reg_alpha": [0, 0.01, 0.1, 1],
        "classifier__reg_lambda": [0.1, 1, 5, 10],
    }
    spaces["XGBoost"] = (xgb_cls, xgb_param_dist, "random")

    # 5. K-Nearest Neighbors (GridSearchCV)
    knn_cls = KNeighborsClassifier()
    knn_param_grid = {
        "classifier__n_neighbors": [3, 5, 7, 9, 11, 13, 15, 17, 19],
        "classifier__weights": ["uniform", "distance"],
        "classifier__metric": ["euclidean", "manhattan", "minkowski"],
        "classifier__p": [1, 2],
    }
    spaces["K-Nearest Neighbors"] = (knn_cls, knn_param_grid, "grid")

    return spaces


def build_search_object(
    model_name: str,
    classifier: Any,
    param_space: Any,
    search_method: str = "grid",
    n_iter: int = 60,
    random_state: int = 42,
) -> Union[GridSearchCV, RandomizedSearchCV]:
    """
    Construct a scikit-learn GridSearchCV or RandomizedSearchCV search object over the full pipeline.

    Args:
        model_name: Human-readable model name.
        classifier: Base classifier instance.
        param_space: Parameter grid or distribution map.
        search_method: "grid" for GridSearchCV, "random" for RandomizedSearchCV.
        n_iter: Iterations count for RandomizedSearchCV.
        random_state: Random state seed.

    Returns:
        Union[GridSearchCV, RandomizedSearchCV]: Configured search object.
    """
    pipeline = build_baseline_pipeline(classifier)
    cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

    if search_method == "grid":
        search = GridSearchCV(
            estimator=pipeline,
            param_grid=param_space,
            scoring="roc_auc",
            cv=cv_strategy,
            refit=True,
            n_jobs=-1,
        )
    elif search_method == "random":
        search = RandomizedSearchCV(
            estimator=pipeline,
            param_distributions=param_space,
            n_iter=n_iter,
            scoring="roc_auc",
            cv=cv_strategy,
            refit=True,
            random_state=random_state,
            n_jobs=-1,
        )
    else:
        raise ValueError(f"Unknown search_method: {search_method}")

    return search


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
