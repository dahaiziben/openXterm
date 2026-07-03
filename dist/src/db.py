import sqlite3
import os
from datetime import datetime

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, 'connections.db')


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS connections (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT,
            host        TEXT NOT NULL,
            port        INTEGER DEFAULT 22,
            username    TEXT NOT NULL,
            password    TEXT,
            jump_host   TEXT,
            jump_port   INTEGER DEFAULT 22,
            jump_user   TEXT,
            jump_password TEXT,
            extra_args  TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_connection(conn_data: dict) -> int:
    conn = get_db()
    now = datetime.now().isoformat()
    conn_data.setdefault("created_at", now)
    conn_data.setdefault("updated_at", now)
    conn_data.setdefault("port", 22)
    conn_data.setdefault("jump_port", 22)
    cols = ", ".join(conn_data.keys())
    placeholders = ", ".join("?" * len(conn_data))
    cursor = conn.execute(
        f"INSERT INTO connections ({cols}) VALUES ({placeholders})",
        list(conn_data.values()),
    )
    conn.commit()
    return cursor.lastrowid


def update_connection(conn_id: int, conn_data: dict):
    conn = get_db()
    conn_data["updated_at"] = datetime.now().isoformat()
    sets = ", ".join(f"{k} = ?" for k in conn_data.keys())
    vals = list(conn_data.values()) + [conn_id]
    conn.execute(f"UPDATE connections SET {sets} WHERE id = ?", vals)
    conn.commit()


def delete_connection(conn_id: int):
    conn = get_db()
    conn.execute("DELETE FROM connections WHERE id = ?", (conn_id,))
    conn.commit()


def get_connection(conn_id: int) -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT * FROM connections WHERE id = ?", (conn_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def list_connections() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT * FROM connections ORDER BY updated_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
