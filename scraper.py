import requests
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor

# المصادر "السرية" اللي كتحط السطور بالـ CAID والكومنتات
SOURCES = [
    "https://raw.githubusercontent.com/yousef-94/Free-CCcam/main/CCcam.txt",
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt",
    "https://vipsat.net/free-cccam-server.php",
    "https://www.cccambird.com/freecccam.php"
]

def check_line(line):
    line = line.strip()
    # كيقبل C و N وكيقرا حتى الكومنتات اللي موراهم
    if not re.match(r'^[CN]:', line, re.I): return None
    
    # استخراج الهوست والبورت للفحص
    parts = line.split()
    if len(parts) < 3: return None
    host, port = parts[1], parts[2]
    
    try:
        start = time.time()
        # فحص جودة الاتصال
        with socket.create_connection((host, int(port)), timeout=0.5):
            latency = (time.time() - start) * 1000
            return {"line": line, "latency": latency}
    except:
        return None

def main():
    print("🎯 جاري اصطياد السيرفرات 'النخبة' (CAID & Comments)...")
    all_raw = ""
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in SOURCES:
        try:
            # كسر الكاش باش نجيبو ديال هاد الدقيقة
            r = requests.get(f"{url}?t={int(time.time())}", headers=headers, timeout=10)
            all_raw += r.text + "\n"
        except: continue

    # Regex كيجيب السطر كامل بالكومنت ديالو #
    lines = re.findall(r'[CN]:\s*\S+\s+\d+\s+\S+\s+\S+.*', all_raw, re.I)
    unique_lines = list(set(lines))
    
    print(f"🔍 لقيت {len(unique_lines)} سيرفر. جاري اختيار الأسرع...")

    results = []
    with ThreadPoolExecutor(max_workers=60) as ex:
        results = [r for r in ex.map(check_line, unique_lines) if r]

    if results:
        # الترتيب حسب السرعة
        results.sort(key=lambda x: x['latency'])
        
        # غنخليو ليك Top 5 حيت هاد النوع كيكون فيه "الضرب" بزاف
        with open("CCcam.cfg", "w", encoding="utf-8") as f:
            for res in results[:5]:
                f.write(res['line'] + "\n")
        
        print(f"✅ تم! ها السيرفر الواعر اللي فيه الـ CAID:\n{results[0]['line']}")
        print(f"⚡ الـ Ping: {int(results[0]['latency'])}ms")
    else:
        print("❌ والو، جرب طفي الـ VPN إلا كنتي خدام بيه.")

if __name__ == "__main__":
    main()
