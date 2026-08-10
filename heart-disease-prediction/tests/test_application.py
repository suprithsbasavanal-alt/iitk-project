"""
Unit Tests for Streamlit Application Integration (Part 8).

Tests model pipeline loading, prediction execution, probability ranges, feature requirements,
input validation, and malformed input handling without starting a live Streamlit server process.
"""

from pathlib import Path
import json
import sys
import unittest
import numpy as np
import pandas as pd

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.predict import predict_heart_disease, validate_input_data, load_final_model, REQUIRED_FEATURES


class TestApplication(unittest.TestCase):
    """Test suite for Part 8 Streamlit application backend functions."""

    @classmethod
    def setUpClass(cls):
        """Set up file paths and test data."""
        cls.final_model_path = project_root / "models" / "final" / "final_model.joblib"
        cls.X_test_raw = pd.read_csv(project_root / "data" / "processed" / "X_test_raw.csv")

    def test_model_loading(self):
        """Test that load_final_model loads the frozen final model pipeline."""
        model = load_final_model(self.final_model_path)
        self.assertIsNotNone(model)
        self.assertTrue(hasattr(model, "predict"))

    def test_valid_prediction(self):
        """Test predict_heart_disease generates valid predictions for test data."""
        sample = self.X_test_raw.head(3)
        res = predict_heart_disease(sample, model_path=self.final_model_path)
        
        self.assertIn("predicted_class", res)
        self.assertEqual(len(res["predicted_class"]), 3)
        self.assertTrue(set(res["predicted_class"]).issubset({0, 1}))

    def test_probability_range_and_sum(self):
        """Test probability outputs are in [0, 1] and sum to 1.0."""
        sample = self.X_test_raw.head(5)
        res = predict_heart_disease(sample, model_path=self.final_model_path)
        
        p_disease = np.array(res["probability_disease"])
        p_no_disease = np.array(res["probability_no_disease"])
        
        self.assertTrue(((p_disease >= 0.0) & (p_disease <= 1.0)).all())
        self.assertTrue(((p_no_disease >= 0.0) & (p_no_disease <= 1.0)).all())
        self.assertTrue(np.allclose(p_disease + p_no_disease, 1.0))

    def test_required_features(self):
        """Test that REQUIRED_FEATURES contains all 13 predictor columns."""
        self.assertEqual(len(REQUIRED_FEATURES), 13)
        expected = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
        self.assertEqual(REQUIRED_FEATURES, expected)

    def test_input_validation(self):
        """Test validate_input_data enforces column ordering and numeric types."""
        sample_dict = {
            "thal": 3, "ca": 0, "slope": 1, "oldpeak": 1.0, "exang": 0,
            "thalach": 150, "restecg": 0, "fbs": 0, "chol": 240,
            "trestbps": 130, "cp": 1, "sex": 1, "age": 55
        }
        val_df = validate_input_data(sample_dict)
        self.assertEqual(list(val_df.columns), REQUIRED_FEATURES)

    def test_malformed_input_handling(self):
        """Test validate_input_data raises ValueError for missing features or non-numeric types."""
        # Missing feature
        missing_dict = {"age": 55, "sex": 1}
        with self.assertRaises(ValueError):
            validate_input_data(missing_dict)

        # Non-numeric invalid value
        invalid_dict = self.X_test_raw.iloc[0].to_dict()
        invalid_dict["age"] = "invalid_string_age"
        with self.assertRaises(ValueError):
            validate_input_data(invalid_dict)


if __name__ == "__main__":
    unittest.main()
