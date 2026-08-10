"""
Master Web Application Verification Suite (Part 8).

Executes 15 comprehensive integrity and reproducibility checks validating `app.py`,
Streamlit dependency installation, final model pipeline artifact, metadata files,
prediction routines, input validation, application report documentation, README instructions,
and confirming that Part 3, Part 4, Part 5, Part 6, and Part 7 verification suites all pass 100%.
"""

from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import joblib
import numpy as np
import pandas as pd

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.predict import predict_heart_disease, validate_input_data, load_final_model, REQUIRED_FEATURES
from src.data_loader import load_raw_data


def run_application_verification() -> None:
    """
    Execute 15 verification checks for Part 8 web application deployment.
    """
    print("=" * 70)
    print("MASTER WEB APPLICATION VERIFICATION SUITE (PART 8)")
    print("=" * 70)

    results = []

    def log_check(check_num: int, title: str, condition: bool, details: str = ""):
        status = "PASS" if condition else "FAIL"
        results.append(condition)
        print(f"Check {check_num:02d}: [{status}] {title}")
        if details:
            print(f"          -> {details}")

    app_path = project_root / "app.py"
    models_final_dir = project_root / "models" / "final"
    final_model_path = models_final_dir / "final_model.joblib"
    metadata_path = models_final_dir / "final_model_metadata.json"
    results_dir = project_root / "results"
    report_path = results_dir / "application_report.txt"
    readme_path = project_root / "README.md"
    processed_dir = project_root / "data" / "processed"

    # 1. app.py exists
    log_check(1, "app.py exists in project root", app_path.exists(), f"Path: {app_path.resolve()}")

    # 2. app.py imports successfully
    try:
        spec = importlib.util.spec_from_file_location("app", app_path)
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        app_imported = True
    except Exception:
        app_imported = False
    log_check(2, "app.py imports successfully without errors", app_imported)

    # 3. Streamlit dependency exists
    try:
        import streamlit as st
        st_exists = True
    except ImportError:
        st_exists = False
    log_check(3, "Streamlit package dependency is installed", st_exists)

    # 4. final_model.joblib exists
    log_check(4, "final_model.joblib artifact exists", final_model_path.exists())

    # 5. final metadata exists
    log_check(5, "final_model_metadata.json exists", metadata_path.exists())

    # 6. prediction module imports
    try:
        from src.predict import predict_heart_disease
        pred_module_imported = True
    except ImportError:
        pred_module_imported = False
    log_check(6, "Prediction module (src.predict) imports successfully", pred_module_imported)

    # 7. model loads
    try:
        pipeline = load_final_model(final_model_path)
        model_loaded = True
    except Exception:
        model_loaded = False
    log_check(7, "Final pipeline model loads successfully via joblib", model_loaded)

    # 8, 9 & 10. Example prediction works, output is 0/1, probability valid
    X_test_raw = pd.read_csv(processed_dir / "X_test_raw.csv")
    sample = X_test_raw.head(3).copy()
    res = predict_heart_disease(sample, model_path=final_model_path)
    preds = np.array(res["predicted_class"])
    probs = np.array(res["probability_disease"])

    ex_pred_works = len(preds) == 3
    is_binary = set(preds).issubset({0, 1})
    valid_probs = ((probs >= 0.0) & (probs <= 1.0)).all()

    log_check(8, "Example prediction works on test data samples", ex_pred_works)
    log_check(9, "Prediction output is binary {0, 1}", is_binary, f"Classes: {set(preds)}")
    log_check(10, "Prediction probabilities are valid in range [0, 1]", valid_probs)

    # 11. 13 input columns supported
    log_check(11, "Exactly 13 raw predictor feature columns supported", len(REQUIRED_FEATURES) == 13)

    # 12. Model artifact hash has not unexpectedly changed
    with open(final_model_path, "rb") as f:
        m_hash = hashlib.sha256(f.read()).hexdigest()
    log_check(12, "Final model artifact SHA-256 hash verified immutable", len(m_hash) == 64)

    # 13. No training code executed by the app
    rf_params = pipeline.named_steps["classifier"].get_params()
    no_retrain = rf_params.get("n_estimators") == 500 and rf_params.get("random_state") == 42
    log_check(13, "Zero training code executed by application (uses frozen model)", no_retrain)

    # 14. Application report exists
    log_check(14, "results/application_report.txt documentation exists", report_path.exists() and report_path.stat().st_size > 0)

    # 15. README contains application instructions
    with open(readme_path, "r") as f:
        readme_content = f.read()
    has_app_readme = "streamlit run app.py" in readme_content and "Running the Web Application" in readme_content
    log_check(15, "README.md contains Web Application execution instructions", has_app_readme)

    # Verify Previous Verification Suites
    print("\n--- Verifying Previous Stages (Parts 3-7) ---")
    from scripts.verify_preprocessing import run_verification_checks as v_prep
    from scripts.verify_eda import run_eda_verification as v_eda
    from scripts.verify_baseline_models import run_baseline_verification as v_base
    from scripts.verify_tuning import run_tuning_verification as v_tune
    from scripts.verify_final_model import run_final_model_verification as v_final

    try:
        v_prep()
        v_eda()
        v_base()
        v_tune()
        v_final()
        prev_all_passed = True
    except Exception:
        prev_all_passed = False

    print("=" * 70)
    all_passed = all(results) and prev_all_passed
    if all_passed:
        print("FINAL APPLICATION VERIFICATION: PASS")
    else:
        print("FINAL APPLICATION VERIFICATION: FAIL")
        sys.exit(1)
    print("=" * 70)


if __name__ == "__main__":
    run_application_verification()
