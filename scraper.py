import requests, re, socket, time, concurrent.futures, base64
from datetime import datetime

# كلمات البحث في GitHub لجلب أحدث السيرفرات "دابا دابا"
GITHUB_SEARCH_QUERIES = [
    'path:*.txt "C:" extension:txt',
    'path:*.cfg "C:" extension:cfg',
    '"C:" filename:cccam.txt',
    '"C:" filename:cccam.cfg'
]

def cccam_verify(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    host, port, user, passwd = match.groups()

    # بلاك ليست قوية باش ميبقاش يبرزطك داكشي اللي مخدامش
    bad = ['streamtveuropa', 'nassim', '37.60.251.20', 'ugeen', 'casacam', 'giize', 'dhoom']
    if any(b in host.lower() for b in bad): return None

    try:
        start = time.perf_counter()
        s = socket.create_connection((host, int(port)), timeout=0.8)
        s.send(b"\x00\x00\x00\x00\x00\x00\x00\x00") 
        data = s.recv(1024)
        latency = int((time.perf_counter() - start) * 1000)
        s.close()
        
        # شرط السرعة: لازم يكون Ping طيارة (تحت 110ms) باش يخدم Astra
        if data and latency < 110:
            return (latency, f"C: {host} {port} {user} {passwd} # 🔥FRESH_HIT_{latency}ms")
    except:
        return None

def fetch_from_github():
    print("🔍 Searching GitHub for fresh leaks...")
    headers = {"Accept": "application/vnd.github.v3+json"}
    found_lines = []
    
    for query in GITHUB_SEARCH_QUERIES:
        try:
            # كنقلبو على الملفات اللي تبدلو مؤخراً (sort:indexed)
            search_url = f"https://api.github.com/search/code?q={query}&sort=indexed&order=desc"
            r = requests.get(search_url, headers=headers, timeout=10)
            items = r.json().get('items', [])
            
            for item in items[:5]: # كناخدو غير أحدث 5 ملفات
                raw_url = item['html_url'].replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
                res = requests.get(raw_url, timeout=5)
                matches = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', res.text, re.I)
                found_lines.extend(matches)
        except: continue
    return list(set(found_lines))

def main():
    print("🚀 Operation: REAL-TIME HUNTING...")
    
    # 1. جلب من GitHub (أحدث التسريبات)
    fresh_lines = fetch_from_github()
    
    # 2. جلب من المصادر التقليدية كاحتياط
    # (تقدر تزيد الروابط اللي عندك هنا)
    
    print(f"📡 Found {len(fresh_lines)} lines to test.")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(cccam_verify, fresh_lines))

    final = sorted([r for r in results if r], key=lambda x: x[0])

    if final:
        with open("VERIFIED_CANNON.cfg", "w") as f:
            f.write(f"# 🔥 LIVE FREESERVERS | {datetime.now().strftime('%H:%M:%S')}\n\n")
            for _, s in final[:15]: # خذ فقط التوب 15 اللي خدامين مية في المية
                f.write(s + "\n")
        print(f"✅ Mission Success! {len(final)} Fresh servers found.")
    else:
        print("❌ Nothing fresh found right now. Retry in 2 minutes.")

if __name__ == "__main__":
    main()
