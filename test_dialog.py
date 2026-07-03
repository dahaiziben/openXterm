import sys, os
sys.path.insert(0, r"E:\code\python\openXterm\dist\OpenXterm.pyz")

# Clean old key
key_dir = os.path.join(os.environ.get("TEMP", os.environ.get("TMP", os.path.expanduser("~"))), "OpenXterm")
key_file = os.path.join(key_dir, ".machine_key")
if os.path.exists(key_file):
    os.remove(key_file)

import tkinter as tk
import main
from db import init_db
init_db()

root = tk.Tk()
app = main.OpenXtermApp(root)

# Simulate clicking "确定" in a new connection dialog
dlg = main.ConnectionDialog(root)
print("Dialog created")

# Fill in required fields
dlg.host_var.set("192.168.1.1")
dlg.user_var.set("admin")
dlg.pwd_entry.delete(0, "end")
dlg.pwd_entry.insert(0, "mypassword")

# Click OK - this calls encrypt_password internally
dlg.ok()
r = dlg.result
print("Result:", r is not None)
print("Host:", r.get("host"))
print("Has encrypted password:", bool(r.get("password")))

root.destroy()
print("SUCCESS: Connection dialog works without error!")
