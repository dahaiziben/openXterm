import os
path = "E:/code/python/openXterm/src/db.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "import sqlite3, sys\nimport os"
new = "import sqlite3, sys, os"

old2 = '''DB_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    os.makedirs(DB_DIR, exist_ok=True)
except PermissionError:
    DB_DIR = os.path.expanduser("~")
DB_PATH = os.path.join(DB_DIR, "connections.db")'''

new2 = '''_file_path = os.path.abspath(__file__)
# Check if running from inside a zipapp/egg
if ".pyz" in _file_path or ".zip" in _file_path or getattr(sys, "frozen", False):
    DB_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "OpenXterm")
else:
    DB_DIR = os.path.dirname(_file_path)
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "connections.db")'''

content = content.replace(old, new)
content = content.replace(old2, new2)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK")