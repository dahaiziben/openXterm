import os

path = "E:/code/python/openXterm/src/db.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the DB_DIR/DB_PATH logic
old = '''DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "connections.db")'''

new = '''# Store db in user AppData or same directory as script
if getattr(sys, "frozen", False) or os.path.dirname(os.path.abspath(__file__)).endswith(".pyz"):
    DB_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "OpenXterm")
else:
    DB_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "connections.db")'''

content = content.replace(old, new)

# Also need to import sys at top
if "import sys" not in content.split("\n")[0:5]:
    content = content.replace("import sqlite3", "import sqlite3, sys")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK")