import re
from typing import Optional


def parse_ssh_command(cmd: str) -> Optional[dict]:
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
                pass  # -J already parsed above
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
