"""
Unit Tests for Literature Survey Module & Verification Artifacts (Part 11).

Tests master literature survey CSV structure, paper counts (8 ML, 8 DL), team member allocations,
schema integrity, DOI format, and verification statuses.
"""

from pathlib import Path
import os
import sys
import unittest
import pandas as pd

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


class TestLiteratureSurvey(unittest.TestCase):
    """Unit test suite for Part 11 Literature Survey artifacts."""

    @classmethod
    def setUpClass(cls):
        """Load literature survey data files."""
        cls.results_dir = project_root / "results"
        cls.lit_csv = cls.results_dir / "literature_survey_16_papers.csv"
        cls.ver_csv = cls.results_dir / "literature_survey_verification.csv"
        cls.alloc_csv = cls.results_dir / "team_literature_allocation.csv"

        cls.df_master = pd.read_csv(cls.lit_csv) if cls.lit_csv.exists() else None
        cls.df_ver = pd.read_csv(cls.ver_csv) if cls.ver_csv.exists() else None
        cls.df_alloc = pd.read_csv(cls.alloc_csv) if cls.alloc_csv.exists() else None

    def test_file_existence(self):
        """Test master literature survey files exist."""
        self.assertTrue(self.lit_csv.exists())
        self.assertTrue(self.ver_csv.exists())
        self.assertTrue(self.alloc_csv.exists())

    def test_paper_counts(self):
        """Test exactly 16 papers exist: 8 Machine Learning and 8 Deep Learning."""
        self.assertIsNotNone(self.df_master)
        self.assertEqual(len(self.df_master), 16)
        
        ml_count = len(self.df_master[self.df_master["Category"] == "Machine Learning"])
        dl_count = len(self.df_master[self.df_master["Category"] == "Deep Learning"])
        self.assertEqual(ml_count, 8)
        self.assertEqual(dl_count, 8)

    def test_unique_paper_titles(self):
        """Test zero duplicate paper titles exist."""
        self.assertIsNotNone(self.df_master)
        titles = self.df_master["Paper Title"].tolist()
        self.assertEqual(len(titles), len(set(titles)))

    def test_team_allocation(self):
        """Test each member (Shreyas, Uday, Suprith, Sahitya) has 4 papers (2 ML + 2 DL)."""
        self.assertIsNotNone(self.df_master)
        members = ["Shreyas", "Uday", "Suprith", "Sahitya"]
        
        for mem in members:
            mem_df = self.df_master[self.df_master["Team Member"] == mem]
            self.assertEqual(len(mem_df), 4)
            ml_c = len(mem_df[mem_df["Category"] == "Machine Learning"])
            dl_c = len(mem_df[mem_df["Category"] == "Deep Learning"])
            self.assertEqual(ml_c, 2)
            self.assertEqual(dl_c, 2)

    def test_schema_columns(self):
        """Test required table columns are present and non-empty."""
        required_columns = {
            "Sl No", "Author/Year", "Paper Title", "Journal/Context", "Publisher",
            "Techniques", "Methods", "Dataset Name", "Main Method", "Limitations",
            "Summary", "Category", "Team Member", "DOI / URL", "Verification Source",
            "Relevance to Our Project"
        }
        self.assertTrue(required_columns.issubset(set(self.df_master.columns)))
        
        self.assertEqual(self.df_master["Paper Title"].isnull().sum(), 0)
        self.assertEqual(self.df_master["DOI / URL"].isnull().sum(), 0)
        self.assertEqual(self.df_master["Dataset Name"].isnull().sum(), 0)

    def test_verification_status(self):
        """Test all 16 papers have status VERIFIED in verification CSV."""
        self.assertIsNotNone(self.df_ver)
        self.assertEqual(len(self.df_ver), 16)
        statuses = self.df_ver["Verification Status"].tolist()
        self.assertTrue(all(s == "VERIFIED" for s in statuses))

    def test_individual_member_files(self):
        """Test individual CSV files for all 4 team members exist in results/literature/."""
        lit_dir = self.results_dir / "literature"
        self.assertTrue(lit_dir.exists())
        for mem in ["Shreyas", "Uday", "Suprith", "Sahitya"]:
            fpath = lit_dir / f"{mem}_literature.csv"
            self.assertTrue(fpath.exists())
            mdf = pd.read_csv(fpath)
            self.assertEqual(len(mdf), 4)


if __name__ == "__main__":
    unittest.main()
