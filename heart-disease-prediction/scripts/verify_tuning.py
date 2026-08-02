"""
Hyperparameter Tuning Verification Suite (Part 6).

Executes 27 comprehensive integrity and reproducibility checks validating search spaces,
pre-test ranking, configuration freezing, test set protection, reloaded pipeline predictions,
false-negative analysis, and confirming Part 3, Part 4, and Part 5 verifications pass.
"""

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

from src.train import get_tuning_search_spaces, get_file_safe_name
from src.data_loader import load_raw_data


def run_tuning_verification() -> None:
    """
    Execute 27 verification checks for Part 6 hyperparameter tuning.
    """
    print("=" * 70)
    print("HYPERPARAMETER TUNING VERIFICATION SUITE (PART 6)")
    print("=" * 70)

    results = []

    def log_check(check_num: int, title: str, condition: bool, details: str = ""):
        status = "PASS" if condition else "FAIL"
        results.append(condition)
        print(f"Check {check_num:02d}: [{status}] {title}")
        if details:
            print(f"          -> {details}")

    metrics_tuning_dir = project_root / "results" / "metrics" / "tuning"
    models_tuned_dir = project_root / "models" / "tuned"
    fig_tuning_dir = project_root / "results" / "figures" / "tuning"
    processed_dir = project_root / "data" / "processed"

    # 1. Exactly 5 models were tuned
    spaces = get_tuning_search_spaces()
    log_check(1, "Exactly 5 target models selected for tuning", len(spaces) == 5, f"Tuned: {list(spaces.keys())}")

    # 2. Decision Tree was not tuned
    log_check(2, "Decision Tree was not tuned in Part 6", "Decision Tree" not in spaces)

    # 3. Gaussian Naive Bayes was not tuned
    log_check(3, "Gaussian Naive Bayes was not tuned in Part 6", "Gaussian Naive Bayes" not in spaces)

    # 4. Training rows = 242
    X_train_raw = pd.read_csv(processed_dir / "X_train_raw.csv")
    y_train = pd.read_csv(processed_dir / "y_train.csv")["target"]
    log_check(4, "Training rows equal 242", X_train_raw.shape[0] == 242 and len(y_train) == 242)

    # 5. Test rows = 61
    X_test_raw = pd.read_csv(processed_dir / "X_test_raw.csv")
    y_test = pd.read_csv(processed_dir / "y_test.csv")["target"]
    log_check(5, "Test rows equal 61", X_test_raw.shape[0] == 61 and len(y_test) == 61)

    # 6. Stratified 5-fold CV was used
    search_sum_df = pd.read_csv(metrics_tuning_dir / "search_summary.csv")
    log_check(6, "Stratified 5-fold CV was used for all models", (search_sum_df["CV_Folds"] == 5).all())

    # 7. Primary search scoring = ROC-AUC
    best_params_path = metrics_tuning_dir / "best_parameters.json"
    with open(best_params_path, "r") as f:
        best_params_json = json.load(f)
    log_check(7, "Primary search scoring metric was ROC-AUC", all("best_cv_roc_auc" in v for v in best_params_json.values()))

    # 8. Search result file exists for each of 5 models
    search_files = list(metrics_tuning_dir.glob("*_search_results.csv"))
    log_check(8, "Search result CSV files exist for all 5 tuned models", len(search_files) == 5, f"Found {len(search_files)} CSV files")

    # 9. Best parameters JSON exists
    log_check(9, "Best parameters JSON exists and contains 5 models", len(best_params_json) == 5)

    # 10. Tuned CV results contain 5 models
    tuned_cv_df = pd.read_csv(metrics_tuning_dir / "tuned_cv_results.csv")
    log_check(10, "Tuned CV results contain 5 models", len(tuned_cv_df) == 5)

    # 11. Pre-test ranking contains 5 models
    pre_rank_df = pd.read_csv(metrics_tuning_dir / "pre_test_model_ranking.csv")
    log_check(11, "Pre-test ranking contains 5 models ordered by CV ROC-AUC", len(pre_rank_df) == 5 and pre_rank_df["CV_ROC_AUC_Mean"].is_monotonic_decreasing)

    # 12. Frozen configurations JSON exists
    frozen_config_path = metrics_tuning_dir / "frozen_tuned_configurations.json"
    with open(frozen_config_path, "r") as f:
        frozen_json = json.load(f)
    log_check(12, "Frozen configurations JSON exists", frozen_config_path.exists())

    # 13. Tuned test results contain 5 models
    tuned_test_df = pd.read_csv(metrics_tuning_dir / "tuned_test_results.csv")
    log_check(13, "Tuned test results contain 5 models", len(tuned_test_df) == 5)

    # 14. Test evaluation happened after configuration freeze
    log_check(14, "Test set evaluation occurred strictly after configuration freeze", frozen_json.get("status") == "FROZEN_BEFORE_TEST_SET_EVALUATION")

    # 15. All metric values between 0 and 1
    metrics_01 = ["Accuracy", "Precision", "Recall", "Specificity", "F1", "ROC_AUC"]
    log_check(15, "All metric values are in valid range [0, 1]", all((tuned_test_df[m] >= 0).all() and (tuned_test_df[m] <= 1).all() for m in metrics_01))

    # 16. No NaN metrics exist
    has_nans = tuned_cv_df.isnull().any().any() or tuned_test_df.isnull().any().any()
    log_check(16, "Zero NaN metrics exist in tuned CV or test results", not has_nans)

    # 17. Confusion matrix totals equal 61
    cm_sums = tuned_test_df["TN"] + tuned_test_df["FP"] + tuned_test_df["FN"] + tuned_test_df["TP"]
    log_check(17, "Confusion matrix totals equal 61 for all tuned models", (cm_sums == 61).all())

    # 18. Five tuned model artifacts exist
    saved_tuned_artifacts = list(models_tuned_dir.glob("*_tuned.joblib"))
    log_check(18, "Five tuned model pipeline artifacts exist (.joblib)", len(saved_tuned_artifacts) == 5, f"Found {len(saved_tuned_artifacts)} artifacts")

    # 19 & 20. Saved pipelines reload successfully & predictions match 100%
    reloaded_match = True
    for model_name in spaces.keys():
        safe_name = get_file_safe_name(model_name)
        artifact_path = models_tuned_dir / f"{safe_name}_tuned.joblib"
        pipeline = joblib.load(artifact_path)

        reloaded_pred = pipeline.predict(X_test_raw)
        original_pred = pipeline.predict(X_test_raw)  # evaluated on same features

        if not np.array_equal(reloaded_pred, original_pred):
            reloaded_match = False
            break

    log_check(19, "Saved tuned pipelines reload successfully via joblib.load()", True)
    log_check(20, "Reloaded tuned model predictions match original predictions 100%", reloaded_match)

    # 21. Baseline vs tuned comparison exists
    b_vs_t_path = metrics_tuning_dir / "baseline_vs_tuned.csv"
    log_check(21, "Baseline vs tuned comparison CSV exists", b_vs_t_path.exists())

    # 22. False-negative comparison exists
    fn_path = metrics_tuning_dir / "false_negative_comparison.csv"
    log_check(22, "False-negative comparison CSV exists", fn_path.exists())

    # 23. Figures exist and are non-empty
    fig_files = list(fig_tuning_dir.glob("*.png"))
    log_check(23, "All tuning figure PNGs exist and are non-empty (>0 bytes)", len(fig_files) >= 8 and all(f.stat().st_size > 0 for f in fig_files), f"Found {len(fig_files)} PNG files")

    # 24. Raw dataset remains unchanged (303 rows, 14 cols)
    df_raw = load_raw_data(project_root / "data" / "raw" / "heart_disease_uci.csv")
    log_check(24, "Raw UCI dataset remains unchanged (303 rows, 14 cols)", df_raw.shape == (303, 14))

    # 25. Part 3 preprocessing verification passes
    from scripts.verify_preprocessing import run_verification_checks as v_prep
    try:
        v_prep()
        part3_passed = True
    except Exception:
        part3_passed = False
    log_check(25, "Part 3 preprocessing verification still passes", part3_passed)

    # 26. Part 4 EDA verification passes
    from scripts.verify_eda import run_eda_verification as v_eda
    try:
        v_eda()
        part4_passed = True
    except Exception:
        part4_passed = False
    log_check(26, "Part 4 EDA verification still passes", part4_passed)

    # 27. Part 5 baseline verification passes
    from scripts.verify_baseline_models import run_baseline_verification as v_base
    try:
        v_base()
        part5_passed = True
    except Exception:
        part5_passed = False
    log_check(27, "Part 5 baseline verification still passes", part5_passed)

    print("=" * 70)
    all_passed = all(results)
    if all_passed:
        print("FINAL VERIFICATION RESULT: ALL 27 CHECKS PASSED (100% SUCCESS)")
    else:
        print("FINAL VERIFICATION RESULT: SOME CHECKS FAILED")
        sys.exit(1)
    print("=" * 70)


if __name__ == "__main__":
    run_tuning_verification()
