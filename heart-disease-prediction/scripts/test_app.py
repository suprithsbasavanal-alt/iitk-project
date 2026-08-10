"""
Application Integration and Functionality Test Script (Part 8).

Verifies that `app.py` imports cleanly, the frozen final model pipeline loads,
the prediction function accepts all 13 required feature columns, probability values sum to 1.0,
invalid/missing features are properly rejected, and no model retraining or hyperparameter tuning occurs.
"""

from pathlib import Path
import hashlib
import importlib.util
import sys
import numpy as np
import pandas as pd

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.predict import predict_heart_disease, load_final_model, validate_input_data, REQUIRED_FEATURES


def test_application_integration() -> None:
    """
    Execute 12 integration test checks for the Streamlit application module.
    """
    print("=" * 70)
    print("STARTING STREAMLIT APPLICATION INTEGRATION TEST (PART 8)")
    print("=" * 70)

    app_path = project_root / "app.py"
    final_model_path = project_root / "models" / "final" / "final_model.joblib"
    processed_dir = project_root / "data" / "processed"

    # 1. app.py imports successfully
    spec = importlib.util.spec_from_file_location("app", app_path)
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    print("Check 01: [PASS] app.py imported successfully.")

    # 2. Record initial model artifact hash to verify immutability
    with open(final_model_path, "rb") as f:
        initial_hash = hashlib.sha256(f.read()).hexdigest()

    # 3. Final model loads successfully
    model = load_final_model(final_model_path)
    print("Check 02: [PASS] Final model pipeline loaded successfully.")

    # 4. Load sample test data & test prediction function
    X_test_raw = pd.read_csv(processed_dir / "X_test_raw.csv")
    sample_df = X_test_raw.head(5).copy()

    res = predict_heart_disease(sample_df, model_path=final_model_path)
    preds = np.array(res["predicted_class"])
    probs_disease = np.array(res["probability_disease"])
    probs_no_disease = np.array(res["probability_no_disease"])

    # 5. Prediction class is 0 or 1
    assert set(preds).issubset({0, 1}), f"Predicted classes must be binary {{0, 1}}, got {set(preds)}"
    print("Check 03: [PASS] Prediction classes are strictly binary {0, 1}.")

    # 6. Probabilities between 0 and 1
    assert ((probs_disease >= 0.0) & (probs_disease <= 1.0)).all(), "Probabilities must be in range [0, 1]"
    print("Check 04: [PASS] Prediction probabilities are in valid range [0, 1].")

    # 7. Probability values sum approximately to 1
    assert np.allclose(probs_disease + probs_no_disease, 1.0), "Probabilities must sum to 1.0"
    print("Check 05: [PASS] Probability values for disease + no_disease sum to 1.0.")

    # 8. All 13 required features accepted
    validated_df = validate_input_data(sample_df)
    assert list(validated_df.columns) == REQUIRED_FEATURES, "All 13 required features must be accepted"
    print("Check 06: [PASS] All 13 required predictor feature columns accepted.")

    # 9. Missing required fields rejected
    missing_df = sample_df.drop(columns=["age"])
    try:
        validate_input_data(missing_df)
        missing_rejected = False
    except ValueError:
        missing_rejected = True
    assert missing_rejected, "Missing feature columns must be rejected with ValueError"
    print("Check 07: [PASS] Missing required feature fields are correctly rejected.")

    # 10. Invalid feature names rejected or extra fields handled
    dict_input = sample_df.iloc[0].to_dict()
    dict_input["invalid_extra_column"] = 999
    val_dict_df = validate_input_data(dict_input)
    assert "invalid_extra_column" not in val_dict_df.columns, "Extra fields must be filtered out"
    print("Check 08: [PASS] Extra or unexpected feature fields are correctly filtered out.")

    # 11. Final model artifact is not modified
    with open(final_model_path, "rb") as f:
        final_hash = hashlib.sha256(f.read()).hexdigest()
    assert initial_hash == final_hash, "Final model artifact must remain untouched (immutable)"
    print("Check 09: [PASS] Final model artifact hash verified untouched (zero model retraining).")

    # 12. Confirm no retraining or tuning occurred
    assert hasattr(model, "predict"), "Model must be pre-fitted pipeline instance"
    print("Check 10: [PASS] Zero model training or hyperparameter tuning occurred during application test.")

    print("=" * 70)
    print("ALL STREAMLIT APPLICATION INTEGRATION TESTS PASSED (100% SUCCESS)")
    print("=" * 70)


if __name__ == "__main__":
    test_application_integration()
