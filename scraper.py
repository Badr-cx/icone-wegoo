import requests
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor

# المصادر المباشرة (Sources) - حيدنا القدام وزدنا اللي فيهم التحديث دابا
SOURCES = [
    "https://vipsat.net/free-cccam-server.php",
    "https://www.cccambird.com/freecccam.php",
    "https://cccam-premium.pro/free-cccam/",
    "http://www.casacam.net/free-cccam-server/",
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt"
]

def measure_speed(line):
    line = line.strip()
    # تنظيف السطر من أي زوائد
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port = match.group(1), match.group(2)
    try:
        start_time = time.time()
        # فحص سريع جداً (0.5 ثانية)
        sock = socket.create_connection((host, int(port)), timeout=0.5)
        latency = (time.time() - start_time) * 1000
        sock.close()
        return {"line": f"C: {match.group(1)} {match.group(2)} {match.group(3)} {match.group(4)}", "latency": latency}
    except:
        return None

def main():
    print("🚀 جاري صيد أحدث سيرفر ناضي...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    all_raw = ""

    for url in SOURCES:
        try:
            # زدنا هاد البارامتر باش نكسرو الكاش (Cache)
            r = requests.get(url + f"?update={int(time.time())}", headers=headers, timeout=10)
            all_raw += r.text + "\n"
        except: continue

    # استخراج السطور
    found = re.findall(r'C:?\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', all_raw, re.I)
    unique_lines = list(set(found))
    
    verified_with_speed = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(measure_speed, unique_lines))
        verified_with_speed = [r for r in results if r]

    if verified_with_speed:
        # ترتيب حسب الأسرع
        verified_with_speed.sort(key=lambda x: x['latency'])
        best = verified_with_speed[0]

        # حفظ في CCcam.cfg (البياسة الواعرة)
        with open("CCcam.cfg", "w") as f:
            f.write(best['line'] + "\n")
            
        # حفظ في الملف التاني اللي عندك ف GitHub
        with open("VERIFIED_CANNON.cfg", "w") as f:
            f.write(f"### TOP SERVER FOUND ###\n{best['line']}\n")
            
        print(f"✅ تم! أقوى سيرفر دابا هو: {best['line']} ({int(best['latency'])}ms)")
    else:
        print("❌ مالقيت حتى سيرفر جديد خدام.")

if __name__ == "__main__":
    main()
