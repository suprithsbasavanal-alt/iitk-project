"""
Deep Learning Artificial Neural Network (ANN) Module (Part 10).

Provides reusable functions for building, compiling, training, evaluating,
saving, loading, and predicting using Keras feed-forward Multi-Layer Perceptrons (ANN).
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Union
import numpy as np
import pandas as pd

# Enforce PyTorch backend for Keras 3.x
os.environ["KERAS_BACKEND"] = "torch"
import keras
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)


def build_ann_model(
    input_dim: int = 28,
    layer_sizes: Optional[List[int]] = None,
    dropout_rates: Optional[List[float]] = None,
    learning_rate: float = 0.001
) -> keras.Model:
    """
    Build and compile a feed-forward Artificial Neural Network (ANN) for binary classification.

    Parameters
    ----------
    input_dim : int
        Number of input features (default: 28).
    layer_sizes : List[int], optional
        Sizes of hidden layers. Default is [64, 32].
    dropout_rates : List[float], optional
        Dropout rate for each hidden layer. Default is [0.3, 0.2].
    learning_rate : float
        Initial Adam optimizer learning rate (default: 0.001).

    Returns
    -------
    keras.Model
        Compiled Keras Sequential model.
    """
    if layer_sizes is None:
        layer_sizes = [64, 32]
    if dropout_rates is None:
        dropout_rates = [0.3, 0.2]

    assert len(layer_sizes) == len(dropout_rates), "Layer sizes and dropout rates must have identical lengths"

    layers = [keras.layers.Input(shape=(input_dim,))]
    for size, drop_rate in zip(layer_sizes, dropout_rates):
        layers.append(keras.layers.Dense(size, activation="relu"))
        if drop_rate > 0.0:
            layers.append(keras.layers.Dropout(drop_rate))

    # Binary Classification Output Layer
    layers.append(keras.layers.Dense(1, activation="sigmoid"))

    model = keras.Sequential(layers)

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(
        optimizer=optimizer,
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            keras.metrics.Precision(name="precision"),
            keras.metrics.Recall(name="recall"),
            keras.metrics.AUC(name="auc")
        ]
    )
    return model


def build_candidate_architectures(input_dim: int = 28) -> Dict[str, Dict[str, Any]]:
    """
    Construct the three candidate ANN architectures for validation comparison.

    Parameters
    ----------
    input_dim : int
        Number of input features (default: 28).

    Returns
    -------
    Dict[str, Dict[str, Any]]
        Dictionary mapping candidate architecture names to their structural parameters.
    """
    return {
        "ANN-1": {
            "description": "28 -> 32 -> 16 -> 1",
            "layer_sizes": [32, 16],
            "dropout_rates": [0.2, 0.1]
        },
        "ANN-2": {
            "description": "28 -> 64 -> 32 -> 1",
            "layer_sizes": [64, 32],
            "dropout_rates": [0.3, 0.2]
        },
        "ANN-3": {
            "description": "28 -> 64 -> 32 -> 16 -> 1",
            "layer_sizes": [64, 32, 16],
            "dropout_rates": [0.3, 0.2, 0.1]
        }
    }


def train_ann(
    model: keras.Model,
    X_train: Union[np.ndarray, pd.DataFrame],
    y_train: Union[np.ndarray, pd.Series],
    X_val: Union[np.ndarray, pd.DataFrame],
    y_val: Union[np.ndarray, pd.Series],
    epochs: int = 150,
    batch_size: int = 16,
    patience_es: int = 15,
    patience_lr: int = 7,
    verbose: int = 0
) -> Tuple[keras.Model, pd.DataFrame]:
    """
    Train an ANN model with EarlyStopping and ReduceLROnPlateau callbacks.

    Parameters
    ----------
    model : keras.Model
        Compiled Keras model.
    X_train : np.ndarray or pd.DataFrame
        Training feature matrix.
    y_train : np.ndarray or pd.Series
        Training labels.
    X_val : np.ndarray or pd.DataFrame
        Validation feature matrix.
    y_val : np.ndarray or pd.Series
        Validation labels.
    epochs : int
        Maximum training epochs (default: 150).
    batch_size : int
        Mini-batch size (default: 16).
    patience_es : int
        Early stopping patience (default: 15).
    patience_lr : int
        Reduce LR patience (default: 7).
    verbose : int
        Verbosity level (default: 0).

    Returns
    -------
    Tuple[keras.Model, pd.DataFrame]
        Trained Keras model and training history DataFrame.
    """
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=patience_es,
            restore_best_weights=True,
            verbose=verbose
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=patience_lr,
            min_lr=1e-6,
            verbose=verbose
        )
    ]

    history = model.fit(
        np.asarray(X_train, dtype=np.float32),
        np.asarray(y_train, dtype=np.float32).reshape(-1, 1),
        validation_data=(
            np.asarray(X_val, dtype=np.float32),
            np.asarray(y_val, dtype=np.float32).reshape(-1, 1)
        ),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=verbose
    )

    history_df = pd.DataFrame(history.history)
    history_df["epoch"] = np.arange(1, len(history_df) + 1)
    return model, history_df


def evaluate_ann(
    model: keras.Model,
    X_eval: Union[np.ndarray, pd.DataFrame],
    y_eval: Union[np.ndarray, pd.Series],
    threshold: float = 0.50
) -> Dict[str, Any]:
    """
    Evaluate ANN model performance on a specified dataset split.

    Parameters
    ----------
    model : keras.Model
        Trained Keras model.
    X_eval : np.ndarray or pd.DataFrame
        Feature matrix.
    y_eval : np.ndarray or pd.Series
        True target labels.
    threshold : float
        Decision threshold for class assignment (default: 0.50).

    Returns
    -------
    Dict[str, Any]
        Dictionary of performance metrics.
    """
    probs = model.predict(np.asarray(X_eval, dtype=np.float32), verbose=0).ravel()
    preds = (probs >= threshold).astype(int)
    y_true = np.asarray(y_eval, dtype=int).ravel()

    tn, fp, fn, tp = confusion_matrix(y_true, preds).ravel()
    acc = accuracy_score(y_true, preds)
    prec = precision_score(y_true, preds, zero_division=0)
    rec = recall_score(y_true, preds, zero_division=0)
    spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    f1 = f1_score(y_true, preds, zero_division=0)
    auc_val = roc_auc_score(y_true, probs)

    return {
        "Accuracy": float(acc),
        "Precision": float(prec),
        "Recall": float(rec),
        "Specificity": float(spec),
        "F1": float(f1),
        "ROC-AUC": float(auc_val),
        "TN": int(tn),
        "FP": int(fp),
        "FN": int(fn),
        "TP": int(tp)
    }


def save_ann_model(model: keras.Model, filepath: Union[str, Path]) -> None:
    """Save trained Keras ANN model to disk."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    model.save(filepath)


def load_ann_model(filepath: Union[str, Path]) -> keras.Model:
    """Load Keras ANN model from disk."""
    return keras.models.load_model(filepath)


def predict_ann(
    model: keras.Model,
    X_input: Union[np.ndarray, pd.DataFrame],
    threshold: float = 0.50
) -> Dict[str, Any]:
    """
    Generate predictions and risk probabilities for input features using trained ANN.

    Parameters
    ----------
    model : keras.Model
        Trained Keras model.
    X_input : np.ndarray or pd.DataFrame
        Input feature matrix (must have 28 preprocessed features).
    threshold : float
        Decision threshold (default: 0.50).

    Returns
    -------
    Dict[str, Any]
        Dictionary with predicted_class, probability_disease, and probability_no_disease.
    """
    probs_disease = model.predict(np.asarray(X_input, dtype=np.float32), verbose=0).ravel()
    probs_no_disease = 1.0 - probs_disease
    pred_class = (probs_disease >= threshold).astype(int)

    return {
        "predicted_class": pred_class.tolist(),
        "probability_disease": probs_disease.tolist(),
        "probability_no_disease": probs_no_disease.tolist()
    }
