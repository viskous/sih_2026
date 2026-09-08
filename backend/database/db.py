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

def get_dashboard_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # total beneficiaries profiled
    cursor.execute("SELECT COUNT(*) FROM conversations")
    total = cursor.fetchone()[0]

    # count by top trade
    cursor.execute("""
        SELECT top_trade, COUNT(*) 
        FROM conversations 
        WHERE top_trade IS NOT NULL
        GROUP BY top_trade
        ORDER BY COUNT(*) DESC
    """)
    trade_counts = cursor.fetchall()

    # count by region
    cursor.execute("""
        SELECT region, COUNT(*) 
        FROM conversations 
        WHERE region IS NOT NULL
        GROUP BY region
        ORDER BY COUNT(*) DESC
    """)
    region_counts = cursor.fetchall()

    # self vs wage split
    cursor.execute("""
        SELECT employment_preference, COUNT(*) 
        FROM conversations 
        WHERE employment_preference IS NOT NULL
        GROUP BY employment_preference
    """)
    employment_split = cursor.fetchall()

    conn.close()

    return {
        "total_beneficiaries": total,
        "trade_demand": [{"trade": t, "count": c} for t, c in trade_counts],
        "region_demand": [{"region": r, "count": c} for r, c in region_counts],
        "employment_split": [{"type": e, "count": c} for e, c in employment_split]
    }