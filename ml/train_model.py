import os
import urllib.request
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def download_data():
    """Downloads the Cleveland heart disease dataset from UCI."""
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
    os.makedirs("ml/dataset", exist_ok=True)
    filepath = "ml/dataset/processed.cleveland.data"
    
    print(f"Downloading dataset from {url}...")
    urllib.request.urlretrieve(url, filepath)
    print(f"Dataset downloaded and saved to {filepath}")
    return filepath

def main():
    # 1. Download and load data
    filepath = download_data()
    
    columns = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'num'
    ]
    
    df = pd.read_csv(filepath, names=columns, na_values="?")
    print(f"Initial shape: {df.shape}")
    print("Null values count before cleaning:\n", df.isnull().sum())
    
    # 2. Data Cleaning
    # Impute missing values (ca and thal have missing values '?') using median
    for col in df.columns:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"Imputed column {col} with median {median_val}")
            
    # Double check no nulls remain
    assert df.isnull().sum().sum() == 0, "Null values still exist!"
    
    # 3. Target mapping
    # num: 0 = Low Risk, 1-2 = Medium Risk, 3-4 = High Risk
    def map_target(num):
        if num == 0:
            return 0  # Low Risk
        elif num in [1, 2]:
            return 1  # Medium Risk
        else:
            return 2  # High Risk
            
    df['risk_class'] = df['num'].apply(map_target)
    
    # Features and Target
    X = df.drop(columns=['num', 'risk_class'])
    y = df['risk_class']
    
    print("\nClass distribution:")
    print(y.value_counts().sort_index())
    
    # 4. Train-Test Split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 5. Feature Engineering / Scaling
    # We fit the scaler on continuous columns
    continuous_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    
    scaler = StandardScaler()
    
    # Fit scaler on train data and transform both train and test
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    
    X_train_scaled[continuous_cols] = scaler.fit_transform(X_train[continuous_cols])
    X_test_scaled[continuous_cols] = scaler.transform(X_test[continuous_cols])
    
    # 6. Train Models (Random Forest)
    # n_estimators=150, max_depth=6, min_samples_split=4, class_weight='balanced' to handle class imbalance
    print("\nTraining Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=150, 
        max_depth=6, 
        min_samples_split=4, 
        class_weight='balanced', 
        random_state=42
    )
    model.fit(X_train_scaled, y_train)
    
    # 7. Evaluate Model
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {acc * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Low Risk', 'Medium Risk', 'High Risk']))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Save the model and scaler
    os.makedirs("ml", exist_ok=True)
    model_path = "ml/heart_model.pkl"
    scaler_path = "ml/scaler.pkl"
    
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)
        
    print(f"\nModel saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")

if __name__ == "__main__":
    main()
