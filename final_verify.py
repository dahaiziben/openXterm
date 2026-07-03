import sys, os
sys.path.insert(0, r"E:\code\python\openXterm\dist\OpenXterm.pyz")

import os
key_dir = os.path.join(os.environ.get("TEMP", os.environ.get("TMP", os.path.expanduser("~"))), "OpenXterm")
key_file = os.path.join(key_dir, ".machine_key")
if os.path.exists(key_file):
    os.remove(key_file)

from crypto import encrypt_password, decrypt_password
enc = encrypt_password("hello123")
dec = decrypt_password(enc)
assert dec == "hello123"
print("1. Crypto: PASS")

from db import init_db, add_connection, add_port_forward, get_port_forwards, list_connections, delete_connection
init_db()
cid = add_connection({"name": "Test", "host": "10.0.0.1", "username": "root"})
fid = add_port_forward({"connection_id": cid, "name": "web", "forward_type": "L", "listen_port": 8888, "dest_host": "localhost", "dest_port": 80})
fws = get_port_forwards(cid)
assert len(fws) == 1
delete_connection(cid)
print("2. DB: PASS")

import main as m
assert hasattr(m, "ConnectionDialog")
assert hasattr(m, "OpenXtermApp")
assert hasattr(m, "PortForwardManager")
print("3. Main classes: PASS")

assert "#ffffff" == m.THEME.get("bg", "")
assert "主机" in m.CN.get("host", "")
print("4. Theme & CN strings: PASS")

import inspect
src = inspect.getsource(m.PortForwardManager.edit_forward)
assert "refresh_forwards" in src
assert "PortForwardDialog" in src
print("5. edit_forward fix: PASS")

assert "Temp" in os.path.normpath(m.crypto.KEY_FILE)
print("6. KEY_FILE path: PASS")

print()
print("ALL VERIFICATIONS PASSED")
