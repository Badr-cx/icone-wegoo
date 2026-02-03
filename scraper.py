import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# المصادر القوية (Astra & Hotbird focus)
SOURCES = [
    "https://cccam.premium.pro/free-cccam/",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://cccamfree.cc/free-cccam-server/",
    "https://www.cccam786.com/free-cccam/",
    "https://cccam.io/free-cccam/",
    "https://sky-cccam.com/free-cccam-server.php",
    "https://cccamspot.com/free-cccam-server/",
    "https://boss-iptv.com/free-cccam/"
]

def check_server(line):
    line = re.sub(r'<[^>]*>', '', line).strip()
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.IGNORECASE)
    if not match: return None
    
    host, port, user, password = match.groups()
    start_time = time.time()
    try:
        # فحص جودة الاتصال في أقل من 0.4 ثانية
        with socket.create_connection((host, int(port)), timeout=0.4):
            latency = (time.time() - start_time) * 1000
            tag = "VIP-GOLD" if latency < 120 else "STABLE"
            return (latency, f"C: {host} {port} {user} {password} # {tag} ({int(latency)}ms)")
    except:
        return None

def main():
    print("🚀 Sniper Mode: Activated")
    all_raw = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10, headers=headers, verify=False)
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.IGNORECASE)
            all_raw.extend(found)
        except: continue

    # إزالة التكرار وفحص السيرفرات
    all_raw = list(set(all_raw))
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = [r for r in executor.map(check_server, all_raw) if r]

    # ترتيب من الأسرع للأبطأ
    results.sort(key=lambda x: x[0])
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("CCcam.cfg", "w") as f:
        f.write(f"### UPDATE: {now} ###\n")
        f.write(f"### ICONE WEGOO READY ###\n\n")
        for lat, line in results[:30]:
            f.write(f"{line}\n")
    print(f"✅ Success! Captured {len(results[:30])} lines.")

if __name__ == "__main__":
    main()
