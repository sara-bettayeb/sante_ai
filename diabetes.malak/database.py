import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diabetes_records.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnostics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            department TEXT NOT NULL,
            inputs_summary TEXT,
            result TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_diagnostic(patient_name: str, department: str, inputs_summary: str, result: str):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO diagnostics (patient_name, department, inputs_summary, result, created_at) VALUES (?, ?, ?, ?, ?)",
        (patient_name, department, inputs_summary, result, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


def get_all_diagnostics(department: str):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id AS 'الرقم', patient_name AS 'اسم المستفيد', inputs_summary AS 'ملخص المؤشرات', result AS 'النتيجة', created_at AS 'التاريخ' FROM diagnostics WHERE department = ? ORDER BY id DESC",
        (department,),
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows