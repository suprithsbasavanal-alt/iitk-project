import os
import pickle
import numpy as np
import pandas as pd
from typing import Dict, Any

class PredictionService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_path = "ml/heart_model.pkl"
        self.scaler_path = "ml/scaler.pkl"
        self.load_artifacts()

    def load_artifacts(self):
        """Loads model and scaler if they exist."""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            try:
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
                with open(self.scaler_path, "rb") as f:
                    self.scaler = pickle.load(f)
                print("ML Model and Scaler loaded successfully.")
            except Exception as e:
                print(f"Error loading ML artifacts: {e}")
        else:
            print("ML artifacts not found. Please train the model first.")

    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs heart disease prediction on the input data.
        Input data should contain:
        age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
        """
        # Reload artifacts if not loaded yet
        if self.model is None or self.scaler is None:
            self.load_artifacts()
            if self.model is None or self.scaler is None:
                raise ValueError("ML model or scaler is not loaded. Ensure ml/train_model.py has been run.")

        # Convert input dictionary to pandas DataFrame with appropriate column order
        cols = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
            'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
        ]
        
        # Build features array
        features_dict = {col: [data[col]] for col in cols}
        input_df = pd.DataFrame(features_dict)

        # Scale continuous features
        continuous_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
        scaled_df = input_df.copy()
        scaled_df[continuous_cols] = self.scaler.transform(input_df[continuous_cols])

        # Run Prediction
        # predict_proba returns [P(Low Risk), P(Medium Risk), P(High Risk)]
        probabilities = self.model.predict_proba(scaled_df)[0]
        predicted_class = int(np.argmax(probabilities))
        
        # Risk levels map
        risk_map = {
            0: "LOW RISK",
            1: "MEDIUM RISK",
            2: "HIGH RISK"
        }
        
        status = risk_map[predicted_class]
        confidence = float(probabilities[predicted_class]) * 100
        
        # Compute Weighted Risk Percentage
        # Low risk class weight: 0.0, Medium: 0.5, High: 1.0
        # Formula: P(Medium) * 50% + P(High) * 100%
        # Or simple weighted index scaled to 100:
        risk_pct = (probabilities[1] * 0.5 + probabilities[2] * 1.0) * 100
        
        # Ensure risk percentage aligns reasonably with predicted status bounds:
        # e.g., if Low Risk, keep it below 35%, if Med, 35-70%, if High, 70-100%
        # The expected value calculation above already behaves this way!
        
        # Default recommendations
        recommendations = ""
        if status == "LOW RISK":
            recommendations = (
                "1. Exercise regularly (at least 150 minutes of moderate activity per week).\n"
                "2. Eat healthy food, rich in fiber, vegetables, and low in saturated fats.\n"
                "3. Plan an annual health checkup to monitor cardiovascular indicators."
            )
        elif status == "MEDIUM RISK":
            recommendations = (
                "1. Consult a general physician for a comprehensive cardiovascular assessment.\n"
                "2. Reduce dietary cholesterol intake and increase soluble fiber.\n"
                "3. Start a daily walking routine (30-45 minutes at a brisk pace).\n"
                "4. Monitor blood pressure and resting heart rate twice weekly."
            )
        else:  # HIGH RISK
            recommendations = (
                "1. Schedule an immediate consultation with a cardiologist.\n"
                "2. Perform diagnostic ECG and complete cardiac lipid/enzyme panels.\n"
                "3. Implement intensive lifestyle modifications (e.g. strict low-sodium dietary plan, smoking cessation).\n"
                "4. Discuss potential preventive therapeutic management (e.g., statins, beta-blockers) with a specialist."
            )

        return {
            "prediction_status": status,
            "prediction_confidence": round(confidence, 1),
            "risk_percentage": round(risk_pct, 1),
            "recommendation": recommendations
        }

prediction_service = PredictionService()
