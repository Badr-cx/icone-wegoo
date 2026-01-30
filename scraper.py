import requests
import re
import socket
from concurrent.futures import ThreadPoolExecutor

# قائمة المواقع اللي عطيتيني
SOURCES = [
    "https://cccamcard.com/free-cccam-server.php",
    "https://testcline.com/free-cccam-server.php",
    "https://cccam.premium.pro/free-cccam/",
    "https://cccam.net/free",
    "https://cccamia.com/free-cccam/",
    "https://www.cccambird.com/freecccam.php",
    "https://www.cccambird2.com/freecccam.php",
    "https://cccamprime.com/cccam48h.php",
    "https://skyhd.xyz/freetest/osm.php",
    "https://www.tvlivepro.com/free_cccam_48h/",
    "https://dhoom.org/test/"
]

def check_server(line):
    try:
        # تنظيف السطر وتقسيمه للحصول على الهوست والبورت
        parts = line.strip().split()
        if len(parts) < 3: return None
        host = parts[1]
        port = int(parts[2].replace(',', ''))
        
        # محاولة الاتصال (Timeout 1.5 ثانية للسرعة)
        with socket.create_connection((host, port), timeout=1.5):
            return line.strip()
    except:
        return None

def scrape_and_save():
    all_raw_lines = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    print("--- البدء في سحب السيرفرات من المواقع ---")
    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            # البحث عن أنماط C: و N: وسط كود الصفحة
            found = re.findall(r'([CN]:\s?\S+\s\d+\s\S+\s\S+)', r.text)
            all_raw_lines.extend(found)
            print(f"✅ تم السحب من: {url.split('/')[2]} (لقينا {len(found)})")
        except:
            print(f"❌ فشل السحب من: {url.split('/')[2]}")

    # إزالة التكرار
    unique_lines = list(set(all_raw_lines))
    print(f"\nإجمالي السيرفرات المسحوبة: {len(unique_lines)}")

    # فحص السيرفرات (Multi-threading)
    print("--- جاري فحص السيرفرات الشغالة (Online) ---")
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(check_server, unique_lines))

    online_servers = [s for s in results if s]

    # حفظ السيرفرات الشغالة فقط في الملف
    with open("CCcam.cfg", "w") as f:
        # إضافة سيرفرك الخاص ديما في الأول
        f.write("C: 151.115.73.226 12001 west bestpsw\n")
        for s in online_servers:
            f.write(s + "\n")

    print(f"\n--- النتيجة النهائية ---")
    print(f"تم إيجاد {len(online_servers)} سيرفر شغال حالياً.")
    print("تم تحديث ملف CCcam.cfg بنجاح.")

if __name__ == "__main__":
    scrape_and_save()
