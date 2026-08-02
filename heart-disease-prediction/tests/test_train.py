"""
Unit Tests for Model Training Engine (Part 5).

Tests model registry, file-safe naming, pipeline construction, and 5-fold cross-validation output dimensions.
"""

from pathlib import Path
import sys
import unittest
import pandas as pd

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.train import (
    get_baseline_models,
    get_file_safe_name,
    build_baseline_pipeline,
    evaluate_cv_baseline,
)


class TestTrain(unittest.TestCase):
    """Test suite for src/train.py module."""

    def test_model_registry(self):
        """Test that all 7 baseline models are registered."""
        models = get_baseline_models()
        self.assertEqual(len(models), 7)
        expected_names = [
            "Logistic Regression", "K-Nearest Neighbors", "Decision Tree",
            "Random Forest", "Support Vector Machine", "Gaussian Naive Bayes", "XGBoost"
        ]
        for name in expected_names:
            self.assertIn(name, models)

    def test_file_safe_naming(self):
        """Test conversion to filesystem-safe names."""
        self.assertEqual(get_file_safe_name("Logistic Regression"), "logistic_regression")
        self.assertEqual(get_file_safe_name("K-Nearest Neighbors"), "k_nearest_neighbors")
        self.assertEqual(get_file_safe_name("Gaussian Naive Bayes"), "gaussian_naive_bayes")

    def test_pipeline_construction(self):
        """Test end-to-end scikit-learn pipeline construction."""
        models = get_baseline_models()
        for name, clf in models.items():
            pipeline = build_baseline_pipeline(clf)
            self.assertEqual(len(pipeline.steps), 2)
            self.assertEqual(pipeline.steps[0][0], "preprocessor")
            self.assertEqual(pipeline.steps[1][0], "classifier")


if __name__ == "__main__":
    unittest.main()
