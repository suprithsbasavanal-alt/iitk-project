"""
Master Hyperparameter Tuning and Optimization Execution Script (Part 6).

This script conducts systematic hyperparameter search (GridSearchCV & RandomizedSearchCV)
for 5 target models on raw training features (242 rows) using 5-fold Stratified CV and ROC-AUC
as the primary search metric. The 61-row test set is kept strictly locked until after search
completion, parameter extraction, pre-test ranking, and configuration freezing.
"""

from datetime import datetime
from pathlib import Path
import json
import sys
import joblib
import numpy as np
import pandas as pd

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.train import (
    get_tuning_search_spaces,
    build_search_object,
    build_baseline_pipeline,
    get_file_safe_name,
    evaluate_cv_baseline,
)
from src.evaluate import (
    calculate_metrics,
    generate_classification_reports,
    plot_confusion_matrix,
    plot_combined_roc_curves,
    plot_model_comparison,
    plot_baseline_vs_tuned_roc_auc,
    plot_baseline_vs_tuned_comparison,
)


def run_hyperparameter_tuning() -> None:
    """
    Execute 15-step hyperparameter search, pre-test ranking, configuration freezing,
    test set evaluation, figure generation, and text report generation.
    """
    print("=" * 70)
    print("STARTING HYPERPARAMETER TUNING AND MODEL OPTIMIZATION (PART 6)")
    print("=" * 70)

    processed_dir = project_root / "data" / "processed"
    models_tuned_dir = project_root / "models" / "tuned"
    metrics_tuning_dir = project_root / "results" / "metrics" / "tuning"
    figures_tuning_dir = project_root / "results" / "figures" / "tuning"

    processed_dir.mkdir(parents=True, exist_ok=True)
    models_tuned_dir.mkdir(parents=True, exist_ok=True)
    metrics_tuning_dir.mkdir(parents=True, exist_ok=True)
    figures_tuning_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Load training data strictly (242 rows). DO NOT LOAD TEST SET YET!
    X_train_raw = pd.read_csv(processed_dir / "X_train_raw.csv")
    y_train = pd.read_csv(processed_dir / "y_train.csv")["target"]

    print(f"Loaded Training Data ONLY: X_train = {X_train_raw.shape}, y_train = {y_train.shape}")
    print("Test set (61 rows) is LOCKED and will not be accessed during tuning or pre-test ranking.")

    # Step 2: Retrieve search spaces for 5 target models
    spaces = get_tuning_search_spaces()
    print(f"\nModels Selected for Tuning ({len(spaces)}): {list(spaces.keys())}")

    best_params_json = {}
    search_summary_list = []
    best_pipelines_dict = {}

    # Step 3: Execute hyperparameter searches on X_train_raw (242 rows)
    for model_name, (cls, param_space, search_method) in spaces.items():
        safe_name = get_file_safe_name(model_name)
        print(f"\n--- Running {search_method.upper()} Search for {model_name} ---")

        search = build_search_object(
            model_name=model_name,
            classifier=cls,
            param_space=param_space,
            search_method=search_method,
            n_iter=60,
            random_state=42,
        )

        # Fit search strictly on training features
        search.fit(X_train_raw, y_train)

        # Extract cv_results_ and save detailed CSV
        cv_results_df = pd.DataFrame(search.cv_results_)
        cv_results_path = metrics_tuning_dir / f"{safe_name}_search_results.csv"
        cv_results_df.to_csv(cv_results_path, index=False)

        candidate_count = len(cv_results_df)
        approx_fits = candidate_count * 5  # 5 CV folds

        best_params = search.best_params_
        best_score = float(search.best_score_)

        print(f"Candidates Evaluated: {candidate_count} | Approx Fits: {approx_fits}")
        print(f"Best CV ROC-AUC:      {best_score:.4f}")
        print(f"Best Parameters:      {best_params}")

        # Clean string keys for JSON serialization
        clean_best_params = {k.replace("classifier__", ""): v for k, v in best_params.items()}

        best_params_json[model_name] = {
            "search_method": "GridSearchCV" if search_method == "grid" else "RandomizedSearchCV",
            "best_params": best_params,
            "clean_best_params": clean_best_params,
            "best_cv_roc_auc": best_score,
            "candidate_configurations_evaluated": candidate_count,
            "total_cv_fits": approx_fits,
        }

        search_summary_list.append({
            "Model": model_name,
            "Search_Method": "GridSearchCV" if search_method == "grid" else "RandomizedSearchCV",
            "Candidate_Configurations": candidate_count,
            "CV_Folds": 5,
            "Approximate_Fits_Performed": approx_fits,
            "Best_CV_ROC_AUC": best_score,
        })

        best_pipelines_dict[model_name] = search.best_estimator_

    # Save best_parameters.json
    best_params_json_path = metrics_tuning_dir / "best_parameters.json"
    with open(best_params_json_path, "w") as f:
        json.dump(best_params_json, f, indent=2)
    print(f"\nSaved Best Parameters: {best_params_json_path.resolve()}")

    # Save search_summary.csv
    search_summary_df = pd.DataFrame(search_summary_list)
    search_summary_path = metrics_tuning_dir / "search_summary.csv"
    search_summary_df.to_csv(search_summary_path, index=False)

    # Step 4: Evaluate tuned pipelines via fresh 5-fold CV on X_train_raw
    print("\n--- Running Fresh 5-Fold Stratified CV for Best Tuned Pipeline Configurations ---")
    tuned_cv_dict = {name: pipe.named_steps["classifier"] for name, pipe in best_pipelines_dict.items()}
    tuned_cv_summary_df, _ = evaluate_cv_baseline(
        tuned_cv_dict, X_train_raw, y_train, n_splits=5, random_state=42
    )

    tuned_cv_summary_path = metrics_tuning_dir / "tuned_cv_results.csv"
    tuned_cv_summary_df.to_csv(tuned_cv_summary_path, index=False)
    print(f"Saved Tuned CV Results: {tuned_cv_summary_path.resolve()}")

    # Step 5: Establish Objective Pre-Test Model Ranking based ONLY on Training CV ROC-AUC
    pre_test_ranking_df = tuned_cv_summary_df.sort_values(by="CV_ROC_AUC_Mean", ascending=False).reset_index(drop=True)
    pre_test_ranking_df["Pre_Test_Rank"] = range(1, len(pre_test_ranking_df) + 1)
    
    # Reorder columns
    cols_order = ["Pre_Test_Rank", "Model", "CV_ROC_AUC_Mean", "CV_ROC_AUC_Std", "CV_F1_Mean", "CV_Recall_Mean", "CV_Accuracy_Mean", "CV_Precision_Mean"]
    pre_test_ranking_df = pre_test_ranking_df[cols_order]

    pre_test_ranking_path = metrics_tuning_dir / "pre_test_model_ranking.csv"
    pre_test_ranking_df.to_csv(pre_test_ranking_path, index=False)
    print("\n--- OBJECTIVE PRE-TEST MODEL RANKING (TRAINING CV ROC-AUC) ---")
    print(pre_test_ranking_df.to_string(index=False))
    print(f"Saved Pre-Test Ranking: {pre_test_ranking_path.resolve()}")

    # Step 6: FREEZE TUNED CONFIGURATIONS BEFORE TEST EVALUATION
    frozen_config = {
        "timestamp": datetime.now().isoformat(),
        "status": "FROZEN_BEFORE_TEST_SET_EVALUATION",
        "primary_metric": "CV_ROC_AUC",
        "pre_test_ranking": pre_test_ranking_df[["Pre_Test_Rank", "Model", "CV_ROC_AUC_Mean"]].to_dict(orient="records"),
        "frozen_models": best_params_json,
    }
    frozen_config_path = metrics_tuning_dir / "frozen_tuned_configurations.json"
    with open(frozen_config_path, "w") as f:
        json.dump(frozen_config, f, indent=2)
    print(f"\n[LOCK] FROZEN TUNED CONFIGURATIONS WRITTEN: {frozen_config_path.resolve()}")
    print("[LOCK] Hyperparameter selection is complete. Test set may now be safely unlocked for evaluation.")

    # Step 7: FIT TUNED PIPELINES ON ALL 242 TRAINING ROWS & SAVE MODEL ARTIFACTS
    print("\n--- Fitting Complete Tuned Pipelines on All 242 Training Rows ---")
    fitted_tuned_pipelines = {}
    for model_name, pipeline in best_pipelines_dict.items():
        safe_name = get_file_safe_name(model_name)

        # Fit complete pipeline on X_train_raw
        pipeline.fit(X_train_raw, y_train)
        fitted_tuned_pipelines[model_name] = pipeline

        # Save to models/tuned/<safe_name>_tuned.joblib
        model_artifact_path = models_tuned_dir / f"{safe_name}_tuned.joblib"
        joblib.dump(pipeline, model_artifact_path)
        print(f"Saved Tuned Model Artifact: {model_artifact_path.resolve()}")

    # Step 8: UNLOCK & LOAD UNTOUCHED TEST SET (61 ROWS) FOR SINGLE-PASS EVALUATION
    print("\n--- UNLOCKING TEST SET (61 Rows) FOR SINGLE-PASS EVALUATION ---")
    X_test_raw = pd.read_csv(processed_dir / "X_test_raw.csv")
    y_test = pd.read_csv(processed_dir / "y_test.csv")["target"]

    tuned_test_metrics_list = []
    tuned_probabilities_dict = {}
    tuned_predictions_dict = {}

    for model_name, pipeline in fitted_tuned_pipelines.items():
        safe_name = get_file_safe_name(model_name)

        y_pred = pipeline.predict(X_test_raw)
        
        if hasattr(pipeline, "predict_proba"):
            y_prob = pipeline.predict_proba(X_test_raw)[:, 1]
        elif hasattr(pipeline, "decision_function"):
            y_prob = pipeline.decision_function(X_test_raw)
        else:
            y_prob = y_pred.astype(float)

        tuned_predictions_dict[model_name] = (y_pred, y_prob)
        tuned_probabilities_dict[model_name] = y_prob

        metrics = calculate_metrics(y_test, y_pred, y_prob)
        tuned_test_metrics_list.append({"Model": model_name, **metrics})

        # Save tuned confusion matrix PNG
        cm_path = figures_tuning_dir / f"{safe_name}_tuned_confusion_matrix.png"
        plot_confusion_matrix(y_test, y_pred, f"{model_name} (Tuned)", cm_path)

    tuned_test_df = pd.DataFrame(tuned_test_metrics_list)
    tuned_test_path = metrics_tuning_dir / "tuned_test_results.csv"
    tuned_test_df.to_csv(tuned_test_path, index=False)
    print(f"Saved Tuned Test Results: {tuned_test_path.resolve()}")

    # Step 9: BASELINE VS TUNED COMPARISON & FALSE-NEGATIVE ANALYSIS
    baseline_test_df = pd.read_csv(project_root / "results" / "metrics" / "baseline_test_results.csv")
    baseline_cv_df = pd.read_csv(project_root / "results" / "metrics" / "baseline_cv_results.csv")

    comparison_list = []
    fn_comparison_list = []

    for model_name in spaces.keys():
        b_test = baseline_test_df[baseline_test_df["Model"] == model_name].iloc[0]
        t_test = tuned_test_df[tuned_test_df["Model"] == model_name].iloc[0]

        b_cv = baseline_cv_df[baseline_cv_df["Model"] == model_name].iloc[0]
        t_cv = tuned_cv_summary_df[tuned_cv_summary_df["Model"] == model_name].iloc[0]

        comparison_list.append({
            "Model": model_name,
            "Baseline_CV_ROC_AUC": b_cv["CV_ROC_AUC_Mean"],
            "Tuned_CV_ROC_AUC": t_cv["CV_ROC_AUC_Mean"],
            "CV_ROC_AUC_Change": t_cv["CV_ROC_AUC_Mean"] - b_cv["CV_ROC_AUC_Mean"],
            "Baseline_CV_F1": b_cv["CV_F1_Mean"],
            "Tuned_CV_F1": t_cv["CV_F1_Mean"],
            "CV_F1_Change": t_cv["CV_F1_Mean"] - b_cv["CV_F1_Mean"],
            "Baseline_Test_Accuracy": b_test["Accuracy"],
            "Tuned_Test_Accuracy": t_test["Accuracy"],
            "Test_Accuracy_Change": t_test["Accuracy"] - b_test["Accuracy"],
            "Baseline_Test_Recall": b_test["Recall"],
            "Tuned_Test_Recall": t_test["Recall"],
            "Test_Recall_Change": t_test["Recall"] - b_test["Recall"],
            "Baseline_Test_F1": b_test["F1"],
            "Tuned_Test_F1": t_test["F1"],
            "Test_F1_Change": t_test["F1"] - b_test["F1"],
            "Baseline_Test_ROC_AUC": b_test["ROC_AUC"],
            "Tuned_Test_ROC_AUC": t_test["ROC_AUC"],
            "Test_ROC_AUC_Change": t_test["ROC_AUC"] - b_test["ROC_AUC"],
        })

        fn_comparison_list.append({
            "Model": model_name,
            "Baseline_FN": int(b_test["FN"]),
            "Tuned_FN": int(t_test["FN"]),
            "FN_Change": int(t_test["FN"] - b_test["FN"]),
        })

    baseline_vs_tuned_df = pd.DataFrame(comparison_list)
    baseline_vs_tuned_path = metrics_tuning_dir / "baseline_vs_tuned.csv"
    baseline_vs_tuned_df.to_csv(baseline_vs_tuned_path, index=False)

    fn_comp_df = pd.DataFrame(fn_comparison_list)
    fn_comp_path = metrics_tuning_dir / "false_negative_comparison.csv"
    fn_comp_df.to_csv(fn_comp_path, index=False)

    # Step 10: GENERATE VISUALIZATIONS
    roc_fig_path = figures_tuning_dir / "tuned_roc_curves.png"
    plot_combined_roc_curves(y_test, tuned_probabilities_dict, roc_fig_path)

    roc_auc_comp_fig_path = figures_tuning_dir / "baseline_vs_tuned_roc_auc.png"
    plot_baseline_vs_tuned_roc_auc(baseline_vs_tuned_df, roc_auc_comp_fig_path)

    tuned_comp_fig_path = figures_tuning_dir / "tuned_model_comparison.png"
    plot_model_comparison(tuned_test_df, tuned_comp_fig_path)

    b_vs_t_comp_fig_path = figures_tuning_dir / "baseline_vs_tuned_comparison.png"
    plot_baseline_vs_tuned_comparison(baseline_vs_tuned_df, b_vs_t_comp_fig_path)

    # Step 11: GENERATE COMPREHENSIVE TEXT REPORT
    report_text = f"""Hyperparameter Tuning and Model Optimization Report (Part 6)
===================================================================
Project: Heart Disease Prediction
Scope: Systematic Hyperparameter Search & Optimization (5 Target Models)

1. Objective & Methodology
--------------------------
The primary goal of Part 6 is to tune promising baseline classification algorithms using 5-Fold Stratified Cross-Validation on the 242-row training set with ROC-AUC as the optimization metric.

2. Test-Set Protection Strategy
--------------------------------
- Training Set: 242 rows (80%)
- Test Set: 61 rows (20%) — Strictly LOCKED during hyperparameter search, parameter selection, and pre-test model ranking.
- Configuration Freezing: Best parameters for all 5 models were written to 'frozen_tuned_configurations.json' BEFORE test set evaluation.

3. Target Models Tuned ({len(spaces)})
-------------------------
1. Logistic Regression (GridSearchCV)
2. Support Vector Machine (GridSearchCV)
3. Random Forest (RandomizedSearchCV, n_iter=60)
4. XGBoost (RandomizedSearchCV, n_iter=60)
5. K-Nearest Neighbors (GridSearchCV)

Un-tuned baseline models preserved for comparison: Decision Tree, Gaussian Naive Bayes.

4. Search Complexity & Fits
----------------------------
{search_summary_df.to_string(index=False)}

5. Pre-Test Model Ranking (Based ONLY on Training CV ROC-AUC)
------------------------------------------------------------
{pre_test_ranking_df.to_string(index=False)}

6. Tuned 5-Fold Cross-Validation Performance (Training Set)
----------------------------------------------------------
{tuned_cv_summary_df.to_string(index=False)}

7. Tuned Test Set Performance (61 Preserved Rows)
-------------------------------------------------
{tuned_test_df.to_string(index=False)}

8. Baseline vs. Tuned Performance Comparison
--------------------------------------------
{baseline_vs_tuned_df[["Model", "Baseline_CV_ROC_AUC", "Tuned_CV_ROC_AUC", "Baseline_Test_ROC_AUC", "Tuned_Test_ROC_AUC", "Baseline_Test_F1", "Tuned_Test_F1"]].to_string(index=False)}

9. False-Negative Analysis (Class 1 = Heart Disease Present)
-----------------------------------------------------------
{fn_comp_df.to_string(index=False)}
Note: Lower FN count reduces the risk of missed heart disease diagnoses on this held-out evaluation split.

10. Best Hyperparameter Configurations
---------------------------------------
"""
    for m_name, meta in best_params_json.items():
        report_text += f"\n[{m_name}] ({meta['search_method']})\n"
        report_text += f"Best CV ROC-AUC: {meta['best_cv_roc_auc']:.4f}\n"
        report_text += f"Parameters: {meta['clean_best_params']}\n"

    report_text += f"""
11. Key Observations & Statistical Caution
------------------------------------------
- Dataset Size: 303 total instances (242 train, 61 test).
- Due to small sample sizes in clinical capstone datasets, metrics represent empirical performance on this specific split. No claims of production readiness or clinical validation are made.

12. Next Steps (Part 7)
-----------------------
In Part 7 (Final Model Selection & Comprehensive Comparison), the single best model will be selected based on clinical requirements (balancing ROC-AUC, Recall, and F1 stability) and evaluated for final deployment packaging.
"""

    report_path = project_root / "results" / "hyperparameter_tuning_report.txt"
    with open(report_path, "w") as f:
        f.write(report_text)

    print("\n=" * 70)
    print("HYPERPARAMETER TUNING EXECUTION COMPLETED SUCCESSFULLY!")
    print(f"Best Parameters Saved:      {best_params_json_path.resolve()}")
    print(f"Frozen Configurations Saved: {frozen_config_path.resolve()}")
    print(f"Tuned Test Results Saved:   {tuned_test_path.resolve()}")
    print(f"Tuned Model Artifacts:     {models_tuned_dir.resolve()}")
    print(f"Report Text Saved:          {report_path.resolve()}")
    print("=" * 70)


if __name__ == "__main__":
    run_hyperparameter_tuning()
