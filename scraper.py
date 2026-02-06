import requests, re, socket, time, concurrent.futures
from datetime import datetime

# مصادر كتحط سيرفرات من نوع mytvworld و vipsat و cccamia
# هادو هوما اللي كيجيبو السيرفرات اللي طلبتي
PREMIUM_SOURCES = [
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://vipsat.net/free-cccam-server.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://clinetest.net/free_cccam.php",
    "https://www.cccam2.com/free-cccam-server.php",
    "https://cccam786.com/free-cccam/",
    "http://www.cccamfree.cc/free-cccam-server/",
    "https://fastcccam.com/free-cccam.php"
]

def check_server(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()

    # كلمات دلالية للسيرفرات اللي بغيتي (Elite Targets)
    premium_keywords = ['mytvworld', 'gold', 'sky', 'vip', 'premium', 'king']
    is_premium = any(key in host.lower() for key in premium_keywords)

    try:
        start = time.perf_counter()
        # فحص فائق السرعة
        with socket.create_connection((host, int(port)), timeout=0.3) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            
            # إذا كان السيرفر من النوع اللي طلبتي، كنعطيوه أولوية في الترتيب
            rank = 0 if is_premium else latency
            tag = "🌟PREMIUM" if is_premium else "✅LIVE"
            
            return (rank, f"C: {host} {port} {user} {passwd} # {tag}_{latency}ms")
    except:
        return None

def main_hunt():
    print("🎯 Target Locked: البحث عن سيرفرات MyTVWorld وأشباهها...")
    
    all_lines = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0'}

    with requests.Session() as session:
        session.headers.update(headers)
        for url in PREMIUM_SOURCES:
            try:
                # تفعيل verify=False لتجاوز مشاكل الشهادات في المواقع
                r = session.get(url, timeout=10, verify=False)
                found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                all_lines.extend(found)
            except: continue

    unique_list = list(set(all_lines))
    print(f"📡 لقيت {len(unique_list)} سطر. جاري الفرز لاستخراج الذهب...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(check_server, unique_list))

    # الترتيب: السيرفرات اللي فيها كلمات (gold, mytvworld...) هي اللولة
    sorted_results = sorted([r for r in results if r], key=lambda x: x[0])

    if sorted_results:
        with open("VERIFIED_CANNON.cfg", "w") as f:
            f.write(f"# SHΔDØW TARGETED HITS | {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            for _, server in sorted_results[:80]:
                f.write(server + "\n")
        print(f"✅ المهمة تمت! الملف فيه {len(sorted_results)} سيرفر واجد.")
    else:
        print("❌ مالقيتش سيرفرات بهاد المواصفات دابا. جرب من بعد 15 دقيقة.")

if __name__ == "__main__":
    main_hunt()
