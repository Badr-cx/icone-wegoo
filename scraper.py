import requests, re, socket, time, concurrent.futures
from datetime import datetime

# 1. المصادر المتنوعة (مواقع + قنوات تيليغرام)
SOURCES = [
    # مواقع (جديدة وقوية)
    "https://cccamcard.com/free-cccam-server.php",
    "https://cccamia.com/cccamfree1/",
    "https://cccam.net/freecccam",
    "https://cccam-premium.pro/free-cccam/",
    "https://vipsat.net/free-cccam-server.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://www.cccam-free.com/",
    "https://free.cccam-premium.pro/",
    # قنوات تيليغرام (عن طريق الويب - Web Preview)
    "https://t.me/s/Free_Cccam_Server_Daily",
    "https://t.me/s/cccam_sharing_tv",
    "https://t.me/s/vipsat_net",
    "https://t.me/s/smart_cccam",
    # Github (الهمزة ديال أوروبا والصين)
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt"
]

def verify_server(line):
    """ فحص السيرفر واش حي وسريع """
    line = line.strip().replace('</td>', ' ').replace('<br>', ' ')
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    
    # حظر السيرفرات الوهمية والهوستات اللي كتثقل السكين
    if any(f in host.lower() for f in ['127.0.0.1', 'localhost', 'nassim', 'stream']): return None

    try:
        start = time.perf_counter()
        with socket.create_connection((host, int(port)), timeout=1.8) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            # قبول السيرفرات اللي تحت 450ms
            if latency < 450:
                return (latency, host, port, user, passwd)
    except:
        return None

def run_scraper():
    print(f"🚀 Mission Started: Scraping Web & Telegram ({len(SOURCES)} sources)...")
    all_raw = []
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    })

    for url in SOURCES:
        try:
            r = session.get(url, timeout=15)
            # تنظيف الـ HTML باش ميغلطش الـ Regex
            text_cleaned = re.sub('<[^<]+?>', ' ', r.text)
            
            # البحث عن صيغة C: التقليدية
            matches = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', text_cleaned, re.I)
            
            # إذا كان السيرفر محطوط بلا "C:" (غالباً فتيليغرام)
            if not matches:
                extra = re.findall(r'([a-zA-Z0-9\-\.]+\s+\d+\s+[a-zA-Z0-9\-\.]+\s+[a-zA-Z0-9\-\.]+)', text_cleaned)
                for e in extra:
                    parts = e.split()
                    if parts[1].isdigit(): # كيتأكد بلي البورت رقم
                        matches.append(f"C: {e}")
            
            all_raw.extend(matches)
            print(f"📡 {url.split('/')[-1]}: Found {len(matches)}")
        except:
            continue

    # حيد المعاود
    unique_list = list(set(all_raw))
    print(f"🧪 Testing {len(unique_list)} unique clines... Hang on!")

    # فحص 120 سيرفر فدقة وحدة (سرعة خيالية)
    with concurrent.futures.ThreadPoolExecutor(max_workers=120) as executor:
        results = [r for r in executor.map(verify_server, unique_list) if r]

    # الترتيب حسب السرعة (Ping)
    results.sort(key=lambda x: x[0])

    if results:
        # 1. ملف ncam.server
        with open("ncam.server", "w", encoding="utf-8") as f:
            f.write(f"### NCAM GENERATED | {datetime.now().strftime('%H:%M:%S')} | {len(results)} Active ###\n")
            for i, (lat, host, port, user, passwd) in enumerate(results[:50]): # أحسن 50 سيرفر
                f.write(f"\n[reader]\nlabel = Server_{i+1}_{lat}ms\nprotocol = cccam\ndevice = {host},{port}\nuser = {user}\npassword = {passwd}\ngroup = 1\ncccversion = 2.3.2\nccckeepalive = 1\n")
        
        # 2. ملف CCcam.cfg
        with open("CCcam.cfg", "w", encoding="utf-8") as f:
            for lat, host, port, user, passwd in results[:50]:
                f.write(f"C: {host} {port} {user} {passwd} # Ping: {lat}ms\n")
        
        print(f"✅ Mission Accomplished! Found {len(results)} live servers.")
        print(f"📂 Saved to ncam.server & CCcam.cfg")
    else:
        print("❌ No active servers found. Check your internet connection!")

if __name__ == "__main__":
    run_scraper()
