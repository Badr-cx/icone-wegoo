import requests
import re
from datetime import datetime

# الرابط ديال اليوم فـ Testious
today = datetime.now().strftime('%Y-%m-%d')
URL = f"https://testious.com/old-free-cccam-servers/{today}/"

def test_scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Connecting to: {URL}")
    
    try:
        response = requests.get(URL, headers=headers, timeout=30)
        # كيهز كاع السيرفرات اللي حداهم [OK]
        matches = re.findall(r'C:\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+([^\s]+).*?OK', response.text, re.IGNORECASE)
        
        if not matches:
            print("⚠️ No active servers found yet.")
            return

        config_data = ""
        for i, (host, port, user, pwd) in enumerate(matches):
            config_data += f"[reader]\nlabel = Testious_OK_{i+1}\nprotocol = cccam\ndevice = {host},{port}\nuser = {user}\npassword = {pwd}\ngroup = 1\nroot = 1\ndisablecrccws = 1\nccckeepalive = 1\n\n"

        # حفظ البيانات فـ ملف محلي فـ GitHub
        with open("ncam.server", "w") as f:
            f.write(config_data)
        
        print(f"✅ Success! {len(matches)} servers saved to ncam.server file.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_scrape()
