import requests, re, socket, time, concurrent.futures
from datetime import datetime

# مصادر تعتمد على صفحات "الفحص المباشر" ونتائج الاختبارات
CHECKER_SOURCES = [
    "https://vipsat.net/free-cccam-server.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://clinetest.net/free_cccam.php",
    "https://fastcccam.com/free-cccam.php",
    "https://cccam786.com/free-cccam/",
    "https://www.cccam2.com/free-cccam-server.php",
    "https://raw.githubusercontent.com/mueof/free-cccam/main/cccam.txt", # مستودع مفحوص آلياً
    "http://www.cccamfree.cc/free-cccam-server/",
]

def intense_check(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    
    # فلترة الهوستات المستهلكة بزاف (باش نجيبو الجديد)
    if any(x in host for x in ['37.60.251.20', 'streamtveuropa']): return None

    try:
        start = time.perf_counter()
        # فحص صارم جداً (0.2 ثانية) - يا إما طيارة يا إما بلاش
        with socket.create_connection((host, int(port)), timeout=0.2) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            return (latency, f"C: {host} {port} {user} {passwd} # 🔥VERIFIED_{latency}ms")
    except:
        return None

def start_hunting():
    print("💀 SHΔDØW CORE: جاري اختراق مواقع الفحص وسحب السيرفرات الحية...")
    
    verified_pool = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://google.com'
    }

    with requests.Session() as session:
        session.headers.update(headers)
        for url in CHECKER_SOURCES:
            try:
                # سحب الداتا حتى من المواقع اللي فيها حماية بسيطة
                r = session.get(url, timeout=8, verify=False)
                # صيد السطور اللي كتكون غالباً وسط جداول النتائج (Tables)
                found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                verified_pool.extend(found)
            except: continue

    unique_list = list(set(verified_pool))
    print(f"📡 تم رصد {len(unique_list)} سطر من مواقع الفحص. جاري التأكيد النهائي...")

    # فحص متوازي فائق السرعة
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        results = list(executor.map(intense_check, unique_list))

    # ترتيب حسب السرعة (الأقل Ping هو الأول)
    final_elite = sorted([r for r in results if r], key=lambda x: x[0])

    if final_elite:
        with open("VERIFIED_CANNON.cfg", "w") as f:
            f.write(f"# SHΔDØW VERIFIED HITS | {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            for _, server in final_elite[:50]: # خذ أفضل 50 سطر "مكدي"
                f.write(server + "\n")
        print(f"✅ مبروك! لقيت ليك {len(final_elite)} سيرفر ناضي من قلب مواقع الفحص.")
        print("📂 الملف واجد: VERIFIED_CANNON.cfg")
    else:
        print("❌ المواقع حالياً "ناشفة" من السيرفرات الجديدة، جرب مرة أخرى بعد قليل.")

if __name__ == "__main__":
    start_hunting()
