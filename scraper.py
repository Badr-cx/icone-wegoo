import requests, re, socket, time, concurrent.futures
from datetime import datetime
import random

# مصادر السيرفرات الحصرية
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/mueof/free-cccam/main/cccam.txt",
    "https://vipsat.net/free-cccam-server.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://clinetest.net/free_cccam.php",
    "https://fastcccam.com/free-cccam.php"
]

# قائمة بروكسيات لفك الحظر (تحديث تلقائي)
PROXY_LIST_URL = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"

def get_random_proxy():
    try:
        r = requests.get(PROXY_LIST_URL, timeout=5)
        proxies = r.text.splitlines()
        return random.choice(proxies) if proxies else None
    except:
        return None

def smart_verify(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    
    # البلاك ليست التقليدية
    forbidden = ['streamtveuropa', 'nassim', '37.60', 'ugeen', 'casacam', 'dhoom']
    if any(f in host.lower() for f in forbidden): return None

    try:
        start = time.perf_counter()
        with socket.create_connection((host, int(port)), timeout=0.8) as sock:
            # محاكاة Login
            sock.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")
            data = sock.recv(1024)
            latency = int((time.perf_counter() - start) * 1000)
            
            if data and latency < 145:
                tag = "💎VIP" if latency < 110 else "✅OK"
                return (latency, f"C: {host} {port} {user} {passwd} # {tag}_{latency}ms")
    except:
        return None

def start_stealth_mission():
    print("🕵️‍♂️ Stealth Mode Active: جاري تخطي الحماية...")
    all_raw = []
    
    proxy = get_random_proxy()
    proxies_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    with requests.Session() as session:
        session.headers.update(headers)
        for url in SOURCES:
            try:
                # محاولة السحب بالبروكسي، وإذا فشل نجرب بدونه
                target_url = f"{url}?v={time.time()}"
                r = session.get(target_url, timeout=15, verify=False, proxies=proxies_dict)
                found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                all_raw.extend(found)
            except:
                try: 
                    r = session.get(url, timeout=10, verify=False)
                    found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                    all_raw.extend(found)
                except: continue

    unique_candidates = list(set(all_raw))
    print(f"📡 Found {len(unique_candidates)} potential servers. Testing...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(smart_verify, unique_candidates))

    final_sorted = sorted([r for r in results if r], key=lambda x: x[0])

    with open("VERIFIED_CANNON.cfg", "w") as f:
        f.write(f"# SHΔDØW STEALTH | {datetime.now().strftime('%H:%M:%S')}\n\n")
        if final_sorted:
            for _, server in final_sorted[:30]:
                f.write(server + "\n")
            print(f"✅ Success! Found {len(final_sorted)} servers.")
        else:
            f.write("# No High-Speed servers found right now.")

if __name__ == "__main__":
    start_stealth_mission()
