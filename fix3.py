path = "E:/code/python/openXterm/src/main.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Fix refresh_forwards method
lines[626] = "            self.tree.delete(item)\n"
lines[627] = "        forwards = get_port_forwards(self.conn_id)\n"
lines[628] = "        for f in forwards:\n"
lines[629] = "            ftype = {\"L\": CN[\"local\"], \"R\": CN[\"remote\"], \"D\": CN[\"dynamic\"]}.get(f[\"forward_type\"], f[\"forward_type\"])\n"
lines[630] = "            listen = f\"{f.get(\"listen_host\", \"127.0.0.1\")}:{f[\"listen_port\"]}\"\n"
lines[631] = "            dest = f\"{f[\"dest_host\"]}:{f[\"dest_port\"]}\" if f[\"forward_type\"] != \"D\" else CN[\"socks\"]\n"
lines[632] = "            self.tree.insert(\"\", tk.END, values=(f[\"id\"], f[\"name\"] or \"-\", ftype, listen, dest))\n"

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)
print("OK")