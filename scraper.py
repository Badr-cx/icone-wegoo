import requests, re, socket, time, concurrent.futures
from datetime import datetime

# 1. المصادر "الحية" (Live Sources) اللي خدامة فهاد اللحظة
SOURCES = [
    # الرابط ديالك اللي تحديث قبل قليل (استعمال v=timestamp لتجاوز الكاش)
    f"https://raw.githubusercontent.com/Badr-cx/icone-wegoo/main/VERIFIED_CANNON.cfg?v={time.time()}",
    # قنوات تيليغرام هي "المنبع" الحقيقي فـ 2026
    "https://t.me/s/Free_Cccam_Server_Daily",
    "https://t.me/s/vipsat_net",
    "https://t.me/s/smart_cccam",
    "https://t.me/s/cccamfree3",
    # روابط Github ديال "العمالقة" اللي كيتحدثوا أوتوماتيكياً
    "https://raw.githubusercontent.com/mueof/free-cccam/main/cccam.txt",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt"
]

def verify_server(line):
    """ فحص السيرفر واش حي دابا (Live Check) """
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    try:
        start = time.perf_counter()
        # محاولة اتصال سريعة (أقل من 1.5 ثانية)
        with socket.create_connection((host, int(port)), timeout=1.5) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            return (latency, host, port, user, passwd)
    except:
        return None

def run_scraper():
    print(f"📅 التاريخ الحالي: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📡 جاري سحب سيرفرات 'النخبة' (Elite Servers)...")
    
    all_raw = []
    session = requests.Session()
    # أهم حاجة فـ 2026 هي الـ User-Agent باش الموقع ما يسدش عليك
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36'
    })

    for url in SOURCES:
        try:
            # طلب الصفحة مع منع الكاش
            r = session.get(url, timeout=10)
            # استخراج الأسطر اللي فيها C:
            matches = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
            
            # إذا الموقع مخبي السيرفرات وسط HTML (بحال تيليغرام)
            if not matches:
                extra = re.findall(r'([a-zA-Z0-9\-\.]+\s+\d+\s+[a-zA-Z0-9\-\.]+\s+[a-zA-Z0-9\-\.]+)', r.text)
                for e in extra:
                    if e.split()[1].isdigit(): matches.append(f"C: {e}")
            
            all_raw.extend(matches)
            print(f"✅ {url.split('/')[-1][:15]}... جاب {len(matches)} سيرفر")
        except: continue

    unique_list = list(set(all_raw))
    print(f"🔍 جاري فحص {len(unique_list)} سيرفر... جيب قهوة!")

    # فحص 150 سيرفر فدقة وحدة باش نساليوا دغيا
    with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
        results = [r for r in executor.map(verify_server, unique_list) if r]

    # ترتيب من الأسرع (أقل Ping)
    results.sort(key=lambda x: x[0])

    if results:
        # حفظ الملف ncam.server
        with open("ncam.server", "w", encoding="utf-8") as f:
            f.write(f"### UPDATED: {datetime.now().strftime('%Y-%m-%d %H:%M')} ###\n")
            for i, (lat, host, port, user, passwd) in enumerate(results[:50]):
                f.write(f"\n[reader]\nlabel = SRV_{i+1}_{lat}ms\nprotocol = cccam\ndevice = {host},{port}\nuser = {user}\npassword = {passwd}\ngroup = 1\nccckeepalive = 1\n")
        
        # حفظ الملف CCcam.cfg
        with open("CCcam.cfg", "w", encoding="utf-8") as f:
            for lat, host, port, user, passwd in results[:50]:
                f.write(f"C: {host} {port} {user} {passwd} # {lat}ms\n")
        
        print(f"✨ مبروك! لقينا {len(results)} سيرفر شغال طازج.")
        print("📂 الملفات CCcam.cfg و ncam.server واجدة.")
    else:
        print("😭 والو! السيرفرات اللي كاينين دابا ميتين أو محظورين. جرب مورا 10 دقايق.")

if __name__ == "__main__":
    run_scraper()
