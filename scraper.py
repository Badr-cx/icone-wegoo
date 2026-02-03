import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# المصادر المختارة بعناية (الثبات والقوة)
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
        # فحص صارم في 0.4 ثانية لضمان الجودة
        with socket.create_connection((host, int(port)), timeout=0.4):
            latency = (time.time() - start_time) * 1000
            
            # تصنيف VIP
            tag = "VIP-STABLE" if latency < 120 else "MULTI-SAT"
            return {
                'latency': latency,
                'host': host, 'port': port, 'user': user, 'pass': password,
                'line': f"C: {host} {port} {user} {password} # {tag} ({int(latency)}ms)"
            }
    except:
        return None

def main():
    print("🚀 Starting Sniper V84...")
    all_raw = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15, headers=headers, verify=False)
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.IGNORECASE)
            all_raw.extend(found)
        except: continue

    all_raw = list(set(all_raw))
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = [r for r in executor.map(check_server, all_raw) if r]

    results.sort(key=lambda x: x['latency'])
    top_results = results[:30] # أفضل 30 سطر

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. حفظ ملف CCcam.cfg (العادي)
    with open("CCcam.cfg", "w") as f:
        f.write(f"### UPDATED: {now} ###\n\n")
        for res in top_results:
            f.write(f"{res['line']}\n")

    # 2. حفظ ملف oscam.server (لأصحاب Wegoo والآيرون)
    with open("oscam.server", "w") as f:
        for i, res in enumerate(top_results):
            f.write(f"[reader]\nlabel = Sniper_Server_{i}\nprotocol = cccam\ndevice = {res['host']},{res['port']}\nuser = {res['user']}\npassword = {res['pass']}\ngroup = 1\ncccversion = 2.3.2\n\n")

    print(f"✅ Mission Accomplished: {len(top_results)} servers captured.")

if __name__ == "__main__":
    main()
