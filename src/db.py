import sqlite3, sys, os
from datetime import datetime

# Store db in user AppData or same directory as script
# Store database in user temp directory
DB_DIR = os.path.join(os.environ.get("TEMP", os.environ.get("TMP", os.path.expanduser("~"))), "OpenXterm")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "connections.db")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS port_forwards (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            connection_id   INTEGER NOT NULL,
            name            TEXT,
            forward_type    TEXT NOT NULL DEFAULT "L",
            listen_port     INTEGER NOT NULL,
            dest_host       TEXT NOT NULL DEFAULT "localhost",
            dest_port       INTEGER NOT NULL,
            listen_host     TEXT DEFAULT "127.0.0.1",
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (connection_id) REFERENCES connections(id) ON DELETE CASCADE
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
    conn.execute("DELETE FROM port_forwards WHERE connection_id = ?", (conn_id,))
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


def add_port_forward(data: dict) -> int:
    conn = get_db()
    now = datetime.now().isoformat()
    data.setdefault("created_at", now)
    cols = ", ".join(data.keys())
    placeholders = ", ".join("?" * len(data))
    cursor = conn.execute(f"INSERT INTO port_forwards ({cols}) VALUES ({placeholders})", list(data.values()))
    conn.commit()
    return cursor.lastrowid


def update_port_forward(fwd_id: int, data: dict):
    conn = get_db()
    sets = ", ".join(f"{k} = ?" for k in data.keys())
    vals = list(data.values()) + [fwd_id]
    conn.execute(f"UPDATE port_forwards SET {sets} WHERE id = ?", vals)
    conn.commit()


def delete_port_forward(fwd_id: int):
    conn = get_db()
    conn.execute("DELETE FROM port_forwards WHERE id = ?", (fwd_id,))
    conn.commit()


def get_port_forwards(connection_id: int) -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT * FROM port_forwards WHERE connection_id = ? ORDER BY id", (connection_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_port_forwards_by_connection(connection_id: int):
    conn = get_db()
    conn.execute("DELETE FROM port_forwards WHERE connection_id = ?", (connection_id,))
    conn.commit()
