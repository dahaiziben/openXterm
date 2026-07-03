#!/usr/bin/env python3
import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crypto import encrypt_password, decrypt_password
from db import init_db, add_connection, update_connection, delete_connection, get_connection, list_connections
from parser import parse_ssh_command, build_ssh_command


class ConnectionDialog:
    def __init__(self, parent, title="\u65b0\u5efa\u8fde\u63a5", conn=None):
        self.conn = conn
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("520x480")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        main_frame = ttk.Frame(self.dialog, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        row = 0

        ttk.Label(main_frame, text="\u8fde\u63a5\u540d\u79f0:").grid(row=row, column=0, sticky=tk.W, pady=3)
        self.name_var = tk.StringVar(value=conn["name"] if conn else "")
        ttk.Entry(main_frame, textvariable=self.name_var, width=40).grid(row=row, column=1, pady=3)
        row += 1

        parse_btn = ttk.Button(main_frame, text="\u4ece SSH \u547d\u4ee4\u89e3\u6790", command=self.parse_ssh)
        parse_btn.grid(row=row, column=0, columnspan=2, pady=5)
        row += 1

        ttk.Label(main_frame, text="\u4e3b\u673a / IP:").grid(row=row, column=0, sticky=tk.W, pady=3)
        self.host_var = tk.StringVar(value=conn["host"] if conn else "")
        ttk.Entry(main_frame, textvariable=self.host_var, width=40).grid(row=row, column=1, pady=3)
        row += 1

        ttk.Label(main_frame, text="\u7aef\u53e3:").grid(row=row, column=0, sticky=tk.W, pady=3)
        self.port_var = tk.StringVar(value=str(conn["port"]) if conn else "22")
        ttk.Entry(main_frame, textvariable=self.port_var, width=40).grid(row=row, column=1, pady=3)
        row += 1

        ttk.Label(main_frame, text="\u7528\u6237\u540d:").grid(row=row, column=0, sticky=tk.W, pady=3)
        self.user_var = tk.StringVar(value=conn["username"] if conn else "")
        ttk.Entry(main_frame, textvariable=self.user_var, width=40).grid(row=row, column=1, pady=3)
        row += 1

        ttk.Label(main_frame, text="\u5bc6\u7801:").grid(row=row, column=0, sticky=tk.W, pady=3)
        pwd_frame = ttk.Frame(main_frame)
        pwd_frame.grid(row=row, column=1, sticky=tk.W, pady=3)
        self.show_password = tk.BooleanVar(value=False)
        self.pwd_entry = ttk.Entry(pwd_frame, width=34, show="*")
        self.pwd_entry.pack(side=tk.LEFT)
        if conn and conn.get("password"):
            try:
                self.pwd_entry.insert(0, decrypt_password(conn["password"]))
            except Exception:
                self.pwd_entry.insert(0, "")
        self.eye_btn = ttk.Button(pwd_frame, text="\u25cf", width=3, command=self.toggle_password)
        self.eye_btn.pack(side=tk.LEFT, padx=2)
        row += 1

        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=10)
        row += 1

        ttk.Label(main_frame, text="\u8df3\u677f\u673a (\u53ef\u9009):").grid(row=row, column=0, sticky=tk.W, pady=3)
        self.jump_host_var = tk.StringVar(value=conn["jump_host"] if conn else "")
        ttk.Entry(main_frame, textvariable=self.jump_host_var, width=40).grid(row=row, column=1, pady=3)
        row += 1

        ttk.Label(main_frame, text="\u8df3\u677f\u7528\u6237:").grid(row=row, column=0, sticky=tk.W, pady=3)
        self.jump_user_var = tk.StringVar(value=conn["jump_user"] if conn else "")
        ttk.Entry(main_frame, textvariable=self.jump_user_var, width=40).grid(row=row, column=1, pady=3)
        row += 1

        ttk.Label(main_frame, text="\u8df3\u677f\u5bc6\u7801:").grid(row=row, column=0, sticky=tk.W, pady=3)
        jump_pwd_frame = ttk.Frame(main_frame)
        jump_pwd_frame.grid(row=row, column=1, sticky=tk.W, pady=3)
        self.jump_pwd_entry = ttk.Entry(jump_pwd_frame, width=34, show="*")
        self.jump_pwd_entry.pack(side=tk.LEFT)
        if conn and conn.get("jump_password"):
            try:
                self.jump_pwd_entry.insert(0, decrypt_password(conn["jump_password"]))
            except Exception:
                self.jump_pwd_entry.insert(0, "")
        self.jump_eye_btn = ttk.Button(jump_pwd_frame, text="\u25cf", width=3, command=self.toggle_jump_password)
        self.jump_eye_btn.pack(side=tk.LEFT, padx=2)
        row += 1

        ttk.Label(main_frame, text="\u989d\u5916\u53c2\u6570:").grid(row=row, column=0, sticky=tk.W, pady=3)
        self.extra_var = tk.StringVar(value=conn["extra_args"] if conn else "")
        ttk.Entry(main_frame, textvariable=self.extra_var, width=40).grid(row=row, column=1, pady=3)
        row += 1

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="\u786e\u5b9a", width=12, command=self.ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="\u53d6\u6d88", width=12, command=self.cancel).pack(side=tk.LEFT, padx=5)

        self.dialog.wait_window()
    def toggle_password(self):
        self.show_password.set(not self.show_password.get())
        self.pwd_entry.config(show="" if self.show_password.get() else "*")
        self.eye_btn.config(text="\u25cb" if self.show_password.get() else "\u25cf")

    def toggle_jump_password(self):
        current = self.jump_pwd_entry.cget("show")
        self.jump_pwd_entry.config(show="" if current == "*" else "*")
        self.jump_eye_btn.config(text="\u25cb" if current == "*" else "\u25cf")

    def parse_ssh(self):
        dialog = tk.Toplevel(self.dialog)
        dialog.title("\u7c98\u8d34 SSH \u547d\u4ee4")
        dialog.geometry("500x150")
        dialog.transient(self.dialog)
        dialog.grab_set()
        ttk.Label(dialog, text="\u8bf7\u7c98\u8d34 SSH \u547d\u4ee4\u5b57\u7b26\u4e32:").pack(pady=8)
        cmd_text = tk.Text(dialog, height=3, width=60)
        cmd_text.pack(padx=10, fill=tk.X)

        def do_parse():
            cmd = cmd_text.get("1.0", tk.END).strip()
            r = parse_ssh_command(cmd)
            if r:
                self.host_var.set(r["host"])
                self.port_var.set(str(r["port"]))
                self.user_var.set(r["username"])
                self.jump_host_var.set(r["jump_host"])
                self.jump_user_var.set(r["jump_user"])
                self.extra_var.set(r["extra_args"])
                dialog.destroy()
            else:
                messagebox.showerror("\u9519\u8bef", "\u65e0\u6cd5\u89e3\u6790\u8be5 SSH \u547d\u4ee4", parent=dialog)

        ttk.Button(dialog, text="\u89e3\u6790", command=do_parse).pack(pady=8)
        dialog.wait_window()

    def collect_data(self):
        data = {
            "name": self.name_var.get().strip(),
            "host": self.host_var.get().strip(),
            "username": self.user_var.get().strip(),
        }
        try:
            data["port"] = int(self.port_var.get().strip() or "22")
        except ValueError:
            data["port"] = 22
        pwd = self.pwd_entry.get()
        if pwd:
            data["password"] = encrypt_password(pwd)
        data["jump_host"] = self.jump_host_var.get().strip()
        data["jump_user"] = self.jump_user_var.get().strip()
        jpwd = self.jump_pwd_entry.get()
        if jpwd:
            data["jump_password"] = encrypt_password(jpwd)
        data["extra_args"] = self.extra_var.get().strip()
        return data

    def ok(self):
        data = self.collect_data()
        if not data["host"] or not data["username"]:
            messagebox.showerror("\u9519\u8bef", "\u4e3b\u673a\u548c\u7528\u6237\u540d\u4e3a\u5fc5\u586b\u5b57\u6bb5", parent=self.dialog)
            return
        self.result = data
        self.dialog.destroy()

    def cancel(self):
        self.dialog.destroy()

class OpenXtermApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenXterm - SSH \u8fde\u63a5\u7ba1\u7406\u5668")
        self.root.geometry("750x520")
        self.root.minsize(600, 400)
        init_db()
        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(toolbar, text="+ \u65b0\u5efa\u8fde\u63a5", command=self.add_connection).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="\u270e \u5237\u65b0", command=self.refresh_list).pack(side=tk.LEFT, padx=2)

        columns = ("id", "name", "host", "port", "username", "jump")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="\u8fde\u63a5\u540d\u79f0")
        self.tree.heading("host", text="\u4e3b\u673a")
        self.tree.heading("port", text="\u7aef\u53e3")
        self.tree.heading("username", text="\u7528\u6237\u540d")
        self.tree.heading("jump", text="\u8df3\u677f\u673a")
        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("name", width=120)
        self.tree.column("host", width=140)
        self.tree.column("port", width=60, anchor=tk.CENTER)
        self.tree.column("username", width=100)
        self.tree.column("jump", width=140)

        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(action_frame, text="\u25b6 \u8fde\u63a5", width=15, command=self.connect_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="\u270f \u7f16\u8f91", width=10, command=self.edit_connection).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="\u2718 \u5220\u9664", width=10, command=self.delete_connection).pack(side=tk.LEFT, padx=2)

        self.status_var = tk.StringVar(value="\u5c31\u7eea")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.tree.bind("<Double-1>", lambda e: self.connect_selected())

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in list_connections():
            jump_display = c.get("jump_host", "") or ""
            if jump_display and c.get("jump_user"):
                jump_display = f"{c['jump_user']}@{jump_display}"
            self.tree.insert("", tk.END, values=(
                c["id"], c["name"] or c["host"], c["host"], c["port"],
                c["username"], jump_display,
            ))
        self.status_var.set(f"\u5171 {len(list_connections())} \u4e2a\u8fde\u63a5")

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("\u63d0\u793a", "\u8bf7\u5148\u9009\u62e9\u4e00\u4e2a\u8fde\u63a5")
            return None
        return int(self.tree.item(sel[0], "values")[0])

    def add_connection(self):
        dlg = ConnectionDialog(self.root)
        if dlg.result:
            add_connection(dlg.result)
            self.refresh_list()

    def edit_connection(self):
        cid = self.get_selected_id()
        if cid is None:
            return
        conn = get_connection(cid)
        dlg = ConnectionDialog(self.root, title="\u7f16\u8f91\u8fde\u63a5", conn=conn)
        if dlg.result:
            update_connection(cid, dlg.result)
            self.refresh_list()

    def delete_connection(self):
        cid = self.get_selected_id()
        if cid is None:
            return
        if messagebox.askyesno("\u786e\u8ba4", "\u786e\u5b9a\u5220\u9664\u8be5\u8fde\u63a5\uff1f", parent=self.root):
            delete_connection(cid)
            self.refresh_list()

    def connect_selected(self):
        cid = self.get_selected_id()
        if cid is None:
            return
        conn = get_connection(cid)
        threading.Thread(target=self.do_connect, args=(conn,), daemon=True).start()

    def do_connect(self, conn):
        try:
            password = ""
            if conn.get("password"):
                try:
                    password = decrypt_password(conn["password"])
                except Exception:
                    password = ""

            ssh_cmd = build_ssh_command(conn)
            self.status_var.set(f"\u6b63\u5728\u8fde\u63a5 {conn['host']}...")

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            if password:
                proc = subprocess.Popen(
                    ssh_cmd,
                    shell=True,
                    stdin=subprocess.PIPE if password else None,
                    startupinfo=startupinfo,
                )
                if password:
                    import time
                    time.sleep(1)
                    try:
                        proc.stdin.write(f"{password}\n".encode())
                        proc.stdin.flush()
                    except:
                        pass
            else:
                subprocess.Popen(ssh_cmd, shell=True, startupinfo=startupinfo)

            self.status_var.set(f"\u5df2\u542f\u52a8 SSH: {conn['host']}")
        except Exception as e:
            self.status_var.set(f"\u9519\u8bef: {e}")
            messagebox.showerror("\u9519\u8bef", str(e), parent=self.root)


def main():
    root = tk.Tk()
    app = OpenXtermApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
