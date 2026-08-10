"""
Unit Tests for Final Machine Learning Model and Inference Routines (Part 7).

Tests final model prediction functionality, input data schema validation, error handling,
metadata structure, and reload consistency.
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


class TestFinalModel(unittest.TestCase):
    """Test suite for Part 7 final model selection and inference pipeline."""

    @classmethod
    def setUpClass(cls):
        """Load sample data for testing."""
        cls.processed_dir = project_root / "data" / "processed"
        cls.X_test_raw = pd.read_csv(cls.processed_dir / "X_test_raw.csv")
        cls.final_model_path = project_root / "models" / "final" / "final_model.joblib"
        cls.metadata_path = project_root / "models" / "final" / "final_model_metadata.json"

    def test_required_features_list(self):
        """Test that exactly 13 predictor features are defined."""
        self.assertEqual(len(REQUIRED_FEATURES), 13)
        self.assertIn("age", REQUIRED_FEATURES)
        self.assertIn("thal", REQUIRED_FEATURES)

    def test_validate_input_data_success(self):
        """Test validate_input_data succeeds with valid DataFrame."""
        sample_df = self.X_test_raw.head(5)
        validated = validate_input_data(sample_df)
        self.assertEqual(validated.shape, (5, 13))
        self.assertEqual(list(validated.columns), REQUIRED_FEATURES)

    def test_validate_input_data_missing_column(self):
        """Test validate_input_data raises ValueError when a feature column is missing."""
        invalid_df = self.X_test_raw.drop(columns=["chol"]).head(2)
        with self.assertRaises(ValueError):
            validate_input_data(invalid_df)

    def test_validate_input_data_invalid_type(self):
        """Test validate_input_data raises TypeError for non-df non-dict inputs."""
        with self.assertRaises(TypeError):
            validate_input_data(["invalid", "list"])

    def test_predict_heart_disease_df_input(self):
        """Test predict_heart_disease returns structured prediction dict for DataFrame input."""
        sample_df = self.X_test_raw.head(3)
        res = predict_heart_disease(sample_df, model_path=self.final_model_path)
        
        self.assertIn("predicted_class", res)
        self.assertIn("predicted_label", res)
        self.assertIn("probability_disease", res)
        self.assertEqual(len(res["predicted_class"]), 3)
        self.assertTrue(set(res["predicted_class"]).issubset({0, 1}))
        for p in res["probability_disease"]:
            self.assertGreaterEqual(p, 0.0)
            self.assertLessEqual(p, 1.0)

    def test_predict_heart_disease_dict_input(self):
        """Test predict_heart_disease returns structured prediction dict for dictionary input."""
        sample_dict = self.X_test_raw.iloc[0].to_dict()
        res = predict_heart_disease(sample_dict, model_path=self.final_model_path)
        
        self.assertEqual(len(res["predicted_class"]), 1)
        self.assertIn(res["predicted_class"][0], [0, 1])
        self.assertTrue(res["prediction_message"][0].startswith("Model prediction:"))

    def test_final_model_metadata_content(self):
        """Test that final_model_metadata.json contains expected fields."""
        self.assertTrue(self.metadata_path.exists())
        with open(self.metadata_path, "r") as f:
            meta = json.load(f)
        
        self.assertEqual(meta["selected_model"], "Tuned Random Forest")
        self.assertEqual(meta["training_rows"], 242)
        self.assertEqual(meta["test_rows"], 61)
        self.assertEqual(meta["random_state"], 42)
        self.assertIn("hyperparameters", meta)
        self.assertEqual(meta["hyperparameters"]["n_estimators"], 500)


if __name__ == "__main__":
    unittest.main()
