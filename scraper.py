import requests, re, socket, time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# مصادر قوية لكل الأقمار (Astra, Hotbird, Hispasat, Eutelsat)
SOURCES = [
    "https://vipsat.net/free-cccam-server.php",
    "https://cccamprime.com/free-cccam/",
    "https://cccamspot.com/free-cccam/",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://clinetest.net/free_cccam.php",
    "https://cccamfree.cc/free-cccam-server/",
    "https://www.cccam786.com/free-cccam/",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://iptv-org.github.io/iptv/provinces/ma.m3u" # مصدر إضافي أحياناً يحتوي سطور
]

def check_line(line):
    line = line.strip()
    m = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not m: return None
    h, p, u, pw = m.groups()
    try:
        start = time.time()
        # فحص جودة السيرفر (0.6 ثانية كحد أقصى لضمان الثبات)
        with socket.create_connection((h, int(p)), timeout=0.6):
            ms = int((time.time() - start) * 1000)
            return (ms, f"C: {h} {p} {u} {pw} # Full_Sat_{ms}ms")
    except: return None

def main():
    raw_lines = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10, headers=headers, verify=False)
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.I)
            raw_lines.extend(found)
        except: continue

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(check_line, list(set(raw_lines))))
    
    # ترتيب: الأسرع هو الأول
    active_servers = sorted([r for r in results if r], key=lambda x: x[0])

    with open("CCcam.cfg", "w") as f:
        f.write(f"# FULL SATELLITE UPDATE: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("# Astra | Hotbird | Hispasat | Nilesat\n\n")
        # نأخذ أفضل 100 سيرفر شغال لضمان فتح كل الباقات
        for _, line in active_servers[:100]:
            f.write(f"{line}\n")

if __name__ == "__main__":
    main()
