"""
Unit Tests for Deep Learning (ANN) Module (Part 10).

Tests model building, layer dimensions, sigmoid output ranges, candidate architecture registry,
model saving/loading, and evaluation functions using fast synthetic inputs.
"""

from pathlib import Path
import json
import os
import sys
import unittest
import numpy as np
import pandas as pd

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.deep_learning import (
    build_ann_model,
    build_candidate_architectures,
    train_ann,
    evaluate_ann,
    save_ann_model,
    load_ann_model,
    predict_ann
)


class TestDeepLearning(unittest.TestCase):
    """Unit test suite for Part 10 Deep Learning module functions."""

    @classmethod
    def setUpClass(cls):
        """Set up synthetic test data and model directory."""
        cls.input_dim = 28
        cls.X_synth = np.random.randn(20, 28).astype(np.float32)
        cls.y_synth = np.random.randint(0, 2, 20)
        cls.temp_model_path = project_root / "scratch" / "unit_test_ann.keras"
        cls.temp_model_path.parent.mkdir(parents=True, exist_ok=True)

    def test_model_creation_and_shapes(self):
        """Test build_ann_model returns a Keras Sequential model with correct layer dimensions."""
        model = build_ann_model(input_dim=28, layer_sizes=[32, 16], dropout_rates=[0.2, 0.1])
        self.assertIsNotNone(model)
        
        preds = model.predict(self.X_synth[:3], verbose=0)
        self.assertEqual(preds.shape, (3, 1))

    def test_sigmoid_output_and_probability_range(self):
        """Test that model output sigmoid activation generates values strictly in [0, 1]."""
        model = build_ann_model(input_dim=28, layer_sizes=[64, 32], dropout_rates=[0.3, 0.2])
        res = predict_ann(model, self.X_synth)
        
        probs = np.array(res["probability_disease"])
        self.assertTrue(((probs >= 0.0) & (probs <= 1.0)).all())
        self.assertEqual(len(res["predicted_class"]), 20)

    def test_architecture_registry(self):
        """Test build_candidate_architectures returns all 3 expected candidates."""
        cands = build_candidate_architectures(input_dim=28)
        self.assertEqual(set(cands.keys()), {"ANN-1", "ANN-2", "ANN-3"})
        self.assertEqual(len(cands["ANN-1"]["layer_sizes"]), 2)
        self.assertEqual(len(cands["ANN-3"]["layer_sizes"]), 3)

    def test_model_save_and_load(self):
        """Test save_ann_model and load_ann_model preserve architecture and predictions."""
        model = build_ann_model(input_dim=28, layer_sizes=[32, 16], dropout_rates=[0.2, 0.1])
        save_ann_model(model, self.temp_model_path)
        self.assertTrue(self.temp_model_path.exists())

        reloaded = load_ann_model(self.temp_model_path)
        self.assertIsNotNone(reloaded)
        
        orig_preds = model.predict(self.X_synth[:2], verbose=0)
        reloaded_preds = reloaded.predict(self.X_synth[:2], verbose=0)
        np.testing.assert_allclose(orig_preds, reloaded_preds, rtol=1e-4)

    def test_evaluation_function(self):
        """Test evaluate_ann computes valid metrics dictionary."""
        model = build_ann_model(input_dim=28, layer_sizes=[32, 16], dropout_rates=[0.2, 0.1])
        metrics = evaluate_ann(model, self.X_synth, self.y_synth, threshold=0.50)
        
        expected_keys = {"Accuracy", "Precision", "Recall", "Specificity", "F1", "ROC-AUC", "TN", "FP", "FN", "TP"}
        self.assertTrue(expected_keys.issubset(set(metrics.keys())))
        self.assertEqual(metrics["TN"] + metrics["FP"] + metrics["FN"] + metrics["TP"], 20)

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary test file."""
        if cls.temp_model_path.exists():
            cls.temp_model_path.unlink()


if __name__ == "__main__":
    unittest.main()
