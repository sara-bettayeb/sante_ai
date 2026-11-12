"""FastAPI application for hypertension prediction.

Educational project - not a medical tool.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.schemas import PredictRequest, PredictResponse
from model.features import FEATURE_COLUMNS

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
MODEL_PATH = PROJECT_ROOT / "model" / "model.pkl"
STATIC_DIR = PROJECT_ROOT / "static"

MODEL_VERSION = "1.0.0"

app = FastAPI(
    title="AI E-Health - Hypertension module",
    description=(
        "Educational hypertension risk predictor (Logistic Regression). "
        "Not a medical tool."
    ),
    version=MODEL_VERSION,
)

# Serve the web UI at / and the static assets under /static
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def root() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


def _load_model() -> dict[str, Any]:
    if not MODEL_PATH.exists():
        raise RuntimeError(
            f"Model file not found at {MODEL_PATH}. "
            "Run `python model/train.py` first."
        )
    return joblib.load(MODEL_PATH)


def _risk_band(prob: float) -> str:
    if prob < 0.33:
        return "low"
    if prob < 0.66:
        return "medium"
    return "high"


try:
    _BUNDLE = _load_model()
    _PIPELINE = _BUNDLE["pipeline"]
    _METRICS = _BUNDLE["metrics"]
    _MODEL_STATUS = "loaded"
except Exception as exc:  # pragma: no cover - exercised only when model missing
    _PIPELINE = None
    _METRICS = {}
    _MODEL_STATUS = f"error: {exc}"


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "model": _MODEL_STATUS, "version": MODEL_VERSION}


@app.get("/api/predict")
def describe() -> dict[str, Any]:
    """Describe the accepted fields and return the model's training metrics."""
    return {
        "fields": FEATURE_COLUMNS,
        "encoding": {
            "gender": "0=female, 1=male",
            "familyHistory": "0=no, 1=yes",
            "smoking": "0=no, 1=yes",
            "physicalActivity": "0=sedentary, 1=active",
            "stress": "0=low, 1=high",
            "diabetes": "0=no, 1=yes",
            "thyroid": "0=no, 1=yes",
        },
        "metrics": _METRICS,
        "model_status": _MODEL_STATUS,
    }


@app.post("/api/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    if _PIPELINE is None:
        raise HTTPException(status_code=503, detail=f"Model not available: {_MODEL_STATUS}")

    row = pd.DataFrame([[getattr(req, f) for f in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)
    prob = float(_PIPELINE.predict_proba(row)[0, 1])
    pred = int(prob >= 0.5)

    return PredictResponse(
        prediction=pred,
        probability=round(prob, 4),
        risk_band=_risk_band(prob),
        model_version=MODEL_VERSION,
    )
