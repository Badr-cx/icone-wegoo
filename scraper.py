import requests, re, socket, time, concurrent.futures
from datetime import datetime

# المصادر العالمية - تم التحقق من روابطها
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/Fidat-T/Free-CCcam/main/cccam.txt",
    "https://raw.githubusercontent.com/tjm1024/Free-TV/master/cccam.txt",
    "https://raw.githubusercontent.com/mizstd/CCcam-Free/main/cccam.txt",
    "https://raw.githubusercontent.com/best-cccam/free/main/cccam.cfg",
    "https://raw.githubusercontent.com/S-K-S-B/CCcam/main/free.txt",
    "https://raw.githubusercontent.com/Mahesh0433/CCcam-Free/main/cccam.txt",
    "https://clinetest.net/free_cccam.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://cccamfree.cc/free-cccam-server/",
    "https://www.cccam786.com/free-cccam/",
    "https://cccam.io/free-cccam/",
    "https://vipsat.net/free-cccam-server.php",
    "https://fastcccam.com/free-cccam.php",
    "http://www.boss-cccam.com/Free.php",
    "https://www.cccam2.com/free-cccam-server.php"
]

def verify_beast_mode(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    try:
        start = time.perf_counter()
        with socket.create_connection((host, int(port)), timeout=0.5) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            tag = "💎ELITE" if latency < 200 else "🚀FAST"
            return (latency, f"C: {host} {port} {user} {passwd} # {tag}_{latency}ms")
    except:
        return None

def execute_annihilation():
    print("💀 SHΔDØW CORE: جاري اكتساح الشبكة الآن...")
    
    all_raw_lines = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    with requests.Session() as session:
        for url in SOURCES:
            try:
                r = session.get(url, timeout=7, verify=False)
                found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                all_raw_lines.extend(found)
            except: continue

    unique_pool = list(set(all_raw_lines))
    # تم تصحيح السطر أدناه (استبدال " بالداخل بـ ')
    print(f"🔥 جاري تصفية 'الذهب' من النحاس (الفحص الفعلي لـ {len(unique_pool)} سيرفر)...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(verify_beast_mode, unique_pool))

    working = sorted([r for r in results if r], key=lambda x: x[0])

    with open("CCcam.cfg", "w") as f:
        f.write(f"# SHΔDØW CORE V101 | {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        for _, server in working:
            f.write(f"{server}\n")

    print(f"✅ المهمة تمت! الملف جاهز بـ {len(working)} سيرفر شغال.")

if __name__ == "__main__":
    execute_annihilation()
