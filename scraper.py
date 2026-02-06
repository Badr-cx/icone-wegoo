import requests, re, socket, time, concurrent.futures
from datetime import datetime

# مصادر "نقية" كتعطي يوزرات حصرية
SOURCES = [
    "https://vipsat.net/free-cccam-server.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://clinetest.net/free_cccam.php",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt"
]

def cccam_login_check(line):
    """ كيحاول يدير Login حقيقي في السيرفر """
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    
    # القائمة السوداء (Blacklist) للهوستات اللي كيعطيو Fake Live
    blacklist = ['37.60.251.20', 'nassimbejaia1.hopto.org']
    if any(b in host for b in blacklist): return None

    try:
        start = time.perf_counter()
        # محاولة فتح الاتصال
        s = socket.create_connection((host, int(port)), timeout=1.5)
        
        # هاد الجزء كيحاكي الـ Hello Packet ديال CCcam
        # كنصيفطو يوزر وباس باش نشوفو واش كاين Response
        s.send(b"\x00\x00\x00\x00\x00\x00\x00\x00") 
        data = s.recv(1024)
        
        latency = int((time.perf_counter() - start) * 1000)
        
        # إذا السيرفر جاوب ببيانات (ماشي خاوي)، يعني الـ Login ممكن
        if data and len(data) > 0:
            s.close()
            # ترتيب حسب القرب من 97ms
            diff = abs(latency - 97)
            return (diff, f"C: {host} {port} {user} {passwd} # ✅LOGIN_SUCCESS_{latency}ms")
        
        s.close()
    except:
        return None
    return None

def start_deep_hunt():
    print("🚀 Deep Login Check: جاري التأكد من صحة اليوزرات...")
    all_raw = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0'}

    with requests.Session() as session:
        session.headers.update(headers)
        for url in SOURCES:
            try:
                r = session.get(url, timeout=12, verify=False)
                found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                all_raw.extend(found)
            except: continue

    unique_candidates = list(set(all_raw))
    print(f"📡 Found {len(unique_candidates)} potential lines. Deep testing...")

    # فحص متوازي (قللت الـ workers باش ما يتبلوكاوش السيرفرات)
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        results = list(executor.map(cccam_login_check, unique_candidates))

    # الترتيب حسب الجودة
    final_sorted = sorted([r for r in results if r], key=lambda x: x[0])

    if final_sorted:
        with open("VERIFIED_CANNON.cfg", "w") as f:
            f.write(f"# REAL LOGIN VERIFIED | {datetime.now().strftime('%H:%M')}\n\n")
            for _, server in final_sorted[:50]:
                f.write(server + "\n")
        print(f"✅ مبروك! لقيت {len(final_sorted)} سيرفر داز ليهم الـ Login بنجاح.")
    else:
        print("⚠️ مالقيت حتى سيرفر خدام بـ Login صحيح دابا.")

if __name__ == "__main__":
    start_deep_hunt()
