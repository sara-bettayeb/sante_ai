import os
import sqlite3
from datetime import datetime

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "sante_ai_db")
DB_USER = os.getenv("DB_USER", "sante_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "sante_pass123")

SQLITE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sante_ai.db")


def get_connection():
    """يتصل بـ PostgreSQL أولاً، وإذا لم يكن الخادم متاحاً يتحول تلقائياً إلى SQLite."""
    if psycopg2 is not None:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                connect_timeout=2,
            )
            return conn, "postgres"
        except Exception:
            pass

    conn = sqlite3.connect(SQLITE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn, "sqlite"


def init_db():
    """ينشئ جدول التشخيصات الطبية إن لم يكن موجوداً."""
    conn, db_type = get_connection()
    cur = conn.cursor()
    if db_type == "postgres":
        cur.execute("""
            CREATE TABLE IF NOT EXISTS diagnostics (
                id SERIAL PRIMARY KEY,
                patient_name VARCHAR(150) NOT NULL,
                module_name VARCHAR(100) NOT NULL,
                inputs_summary TEXT,
                prediction_result VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    else:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS diagnostics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                module_name TEXT NOT NULL,
                inputs_summary TEXT,
                prediction_result TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.commit()
    cur.close()
    conn.close()


def save_diagnostic(patient_name: str, module_name: str, inputs_summary: str, prediction_result: str):
    """يحفظ نتيجة تشخيص جديدة في قاعدة البيانات."""
    init_db()
    conn, db_type = get_connection()
    cur = conn.cursor()
    clean_name = patient_name.strip() if patient_name and patient_name.strip() else "Patient Anonyme"
    if db_type == "postgres":
        cur.execute(
            """
            INSERT INTO diagnostics (patient_name, module_name, inputs_summary, prediction_result)
            VALUES (%s, %s, %s, %s);
            """,
            (clean_name, module_name, inputs_summary, prediction_result),
        )
    else:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(
            """
            INSERT INTO diagnostics (patient_name, module_name, inputs_summary, prediction_result, created_at)
            VALUES (?, ?, ?, ?, ?);
            """,
            (clean_name, module_name, inputs_summary, prediction_result, now_str),
        )
    conn.commit()
    cur.close()
    conn.close()


def get_all_diagnostics(module_name: str = None):
    """يجلب سجل التشخيصات (الكل أو لوحدة طبية محددة)."""
    init_db()
    conn, db_type = get_connection()
    if db_type == "postgres":
        cur = conn.cursor(cursor_factory=RealDictCursor)
        if module_name:
            cur.execute(
                "SELECT id, patient_name, module_name, inputs_summary, prediction_result, created_at FROM diagnostics WHERE module_name = %s ORDER BY id DESC;",
                (module_name,),
            )
        else:
            cur.execute(
                "SELECT id, patient_name, module_name, inputs_summary, prediction_result, created_at FROM diagnostics ORDER BY id DESC;"
)
        rows = [dict(r) for r in cur.fetchall()]
    else:
        cur = conn.cursor()
        if module_name:
            cur.execute(
                "SELECT id, patient_name, module_name, inputs_summary, prediction_result, created_at FROM diagnostics WHERE module_name = ? ORDER BY id DESC;",
                (module_name,),
            )
        else:
            cur.execute(
                "SELECT id, patient_name, module_name, inputs_summary, prediction_result, created_at FROM diagnostics ORDER BY id DESC;"
            )
        rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return rows
