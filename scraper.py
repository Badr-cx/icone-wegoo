import requests
import re
import socket
from datetime import datetime

# المواقع اللي غايجيب منها
SOURCES = [
    "https://testcline.com/free-cccam-server.php",
    "https://cccamcard.com/free-cccam-server.php",
    "https://cccam.premium.pro/free-cccam/"
]

def main():
    # توقيت المغرب (اليوم)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    valid_servers = []
    
    print(f"🧹 جاري تنظيف الملف الضخم وتحديثه: {now}")

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            # استخراج السطور
            found = re.findall(r'C:\s*\S+\s+\d+\s+\S+\s+\S+', r.text, re.IGNORECASE)
            # فحص سريع لـ 10 سيرفرات فقط من كل موقع لضمان السرعة والخفة
            for s in list(set(found))[:15]:
                valid_servers.append(s)
        except: continue

    # دابا غانمسحو الملف القديم (الكبير) ونحطو الجديد
    with open("CCcam.cfg", "w") as f:
        f.write(f"### LAST UPDATE: {now} ###\n")
        f.write(f"### FILE CLEANED: {len(valid_servers)} SERVERS ###\n\n")
        for s in valid_servers:
            f.write(s + "\n")
    
    print("✅ تم تنظيف الملف بنجاح!")

if __name__ == "__main__":
    main()
