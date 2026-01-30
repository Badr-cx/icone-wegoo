import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

SOURCES = [
    "https://cccamcard.com/free-cccam-server.php",
    "https://testcline.com/free-cccam-server.php",
    "https://cccam.premium.pro/free-cccam/",
    "https://cccamia.com/free-cccam/",
    "https://raw.githubusercontent.com/Badr-cx/icone-wegoo/refs/heads/main/CCcam.cfg"
]

def advanced_tester(line):
    """محاكاة بسيطة للـ Handshake اللي في كود C"""
    line = re.sub(r'<[^>]*>', '', line).strip()
    match = re.search(r'([CN]:\s*\S+\s+\d+\s+\S+\s+\S+)', line)
    if not match: return None
    
    clean_line = match.group(1)
    parts = clean_line.split()
    host, port = parts[1], int(parts[2].replace(',', ''))
    
    try:
        # 1. محاولة الاتصال (TCP Connection)
        with socket.create_connection((host, port), timeout=0.8) as sock:
            # 2. انتظار الـ Hello Seed من السيرفر (بحرال كود C اللي كيتسنى 16 byte)
            sock.settimeout(1.0)
            seed = sock.recv(16)
            
            if len(seed) >= 12: # السيرفرات الحقيقية هي اللي كتصيفط هاد الـ Seed
                return clean_line
            return None
    except:
        return None

def main():
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_found = []
    
    print(f"🚀 بدء الفحص الاحترافي - تحديث {today}")

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            found = re.findall(r'[CN]:\s?\S+\s\d+\s\S+\s\S+', r.text)
            all_found.extend(found)
        except: continue

    unique_lines = list(set(all_found))
    print(f"🔍 لقيت {len(unique_lines)} سطر. جاري الفحص المعمق...")

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(advanced_tester, unique_lines))

    online = [s for s in results if s]

    with open("CCcam.cfg", "w") as f:
        f.write(f"# 📅 Last Verified: {today}\n")
        f.write(f"# 🛰️ Status: {len(online)} Servers Online\n\n")
        for s in online:
            f.write(s + "\n")

    print(f"✅ تم التحديث! بقاو {len(online)} سيرفر ناضيين.")

if __name__ == "__main__":
    main()
