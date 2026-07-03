import zipfile, os

src_dir = r"E:\code\python\openXterm\src"
main_py = os.path.join(src_dir, "main.py")

with open(main_py, "r", encoding="utf-8") as f:
    main = f.read()

# Disable keyboard-interactive auth to prevent password prompt
# In all jc.connect and c.connect calls, add disabled_algorithms
old1 = """jc.connect(jump_host, port=jump_port, username=jump_user,
                                   password=jump_password if jump_password else None,
                                   look_for_keys=False, allow_agent=False, timeout=10)"""
new1 = """jc.connect(jump_host, port=jump_port, username=jump_user,
                                   password=jump_password if jump_password else None,
                                   look_for_keys=False, allow_agent=False, timeout=10,
                                   disabled_algorithms={"auth": ["keyboard-interactive"]})"""
main = main.replace(old1, new1)

old2 = """c.connect(host, port=port, username=username,
                                   password=password if password else None,
                                   sock=sock, look_for_keys=False, allow_agent=False, timeout=10)"""
new2 = """c.connect(host, port=port, username=username,
                                   password=password if password else None,
                                   sock=sock, look_for_keys=False, allow_agent=False, timeout=10,
                                   disabled_algorithms={"auth": ["keyboard-interactive"]})"""
main = main.replace(old2, new2)

old3 = """c.connect(host, port=port, username=username,
                                   password=password if password else None,
                                   look_for_keys=False, allow_agent=False, timeout=10)"""
new3 = """c.connect(host, port=port, username=username,
                                   password=password if password else None,
                                   look_for_keys=False, allow_agent=False, timeout=10,
                                   disabled_algorithms={"auth": ["keyboard-interactive"]})"""
main = main.replace(old3, new3)

with open(main_py, "w", encoding="utf-8") as f:
    f.write(main)

# Rebuild pyz
import zipapp
zipapp.create_archive(src_dir, r"E:\code\python\openXterm\dist\OpenXterm.pyz")

# Verify
with zipfile.ZipFile(r"E:\code\python\openXterm\dist\OpenXterm.pyz", "r") as z:
    m = z.read("main.py").decode()
    count = m.count("disabled_algorithms")
    print(f"disabled_algorithms occurrences: {count} (expected 3)")
    print("Fix applied!" if count == 3 else "SOMETHING WRONG")
