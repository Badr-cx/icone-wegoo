import requests
import re
import socket
from datetime import datetime

def check_server(line):
    # تنقية السطر من HTML
    line = re.sub(r'<[^>]*>', '', line).strip()
    match = re.search(r'([CN]:\s*\S+\s+\d+\s+\S+\s+\S+)', line)
    if not match: return None
    clean_line = match.group(1)
    try:
        parts = clean_line.split()
        host, port = parts[1], int(parts[2].replace(',', ''))
        # فحص سريع للاتصال
        with socket.create_connection((host, port), timeout=1):
            return clean_line
    except: return None

def main():
    # توقيت التحديث
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # المصادر (تقدر تزيد اللي بغيتي)
    urls = [
        "https://cccamcard.com/free-cccam-server.php",
        "https://testcline.com/free-cccam-server.php",
        "https://raw.githubusercontent.com/Badr-cx/icone-wegoo/main/CCcam.cfg"
    ]
    
    all_found = []
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            found = re.findall(r'[CN]:\s?\S+\s\d+\s\S+\s\S+', r.text)
            all_found.extend(found)
        except: continue

    # تصفية وفحص
    unique_lines = list(set(all_found))
    online_servers = []
    for line in unique_lines:
        res = check_server(line)
        if res: online_servers.append(res)

    # كتابة الملف النهائي
    with open("CCcam.cfg", "w") as f:
        f.write(f"### LAST UPDATE: {now} ###\n")
        f.write(f"### SERVERS ONLINE: {len(online_servers)} ###\n\n")
        for s in online_servers:
            f.write(s + "\n")
    print(f"Update successful at {now}")

if __name__ == "__main__":
    main()
