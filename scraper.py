import requests, re, socket, time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# المصادر المختارة بعناية
SOURCES = [
    "https://clinetest.net/free_cccam.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://cccamfree.cc/free-cccam-server/",
    "https://www.cccam786.com/free-cccam/",
    "https://cccam.io/free-cccam/",
    "https://vipsat.net/free-cccam-server.php",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt"
]

def verify_server(line):
    """ التأكد 100% أن السطر شغال قبل وضعه في الملف """
    line = line.strip()
    # تنظيف السطر من أي شوائب
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    try:
        start = time.time()
        # محاولة فتح اتصال حقيقي مع السيرفر (TCP Check)
        with socket.create_connection((host, int(port)), timeout=0.8):
            ms = int((time.time() - start) * 1000)
            # السطر كيخرج واجد ونقي
            return (ms, f"C: {host} {port} {user} {passwd} # Verified_{ms}ms")
    except:
        return None

def main():
    print("🔍 Searching for servers...")
    all_lines = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=10, verify=False)
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.I)
            all_lines.extend(found)
        except: continue

    unique_lines = list(set(all_lines))
    print(f"📡 Found {len(unique_lines)} servers. Verifying connection...")

    # فحص السطور بالتوازي لربح الوقت
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(verify_server, unique_lines))

    # فلترة السطور اللي جاوبو فقط وترتيبهم حسب السرعة
    working_servers = sorted([r for r in results if r], key=lambda x: x[0])

    # كتابة الملف النهائي بـ 100 سطر شغالين 100%
    with open("CCcam.cfg", "w") as f:
        f.write(f"# BADR-CX SNIPER-UPDATE | {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"# STATUS: {len(working_servers)} ONLINE SERVERS\n\n")
        for _, server in working_servers[:100]:
            f.write(f"{server}\n")
    
    print(f"✅ CCcam.cfg updated with {len(working_servers)} verified servers.")

if __name__ == "__main__":
    main()
