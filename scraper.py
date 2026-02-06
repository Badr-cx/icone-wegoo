import requests, re, socket, time, concurrent.futures
from datetime import datetime

# مصادر متنوعة باش ديما يكون الجديد
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/mueof/free-cccam/main/cccam.txt",
    "https://vipsat.net/free-cccam-server.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://clinetest.net/free_cccam.php",
    "https://fastcccam.com/free-cccam.php",
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt"
]

def clean_verify(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    
    # 🚫 البلاك ليست المحدثة (ممنوع الغلط)
    # زدنا cam2.cline.wf و cam1 و كاع دوك اللي مخدامينش
    forbidden = [
        'streamtveuropa', 'nassim', '37.60.251.20', 'visit', 
        'ugeen', 'casacam', 'dhoom', 'cline.wf', 'giize'
    ]
    
    if any(f in host.lower() for f in forbidden): 
        return None

    try:
        start = time.perf_counter()
        # فحص الاتصال (TCP Check)
        with socket.create_connection((host, int(port)), timeout=1.2) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            
            # وسعنا الـ Ping شوية لـ 280ms باش الملف ديما يلقى ما يحط
            if latency < 280:
                tag = "⚡FAST" if latency < 120 else "✅LIVE"
                return (latency, f"C: {host} {port} {user} {passwd} # {tag}_{latency}ms")
    except:
        return None

def run_mission():
    print("🚀 Target: Fresh & Real Servers...")
    all_raw = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    with requests.Session() as s:
        s.headers.update(headers)
        for url in SOURCES:
            try:
                # Cache busting باش مايجيبش القديم
                r = s.get(f"{url}?v={time.time()}", timeout=10, verify=False)
                matches = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                all_raw.extend(matches)
            except: continue

    unique_list = list(set(all_raw))
    print(f"📡 Found {len(unique_list)} candidates. Testing...")

    # فحص سريع بـ 100 خيط (Threads)
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(clean_verify, unique_list))

    # الترتيب حسب السرعة
    final = sorted([r for r in results if r], key=lambda x: x[0])

    with open("VERIFIED_CANNON.cfg", "w") as f:
        f.write(f"# 🛡️ CLEAN ELITE LIST | {datetime.now().strftime('%H:%M:%S')}\n\n")
        if final:
            for _, server in final[:50]: # توب 50 سيرفر "منقي"
                f.write(server + "\n")
            print(f"✅ DONE! Found {len(final)} working servers.")
        else:
            f.write("# No real servers found right now. Retrying next cycle...")
            print("❌ No servers passed the filter.")

if __name__ == "__main__":
    run_mission()
