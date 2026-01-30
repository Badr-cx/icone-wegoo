import requests
import re
import socket
from concurrent.futures import ThreadPoolExecutor

# المصادر (درت ليك غير المصادر اللي ديما فيها الجديد)
SOURCES = [
    "https://cccamcard.com/free-cccam-server.php",
    "https://testcline.com/free-cccam-server.php",
    "https://cccam.premium.pro/free-cccam/",
    "https://cccamia.com/free-cccam/",
    "https://www.cccambird.com/freecccam.php",
    "https://cccamprime.com/cccam48h.php",
    "https://dhoom.org/test/"
]

def verify_server(line):
    # 1. تنظيف السطر
    line = line.replace("</div>", "").strip()
    # مسح أي حاجة من غير السطر الأساسي
    match = re.search(r'([CN]:\s*\S+\s+\d+\s+\S+\s+\S+)', line)
    if not match:
        return None
    
    clean_line = match.group(1)
    parts = clean_line.split()
    host = parts[1]
    port = int(parts[2])

    # 2. فلتر الهوستات "الخادعة" (اللي كتكون Online ولكن ما فاتحاش)
    blacklist = ["127.0.0.1", "localhost", "0.0.0.0"]
    if host in blacklist:
        return None

    # 3. الفحص الصارم (Strict Check)
    try:
        # استعملنا 1.0 ثانية فقط. إلا تعطل السيرفر كتر من ثانية يعني ثقيل وغادي يقطع ليك
        with socket.create_connection((host, port), timeout=1.0):
            return clean_line
    except:
        return None

def main():
    all_lines = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    print("--- جاري جمع السيرفرات من المصادر ---")
    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=5)
            # استخراج السطور
            found = re.findall(r'[CN]:\s?\S+\s\d+\s\S+\s\S+', r.text)
            all_lines.extend(found)
        except:
            continue

    # حيد المعاودين
    unique_lines = list(set(all_lines))
    print(f"لقينا {len(unique_lines)} سطر. جاري الفحص الصارم...")

    # الفحص السريع
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(verify_server, unique_lines))

    # التصفية النهائية
    online_servers = [s for s in results if s]

    # حفظ الملف
    with open("CCcam.cfg", "w") as f:
        # ديما زيد سطر واحد "شغال 100%" كاحتياط في الأول
        f.write("C: 151.115.73.226 12001 west bestpsw\n")
        for s in online_servers:
            f.write(s + "\n")

    print(f"✅ مبروك! صفينا كولشي وخلينا غير {len(online_servers)} سيرفر شغال مزيان.")

if __name__ == "__main__":
    main()
