"""Smoke tests for the hypertension API.

Run with `pytest` from the project root.
"""
from __future__ import annotations

import joblib
from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["model"] == "loaded"


def test_describe_lists_all_fields() -> None:
    r = client.get("/api/predict")
    assert r.status_code == 200
    body = r.json()
    assert len(body["fields"]) == 14
    assert "metrics" in body


def test_predict_low_risk_profile() -> None:
    # Young, active, non-smoker, normal vitals -> should be low risk.
    payload = {
        "age": 25, "gender": 1, "bmi": 22.0, "systolic": 110, "diastolic": 70,
        "heartRate": 68, "familyHistory": 0, "smoking": 0, "physicalActivity": 1,
        "salt": 5.0, "stress": 0, "sleep": 8.0, "diabetes": 0, "thyroid": 0,
    }
    r = client.post("/api/predict", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["prediction"] in (0, 1)
    assert 0.0 <= body["probability"] <= 1.0
    assert body["risk_band"] in ("low", "medium", "high")


def test_predict_high_risk_profile() -> None:
    # Old, smoker, hypertensive vitals, family history -> should be high risk.
    payload = {
        "age": 72, "gender": 0, "bmi": 34.0, "systolic": 180, "diastolic": 110,
        "heartRate": 95, "familyHistory": 1, "smoking": 1, "physicalActivity": 0,
        "salt": 11.0, "stress": 1, "sleep": 4.0, "diabetes": 1, "thyroid": 1,
    }
    r = client.post("/api/predict", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["prediction"] == 1
    assert body["probability"] >= 0.5
    assert body["risk_band"] == "high"


def test_high_risk_prob_strictly_greater_than_low_risk() -> None:
    low = {
        "age": 22, "gender": 1, "bmi": 21.0, "systolic": 105, "diastolic": 65,
        "heartRate": 60, "familyHistory": 0, "smoking": 0, "physicalActivity": 1,
        "salt": 4.0, "stress": 0, "sleep": 8.5, "diabetes": 0, "thyroid": 0,
    }
    high = {
        "age": 75, "gender": 1, "bmi": 36.0, "systolic": 185, "diastolic": 115,
        "heartRate": 100, "familyHistory": 1, "smoking": 1, "physicalActivity": 0,
        "salt": 12.0, "stress": 1, "sleep": 3.5, "diabetes": 1, "thyroid": 1,
    }
    p_low = client.post("/api/predict", json=low).json()["probability"]
    p_high = client.post("/api/predict", json=high).json()["probability"]
    assert p_high > p_low


def test_validation_rejects_out_of_range() -> None:
    bad = {
        "age": 999, "gender": 1, "bmi": 22.0, "systolic": 110, "diastolic": 70,
        "heartRate": 68, "familyHistory": 0, "smoking": 0, "physicalActivity": 1,
        "salt": 5.0, "stress": 0, "sleep": 8.0, "diabetes": 0, "thyroid": 0,
    }
    r = client.post("/api/predict", json=bad)
    assert r.status_code == 422
