"""
Dataset Download Script for UCI Heart Disease Dataset (ID 45).

This script programmatically downloads the official Heart Disease dataset from the
UCI Machine Learning Repository using `ucimlrepo`, combines features and targets
without preprocessing, and saves the immutable raw dataset locally.
"""

from pathlib import Path
import pandas as pd
from ucimlrepo import fetch_ucirepo


def download_dataset() -> Path:
    """
    Fetch UCI Heart Disease dataset (ID 45) and save as raw CSV.

    Returns:
        Path: Path to the saved raw dataset CSV.
    """
    print("Fetching UCI Heart Disease Dataset (ID 45)...")
    heart_disease = fetch_ucirepo(id=45)

    # Obtain feature dataframe and target dataframe
    X = heart_disease.data.features
    y = heart_disease.data.targets

    # Combine features and target dataframe while preserving original column names
    raw_df = pd.concat([X, y], axis=1)

    # Determine save path relative to project root
    project_root = Path(__file__).resolve().parent.parent
    raw_data_dir = project_root / "data" / "raw"
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    
    save_path = raw_data_dir / "heart_disease_uci.csv"

    # Save to CSV without modifying values or indexing
    raw_df.to_csv(save_path, index=False)

    print("\nDataset successfully acquired and saved!")
    print(f"Save Location: {save_path.resolve()}")
    print(f"Number of Rows: {raw_df.shape[0]}")
    print(f"Number of Columns: {raw_df.shape[1]}")

    return save_path


if __name__ == "__main__":
    download_dataset()
