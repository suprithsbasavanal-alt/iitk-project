"""
Model Evaluation and Visualization Module for Heart Disease Prediction.

This module provides reusable utilities for calculating metrics (Accuracy, Precision,
Recall, Specificity, F1, ROC-AUC, Confusion Matrix parameters), exporting classification
reports, and plotting confusion matrices, combined ROC curves, and model comparison charts.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


def calculate_specificity(y_true: Union[pd.Series, np.ndarray], y_pred: Union[pd.Series, np.ndarray]) -> float:
    """
    Calculate Specificity (True Negative Rate): TN / (TN + FP).

    Args:
        y_true: Ground truth binary labels.
        y_pred: Predicted binary labels.

    Returns:
        float: Specificity score.
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0


def calculate_metrics(
    y_true: Union[pd.Series, np.ndarray],
    y_pred: Union[pd.Series, np.ndarray],
    y_prob: Optional[Union[pd.Series, np.ndarray]] = None,
) -> Dict[str, Any]:
    """
    Calculate comprehensive binary classification performance metrics.

    Args:
        y_true: Ground truth binary labels (0 = No Disease, 1 = Disease Present).
        y_pred: Predicted binary labels.
        y_prob: Predicted probabilities for positive class 1.

    Returns:
        Dict[str, Any]: Dictionary of metric values.
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))
    spec = float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0
    f1 = float(f1_score(y_true, y_pred, zero_division=0))

    roc_auc = float(roc_auc_score(y_true, y_prob)) if y_prob is not None else 0.0

    return {
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "Specificity": spec,
        "F1": f1,
        "ROC_AUC": roc_auc,
        "TN": int(tn),
        "FP": int(fp),
        "FN": int(fn),
        "TP": int(tp),
    }


def generate_classification_reports(
    y_true: Union[pd.Series, np.ndarray],
    predictions_dict: Dict[str, Tuple[np.ndarray, np.ndarray]],
    output_dir: Path,
) -> List[Path]:
    """
    Export classification text reports for each model.

    Args:
        y_true: Ground truth binary labels.
        predictions_dict: Map of model_name -> (y_pred, y_prob).
        output_dir: Destination directory.

    Returns:
        List[Path]: Paths to created report files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    report_paths = []

    target_names = ["Class 0: No Heart Disease", "Class 1: Heart Disease Present"]

    for model_name, (y_pred, _) in predictions_dict.items():
        safe_name = model_name.lower().replace(" ", "_").replace("-", "_")
        report_str = f"Classification Report — {model_name}\n"
        report_str += "=" * 50 + "\n\n"
        report_str += classification_report(y_true, y_pred, target_names=target_names, digits=4)

        report_path = output_dir / f"{safe_name}.txt"
        with open(report_path, "w") as f:
            f.write(report_str)

        report_paths.append(report_path)

    return report_paths


def plot_confusion_matrix(
    y_true: Union[pd.Series, np.ndarray],
    y_pred: Union[pd.Series, np.ndarray],
    model_name: str,
    save_path: Path,
) -> Path:
    """
    Generate and save a 300-DPI confusion matrix figure.

    Args:
        y_true: Ground truth binary labels.
        y_pred: Predicted binary labels.
        model_name: Name of model for title.
        save_path: Output file destination path.

    Returns:
        Path: Path to saved figure.
    """
    save_path.parent.mkdir(parents=True, exist_ok=True)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

    fig, ax = plt.subplots(figsize=(6, 5))
    cax = ax.matshow(cm, cmap="Blues", alpha=0.8)
    fig.colorbar(cax)

    labels = ["Predicted No Disease", "Predicted Disease"]
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_yticklabels(["Actual No Disease", "Actual Disease"], fontsize=10)
    ax.set_title(f"Confusion Matrix — {model_name}", fontsize=12, pad=20)

    for i in range(2):
        for j in range(2):
            val = cm[i, j]
            ax.text(j, i, f"{val}", ha="center", va="center", fontsize=14, fontweight="bold",
                    color="white" if val > cm.max()/2 else "black")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    return save_path


def plot_combined_roc_curves(
    y_true: Union[pd.Series, np.ndarray],
    probabilities_dict: Dict[str, np.ndarray],
    save_path: Path,
) -> Path:
    """
    Generate and save a combined ROC curves figure for all models.

    Args:
        y_true: Ground truth binary labels.
        probabilities_dict: Map of model_name -> y_prob.
        save_path: Output file destination path.

    Returns:
        Path: Path to saved figure.
    """
    save_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]

    for (model_name, y_prob), color in zip(probabilities_dict.items(), colors):
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        auc_score = roc_auc_score(y_true, y_prob)
        ax.plot(fpr, tpr, label=f"{model_name} (AUC = {auc_score:.4f})", linewidth=2, color=color)

    # Random baseline diagonal
    ax.plot([0, 1], [0, 1], "k--", label="Random Classifier (AUC = 0.5000)", linewidth=1.5)

    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=11)
    ax.set_ylabel("True Positive Rate (Recall / Sensitivity)", fontsize=11)
    ax.set_title("Combined ROC Curves — Baseline Classifiers", fontsize=13, pad=15)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    return save_path


def plot_model_comparison(
    test_results_df: pd.DataFrame,
    save_path: Path,
) -> Path:
    """
    Generate and save a bar chart comparing performance metrics across models.

    Args:
        test_results_df: DataFrame containing test metrics for all models.
        save_path: Output file destination path.

    Returns:
        Path: Path to saved figure.
    """
    save_path.parent.mkdir(parents=True, exist_ok=True)

    metrics_to_plot = ["Accuracy", "Precision", "Recall", "F1", "ROC_AUC"]
    models = test_results_df["Model"].tolist()

    x = np.arange(len(models))
    width = 0.15

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ["#2b5c8f", "#3182bd", "#6baed6", "#d95f02", "#7570b3"]

    for i, metric in enumerate(metrics_to_plot):
        values = test_results_df[metric].tolist()
        offset = (i - 2) * width
        ax.bar(x + offset, values, width, label=metric, color=colors[i])

    ax.set_title("Baseline Machine Learning Models — Test Performance Comparison", fontsize=13, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=15, ha="right", fontsize=10)
    ax.set_ylabel("Score (0.0 to 1.0)", fontsize=11)
    ax.set_ylim([0.0, 1.05])
    ax.legend(loc="lower left", fontsize=10)
    ax.grid(axis="y", linestyle=":", alpha=0.6)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    return save_path
