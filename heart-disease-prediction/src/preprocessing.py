"""
Data Preprocessing Module for Heart Disease Prediction.

This module provides reusable functions for target transformation (binary mapping),
feature grouping, train/test splitting, and constructing a leakage-safe scikit-learn
preprocessing pipeline (imputation, scaling, and one-hot encoding).
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import sys

# Ensure project root is on sys.path for direct script execution
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.data_loader import load_raw_data, validate_dataset


def create_binary_target(df: pd.DataFrame, raw_target_col: str = "num") -> pd.Series:
    """
    Transform original UCI multiclass target ('num': 0, 1, 2, 3, 4) into binary target.

    Mapping:
        0 -> 0 (No Heart Disease)
        1, 2, 3, 4 -> 1 (Heart Disease Present)

    Args:
        df (pd.DataFrame): Input raw DataFrame.
        raw_target_col (str): Name of raw target column. Defaults to 'num'.

    Returns:
        pd.Series: Binary target series named 'target'.

    Raises:
        ValueError: If target values violate expected 0-4 range or final distribution.
    """
    if raw_target_col not in df.columns:
        raise ValueError(f"Raw target column '{raw_target_col}' not found in DataFrame.")

    # Create binary series
    binary_target = df[raw_target_col].apply(lambda x: 0 if x == 0 else 1).astype(int)
    binary_target.name = "target"

    # Validate distribution against verified UCI Cleveland baseline (164 negative, 139 positive)
    counts = binary_target.value_counts().to_dict()
    if counts.get(0, 0) != 164 or counts.get(1, 0) != 139:
        raise ValueError(
            f"Unexpected binary target distribution: {counts}. Expected {{0: 164, 1: 139}}."
        )

    return binary_target


def get_feature_groups() -> Tuple[List[str], List[str]]:
    """
    Return intended numerical and categorical feature groupings verified from data dictionary.

    Decisions:
        - Continuous Numerical (5): age, trestbps, chol, thalach, oldpeak
        - Discrete / Categorical (8): sex, cp, fbs, restecg, exang, slope, ca, thal
          * 'ca' represents number of major vessels colored by fluoroscopy (0-3).
            Although stored numerically, it is a small discrete variable and treated as categorical.

    Returns:
        Tuple[List[str], List[str]]: (numerical_features, categorical_features)
    """
    numerical_features = ["age", "trestbps", "chol", "thalach", "oldpeak"]
    categorical_features = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]
    return numerical_features, categorical_features


def prepare_features_and_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Separate predictor variables X from binary target y.

    Args:
        df (pd.DataFrame): Raw DataFrame containing features and 'num' column.

    Returns:
        Tuple[pd.DataFrame, pd.Series]: (X feature DataFrame, y binary target Series).
    """
    validate_dataset(df)
    y = create_binary_target(df, raw_target_col="num")

    # Exclude raw target 'num' and any derived 'target' column from feature matrix X
    drop_cols = [col for col in ["num", "target"] if col in df.columns]
    X = df.drop(columns=drop_cols).copy()

    return X, y


def build_preprocessor(
    numerical_features: List[str], categorical_features: List[str]
) -> ColumnTransformer:
    """
    Construct scikit-learn ColumnTransformer for numerical and categorical pipelines.

    Pipelines:
        - Numerical: SimpleImputer(strategy="median") -> StandardScaler()
        - Categorical: SimpleImputer(strategy="most_frequent") -> OneHotEncoder(handle_unknown="ignore")

    Args:
        numerical_features (List[str]): List of continuous feature names.
        categorical_features (List[str]): List of discrete/categorical feature names.

    Returns:
        ColumnTransformer: Unfitted ColumnTransformer preprocessor object.
    """
    numerical_pipeline = [
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]

    categorical_pipeline = [
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ]

    from sklearn.pipeline import Pipeline

    num_transformer = Pipeline(numerical_pipeline)
    cat_transformer = Pipeline(categorical_pipeline)

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_transformer, numerical_features),
            ("cat", cat_transformer, categorical_features),
        ],
        remainder="drop",
    )

    return preprocessor


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.20,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Perform stratified train/test split.

    Args:
        X (pd.DataFrame): Predictor variables DataFrame.
        y (pd.Series): Binary target Series.
        test_size (float): Fraction of data reserved for test set. Defaults to 0.20.
        random_state (int): Seed for reproducibility. Defaults to 42.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    return X_train, X_test, y_train, y_test


def run_preprocessing_pipeline(
    data_path: Optional[Union[str, Path]] = None,
    output_dir: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    """
    Execute complete end-to-end preprocessing workflow with zero data leakage.

    Workflow:
        1. Load raw dataset.
        2. Create binary target 'y' and feature matrix 'X'.
        3. Perform 80/20 stratified split into X_train, X_test, y_train, y_test.
        4. Save un-transformed split CSV files to data/processed/.
        5. Build ColumnTransformer.
        6. Fit preprocessor ONLY on X_train.
        7. Transform X_train and X_test.
        8. Save fitted preprocessor to models/preprocessor.joblib.
        9. Export feature names and preprocessing report to results/.

    Args:
        data_path (Optional[Union[str, Path]]): Custom path to raw dataset.
        output_dir (Optional[Union[str, Path]]): Custom output directory.

    Returns:
        Dict[str, Any]: Dictionary containing artifacts, shapes, and metrics.
    """
    project_root = Path(__file__).resolve().parent.parent
    processed_dir = project_root / "data" / "processed" if output_dir is None else Path(output_dir)
    models_dir = project_root / "models"
    results_dir = project_root / "results"

    processed_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load raw data
    df_raw = load_raw_data(data_path)

    # 2. Prepare X and y
    X, y = prepare_features_and_target(df_raw)

    # 3. Stratified Train / Test Split
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.20, random_state=42)

    # 4. Save raw splits BEFORE fit/transform to data/processed/
    X_train.to_csv(processed_dir / "X_train_raw.csv", index=False)
    X_test.to_csv(processed_dir / "X_test_raw.csv", index=False)
    y_train.to_frame().to_csv(processed_dir / "y_train.csv", index=False)
    y_test.to_frame().to_csv(processed_dir / "y_test.csv", index=False)

    # 5. Build preprocessor
    num_features, cat_features = get_feature_groups()
    preprocessor = build_preprocessor(num_features, cat_features)

    # 6. Fit ONLY on X_train (Data Leakage Prevention)
    preprocessor.fit(X_train)

    # 7. Transform X_train and X_test
    X_train_transformed = preprocessor.transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    # 8. Save fitted preprocessor artifact
    preprocessor_path = models_dir / "preprocessor.joblib"
    joblib.dump(preprocessor, preprocessor_path)

    # 9. Extract transformed feature names
    feature_names = preprocessor.get_feature_names_out()

    # Save feature names text artifact
    feature_names_path = results_dir / "processed_feature_names.txt"
    with open(feature_names_path, "w") as f:
        for idx, name in enumerate(feature_names, 1):
            f.write(f"{idx}. {name}\n")

    # Save transformed CSVs
    X_train_trans_df = pd.DataFrame(X_train_transformed, columns=feature_names)
    X_test_trans_df = pd.DataFrame(X_test_transformed, columns=feature_names)
    X_train_trans_df.to_csv(processed_dir / "X_train_preprocessed.csv", index=False)
    X_test_trans_df.to_csv(processed_dir / "X_test_preprocessed.csv", index=False)

    # 10. Generate preprocessing report
    report_text = f"""Preprocessing & Data Leakage Prevention Report
===============================================
Project: Heart Disease Prediction
Generated: Leakage-Safe Preprocessing Pipeline

1. Dataset & Target Transformation
----------------------------------
- Original Raw Dataset Shape: {df_raw.shape} (303 rows, 14 columns)
- Target Transformation: 'num' (0,1,2,3,4) mapped to binary 'target' (0 vs 1)
- Final Binary Class Distribution:
  * Class 0 (No Heart Disease): 164 (54.13%)
  * Class 1 (Heart Disease Present): 139 (45.87%)
  * Total Instances: 303 (100.00%)

2. Feature Classification & Pipeline Configuration
--------------------------------------------------
- Continuous Numerical Features ({len(num_features)}): {num_features}
  * Pipeline: SimpleImputer(strategy='median') -> StandardScaler()
- Categorical / Discrete Features ({len(cat_features)}): {cat_features}
  * Pipeline: SimpleImputer(strategy='most_frequent') -> OneHotEncoder(handle_unknown='ignore')
  * Note on 'ca': Treated as discrete categorical variable (0-3 major vessels).

3. Missing Values Strategy
--------------------------
- Raw missing values: 'ca' (4 missing), 'thal' (2 missing). Total missing cells = 6.
- Imputation Rule: Learned STRICTLY from training set during preprocessor.fit(X_train).
- Numerical imputation: median (learned from X_train).
- Categorical imputation: most_frequent (learned from X_train).

4. Train / Test Split Parameters
--------------------------------
- Split Method: Stratified Train/Test Split (stratify=y)
- Split Ratio: 80% Training / 20% Testing (test_size=0.20, random_state=42)
- Row Counts:
  * X_train shape: {X_train.shape} ({X_train.shape[0]} rows, {X_train.shape[1]} features)
  * X_test shape:  {X_test.shape} ({X_test.shape[0]} rows, {X_test.shape[1]} features)
  * y_train shape: {y_train.shape}
  * y_test shape:  {y_test.shape}

5. Class Distribution across Splits
-----------------------------------
- Training Set (y_train count = {len(y_train)}):
  * Class 0: {(y_train == 0).sum()} ({(y_train == 0).mean() * 100:.2f}%)
  * Class 1: {(y_train == 1).sum()} ({(y_train == 1).mean() * 100:.2f}%)
- Test Set (y_test count = {len(y_test)}):
  * Class 0: {(y_test == 0).sum()} ({(y_test == 0).mean() * 100:.2f}%)
  * Class 1: {(y_test == 1).sum()} ({(y_test == 1).mean() * 100:.2f}%)

6. Transformed Feature Dimensions
----------------------------------
- Original Predictors: {X.shape[1]}
- Transformed Feature Matrix Predictors: {len(feature_names)}
- Transformed Train Shape: {X_train_transformed.shape}
- Transformed Test Shape:  {X_test_transformed.shape}
- NaN values remaining in transformed matrices: {np.isnan(X_train_transformed).sum() + np.isnan(X_test_transformed).sum()}

7. Data Leakage Prevention Guarantees
-------------------------------------
- Imputer statistics (median & mode), StandardScaler mean/std, and OneHotEncoder categories were fitted ONLY on X_train.
- Test set (X_test) was strictly transformed using parameters learned from X_train.
- Saved fitted preprocessor artifact: '{preprocessor_path.resolve()}'.
- NO MACHINE LEARNING PREDICTION MODEL WAS TRAINED IN THIS PIPELINE.
"""

    report_path = results_dir / "preprocessing_report.txt"
    with open(report_path, "w") as f:
        f.write(report_text)

    print("Preprocessing pipeline executed successfully!")
    print(f"Fitted Preprocessor Saved: {preprocessor_path}")
    print(f"X_train shape: {X_train.shape} -> Transformed: {X_train_transformed.shape}")
    print(f"X_test shape:  {X_test.shape}  -> Transformed: {X_test_transformed.shape}")
    print(f"Transformed Features: {len(feature_names)}")

    return {
        "X_train_raw": X_train,
        "X_test_raw": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "X_train_transformed": X_train_transformed,
        "X_test_transformed": X_test_transformed,
        "preprocessor": preprocessor,
        "feature_names": feature_names,
    }


if __name__ == "__main__":
    run_preprocessing_pipeline()
