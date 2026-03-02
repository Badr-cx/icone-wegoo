import requests
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor

# المصادر المختارة بعناية
SOURCES = [
    "https://vipsat.net/free-cccam-server.php",
    "https://www.cccambird.com/freecccam.php",
    "https://cccam-premium.pro/free-cccam/",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt"
]

def measure_speed(line):
    line = line.strip()
    clean_line = re.sub(r'#.*', '', line).strip()
    parts = clean_line.split()
    if len(parts) < 4: return None
    
    host, port = parts[1], parts[2]
    try:
        start_time = time.time()
        # فحص صارم في أقل من ثانية
        sock = socket.create_connection((host, int(port)), timeout=0.8)
        latency = (time.time() - start_time) * 1000
        sock.close()
        return {"line": clean_line, "latency": latency}
    except:
        return None

def main():
    print("🚀 جاري البحث عن أقوى سيرفر في العالم حالياً...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    raw_found = []

    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            matches = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
            raw_found.extend(matches)
        except: continue

    unique_lines = list(set(raw_found))
    verified_with_speed = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(measure_speed, unique_lines))
        verified_with_speed = [r for r in results if r]

    if verified_with_speed:
        # ترتيب حسب السرعة (الـ Ping الأصغر هو الأول)
        verified_with_speed.sort(key=lambda x: x['latency'])
        
        # اختيار أسرع واحد فقط
        best_server = verified_with_speed[0]

        with open("CCcam.cfg", "w") as f:
            f.write(f"{best_server['line']} # ⚡ TOP SERVER | {int(best_server['latency'])}ms\n")
        
        print(f"✅ تم الحفظ! أقوى سيرفر هو: {best_server['line']}")
        print(f"⏱️ سرعة الاستجابة: {int(best_server['latency'])}ms")
    else:
        print("❌ لم يتم العثور على أي سيرفر شغال.")

if __name__ == "__main__":
    main()
