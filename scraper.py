import requests
import re
import socket

def check_server(host, port):
    try:
        # كيجرب يتصل بالبورت لمدة 2 ثواني
        sock = socket.create_connection((host, int(port)), timeout=2)
        sock.close()
        return True
    except:
        return False

def scrape_and_filter():
    sources = [
        "https://cccamcard.com/free-cccam-server.php",
        "https://clinetest.net/free_cccam.php",
        "https://raw.githubusercontent.com/yebekhe/TVHub/main/pannels/channels.txt"
    ]
    
    found_raw = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in sources:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            matches = re.findall(r'([CN]:\s?(\S+)\s(\d+)\s\S+\s\S+)', r.text)
            found_raw.extend(matches) # كيجيب (السطر كامل، الهوست، البورت)
        except:
            continue

    online_servers = []
    print("Checking servers status...")

    # تصفية السيرفرات (Checking)
    for full_line, host, port in found_raw:
        if check_server(host, port):
            online_servers.append(full_line.strip())
            print(f"[✅ ONLINE] {host}")
        else:
            print(f"[❌ OFFLINE] {host}")

    # حفظ السيرفرات اللي خدامة فقط
    with open("CCcam.cfg", "w") as f:
        # ديما حط سيرفرك الخاص هو الأول (اختياري)
        f.write("C: 151.115.73.226 12001 west bestpsw\n")
        
        # حط السيرفرات اللي دازت من التيست بلا تكرار
        for s in list(set(online_servers)):
            f.write(s + "\n")

if __name__ == "__main__":
    scrape_and_filter()
