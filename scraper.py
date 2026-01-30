import cloudscraper
import re
import socket

# القائمة الشاملة والنهائية للمنابع القوية
URLS = [
    "https://www.cccambird.com/index.php",
    "https://kinghd.info/packs.php",
    "https://dhoom.org/test/",
    "https://cccam.net/freecccam",
    "https://cccamia.com/cccamfree1/",
    "https://www.cccampri.me/cccam24h.php",
    "https://cccam-premium.pro/free-cccam/",
    "http://cccam24h.com/lik1.php"
]

def is_online(host, port):
    """فحص الاتصال الفعلي بالسيرفر لضمان الجودة"""
    try:
        # محاولة فتح اتصال في 3 ثواني فقط لتسريع العملية
        sock = socket.create_connection((host, int(port)), timeout=3)
        sock.close()
        return True
    except:
        return False

def run_scraper():
    results = []
    # استخدام cloudscraper لتخطي حماية المواقع المتطورة
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )

    for url in URLS:
        try:
            print(f"جاري مسح المصدر: {url}")
            r = scraper.get(url, timeout=30)
            
            # رادار ذكي جداً لاستخراج السطر مع عزل الهوست والبورت للفحص
            # هذا النمط يضمن استخراج السيرفرات الحقيقية فقط واستبعاد الروابط
            pattern = r'([CN]:\s*([a-zA-Z0-9\.\-]+\.[a-z]{2,6})\s+(\d+)\s+([a-zA-Z0-9\.\-_]+)\s+([a-zA-Z0-9\.\-_]+))'
            matches = re.findall(pattern, r.text, re.IGNORECASE)
            
            for full_line, host, port, user, password in matches:
                # فلتر "الديطاي": استبعاد ملفات الخطوط والأكواد البرمجية
                if not any(x in full_line.lower() for x in ['.woff2', 'url(', 'font-', '.css', 'unicode-range']):
                    # الفحص التقني للسيرفر (Checker)
                    if is_online(host, port):
                        line_to_add = f"C: {host} {port} {user} {password}"
                        results.append(line_to_add.strip())
                        print(f"✅ متصل وشغال: {host}:{port}")
                    else:
                        print(f"❌ سيرفر ميت: {host}:{port}")
        except Exception as e:
            print(f"فشل الوصول للموقع {url}")
            continue

    # تنقية المكرر وترتيب النتائج
    unique_results = sorted(list(set(results)))
    
    with open("CCcam.cfg", "w") as f:
        f.write(f"# Badr-cx Master Scraper | 2026-01-30\n")
        f.write(f"# Total Live & Verified Servers: {len(unique_results)}\n\n")
        if unique_results:
            f.write("\n".join(unique_results))
        else:
            f.write("# Warning: No active servers found. Checking again in 6 hours.")
            
    print(f"انتهى! الكفة فيها {len(unique_results)} سيرفر حقيقي شغال.")

if __name__ == "__main__":
    run_scraper()
