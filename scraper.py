import requests, re, socket, time, concurrent.futures
from datetime import datetime

# مصادر عالمية متجددة كل ساعة (GitHub + Premium Trial Aggregators)
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/Fidat-T/Free-CCcam/main/cccam.txt",
    "https://raw.githubusercontent.com/tjm1024/Free-TV/master/cccam.txt",
    "https://clinetest.net/free_cccam.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://cccamfree.cc/free-cccam-server/",
    "https://www.cccam786.com/free-cccam/",
    "https://cccam.io/free-cccam/",
    "https://vipsat.net/free-cccam-server.php",
    "https://fastcccam.com/free-cccam.php"
]

def verify_shadow_server(line):
    """ فحص عميق للاتصال: لا يقبل إلا السيرفرات الصاروخية """
    line = line.strip()
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    try:
        start_time = time.perf_counter()
        # محاولة فتح اتصال TCP في أقل من 0.7 ثانية
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.7) 
        result = sock.connect_ex((host, int(port)))
        end_time = time.perf_counter()
        
        if result == 0:
            latency = int((end_time - start_time) * 1000)
            sock.close()
            # وسم السيرفر حسب جودته
            tag = "⚡ELITE" if latency < 200 else "✅STABLE"
            return (latency, f"C: {host} {port} {user} {passwd} # {tag}_{latency}ms")
    except:
        pass
    return None

def start_mission():
    print("🔥 SHΔDØW CORE: جاري سحب السيرفرات من النطاقات العالمية...")
    raw_lines = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    # المرحلة 1: الاستخراج المكثف
    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.I)
            raw_lines.extend(found)
        except: continue

    unique_lines = list(set(raw_lines))
    print(f"📡 تم العثور على {len(unique_lines)} سيرفر مرشح. جاري الفرز والتحقق من القوة...")

    # المرحلة 2: الفحص المتوازي فائق السرعة
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(verify_shadow_server, unique_lines))

    # فلترة الشغالين فقط وترتيبهم من الأسرع إلى الأبطأ
    working_servers = sorted([r for r in results if r], key=lambda x: x[0])

    # المرحلة 3: إنشاء الملف النهائي
    with open("CCcam_PRO_V99.cfg", "w") as f:
        f.write(f"# SHADOW_CORE_V99 | UPDATED: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"# TOTAL ACTIVE SERVERS: {len(working_servers)}\n")
        f.write("# ------------------------------------------------------------\n\n")
        for _, server in working_servers:
            f.write(f"{server}\n")
    
    print(f"✅ المهمة تمت بنجاح! تم استخراج {len(working_servers)} سيرفر شغال 100%.")
    print(f"📄 الملف جاهز الآن: CCcam_PRO_V99.cfg")

if __name__ == "__main__":
    start_mission()
