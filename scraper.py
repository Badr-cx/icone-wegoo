import requests
import re
import socket
import time

# المصادر المختلطة لضمان النتيجة (المواقع البريميوم + روابط RAW)
TARGETS = [
    "https://cccam-premium.pro/free-cccam/",
    "https://cccam.net/",
    "https://vipsat.net/free-cccam-server.php",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt"
]

def verify_server(host, port):
    try:
        with socket.create_connection((host, int(port)), timeout=1.5):
            return True
    except:
        return False

def run_scraper():
    print("🚀 Starting Scraper for Badr-cx/icone-wegoo...")
    final_clines = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in TARGETS:
        try:
            # إضافة بارامتر عشوائي لتجنب التخزين المؤقت (Cache)
            r = requests.get(f"{url}?v={time.time()}", headers=headers, timeout=10)
            matches = re.findall(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', r.text, re.I)
            
            for host, port, user, passwd in matches:
                if verify_server(host, port):
                    cline = f"C: {host} {port} {user} {passwd}"
                    if cline not in final_clines:
                        final_clines.append(cline)
        except:
            continue

    if final_clines:
        # تحديث ملف VERIFIED_CANNON.cfg المطلوب
        with open("VERIFIED_CANNON.cfg", "w", encoding="utf-8") as f:
            f.write("\n".join(final_clines))
        print(f"✅ Success! Updated VERIFIED_CANNON.cfg with {len(final_clines)} live servers.")
    else:
        print("⚠️ No live servers found right now.")

if __name__ == "__main__":
    run_scraper()
