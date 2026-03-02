import requests
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor

# المصادر "الوحوش"
MAWA9I3 = [
    "https://vipsat.net/free-cccam-server.php",
    "https://www.cccambird.com/freecccam.php",
    "https://cccam-premium.pro/free-cccam/",
    "https://www.boss-cccam.com/",
    "https://www.sonic-cccam.com/free-cccam-6-months/",
    "https://cccamgenerator.com/",
    "https://www.cccam-free.com/free-cccam-1-month/"
]

def check_elite(line):
    line = line.strip()
    # تنظيف السطر من أي خزعبلات HTML
    line = re.sub('<[^<]+?>', '', line)
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port = match.group(1), match.group(2)
    try:
        start = time.time()
        # فحص صارم: 0.6 ثانية كحد أقصى للرد
        with socket.create_connection((host, int(port)), timeout=0.6):
            latency = (time.time() - start) * 1000
            return {
                "line": f"C: {match.group(1)} {match.group(2)} {match.group(3)} {match.group(4)}",
                "latency": latency
            }
    except:
        return None

def main():
    print("🌪️  جاري اكتساح المواقع وجلب السيرفرات...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    all_content = ""

    for url in MAWA9I3:
        try:
            r = requests.get(url, headers=headers, timeout=12)
            all_content += r.text + "\n"
        except: continue

    # البحث عن السيرفرات بأي صيغة كانت
    found = re.findall(r'C:?\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', all_content, re.I)
    unique = list(set(found))
    print(f"🔍 لقيت {len(unique)} سيرفر محتمل. جاري استخراج الأقوى على الإطلاق...")

    results = []
    with ThreadPoolExecutor(max_workers=100) as ex:
        results = [r for r in ex.map(check_elite, unique) if r]

    if results:
        # الترتيب حسب السرعة (الأسرع هو الأول)
        results.sort(key=lambda x: x['latency'])
        
        # غنخليو ليك أقوى 3 سيرفرات باش إلا طاح واحد يخدم لاخور فالبلاصة
        with open("CCcam.cfg", "w") as f:
            for i, res in enumerate(results[:3]):
                f.write(f"{res['line']} # Rank_{i+1}_{int(res['latency'])}ms\n")
        
        print(f"✅ ناضي! أقوى سيرفر حالياً هو: {results[0]['line']}")
        print(f"🚀 الـ Ping ديالو: {int(results[0]['latency'])}ms (طيارة)")
    else:
        print("⚠️ المواقع دابا مزيرين، جرب من بعد 10 دقايق كيكون التحديث.")

if __name__ == "__main__":
    main()
