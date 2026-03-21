from datetime import datetime, timezone
from uuid import uuid4
from db import get_connection


def normalize_row(row):
    data = dict(row)
    data["needs_human"] = bool(data.get("needs_human"))
    return data


def create_log(question: str, result: dict):
    entry = {
        "id": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "intent": result.get("intent"),
        "order_number": result.get("order_number"),
        "order_status": result.get("order_status"),
        "decision": result.get("decision"),
        "answer": result.get("answer"),
        "needs_human": result.get("needs_human"),
        "escalation_reason": result.get("escalation_reason"),
    }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO decision_logs (
        id, timestamp, question, intent, order_number, order_status,
        decision, answer, needs_human, escalation_reason
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entry["id"],
        entry["timestamp"],
        entry["question"],
        entry["intent"],
        entry["order_number"],
        entry["order_status"],
        entry["decision"],
        entry["answer"],
        int(bool(entry["needs_human"])),
        entry["escalation_reason"],
    ))

    conn.commit()
    conn.close()

    return entry


def get_logs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM decision_logs ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    return [normalize_row(row) for row in rows]


def get_logs_by_order(order_number: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM decision_logs
    WHERE order_number = ?
    ORDER BY timestamp DESC
    """, (order_number,))
    rows = cursor.fetchall()
    conn.close()

    return [normalize_row(row) for row in rows]


def get_escalation_logs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM decision_logs
    WHERE needs_human = 1
    ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    return [normalize_row(row) for row in rows]
