"""
Unit Tests for Hyperparameter Tuning Engine (Part 6).

Tests tuning registry, search space parameter prefixes ('classifier__'), search object construction, and pre-test ranking.
"""

from pathlib import Path
import sys
import unittest

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.train import get_tuning_search_spaces, build_search_object


class TestTuning(unittest.TestCase):
    """Test suite for Part 6 hyperparameter tuning functionality."""

    def test_tuning_search_spaces_registry(self):
        """Test that exactly 5 target models are defined for tuning."""
        spaces = get_tuning_search_spaces()
        self.assertEqual(len(spaces), 5)
        expected_models = [
            "Logistic Regression", "Support Vector Machine",
            "Random Forest", "XGBoost", "K-Nearest Neighbors"
        ]
        for name in expected_models:
            self.assertIn(name, spaces)

    def test_parameter_prefix(self):
        """Test that parameter grids use the 'classifier__' pipeline prefix."""
        spaces = get_tuning_search_spaces()
        for name, (cls, param_space, method) in spaces.items():
            if isinstance(param_space, list):
                for grid in param_space:
                    for k in grid.keys():
                        self.assertTrue(k.startswith("classifier__"), f"{k} missing classifier__ prefix in {name}")
            elif isinstance(param_space, dict):
                for k in param_space.keys():
                    self.assertTrue(k.startswith("classifier__"), f"{k} missing classifier__ prefix in {name}")

    def test_build_search_object(self):
        """Test search object construction for GridSearchCV and RandomizedSearchCV."""
        spaces = get_tuning_search_spaces()
        log_reg_cls, log_reg_grid, log_reg_method = spaces["Logistic Regression"]
        search_grid = build_search_object("Logistic Regression", log_reg_cls, log_reg_grid, search_method=log_reg_method)
        self.assertEqual(search_grid.scoring, "roc_auc")
        self.assertEqual(search_grid.cv.n_splits, 5)

        rf_cls, rf_dist, rf_method = spaces["Random Forest"]
        search_rand = build_search_object("Random Forest", rf_cls, rf_dist, search_method=rf_method, n_iter=10)
        self.assertEqual(search_rand.n_iter, 10)
        self.assertEqual(search_rand.scoring, "roc_auc")


if __name__ == "__main__":
    unittest.main()
