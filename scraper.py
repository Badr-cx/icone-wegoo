import requests
import re
from datetime import datetime
import os

# رابط اليوم من موقع Testious
today = datetime.now().strftime('%Y-%m-%d')
URL = f"https://testious.com/old-free-cccam-servers/{today}/"

def scrape_to_ncam():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        # جلب الهوست والبورت واليوزر والباص
        matches = re.findall(r'C:\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+([^\s]+)', response.text, re.IGNORECASE)
        
        # الإعدادات اللي طلبتيها (الزربة والثبات)
        config_template = """[reader]
label                         = {label}
protocol                      = cccam
device                        = {host},{port}
user                          = {user}
password                      = {pwd}
group                         = 1
root                          = 1
inactivitytimeout             = 30
reconnecttimeout              = 2
disablecrccws                 = 1
cccversion                    = 2.3.2
ccckeepalive                  = 1
audisabled                    = 1

"""
        
        final_content = ""
        
        if matches:
            for i, (host, port, user, pwd) in enumerate(matches):
                # كيطبق القالب على كل سيرفر لقى
                final_content += config_template.format(
                    label=f"OrcaGold_Server_{i+1}",
                    host=host,
                    port=port,
                    user=user,
                    pwd=pwd
                )
        else:
            final_content = "# No servers found for today yet\n"

        # حفظ النتيجة في الملف اللي غيقرأه البلوجين
        with open("ncam.server", "w") as f:
            f.write(final_content)
        
        print(f"✅ Created ncam.server with {len(matches)} servers in Dhoom format.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scrape_to_ncam()
