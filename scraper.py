import requests
import re
import socket
import time
import random
from concurrent.futures import ThreadPoolExecutor

# مصادر "حارقة" كتحط التحديث بالثانية
MAWA9I3 = [
    f"https://vipsat.net/free-cccam-server.php?v={random.randint(1, 99999)}",
    f"https://www.cccambird.com/freecccam.php?v={random.randint(1, 99999)}",
    "https://cccam-premium.pro/free-cccam/",
    "http://www.casacam.net/free-cccam-server/",
    "https://www.cccamgenerator.com/free-cccam-24h/",
    "https://sonic-cccam.com/free-cccam-6-months/"
]

def check_elite(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port = match.group(1), match.group(2)
    try:
        start = time.time()
        # فحص صارم جداً (0.5 ثانية) باش نجيبو غير اللي طيارة
        with socket.create_connection((host, int(port)), timeout=0.5):
            latency = (time.time() - start) * 1000
            return {"line": f"C: {match.group(1)} {match.group(2)} {match.group(3)} {match.group(4)}", "latency": latency}
    except:
        return None

def main():
    print("🧨 جاري كسر الـ Cache وجلب سيرفرات اللحظة...")
    # هيدرز متنوعة باش الموقع ما يعرفكش
    headers = {
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100, 122)}.0.0.0 Safari/537.36',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
    
    all_content = ""
    for url in MAWA9I3:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                all_content += r.text + "\n"
        except: continue

    # صيد السيرفرات بـ Regex مطور
    found = re.findall(r'C:?\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', all_content, re.I)
    unique = list(set(found))
    print(f"🔍 لقيت {len(unique)} سيرفر محتمل. جاري تصفية 'الخردة' واختيار الأسرع...")

    results = []
    with ThreadPoolExecutor(max_workers=50) as ex:
        results = [r for r in ex.map(check_elite, unique) if r]

    if results:
        # ترتيب حسب السرعة (الأسرع هو الأول)
        results.sort(key=lambda x: x['latency'])
        
        # غانخليو ليك أسرع واحد فقط فـ CCcam.cfg باش الجهاز يطير
        with open("CCcam.cfg", "w") as f:
            f.write(f"{results[0]['line']}\n")
        
        print(f"✅ ناضي! السيرفر الجديد والواعر هو: {results[0]['line']}")
        print(f"⏱️ الـ Ping: {int(results[0]['latency'])}ms (سرعة خيالية)")
    else:
        print("❌ والو، السيرفرات اللي كاينين دابا إما طافيين أو المواقع معطلين فالتحديث.")

if __name__ == "__main__":
    main()
