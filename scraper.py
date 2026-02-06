import requests, re, socket, time, concurrent.futures
from datetime import datetime

# 1. المصادر "الهمزة"
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://raw.githubusercontent.com/mueof/free-cccam/main/cccam.txt",
    "https://vipsat.net/free-cccam-server.php",
    "https://boss-cccam.com/free-cccam-server.php",
    "https://clinetest.net/free_cccam.php",
    "https://fastcccam.com/free-cccam.php",
    "https://raw.githubusercontent.com/mizstd/free-cccam-servers/main/cccam.txt"
]

# الـ Readers الثابتة ديال AFN و SoftCam
NCAM_HEADER = """[reader]
label                         = github:SoftCam_AutoUpdate
enable                        = 1
protocol                      = emu
device                        = https://raw.githubusercontent.com/JetCamFastCam/JetFastCamRza/main/SoftCam.Key
disablecrccws_only_for        = 0E00:000000
caid                          = 0500,0604,090F,0E00,1010,1801,2600,2602,2610,4AE1
detect                        = cd
ident                         = 0500:000000,007400,007800,021110,023800;0604:000000;090F:000000;0E00:000000;1010:000000;1801:000000,001101,002111,007301;2600:000000;2602:000000;2610:000000;4AE1:000011,000014,0000FE
group                         = 1
emmcache                      = 2,1,2,1
emu_auproviders               = 0604:010200;0E00:000000;1010:000000;2610:000000;4AE1:000011,000014,0000FE

[reader]
label                         = Emulator_Local
enable                        = 1
protocol                      = emu
device                        = emulator
group                         = 1
"""

def verify_server(line):
    line = line.strip()
    match = re.search(r'C:\s*([a-zA-Z0-9\-\.]+)\s+(\d+)\s+(\S+)\s+(\S+)', line, re.I)
    if not match: return None
    
    host, port, user, passwd = match.groups()
    
    # البلاك ليست (حظر الهوستات اللي مخدامينش)
    forbidden = ['streamtveuropa', 'nassim', '37.60.251.20', 'visit', 'cam2.cline.wf', 'ugeen', 'casacam']
    if any(f in host.lower() for f in forbidden): return None

    try:
        start = time.perf_counter()
        with socket.create_connection((host, int(port)), timeout=1.0) as sock:
            latency = int((time.perf_counter() - start) * 1000)
            if latency < 250: # شرط السرعة
                return (latency, host, port, user, passwd)
    except:
        return None

def run_scraper():
    print("🛰️ Starting Stealth Hunt for Ncam...")
    all_raw = []
    
    with requests.Session() as s:
        s.headers.update({'User-Agent': 'Mozilla/5.0'})
        for url in SOURCES:
            try:
                r = s.get(f"{url}?v={time.time()}", timeout=10)
                matches = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', r.text, re.I)
                all_raw.extend(matches)
            except: continue

    unique_list = list(set(all_raw))
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as executor:
        results = [r for r in executor.map(verify_server, unique_list) if r]

    # الترتيب حسب السرعة
    results.sort(key=lambda x: x[0])

    # 1. كتابة ملف ncam.server
    with open("ncam.server", "w") as f:
        f.write(f"### NCAM GENERATED | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ###\n\n")
        f.write(NCAM_HEADER)
        
        for i, (lat, host, port, user, passwd) in enumerate(results[:25]): # أحسن 25 سيرفر
            f.write(f"\n[reader]\n")
            f.write(f"label                         = Server_{i}_Ping_{lat}ms\n")
            f.write(f"protocol                      = cccam\n")
            f.write(f"device                        = {host},{port}\n")
            f.write(f"user                          = {user}\n")
            f.write(f"password                      = {passwd}\n")
            f.write(f"group                         = 1\n")
            f.write(f"cccversion                    = 2.3.2\n")
            f.write(f"ccckeepalive                  = 1\n")

    # 2. كتابة ملف .cfg (للاحتياط)
    with open("VERIFIED_CANNON.cfg", "w") as f:
        f.write(f"# NCAM CONFIG | {datetime.now().strftime('%H:%M:%S')}\n\n")
        for lat, host, port, user, passwd in results[:25]:
            f.write(f"C: {host} {port} {user} {passwd} # ✅{lat}ms\n")

    print(f"✅ Mission Accomplished! ncam.server and .cfg files updated.")

if __name__ == "__main__":
    run_scraper()
