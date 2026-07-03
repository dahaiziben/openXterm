import os

with open(r"E:\code\python\openXterm\src\main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace THEME with a cleaner, modern look
old_theme_start = content.find("THEME = {")
depth = 0
end_pos = old_theme_start
for i in range(old_theme_start, len(content)):
    if content[i] == "{":
        depth += 1
    elif content[i] == "}":
        depth -= 1
        if depth == 0:
            end_pos = i + 1
            break

new_theme = """THEME = {
    "bg": "#ffffff",
    "fg": "#1a1a2e",
    "select": "#e8f0fe",
    "accent": "#4f6ef7",
    "accent_fg": "#ffffff",
    "tree_bg": "#f8f9fc",
    "tree_fg": "#1a1a2e",
    "tree_sel": "#dce5ff",
    "header_bg": "#f0f2f5",
    "btn_bg": "#4f6ef7",
    "btn_fg": "#ffffff",
    "success": "#2ecc71",
    "error": "#e74c3c",
    "border": "#dfe3e8",
}"""

content = content[:old_theme_start] + new_theme + content[end_pos:]

# Also update the hint_label text
old_hint = '\u63d0\u793a: \u53cc\u51fb\u8fde\u63a5 | \u53f3\u952e\u83dc\u5355'
new_hint = '\u63d0\u793a: \u53cc\u51fb\u8fde\u63a5 | \u53f3\u952e\u83dc\u5355'
print("Old hint present:", old_hint in content)

# Find the hint label more robustly
import re
match = re.search(r'hint_label = ttk\.Label\(self\.root, text="[^"]+", foreground=THEME\["accent"\], background=THEME\["bg"\]\)', content)
if match:
    print("Found hint_label:", match.group()[:60])
    content = content.replace(match.group(), 'hint_label = ttk.Label(self.root, text="\u63d0\u793a: \u53cc\u51fb\u8fde\u63a5 | \u53f3\u952e\u83dc\u5355", foreground=THEME["accent"], background=THEME["bg"])')

with open(r"E:\code\python\openXterm\src\main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Theme and hint updated successfully")
