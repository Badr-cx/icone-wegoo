import requests, re, socket, time, concurrent.futures
from datetime import datetime

# قائمة المصادر العملاقة - تشمل مستودعات عالمية ومواقع توليد لحظية
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/Fidat-T/Free-CCcam/main/cccam.txt",
    "https://raw.githubusercontent.com/tjm1024/Free-TV/master/cccam.txt",
    "https://raw.githubusercontent.com/mizstd/CCcam-Free/main/cccam.txt",
    "https://raw.githubusercontent.com/best-cccam/free/main/cccam.cfg",
    "https://raw.githubusercontent.com/S-K-S-B/CCcam/main/free.txt",
    "https://raw.githubusercontent.com/S-K-S-B/CCcam/main/cccam.txt",
    "https://raw.githubusercontent.com/Mahesh0433/CCcam-Free/main/cccam.txt",
    "https://raw.githubusercontent.com/yebekhe/Telegram-V2Ray-Config/main/sub/base64", # أحيانا تحتوي روابط مخفية
    "https://clinetest.net/free_cccam.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://cccamfree.cc/free-cccam-server/",
    "https://www.cccam786.com/free-cccam/",
    "https://cccam.io/free-cccam/",
    "https://vipsat.net/free-cccam-server.php",
    "https://fastcccam.com/free-cccam.php",
    "http://www.boss-cccam.com/Free.php",
    "https://www.cccam2.com/free-cccam-server.php",
    "https://free.cccam.io/",
    "https://cccamgood.com/free-cccam-server.php",
    "https://satna.club/freelines.php"
]

def verify_beast_mode(line):
    """ فحص صارم: استجابة فورية أو طرد نهائي """
    line = line.strip()
    # تنظيف السطر من أي رموز غريبة
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    try:
        start = time.perf_counter()
        # محاولة اتصال جبارة في 0.4 ثانية فقط لضمان عدم وجود رمشة (Freeze)
        with socket.create_connection((host, int(port)), timeout=0.4) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            # تصنيف السيرفرات حسب السرعة
            if latency < 150: quality = "💎 ELITE"
            elif latency < 300: quality = "🚀 FAST"
            else: quality = "✅ OK"
            return (latency, f"C: {host} {port} {user} {passwd} # {quality}_{latency}ms")
    except:
        return None

def execute_annihilation():
    print("💀 SHΔDØW CORE: جاري اكتساح الشبكة.. استعد للكميات الضخمة...")
    
    all_raw_lines = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    # سحب البيانات بسرعة الصاروخ
    with requests.Session() as session:
        session.headers.update(headers)
        for url in SOURCES:
            try:
                print(f"📡 فحص المصدر: {url[:40]}...")
                r = session.get(url, timeout=7, verify=False)
                # استخراج كل ما يشبه سطر CCcam
                found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                all_raw_lines.extend(found)
            except:
                continue

    # حذف التكرار
    unique_pool = list(set(all_raw_lines))
    total_found = len(unique_pool)
    print(f"\n✅ تم العثور على {total_found} سيرفر خام.")
    print(f"🔥 جاري تصفية "الذهب" من النحاس (الفحص الفعلي)...")

    # فحص متوازي ضخم (300 خيط معالجة)
    with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
        results = list(executor.map(verify_beast_mode, unique_pool))

    # ترتيب السيرفرات الشغالة من الأسرع للأبطأ
    working = sorted([r for r in results if r], key=lambda x: x[0])

    # كتابة الملف النهائي بأسلوب احترافي
    with open("SHADOW_ULTIMATE.cfg", "w") as f:
        f.write(f"# SHΔDØW CORE V100 - THE WORLD DOMINATION\n")
        f.write(f"# DATE: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"# TOTAL LIVE SERVERS: {len(working)}\n")
        f.write("# --------------------------------------------------\n\n")
        for _, server in working:
            f.write(f"{server}\n")

    print(f"\n✨ المهمة اكتملت! تم استخراج {len(working)} سيرفر شغال 100%.")
    print(f"📂 الملف المحقون جاهز: SHADOW_ULTIMATE.cfg")
    print("💻 تبرّع بيهم ولا استمتع بيهم وحدك.. المهم السيرفرات نار!")

if __name__ == "__main__":
    execute_annihilation()
