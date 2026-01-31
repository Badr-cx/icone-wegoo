import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# القائمة الشاملة لجميع المصادر التي أرسلتها
SOURCES = [
    "https://cccam.premium.pro/free-cccam/",
    "https://cccam.net/free",
    "https://cccamia.com/free-cccam/",
    "https://www.cccambird.com/freecccam.php",
    "https://www.cccambird2.com/freecccam.php",
    "https://cccamprime.com/cccam48h.php",
    "https://skyhd.xyz/freetest/osm.php",
    "https://www.tvlivepro.com/free_cccam_48h/",
    "https://dhoom.org/test/",
    "https://cccam.net/freecccam",
    "https://cccamia.com/cccamfree1/",
    "https://www.cccampri.me/cccam24h.php",
    "https://cccam-premium.pro/free-cccam/",
    "https://kinghd.info/packs.php",
    "https://www.cccambird.com/index.php",
    "https://testcline.com/free-cccam-server.php"
]

def detailed_tester(line):
    # تنقية السطر من HTML وأي رموز غريبة (مثل </div>)
    line = re.sub(r'<[^>]*>', '', line).strip()
    line = line.split('\r')[0].split('\n')[0].strip()
    
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.IGNORECASE)
    if not match: return None
    
    host, port, user, password = match.groups()
    start_time = time.time()
    try:
        # فحص جودة الاتصال (Timeout قصير لفلترة السيرفرات الثقيلة)
        with socket.create_connection((host, int(port)), timeout=0.8):
            latency = (time.time() - start_time) * 1000
            
            if latency < 250:
                status = "🚀 FAST"
            elif latency < 600:
                status = "✅ STABLE"
            else:
                status = "📶 SLOW"
                
            clean_line = f"C: {host} {port} {user} {password}"
            return (latency, f"{clean_line} # Status: {status} ({int(latency)}ms)")
    except:
        return None

def main():
    # توقيت المغرب (GMT+1)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_raw = []
    
    print(f"📡 جاري مسح {len(SOURCES)} موقعاً بحثاً عن السيرفرات...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=12, headers=headers)
            # استخراج جميع أسطر C:
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.IGNORECASE)
            all_raw.extend(found)
            print(f"✅ {url.split('/')[2]} -> {len(found)} سيرفر")
        except:
            continue

    # إزالة التكرار
    unique_lines = list(set(all_raw))
    print(f"🔍 فحص {len(unique_lines)} سيرفر فريد... المرجو الانتظار.")
    
    # فحص متوازي بـ 60 خيط لضمان السرعة
    with ThreadPoolExecutor(max_workers=60) as executor:
        results = list(executor.map(detailed_tester, unique_lines))

    # ترتيب النتائج: الأسرع أولاً
    valid_results = sorted([r for r in results if r], key=lambda x: x[0])
    
    # اختيار أفضل 20 سيرفر فقط لضمان خفة الملف على الرسيفر
    top_20 = valid_results[:20]

    # كتابة الملف النهائي
    with open("CCcam.cfg", "w") as f:
        f.write(f"### LAST UPDATE: {now} ###\n")
        f.write(f"### SOURCES: {len(SOURCES)} PREMIUM SITES ###\n")
        f.write(f"### QUALITY: TOP 20 FASTEST SERVERS ###\n\n")
        for latency, s in top_20:
            f.write(f"{s}\n")

    print(f"✅ انتهى! تم العثور على {len(valid_results)} سيرفر شغّال، وتم اختيار أفضل 20.")

if __name__ == "__main__":
    main()
