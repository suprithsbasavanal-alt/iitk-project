"""
Streamlit Web Application for Heart Disease Prediction (Part 8 & Part 10).

This application serves as the interactive deployment interface for the frozen final machine
learning pipeline (Tuned Random Forest) and the benchmarked Deep Learning pipeline (ANN).
It provides user controls for all 13 clinical predictors, validates schema inputs,
executes leak-free inference, displays risk probabilities, visualizes feature importances,
compares ML vs DL performance, and provides prominent educational disclaimers.

Run locally:
    streamlit run app.py
"""

import json
import os
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import streamlit as st

# Enforce PyTorch backend for Keras
os.environ["KERAS_BACKEND"] = "torch"

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.predict import predict_heart_disease, load_final_model, validate_input_data, REQUIRED_FEATURES
from src.deep_learning import load_ann_model, predict_ann

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Heart Disease Prediction | ML & DL Capstone",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Cached Resource Loaders
@st.cache_resource
def get_ml_model():
    """Load and cache the frozen final ML model pipeline."""
    model_path = PROJECT_ROOT / "models" / "final" / "final_model.joblib"
    return load_final_model(model_path)


@st.cache_resource
def get_dl_model():
    """Load and cache the frozen final Deep Learning ANN model."""
    dl_model_path = PROJECT_ROOT / "models" / "deep_learning" / "final_ann.keras"
    if dl_model_path.exists():
        return load_ann_model(dl_model_path)
    return None


@st.cache_resource
def get_preprocessor():
    """Load preprocessor joblib to transform raw inputs for ANN inference."""
    import joblib
    prep_path = PROJECT_ROOT / "models" / "preprocessor.joblib"
    if prep_path.exists():
        return joblib.load(prep_path)
    return None


@st.cache_data
def get_metadata():
    """Load and cache final ML model metadata."""
    meta_path = PROJECT_ROOT / "models" / "final" / "final_model_metadata.json"
    if meta_path.exists():
        with open(meta_path, "r") as f:
            return json.load(f)
    return {}


@st.cache_data
def get_feature_importance():
    """Load and cache final feature importance rankings."""
    fi_path = PROJECT_ROOT / "results" / "final_feature_importance.csv"
    if fi_path.exists():
        return pd.read_csv(fi_path)
    return pd.DataFrame()


@st.cache_data
def get_comparison_table():
    """Load and cache 12-model benchmark comparison table."""
    comp_path = PROJECT_ROOT / "results" / "metrics" / "model_selection_comparison.csv"
    if comp_path.exists():
        return pd.read_csv(comp_path)
    return pd.DataFrame()


@st.cache_data
def get_ml_vs_dl_table():
    """Load and cache ML vs DL benchmark comparison table."""
    comp_path = PROJECT_ROOT / "results" / "metrics" / "ml_vs_dl_comparison.csv"
    if comp_path.exists():
        return pd.read_csv(comp_path)
    return pd.DataFrame()


@st.cache_data
def get_sample_test_records():
    """Load sample test records from X_test_raw.csv for demonstration."""
    test_path = PROJECT_ROOT / "data" / "processed" / "X_test_raw.csv"
    if test_path.exists():
        return pd.read_csv(test_path)
    return pd.DataFrame()


def main():
    # Render Sidebar
    st.sidebar.title("🫀 Project Navigation")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Model Specification")
    st.sidebar.info(
        "**Primary Model**: Tuned Random Forest (ML)\n\n"
        "**Secondary Model**: Multi-Layer Perceptron (DL ANN-3)\n\n"
        "**Dataset**: UCI Heart Disease (Cleveland)\n\n"
        "**Total Samples**: 303\n\n"
        "**Train Split**: 242 (80%)\n\n"
        "**Test Split**: 61 (20%)\n\n"
        "**Random Seed**: 42"
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Held-Out Test Set Comparison")
    st.sidebar.metric("Tuned Random Forest (ML) Acc", "90.16%", "96.43% Recall")
    st.sidebar.metric("Final ANN (DL) Acc", "85.25%", "96.43% Recall")
    st.sidebar.caption("Evaluated on the 61-row held-out test split.")

    # Main Page Header
    st.title("🫀 Heart Disease Risk Prediction System")
    st.subheader("Machine Learning & Deep Learning Capstone Project — Educational Demonstration")
    st.markdown(
        "This application evaluates patient cardiovascular risk using frozen **Machine Learning (Tuned Random Forest)** "
        "and **Deep Learning (Artificial Neural Network - ANN)** pipelines trained on clinical diagnostic attributes "
        "from the UCI Heart Disease dataset."
    )
    st.markdown("---")

    # Disclaimer Banner
    st.warning(
        "⚠️ **Educational Disclaimer**: This application is an educational/research demonstration created "
        "for a college capstone project. It is not a clinically validated medical diagnostic system "
        "and should not be used for medical decision-making."
    )

    # Check ML Model Artifact Availability
    try:
        ml_model = get_ml_model()
    except Exception as e:
        st.error(f"Error loading ML model artifact: {e}. Please ensure `models/final/final_model.joblib` exists.")
        return

    # Sample Record Loader & Reset Controls
    sample_df = get_sample_test_records()
    
    col_demo1, col_demo2 = st.columns([3, 1])
    
    with col_demo1:
        if not sample_df.empty:
            sample_idx = st.selectbox(
                "💡 Select an Example Patient Record from Held-Out Test Set (for Demonstration):",
                options=[None] + list(range(len(sample_df))),
                format_func=lambda x: "Choose an example patient record..." if x is None else f"Patient Record #{x + 1} (Age: {sample_df.iloc[x]['age']}, Sex: {'Male' if sample_df.iloc[x]['sex']==1 else 'Female'}, Max HR: {sample_df.iloc[x]['thalach']})"
            )
        else:
            sample_idx = None

    with col_demo2:
        st.write("") # Spacer
        st.write("")
        reset_pressed = st.button("🔄 Reset Inputs")

    if reset_pressed:
        st.session_state.clear()
        st.rerun()

    # Pre-populate form values if example record selected
    if sample_idx is not None and not sample_df.empty:
        row = sample_df.iloc[sample_idx]
        default_age = int(row["age"])
        default_sex = int(row["sex"])
        default_cp = int(row["cp"])
        default_trestbps = int(row["trestbps"])
        default_chol = int(row["chol"])
        default_fbs = int(row["fbs"])
        default_restecg = int(row["restecg"])
        default_thalach = int(row["thalach"])
        default_exang = int(row["exang"])
        default_oldpeak = float(row["oldpeak"])
        default_slope = int(row["slope"])
        default_ca = int(row["ca"])
        default_thal = int(row["thal"])
        st.info(f"Loaded Patient Record #{sample_idx + 1} from held-out test set — for demonstration only.")
    else:
        default_age = 55
        default_sex = 1
        default_cp = 1
        default_trestbps = 130
        default_chol = 240
        default_fbs = 0
        default_restecg = 0
        default_thalach = 150
        default_exang = 0
        default_oldpeak = 1.0
        default_slope = 1
        default_ca = 0
        default_thal = 3

    # Main Clinical Input Form
    with st.form("patient_prediction_form"):
        st.markdown("### Patient Clinical Features Form")

        # Model Architecture Selection Choice
        selected_model_type = st.radio(
            "Select Prediction Engine:",
            options=["Machine Learning (Tuned Random Forest — Recommended)", "Deep Learning (Artificial Neural Network — ANN-3)"],
            index=0,
            horizontal=True,
            help="Choose between the primary frozen Random Forest ML model or the secondary Deep Learning ANN model."
        )

        st.markdown("---")

        # --- Section 1: Patient Information ---
        st.markdown("#### 1. Patient Demographic Information")
        c1, c2 = st.columns(2)
        with c1:
            age = st.number_input(
                "Age (years)",
                min_value=20,
                max_value=100,
                value=default_age,
                help="Patient age in years [Observed dataset range: 29–77]"
            )
        with c2:
            sex_options = {1: "Male", 0: "Female"}
            sex = st.selectbox(
                "Sex",
                options=list(sex_options.keys()),
                format_func=lambda x: sex_options[x],
                index=0 if default_sex == 1 else 1,
                help="Patient biological sex"
            )

        st.markdown("---")

        # --- Section 2: Clinical Measurements ---
        st.markdown("#### 2. Physiological & Hemodynamic Measurements")
        c3, c4 = st.columns(2)
        with c3:
            trestbps = st.number_input(
                "Resting Blood Pressure (mm Hg)",
                min_value=80,
                max_value=220,
                value=default_trestbps,
                help="Resting blood pressure in mm Hg on admission to hospital [Observed dataset range: 94–200]"
            )
            chol = st.number_input(
                "Serum Cholesterol (mg/dl)",
                min_value=100,
                max_value=600,
                value=default_chol,
                help="Serum cholesterol measurement in mg/dl [Observed dataset range: 126–564]"
            )
        with c4:
            thalach = st.number_input(
                "Maximum Heart Rate Achieved (bpm)",
                min_value=60,
                max_value=220,
                value=default_thalach,
                help="Maximum heart rate achieved during exercise stress test [Observed dataset range: 71–202]"
            )
            oldpeak = st.number_input(
                "ST Depression (Oldpeak)",
                min_value=0.0,
                max_value=10.0,
                value=default_oldpeak,
                step=0.1,
                help="ST depression induced by exercise relative to rest [Observed dataset range: 0.0–6.2]"
            )

        st.markdown("---")

        # --- Section 3: Heart & ECG Characteristics ---
        st.markdown("#### 3. Cardiac & Electrocardiographic Characteristics")
        c5, c6 = st.columns(2)
        
        with c5:
            cp_options = {
                1: "1 - Typical Angina",
                2: "2 - Atypical Angina",
                3: "3 - Non-Anginal Pain",
                4: "4 - Asymptomatic"
            }
            cp = st.selectbox(
                "Chest Pain Type (cp)",
                options=list(cp_options.keys()),
                format_func=lambda x: cp_options[x],
                index=max(0, min(default_cp - 1, 3)),
                help="Chest pain type category reported by patient"
            )

            fbs_options = {0: "False (<= 120 mg/dl)", 1: "True (> 120 mg/dl)"}
            fbs = st.selectbox(
                "Fasting Blood Sugar > 120 mg/dl (fbs)",
                options=list(fbs_options.keys()),
                format_func=lambda x: fbs_options[x],
                index=0 if default_fbs == 0 else 1,
                help="Fasting blood sugar > 120 mg/dl indicator"
            )

            restecg_options = {
                0: "0 - Normal",
                1: "1 - ST-T Wave Abnormality",
                2: "2 - Left Ventricular Hypertrophy"
            }
            restecg = st.selectbox(
                "Resting ECG Results (restecg)",
                options=list(restecg_options.keys()),
                format_func=lambda x: restecg_options[x],
                index=max(0, min(default_restecg, 2)),
                help="Resting electrocardiographic results"
            )

            exang_options = {0: "No", 1: "Yes"}
            exang = st.selectbox(
                "Exercise-Induced Angina (exang)",
                options=list(exang_options.keys()),
                format_func=lambda x: exang_options[x],
                index=0 if default_exang == 0 else 1,
                help="Exercise induced angina present"
            )

        with c6:
            slope_options = {
                1: "1 - Upsloping",
                2: "2 - Flat",
                3: "3 - Downsloping"
            }
            slope = st.selectbox(
                "ST Segment Slope (slope)",
                options=list(slope_options.keys()),
                format_func=lambda x: slope_options[x],
                index=max(0, min(default_slope - 1, 2)),
                help="Slope of the peak exercise ST segment"
            )

            ca_options = {0: "0 Vessels", 1: "1 Vessel", 2: "2 Vessels", 3: "3 Vessels"}
            ca = st.selectbox(
                "Number of Major Vessels Colored by Fluoroscopy (ca)",
                options=list(ca_options.keys()),
                format_func=lambda x: ca_options[x],
                index=max(0, min(default_ca, 3)),
                help="Number of major vessels (0-3) colored by fluoroscopy"
            )

            thal_options = {
                3: "3 - Normal",
                6: "6 - Fixed Defect",
                7: "7 - Reversible Defect"
            }
            thal_keys = list(thal_options.keys())
            thal_idx = thal_keys.index(default_thal) if default_thal in thal_keys else 0
            thal = st.selectbox(
                "Thalassemia (thal)",
                options=thal_keys,
                format_func=lambda x: thal_options[x],
                index=thal_idx,
                help="Thalassemia nuclear blood disorder status"
            )

        submit_btn = st.form_submit_button("🩺 Predict Heart Disease Risk", type="primary")

    # Execution of Model Prediction Routine
    if submit_btn:
        input_data = {
            "age": age,
            "sex": sex,
            "cp": cp,
            "trestbps": trestbps,
            "chol": chol,
            "fbs": fbs,
            "restecg": restecg,
            "thalach": thalach,
            "exang": exang,
            "oldpeak": oldpeak,
            "slope": slope,
            "ca": ca,
            "thal": thal
        }

        try:
            if "Machine Learning" in selected_model_type:
                result = predict_heart_disease(input_data)
                pred_class = result["predicted_class"][0]
                prob_disease = result["probability_disease"][0]
                prob_no_disease = result["probability_no_disease"][0]
                engine_name = "Frozen Tuned Random Forest (ML)"
            else:
                dl_model = get_dl_model()
                preprocessor = get_preprocessor()
                if dl_model is None or preprocessor is None:
                    st.error("Deep Learning model or preprocessor artifact not found.")
                    return
                
                validated_df = validate_input_data(input_data)
                X_trans = preprocessor.transform(validated_df)
                dl_res = predict_ann(dl_model, X_trans)
                pred_class = dl_res["predicted_class"][0]
                prob_disease = dl_res["probability_disease"][0]
                prob_no_disease = dl_res["probability_no_disease"][0]
                engine_name = "Frozen Artificial Neural Network (DL ANN-3)"

            st.markdown(f"### Model Output & Risk Estimation (`{engine_name}`)")
            
            res_col1, res_col2, res_col3 = st.columns([2, 1, 1])

            with res_col1:
                if pred_class == 1:
                    st.error("### Model Prediction: Heart Disease Present")
                    st.write(f"**Assessment**: The `{engine_name}` pipeline estimates elevated likelihood of cardiovascular disease presence.")
                else:
                    st.success("### Model Prediction: No Heart Disease")
                    st.write(f"**Assessment**: The `{engine_name}` pipeline estimates low likelihood of cardiovascular disease presence.")

            with res_col2:
                st.metric("Heart Disease Probability", f"{prob_disease * 100:.1f}%")

            with res_col3:
                st.metric("No Disease Probability", f"{prob_no_disease * 100:.1f}%")

            st.markdown("---")

        except Exception as e:
            st.error(f"An error occurred during model inference: {e}")

    # Expandable Details Sections
    st.markdown("### 📊 Project Insights & Benchmark Details")

    with st.expander("🤖 Machine Learning vs Deep Learning Benchmark Comparison"):
        ml_dl_df = get_ml_vs_dl_table()
        if not ml_dl_df.empty:
            st.dataframe(ml_dl_df, use_container_width=True)
            ml_dl_fig_path = PROJECT_ROOT / "results" / "figures" / "deep_learning" / "ml_vs_dl_comparison.png"
            if ml_dl_fig_path.exists():
                st.image(str(ml_dl_fig_path), caption="ML vs DL Held-Out Test Metric Comparison", use_container_width=True)

    with st.expander("ℹ️ About the Frozen Models"):
        metadata = get_metadata()
        st.write("**Primary Model (ML)**: Tuned Random Forest (`RandomForestClassifier`) — Test Acc: 90.16%, Recall: 96.43%, ROC-AUC: 0.9567")
        st.write("**Secondary Model (DL)**: Artificial Neural Network (`ANN-3: 28->64->32->16->1`) — Test Acc: 85.25%, Recall: 96.43%, ROC-AUC: 0.9253")

    with st.expander("⭐ Model Feature Importance Rankings"):
        fi_df = get_feature_importance()
        if not fi_df.empty:
            st.caption("Feature importance indicates how the trained model used transformed features for prediction; it does not establish medical causation.")
            st.dataframe(fi_df.head(15), use_container_width=True)

    # Footer
    st.markdown("---")
    st.caption("Heart Disease Prediction Capstone Project | Department of Computer Science & Engineering | Part 10 DL Integration")


if __name__ == "__main__":
    main()
