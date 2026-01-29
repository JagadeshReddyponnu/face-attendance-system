import sqlite3
from datetime import datetime, date

DB_NAME = "attendance.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS attendance (name TEXT, time TEXT, type TEXT)"
    )
    conn.commit()
    conn.close()

def mark_attendance(name, entry_type):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO attendance VALUES (?, ?, ?)",
        (name, datetime.now().isoformat(), entry_type)
    )
    conn.commit()
    conn.close()

def last_entry(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT time, type FROM attendance WHERE name=? ORDER BY time DESC LIMIT 1",
        (name,)
    )
    row = cur.fetchone()
    conn.close()
    return row

def last_entry_today(name):
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT type FROM attendance WHERE name=? AND time LIKE ? ORDER BY time DESC LIMIT 1",
        (name, f"{today}%")
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None