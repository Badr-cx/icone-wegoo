import socket
import re
from concurrent.futures import ThreadPoolExecutor

# حط هنا لقمة ديال السيرفرات اللي عطيتيني
raw_data = """
C: 151.115.73.226 12001 west bestpsw
C: 38.210.227.156 21000 tlegram https
# ... كمل السطور ديالك هنا
"""

def check_server(line):
    line = line.strip()
    if not line: return None
    try:
        parts = line.split()
        host = parts[1]
        port = int(parts[2])
        # فحص الاتصال في 2 ثواني
        with socket.create_connection((host, port), timeout=2.0):
            print(f"✅ خدام: {host}")
            return line
    except:
        print(f"❌ ميت: {line.split()[1] if len(line.split())>1 else 'unknown'}")
        return None

def main():
    # استخراج السطور
    all_lines = re.findall(r'([CN]:\s?\S+\s\d+\s\S+\s\S+.*)', raw_data)
    print(f"البدء في فحص {len(all_lines)} سيرفر...")

    with ThreadPoolExecutor(max_workers=30) as executor:
        results = list(executor.map(check_server, all_lines))

    online_servers = [s for s in results if s]

    with open("CCcam.cfg", "w") as f:
        # ديما زيد سيرفرك الخاص فالبداية كاحتياط
        f.write("C: 151.115.73.226 12001 west bestpsw\n")
        for s in set(online_servers):
            f.write(s + "\n")
            
    print(f"تم بنجاح! السيرفرات الشغالة حالياً: {len(online_servers)}")

if __name__ == "__main__":
    main()
