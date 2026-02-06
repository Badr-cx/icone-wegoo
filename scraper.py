import requests, re, socket, time, concurrent.futures
from datetime import datetime

# Direct sources for cleaner results
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/mueof/free-cccam/main/cccam.txt",
    "https://vipsat.net/free-cccam-server.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://clinetest.net/free_cccam.php",
    "https://fastcccam.com/free-cccam.php"
]

def verify_server(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    host, port, user, passwd = match.groups()
    try:
        start = time.perf_counter()
        with socket.create_connection((host, int(port)), timeout=0.5) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            diff = abs(latency - 97)
            tag = "TARGET_97" if diff < 20 else "LIVE"
            return (diff, f"C: {host} {port} {user} {passwd} # {tag}_{latency}ms")
    except:
        return None

def start():
    print("Mission started...")
    raw_lines = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    with requests.Session() as session:
        for url in SOURCES:
            try:
                r = session.get(url, timeout=10, verify=False)
                found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                raw_lines.extend(found)
            except: continue

    unique = list(set(raw_lines))
    print(f"Found {len(unique)} candidates. Checking...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(verify_server, unique))

    final = sorted([r for r in results if r], key=lambda x: x[0])

    if final:
        with open("VERIFIED_CANNON.cfg", "w") as f:
            f.write(f"# UPDATED: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            for _, s in final[:100]:
                f.write(s + "\n")
        print("Success: File saved.")
    else:
        print("No live servers found.")

if __name__ == "__main__":
    start()
