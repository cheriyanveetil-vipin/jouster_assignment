import sqlite3
from typing import List, Dict

DB_FILE = "analysis.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
            create table if not exists analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                summary TEXT,
                title TEXT,
                topics TEXT,
                sentiment TEXT,
                keywords TEXT
        )"""
    )
    conn.commit()
    conn.close()

def insert_analysis(summary: str, title: str, topics: List[str], sentiment: str, keywords: List[str]):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO analyses (summary, title, topics, sentiment, keywords) VALUES (?,?,?,?,?)",
        (summary, title, topics, sentiment, keywords),
    )
    conn.commit()
    conn.close()

def search_analysis(topic: str) -> List[Dict]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT summary, title, topics, sentiment, keywords FROM analyses WHERE topics LIKE ? OR keywords LIKE ?",
        (f"%{topic}%", f"%{topic}%"),
    )
    rows = c.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "summary": row[0],
            "title": row[1],
            "topics": row[2].split(","),
            "sentiment": row[3],
            "keywords": row[4].split(","),
        })
    return results
