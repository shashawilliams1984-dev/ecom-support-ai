import sqlite3

conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    user_message TEXT,
    ai_response TEXT
)
""")

conn.commit()

# Save function
def save_chat(session_id, user_message, ai_response):
    cursor.execute(
        "INSERT INTO conversations (session_id, user_message, ai_response) VALUES (?, ?, ?)",
        (session_id, user_message, ai_response)
    )
    conn.commit()
