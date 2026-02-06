import requests, re, socket, time, concurrent.futures
from datetime import datetime

# روابط "الهمزة" (Private API & GitHub Scrapers)
# هاد الروابط كتركز على السيرفرات اللي يلاه ترفعوا
SOURCES = [
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt",
    "https://raw.githubusercontent.com/freetv-org/cccam/main/cccam.txt",
    "https://raw.githubusercontent.com/monosat/cccam/main/cccam.txt",
    "https://raw.githubusercontent.com/ndnd7/cccam/main/cccam.txt",
    # هاد الرابط كيجيب "التسريبات" من منتديات إسبانية وألمانية
    "https://api.github.com/search/code?q=extension:cfg+C:+Astra&sort=indexed&order=desc"
]

def final_verify(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    
    # القائمة السوداء اللي هضرنا عليها (ممنوع الغلط)
    forbidden = ['streamtveuropa', 'nassim', '37.60', 'ugeen', 'casacam', 'dhoom', 'kinghd', 'visit']
    if any(f in host.lower() or f in user.lower() for f in forbidden):
        return None

    try:
        start = time.perf_counter()
        # فحص الاتصال الحقيقي
        with socket.create_connection((host, int(port)), timeout=0.6) as s:
            s.send(b"\x00\x00\x00\x00\x00\x00\x00\x00") 
            data = s.recv(1024)
            latency = int((time.perf_counter() - start) * 1000)
            
            # الهدف هو Astra: لازم Ping تحت 100ms
            if data and latency < 100:
                return (latency, f"C: {host} {port} {user} {passwd} # 💎ASTRA_ELITE_{latency}ms")
    except:
        return None

def start_mission():
    print("🕵️‍♂️ Astra Hunt: Searching for Fresh Leaks...")
    all_raw = []
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.v3+json'}
    
    with requests.Session() as session:
        for url in SOURCES:
            try:
                # Cache Busting (باش ما يعطيكش داكشي القديم)
                target = f"{url}&v={time.time()}" if '?' in url else f"{url}?v={time.time()}"
                r = session.get(target, headers=headers, timeout=10)
                
                # إذا كان الرابط هو GitHub API كنخرجو الداتا بطريقة مختلفة
                if "api.github.com" in url:
                    items = r.json().get('items', [])
                    for item in items[:10]:
                        raw_res = session.get(item['html_url'].replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/'))
                        matches = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', raw_res.text, re.I)
                        all_raw.extend(matches)
                else:
                    found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                    all_raw.extend(found)
            except: continue

    unique_list = list(set(all_raw))
    print(f"📡 Found {len(unique_list)} candidates. Testing for Astra Quality...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(final_verify, unique_list))

    final = sorted([r for r in results if r], key=lambda x: x[0])

    with open("VERIFIED_CANNON.cfg", "w") as f:
        f.write(f"# 🇪🇸 ASTRA FRESH ELITE | {datetime.now().strftime('%H:%M:%S')}\n\n")
        if final:
            for _, s in final[:15]: # كناخدو غير أحسن 15 سيرفر طيارة
                f.write(s + "\n")
            print(f"✅ Mission Success: {len(final)} Fresh Servers found.")
        else:
            f.write("# No High-Speed Astra Servers found right now.")
            print("⚠️ No elite servers matched the < 100ms criteria.")

if __name__ == "__main__":
    start_mission()
