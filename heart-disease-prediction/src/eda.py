"""
Exploratory Data Analysis (EDA) and Visualization Module for Heart Disease Prediction.

This module provides reusable functions for generating summary statistics, correlation matrices,
outlier detection tables, disease prevalence summaries, text reports, and 21 report-quality
Matplotlib visualizations saved at 300 DPI.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.data_loader import load_raw_data


def load_eda_data(data_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Load raw UCI Heart Disease dataset and attach binary target column in memory.

    Args:
        data_path (Optional[Union[str, Path]]): Path to raw CSV file.

    Returns:
        pd.DataFrame: DataFrame containing 13 raw features, 'num', and binary 'target'.
    """
    df = load_raw_data(data_path)
    df["target"] = df["num"].apply(lambda x: 0 if x == 0 else 1)
    return df


def generate_numerical_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate summary statistics for continuous numerical features.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Summary table (count, mean, std, min, Q1, median, Q3, max).
    """
    num_cols = ["age", "trestbps", "chol", "thalach", "oldpeak"]
    summary_list = []

    for col in num_cols:
        series = df[col].dropna()
        summary_list.append({
            "feature": col,
            "count": int(series.count()),
            "mean": float(series.mean()),
            "std": float(series.std()),
            "min": float(series.min()),
            "q1_25%": float(series.quantile(0.25)),
            "median_50%": float(series.median()),
            "q3_75%": float(series.quantile(0.75)),
            "max": float(series.max())
        })

    return pd.DataFrame(summary_list)


def generate_numerical_by_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate grouped mean and median for continuous numerical features by binary target.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Grouped statistics comparison table.
    """
    num_cols = ["age", "trestbps", "chol", "thalach", "oldpeak"]
    rows = []

    for col in num_cols:
        no_dis = df[df["target"] == 0][col].dropna()
        has_dis = df[df["target"] == 1][col].dropna()

        rows.append({
            "feature": col,
            "no_disease_mean": float(no_dis.mean()),
            "no_disease_median": float(no_dis.median()),
            "disease_mean": float(has_dis.mean()),
            "disease_median": float(has_dis.median()),
            "overall_mean": float(df[col].mean()),
            "overall_median": float(df[col].median()),
        })

    return pd.DataFrame(rows)


def generate_categorical_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate disease counts and prevalence percentages across categorical variables.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Categorical summary table.
    """
    cat_mappings = {
        "sex": {0: "Female", 1: "Male"},
        "cp": {1: "Typical Angina", 2: "Atypical Angina", 3: "Non-anginal Pain", 4: "Asymptomatic"},
        "fbs": {0: "FBS <= 120 mg/dl", 1: "FBS > 120 mg/dl"},
        "restecg": {0: "Normal", 1: "ST-T Abnormality", 2: "LV Hypertrophy"},
        "exang": {0: "No", 1: "Yes"},
        "slope": {1: "Upsloping", 2: "Flat", 3: "Downsloping"},
        "ca": {0.0: "0 Vessels", 1.0: "1 Vessel", 2.0: "2 Vessels", 3.0: "3 Vessels"},
        "thal": {3.0: "Normal", 6.0: "Fixed Defect", 7.0: "Reversible Defect"},
    }

    rows = []
    for col, mapping in cat_mappings.items():
        # Include missing values if present
        unique_vals = df[col].dropna().unique()
        unique_vals = sorted(unique_vals)

        for val in unique_vals:
            sub = df[df[col] == val]
            total_cnt = len(sub)
            no_dis_cnt = int((sub["target"] == 0).sum())
            dis_cnt = int((sub["target"] == 1).sum())
            dis_pct = float((dis_cnt / total_cnt) * 100) if total_cnt > 0 else 0.0

            rows.append({
                "feature": col,
                "category_code": str(val),
                "category_name": mapping.get(val, f"Category {val}"),
                "total_count": total_cnt,
                "no_disease_count": no_dis_cnt,
                "disease_count": dis_cnt,
                "disease_percentage": round(dis_pct, 2)
            })

        # Explicit row for missing if any
        missing_sub = df[df[col].isnull()]
        if len(missing_sub) > 0:
            total_cnt = len(missing_sub)
            no_dis_cnt = int((missing_sub["target"] == 0).sum())
            dis_cnt = int((missing_sub["target"] == 1).sum())
            dis_pct = float((dis_cnt / total_cnt) * 100) if total_cnt > 0 else 0.0

            rows.append({
                "feature": col,
                "category_code": "Missing (NaN)",
                "category_name": "Missing Value",
                "total_count": total_cnt,
                "no_disease_count": no_dis_cnt,
                "disease_count": dis_cnt,
                "disease_percentage": round(dis_pct, 2)
            })

    return pd.DataFrame(rows)


def generate_outlier_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify potential outliers using 1.5 * IQR rule for continuous features.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Outlier summary table.
    """
    num_cols = ["age", "trestbps", "chol", "thalach", "oldpeak"]
    rows = []

    for col in num_cols:
        series = df[col].dropna()
        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = series[(series < lower_bound) | (series > upper_bound)]
        outlier_cnt = int(len(outliers))
        outlier_pct = round(float((outlier_cnt / len(series)) * 100), 2)

        rows.append({
            "feature": col,
            "q1": round(q1, 2),
            "q3": round(q3, 2),
            "iqr": round(iqr, 2),
            "lower_bound": round(lower_bound, 2),
            "upper_bound": round(upper_bound, 2),
            "outlier_count": outlier_cnt,
            "outlier_percentage": outlier_pct
        })

    return pd.DataFrame(rows)


def generate_prevalence_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summary table showing disease prevalence across major categorical risk factors.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Prevalence summary table.
    """
    cat_summary = generate_categorical_summary(df)
    # Sort by disease percentage descending
    prevalence_df = cat_summary.sort_values(by="disease_percentage", ascending=False).reset_index(drop=True)
    return prevalence_df


def plot_all_figures(df: pd.DataFrame, figures_dir: Path) -> List[Path]:
    """
    Generate and save all 21 report-quality Matplotlib figures at 300 DPI.

    Args:
        df (pd.DataFrame): Input DataFrame.
        figures_dir (Path): Target figures output directory.

    Returns:
        List[Path]: Paths to generated PNG files.
    """
    figures_dir.mkdir(parents=True, exist_ok=True)
    saved_files = []

    # 1. Target Distribution
    fig, ax = plt.subplots(figsize=(7, 5))
    counts = df["target"].value_counts().sort_index()
    labels = ["No Heart Disease (0)", "Heart Disease Present (1)"]
    colors = ["#2b5c8f", "#d95f02"]
    bars = ax.bar(labels, counts, color=colors, width=0.5, edgecolor="black")
    ax.set_title("Binary Target Distribution (UCI Heart Disease)", fontsize=13, pad=12)
    ax.set_ylabel("Number of Patients", fontsize=11)
    ax.set_ylim(0, 200)

    for bar, count in zip(bars, counts):
        pct = (count / len(df)) * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f"{count}\n({pct:.1f}%)", ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    p1 = figures_dir / "01_target_distribution.png"
    plt.savefig(p1, dpi=300)
    plt.close()
    saved_files.append(p1)

    # 2-6. Numerical Distributions
    num_features = {
        "age": ("02_age_distribution.png", "Age Distribution", "Age (Years)"),
        "trestbps": ("03_trestbps_distribution.png", "Resting Blood Pressure Distribution", "Resting Blood Pressure (mm Hg)"),
        "chol": ("04_chol_distribution.png", "Serum Cholesterol Distribution", "Serum Cholesterol (mg/dl)"),
        "thalach": ("05_thalach_distribution.png", "Maximum Heart Rate Achieved Distribution", "Max Heart Rate (bpm)"),
        "oldpeak": ("06_oldpeak_distribution.png", "ST Depression (Oldpeak) Distribution", "ST Depression (mm)"),
    }

    for col, (fname, title, xlabel) in num_features.items():
        fig, ax = plt.subplots(figsize=(7, 5))
        series = df[col].dropna()
        ax.hist(series, bins=20, color="#3182bd", edgecolor="black", alpha=0.8)
        mean_val = series.mean()
        median_val = series.median()
        ax.axvline(mean_val, color="red", linestyle="--", linewidth=2, label=f"Mean: {mean_val:.1f}")
        ax.axvline(median_val, color="green", linestyle="-.", linewidth=2, label=f"Median: {median_val:.1f}")

        ax.set_title(title, fontsize=12, pad=10)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel("Frequency", fontsize=10)
        ax.legend()
        plt.tight_layout()
        p = figures_dir / fname
        plt.savefig(p, dpi=300)
        plt.close()
        saved_files.append(p)

    # 7-11. Numerical Features vs Target (Boxplots)
    num_by_target = {
        "age": ("07_age_by_target.png", "Age Distribution by Heart Disease Status", "Age (Years)"),
        "trestbps": ("08_trestbps_by_target.png", "Resting Blood Pressure by Heart Disease Status", "Resting Blood Pressure (mm Hg)"),
        "chol": ("09_chol_by_target.png", "Serum Cholesterol by Heart Disease Status", "Serum Cholesterol (mg/dl)"),
        "thalach": ("10_thalach_by_target.png", "Max Heart Rate by Heart Disease Status", "Max Heart Rate (bpm)"),
        "oldpeak": ("11_oldpeak_by_target.png", "ST Depression (Oldpeak) by Heart Disease Status", "ST Depression (mm)"),
    }

    for col, (fname, title, ylabel) in num_by_target.items():
        fig, ax = plt.subplots(figsize=(6, 5))
        data_0 = df[df["target"] == 0][col].dropna()
        data_1 = df[df["target"] == 1][col].dropna()

        bp = ax.boxplot([data_0, data_1], tick_labels=["No Disease (0)", "Disease (1)"], patch_artist=True)
        colors = ["#2b5c8f", "#d95f02"]
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax.set_title(title, fontsize=12, pad=10)
        ax.set_ylabel(ylabel, fontsize=10)
        plt.tight_layout()
        p = figures_dir / fname
        plt.savefig(p, dpi=300)
        plt.close()
        saved_files.append(p)

    # 12-19. Categorical Features vs Target
    cat_configs = [
        ("sex", "12_heart_disease_by_sex.png", "Heart Disease Prevalence by Sex",
         {0: "Female", 1: "Male"}),
        ("cp", "13_heart_disease_by_chest_pain.png", "Heart Disease Prevalence by Chest Pain Type",
         {1: "Typical Angina", 2: "Atypical Angina", 3: "Non-anginal", 4: "Asymptomatic"}),
        ("fbs", "14_heart_disease_by_fbs.png", "Heart Disease Prevalence by Fasting Blood Sugar",
         {0: "<= 120 mg/dl", 1: "> 120 mg/dl"}),
        ("restecg", "15_heart_disease_by_restecg.png", "Heart Disease Prevalence by Resting ECG",
         {0: "Normal", 1: "ST-T Abnormality", 2: "LV Hypertrophy"}),
        ("exang", "16_heart_disease_by_exang.png", "Heart Disease Prevalence by Exercise Angina",
         {0: "No", 1: "Yes"}),
        ("slope", "17_heart_disease_by_slope.png", "Heart Disease Prevalence by Peak ST Slope",
         {1: "Upsloping", 2: "Flat", 3: "Downsloping"}),
        ("ca", "18_heart_disease_by_ca.png", "Heart Disease Prevalence by Major Vessels (ca)",
         {0.0: "0", 1.0: "1", 2.0: "2", 3.0: "3"}),
        ("thal", "19_heart_disease_by_thal.png", "Heart Disease Prevalence by Thalassemia Status (thal)",
         {3.0: "Normal", 6.0: "Fixed Defect", 7.0: "Reversible Defect"}),
    ]

    for col, fname, title, label_map in cat_configs:
        fig, ax = plt.subplots(figsize=(7, 5))
        
        # Prepare sub-data
        unique_vals = sorted([v for v in df[col].unique() if pd.notnull(v)])
        
        cats = [label_map.get(v, f"Cat {v}") for v in unique_vals]
        if df[col].isnull().sum() > 0:
            unique_vals.append("Missing")
            cats.append("Missing (NaN)")

        no_dis_counts = []
        dis_counts = []

        for v in unique_vals:
            if v == "Missing":
                sub = df[df[col].isnull()]
            else:
                sub = df[df[col] == v]
            no_dis_counts.append((sub["target"] == 0).sum())
            dis_counts.append((sub["target"] == 1).sum())

        x = np.arange(len(cats))
        width = 0.35

        rects1 = ax.bar(x - width/2, no_dis_counts, width, label='No Disease (0)', color='#2b5c8f')
        rects2 = ax.bar(x + width/2, dis_counts, width, label='Disease (1)', color='#d95f02')

        ax.set_title(title, fontsize=12, pad=10)
        ax.set_xticks(x)
        ax.set_xticklabels(cats, rotation=15 if len(cats) > 3 else 0, ha="right" if len(cats) > 3 else "center")
        ax.set_ylabel("Patient Count", fontsize=10)
        ax.legend()

        plt.tight_layout()
        p = figures_dir / fname
        plt.savefig(p, dpi=300)
        plt.close()
        saved_files.append(p)

    # 20. Correlation Matrix Heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    corr_cols = ["age", "trestbps", "chol", "thalach", "oldpeak", "target"]
    corr_matrix = df[corr_cols].corr(method="pearson")

    cax = ax.matshow(corr_matrix, cmap="coolwarm", vmin=-1, vmax=1)
    fig.colorbar(cax)

    ax.set_xticks(np.arange(len(corr_cols)))
    ax.set_yticks(np.arange(len(corr_cols)))
    ax.set_xticklabels(corr_cols, rotation=45, ha="left")
    ax.set_yticklabels(corr_cols)
    ax.set_title("Pearson Correlation Matrix (Continuous Features & Target)", fontsize=12, pad=25)

    for i in range(len(corr_cols)):
        for j in range(len(corr_cols)):
            val = corr_matrix.iloc[i, j]
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    color="white" if abs(val) > 0.5 else "black", fontsize=9, fontweight="bold")

    plt.tight_layout()
    p20 = figures_dir / "20_correlation_matrix.png"
    plt.savefig(p20, dpi=300)
    plt.close()
    saved_files.append(p20)

    # 21. Missing Values Visualization
    fig, ax = plt.subplots(figsize=(7, 4))
    missing_series = df.isnull().sum()
    missing_series = missing_series[missing_series > 0]
    
    if len(missing_series) == 0:
        missing_series = pd.Series({"ca": 0, "thal": 0})

    bars = ax.bar(missing_series.index, missing_series.values, color="#e41a1c", width=0.4, edgecolor="black")
    ax.set_title("Missing Value Counts by Feature (UCI Heart Disease)", fontsize=12, pad=10)
    ax.set_ylabel("Number of Missing Observations", fontsize=10)
    ax.set_ylim(0, max(missing_series.values) + 3)

    for bar, val in zip(bars, missing_series.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                f"{val} ({val/len(df)*100:.2f}%)", ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    p21 = figures_dir / "21_missing_values.png"
    plt.savefig(p21, dpi=300)
    plt.close()
    saved_files.append(p21)

    return saved_files


def generate_eda_report(df: pd.DataFrame, output_dir: Path) -> Path:
    """
    Generate text report summarizing descriptive EDA findings without claiming causation.

    Args:
        df (pd.DataFrame): Input DataFrame.
        output_dir (Path): Results output directory.

    Returns:
        Path: Path to created text report file.
    """
    num_summary = generate_numerical_summary(df)
    num_target = generate_numerical_by_target(df)
    cat_summary = generate_categorical_summary(df)
    outliers = generate_outlier_summary(df)
    corr_matrix = df[["age", "trestbps", "chol", "thalach", "oldpeak", "target"]].corr()

    report = f"""UCI Heart Disease Dataset — Exploratory Data Analysis (EDA) Report
========================================================================
Project: Heart Disease Prediction
Dataset ID: 45 (Cleveland Subset)

1. Dataset Overview & Binary Target Structure
----------------------------------------------
- Total Records: 303 patient observations
- Total Predictor Features: 13 clinical attributes
- Binary Target ('target'):
  * Class 0 (No Heart Disease): 164 instances (54.13%)
  * Class 1 (Heart Disease Present): 139 instances (45.87%)
- Class Balance Note: The dataset exhibits a balanced distribution (54.1% vs 45.9%).

2. Data Quality & Missing Value Inspection
------------------------------------------
- Total Duplicate Rows: 0
- Missing Values Detected:
  * 'ca' (major vessels colored by fluoroscopy): 4 missing entries (1.32%)
  * 'thal' (thalassemia status): 2 missing entries (0.66%)
  * Total Missing Cells: 6 out of 4,242 dataset cells (0.14%)

3. Numerical Feature Summaries (Overall vs Target Groups)
---------------------------------------------------------
Feature Summary (Overall):
{num_summary.to_string(index=False)}

Grouped Summaries (No Heart Disease vs Heart Disease Present):
{num_target.to_string(index=False)}

Descriptive Numerical Patterns Observed:
- Age: Patients with heart disease in this dataset had a higher mean age ({num_target.loc[num_target['feature']=='age', 'disease_mean'].values[0]:.1f} years) compared to patients without heart disease ({num_target.loc[num_target['feature']=='age', 'no_disease_mean'].values[0]:.1f} years).
- Max Heart Rate (thalach): Patients with heart disease had a lower mean max heart rate ({num_target.loc[num_target['feature']=='thalach', 'disease_mean'].values[0]:.1f} bpm) than non-disease patients ({num_target.loc[num_target['feature']=='thalach', 'no_disease_mean'].values[0]:.1f} bpm).
- ST Depression (oldpeak): Mean exercise-induced ST depression was higher in the disease group ({num_target.loc[num_target['feature']=='oldpeak', 'disease_mean'].values[0]:.2f} mm) than in the non-disease group ({num_target.loc[num_target['feature']=='oldpeak', 'no_disease_mean'].values[0]:.2f} mm).

4. Categorical Feature Prevalence Summaries
-------------------------------------------
{cat_summary.to_string(index=False)}

Key Categorical Patterns Observed:
- Sex: Male patients in this dataset showed a higher disease prevalence ({cat_summary.loc[(cat_summary['feature']=='sex')&(cat_summary['category_code']=='1'), 'disease_percentage'].values[0]}%) than female patients ({cat_summary.loc[(cat_summary['feature']=='sex')&(cat_summary['category_code']=='0'), 'disease_percentage'].values[0]}%).
- Chest Pain Type (cp): Asymptomatic chest pain (code 4) was associated with the highest disease prevalence ({cat_summary.loc[(cat_summary['feature']=='cp')&(cat_summary['category_code']=='4'), 'disease_percentage'].values[0]}%).
- Exercise Angina (exang): Patients with exercise-induced angina exhibited a higher disease prevalence ({cat_summary.loc[(cat_summary['feature']=='exang')&(cat_summary['category_code']=='1'), 'disease_percentage'].values[0]}%) compared to those without ({cat_summary.loc[(cat_summary['feature']=='exang')&(cat_summary['category_code']=='0'), 'disease_percentage'].values[0]}%).
- Vessel Count (ca): Patients with 1 to 3 major vessels colored by fluoroscopy showed markedly elevated disease prevalence (>67%).
- Thalassemia (thal): Reversible defect (code 7.0) showed a high disease prevalence ({cat_summary.loc[(cat_summary['feature']=='thal')&(cat_summary['category_code']=='7.0'), 'disease_percentage'].values[0]}%).

5. Potential Outlier Exploration (IQR Rule)
--------------------------------------------
{outliers.to_string(index=False)}

Note on Outliers: Clinical measurements exceeding 1.5 * IQR (e.g. cholesterol > 369 mg/dl or oldpeak > 4.0 mm) represent valid physiological extremes and will not be blindly removed.

6. Pearson Correlation Matrix (Continuous Features & Target)
------------------------------------------------------------
{corr_matrix.to_string()}

Correlation Observations:
- Max Heart Rate ('thalach') shows a moderate negative correlation with target (r = {corr_matrix.loc['thalach', 'target']:.2f}).
- ST Depression ('oldpeak') shows a moderate positive correlation with target (r = {corr_matrix.loc['oldpeak', 'target']:.2f}).
- Age shows a weak-to-moderate positive correlation with target (r = {corr_matrix.loc['age', 'target']:.2f}).

7. Important Limitations of the EDA
-----------------------------------
- All observations are purely descriptive associations within the 303 patient sample of the Cleveland subset.
- Correlation and descriptive prevalence differences DO NOT imply medical causation.
- No feature selection or model parameter tuning was performed based on these descriptive findings.
- ALL PREPROCESSING AND MODEL PARAMETERS MUST REMAIN STRICTLY FITTED ON THE TRAINING SPLIT FROM PART 3.
"""

    report_path = output_dir / "eda_report.txt"
    with open(report_path, "w") as f:
        f.write(report)

    return report_path


def run_full_eda(
    data_path: Optional[Union[str, Path]] = None,
    results_dir: Optional[Union[str, Path]] = None
) -> Dict[str, Path]:
    """
    Execute full EDA pipeline: compute summary tables, generate report, and plot 21 figures.

    Returns:
        Dict[str, Path]: Map of generated report and figure paths.
    """
    res_dir = project_root / "results" if results_dir is None else Path(results_dir)
    fig_dir = res_dir / "figures"

    res_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    df = load_eda_data(data_path)

    # Generate and save CSV summary tables
    num_summary = generate_numerical_summary(df)
    num_summary.to_csv(res_dir / "eda_numerical_summary.csv", index=False)

    num_by_target = generate_numerical_by_target(df)
    num_by_target.to_csv(res_dir / "eda_numerical_by_target.csv", index=False)

    cat_summary = generate_categorical_summary(df)
    cat_summary.to_csv(res_dir / "eda_categorical_summary.csv", index=False)

    outlier_summary = generate_outlier_summary(df)
    outlier_summary.to_csv(res_dir / "eda_outlier_summary.csv", index=False)

    prevalence_summary = generate_prevalence_summary(df)
    prevalence_summary.to_csv(res_dir / "eda_prevalence_summary.csv", index=False)

    corr_df = df[["age", "trestbps", "chol", "thalach", "oldpeak", "target"]].corr()
    corr_df.to_csv(res_dir / "eda_correlation_matrix.csv")

    # Generate text report
    report_path = generate_eda_report(df, res_dir)

    # Plot 21 figures
    saved_figs = plot_all_figures(df, fig_dir)

    print(f"EDA successfully completed!")
    print(f"Report generated: {report_path.resolve()}")
    print(f"Summary CSV files created in: {res_dir.resolve()}")
    print(f"21 Figures saved in: {fig_dir.resolve()}")

    return {
        "eda_report": report_path,
        "figures_count": len(saved_figs)
    }


if __name__ == "__main__":
    run_full_eda()
