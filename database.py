import sqlite3
import json


def init_db(path="earnings.db"):
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            quarter TEXT NOT NULL,
            section TEXT NOT NULL,
            sentiment REAL,
            confidence REAL,
            hedging INTEGER,
            tone TEXT,
            raw_json TEXT,
            UNIQUE(ticker, quarter, section)
        )
    """)
    conn.commit()
    return conn


def already_done(conn, ticker, quarter, section):
    """True if we've already analyzed this exact section."""
    cur = conn.execute(
        "SELECT 1 FROM analyses WHERE ticker=? AND quarter=? AND section=?",
        (ticker, quarter, section),
    )
    return cur.fetchone() is not None


def save(conn, ticker, quarter, section, result):
    conn.execute("""
        INSERT OR REPLACE INTO analyses
            (ticker, quarter, section, sentiment, confidence, hedging,
             tone, raw_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticker,
        quarter,
        section,
        result.get("sentiment_score"),
        result.get("confidence_score"),
        result.get("hedging_count"),
        result.get("forward_looking_tone"),
        json.dumps(result),
    ))
    conn.commit()