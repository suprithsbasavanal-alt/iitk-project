"""
EDA Verification Script (Part 4).

Verifies dataset shape integrity, presence and non-emptiness of all 6 summary CSV/TXT
reports, non-empty existence of all 21 figure PNG files, and confirms zero model training.
"""

from pathlib import Path
import sys
import pandas as pd

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.data_loader import load_raw_data


def run_eda_verification() -> None:
    """
    Execute 14 verification checks for Part 4 EDA module.
    """
    print("=" * 60)
    print("EXPLORATORY DATA ANALYSIS (EDA) VERIFICATION SUITE (PART 4)")
    print("=" * 60)

    results = []

    def log_check(check_num: int, title: str, condition: bool, details: str = ""):
        status = "PASS" if condition else "FAIL"
        results.append(condition)
        print(f"Check {check_num:02d}: [{status}] {title}")
        if details:
            print(f"          -> {details}")

    raw_path = project_root / "data" / "raw" / "heart_disease_uci.csv"
    df_raw = load_raw_data(raw_path)

    # 1. Raw dataset shape 303 rows
    log_check(1, "Raw dataset has 303 rows", df_raw.shape[0] == 303, f"Actual rows: {df_raw.shape[0]}")

    # 2. Raw dataset 14 columns
    log_check(2, "Raw dataset has 14 columns", df_raw.shape[1] == 14, f"Actual columns: {df_raw.shape[1]}")

    # 3. Raw 'num' target unchanged
    raw_num_vals = set(df_raw["num"].unique())
    log_check(3, "Raw target 'num' values remain {0,1,2,3,4}", raw_num_vals == {0, 1, 2, 3, 4}, f"Values: {raw_num_vals}")

    # 4. Binary target 164 / 139
    binary_y = df_raw["num"].apply(lambda x: 0 if x == 0 else 1)
    counts = binary_y.value_counts().to_dict()
    log_check(4, "Binary target distribution is {0: 164, 1: 139}", counts == {0: 164, 1: 139}, f"Actual: {counts}")

    # 5. Missing counts ca=4, thal=2
    missing_dict = df_raw.isnull().sum()[df_raw.isnull().sum() > 0].to_dict()
    log_check(5, "Missing counts remain ca=4, thal=2", missing_dict == {"ca": 4, "thal": 2}, f"Actual: {missing_dict}")

    # 6. Duplicate count remains 0
    dups = df_raw.duplicated().sum()
    log_check(6, "Duplicate count remains 0", dups == 0, f"Duplicates: {dups}")

    # 7. eda_numerical_summary.csv exists and non-empty
    num_csv = project_root / "results" / "eda_numerical_summary.csv"
    log_check(7, "eda_numerical_summary.csv exists and is non-empty", num_csv.exists() and num_csv.stat().st_size > 0, f"Path: {num_csv}")

    # 8. eda_categorical_summary.csv exists and non-empty
    cat_csv = project_root / "results" / "eda_categorical_summary.csv"
    log_check(8, "eda_categorical_summary.csv exists and is non-empty", cat_csv.exists() and cat_csv.stat().st_size > 0, f"Path: {cat_csv}")

    # 9. eda_correlation_matrix.csv exists and non-empty
    corr_csv = project_root / "results" / "eda_correlation_matrix.csv"
    log_check(9, "eda_correlation_matrix.csv exists and is non-empty", corr_csv.exists() and corr_csv.stat().st_size > 0, f"Path: {corr_csv}")

    # 10. eda_outlier_summary.csv exists and non-empty
    outlier_csv = project_root / "results" / "eda_outlier_summary.csv"
    log_check(10, "eda_outlier_summary.csv exists and is non-empty", outlier_csv.exists() and outlier_csv.stat().st_size > 0, f"Path: {outlier_csv}")

    # 11. eda_report.txt exists and non-empty
    report_txt = project_root / "results" / "eda_report.txt"
    log_check(11, "eda_report.txt exists and is non-empty", report_txt.exists() and report_txt.stat().st_size > 0, f"Path: {report_txt}")

    # 12 & 13. Check all 21 expected figure PNG files exist and are non-empty
    fig_dir = project_root / "results" / "figures"
    expected_figs = [
        "01_target_distribution.png", "02_age_distribution.png", "03_trestbps_distribution.png",
        "04_chol_distribution.png", "05_thalach_distribution.png", "06_oldpeak_distribution.png",
        "07_age_by_target.png", "08_trestbps_by_target.png", "09_chol_by_target.png",
        "10_thalach_by_target.png", "11_oldpeak_by_target.png", "12_heart_disease_by_sex.png",
        "13_heart_disease_by_chest_pain.png", "14_heart_disease_by_fbs.png", "15_heart_disease_by_restecg.png",
        "16_heart_disease_by_exang.png", "17_heart_disease_by_slope.png", "18_heart_disease_by_ca.png",
        "19_heart_disease_by_thal.png", "20_correlation_matrix.png", "21_missing_values.png"
    ]

    all_figs_exist = all((fig_dir / f).exists() for f in expected_figs)
    all_figs_non_empty = all((fig_dir / f).stat().st_size > 0 for f in expected_figs if (fig_dir / f).exists())

    log_check(12, "All 21 expected figure PNG files exist in results/figures/", all_figs_exist, f"Found {len(list(fig_dir.glob('*.png')))} PNG files")
    log_check(13, "All 21 figure PNG files are non-empty (>0 bytes)", all_figs_non_empty)

    # 14. Confirm zero ML prediction model files in models/
    models_dir = project_root / "models"
    model_files = [f for f in models_dir.glob("*") if f.suffix in [".pkl", ".joblib", ".h5"] and f.name != "preprocessor.joblib"]
    log_check(14, "Zero prediction model files created in models/", len(model_files) == 0, f"Non-preprocessor model count: {len(model_files)}")

    print("=" * 60)
    all_passed = all(results)
    if all_passed:
        print("FINAL VERIFICATION RESULT: ALL 14 CHECKS PASSED (100% SUCCESS)")
    else:
        print("FINAL VERIFICATION RESULT: SOME CHECKS FAILED")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    run_eda_verification()
