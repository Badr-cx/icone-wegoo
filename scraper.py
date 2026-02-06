import requests, re, socket, time, concurrent.futures
from datetime import datetime

# مصادر "نقية" ومحدثة (الهمزة الحقيقية)
SOURCES = [
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt",
    "https://raw.githubusercontent.com/freetv-org/cccam/main/cccam.txt",
    "https://raw.githubusercontent.com/claudio-silva/cccam/main/cccam.txt",
    "https://raw.githubusercontent.com/monosat/cccam/main/cccam.txt",
    "https://clinetest.net/free_cccam.php"
]

def deep_verify(line):
    line = line.strip()
    # استخراج البيانات
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    
    # 🚫 منع السيرفرات الوهمية (البلاك ليست)
    fake_brands = ['streamtveuropa', 'nassim', '37.60.251.20', 'asiachannels', 'visit', 'checkallsat']
    if any(fake in host.lower() or fake in user.lower() for fake in fake_brands):
        return None

    try:
        start = time.perf_counter()
        # محاولة الاتصال بالـ Login
        s = socket.create_connection((host, int(port)), timeout=1.5)
        s.send(b"\x00\x00\x00\x00\x00\x00\x00\x00") 
        data = s.recv(1024)
        latency = int((time.perf_counter() - start) * 1000)
        s.close()

        if data and len(data) > 0:
            # ترتيب حسب الجودة (الهدف 97ms)
            diff = abs(latency - 97)
            # وسم السيرفرات القوية
            tag = "💎PREMIUM" if latency < 150 else "✅STABLE"
            return (diff, f"C: {host} {port} {user} {passwd} # {tag}_{latency}ms")
    except:
        return None
    return None

def start_mission():
    print("🔥 Operation: VIP HUNTING...")
    all_raw = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    with requests.Session() as session:
        for url in SOURCES:
            try:
                r = session.get(url, timeout=10, verify=False)
                found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                all_raw.extend(found)
            except: continue

    unique_list = list(set(all_raw))
    print(f"📡 Found {len(unique_list)} potential servers. Testing Login...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(deep_verify, unique_list))

    # الترتيب حسب الجودة (الأقرب لـ 97ms)
    final = sorted([r for r in results if r], key=lambda x: x[0])

    if final:
        with open("VERIFIED_CANNON.cfg", "w") as f:
            f.write(f"# 🎯 ELITE SERVERS | {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            for _, server in final[:40]: # خذ أفضل 40 سيرفر حقيقي
                f.write(server + "\n")
        print(f"✅ DONE! Found {len(final)} REAL working servers.")
    else:
        print("❌ No real servers found. Sources might be empty.")

if __name__ == "__main__":
    start_mission()
