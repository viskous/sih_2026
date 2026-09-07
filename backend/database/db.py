import sqlite3
import json
from datetime import datetime

DB_PATH = "data/app.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            conversation_text TEXT,
            profile_json TEXT,
            recommendations_json TEXT,
            region TEXT,
            employment_preference TEXT,
            top_trade TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_conversation(conversation_text, profile, recommendations):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    top_trade = recommendations[0]["trade"] if recommendations else None

    cursor.execute("""
        INSERT INTO conversations 
        (timestamp, conversation_text, profile_json, recommendations_json, region, employment_preference, top_trade)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        conversation_text,
        json.dumps(profile),
        json.dumps(recommendations),
        profile.get("region"),
        profile.get("employment_preference"),
        top_trade
    ))
    conn.commit()
    conn.close()