"""Train a Logistic Regression model for hypertension prediction.

Usage:
    python model/train.py                  # trains on synthetic data, saves model/model.pkl
    python model/train.py data/real.csv    # trains on a real CSV dataset

The CSV must contain the 14 feature columns listed in `model/features.py`
plus a `target` column (0 = no hypertension, 1 = hypertension). Binary
features must already be encoded as 0/1.

Educational project - not a medical tool.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

# Make `model.features` importable when running as `python model/train.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from model.features import (  # noqa: E402
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    BINARY_FEATURES,
    NUMERIC_RANGES,
)

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
MODEL_PATH = HERE / "model.pkl"


def generate_synthetic_data(n_samples: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Generate a small synthetic dataset for demonstration purposes.

    The data is generated so that hypertension risk increases with age,
    BMI, blood pressure, salt intake, smoking, family history, diabetes,
    thyroid disease, stress, and low sleep; and decreases with physical
    activity. Replace this with a real dataset before any serious use.
    """
    rng = np.random.default_rng(seed)

    data = {}
    data["age"] = rng.integers(NUMERIC_RANGES["age"][0], NUMERIC_RANGES["age"][1] + 1, n_samples)
    data["gender"] = rng.integers(0, 2, n_samples)
    data["bmi"] = rng.uniform(*NUMERIC_RANGES["bmi"], n_samples).round(1)
    data["systolic"] = rng.integers(NUMERIC_RANGES["systolic"][0], NUMERIC_RANGES["systolic"][1] + 1, n_samples)
    data["diastolic"] = rng.integers(NUMERIC_RANGES["diastolic"][0], NUMERIC_RANGES["diastolic"][1] + 1, n_samples)
    data["heartRate"] = rng.integers(NUMERIC_RANGES["heartRate"][0], NUMERIC_RANGES["heartRate"][1] + 1, n_samples)
    data["familyHistory"] = rng.integers(0, 2, n_samples)
    data["smoking"] = rng.integers(0, 2, n_samples)
    data["physicalActivity"] = rng.integers(0, 2, n_samples)
    data["salt"] = rng.uniform(*NUMERIC_RANGES["salt"], n_samples).round(1)
    data["stress"] = rng.integers(0, 2, n_samples)
    data["sleep"] = rng.uniform(*NUMERIC_RANGES["sleep"], n_samples).round(1)
    data["diabetes"] = rng.integers(0, 2, n_samples)
    data["thyroid"] = rng.integers(0, 2, n_samples)

    df = pd.DataFrame(data)

    # Logistic-style risk score -> probability -> label
    z = (
        0.04 * (df["age"] - 50)
        + 0.06 * (df["bmi"] - 25)
        + 0.03 * (df["systolic"] - 120)
        + 0.03 * (df["diastolic"] - 80)
        + 0.02 * (df["heartRate"] - 75)
        + 0.5 * df["familyHistory"]
        + 0.6 * df["smoking"]
        - 0.5 * df["physicalActivity"]
        + 0.15 * (df["salt"] - 5)
        + 0.5 * df["stress"]
        - 0.20 * (df["sleep"] - 7)
        + 0.7 * df["diabetes"]
        + 0.4 * df["thyroid"]
    )
    prob = 1 / (1 + np.exp(-z))
    df[TARGET_COLUMN] = (rng.random(n_samples) < prob).astype(int)
    return df


def load_data(csv_path: str | None) -> pd.DataFrame:
    if csv_path:
        df = pd.read_csv(csv_path)
        missing = [c for c in FEATURE_COLUMNS + [TARGET_COLUMN] if c not in df.columns]
        if missing:
            raise SystemExit(
                f"CSV is missing required columns: {missing}. "
                f"Expected: {FEATURE_COLUMNS + [TARGET_COLUMN]}"
            )
        return df[FEATURE_COLUMNS + [TARGET_COLUMN]]
    return generate_synthetic_data()


def train(df: pd.DataFrame) -> tuple[Pipeline, dict]:
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
    ])
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "n_features": len(FEATURE_COLUMNS),
        "features": FEATURE_COLUMNS,
        "binary_features": sorted(BINARY_FEATURES),
    }

    print("=== Hypertension model training ===")
    print(f"Train size: {len(y_train)} | Test size: {len(y_test)}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"ROC-AUC : {metrics['roc_auc']:.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, target_names=["no hypertension", "hypertension"]))
    return pipeline, metrics


def save_model(pipeline: Pipeline, metrics: dict) -> None:
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipeline, "metrics": metrics}, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")


def main() -> None:
    csv_path = sys.argv[1] if len(sys.argv) > 1 else None
    if csv_path:
        print(f"Training on real dataset: {csv_path}")
    else:
        print("No CSV provided - training on synthetic data (educational only).")

    df = load_data(csv_path)
    pipeline, metrics = train(df)
    save_model(pipeline, metrics)


if __name__ == "__main__":
    main()
