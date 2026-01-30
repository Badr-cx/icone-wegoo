import requests
import re
import socket
from concurrent.futures import ThreadPoolExecutor

# قائمة المواقع
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

def verify_server(line):
    """هاد الدالة هي اللي كتحكم واش السيرفر خدام ولا لا"""
    line = line.replace("</div>", "").strip()
    try:
        # استخراج الهوست والبورت باستعمال Regex
        match = re.search(r'[CN]:\s*(\S+)\s+(\d+)', line)
        if not match:
            return None
            
        host = match.group(1)
        port = int(match.group(2))
        
        # محاولة فتح اتصال حقيقي (Timeout 1.5 ثانية)
        with socket.create_connection((host, port), timeout=1.5):
            return line # إلا نجح الاتصال كيرجع السطر
    except:
        return None # إلا فشل كيتجاهلو

def main():
    raw_lines = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    print("--- البدء في سحب السيرفرات ---")
    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            # جبد أي سطر كيبدا بـ C: أو N:
            found = re.findall(r'([CN]:\s?\S+\s\d+\s\S+\s\S+.*)', r.text)
            raw_lines.extend(found)
            print(f"✅ تم سحب {len(found)} من {url.split('/')[2]}")
        except:
            print(f"❌ الموقع لا يستجيب: {url.split('/')[2]}")

    # حيد المعاودين قبل الفحص
    unique_raw = list(set(raw_lines))
    print(f"\nجاري فحص {len(unique_raw)} سيرفر (التحقق من الاتصال)...")

    # فحص السيرفرات بـ 50 خيط (Thread) لسرعة خيالية
    with ThreadPoolExecutor(max_workers=50) as executor:
        final_list = list(executor.map(verify_server, unique_raw))

    # تصفية النتائج (إزالة الروابط الميتة)
    online_servers = [s for s in final_list if s]

    # كتابة الملف النهائي
    with open("CCcam.cfg", "w") as f:
        for s in online_servers:
            f.write(s + "\n")

    print(f"\n--- النتيجة النهائية ---")
    print(f"إجمالي السيرفرات الميتة: {len(unique_raw) - len(online_servers)}")
    print(f"إجمالي السيرفرات الشغالة ✅: {len(online_servers)}")

if __name__ == "__main__":
    main()
