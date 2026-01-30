import requests
import re
import socket
from concurrent.futures import ThreadPoolExecutor

# 1. المواقع اللي غنجبدو منها السيرفرات أوتوماتيكيا
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

# 2. السيرفرات اللي حطيتي ليا نتا (Manual List)
MANUAL_SERVERS = """
C: 151.115.73.226 12001 west bestpsw
C: free.cccam-premium.pro 15014 0gqtm6 cccam-premium.co</div>
C: free.cccam-premium.pro 15014 ypr1c2 cccam-premium.co</div>
N: cardsharing-sat.camdvr.org 17102 6b6a6k4 www.cardsharing-sat.com
# ... تقدر تزيد السطور ديالك هنا
"""

def check_server(line):
    # تنظيف السطر من كود HTML والفراغات
    line = line.replace("</div>", "").strip()
    try:
        parts = line.split()
        if len(parts) < 3: return None
        host = parts[1]
        port = int(parts[2].replace(',', ''))
        # تجربة الاتصال
        with socket.create_connection((host, port), timeout=1.5):
            return line
    except:
        return None

def main():
    all_found = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    print("--- البدء في جمع السيرفرات ---")
    
    # سحب من المواقع
    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            found = re.findall(r'([CN]:\s?\S+\s\d+\s\S+\s\S+)', r.text)
            all_found.extend(found)
            print(f"✅ تم السحب من: {url.split('/')[2]}")
        except: pass

    # إضافة السيرفرات اليدوية
    manual_found = re.findall(r'([CN]:\s?\S+\s\d+\s\S+\s\S+)', MANUAL_SERVERS)
    all_found.extend(manual_found)

    # حيد المعاودين
    unique_servers = list(set(all_found))
    print(f"\nإجمالي السيرفرات المجموعة: {len(unique_servers)}")
    print("--- جاري فحص السيرفرات الشغالة ---")

    # فحص 100 سيرفر في وقت واحد للسرعة
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(check_server, unique_servers))

    online_servers = [s for s in results if s]

    # حفظ النتيجة النهائية
    with open("CCcam.cfg", "w") as f:
        # ديما سطر البداية ديالك
        f.write("C: 151.115.73.226 12001 west bestpsw\n")
        for s in online_servers:
            f.write(s + "\n")

    print(f"\n✅ النتيجة: تم حفظ {len(online_servers)} سيرفر شغال في CCcam.cfg")

if __name__ == "__main__":
    main()
