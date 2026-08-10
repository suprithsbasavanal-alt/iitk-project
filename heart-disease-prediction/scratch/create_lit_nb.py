"""
Script to create and execute notebooks/06_literature_survey.ipynb with 10 sections.
"""

from pathlib import Path
import json
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

repo_dir = Path("/Users/suprith.s.basavanal/Documents/antigrativity /iitk-project/heart-disease-prediction")
nb_path = repo_dir / "notebooks" / "06_literature_survey.ipynb"

nb = nbf.v4.new_notebook()

cells = [
    # 1. Objective
    nbf.v4.new_markdown_cell("""# Notebook 06: Comprehensive 16-Paper Literature Survey & Meta-Analysis

**Project Title**: Heart Disease Prediction Using Machine Learning and Deep Learning Techniques  
**Part 11**: Literature Survey Compilation, Methodological Comparison, Research Gap Analysis, and Team Allocation  

### 1. Objective
The objective of this notebook is to document, analyze, and synthesize 16 verified academic research papers (8 Machine Learning papers and 8 Deep Learning papers) focused on cardiovascular disease risk prediction, mapping their findings directly to our capstone project implementation choices.
"""),

    # 2. Setup & Data Loading
    nbf.v4.new_code_cell("""import sys
import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = Path('.').resolve().parent if Path('.').resolve().name == 'notebooks' else Path('.').resolve()

survey_df = pd.read_csv(PROJECT_ROOT / 'results' / 'literature_survey_16_papers.csv')
alloc_df = pd.read_csv(PROJECT_ROOT / 'results' / 'team_literature_allocation.csv')

print(f"Total Reviewed Papers: {len(survey_df)}")
print(f"Machine Learning Papers: {len(survey_df[survey_df['Category'] == 'Machine Learning'])}")
print(f"Deep Learning Papers: {len(survey_df[survey_df['Category'] == 'Deep Learning'])}")
"""),

    # 3. Selection Criteria
    nbf.v4.new_markdown_cell("""### 2. Paper Selection & Verification Criteria
Papers were selected from reputable academic databases (IEEE Xplore, ScienceDirect/Elsevier, Springer Nature, PubMed, Hindawi, MDPI). Every paper was verified for:
1. **Authenticity**: Verified official DOI / publisher URLs.
2. **Relevance**: Direct focus on tabular cardiovascular disease risk prediction or deep learning classification.
3. **Reproducibility**: Clear identification of datasets (e.g., UCI Cleveland), preprocessing methods, and model evaluation metrics.
"""),

    # 4. Machine Learning Papers
    nbf.v4.new_markdown_cell("""### 3. Machine Learning Papers (8 Papers)
Summary of the 8 verified Machine Learning publications:
"""),
    nbf.v4.new_code_cell("""ml_df = survey_df[survey_df['Category'] == 'Machine Learning'][['Sl No', 'Author/Year', 'Paper Title', 'Journal/Context', 'Publisher', 'Main Method', 'Team Member']]
ml_df
"""),

    # 5. Deep Learning Papers
    nbf.v4.new_markdown_cell("""### 4. Deep Learning Papers (8 Papers)
Summary of the 8 verified Deep Learning publications:
"""),
    nbf.v4.new_code_cell("""dl_df = survey_df[survey_df['Category'] == 'Deep Learning'][['Sl No', 'Author/Year', 'Paper Title', 'Journal/Context', 'Publisher', 'Main Method', 'Team Member']]
dl_df
"""),

    # 6. Dataset & Publisher Breakdown
    nbf.v4.new_markdown_cell("""### 5. Dataset & Publisher Breakdown Analysis
Visualizing dataset usage frequency and academic publisher representation across all 16 papers.
"""),
    nbf.v4.new_code_cell("""fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

dataset_counts = survey_df['Dataset Name'].value_counts()
ax1.barh(dataset_counts.index, dataset_counts.values, color='#1B365D')
ax1.set_title('Dataset Usage in Reviewed Literature', fontsize=12, fontweight='bold')
ax1.set_xlabel('Number of Papers')

pub_counts = survey_df['Publisher'].value_counts()
ax2.bar(pub_counts.index, pub_counts.values, color='#4B6B94')
ax2.set_title('Publisher Distribution', fontsize=12, fontweight='bold')
ax2.set_ylabel('Number of Papers')
plt.xticks(rotation=30, ha='right')

plt.tight_layout()
plt.show()
"""),

    # 7. Technique Comparison
    nbf.v4.new_markdown_cell("""### 6. Methodological & Algorithmic Comparison
Comparing techniques across Machine Learning and Deep Learning paradigms.
"""),
    nbf.v4.new_code_cell("""comp_df = pd.read_csv(PROJECT_ROOT / 'results' / 'literature_comparison.csv')
comp_df[['Paper', 'Category', 'Technique', 'Main Method', 'Strength']]
"""),

    # 8. Research Gap Analysis
    nbf.v4.new_markdown_cell("""### 7. Synthesized Research Gaps in Existing Literature
Key limitations identified across published literature:
1. **Small Tabular Sample Constraints**: Over-reliance on ~300 patient records limits deep learning parameter optimization.
2. **Single-Dataset Evaluation**: Lack of cross-hospital prospective validation.
3. **Opaque Black-Box Models**: Absence of clinical feature importance explanations in deep neural networks.
4. **Lack of Interactive Deployment**: Most studies end at paper publication without functional user interfaces.
"""),

    # 9. Relevance to Our Project
    nbf.v4.new_markdown_cell("""### 8. Relevance & Direct Mapping to Our Project Implementation
Our project directly addresses these gaps:
- **Dataset Choice**: Uses the benchmark **UCI Cleveland dataset** (303 records).
- **Leak-Free Benchmark**: Compares **Tuned Random Forest (ML)** vs **Final ANN (DL)** on a locked 61-row test set.
- **Model Explainability**: Formulates feature importances showing `cp`, `thalach`, `oldpeak`, and `ca` as top predictors.
- **Interactive Web App**: Deploys a full-featured **Streamlit app** (`app.py`) for dual ML/DL risk prediction.
"""),

    # 10. Team Allocation
    nbf.v4.new_markdown_cell("""### 9. Team Member Allocation Summary
Allocation of 16 papers (exactly 2 ML + 2 DL = 4 papers per member):
"""),
    nbf.v4.new_code_cell("""alloc_df
"""),

    # 11. Conclusion
    nbf.v4.new_markdown_cell("""### 10. Conclusion
Part 11 successfully compiled, verified, and meta-analyzed a comprehensive 16-paper literature survey. The literature strongly supports our capstone project's pipeline design, feature engineering choices, model benchmarking results, and Streamlit deployment.
""")
]

nb.cells = cells

with open(nb_path, "w") as f:
    nbf.write(nb, f)

print(f"Created notebook `{nb_path}`. Now executing...")

ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
with open(nb_path) as f:
    nb_to_run = nbf.read(f, as_version=4)

ep.preprocess(nb_to_run, {"metadata": {"path": str(repo_dir / "notebooks")}})

with open(nb_path, "w") as f:
    nbf.write(nb_to_run, f)

print(f"Successfully executed and saved `{nb_path}`.")
