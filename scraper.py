import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# جميع المصادر اللي عطيتيني
SOURCES = [
    "https://cccam.premium.pro/free-cccam/", "https://cccam.net/free",
    "https://cccamia.com/free-cccam/", "https://www.cccambird.com/freecccam.php",
    "https://www.cccambird2.com/freecccam.php", "https://cccamprime.com/cccam48h.php",
    "https://skyhd.xyz/freetest/osm.php", "https://www.tvlivepro.com/free_cccam_48h/",
    "https://dhoom.org/test/", "https://cccam.net/freecccam",
    "https://cccamia.com/cccamfree1/", "https://www.cccampri.me/cccam24h.php",
    "https://cccam-premium.pro/free-cccam/", "https://kinghd.info/packs.php",
    "https://testcline.com/free-cccam-server.php"
]

def detailed_tester(line):
    # تنقية السطر من HTML و </div>
    line = re.sub(r'<[^>]*>', '', line).strip()
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.IGNORECASE)
    if not match: return None
    
    host, port, user, password = match.groups()
    start_time = time.time()
    try:
        with socket.create_connection((host, int(port)), timeout=0.8) as sock:
            latency = (time.time() - start_time) * 1000
            status = "🚀 FAST" if latency < 200 else "✅ STABLE"
            # السطر كيرجع نقي مع التعليق فـ الأخير
            return (latency, host, f"C: {host} {port} {user} {password} # {status} ({int(latency)}ms)")
    except: return None

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_raw = []
    print(f"🚀 Starting Deep Scrape & Test: {now}")

    headers = {'User-Agent': 'Mozilla/5.0'}
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10, headers=headers)
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.IGNORECASE)
            all_raw.extend(found)
        except: continue

    # التيست والفلترة
    with ThreadPoolExecutor(max_workers=60) as executor:
        results = [r for r in executor.map(detailed_tester, list(set(all_raw))) if r]

    # ترتيب حسب السرعة + منع تكرار نفس الـ Host
    results.sort(key=lambda x: x[0])
    seen_hosts = set()
    final_servers = []
    for lat, host, line in results:
        if host not in seen_hosts and len(final_servers) < 20:
            final_servers.append(line)
            seen_hosts.add(host)

    # الكتابة فـ الملف
    with open("CCcam.cfg", "w") as f:
        f.write(f"### LAST UPDATE: {now} ###\n")
        f.write(f"### QUALITY: TOP {len(final_servers)} UNIQUE SERVERS ###\n\n")
        for s in final_servers:
            f.write(f"{s}\n")
    print(f"✅ Done! {len(final_servers)} high-quality servers saved.")

if __name__ == "__main__":
    main()
