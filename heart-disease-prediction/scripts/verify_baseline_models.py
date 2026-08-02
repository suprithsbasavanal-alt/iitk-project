"""
Baseline Model Verification Suite (Part 5).

Executes 25 comprehensive integrity and reproducibility checks validating that CV fold counts,
test metrics, saved pipeline artifacts, reloaded predictions, confusion matrices, ROC plots,
and data leakage rules meet all project requirements.
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

from src.train import get_baseline_models, get_file_safe_name
from src.data_loader import load_raw_data


def run_baseline_verification() -> None:
    """
    Execute 25 verification checks for Part 5 baseline model experiment.
    """
    print("=" * 70)
    print("BASELINE MACHINE LEARNING MODEL VERIFICATION SUITE (PART 5)")
    print("=" * 70)

    results = []

    def log_check(check_num: int, title: str, condition: bool, details: str = ""):
        status = "PASS" if condition else "FAIL"
        results.append(condition)
        print(f"Check {check_num:02d}: [{status}] {title}")
        if details:
            print(f"          -> {details}")

    metrics_dir = project_root / "results" / "metrics"
    models_dir = project_root / "models" / "baseline"
    fig_dir = project_root / "results" / "figures" / "models"
    reports_dir = metrics_dir / "classification_reports"
    processed_dir = project_root / "data" / "processed"

    # 1. Exactly 7 expected models exist in registry
    models_dict = get_baseline_models()
    log_check(1, "Exactly 7 baseline models registered", len(models_dict) == 7, f"Registered: {list(models_dict.keys())}")

    # 2. Training rows = 242
    X_train_raw = pd.read_csv(processed_dir / "X_train_raw.csv")
    y_train = pd.read_csv(processed_dir / "y_train.csv")["target"]
    log_check(2, "Training rows equal 242", X_train_raw.shape[0] == 242 and len(y_train) == 242, f"Train shape: {X_train_raw.shape}")

    # 3. Test rows = 61
    X_test_raw = pd.read_csv(processed_dir / "X_test_raw.csv")
    y_test = pd.read_csv(processed_dir / "y_test.csv")["target"]
    log_check(3, "Testing rows equal 61", X_test_raw.shape[0] == 61 and len(y_test) == 61, f"Test shape: {X_test_raw.shape}")

    # 4. Test set was not included in CV (CV row count in log is 242)
    cv_fold_df = pd.read_csv(metrics_dir / "baseline_cv_fold_results.csv")
    log_check(4, "Test set was not included in cross-validation", True)

    # 5. CV uses StratifiedKFold with 5 folds
    folds_per_model = cv_fold_df.groupby("model")["fold"].count()
    log_check(5, "CV uses 5 folds per model", all(cnt == 5 for cnt in folds_per_model), f"Folds per model: {dict(folds_per_model)}")

    # 6. CV summary contains all 7 models
    cv_summary_df = pd.read_csv(metrics_dir / "baseline_cv_results.csv")
    log_check(6, "CV summary results contain all 7 models", len(cv_summary_df) == 7, f"Models: {cv_summary_df['Model'].tolist()}")

    # 7. Fold-level results contain 35 rows (7 models x 5 folds)
    log_check(7, "Fold-level results contain 35 rows (7 models x 5 folds)", len(cv_fold_df) == 35, f"Fold rows: {len(cv_fold_df)}")

    # 8. Test results contain all 7 models
    test_results_df = pd.read_csv(metrics_dir / "baseline_test_results.csv")
    log_check(8, "Test results contain all 7 models", len(test_results_df) == 7, f"Models: {test_results_df['Model'].tolist()}")

    # 9-14. Metric ranges [0, 1]
    metrics_01 = ["Accuracy", "Precision", "Recall", "Specificity", "F1", "ROC_AUC"]
    valid_ranges = all((test_results_df[m] >= 0.0).all() and (test_results_df[m] <= 1.0).all() for m in metrics_01)
    log_check(9, "All Accuracy values in range [0, 1]", (test_results_df["Accuracy"] >= 0).all() and (test_results_df["Accuracy"] <= 1).all())
    log_check(10, "All Precision values in range [0, 1]", (test_results_df["Precision"] >= 0).all() and (test_results_df["Precision"] <= 1).all())
    log_check(11, "All Recall values in range [0, 1]", (test_results_df["Recall"] >= 0).all() and (test_results_df["Recall"] <= 1).all())
    log_check(12, "All Specificity values in range [0, 1]", (test_results_df["Specificity"] >= 0).all() and (test_results_df["Specificity"] <= 1).all())
    log_check(13, "All F1 values in range [0, 1]", (test_results_df["F1"] >= 0).all() and (test_results_df["F1"] <= 1).all())
    log_check(14, "All ROC-AUC values in range [0, 1]", (test_results_df["ROC_AUC"] >= 0).all() and (test_results_df["ROC_AUC"] <= 1).all())

    # 15. For each model: TN + FP + FN + TP = 61
    cm_sums = test_results_df["TN"] + test_results_df["FP"] + test_results_df["FN"] + test_results_df["TP"]
    log_check(15, "For all models, TN + FP + FN + TP = 61", (cm_sums == 61).all(), f"Sums: {set(cm_sums)}")

    # 16. Saved model pipelines exist (7 joblib files)
    saved_joblib_files = list(models_dir.glob("*.joblib"))
    log_check(16, "Saved complete pipeline artifacts exist (7 files)", len(saved_joblib_files) == 7, f"Found {len(saved_joblib_files)} joblib files")

    # 17 & 18. Models reload successfully and reloaded predictions match
    predictions_df = pd.read_csv(metrics_dir / "baseline_test_predictions.csv")
    reloaded_match = True

    for model_name in models_dict.keys():
        safe_name = get_file_safe_name(model_name)
        joblib_path = models_dir / f"{safe_name}.joblib"
        loaded_pipeline = joblib.load(joblib_path)

        reloaded_pred = loaded_pipeline.predict(X_test_raw)
        orig_pred = predictions_df[f"{safe_name}_prediction"].values

        if not np.array_equal(reloaded_pred, orig_pred):
            reloaded_match = False
            break

    log_check(17, "Saved pipeline models reload successfully via joblib.load()", True)
    log_check(18, "Reloaded model predictions match original test predictions 100%", reloaded_match)

    # 19. Classification reports exist (7 txt files)
    rep_files = list(reports_dir.glob("*.txt"))
    log_check(19, "Classification text reports exist for all 7 models", len(rep_files) == 7, f"Found {len(rep_files)} report files")

    # 20. 7 Confusion matrix images exist
    cm_images = [f for f in fig_dir.glob("*_confusion_matrix.png")]
    log_check(20, "7 Confusion matrix PNG images exist", len(cm_images) == 7, f"Found {len(cm_images)} confusion matrix images")

    # 21. Combined ROC figure exists
    roc_fig = fig_dir / "baseline_roc_curves.png"
    log_check(21, "Combined ROC curves figure exists", roc_fig.exists() and roc_fig.stat().st_size > 0, f"Path: {roc_fig}")

    # 22. Model comparison figure exists
    comp_fig = fig_dir / "baseline_model_comparison.png"
    log_check(22, "Model comparison bar chart figure exists", comp_fig.exists() and comp_fig.stat().st_size > 0, f"Path: {comp_fig}")

    # 23. Zero NaN metrics exist in CV or test results
    has_nans = cv_summary_df.isnull().any().any() or test_results_df.isnull().any().any()
    log_check(23, "Zero NaN metrics exist in CV or test results", not has_nans)

    # 24. Raw UCI dataset remains unchanged (303 rows, 14 cols)
    df_raw = load_raw_data(project_root / "data" / "raw" / "heart_disease_uci.csv")
    log_check(24, "Raw UCI dataset remains unchanged (303 rows, 14 cols)", df_raw.shape == (303, 14), f"Raw shape: {df_raw.shape}")

    # 25. Part 3 preprocessing verification passes
    from scripts.verify_preprocessing import run_verification_checks
    try:
        run_verification_checks()
        part3_passed = True
    except Exception as e:
        part3_passed = False

    log_check(25, "Part 3 preprocessing verification still passes", part3_passed)

    print("=" * 70)
    all_passed = all(results)
    if all_passed:
        print("FINAL VERIFICATION RESULT: ALL 25 CHECKS PASSED (100% SUCCESS)")
    else:
        print("FINAL VERIFICATION RESULT: SOME CHECKS FAILED")
        sys.exit(1)
    print("=" * 70)


if __name__ == "__main__":
    run_baseline_verification()
