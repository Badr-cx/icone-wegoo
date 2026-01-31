import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

SOURCES = [
    "https://testcline.com/free-cccam-server.php",
    "https://cccamcard.com/free-cccam-server.php",
    "https://cccam.premium.pro/free-cccam/",
    "https://cccamia.com/free-cccam/"
]

def check_server_speed(line):
    """كيحسب سرعة الاستجابة وكيحيد HTML"""
    line = line.split('<')[0].strip()
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.IGNORECASE)
    if not match: return None
    
    host, port = match.group(1), int(match.group(2))
    start_time = time.time()
    try:
        # اتصال سريع جداً لجس النبض
        with socket.create_connection((host, port), timeout=0.6):
            latency = time.time() - start_time
            return (latency, line) # كيرجع السرعة مع السطر
    except:
        return None

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_raw = []

    print(f"🚀 جاري البحث عن أسرع 10 سيرفرات: {now}")

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=8, headers={'User-Agent': 'Mozilla/5.0'})
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.IGNORECASE)
            all_raw.extend(found)
        except: continue

    unique_lines = list(set(all_raw))
    
    # فحص السرعة لجميع السيرفرات
    with ThreadPoolExecutor(max_workers=40) as executor:
        results = list(executor.map(check_server_speed, unique_lines))

    # تصفية السيرفرات اللي جابو نتيجة وترتيبهم من الأسرع للأبطأ
    valid_results = [r for r in results if r is not None]
    valid_results.sort(key=lambda x: x[0]) # الترتيب حسب الـ Latency

    # اختيار أفضل 10 فقط
    best_10 = valid_results[:10]

    with open("CCcam.cfg", "w") as f:
        f.write(f"### LAST UPDATE: {now} ###\n")
        f.write(f"### QUALITY: TOP 10 FASTEST SERVERS ###\n\n")
        for latency, s in best_10:
            f.write(f"{s}\n") # حيدنا الـ </div> نهائياً هنا

    print(f"✅ تم اختيار {len(best_10)} سيرفرات هي الأسرع حالياً.")

if __name__ == "__main__":
    main()
