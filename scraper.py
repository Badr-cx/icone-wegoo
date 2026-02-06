import requests, re, socket, time, concurrent.futures
from datetime import datetime
import random

SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/mueof/free-cccam/main/cccam.txt",
    "https://vipsat.net/free-cccam-server.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://clinetest.net/free_cccam.php",
    "https://fastcccam.com/free-cccam.php"
]

def smart_verify(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    host, port, user, passwd = match.groups()
    try:
        start = time.perf_counter()
        with socket.create_connection((host, int(port)), timeout=0.6) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            diff = abs(latency - 97)
            return (diff, latency, f"C: {host} {port} {user} {passwd} # LATENCY_{latency}ms")
    except:
        return None

def start_mission():
    print("Starting Stealth Scan...")
    all_raw = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    with requests.Session() as session:
        session.headers.update(headers)
        for url in SOURCES:
            try:
                r = session.get(url, timeout=15, verify=False)
                found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                all_raw.extend(found)
            except: continue

    unique_candidates = list(set(all_raw))
    print(f"Found {len(unique_candidates)} lines. Verifying...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(smart_verify, unique_candidates))

    final_sorted = sorted([r for r in results if r], key=lambda x: x[0])

    if final_sorted:
        with open("VERIFIED_CANNON.cfg", "w") as f:
            f.write(f"# TARGET 97ms | {datetime.now().strftime('%H:%M')}\n\n")
            for _, lat, server in final_sorted[:100]:
                f.write(server + "\n")
        print("Success: VERIFIED_CANNON.cfg created.")
    else:
        print("No servers found.")

if __name__ == "__main__":
    start_mission()
