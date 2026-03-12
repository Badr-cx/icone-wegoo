import requests
import re
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')
URL = f"https://testious.com/old-free-cccam-servers/{today}/"

def test_scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://testious.com/'
    }
    
    print(f"Connecting to: {URL}")
    
    try:
        response = requests.get(URL, headers=headers, timeout=30)
        # دابا غيهز أي سطر كيبدا بـ C: واخا ماتكونش حداه OK
        matches = re.findall(r'C:\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+([^\s]+)', response.text, re.IGNORECASE)
        
        if not matches:
            print("⚠️ No servers found at all on this page.")
            # غادي نكريو ملف خاوي غير باش ما يعطيش Git Error
            with open("ncam.server", "w") as f:
                f.write("# No servers found today yet\n")
            return

        config_data = ""
        for i, (host, port, user, pwd) in enumerate(matches):
            config_data += f"[reader]\nlabel = Test_Server_{i+1}\nprotocol = cccam\ndevice = {host},{port}\nuser = {user}\npassword = {pwd}\ngroup = 1\nroot = 1\ndisablecrccws = 1\nccckeepalive = 1\n\n"

        with open("ncam.server", "w") as f:
            f.write(config_data)
        
        print(f"✅ Success! {len(matches)} servers found and saved.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_scrape()
