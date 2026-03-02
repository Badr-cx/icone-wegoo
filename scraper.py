import requests
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor

# 🌐 أقوى المصادر + زدت ليك اللي كيعطيو N-Lines
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt",
    "https://cccam-premium.pro/free-cccam/",
    "https://vipsat.net/free-cccam-server.php",
    "https://www.cccambird.com/freecccam.php",
    "https://free-cccam.top/",
    "https://boss-cam.com/free-cccam/",
    "https://gold-cccam.tv/free-server/"
]

OUTPUT_FILE = "VERIFIED_BADR.cfg"

def check_line(line):
    """فحص السطر واش السيرفر حي (Live)"""
    # تنظيف السطر من أي فراغات زايدة
    line = line.strip()
    parts = line.split()
    if len(parts) < 4: return None
    
    host = parts[1]
    port = parts[2]
    
    try:
        # فحص الاتصال بالبورت في أقل من ثانية
        with socket.create_connection((host, int(port)), timeout=0.8):
            return line
    except:
        return None

def main():
    print(f"--- 🛰️  Badr-cx / Icone Auto-Scraper 2026 ---")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    raw_lines = []

    # 1. جلب البيانات
    for url in SOURCES:
        try:
            print(f"📥 جلب البيانات من: {url[:35]}...")
            response = requests.get(f"{url}?update={time.time()}", headers=headers, timeout=10)
            
            # Regex مطور كيقبط C: و N: بجوج وكينقي السطر من الزوائد
            matches = re.findall(r'([CN]:\s*[a-zA-Z0-9\-\.]+\s+[0-9]+\s+\S+\s+\S+)', response.text, re.I)
            raw_lines.extend(matches)
        except:
            print(f"❌ فشل الاتصال بالمصدر")

    # 2. إزالة التكرار
    unique_lines = list(set(raw_lines))
    print(f"🔍 لقيت {len(unique_lines)} سطر فريد. جاري الفحص...")

    # 3. الفحص المتوازي (50 Thread لسرعة خيالية)
    verified_clines = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(check_line, unique_lines))
        verified_clines = [r for r in results if r]

    # 4. حفظ النتائج
    if verified_clines:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"########################################\n")
            f.write(f"# Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Found {len(verified_clines)} Live Servers\n")
            f.write(f"########################################\n\n")
            f.write("\n".join(verified_clines))
        print(f"\n✅ ناضي! السيرفرات اللي خدامين ({len(verified_clines)}) تلقاهم فـ {OUTPUT_FILE}")
    else:
        print("\n⚠️ حتى سطر ما خدام حاليا.")

if __name__ == "__main__":
    main()
