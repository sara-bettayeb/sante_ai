"""Pydantic schemas for the /api/predict endpoint."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    age: int = Field(..., ge=0, le=120, description="Age in years")
    gender: int = Field(..., ge=0, le=1, description="0 = female, 1 = male")
    bmi: float = Field(..., ge=10.0, le=60.0, description="Body mass index")
    systolic: int = Field(..., ge=60, le=250, description="Systolic blood pressure (mmHg)")
    diastolic: int = Field(..., ge=40, le=150, description="Diastolic blood pressure (mmHg)")
    heartRate: int = Field(..., ge=30, le=220, description="Resting heart rate (bpm)")
    familyHistory: int = Field(..., ge=0, le=1, description="0 = no, 1 = yes")
    smoking: int = Field(..., ge=0, le=1, description="0 = no, 1 = yes")
    physicalActivity: int = Field(..., ge=0, le=1, description="0 = sedentary, 1 = active")
    salt: float = Field(..., ge=0.0, le=30.0, description="Daily salt intake (grams)")
    stress: int = Field(..., ge=0, le=1, description="0 = low, 1 = high")
    sleep: float = Field(..., ge=0.0, le=24.0, description="Sleep hours per night")
    diabetes: int = Field(..., ge=0, le=1, description="0 = no, 1 = yes")
    thyroid: int = Field(..., ge=0, le=1, description="0 = no, 1 = yes")


class PredictResponse(BaseModel):
    prediction: int = Field(..., description="0 = no hypertension, 1 = hypertension")
    probability: float = Field(..., description="Probability of hypertension (0..1)")
    risk_band: str = Field(..., description="low / medium / high")
    model_version: str
