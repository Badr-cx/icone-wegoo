import requests
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor

# القنوات اللي اخترتيها (Preview Mode)
TELEGRAM_CHANNELS = [
    "https://t.me/s/dsererer",
    "https://t.me/s/tvsatcccam"
]

def clean_line(line):
    """تنظيف سطر السيرفر من بقايا HTML ورموز التيليجرام"""
    line = re.sub(r'<[^>]*>', '', line) # مسح Tags
    line = line.replace('&nbsp;', ' ').replace('&amp;', '&').strip()
    return line

def check_line(line):
    line = clean_line(line)
    
    # التأكد أن السطر يبدأ بـ C: أو N: وفيه الهوست والبورت
    if not re.match(r'^[CN]:', line, re.I): return None
    
    parts = line.split()
    if len(parts) < 4: return None
    
    host, port = parts[1], parts[2]
    try:
        start = time.time()
        # فحص جودة الاتصال في 0.5 ثانية لضمان التلوين السريع
        with socket.create_connection((host, int(port)), timeout=0.5):
            latency = (time.time() - start) * 1000
            return {"line": line, "latency": latency}
    except:
        return None

def main():
    print("📡 جاري استخراج السيرفرات من قنوات Telegram...")
    all_raw = ""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    for url in TELEGRAM_CHANNELS:
        try:
            # كسر الكاش لضمان جلب آخر الميساجات
            r = requests.get(f"{url}?t={int(time.time())}", headers=headers, timeout=15)
            if r.status_code == 200:
                all_raw += r.text + "\n"
        except: continue

    # البحث عن السطور التي تبدأ بـ C: أو N: حتى نهاية الكومنت #
    # هاد Regex كيجيب السطر "البياسة" اللي فيه CAID والديتاي
    lines = re.findall(r'[CN]:\s*[^<>\n]+', all_raw, re.I)
    
    unique_lines = list(set(lines))
    print(f"🔍 لقيت {len(unique_lines)} سيرفر محتمل في القنوات. جاري الفحص...")

    results = []
    with ThreadPoolExecutor(max_workers=50) as ex:
        results = [r for r in ex.map(check_line, unique_lines) if r]

    if results:
        # ترتيب حسب السرعة (الأسرع هو الأول)
        results.sort(key=lambda x: x['latency'])
        
        # حفظ أقوى 10 سيرفرات في ملف CCcam.cfg
        with open("CCcam.cfg", "w", encoding="utf-8") as f:
            for res in results[:10]:
                f.write(res['line'] + "\n")
        
        print(f"✅ تم! جلبنا السيرفرات من التيليجرام بنجاح.")
        print(f"🎯 أسرع سيرفر لقيناه: {results[0]['line']}")
        print(f"⚡ الـ Ping: {int(results[0]['latency'])}ms (ثابت وممتاز للتلوين)")
    else:
        print("❌ لم يتم العثور على سيرفرات شغالة حالياً في القنوات.")

if __name__ == "__main__":
    main()
