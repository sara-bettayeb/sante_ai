# AI E-Health — Hypertension module (Python)

Educational project — **not a medical tool.**
FastAPI + scikit-learn (Logistic Regression) + Docker. No database.

## Run locally
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements-dev.txt
python model/train.py           # trains + saves model/model.pkl
uvicorn app.main:app --reload   # http://localhost:8000  (docs: /docs)
pytest                          # tests
```

## Docker
```bash
docker compose up -d --build    # http://localhost:8004
```

## API
`POST /api/predict` — body fields: age, gender, bmi, systolic, diastolic, heartRate,
familyHistory, smoking, physicalActivity, salt, stress, sleep, diabetes, thyroid.
`GET /api/predict` — accepted fields + model metrics. `GET /health` — healthcheck.

## Use a real dataset
`python model/train.py data/real.csv` (CSV with the 14 feature columns + `target` 0/1,
encoded as described in `model/train.py`).
