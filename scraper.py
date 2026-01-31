import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# المصادر الشاملة للأقمار الأربعة
SOURCES = [
    "https://cccam.premium.pro/free-cccam/",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://cccamfree.cc/free-cccam-server/",
    "https://testcline.com/free-cccam-server.php",
    "https://cccamcard.com/free-cccam-server.php",
    "https://www.cccambird.com/freecccam.php",
    "https://iptv-m3u.online/free-cccam-server/"
]

def multi_sat_sniper(line):
    line = re.sub(r'<[^>]*>', '', line).strip()
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.IGNORECASE)
    if not match: return None
    
    host, port, user, password = match.groups()
    
    # تحديد الهوية التقنية للسيرفر
    host_lower = host.lower()
    is_astra_king = any(k in host_lower for k in ['51.', '185.233', '57.', 'lisboa'])
    is_hotbird_16e = any(k in host_lower for k in ['starcline', 'mytvworld', '8safenine', 'ugeen'])
    
    start_time = time.time()
    try:
        # فحص جودة صارم (0.28 ثانية)
        with socket.create_connection((host, int(port)), timeout=0.28):
            latency = (time.time() - start_time) * 1000
            
            # نظام الأولوية (Priority Score)
            if is_astra_king and latency < 120:
                score, tag = 1, "👑 ASTRA-ULTRA" # التوب ديال أسترا
            elif is_hotbird_16e and latency < 150:
                score, tag = 2, "📡 HB/16E-POWER" # التوب ديال هوتبرد و 16 شرق
            elif latency < 180:
                score, tag = 3, "⚽ MULTI-SAT" # الباقي (Hispasat + Others)
            else:
                return None
                
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

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = [r for r in executor.map(multi_sat_sniper, list(set(all_raw))) if r]

    # الترتيب حسب الطبقات ثم السرعة
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
        f.write(f"### MISSION: ASTRA-KING + HB/16E/30W ###\n\n")
        for s in final_servers:
            f.write(f"{s}\n")

if __name__ == "__main__":
    main()
