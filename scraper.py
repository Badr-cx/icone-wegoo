import requests, re, socket, time, concurrent.futures
from datetime import datetime

# المصادر المحدثة بروابط الـ RAW المباشرة
SOURCES = [
    # الرابط الخاص بك (تم تحويله لـ RAW ليقرأ المحتوى مباشرة)
    "https://raw.githubusercontent.com/Badr-cx/icone-wegoo/main/VERIFIED_CANNON.cfg",
    # روابط تيليغرام قوية جداً
    "https://t.me/s/Free_Cccam_Server_Daily",
    "https://t.me/s/vipsat_net",
    "https://t.me/s/smart_cccam",
    # مواقع أوروبية (تعطي سيرفرات طازجة)
    "https://cccamia.com/cccamfree1/",
    "https://cccamcard.com/free-cccam-server.php",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt"
]

def verify_server(line):
    # تنظيف السطر من أي شوائب HTML أو مسافات زائدة
    line = re.sub('<[^<]+?>', '', line).strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    if any(f in host.lower() for f in ['127.0.0.1', 'nassim', 'stream']): return None

    try:
        start = time.perf_counter()
        # محاولة اتصال حقيقية بالمنفذ (Port) للتأكد من اشتغال السيرفر
        with socket.create_connection((host, int(port)), timeout=2.0) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            return (latency, host, port, user, passwd)
    except:
        return None

def run_scraper():
    print(f"🚀 جاري استخراج السيرفرات من {len(SOURCES)} مصادر...")
    all_raw = []
    
    session = requests.Session()
    # إضافة User-Agent لتبدو كمتصفح حقيقي وتتجنب الحظر
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

    for url in SOURCES:
        try:
            r = session.get(url, timeout=15)
            # استخراج أسطر C: التقليدية
            matches = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
            
            # في حال كانت السيرفرات في تيليغرام بدون حرف C:
            if not matches:
                extra = re.findall(r'([a-zA-Z0-9\-\.]+\s+\d+\s+[a-zA-Z0-9\-\.]+\s+[a-zA-Z0-9\-\.]+)', r.text)
                for e in extra:
                    if e.split()[1].isdigit(): matches.append(f"C: {e}")
            
            all_raw.extend(matches)
            print(f"✅ {url.split('/')[-1]}: وجدنا {len(matches)} سيرفر")
        except: continue

    unique_list = list(set(all_raw))
    print(f"🧪 جاري فحص جودة {len(unique_list)} سيرفر... انتظر قليلاً.")

    # فحص 150 سيرفر في وقت واحد (سرعة صاروخية)
    with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
        results = [r for r in executor.map(verify_server, unique_list) if r]

    # ترتيب من الأسرع للأبطأ
    results.sort(key=lambda x: x[0])

    if results:
        with open("ncam.server", "w", encoding="utf-8") as f:
            f.write(f"### GENERATED | {datetime.now().strftime('%H:%M')} ###\n")
            for i, (lat, host, port, user, passwd) in enumerate(results[:50]):
                f.write(f"\n[reader]\nlabel = Server_{i+1}_{lat}ms\nprotocol = cccam\ndevice = {host},{port}\nuser = {user}\npassword = {passwd}\ngroup = 1\ncccversion = 2.3.2\nccckeepalive = 1\n")
        
        with open("CCcam.cfg", "w", encoding="utf-8") as f:
            for lat, host, port, user, passwd in results[:50]:
                f.write(f"C: {host} {port} {user} {passwd} # {lat}ms\n")
        
        print(f"✨ تم العثور على {len(results)} سيرفر شغال 100%!")
        print(f"📂 الملفات ncam.server و CCcam.cfg جاهزة الآن.")
    else:
        print("❌ لم نجد أي سيرفر شغال حالياً. ربما السيرفرات في الروابط توقفت.")

if __name__ == "__main__":
    run_scraper()
