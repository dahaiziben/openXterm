import base64, os

print("Starting rebuild...")

# Read the base64-encoded fix script
b64 = open("E:\\code\\python\\openXterm\\b64_fix2.txt").read()
script = base64.b64decode(b64).decode("utf-8")
exec(script)
