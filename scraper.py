import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# قائمة المواقع القوية
SOURCES = [
    "https://cccam.premium.pro/free-cccam/",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://cccamfree.cc/free-cccam-server/",
    "https://testcline.com/free-cccam-server.php",
    "https://cccamcard.com/free-cccam-server.php",
    "https://dhoom.org/test/",
    "https://iptv-m3u.online/free-cccam-server/"
]

# --- خاصية مسح السيرفرات الميتة (Blacklist) ---
DEAD_HOSTS = ['127.0.0.1', 'localhost', 'test.com', 'example.com']
DEAD_PORTS = ['80', '8080', '443', '21'] # بورتات مستحيل تكون CCcam

def extreme_tester(line):
    line = re.sub(r'<[^>]*>', '', line).strip()
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.IGNORECASE)
    if not match: return None
    
    host, port, user, password = match.groups()
    
    # 1. فلتر البورتات والهوسات الميتة (ربح الوقت)
    if host in DEAD_HOSTS or port in DEAD_PORTS:
        return None
    
    # 2. تحديد الجودة (Astra/Hispasat Focus)
    is_top = any(x in host.lower() for x in ['lisboa', '51.', '185.', '57.', 'gold', 'premium'])
    
    start_time = time.time()
    try:
        # فحص فائق السرعة
        with socket.create_connection((host, int(port)), timeout=0.25):
            latency = (time.time() - start_time) * 1000
            
            if is_top and latency < 100:
                tag, score = "⚽ ASTRA/HISPA-VIP", 1
            elif latency < 150:
                tag, score = "💎 MULTI-SAT", 2
            else:
                tag, score = "✅ STABLE", 3
                
            return (score, latency, host, user, f"C: {host} {port} {user} {password} # {tag} ({int(latency)}ms)")
    except: return None

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_raw = []
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.IGNORECASE)
            all_raw.extend(found)
        except: continue

    # فحص متوازي (Parallel Testing)
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = [r for r in executor.map(extreme_tester, list(set(all_raw))) if r]

    results.sort(key=lambda x: (x[0], x[1]))
    
    final_servers = []
    seen_hosts, seen_users = set(), set()
    
    for score, lat, host, user, line in results:
        if host not in seen_hosts and user not in seen_users and len(final_servers) < 15:
            final_servers.append(line)
            seen_hosts.add(host)
            seen_users.add(user)

    with open("CCcam.cfg", "w") as f:
        f.write(f"### LAST UPDATE: {now} ###\n")
        f.write(f"### SPEED-BOOSTED & CLEANED SYSTEM ###\n\n")
        for s in final_servers:
            f.write(f"{s}\n")

if __name__ == "__main__":
    main()
