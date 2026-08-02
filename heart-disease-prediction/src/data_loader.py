"""
Data Loader Module for Heart Disease Prediction.

This module provides reusable utilities for loading raw dataset files and performing
basic verification checks without applying preprocessing or transformations.
"""

from pathlib import Path
from typing import Union, Optional
import pandas as pd


def load_raw_data(data_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Safely load the raw Heart Disease dataset from disk.

    Args:
        data_path (Optional[Union[str, Path]]): File path to raw CSV dataset.
            If None, defaults to 'data/raw/heart_disease_uci.csv' relative to project root.

    Returns:
        pd.DataFrame: Unmodified raw clinical patient DataFrame.

    Raises:
        FileNotFoundError: If target raw dataset file does not exist.
        ValueError: If file is empty or corrupted.
    """
    if data_path is None:
        project_root = Path(__file__).resolve().parent.parent
        data_path = project_root / "data" / "raw" / "heart_disease_uci.csv"
    else:
        data_path = Path(data_path)

    if not data_path.exists():
        raise FileNotFoundError(
            f"Raw dataset file not found at: '{data_path.resolve()}'. "
            "Please run 'python src/download_data.py' to acquire the dataset."
        )

    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        raise ValueError(f"Failed to read CSV dataset from '{data_path}': {e}") from e

    if df.empty:
        raise ValueError(f"The loaded dataset file at '{data_path}' is empty.")

    return df


def validate_dataset(df: pd.DataFrame) -> bool:
    """
    Validate basic structural integrity of loaded dataset.

    Args:
        df (pd.DataFrame): Input dataset DataFrame.

    Returns:
        bool: True if dataset passes basic structural verification.

    Raises:
        ValueError: If dataset lacks expected shape or columns.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input dataset is not a valid pandas DataFrame.")

    if df.shape[0] == 0 or df.shape[1] == 0:
        raise ValueError(f"Dataset has invalid shape: {df.shape}")

    expected_columns = [
        "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
        "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"
    ]

    missing_cols = [col for col in expected_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")

    return True


def load_processed_data(data_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Placeholder for loading processed dataset in future stages.

    Args:
        data_path (Optional[Union[str, Path]]): File path to processed dataset.

    Returns:
        pd.DataFrame: Processed feature DataFrame.
    """
    # TODO: Implement processed data loader in preprocessing stage
    raise NotImplementedError("Processed data loading will be implemented in preprocessing phase.")
