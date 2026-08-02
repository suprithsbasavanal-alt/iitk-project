"""
EDA Reproduction Script.

This script reproduces all summary CSV tables, text reports, and 21 Matplotlib
visualizations from the raw UCI Heart Disease dataset.
"""

from pathlib import Path
import sys

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.eda import run_full_eda


def main() -> None:
    """
    Main function executing full EDA reproduction.
    """
    print("=" * 60)
    print("REPRODUCING EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 60)
    result = run_full_eda()
    print("=" * 60)
    print(f"REPRODUCTION SUCCESSFUL! 21 Figures generated.")
    print("=" * 60)


if __name__ == "__main__":
    main()
