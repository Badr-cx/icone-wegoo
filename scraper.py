import requests, re, socket, time, concurrent.futures
from datetime import datetime

# مصادر "خام" وسيرفرات مسربة (Leaked & Auto-Generated)
# هاد الروابط كتحط سيرفرات قبل ما توصل للمواقع المشهورة
SOURCES = [
    "https://raw.githubusercontent.com/mueof/free-cccam/main/cccam.txt",
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/tjm1024/Free-TV/master/cccam.txt",
    "https://raw.githubusercontent.com/Fidat-T/Free-CCcam/main/cccam.txt",
    "https://raw.githubusercontent.com/S-K-S-B/CCcam/main/cccam.txt",
    "https://clinetest.net/free_cccam.php",
    "https://vipsat.net/free-cccam-server.php",
    "https://fastcccam.com/free-cccam.php"
]

def verify_leaked_server(line):
    """ فحص فائق السرعة: أي سيرفر تقيل كيطير """
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    try:
        start = time.perf_counter()
        # تقليص الـ timeout لـ 0.25 ثانية فقط (غير اللي طيارة غيدوز)
        with socket.create_connection((host, int(port)), timeout=0.25) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            # وسم خاص للسيرفرات اللي كتحل باقات تقيلة
            if latency < 120: tag = "💎PREMIUM"
            else: tag = "✅STABLE"
            return (latency, f"C: {host} {port} {user} {passwd} # {tag}_{latency}ms")
    except:
        return None

def main_hunt():
    print("🎯 SHΔDØW CORE: جاري سحب السيرفرات من 'الكرش' ديال الويب...")
    
    all_hits = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    with requests.Session() as session:
        for url in SOURCES:
            try:
                # تجاوز حماية المواقع بـ verify=False
                r = session.get(url, timeout=6, verify=False)
                # صيد السطور بـ Regex كيقبل الحروف والأرقام فقط
                found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                all_hits.extend(found)
            except: continue

    # تنظيف القائمة من التكرار
    clean_hits = list(set(all_hits))
    print(f"📡 لقينا {len(clean_hits)} سيرفر مرشح. جاري الفرز النووي...")

    # فحص متوازي بـ 250 خيط (بسرعة البرق)
    with concurrent.futures.ThreadPoolExecutor(max_workers=250) as executor:
        results = list(executor.map(verify_leaked_server, clean_hits))

    # فلترة الشغالين وترتيبهم حسب الجودة
    live_servers = sorted([r for r in results if r], key=lambda x: x[0])

    if not live_servers:
        print("❌ الموارد حالياً ناشفة، جرب من هنا 10 دقايق.")
        return

    # حفظ أفضل 100 سيرفر فقط لضمان عدم ثقل الريسيفر
    with open("SHADOW_LEAKED.cfg", "w") as f:
        f.write(f"# LEAKED VIP SERVERS | {datetime.now().strftime('%H:%M:%S')}\n")
        f.write(f"# BEST FOR ASTRA/HOTBIRD | TOTAL: {len(live_servers[:100])}\n\n")
        for _, s in live_servers[:100]:
            f.write(s + "\n")

    print(f"✨ المهمة تمت! الملف 'SHADOW_LEAKED.cfg' فيه {len(live_servers[:100])} سيرفر ناضي.")
    print("🎬 جرب السطور اللي فيهم PREMIUM هوما اللولين.")

if __name__ == "__main__":
    main_hunt()
