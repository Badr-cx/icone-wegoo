import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# المصادر المباشرة (Generator Sites)
SOURCES = [
    "https://clinetest.net/free_cccam.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://cccamfree.cc/free-cccam-server/",
    "https://testcline.com/free-cccam-server.php",
    "https://cccamcard.com/free-cccam-server.php",
    "https://www.cccambird.com/freecccam.php",
    "https://iptv-m3u.online/free-cccam-server/",
    "https://vau-cccam.com/free-cccam/",
    "https://boss-iptv.com/free-cccam/"
]

def check_server(line):
    # تنظيف السطر من أي رموز HTML قد تكون عالقة
    line = re.sub(r'<[^>]*>', '', line).strip()
    match = re.search(r'C:\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.IGNORECASE)
    if not match: return None
    
    host, port, user, password = match.groups()
    try:
        start_time = time.time()
        # فحص جودة الاتصال (Timeout 1s)
        with socket.create_connection((host, int(port)), timeout=1.0):
            latency = (time.time() - start_time) * 1000
            return (latency, f"C: {host} {port} {user} {password} # Ping: {int(latency)}ms")
    except:
        return None

def main():
    print("--- [ 🚀 SNIPER V86 - DIRECT SOURCE MODE ] ---")
    all_raw = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Referer': 'https://google.com'
    }

    for url in SOURCES:
        try:
            print(f"[*] جاري سحب البيانات من: {url.split('/')[2]}...")
            # إرسال طلب للموقع مع تجاوز حماية SSL
            r = requests.get(url, timeout=15, headers=headers, verify=False)
            
            # محاولة صيد الأسطر بنمط ذكي (Regex)
            # هاد النمط غيجبد السطر وخا يكون وسط الـ Text
            found = re.findall(r'C:\s*[a-zA-Z0-9\.\-]+\s+[0-9]+\s+[a-zA-Z0-9\.\-_]+\s+[a-zA-Z0-9\.\-_]+', r.text, re.IGNORECASE)
            
            if found:
                print(f"   [✔] تم صيد {len(found)} سطر!")
                all_raw.extend(found)
            else:
                print("   [!] لم يتم العثور على أسطر (قد يحتاج الموقع لتحديث يدوياً).")
        except Exception as e:
            print(f"   [X] خطأ في الاتصال: {url.split('/')[2]}")

    all_raw = list(set(all_raw)) # إزالة التكرار
    print(f"\n[*] إجمالي الأسطر المحتملة: {len(all_raw)}")

    if not all_raw:
        print("!!! [فشل] لم يتم العثور على أي سطر شغال حالياً.")
        return

    # الفحص المتوازي لضمان السرعة
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = [r for r in executor.map(check_server, all_raw) if r]

    # ترتيب الأسطر من الأسرع للأبطأ
    results.sort(key=lambda x: x[0])

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("CCcam.cfg", "w") as f:
        f.write(f"### LAST UPDATE: {now} ###\n")
        f.write(f"### SOURCES: DIRECT GENERATORS ###\n\n")
        for lat, line in results[:25]:
            f.write(f"{line}\n")
    
    print(f"\n[✔] انتهت المهمة! تم حفظ {len(results[:25])} سطر في CCcam.cfg")

if __name__ == "__main__":
    main()
