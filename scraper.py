import requests, re, socket, time, concurrent.futures

SOURCES = [
    "https://vipsat.net/free-cccam-server.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://clinetest.net/free_cccam.php",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt"
]

def strict_verify(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    
    # --- قائمة الحظر (البلاك ليست) للسيرفرات الوهمية ---
    fake_brands = ['streamtveuropa', '37.60.251.20', 'nassimbejaia', 'asiachannels']
    if any(fake in host.lower() for fake in fake_brands):
        return None

    try:
        start = time.perf_counter()
        s = socket.create_connection((host, int(port)), timeout=0.8)
        # محاكاة طلب بيانات حقيقية
        s.send(b"\x00\x00\x00\x00\x00\x00\x00\x00") 
        data = s.recv(1024)
        latency = int((time.perf_counter() - start) * 1000)
        s.close()

        # إذا كان السيرفر بريميوم (اليوزر ماشي سميت السيرفر) غيكون أفضل
        if data and user.lower() not in host.lower():
            return (latency, f"C: {host} {port} {user} {passwd} # 💎REAL_HIT_{latency}ms")
    except:
        return None

def main():
    print("🧹 Cleaning the trash and hunting real servers...")
    # ... نفس كود السحب (Request) اللي عندك ...
    # (تأكد من استعمال الـ Filter الجديد 'strict_verify')
