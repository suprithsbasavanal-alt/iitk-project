"""
Unit Tests for Data Preprocessing Module (Part 3).

Tests binary target mapping, feature/target separation, ColumnTransformer
construction, missing value imputation, and dataset splitting routines.
"""

from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.data_loader import load_raw_data
from src.preprocessing import (
    create_binary_target,
    get_feature_groups,
    prepare_features_and_target,
    split_data,
    build_preprocessor,
)


class TestPreprocessing(unittest.TestCase):
    """Test suite for src/preprocessing.py module."""

    @classmethod
    def setUpClass(cls):
        """Load raw dataset once for test cases."""
        raw_path = project_root / "data" / "raw" / "heart_disease_uci.csv"
        cls.df_raw = load_raw_data(raw_path)

    def test_create_binary_target(self):
        """Test binary target conversion mapping and class counts."""
        y = create_binary_target(self.df_raw, raw_target_col="num")
        self.assertEqual(len(y), 303)
        self.assertEqual(set(y.unique()), {0, 1})
        counts = y.value_counts().to_dict()
        self.assertEqual(counts[0], 164)
        self.assertEqual(counts[1], 139)

    def test_prepare_features_and_target(self):
        """Test feature and target extraction."""
        X, y = prepare_features_and_target(self.df_raw)
        self.assertEqual(X.shape[0], 303)
        self.assertEqual(X.shape[1], 13)
        self.assertNotIn("num", X.columns)
        self.assertNotIn("target", X.columns)

    def test_feature_groups(self):
        """Test numerical and categorical feature definitions."""
        num_feats, cat_feats = get_feature_groups()
        self.assertEqual(len(num_feats), 5)
        self.assertEqual(len(cat_feats), 8)
        self.assertIn("ca", cat_feats)
        self.assertIn("age", num_feats)

    def test_split_data(self):
        """Test stratified 80/20 train-test split proportions."""
        X, y = prepare_features_and_target(self.df_raw)
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.20, random_state=42)
        self.assertEqual(X_train.shape[0], 242)
        self.assertEqual(X_test.shape[0], 61)
        self.assertEqual(y_train.shape[0], 242)
        self.assertEqual(y_test.shape[0], 61)
        # Check stratification ratios match approximately (45.87% positive)
        self.assertAlmostEqual(y_train.mean(), y_test.mean(), delta=0.05)

    def test_preprocessor_transformation(self):
        """Test preprocessor fitting, imputation, scaling, and encoding."""
        X, y = prepare_features_and_target(self.df_raw)
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.20, random_state=42)

        num_feats, cat_feats = get_feature_groups()
        preprocessor = build_preprocessor(num_feats, cat_feats)

        # Fit on training set only
        preprocessor.fit(X_train)

        X_train_trans = preprocessor.transform(X_train)
        X_test_trans = preprocessor.transform(X_test)

        self.assertEqual(X_train_trans.shape[0], 242)
        self.assertEqual(X_test_trans.shape[0], 61)
        self.assertEqual(X_train_trans.shape[1], 28)
        self.assertEqual(X_test_trans.shape[1], 28)

        # Verify zero missing values remain after imputation
        self.assertEqual(np.isnan(X_train_trans).sum(), 0)
        self.assertEqual(np.isnan(X_test_trans).sum(), 0)


if __name__ == "__main__":
    unittest.main()
