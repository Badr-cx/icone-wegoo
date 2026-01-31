import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# القائمة الكاملة والنهائية للمصادر (أقوى ما كاين)
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

def power_tester(line):
    # تنقية السطر
    line = re.sub(r'<[^>]*>', '', line).strip()
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.IGNORECASE)
    if not match: return None
    
    host, port, user, password = match.groups()
    
    # فحص الكلمات المفتاحية للسيرفرات القوية
    is_premium = any(x in host.lower() for x in ['lisboa', 'gold', '51.', '185.', '57.', 'premium', 'vip'])
    
    start_time = time.time()
    try:
        # فحص صارم جداً (0.35 ثانية) لضمان "القرطاسة" فقط
        with socket.create_connection((host, int(port)), timeout=0.35):
            latency = (time.time() - start_time) * 1000
            
            # تنقيط السيرفر (Score)
            if is_premium and latency < 130:
                score = 1  # Super VIP
            elif latency < 180:
                score = 2  # Stable
            else:
                score = 3  # Normal
                
            clean_line = f"C: {host} {port} {user} {password}"
            return (score, latency, host, f"{clean_line} # 💎 POWER-SERVER ({int(latency)}ms)")
    except:
        return None

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_raw = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    print(f"📡 جاري مسح {len(SOURCES)} مصادر قوية...")
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=12, headers=headers)
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.IGNORECASE)
            all_raw.extend(found)
        except: continue

    # فحص متوازي فائق السرعة
    with ThreadPoolExecutor(max_workers=70) as executor:
        results = [r for r in executor.map(power_tester, list(set(all_raw))) if r]

    # الترتيب: الأقوى ثم الأسرع
    results.sort(key=lambda x: (x[0], x[1]))
    
    # اختيار أفضل 10 سيرفرات مختلفة
    final_servers = []
    seen_hosts = set()
    for score, lat, host, line in results:
        if host not in seen_hosts and len(final_servers) < 10:
            final_servers.append(line)
            seen_hosts.add(host)

    # كتابة الملف
    with open("CCcam.cfg", "w") as f:
        f.write(f"### LAST UPDATE: {now} ###\n")
        f.write(f"### SYSTEM: TOP 10 ELITE SERVERS ###\n\n")
        for s in final_servers:
            f.write(f"{s}\n")
    
    print(f"✅ تم بنجاح! الرابط دابا عامر 'نحل'.")

if __name__ == "__main__":
    main()
