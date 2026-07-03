import os
path = "E:/code/python/openXterm/src/db.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = '''if getattr(sys, "frozen", False) or os.path.dirname(os.path.abspath(__file__)).endswith(".pyz"):
    DB_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "OpenXterm")
else:
    DB_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "connections.db")'''

new = '''DB_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    os.makedirs(DB_DIR, exist_ok=True)
except PermissionError:
    DB_DIR = os.path.expanduser("~")
DB_PATH = os.path.join(DB_DIR, "connections.db")'''

content = content.replace(old, new)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK")