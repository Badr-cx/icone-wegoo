import requests, re, socket, time, concurrent.futures
from datetime import datetime

# مصادر "خفية" وتحديثات برمجية (GitHub Gists & Hidden Repos)
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/Fidat-T/Free-CCcam/main/cccam.txt",
    "https://raw.githubusercontent.com/tjm1024/Free-TV/master/cccam.txt",
    "https://raw.githubusercontent.com/mizstd/CCcam-Free/main/cccam.txt",
    "https://raw.githubusercontent.com/best-cccam/free/main/cccam.cfg",
    "https://raw.githubusercontent.com/S-K-S-B/CCcam/main/free.txt",
    "https://raw.githubusercontent.com/mueof/free-cccam/main/cccam.txt", # مصدر جديد
    "https://raw.githubusercontent.com/vaxilu/x-ui/main/cccam.txt",     # مصدر جديد
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt", # مصدر جديد
    "http://www.cccam-free.com/",
    "http://www.freecccamserver.com/",
    "http://www.boss-cccam.com/Free.php"
]

def check_satellite_reach(line):
    """ فحص جودة السيرفر: السرعة هي كل شيء """
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    try:
        start = time.perf_counter()
        # تقليل الـ timeout لـ 0.3 ثانية باش نجيبو غير الصوارخ
        with socket.create_connection((host, int(port)), timeout=0.3) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            # تصنيف السيرفرات حسب استجابتها للباقات
            status = "🌟ULTRA" if latency < 100 else "⚡FAST"
            return (latency, f"C: {host} {port} {user} {passwd} # {status}_{latency}ms")
    except:
        return None

def start_scraping():
    print("🕵️‍♂️ SHΔDØW CORE: جاري اختراق المصادر الحصرية...")
    raw_lines = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

    with requests.Session() as session:
        session.headers.update(headers)
        for url in SOURCES:
            try:
                r = session.get(url, timeout=5, verify=False)
                # استخراج السطور بدقة عالية
                found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                raw_lines.extend(found)
            except: continue

    unique_pool = list(set(raw_lines))
    print(f"📡 لقيت {len(unique_pool)} سيرفر خام. غنصفي منهم غير 'الهربانين'...")

    # فحص 150 سيرفر في دقة وحدة
    with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
        results = list(executor.map(check_satellite_reach, unique_pool))

    # الترتيب من الأسرع للأبطأ
    valid = sorted([r for r in results if r], key=lambda x: x[0])

    with open("VIP_ELITE_SERVERS.cfg", "w") as f:
        f.write(f"# SHΔDØW ELITE EXCLUSIVE | {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"# TARGET: ASTRA - HOTBIRD - HISPASAT\n\n")
        for _, s in valid[:150]: # خذ فقط أفضل 150 سيرفر
            f.write(s + "\n")

    print(f"✅ تم بنجاح! الملف 'VIP_ELITE_SERVERS.cfg' واجد فيه {len(valid[:150])} سيرفر ناضي.")

if __name__ == "__main__":
    start_scraping()
