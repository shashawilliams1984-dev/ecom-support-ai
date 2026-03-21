import sqlite3

DB_NAME = "support_ai.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_column(cursor, table_name: str, column_name: str, definition: str):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]

    if column_name not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decision_logs (
        id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        question TEXT NOT NULL,
        intent TEXT,
        order_number TEXT,
        order_status TEXT,
        decision TEXT,
        answer TEXT,
        needs_human INTEGER DEFAULT 0,
        escalation_reason TEXT
    )
    """)

    ensure_column(cursor, "decision_logs", "needs_human", "INTEGER DEFAULT 0")
    ensure_column(cursor, "decision_logs", "escalation_reason", "TEXT")

    conn.commit()
    conn.close()
