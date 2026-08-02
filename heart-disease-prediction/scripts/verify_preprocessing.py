"""
Preprocessing Pipeline Verification Script.

This script executes 14 comprehensive integrity checks to ensure that target conversion,
train/test splitting, ColumnTransformer construction, and data leakage prevention
operate correctly and safely.
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

from src.data_loader import load_raw_data
from src.preprocessing import (
    create_binary_target,
    get_feature_groups,
    prepare_features_and_target,
    split_data,
    build_preprocessor,
)


def run_verification_checks() -> None:
    """
    Execute 14 verification checks for Part 3 preprocessing pipeline.
    """
    print("=" * 60)
    print("PREPROCESSING PIPELINE VERIFICATION SUITE (PART 3)")
    print("=" * 60)

    results = []

    def log_check(check_num: int, title: str, condition: bool, details: str = ""):
        status = "PASS" if condition else "FAIL"
        results.append(condition)
        print(f"Check {check_num:02d}: [{status}] {title}")
        if details:
            print(f"          -> {details}")

    # Load raw dataset
    raw_path = project_root / "data" / "raw" / "heart_disease_uci.csv"
    df_raw = load_raw_data(raw_path)

    # 1. Raw dataset loads correctly
    log_check(1, "Raw dataset loads correctly", df_raw is not None and not df_raw.empty)

    # 2. Raw dataset still has 303 rows
    log_check(2, "Raw dataset has 303 rows", df_raw.shape[0] == 303, f"Actual rows: {df_raw.shape[0]}")

    # 3. Raw target contains original values 0-4
    raw_target_vals = set(df_raw["num"].unique())
    log_check(3, "Raw target 'num' contains values 0-4", raw_target_vals == {0, 1, 2, 3, 4}, f"Values: {raw_target_vals}")

    # 4. Binary target contains only 0 and 1
    y_binary = create_binary_target(df_raw, raw_target_col="num")
    binary_vals = set(y_binary.unique())
    log_check(4, "Binary target contains only {0, 1}", binary_vals == {0, 1}, f"Values: {binary_vals}")

    # 5. Binary distribution is 0=164, 1=139
    counts = y_binary.value_counts().to_dict()
    expected_dist = {0: 164, 1: 139}
    log_check(5, "Binary target distribution is {0: 164, 1: 139}", counts == expected_dist, f"Actual distribution: {counts}")

    # 6. Feature matrix X does not contain target columns 'num' or 'target'
    X, y = prepare_features_and_target(df_raw)
    no_target_in_X = ("num" not in X.columns) and ("target" not in X.columns)
    log_check(6, "Feature matrix X excludes 'num' and 'target'", no_target_in_X, f"Columns: {list(X.columns)}")

    # 7. Train/Test split row index overlap check
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.20, random_state=42)
    overlap = set(X_train.index).intersection(set(X_test.index))
    log_check(7, "Train and Test splits have no overlapping row indices", len(overlap) == 0, f"Overlapping indices count: {len(overlap)}")

    # 8. Total train + test rows equal 303
    total_split_rows = X_train.shape[0] + X_test.shape[0]
    log_check(8, "Total train + test rows equal 303", total_split_rows == 303, f"Train ({X_train.shape[0]}) + Test ({X_test.shape[0]}) = {total_split_rows}")

    # 9. Preprocessor fits on training data ONLY
    num_features, cat_features = get_feature_groups()
    preprocessor = build_preprocessor(num_features, cat_features)
    preprocessor.fit(X_train)
    log_check(9, "Preprocessor fits strictly on X_train without error", hasattr(preprocessor, "transformers_"))

    # 10. Training data transforms successfully
    X_train_trans = preprocessor.transform(X_train)
    log_check(10, "X_train transforms successfully", X_train_trans.shape[0] == X_train.shape[0])

    # 11. Test data transforms successfully
    X_test_trans = preprocessor.transform(X_test)
    log_check(11, "X_test transforms successfully", X_test_trans.shape[0] == X_test.shape[0])

    # 12. No NaN values remain in transformed matrices
    nans_train = np.isnan(X_train_trans).sum()
    nans_test = np.isnan(X_test_trans).sum()
    log_check(12, "Zero NaN values in transformed matrices", (nans_train + nans_test) == 0, f"Train NaNs: {nans_train}, Test NaNs: {nans_test}")

    # 13. Train and test transformed matrices have identical feature counts
    log_check(13, "Train and test transformed matrices have identical feature count", X_train_trans.shape[1] == X_test_trans.shape[1], f"Transformed features: {X_train_trans.shape[1]}")

    # 14. Saved preprocessor loads successfully from models/preprocessor.joblib
    preprocessor_file = project_root / "models" / "preprocessor.joblib"
    loaded_preprocessor = joblib.load(preprocessor_file)
    X_test_loaded_trans = loaded_preprocessor.transform(X_test)
    is_identical = np.allclose(X_test_trans, X_test_loaded_trans)
    log_check(14, "Saved preprocessor loads from joblib and produces identical transforms", is_identical, f"File: {preprocessor_file}")

    print("=" * 60)
    all_passed = all(results)
    if all_passed:
        print("FINAL VERIFICATION RESULT: ALL 14 CHECKS PASSED (100% SUCCESS)")
    else:
        print("FINAL VERIFICATION RESULT: SOME CHECKS FAILED")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    run_verification_checks()
