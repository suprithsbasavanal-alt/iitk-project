"""
Dataset Verification Script.

This script loads the local raw Heart Disease dataset using `src.data_loader`,
verifies its structural integrity, and prints summary statistics without modifying
the raw data.
"""

from pathlib import Path
import sys

# Ensure src module can be resolved
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.data_loader import load_raw_data, validate_dataset


def verify_dataset() -> None:
    """
    Load raw dataset and output verification summary to terminal.
    """
    raw_path = project_root / "data" / "raw" / "heart_disease_uci.csv"

    print("Dataset Verification")
    print("--------------------")
    print(f"Dataset Source: UCI Machine Learning Repository (Dataset ID: 45)")
    print(f"File Location:  {raw_path.resolve()}")

    # Load and validate using project data_loader
    df = load_raw_data(raw_path)
    validate_dataset(df)

    print(f"Shape:           {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Columns:         {list(df.columns)}")
    print(f"Missing Values:  {df.isnull().sum().sum()} total ({dict(df.isnull().sum()[df.isnull().sum() > 0])})")
    print(f"Duplicate Count: {df.duplicated().sum()}")
    print(f"Target Column:   'num'")
    print(f"Target Distribution:\n{df['num'].value_counts().sort_index().to_string()}")
    print("--------------------")
    print("Verification Status: SUCCESS (Raw dataset loaded intact without modifications)")


if __name__ == "__main__":
    verify_dataset()
