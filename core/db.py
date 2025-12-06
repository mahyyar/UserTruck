import sqlite3

DB_PATH = "data/database.db"


def connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        numeric_id TEXT,
        panel_name TEXT,
        expire_day INTEGER,
        last_extended TEXT,
        history TEXT,
        note TEXT
    );
    """)

    conn.commit()
    conn.close()


def optimize_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("CREATE INDEX IF NOT EXISTS idx_numeric_id ON users(numeric_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_panel_name ON users(panel_name)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_expire_day ON users(expire_day)")

    conn.commit()
    conn.close()
