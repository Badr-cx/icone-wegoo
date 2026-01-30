import requests
import re
import socket
from concurrent.futures import ThreadPoolExecutor

# الرابط ديالك
RAW_URL = "https://raw.githubusercontent.com/Badr-cx/icone-wegoo/refs/heads/main/CCcam.cfg"

def check_server(line):
    # تنقية السطر من HTML والتخربيق
    line = re.sub(r'<[^>]*>', '', line).strip()
    if not (line.startswith('C:') or line.startswith('N:')):
        return None
    
    try:
        parts = line.split()
        host = parts[1]
        port = int(parts[2].replace(',', ''))
        
        # فحص صارم جدا (0.7 ثانية) - السيرفر الثقيل ماعندنا مابغينا بيه
        with socket.create_connection((host, port), timeout=0.7):
            return line
    except:
        return None

def main():
    print("🚀 جاري تنقية الرابط ديالك...")
    try:
        r = requests.get(RAW_URL, timeout=10)
        # البحث عن السطور الحقيقية فقط
        potential_lines = re.findall(r'([CN]:\s?\S+\s\d+\s\S+\s\S+)', r.text)
    except:
        return

    # حيد المعاودين (Unique only)
    unique_lines = list(set(potential_lines))
    print(f"🔍 لقيت {len(unique_lines)} سطر فريد. جاري الفحص...")

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(check_server, unique_lines))

    online_servers = [s for s in results if s]

    # حفظ الملف
    with open("CCcam.cfg", "w") as f:
        f.write("# Cleaned & Checked by Gemini Scraper\n")
        for s in online_servers:
            f.write(s + "\n")

    print(f"✅ تم! من أصل {len(unique_lines)} سطر، بقاو غير {len(online_servers)} اللي ناضيين.")

if __name__ == "__main__":
    main()
