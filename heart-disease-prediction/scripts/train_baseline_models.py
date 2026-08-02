"""
Master Baseline Model Training and Evaluation Script (Part 5).

This script executes 5-fold Stratified Cross-Validation on raw training data,
fits 7 complete baseline scikit-learn pipelines on all 242 training rows, evaluates on
the 61-row test set, persists full pipeline artifacts, and generates all metric CSVs,
classification reports, figures, and text reports.
"""

from pathlib import Path
import sys
import joblib
import numpy as np
import pandas as pd

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.train import (
    get_baseline_models,
    get_file_safe_name,
    build_baseline_pipeline,
    evaluate_cv_baseline,
)
from src.evaluate import (
    calculate_metrics,
    generate_classification_reports,
    plot_confusion_matrix,
    plot_combined_roc_curves,
    plot_model_comparison,
)


def run_baseline_experiments() -> None:
    """
    Execute baseline training, CV, test evaluation, and report generation.
    """
    print("=" * 70)
    print("STARTING BASELINE MACHINE LEARNING EXPERIMENT (PART 5)")
    print("=" * 70)

    processed_dir = project_root / "data" / "processed"
    models_dir = project_root / "models" / "baseline"
    metrics_dir = project_root / "results" / "metrics"
    reports_dir = metrics_dir / "classification_reports"
    figures_models_dir = project_root / "results" / "figures" / "models"

    processed_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    figures_models_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load raw split files
    X_train_raw = pd.read_csv(processed_dir / "X_train_raw.csv")
    X_test_raw = pd.read_csv(processed_dir / "X_test_raw.csv")
    y_train = pd.read_csv(processed_dir / "y_train.csv")["target"]
    y_test = pd.read_csv(processed_dir / "y_test.csv")["target"]

    print(f"Loaded Train Data: X_train = {X_train_raw.shape}, y_train = {y_train.shape}")
    print(f"Loaded Test Data:  X_test  = {X_test_raw.shape}, y_test  = {y_test.shape}")

    # 2. Get baseline models
    models_dict = get_baseline_models()
    print(f"\nModels Registered ({len(models_dict)}): {list(models_dict.keys())}")

    # 3. Stratified 5-Fold Cross-Validation on X_train_raw (242 rows)
    print("\n--- Running 5-Fold Stratified Cross-Validation on Training Set ---")
    cv_summary_df, cv_fold_details_df = evaluate_cv_baseline(
        models_dict, X_train_raw, y_train, n_splits=5, random_state=42
    )

    # Save CV CSV outputs
    cv_summary_path = metrics_dir / "baseline_cv_results.csv"
    cv_fold_path = metrics_dir / "baseline_cv_fold_results.csv"
    cv_summary_df.to_csv(cv_summary_path, index=False)
    cv_fold_details_df.to_csv(cv_fold_path, index=False)
    print(f"Saved CV Summary: {cv_summary_path.resolve()}")
    print(f"Saved CV Fold Details ({len(cv_fold_details_df)} rows): {cv_fold_path.resolve()}")

    # 4. Final Fit on All 242 Training Rows & Test Set Evaluation (61 rows)
    print("\n--- Fitting Complete Pipelines on All Training Rows & Evaluating on Test Set ---")
    test_metrics_list = []
    cv_vs_test_list = []
    predictions_dict = {}
    probabilities_dict = {}
    fitted_pipelines_dict = {}

    predictions_export_df = pd.DataFrame({
        "sample_index": X_test_raw.index,
        "actual_target": y_test.values
    })

    for model_name, classifier in models_dict.items():
        safe_name = get_file_safe_name(model_name)
        pipeline = build_baseline_pipeline(classifier)

        # Fit complete pipeline (preprocessor + classifier) on X_train_raw
        pipeline.fit(X_train_raw, y_train)

        # Generate test predictions and probabilities
        y_pred = pipeline.predict(X_test_raw)
        
        # Extract probability for positive class 1
        if hasattr(pipeline, "predict_proba"):
            y_prob = pipeline.predict_proba(X_test_raw)[:, 1]
        elif hasattr(pipeline, "decision_function"):
            y_prob = pipeline.decision_function(X_test_raw)
        else:
            y_prob = y_pred.astype(float)

        predictions_dict[model_name] = (y_pred, y_prob)
        probabilities_dict[model_name] = y_prob
        fitted_pipelines_dict[model_name] = pipeline

        # Save pipeline artifact to models/baseline/<safe_name>.joblib
        pipeline_file = models_dir / f"{safe_name}.joblib"
        joblib.dump(pipeline, pipeline_file)

        # Compute test metrics
        metrics = calculate_metrics(y_test, y_pred, y_prob)
        metrics_row = {"Model": model_name, **metrics}
        test_metrics_list.append(metrics_row)

        # Record test predictions for auditability
        predictions_export_df[f"{safe_name}_prediction"] = y_pred
        predictions_export_df[f"{safe_name}_probability"] = y_prob

        # Save individual confusion matrix plot
        cm_path = figures_models_dir / f"{safe_name}_confusion_matrix.png"
        plot_confusion_matrix(y_test, y_pred, model_name, cm_path)

        # Compare CV mean vs Test metric
        cv_row = cv_summary_df[cv_summary_df["Model"] == model_name].iloc[0]
        cv_vs_test_list.append({
            "Model": model_name,
            "CV_Accuracy_Mean": cv_row["CV_Accuracy_Mean"],
            "Test_Accuracy": metrics["Accuracy"],
            "CV_Recall_Mean": cv_row["CV_Recall_Mean"],
            "Test_Recall": metrics["Recall"],
            "CV_F1_Mean": cv_row["CV_F1_Mean"],
            "Test_F1": metrics["F1"],
            "CV_ROC_AUC_Mean": cv_row["CV_ROC_AUC_Mean"],
            "Test_ROC_AUC": metrics["ROC_AUC"],
        })

    # Save test metrics CSV
    test_results_df = pd.DataFrame(test_metrics_list)
    test_results_path = metrics_dir / "baseline_test_results.csv"
    test_results_df.to_csv(test_results_path, index=False)

    # Save CV vs Test comparison CSV
    cv_vs_test_df = pd.DataFrame(cv_vs_test_list)
    cv_vs_test_path = metrics_dir / "cv_vs_test_comparison.csv"
    cv_vs_test_df.to_csv(cv_vs_test_path, index=False)

    # Save predictions CSV
    predictions_export_path = metrics_dir / "baseline_test_predictions.csv"
    predictions_export_df.to_csv(predictions_export_path, index=False)

    # Save classification reports text files
    generate_classification_reports(y_test, predictions_dict, reports_dir)

    # Save combined ROC curve PNG
    roc_curve_path = figures_models_dir / "baseline_roc_curves.png"
    plot_combined_roc_curves(y_test, probabilities_dict, roc_curve_path)

    # Save model comparison bar chart PNG
    comparison_fig_path = figures_models_dir / "baseline_model_comparison.png"
    plot_model_comparison(test_results_df, comparison_fig_path)

    # 5. Generate Summary Report text file
    best_acc = test_results_df.loc[test_results_df["Accuracy"].idxmax()]["Model"]
    best_prec = test_results_df.loc[test_results_df["Precision"].idxmax()]["Model"]
    best_rec = test_results_df.loc[test_results_df["Recall"].idxmax()]["Model"]
    best_f1 = test_results_df.loc[test_results_df["F1"].idxmax()]["Model"]
    best_auc = test_results_df.loc[test_results_df["ROC_AUC"].idxmax()]["Model"]

    report_text = f"""Baseline Machine Learning Model Experiment Report (Part 5)
===================================================================
Project: Heart Disease Prediction
Scope: Baseline Classifier Benchmarking (No Hyperparameter Tuning)

1. Experiment Setup
-------------------
- Dataset: UCI Heart Disease Dataset (ID 45)
- Training Set Size: 242 rows (80%)
- Test Set Size: 61 rows (20%) — Strictly preserved untouched during CV & fitting
- Binary Target: 'target' (0 = No Heart Disease [164 total], 1 = Heart Disease Present [139 total])
- Cross-Validation: 5-Fold StratifiedKFold (shuffle=True, random_state=42) on X_train_raw
- Modeling Architecture: End-to-End scikit-learn Pipelines (Preprocessor + Classifier)

2. Models Evaluated ({len(models_dict)})
-----------------------
1. Logistic Regression
2. K-Nearest Neighbors
3. Decision Tree
4. Random Forest
5. Support Vector Machine (probability=True)
6. Gaussian Naive Bayes
7. XGBoost (eval_metric='logloss')

3. Stratified 5-Fold Cross-Validation Summary
---------------------------------------------
{cv_summary_df.to_string(index=False)}

4. Final Test Set Evaluation Results (61 Rows)
---------------------------------------------
{test_results_df.to_string(index=False)}

5. Confusion Matrix Summary (Test Set)
--------------------------------------
"""
    for _, row in test_results_df.iterrows():
        report_text += f"- {row['Model']}: TN={row['TN']}, FP={row['FP']}, FN={row['FN']}, TP={row['TP']}\n"

    report_text += f"""
6. Best Baseline Models by Metric
----------------------------------
- Highest Test Accuracy:    {best_acc} ({test_results_df.loc[test_results_df['Model']==best_acc, 'Accuracy'].values[0]:.4f})
- Highest Test Precision:   {best_prec} ({test_results_df.loc[test_results_df['Model']==best_prec, 'Precision'].values[0]:.4f})
- Highest Test Recall:      {best_rec} ({test_results_df.loc[test_results_df['Model']==best_rec, 'Recall'].values[0]:.4f})
- Highest Test F1-Score:    {best_f1} ({test_results_df.loc[test_results_df['Model']==best_f1, 'F1'].values[0]:.4f})
- Highest Test ROC-AUC:     {best_auc} ({test_results_df.loc[test_results_df['Model']==best_auc, 'ROC_AUC'].values[0]:.4f})

7. Cross-Validation vs Test Comparison
--------------------------------------
{cv_vs_test_df.to_string(index=False)}

8. Medical Evaluation Context
-----------------------------
In clinical heart disease prediction, False Negatives (predicting No Disease when Disease is Present) represent missed diagnoses and carry high medical risk. Models exhibiting high Recall (Sensitivity) alongside balanced F1 and ROC-AUC scores provide strong candidates for hyperparameter tuning in Part 6.

9. Next Steps
-------------
Promising baseline models will be advanced to Part 6 for systematic hyperparameter tuning using Stratified Cross-Validation.

10. Disclaimer
--------------
This project is conducted strictly for educational and academic research purposes as part of a college capstone project.
"""

    report_path = project_root / "results" / "baseline_model_report.txt"
    with open(report_path, "w") as f:
        f.write(report_text)

    print("\n=" * 70)
    print("BASELINE EXPERIMENT EXECUTION COMPLETED SUCCESSFULLY!")
    print(f"Test Results Saved:       {test_results_path.resolve()}")
    print(f"Pipeline Models Saved:    {models_dir.resolve()}")
    print(f"ROC Curve Plot Saved:     {roc_curve_path.resolve()}")
    print(f"Report Text Saved:        {report_path.resolve()}")
    print("=" * 70)


if __name__ == "__main__":
    run_baseline_experiments()
