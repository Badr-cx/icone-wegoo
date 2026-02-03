import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# المصادر الموثوقة اللي فيها التحديث يومي
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
    # تنظيف السطر من أي بقايا HTML
    line = re.sub(r'<[^>]*>', '', line).strip()
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.IGNORECASE)
    if not match: return None
    
    host, port, user, password = match.groups()
    
    # فحص تقني للسيرفر
    start_time = time.time()
    try:
        # فحص الاتصال (Ping) في أقل من 0.5 ثانية
        with socket.create_connection((host, int(port)), timeout=0.5):
            latency = (time.time() - start_time) * 1000
            
            # تصنيف السيرفرات حسب القوة
            tag = "⚽ MULTI-SAT"
            if "king" in host.lower() or "51." in host: tag = "👑 ASTRA-KING"
            if "star" in host.lower() or "85." in host: tag = "📡 HOTBIRD-POWER"
            
            return (latency, f"C: {host} {port} {user} {password} # {tag} ({int(latency)}ms)")
    except:
        return None

def main():
    print("--- [ 🚀 SHΔDØW SNIPER V82 - STARTING MISSION ] ---")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_raw = []
    
    # 1. سحب الأسطر من جميع المصادر
    for url in SOURCES:
        try:
            print(f"[*] جاري سحب الأسطر من: {url.split('/')[2]}...")
            r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.IGNORECASE)
            all_raw.extend(found)
        except:
            continue

    all_raw = list(set(all_raw)) # إزالة التكرار
    print(f"[✔] تم العثور على {len(all_raw)} سطر محتمل. جاري الفحص...")

    # 2. الفحص المتوازي (سرعة خارقة)
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = [r for r in executor.map(multi_sat_sniper, all_raw) if r]

    # 3. الترتيب حسب السرعة (الأسرع هو الأول)
    results.sort(key=lambda x: x[0])
    
    # 4. حفظ أفضل 20 سطر فقط
    with open("CCcam.cfg", "w") as f:
        f.write(f"### LAST UPDATE: {now} ###\n")
        f.write(f"### TOP 20 FASTEST SERVERS ###\n\n")
        for i, (lat, line) in enumerate(results[:20]):
            f.write(f"{line}\n")
            if i < 3: print(f"🔥 سطر ذهبي: {line}")

    print(f"\n[✔] المهمة اكتملت! تم حفظ أفضل {len(results[:20])} سطر في ملف CCcam.cfg")

if __name__ == "__main__":
    main()
