import os, sys, json, base64

# The main.py source code in base64
B64_DATA = "REPLACE_ME"

def main():
    data = base64.b64decode(B64_DATA).decode("utf-8")
    path = os.path.join(os.path.dirname(__file__), "src", "main.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("Written OK:", len(data), "bytes")

if __name__ == "__main__":
    main()