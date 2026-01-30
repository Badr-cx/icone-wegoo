import requests
import re
import socket
from concurrent.futures import ThreadPoolExecutor

# الرابط ديالك باش السكريبت يقرا منو نيشان
RAW_URL = "https://raw.githubusercontent.com/Badr-cx/icone-wegoo/refs/heads/main/CCcam.cfg"

def strict_check(line):
    # تنظيف السطر من أي شوائب
    line = line.strip()
    if not line or not (line.startswith('C:') or line.startswith('N:')):
        return None
    
    try:
        # تقطيع السطر للحصول على الهوست والبورت
        parts = line.split()
        host = parts[1]
        port = int(parts[2].replace(',', ''))
        
        # فحص الاتصال: التوقيت (Timeout) رديناه 0.8 ثانية
        # السيرفر اللي كيتعطل كتر من هاد الوقت غيتقطع فالماتشات، أحسن نمسحوه
        with socket.create_connection((host, port), timeout=0.8) as sock:
            return line
    except:
        return None

def main():
    print("--- جاري سحب الملف من GitHub وفحصه ---")
    try:
        r = requests.get(RAW_URL, timeout=10)
        # استخراج السطور اللي باديين بـ C: أو N:
        lines = re.findall(r'([CN]:\s?\S+\s\d+\s\S+\s\S+.*)', r.text)
    except:
        print("❌ مقدرتش نوصل للرابط!")
        return

    # إزالة السطور المعاودة (بزاف عندك فالموقع)
    unique_lines = list(set(lines))
    print(f"لقيت {len(unique_lines)} سطر فريد. جاري التصفية...")

    # الفحص بـ 100 خيط للسرعة
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(strict_check, unique_lines))

    online_servers = [s for s in results if s]

    # حفظ الملف الجديد
    with open("CCcam.cfg", "w") as f:
        for s in online_servers:
            f.write(s + "\n")

    print(f"✅ كملت! من أصل {len(unique_lines)}، لقيت {len(online_servers)} خدامين.")
    print("الملف CCcam.cfg دابا واجد ونقي.")

if __name__ == "__main__":
    main()
