import os
import sqlite3
import pytest
import joblib
import numpy as np


def test_database_initialization(tmp_path, monkeypatch):
    import database
    test_db = str(tmp_path / "test_sante.db")
    monkeypatch.setattr(database, "DB_PATH", test_db)
    database.init_db()
    assert os.path.exists(test_db)

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    assert len(tables) > 0


def test_model_prediction():
    model_path = os.path.join("models", "ensemble.joblib")
    if not os.path.exists(model_path):
        pytest.skip("Model file not found")
    model = joblib.load(model_path)
    sample_patient = np.array([[55, 1, 0, 140, 240, 0, 1, 150, 0, 1.5, 1, 0, 2]])
    prediction = model.predict(sample_patient)
    assert prediction[0] in [0, 1]


def test_core_files_exist():
    for f in ["app.py", "database.py", "streamlit_app.py", "docker-compose.yml"]:
        assert os.path.exists(f), f"Missing: {f}"