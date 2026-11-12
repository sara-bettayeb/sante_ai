"""Feature column definitions shared by training and inference.

Keeping these in one place avoids drift between `model/train.py` and `app/main.py`.
"""

# Order matters: it is the exact column order the model was trained on.
FEATURE_COLUMNS = [
    "age",
    "gender",
    "bmi",
    "systolic",
    "diastolic",
    "heartRate",
    "familyHistory",
    "smoking",
    "physicalActivity",
    "salt",
    "stress",
    "sleep",
    "diabetes",
    "thyroid",
]

TARGET_COLUMN = "target"

# Binary features (already 0/1 in the input). Numeric features are passed through.
BINARY_FEATURES = {
    "gender",            # 0 = female, 1 = male
    "familyHistory",     # 0 = no, 1 = yes
    "smoking",           # 0 = no, 1 = yes
    "physicalActivity",  # 0 = sedentary, 1 = active
    "stress",            # 0 = low, 1 = high
    "diabetes",          # 0 = no, 1 = yes
    "thyroid",           # 0 = no, 1 = yes
}

# Numeric ranges used by the synthetic data generator (kept here so the
# training script and the docs agree on plausible value ranges).
NUMERIC_RANGES = {
    "age":        (18, 90),
    "bmi":        (16.0, 45.0),
    "systolic":   (90, 200),
    "diastolic":  (60, 120),
    "heartRate":  (50, 120),
    "salt":       (1.0, 12.0),   # grams/day
    "sleep":      (3.0, 10.0),   # hours/night
}
