import os
path = r"E:\code\python\openXterm\src\main.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find and fix the do_connect method by rebuilding it
new_lines = []
in_do_connect = False
in_worker = False
skip_mode = False
for line in lines:
    if line.strip().startswith("def do_connect(self, conn):"):
        in_do_connect = True
        skip_mode = True
        new_lines.append(line)
        continue
    if in_do_connect and line.strip().startswith("def _show_error"):
        in_do_connect = False
        skip_mode = False
        new_lines.append(line)
        continue
    if in_do_connect and line.strip().startswith("def main():"):
        in_do_connect = False
        skip_mode = False
        new_lines.append(line)
        continue
    
    if not skip_mode:
        new_lines.append(line)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Removed corrupted do_connect, need to insert new one")
