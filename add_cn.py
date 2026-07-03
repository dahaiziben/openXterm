path = "E:/code/python/openXterm/src/main.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Find where THEME ends and insert CN dict
theme_end = content.find("}\n\n")
if theme_end > 0:
    cn_dict = '''
CN = {
    "port_forward": "\u7aef\u53e3\u8f6c\u53d1",
    "forward_name": "\u8f6c\u53d1\u540d\u79f0",
    "forward_type": "\u8f6c\u53d1\u7c7b\u578b",
    "listen_port": "\u76d1\u542c\u7aef\u53e3",
    "dest_host": "\u76ee\u6807\u4e3b\u673a",
    "dest_port": "\u76ee\u6807\u7aef\u53e3",
    "new_conn": "\u65b0\u8fde\u63a5",
    "edit_conn": "\u7f16\u8f91\u8fde\u63a5",
    "connection_mgr": "OpenXterm - SSH \u8fde\u63a5\u7ba1\u7406\u5668",
    "conn_name": "\u8fde\u63a5\u540d\u79f0:",
    "host": "\u4e3b\u673a / IP:",
    "port": "\u7aef\u53e3:",
    "username": "\u7528\u6237\u540d:",
    "password": "\u5bc6\u7801:",
    "jump_host": "\u8df3\u677f\u673a (\u53ef\u9009):",
    "jump_user": "\u8df3\u677f\u7528\u6237:",
    "jump_password": "\u8df3\u677f\u5bc6\u7801:",
    "extra_args": "\u989d\u5916\u53c2\u6570:",
    "add_conn": "+ \u65b0\u5efa\u8fde\u63a5",
    "refresh": "\u27f3 \u5237\u65b0",
    "connect": "\u25b6 \u8fde\u63a5",
    "edit": "\u270f \u7f16\u8f91",
    "delete": "\u2718 \u5220\u9664",
    "port_forward_mgr": "\u2194 \u7aef\u53e3\u8f6c\u53d1",
    "confirm_delete": "\u786e\u5b9a\u5220\u9664?",
    "select_first": "\u8bf7\u5148\u9009\u62e9\u4e00\u4e2a\u8fde\u63a5",
    "required": "\u4e3b\u673a\u548c\u7528\u6237\u540d\u4e3a\u5fc5\u586b\u5b57\u6bb5",
    "parse_ssh": "\u4eceSSH\u547d\u4ee4\u89e3\u6790",
    "ssh_from_cmd": "\u4eceSSH\u547d\u4ee4\u89e3\u6790",
    "paste_ssh": "\u8bf7\u7c98\u8d34 SSH \u547d\u4ee4\u5b57\u7b26\u4e32",
    "parse": "\u89e3\u6790",
    "parse_fail": "\u65e0\u6cd5\u89e3\u6790\u8be5 SSH \u547d\u4ee4",
    "cancel": "\u53d6\u6d88",
    "ok": "\u786e\u5b9a",
    "connecting": "\u6b63\u5728\u8fde\u63a5",
    "connected": "\u5df2\u8fde\u63a5",
    "error": "\u9519\u8bef",
    "connect_fail": "\u8fde\u63a5\u5931\u8d25",
    "tunnel_established": "\u96a7\u9053\u5df2\u5efa\u7acb",
    "local": "\u672c\u5730",
    "remote": "\u8fdc\u7a0b",
    "dynamic": "\u52a8\u6001",
    "socks": "SOCKS",
    "add_forward_btn": "+ \u6dfb\u52a0\u8f6c\u53d1",
    "onekey_connect": "\u25b6 \u4e00\u952e\u8fde\u63a5+\u8f6c\u53d1",
    "forward_mgr_title": "\u7aef\u53e3\u8f6c\u53d1",
    "conn_mgr_tab": "  \u8fde\u63a5\u7ba1\u7406  ",
    "select_forward_first": "\u8bf7\u5148\u9009\u62e9\u4e00\u4e2a\u8f6c\u53d1\u89c4\u5219",
    "confirm_del_forward": "\u786e\u5b9a\u5220\u9664\u8be5\u8f6c\u53d1\u89c4\u5219?",
    "port_must_be_num": "\u7aef\u53e3\u5fc5\u987b\u662f\u6570\u5b57",
    "edit_forward": "\u7f16\u8f91\u8f6c\u53d1",
    "del_forward": "\u5220\u9664\u8f6c\u53d1",
    "ready": "\u5c31\u7eea",
    "total_conns": "\u5171 {} \u4e2a\u8fde\u63a5",
    "conn_id": "ID",
    "conn_name_col": "\u8fde\u63a5\u540d\u79f0",
    "host_col": "\u4e3b\u673a",
    "port_col": "\u7aef\u53e3",
    "user_col": "\u7528\u6237\u540d",
    "jump_col": "\u8df3\u677f\u673a",
    "confirm_del_conn": "\u786e\u5b9a\u5220\u9664\u8be5\u8fde\u63a5?",
    "forward_name_col": "\u540d\u79f0",
    "forward_type_col": "\u7c7b\u578b",
    "forward_listen_col": "\u76d1\u542c",
    "forward_dest_col": "\u76ee\u6807",
    "tunnel_active": "\u96a7\u9053\u6d3b\u8dc3: {}",
}
'''
    insert_pos = theme_end + 3  # after "}\n\n" + THEME ending brace
    content = content[:insert_pos] + cn_dict + content[insert_pos:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK - added CN dict")
else:
    print("Could not find THEME end")