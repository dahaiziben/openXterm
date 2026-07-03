import os, sys
sys.stdout.reconfigure(encoding="utf-8")

SRC = r"E:\code\python\openXterm\src"

files = {}

# crypto.py
files["crypto.py"] = r"""import base64
import os
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


SALT = b"openxterm_salt_v1"
ITERATIONS = 200000
KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".machine_key")


def _get_or_create_key() -> bytes:
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return f.read().strip().encode()
    master = secrets.token_hex(32)
    with open(KEY_FILE, "w") as f:
        f.write(master)
    return master.encode()


def _derive_key(master_password: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))


def encrypt_password(plain_password: str) -> str:
    key = _derive_key(_get_or_create_key().decode())
    fernet = Fernet(key)
    return fernet.encrypt(plain_password.encode()).decode()


def decrypt_password(encrypted_password: str) -> str:
    key = _derive_key(_get_or_create_key().decode())
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password.encode()).decode()
"""

# db.py
files["db.py"] = r"""import sqlite3
import os
from datetime import datetime

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "connections.db")


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
"""

# parser.py
files["parser.py"] = r'''import re
from typing import Optional


def parse_ssh_command(cmd: str) -> Optional[dict]:
    """
    Parse an SSH command string like:
      ssh -L 3306:127.0.0.1:3306 user@host -J jump@jump_host
      ssh -L 9099:127.0.0.1:9090 hsadmin@172.16.242.2 -J changhy@47.98.38.160
    """
    cmd = cmd.strip()
    if not cmd.startswith("ssh"):
        return None

    rest = cmd[3:].strip()
    result = {
        "host": "",
        "port": 22,
        "username": "",
        "password": "",
        "jump_host": "",
        "jump_port": 22,
        "jump_user": "",
        "jump_password": "",
        "extra_args": "",
    }

    extra_parts = []
    tokens = rest.split()
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in ("-L", "-R", "-D"):
            extra_parts.append(t)
            i += 1
            if i < len(tokens):
                extra_parts.append(tokens[i])
            i += 1
        elif t == "-J":
            i += 1
            if i < len(tokens):
                jump_part = tokens[i]
                if "@" in jump_part:
                    j_user, j_host = jump_part.rsplit("@", 1)
                    result["jump_user"] = j_user
                    if ":" in j_host:
                        j_host, j_port = j_host.rsplit(":", 1)
                        try:
                            result["jump_port"] = int(j_port)
                        except ValueError:
                            pass
                    result["jump_host"] = j_host
                else:
                    result["jump_host"] = jump_part
                extra_parts.extend(["-J", tokens[i]])
            i += 1
        elif t.startswith("-") and len(t) > 1:
            extra_parts.append(t)
            i += 1
            if i < len(tokens) and not tokens[i].startswith("-"):
                extra_parts.append(tokens[i])
                i += 1
        else:
            if "@" in t:
                result["username"], host_part = t.rsplit("@", 1)
                if ":" in host_part:
                    host_part, port_str = host_part.rsplit(":", 1)
                    try:
                        result["port"] = int(port_str)
                    except ValueError:
                        pass
                result["host"] = host_part
            else:
                if ":" in t:
                    t, port_str = t.rsplit(":", 1)
                    try:
                        result["port"] = int(port_str)
                    except ValueError:
                        pass
                result["host"] = t
            i += 1

    if extra_parts:
        result["extra_args"] = " ".join(extra_parts)

    return result if result["host"] else None


def build_ssh_command(conn: dict) -> str:
    """Build SSH command string from connection dict."""
    parts = ["ssh"]
    extra = conn.get("extra_args", "") or ""
    if extra:
        parts.append(extra)

    user = conn.get("username", "")
    host = conn.get("host", "")
    port = conn.get("port", 22)
    user_at = f"{user}@" if user else ""
    host_part = f"{user_at}{host}"
    if port != 22:
        host_part = f"{user_at}{host}:{port}"

    jump_host = conn.get("jump_host", "") or ""
    if jump_host:
        jump_user = conn.get("jump_user", "") or ""
        jump_port = conn.get("jump_port", 22)
        j_user_at = f"{jump_user}@" if jump_user else ""
        j_part = f"{j_user_at}{jump_host}"
        if jump_port != 22:
            j_part = f"{j_user_at}{jump_host}:{jump_port}"
        parts.append(f"-J {j_part}")

    parts.append(host_part)
    return " ".join(parts)
'''

for fname, content in files.items():
    path = os.path.join(SRC, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.lstrip("\n"))
    print(f"Written {fname} ({len(content)} chars)")

print("All source files generated successfully")
