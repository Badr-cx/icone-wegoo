import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# المصادر اللي ثبتات القوة ديالها فـ الكروت
SOURCES = [
    "https://cccam.premium.pro/free-cccam/",
    "https://testcline.com/free-cccam-server.php",
    "https://cccamcard.com/free-cccam-server.php",
    "https://www.tvlivepro.com/free_cccam_48h/",
    "https://dhoom.org/test/",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://cccamia.com/free-cccam/",
    "https://cccam.net/freecccam",
    "https://www.cccambird.com/freecccam.php",
    "https://skyhd.xyz/freetest/osm.php",
    "https://kinghd.info/packs.php",
    "https://iptv-m3u.online/free-cccam-server/"
]

def elite_tester(line):
    # تنقية السطر من أي HTML
    line = re.sub(r'<[^>]*>', '', line).strip()
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.IGNORECASE)
    if not match: return None
    
    host, port, user, password = match.groups()
    
    # تحديد السيرفرات "النخبة" (Lisboa, OVH, Premium)
    is_elite = any(x in host.lower() for x in ['lisboa', 'gold', '51.', '185.', '57.', 'premium'])
    
    start_time = time.time()
    try:
        # فحص صارم جداً (0.3 ثانية) - السيرفر اللي تعطل غير 1ms زيادة كيطير
        with socket.create_connection((host, int(port)), timeout=0.3):
            latency = (time.time() - start_time) * 1000
            
            # تنقيط السيرفر
            if is_elite and latency < 120:
                score = 1  # VIP Elite
            elif latency < 180:
                score = 2  # High Quality
            else:
                score = 3  # Standard
                
            return (score, latency, host, user, f"C: {host} {port} {user} {password} # 💎 POWER-SERVER ({int(latency)}ms)")
    except:
        return None

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_raw = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    print(f"📡 فحص النخبة جارٍ... {now}")
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10, headers=headers)
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.IGNORECASE)
            all_raw.extend(found)
        except: continue

    # فحص متوازي بـ 80 خيط لضمان السرعة
    with ThreadPoolExecutor(max_workers=80) as executor:
        results = [r for r in executor.map(elite_tester, list(set(all_raw))) if r]

    # الترتيب: الأقوى ثم الأسرع
    results.sort(key=lambda x: (x[0], x[1]))
    
    final_servers = []
    seen_hosts = set()
    seen_users = set() # منع تكرار اليوزر لضمان الاتصال
    
    for score, lat, host, user, line in results:
        # شرط: السيرفر ما يتعاودش واليوزر ما يتعاودش
        if host not in seen_hosts and user not in seen_users and len(final_servers) < 10:
            final_servers.append(line)
            seen_hosts.add(host)
            seen_users.add(user)

    # كتابة الملف النهائي
    with open("CCcam.cfg", "w") as f:
        f.write(f"### LAST UPDATE: {now} ###\n")
        f.write(f"### SYSTEM: ANTI-BLOCK ELITE FILTER ###\n\n")
        for s in final_servers:
            f.write(f"{s}\n")
    
    print(f"✅ مبروك! عندك دابا أنقى وأقوى 10 سطور فـ العالم المجاني.")

if __name__ == "__main__":
    main()
