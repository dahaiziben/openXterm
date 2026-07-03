import re

with open(r"E:\code\python\openXterm\src\main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace setup_ui style block - match lines precisely
lines = content.split("\n")
new_lines = []
i = 0
in_style_block = False
style_lines = []
while i < len(lines):
    line = lines[i]
    
    # Detect start of setup_ui style block
    if line.rstrip() == 'style = ttk.Style()' and i > 0 and 'def setup_ui' in lines[i-1]:
        in_style_block = True
        style_lines = []
    
    if in_style_block:
        if line.strip().startswith('style.') or line.strip() == '':
            style_lines.append(line)
            i += 1
            continue
        else:
            # End of style block - replace
            in_style_block = False
            new_lines.append('        style = ttk.Style()')
            new_lines.append('        style.theme_use("clam")')
            new_lines.append('        style.configure("TLabel", background=THEME["bg"], foreground=THEME["fg"], font=("Segoe UI", 10))')
            new_lines.append('        style.configure("TFrame", background=THEME["bg"])')
            new_lines.append('        style.configure("TButton", background=THEME["btn_bg"], foreground=THEME["btn_fg"], borderwidth=1, font=("Segoe UI", 10))')
            new_lines.append('        style.configure("Treeview", background=THEME["tree_bg"], foreground=THEME["tree_fg"], fieldbackground=THEME["tree_bg"], font=("Segoe UI", 10))')
            new_lines.append('        style.configure("Treeview.Heading", background=THEME["header_bg"], foreground=THEME["fg"], relief="flat", font=("Segoe UI", 10, "bold"))')
            new_lines.append('        style.map("Treeview", background=[("selected", THEME["tree_sel"])], foreground=[("selected", THEME["fg"])])')
            new_lines.append('        style.map("TButton", background=[("active", THEME["accent"])], foreground=[("active", THEME["accent_fg"])])')
            new_lines.append('        style.configure("TNotebook", background=THEME["bg"])')
            new_lines.append('        style.configure("TNotebook.Tab", background=THEME["header_bg"], foreground=THEME["fg"])')
            new_lines.append('        style.map("TNotebook.Tab", background=[("selected", THEME["bg"])], foreground=[("selected", THEME["accent"])])')
            new_lines.append('        style.configure("TSeparator", background=THEME["border"])')
            continue
    
    new_lines.append(line)
    i += 1

content = "\n".join(new_lines)

# Update ConnectionDialog style block
old_cd = [
    '        style = ttk.Style()',
    '        style.theme_use("clam")',
    '        style.configure("TLabel", background=THEME["bg"], foreground=THEME["fg"])',
    '        style.configure("TEntry", fieldbackground=THEME["select"], foreground=THEME["fg"])',
    '        style.configure("TFrame", background=THEME["bg"])',
    '        style.configure("TButton", background=THEME["btn_bg"], foreground=THEME["btn_fg"])',
    '        style.configure("TSeparator", background=THEME["border"])',
    '        style.map("TButton", background=[("active", THEME["accent"])], foreground=[("active", THEME["accent_fg"])])',
]

new_cd = [
    '        style = ttk.Style()',
    '        style.theme_use("clam")',
    '        style.configure("TLabel", background=THEME["bg"], foreground=THEME["fg"], font=("Segoe UI", 10))',
    '        style.configure("TEntry", fieldbackground=THEME["select"], foreground=THEME["fg"], font=("Segoe UI", 10))',
    '        style.configure("TFrame", background=THEME["bg"])',
    '        style.configure("TButton", background=THEME["btn_bg"], foreground=THEME["btn_fg"], font=("Segoe UI", 10))',
    '        style.configure("TSeparator", background=THEME["border"])',
    '        style.map("TButton", background=[("active", THEME["accent"])], foreground=[("active", THEME["accent_fg"])])',
]

old_str = "\n".join(old_cd)
new_str = "\n".join(new_cd)
content = content.replace(old_str, new_str)

# Also update PortForwardDialog and PortForwardManager style blocks  
old_pfd = [
    '        style.configure("TLabel", background=THEME["bg"], foreground=THEME["fg"])',
    '        style.configure("TEntry", fieldbackground=THEME["select"], foreground=THEME["fg"])',
    '        style.configure("TFrame", background=THEME["bg"])',
]
new_pfd = [
    '        style.configure("TLabel", background=THEME["bg"], foreground=THEME["fg"], font=("Segoe UI", 10))',
    '        style.configure("TEntry", fieldbackground=THEME["select"], foreground=THEME["fg"], font=("Segoe UI", 10))',
    '        style.configure("TFrame", background=THEME["bg"])',
]
for o, n in zip(old_pfd, new_pfd):
    content = content.replace(o, n)

# Update status bar
content = content.replace(
    'relief=tk.SUNKEN, anchor=tk.W, background=THEME["header_bg"], foreground=THEME["fg"]',
    'relief=tk.FLAT, anchor=tk.W, background=THEME["header_bg"], foreground=THEME["fg"], padding=(8, 4)'
)

with open(r"E:\code\python\openXterm\src\main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Style updates applied successfully")
