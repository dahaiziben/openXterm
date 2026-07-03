import base64
import os
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


SALT = b"openxterm_salt_v1"
ITERATIONS = 200000

# Store machine key alongside the DB in user temp directory
_KEY_DIR = os.path.join(os.environ.get("TEMP", os.environ.get("TMP", os.path.expanduser("~"))), "OpenXterm")
os.makedirs(_KEY_DIR, exist_ok=True)
KEY_FILE = os.path.join(_KEY_DIR, ".machine_key")


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
