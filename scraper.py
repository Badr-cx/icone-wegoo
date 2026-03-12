import requests
import re
from datetime import datetime
import os

# إعدادات
DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN')
# كيجيب التاريخ ديال اليوم أوتوماتيكيا (YYYY-MM-DD)
today = datetime.now().strftime('%Y-%m-%d')
URL = f"https://testious.com/old-free-cccam-servers/{today}/"

def scrape_and_upload():
    headers = {'User-Agent': 'Mozilla/5.0'}
    print(f"Connecting to: {URL}")
    
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        # البحث عن السيرفرات الشغالة فقط [OK]
        matches = re.findall(r'C:\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+([^\s]+).*?OK', response.text, re.IGNORECASE)
        
        if not matches:
            print("No active servers found today.")
            return

        config_data = ""
        for i, (host, port, user, pwd) in enumerate(matches):
            config_data += f"[reader]\nlabel = Testious_OK_{i+1}\nprotocol = cccam\ndevice = {host},{port}\nuser = {user}\npassword = {pwd}\ngroup = 1\nroot = 1\ndisablecrccws = 1\nccckeepalive = 1\naudisabled = 1\n\n"

        # الرفع لـ Dropbox (Overwrite للملف القديم)
        dbx_url = "https://content.dropboxapi.com/2/files/upload"
        dbx_headers = {
            "Authorization": f"Bearer {DROPBOX_TOKEN}",
            "Dropbox-API-Arg": '{"path": "/ncam.server","mode": "overwrite"}',
            "Content-Type": "application/octet-stream"
        }
        r = requests.post(dbx_url, headers=dbx_headers, data=config_data.encode('utf-8'))
        
        if r.status_code == 200:
            print(f"✅ Success! {len(matches)} servers uploaded to Dropbox.")
        else:
            print(f"❌ Dropbox Error: {r.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scrape_and_upload()
