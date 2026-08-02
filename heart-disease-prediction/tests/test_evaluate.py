"""
Unit Tests for Model Evaluation Module (Part 5).

Tests metric calculation accuracy, specificity formula, confusion matrix parameters, and report generation.
"""

from pathlib import Path
import sys
import unittest
import numpy as np

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.evaluate import calculate_metrics, calculate_specificity


class TestEvaluate(unittest.TestCase):
    """Test suite for src/evaluate.py module."""

    def test_specificity_calculation(self):
        """Test Specificity formula: TN / (TN + FP)."""
        # TN=8, FP=2, FN=1, TP=9
        y_true = np.array([0]*10 + [1]*10)
        y_pred = np.array([0]*8 + [1]*2 + [0]*1 + [1]*9)

        spec = calculate_specificity(y_true, y_pred)
        self.assertAlmostEqual(spec, 8 / 10, places=4)

    def test_calculate_metrics(self):
        """Test comprehensive metric dictionary calculations."""
        y_true = np.array([0, 0, 0, 0, 1, 1, 1, 1])
        y_pred = np.array([0, 0, 0, 1, 0, 1, 1, 1])
        y_prob = np.array([0.1, 0.2, 0.3, 0.7, 0.4, 0.8, 0.9, 0.95])

        metrics = calculate_metrics(y_true, y_pred, y_prob)

        self.assertEqual(metrics["TN"], 3)
        self.assertEqual(metrics["FP"], 1)
        self.assertEqual(metrics["FN"], 1)
        self.assertEqual(metrics["TP"], 3)
        self.assertAlmostEqual(metrics["Accuracy"], 6 / 8, places=4)
        self.assertAlmostEqual(metrics["Specificity"], 3 / 4, places=4)
        self.assertAlmostEqual(metrics["Recall"], 3 / 4, places=4)
        self.assertAlmostEqual(metrics["Precision"], 3 / 4, places=4)
        self.assertGreater(metrics["ROC_AUC"], 0.5)


if __name__ == "__main__":
    unittest.main()
