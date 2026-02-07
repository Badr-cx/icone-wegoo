import requests, re, socket, time, concurrent.futures
from datetime import datetime

# المصادر شاملة الرابط اللي عطيتيني (بصيغة RAW)
SOURCES = [
    # الرابط ديالك (تم تحويله لـ RAW باش يقرأ الكود نيشان)
    "https://raw.githubusercontent.com/Badr-cx/icone-wegoo/main/VERIFIED_CANNON.cfg",
    # مصادر Github أخرى نشيطة (Live)
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt",
    "https://raw.githubusercontent.com/tarekzoka/free/main/cccam.txt",
    # قنوات تيليغرام (Web View)
    "https://t.me/s/Free_Cccam_Server_Daily",
    "https://t.me/s/vipsat_net",
    # مواقع (السرعة)
    "https://cccamia.com/cccamfree1/",
    "https://cccamcard.com/free-cccam-server.php"
]

def verify_server(line):
    # تنظيف السطر من أي رموز HTML أو فراغات
    line = line.strip()
    # Regex كيجبد السيرفر واخا يكون السطر فيه تعليقات # أو رموز
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    
    # فلتر للهوستات الميتة
    if any(f in host.lower() for f in ['127.0.0.1', 'nassim', 'stream']): return None

    try:
        start = time.perf_counter()
        # محاولة اتصال حقيقية بالبورت
        with socket.create_connection((host, int(port)), timeout=1.5) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            return (latency, host, port, user, passwd)
    except:
        return None

def run_scraper():
    print("🛰️  Starting Global Search (GitHub, Telegram, Web)...")
    all_raw = []
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})

    for url in SOURCES:
        try:
            r = session.get(url, timeout=10)
            # استخراج أسطر C: من وسط أي نص
            matches = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
            
            # محاولة تانية لأسطر بلا C: (لقنص السيرفرات المخفية)
            if not matches:
                extra = re.findall(r'([a-zA-Z0-9\-\.]+\s+\d+\s+[a-zA-Z0-9\-\.]+\s+[a-zA-Z0-9\-\.]+)', r.text)
                for e in extra:
                    if e.split()[1].isdigit(): matches.append(f"C: {e}")
            
            all_raw.extend(matches)
            print(f"🔎 {url.split('/')[-1]}: Found {len(matches)}")
        except: continue

    unique_list = list(set(all_raw))
    print(f"🧪 Testing {len(unique_list)} clines... please wait.")

    # فحص متوازي سريع جداً
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = [r for r in executor.map(verify_server, unique_list) if r]

    # ترتيب حسب Ping (الأسرع أولاً)
    results.sort(key=lambda x: x[0])

    if results:
        # حفظ ncam.server (لأجهزة Enigma2 و Icone)
        with open("ncam.server", "w", encoding="utf-8") as f:
            f.write(f"### GENERATED {datetime.now().strftime('%Y-%m-%d %H:%M')} ###\n")
            for i, (lat, host, port, user, passwd) in enumerate(results[:30]):
                f.write(f"\n[reader]\nlabel = Server_{i+1}_{lat}ms\nprotocol = cccam\ndevice = {host},{port}\nuser = {user}\npassword = {passwd}\ngroup = 1\n")
        
        # حفظ CCcam.cfg
        with open("CCcam.cfg", "w", encoding="utf-8") as f:
            for lat, host, port, user, passwd in results[:30]:
                f.write(f"C: {host} {port} {user} {passwd} # Ping: {lat}ms\n")
        
        print(f"✅ Mission Success! {len(results)} active servers found.")
    else:
        print("❌ All servers in these links are DEAD. You need fresh sources!")

if __name__ == "__main__":
    run_scraper()
