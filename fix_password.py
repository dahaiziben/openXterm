import zipfile, os

pyz = r"E:\code\python\openXterm\dist\OpenXterm.pyz"
src_dir = r"E:\code\python\openXterm\src"
main_py = os.path.join(src_dir, "main.py")

with open(main_py, "r", encoding="utf-8") as f:
    main = f.read()

# Fix the triple-quote password bug
old_pwd = '            password = """\n            if conn.get("password"):'
new_pwd = '            password = ""\n            if conn.get("password"):'
main = main.replace(old_pwd, new_pwd)

old_pwd2 = '                except Exception:\n                    password = """'
new_pwd2 = '                except Exception:\n                    password = ""'
main = main.replace(old_pwd2, new_pwd2)

old_jpwd = '            jump_password = """\n            if conn.get("jump_password"):'
new_jpwd = '            jump_password = ""\n            if conn.get("jump_password"):'
main = main.replace(old_jpwd, new_jpwd)

old_jpwd2 = '                except Exception:\n                    jump_password = """'
new_jpwd2 = '                except Exception:\n                    jump_password = ""'
main = main.replace(old_jpwd2, new_jpwd2)

# Verify no more triple quotes
print("password triple quotes:", main.count('password = """'))
print("jump_password triple quotes:", main.count('jump_password = """'))

# Write fixed src
with open(main_py, "w", encoding="utf-8") as f:
    f.write(main)
print("src/main.py fixed")

# Rebuild pyz
import zipapp
zipapp.create_archive(src_dir, pyz)
print("pyz rebuilt")

# Verify fix
with zipfile.ZipFile(pyz, "r") as z:
    m = z.read("main.py").decode()
    print("pyz verify - password bugs:", m.count('password = """'))
    # Show the fixed area
    idx = m.find("do_connect")
    print(m[idx:idx+450])
