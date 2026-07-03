import os

# Read the current main.py
with open(r"E:\code\python\openXterm\src\main.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1) Replace the entire CN dict with proper UTF-8
old_cn_start = content.find("CN = {")
depth = 0
end_pos = old_cn_start
for i in range(old_cn_start, len(content)):
    if content[i] == "{":
        depth += 1
    elif content[i] == "}":
        depth -= 1
        if depth == 0:
            end_pos = i + 1
            break

cn_lines = []
cn_lines.append("CN = {")
pairs = [
    ('port_forward', '端口转发'),
    ('forward_name', '转发名称'),
    ('forward_type', '转发类型'),
    ('listen_port', '监听端口'),
    ('dest_host', '目标主机'),
    ('dest_port', '目标端口'),
    ('new_conn', '新建连接'),
    ('edit_conn', '编辑连接'),
    ('connection_mgr', 'OpenXterm - SSH 连接管理器'),
    ('conn_name', '连接名称:'),
    ('host', '主机 / IP:'),
    ('port', '端口:'),
    ('username', '用户名:'),
    ('password', '密码:'),
    ('jump_host', '跳板机(可选):'),
    ('jump_user', '跳板用户:'),
    ('jump_password', '跳板密码:'),
    ('extra_args', '额外参数:'),
    ('add_conn', '+ 新建连接'),
    ('refresh', '刷新'),
    ('connect', '连接'),
    ('edit', '编辑'),
    ('delete', '删除'),
    ('port_forward_mgr', '端口转发'),
    ('confirm_delete', '确认删除?'),
    ('select_first', '请先选择一个连接'),
    ('required', '主机和用户名为必填字段'),
    ('parse_ssh', '从SSH命令解析'),
    ('ssh_from_cmd', '从SSH命令解析'),
    ('paste_ssh', '请粘贴 SSH 命令字符串:'),
    ('parse', '解析'),
    ('parse_fail', '无法解析该 SSH 命令'),
    ('cancel', '取消'),
    ('ok', '确定'),
    ('connecting', '正在连接'),
    ('connected', '已连接'),
    ('error', '错误'),
    ('connect_fail', '连接失败'),
    ('tunnel_established', '隧道已建立'),
    ('local', '本地'),
    ('remote', '远程'),
    ('dynamic', '动态'),
    ('socks', 'SOCKS'),
    ('add_forward_btn', '+ 添加转发'),
    ('onekey_connect', '一键连接+转发'),
    ('forward_mgr_title', '端口转发'),
    ('conn_mgr_tab', '  连接管理  '),
    ('select_forward_first', '请先选择一个转发规则'),
    ('confirm_del_forward', '确认删除该转发规则?'),
    ('port_must_be_num', '端口必须是数字'),
    ('edit_forward', '编辑转发'),
    ('del_forward', '删除转发'),
    ('ready', '就绪'),
    ('total_conns', '共 {} 个连接'),
    ('conn_id', 'ID'),
    ('conn_name_col', '连接名称'),
    ('host_col', '主机'),
    ('port_col', '端口'),
    ('user_col', '用户名'),
    ('jump_col', '跳板机'),
    ('confirm_del_conn', '确认删除该连接?'),
    ('forward_name_col', '名称'),
    ('forward_type_col', '类型'),
    ('forward_listen_col', '监听'),
    ('forward_dest_col', '目标'),
    ('tunnel_active', '隧道活跃: {}'),
]
for k, v in pairs:
    cn_lines.append(f'    "{k}": "{v}",')
cn_lines.append("}")
new_cn = "\n".join(cn_lines)

content = content[:old_cn_start] + new_cn + content[end_pos:]

# 2) Fix PortForwardManager.edit_forward method
old_edit = ('''    def edit_forward(self):
        fid = self.get_selected_fwd()
        if fid is None:
            return
        fwd = next((f for f in forwards if f["id"] == fid), None)
        if not fwd:
            return
        if dlg.result:
            update_port_forward(fid, dlg.result)''')

new_edit = ('''    def edit_forward(self):
        fid = self.get_selected_fwd()
        if fid is None:
            return
        forwards = get_port_forwards(self.conn_id)
        fwd = next((f for f in forwards if f["id"] == fid), None)
        if not fwd:
            return
        dlg = PortForwardDialog(self.dialog, self.conn_id, title=CN["edit_forward"], fwd=fwd)
        if dlg.result:
            update_port_forward(fid, dlg.result)
            self.refresh_forwards()''')

if old_edit in content:
    content = content.replace(old_edit, new_edit)
    print("Fixed edit_forward method")
else:
    print("edit_forward pattern not found")

# 3) Add missing blank line
old_rf = '''            self.tree.insert("", tk.END, values=(f["id"], f["name"] or "-", ftype, listen, dest))
    def get_selected_fwd(self):'''
new_rf = '''            self.tree.insert("", tk.END, values=(f["id"], f["name"] or "-", ftype, listen, dest))

    def get_selected_fwd(self):'''
content = content.replace(old_rf, new_rf)

# 4) Fix ForwardManager.add_forward - missing refresh
old_af = '''    def add_forward(self):
        dlg = PortForwardDialog(self.dialog, self.conn_id)
        if dlg.result:
            add_port_forward(dlg.result)'''
new_af = '''    def add_forward(self):
        dlg = PortForwardDialog(self.dialog, self.conn_id)
        if dlg.result:
            add_port_forward(dlg.result)
            self.refresh_forwards()'''
content = content.replace(old_af, new_af)

# 5) Fix delete_forward - missing refresh
old_df = '''    def delete_forward(self):
        fid = self.get_selected_fwd()
        if fid is None:
            return
        delete_port_forward(fid)'''
new_df = '''    def delete_forward(self):
        fid = self.get_selected_fwd()
        if fid is None:
            return
        delete_port_forward(fid)
        self.refresh_forwards()'''
content = content.replace(old_df, new_df)

with open(r"E:\code\python\openXterm\src\main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Done! File updated successfully.")
