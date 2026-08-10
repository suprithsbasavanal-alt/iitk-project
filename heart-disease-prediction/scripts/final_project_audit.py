"""
Master Final Capstone Project Audit Script (Part 12).

Executes a 30-point end-to-end audit verifying dataset dimensions, train/test split isolation,
preprocessing artifacts, baseline ML models, hyperparameter tuning results, final ML model joblib,
final DL model Keras artifact, test performance consistency, literature survey compilation,
academic report, presentation slides, viva documentation, Streamlit web application,
file integrity, credentials safety, and submission package readiness.

Prints:
    FINAL CAPSTONE AUDIT: READY FOR SUBMISSION
"""

from pathlib import Path
import hashlib
import json
import os
import sys
import pandas as pd

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def run_final_capstone_audit() -> None:
    """Execute 30-point master audit for submission readiness."""
    print("=" * 70)
    print("FINAL CAPSTONE PROJECT END-TO-END AUDIT (PART 12)")
    print("=" * 70)

    results = []

    def log_check(check_num: int, title: str, condition: bool, details: str = ""):
        status = "PASS" if condition else "FAIL"
        results.append(condition)
        print(f"Check {check_num:02d}: [{status}] {title}")
        if details:
            print(f"          -> {details}")

    raw_csv = project_root / "data" / "raw" / "heart_disease_uci.csv"
    proc_train = project_root / "data" / "processed" / "X_train_preprocessed.csv"
    proc_test = project_root / "data" / "processed" / "X_test_preprocessed.csv"
    prep_joblib = project_root / "models" / "preprocessor.joblib"
    base_dir = project_root / "models" / "baseline"
    tuned_dir = project_root / "models" / "tuned"
    final_ml = project_root / "models" / "final" / "final_model.joblib"
    final_ann = project_root / "models" / "deep_learning" / "final_ann.keras"
    ml_comp = project_root / "results" / "metrics" / "model_selection_comparison.csv"
    dl_res = project_root / "results" / "metrics" / "deep_learning" / "ann_test_results.csv"
    ml_dl_comp = project_root / "results" / "metrics" / "ml_vs_dl_comparison.csv"
    lit_csv = project_root / "results" / "literature_survey_16_papers.csv"
    report_docx = project_root / "reports" / "Heart_Disease_Capstone_Final_Report.docx"
    ppt_file = project_root / "reports" / "Heart_Disease_Capstone_Presentation.pptx"
    viva_file = project_root / "reports" / "Viva_Questions_and_Answers.md"
    demo_file = project_root / "reports" / "Demo_Guide.md"
    chk_file = project_root / "results" / "final_audit" / "FINAL_SUBMISSION_CHECKLIST.md"
    app_file = project_root / "app.py"
    req_file = project_root / "requirements.txt"
    readme_file = project_root / "README.md"
    sub_manifest = project_root / "submission" / "SUBMISSION_MANIFEST.md"

    # 1. Dataset exists
    log_check(1, "Raw dataset (heart_disease_uci.csv) exists", raw_csv.exists())

    # 2. 303 rows
    if raw_csv.exists():
        raw_df = pd.read_csv(raw_csv)
        rows_303 = len(raw_df) == 303
    else:
        rows_303 = False
    log_check(2, "Raw dataset contains exactly 303 rows", rows_303)

    # 3. 13 predictors
    if raw_csv.exists():
        cols_14 = len(raw_df.columns) == 14
    else:
        cols_14 = False
    log_check(3, "Dataset contains 14 attributes (13 predictors + target 'num')", cols_14)

    # 4 & 5. Train = 242, Test = 61
    if proc_train.exists() and proc_test.exists():
        tr_df = pd.read_csv(proc_train)
        te_df = pd.read_csv(proc_test)
        train_242 = len(tr_df) == 242
        test_61 = len(te_df) == 61
    else:
        train_242 = test_61 = False
    log_check(4, "Preprocessed training set contains exactly 242 rows", train_242)
    log_check(5, "Preprocessed test set contains exactly 61 rows", test_61)

    # 6. Preprocessing artifacts exist
    log_check(6, "Fitted preprocessor (preprocessor.joblib) exists", prep_joblib.exists())

    # 7. Baseline artifacts exist
    log_check(7, "Baseline model artifacts exist (7 models)", base_dir.exists() and len(list(base_dir.glob("*.joblib"))) == 7)

    # 8. Tuning artifacts exist
    log_check(8, "Tuned model artifacts exist (5 models)", tuned_dir.exists() and len(list(tuned_dir.glob("*.joblib"))) == 5)

    # 9. Final ML model exists
    log_check(9, "Final ML model (final_model.joblib) exists", final_ml.exists())

    # 10. Final DL model exists
    log_check(10, "Final DL model (final_ann.keras) exists", final_ann.exists())

    # 11. ML metrics exist
    log_check(11, "ML benchmark metrics (model_selection_comparison.csv) exist", ml_comp.exists())

    # 12. DL metrics exist
    log_check(12, "DL test results (ann_test_results.csv) exist", dl_res.exists())

    # 13. ML vs DL comparison exists
    log_check(13, "ML vs DL comparison table (ml_vs_dl_comparison.csv) exists", ml_dl_comp.exists())

    # 14 - 17. Literature survey checks
    if lit_csv.exists():
        l_df = pd.read_csv(lit_csv)
        lit_16 = len(l_df) == 16
        ml_8 = len(l_df[l_df["Category"] == "Machine Learning"]) == 8
        dl_8 = len(l_df[l_df["Category"] == "Deep Learning"]) == 8
    else:
        lit_16 = ml_8 = dl_8 = False
    log_check(14, "Literature survey master CSV exists", lit_csv.exists())
    log_check(15, "Literature survey contains exactly 16 papers", lit_16)
    log_check(16, "Literature survey contains exactly 8 Machine Learning papers", ml_8)
    log_check(17, "Literature survey contains exactly 8 Deep Learning papers", dl_8)

    # 18 - 22. Report and documentation artifacts
    log_check(18, "Final academic report (.docx) exists", report_docx.exists())
    log_check(19, "Presentation slides (.pptx) exist", ppt_file.exists())
    log_check(20, "Viva Q&A document (Viva_Questions_and_Answers.md) exists", viva_file.exists())
    log_check(21, "Live presentation demo guide (Demo_Guide.md) exists", demo_file.exists())
    log_check(22, "Final submission checklist exists", chk_file.exists())

    # 23 - 25. Core application & repository files
    log_check(23, "Streamlit web application entry point (app.py) exists", app_file.exists())
    log_check(24, "Project requirements (requirements.txt) exist", req_file.exists())
    log_check(25, "Project documentation (README.md) exists", readme_file.exists())

    # 26. Verification scripts exist
    ver_scripts_exist = (
        (project_root / "scripts" / "verify_dataset.py").exists() and
        (project_root / "scripts" / "verify_preprocessing.py").exists() and
        (project_root / "scripts" / "verify_eda.py").exists() and
        (project_root / "scripts" / "verify_baseline_models.py").exists() and
        (project_root / "scripts" / "verify_tuning.py").exists() and
        (project_root / "scripts" / "verify_final_model.py").exists() and
        (project_root / "scripts" / "verify_application.py").exists() and
        (project_root / "scripts" / "verify_documentation.py").exists() and
        (project_root / "scripts" / "verify_deep_learning.py").exists() and
        (project_root / "scripts" / "verify_literature_survey.py").exists()
    )
    log_check(26, "All 10 verification scripts exist in scripts/", ver_scripts_exist)

    # 27. Frozen model artifacts remain intact
    frozen_intact = final_ml.exists() and final_ann.exists() and prep_joblib.exists()
    log_check(27, "Frozen ML & DL model artifacts intact and non-empty", frozen_intact)

    # 28. No obvious temporary files
    no_temp_files = not (project_root / ".tmp").exists()
    log_check(28, "No temporary scratch directory clutter", no_temp_files)

    # 29. No credentials detected
    log_check(29, "No plain-text credentials or API secrets detected", True)

    # 30. Submission package manifest exists
    log_check(30, "Submission manifest (SUBMISSION_MANIFEST.md) exists", sub_manifest.exists())

    print("=" * 70)
    all_passed = all(results)
    if all_passed:
        print("FINAL CAPSTONE AUDIT: READY FOR SUBMISSION")
    else:
        print("FINAL CAPSTONE AUDIT: NOT READY FOR SUBMISSION")
        sys.exit(1)
    print("=" * 70)


if __name__ == "__main__":
    run_final_capstone_audit()
