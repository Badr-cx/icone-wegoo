import requests
import re
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# المصادر اللي غايجبد منها + الرابط ديالك باش ينقيه
SOURCES = [
    "https://cccamcard.com/free-cccam-server.php",
    "https://testcline.com/free-cccam-server.php",
    "https://cccam.premium.pro/free-cccam/",
    "https://cccamia.com/free-cccam/",
    "https://raw.githubusercontent.com/Badr-cx/icone-wegoo/refs/heads/main/CCcam.cfg"
]

def cccam_tester(line):
    """هاد الدالة كتحاكي دالة cc_connect اللي عطيتيني فكود C"""
    # تنقية السطر من HTML (</div>, <span>...)
    line = re.sub(r'<[^>]*>', '', line).strip()
    match = re.search(r'([CN]:\s*\S+\s+\d+\s+\S+\s+\S+)', line)
    if not match: return None
    
    clean_line = match.group(1)
    parts = clean_line.split()
    host, port = parts[1], int(parts[2].replace(',', ''))
    
    try:
        # محاولة فتح اتصال TCP
        with socket.create_connection((host, port), timeout=0.8) as sock:
            # محاكاة الـ cc_recv_to اللي فكود C (انتظار 16 byte ديال الـ Seed)
            sock.settimeout(1.2)
            seed = sock.recv(16)
            
            # إذا السيرفر صيفط الـ Seed يعني راه CCcam شغال ومستعد للـ Login
            if len(seed) >= 12:
                return clean_line
    except:
        return None
    return None

def main():
    # تاريخ اليوم والساعة
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    all_raw = []
    
    print(f"🚀 بدء عملية التحيين والفحص: {now}")

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            found = re.findall(r'[CN]:\s?\S+\s\d+\s\S+\s\S+', r.text)
            all_raw.extend(found)
        except: continue

    # إزالة التكرار
    unique_lines = list(set(all_raw))
    print(f"🔍 لقيت {len(unique_lines)} سطر. جاري الغربلة (Deep Testing)...")

    # فحص 100 سطر في دقة واحدة للسرعة
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(cccam_tester, unique_lines))

    online_servers = [s for s in results if s]

    # كتابة الملف النهائي
    with open("CCcam.cfg", "w") as f:
        f.write(f"# 📅 Last Update: {now}\n")
        f.write(f"# ✅ Active Servers: {len(online_servers)}\n")
        f.write("# 🤖 Verified by Gemini Pro Tester\n\n")
        for s in online_servers:
            f.write(s + "\n")

    print(f"✅ مبروك! الرابط ديالك دابا فيه {len(online_servers)} سيرفر ناضيين.")

if __name__ == "__main__":
    main()
