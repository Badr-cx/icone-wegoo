import socket
import time
from concurrent.futures import ThreadPoolExecutor

# حط القائمة ديالك هنا (أنا درت مثال ببعض الأسطر من اللي عطيتيني)
RAW_DATA = """
C: streamtveuropa.com 1990 streamtveuropa16 streamtveuropa
C: 37.60.251.20 14095 visit67 www
C: nassimbejaia1.hopto.org 15004 335779 nassim
C: cccam4k.casacam.net 43000 telegrami28 t
""" # كمل القائمة هنا...

def verify_elite(line):
    line = line.strip()
    if not line.startswith('C:'): return None
    
    parts = line.split()
    if len(parts) < 4: return None
    
    host, port = parts[1], parts[2]
    try:
        start = time.time()
        with socket.create_connection((host, int(port)), timeout=0.6):
            latency = int((time.time() - start) * 1000)
            return f"{line} # ✅ LIVE_{latency}ms"
    except:
        return None

def main():
    # تنظيف القائمة من الفراغات والتكرار
    lines = list(set([l.strip() for l in RAW_DATA.strip().split('\n') if l.strip()]))
    print(f"🔍 جاري فحص {len(lines)} سطر من فئة Elite...")

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(verify_elite, lines))
        verified = [r for r in results if r]

    # حفظ الصافي
    with open("ELITE_CANNON.cfg", "w", encoding="utf-8") as f:
        f.write(f"# SHADOW CORE V101 - CLEANED\n# Found {len(verified)} Active Servers\n\n")
        f.write("\n".join(verified))
    
    print(f"✅ تم! الملف واجد سميتو ELITE_CANNON.cfg فيه {len(verified)} سيرفر شغال.")

if __name__ == "__main__":
    main()
