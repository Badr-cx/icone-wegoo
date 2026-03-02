import requests
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor

# المصادر الواعرة
SOURCES = [
    "https://vipsat.net/free-cccam-server.php",
    "https://www.cccambird.com/freecccam.php",
    "https://cccam-premium.pro/free-cccam/",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt"
]

def measure_speed(line):
    line = line.strip()
    # تنظيف السطر من أي تعاليق قديمة
    clean_line = re.sub(r'#.*', '', line).strip()
    parts = clean_line.split()
    if len(parts) < 4: return None
    
    host, port = parts[1], parts[2]
    try:
        start_time = time.time()
        # فحص الاتصال
        sock = socket.create_connection((host, int(port)), timeout=0.8)
        latency = (time.time() - start_time) * 1000  # تحويل لـ ms
        sock.close()
        return {"line": clean_line, "latency": latency}
    except:
        return None

def main():
    print("🎯 جاري صيد السيرفرات وقياس السرعة...")
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

    # فحص السرعة بـ Threads
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(measure_speed, unique_lines))
        verified_with_speed = [r for r in results if r]

    # 🔥 الترتيب من الأسرع (أقل ms) إلى الأبطأ
    verified_with_speed.sort(key=lambda x: x['latency'])

    # خذ أفضل 10 سيرفرات فقط باش الجهاز يطير
    top_servers = verified_with_speed[:10]

    if top_servers:
        with open("CCcam.cfg", "w") as f:
            for item in top_servers:
                # حفظ السطر مع كتابة الـ ms حداه غير باش تعرف السرعة
                f.write(f"{item['line']} # ⚡ {int(item['latency'])}ms\n")
        
        print(f"✅ تم! أقوى سيرفر هو: {top_servers[0]['line']} ({int(top_servers[0]['latency'])}ms)")
        print(f"🚀 الملف CCcam.cfg فيه دابا أفضل {len(top_servers)} سيرفرات فـ العالم حالياً.")
    else:
        print("⚠️ مالقيت حتى سيرفر شغال مزيان.")

if __name__ == "__main__":
    main()
