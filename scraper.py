import requests
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor

# 🌐 أقوى المصادر المحدثة لعام 2026 (Premium & Raw)
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

OUTPUT_FILE = "VERIFIED_CANNON.cfg"

def check_line(line_data):
    """فحص السطر هل هو متصل (Live) أم لا"""
    host, port, user, pwd = line_data
    try:
        # فحص المنفذ بسرعة (Timeout 0.8 ثانية لضمان السرعة القصوى)
        with socket.create_connection((host, int(port)), timeout=0.8):
            return f"C: {host} {port} {user} {pwd}"
    except:
        return None

def main():
    print(f"--- 🛰️  Badr-cx / Icone Auto-Scraper 2026 ---")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    raw_lines = []

    # 1. جلب البيانات من كل المصادر
    for url in SOURCES:
        try:
            print(f"📥 جلب البيانات من: {url[:30]}...")
            response = requests.get(f"{url}?update={time.time()}", headers=headers, timeout=10)
            # Regex متطور كيقبط أي صيغة مكتوب بها السطر
            matches = re.findall(r'C:\s*([a-zA-Z0-9\-\.]+)\s+([0-9]+)\s+(\S+)\s+(\S+)', response.text, re.I)
            raw_lines.extend(matches)
        except:
            print(f"❌ فشل الاتصال بالمصدر: {url[:30]}")

    # 2. إزالة التكرار لضمان الكفاءة
    unique_lines = list(set(raw_lines))
    print(f"🔍 تم العثور على {len(unique_lines)} سطر فريد. جاري الفحص...")

    # 3. الفحص المتوازي (Multi-threading) لسرعة خيالية
    verified_clines = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(check_line, unique_lines))
        verified_clines = [r for r in results if r]

    # 4. حفظ النتائج في الملف
    if verified_clines:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Found {len(verified_clines)} Live Servers\n")
            f.write("\n".join(verified_clines))
        print(f"✅ تم بنجاح! السيرفرات الشغالة ({len(verified_clines)}) موجودة الآن في {OUTPUT_FILE}")
    else:
        print("⚠️ للأسف، لم يتم العثور على أي سيرفر شغال حالياً. جرب لاحقاً.")

if __name__ == "__main__":
    main()
