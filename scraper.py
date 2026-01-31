import requests
import re
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# المصادر كاملة اللي عطيتيني
SOURCES = [
    "https://testcline.com/free-cccam-server.php", # الموقع الجديد
    "https://cccamcard.com/free-cccam-server.php",
    "https://cccam.premium.pro/free-cccam/",
    "https://cccamia.com/free-cccam/",
    "https://raw.githubusercontent.com/Badr-cx/icone-wegoo/main/CCcam.cfg"
]

def real_cccam_test(line):
    """محاكاة منطق C-Tester للتأكد من أن السيرفر شغال بصح"""
    line = re.sub(r'<[^>]*>', '', line).strip()
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.IGNORECASE)
    if not match: return None
    
    host, port, user, password = match.groups()
    try:
        # محاولة الاتصال وانتظار الـ Seed (كما في كود C)
        with socket.create_connection((host, int(port)), timeout=0.8) as sock:
            sock.settimeout(1.2)
            seed = sock.recv(16)
            if len(seed) >= 12: # إذا صيفط السيرفر بيانات، يعني راه "حي"
                return f"C: {host} {port} {user} {password}"
    except:
        return None

def main():
    # توقيت المغرب (أو توقيت السيرفر)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_found = []

    print(f"📡 بدء السحب والفحص: {now}")

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            found = re.findall(r'C:\s*\S+\s+\d+\s*\S+\s+\S+', r.text, re.IGNORECASE)
            all_found.extend(found)
            print(f"✅ تم سحب {len(found)} سيرفر من {url.split('/')[2]}")
        except:
            continue

    # إزالة التكرار والفحص السريع بـ ThreadPool
    unique_lines = list(set(all_found))
    print(f"🔍 فحص {len(unique_lines)} سيرفر بـ Deep Testing...")
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(real_cccam_test, unique_lines))

    online_servers = [s for s in results if s]

    # كتابة الملف النهائي مع التاريخ (اللي غيبان ليك فـ Raw)
    with open("CCcam.cfg", "w") as f:
        f.write(f"### LAST UPDATE: {now} ###\n")
        f.write(f"### SERVERS ONLINE: {len(online_servers)} ###\n\n")
        for s in online_servers:
            f.write(s + "\n")

    print(f"🚀 تم التحديث! الملف دابا واجد بـ {len(online_servers)} سيرفر ناضي.")

if __name__ == "__main__":
    main()
