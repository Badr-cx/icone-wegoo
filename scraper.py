import requests, re, socket, time, concurrent.futures
from datetime import datetime

CHECKER_SOURCES = [
    "https://vipsat.net/free-cccam-server.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://clinetest.net/free_cccam.php",
    "https://fastcccam.com/free-cccam.php",
    "https://cccam786.com/free-cccam/",
    "https://www.cccam2.com/free-cccam-server.php",
    "https://raw.githubusercontent.com/mueof/free-cccam/main/cccam.txt",
    "http://www.cccamfree.cc/free-cccam-server/",
]

def intense_check(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    host, port, user, passwd = match.groups()
    if any(x in host for x in ['37.60.251.20', 'streamtveuropa']): return None
    try:
        start = time.perf_counter()
        with socket.create_connection((host, int(port)), timeout=0.3) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            return (latency, f"C: {host} {port} {user} {passwd} # VERIFIED_{latency}ms")
    except:
        return None

def start_hunting():
    print("Starting Hunt... جاري البحث")
    verified_pool = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    with requests.Session() as session:
        for url in CHECKER_SOURCES:
            try:
                r = session.get(url, timeout=10, verify=False)
                found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                verified_pool.extend(found)
            except: continue

    unique_list = list(set(verified_pool))
    # هاد السطر هو اللي كان فيه المشكل (75)
    print(f"Filtering {len(unique_list)} lines... جاري التصفية")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(intense_check, unique_list))

    final_elite = sorted([r for r in results if r], key=lambda x: x[0])

    if final_elite:
        with open("VERIFIED_CANNON.cfg", "w") as f:
            f.write(f"# SHΔDØW VERIFIED | {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            for _, server in final_elite[:100]:
                f.write(server + "\n")
        print("Success! الملف واجد")
    else:
        # هاد السطر هو اللي كان فيه المشكل (73)
        print("Empty: المواقع ناشفة حاليا")

if __name__ == "__main__":
    start_hunting()
