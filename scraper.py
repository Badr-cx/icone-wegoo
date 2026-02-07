import requests
import re
import socket

# المصادر المستهدفة
SOURCES = [
    "https://cccam-premium.pro/free-cccam/",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt"
]

def check_server(host, port):
    try:
        with socket.create_connection((host, int(port)), timeout=2):
            return True
    except:
        return False

def main():
    print("🚀 Starting Server Scraper...")
    all_clines = []
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            matches = re.findall(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', r.text, re.I)
            for m in matches:
                host, port, user, pw = m
                if check_server(host, port):
                    all_clines.append(f"C: {host} {port} {user} {pw}")
        except:
            continue

    # إزالة التكرار
    unique_clines = list(set(all_clines))
    
    # حفظ في الملف
    if unique_clines:
        with open("VERIFIED_CANNON.cfg", "w") as f:
            f.write("\n".join(unique_clines))
        print(f"✅ Saved {len(unique_clines)} verified servers.")

if __name__ == "__main__":
    main()
