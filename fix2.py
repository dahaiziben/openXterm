import re

path = "E:/code/python/openXterm/src/main.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "    def do_connect(self, conn):"
end_marker = "class PortForwardManager:"

new_do_connect = """    def do_connect(self, conn):
        try:
            password = \"\"\"
            if conn.get(\"password\"):
                try:
                    password = decrypt_password(conn[\"password\"])
                except Exception:
                    password = \"\"\"

            jump_password = \"\"\"
            if conn.get(\"jump_password\"):
                try:
                    jump_password = decrypt_password(conn[\"jump_password\"])
                except Exception:
                    jump_password = \"\"\"

            host = conn.get(\"host\", \"\")
            port = int(conn.get(\"port\", 22))
            username = conn.get(\"username\", \"\")
            jump_host = conn.get(\"jump_host\", \"\") or \"\"
            jump_port = int(conn.get(\"jump_port\", 22))
            jump_user = conn.get(\"jump_user\", \"\") or \"\"
            extra_args = conn.get(\"extra_args\", \"\") or \"\"

            cid = conn.get(\"id\")
            forwards = get_port_forwards(cid) if cid else []
            is_port_forward = bool(forwards) or \"-L\" in extra_args or \"-R\" in extra_args or \"-D\" in extra_args

            def worker():
                import paramiko
                import re
                import time

                try:
                    c = None
                    jc = None
                    if jump_host and jump_user:
                        jc = paramiko.SSHClient()
                        jc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        jc.connect(jump_host, port=jump_port, username=jump_user,
                                   password=jump_password if jump_password else None,
                                   look_for_keys=False, allow_agent=False, timeout=10)
                        sock = jc.get_transport().open_channel(
                            \"direct-tcpip\", (host, port), (jump_host, 0))
                        c = paramiko.SSHClient()
                        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        c.connect(host, port=port, username=username,
                                   password=password if password else None,
                                   sock=sock, look_for_keys=False, allow_agent=False, timeout=10)
                    else:
                        c = paramiko.SSHClient()
                        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        c.connect(host, port=port, username=username,
                                   password=password if password else None,
                                   look_for_keys=False, allow_agent=False, timeout=10)

                    self.root.after(0, lambda: self.status_var.set(f\"{CN['connected']}: {host}\"))
                    self.root.after(0, lambda: self.connect_btn.config(state=tk.NORMAL))

                    if is_port_forward:
                        trans = c.get_transport()
                        tunnel_msgs = []
                        for fwd in forwards:
                            ft = fwd[\"forward_type\"]
                            lp = fwd[\"listen_port\"]
                            dh = fwd[\"dest_host\"]
                            dp = fwd[\"dest_port\"]
                            lh = fwd.get(\"listen_host\", \"127.0.0.1\") or \"127.0.0.1\"
                            if ft == \"L\":
                                trans.request_port_forward(\"\", lp, (dh, dp))
                                tunnel_msgs.append(f\"{CN['local']} {lh}:{lp} -> {dh}:{dp}\")
                            elif ft == \"R\":
                                trans.request_port_forward(\"remote\", lp, (dh, dp))
                                tunnel_msgs.append(f\"{CN['remote']} *:{lp} -> {dh}:{dp}\")
                            elif ft == \"D\":
                                pass

                        for m in re.finditer(r\"-L\\s+(\\d+):([^:]+):(\\d+)\", extra_args):
                            lp = int(m.group(1))
                            dh = m.group(2)
                            dp = int(m.group(3))
                            trans.request_port_forward(\"\", lp, (dh, dp))
                            tunnel_msgs.append(f\"{CN['local']} localhost:{lp} -> {dh}:{dp}\")

                        if tunnel_msgs:
                            msg = \"\\n\".join(tunnel_msgs)
                            self.root.after(0, lambda m=msg: messagebox.showinfo(CN[\"tunnel_established\"], m, parent=self.root))
                            self.root.after(0, lambda: self.status_var.set(CN[\"tunnel_active\"].format(host)))

                        self.root.after(0, lambda: self.active_tunnels.__setitem__(cid, {
                            \"client\": c,
                            \"jump_client\": jc,
                            \"transport\": trans,
                            \"host\": host,
                        }))

                        try:
                            while True:
                                time.sleep(30)
                                if not trans.is_active():
                                    break
                        except Exception:
                            pass
                    else:
                        ssh_cmd = build_ssh_command(conn)
                        bat_path = os.path.join(os.environ.get(\"TEMP\", \"C:\\\\Temp\"), \"ox_ssh.bat\")
                        with open(bat_path, \"w\") as f:
                            f.write(\"@echo off\\n\")
                            f.write(\"title OpenXterm - \" + host + \"\\n\")
                            f.write(ssh_cmd + \"\\n\")
                            f.write(\"echo.\\n\")
                            f.write(\"pause\\n\")
                        subprocess.Popen(\"start cmd /k \\\"\" + bat_path + \"\\\"\", shell=True)
                        self.root.after(0, lambda: self.connect_btn.config(state=tk.NORMAL))

                except Exception as e:
                    err_str = str(e)
                    self.root.after(0, lambda e=err_str: self._show_error(e))
                    self.root.after(0, lambda: self.status_var.set(f\"{CN['error']}: {err_str}\"))
                    self.root.after(0, lambda: self.connect_btn.config(state=tk.NORMAL))

            t = threading.Thread(target=worker, daemon=True)
            t.start()

        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f\"{CN['error']}: {e}\"))
            self.root.after(0, lambda: self.connect_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda e=str(e): self._show_error(e))

    def _show_error(self, msg):
        try:
            messagebox.showerror(CN[\"connect_fail\"], msg)
        except Exception:
            pass

"""

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx + 1)

if start_idx >= 0 and end_idx > start_idx:
    content = content[:start_idx] + new_do_connect + "\n\n" + content[end_idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK")
else:
    print("not found")