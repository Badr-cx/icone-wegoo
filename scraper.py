import requests, re, socket, time, concurrent.futures
from datetime import datetime

# مصادر "بريما" وسيرفرات مدفوعة مؤقتة (Trial/Paid Servers)
VIP_SOURCES = [
    "https://raw.githubusercontent.com/mueof/free-cccam/main/cccam.txt",
    "https://vipsat.net/free-cccam-server.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://clinetest.net/free_cccam.php",
    "https://fastcccam.com/free-cccam.php",
    "https://cccam786.com/free-cccam-servers/",
    "http://www.clinetest.net/free_cccam.php",
    "http://www.cccam-free.com/",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt"
]

def vip_check(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    
    try:
        start = time.perf_counter()
        # فحص صارم بـ 0.2 ثانية باش نعزلو غير الطيارة
        with socket.create_connection((host, int(port)), timeout=0.25) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            
            # كنقلبو على الـ Ping القريب من 97ms (مثلا بين 80 و 110)
            if 80 <= latency <= 115:
                tag = "💎ULTRA_VIP"
                priority = 0 # هو الأول في الترتيب
            elif latency < 80:
                tag = "⚡LOCAL_FAST"
                priority = 1
            else:
                return None # أي حاجة تقيلة كترفض

            return (priority, latency, f"C: {host} {port} {user} {passwd} # {tag}_{latency}ms")
    except:
        return None

def main_mission():
    print("🕵️‍♂️ Hunting for Paid-Grade Servers (Target: ~97ms)...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0'}
    all_raw = []

    with requests.Session() as session:
        session.headers.update(headers)
        for url in VIP_SOURCES:
            try:
                # تجاوز حماية المواقع بالـ Cookies والـ Headers
                r = session.get(url, timeout=12, verify=False)
                found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                all_raw.extend(found)
            except: continue

    unique_candidates = list(set(all_raw))
    print(f"📡 لقيت {len(unique_candidates)} سطر مرشح. جاري عزل السيرفرات المدفوعة...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
        results = list(executor.map(vip_check, unique_candidates))

    # الترتيب: السيرفرات القريبة من 97ms هي اللولة
    final_list = sorted([r for r in results if r], key=lambda x: (x[0], x[1]))

    if final_list:
        with open("PAID_GRADE.cfg", "w") as f:
            f.write(f"# VIP PAID-GRADE SERVERS | TARGET PING: 97ms\n")
            f.write(f"# GENERATED: {datetime.now().strftime('%H:%M:%S')}\n\n")
            for _, lat, server in final_list[:40]: # خذ فقط أفضل 40 سطر طيارة
                f.write(server + "\n")
        print(f"✅ تم! الملف 'PAID_GRADE.cfg' فيه {len(final_list[:40])} سيرفر 'مدفوع' بـ Ping خيالي.")
    else:
        print("❌ مالقيتش سيرفرات بهاد السرعة دابا. كاع اللي كاينين تقال.")

if __name__ == "__main__":
    main_mission()
