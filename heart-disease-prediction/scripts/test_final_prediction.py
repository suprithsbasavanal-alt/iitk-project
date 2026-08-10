"""
Final Model Prediction and Reloading Verification Script (Part 7).

Verifies that the serialized final model pipeline artifact ('models/final/final_model.joblib')
loads cleanly, accepts raw patient clinical features, performs schema validation, generates valid
binary class predictions (0/1) and probabilities in range [0, 1], and produces 100% identical
predictions across reloaded instances.
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

from src.predict import predict_heart_disease, load_final_model, validate_input_data


def test_final_prediction_and_reloading() -> None:
    """
    Execute prediction testing and model reload verification checks.
    """
    print("=" * 70)
    print("STARTING FINAL MODEL PREDICTION & RELOADING VERIFICATION TEST")
    print("=" * 70)

    processed_dir = project_root / "data" / "processed"
    final_model_path = project_root / "models" / "final" / "final_model.joblib"

    # Step 1: Load sample raw test rows
    X_test_raw = pd.read_csv(processed_dir / "X_test_raw.csv")
    sample_rows = X_test_raw.head(10).copy()

    print(f"Loaded 10 Sample Rows from X_test_raw for Inference Testing. Shape: {sample_rows.shape}")

    # Step 2: Test prediction function on DataFrame input
    res_df = predict_heart_disease(sample_rows, model_path=final_model_path)

    preds_df = np.array(res_df["predicted_class"])
    probs_df = np.array(res_df["probability_disease"])
    probs_no_df = np.array(res_df["probability_no_disease"])

    assert preds_df.shape == (10,), f"Expected prediction shape (10,), got {preds_df.shape}"
    assert probs_df.shape == (10,), f"Expected probability shape (10,), got {probs_df.shape}"
    assert set(preds_df).issubset({0, 1}), f"Predicted classes must be binary {{0, 1}}, got {set(preds_df)}"
    assert ((probs_df >= 0.0) & (probs_df <= 1.0)).all(), "Probabilities must be in range [0, 1]"
    assert np.allclose(probs_df + probs_no_df, 1.0), "Probabilities for disease + no_disease must sum to 1.0"

    print("Check 01: [PASS] DataFrame prediction shape and probability ranges are valid.")

    # Step 3: Test prediction function on single dict input
    sample_dict = sample_rows.iloc[0].to_dict()
    res_dict = predict_heart_disease(sample_dict, model_path=final_model_path)

    assert len(res_dict["predicted_class"]) == 1, "Single dict input must return 1 prediction"
    assert res_dict["predicted_class"][0] in [0, 1], "Single prediction class must be binary 0 or 1"
    assert "Model prediction:" in res_dict["prediction_message"][0], "Prediction message must use 'Model prediction:' prefix"

    print("Check 02: [PASS] Single dict prediction & message formatting are valid.")

    # Step 4: Verify Model Reloading Integrity & 100% Prediction Match
    m1 = load_final_model(final_model_path)
    m2 = load_final_model(final_model_path)

    pred1 = m1.predict(X_test_raw)
    pred2 = m2.predict(X_test_raw)

    prob1 = m1.predict_proba(X_test_raw)[:, 1]
    prob2 = m2.predict_proba(X_test_raw)[:, 1]

    assert np.array_equal(pred1, pred2), "Reloaded model predictions must match 100%"
    assert np.allclose(prob1, prob2), "Reloaded model probabilities must match 100%"

    print("Check 03: [PASS] Reloaded model artifact produces 100% identical predictions.")

    print("=" * 70)
    print("ALL FINAL MODEL PREDICTION & RELOADING TESTS PASSED (100% SUCCESS)")
    print("=" * 70)


if __name__ == "__main__":
    test_final_prediction_and_reloading()
