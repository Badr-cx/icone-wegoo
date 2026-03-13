import requests
import re
from datetime import datetime

# كيجيب التاريخ ديال اليوم أوتوماتيكياً
today = datetime.now().strftime('%Y-%m-%d')
URL = f"https://testious.com/old-free-cccam-servers/{today}/"

def scrape_to_ncam():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        
        # التعديل هنا: السكريبت غايقلب دابا غير على السطورة اللي كيساليو بـ [OK]
        # هادي هي الطريقة باش كنجيبو أقوى السيرفرات اللي ديجا تيستاهوم الموقع
        matches = re.findall(r'C:\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+([^\s]+).*?\[OK\]', response.text, re.IGNORECASE)
        
        config_template = """[reader]
label                         = OrcaGold_Server_{index}
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
                final_content += config_template.format(
                    index=i+1,
                    host=host,
                    port=port,
                    user=user,
                    pwd=pwd
                )
            print(f"✅ Success! Found {len(matches)} ACTIVE servers [OK].")
        else:
            # إيلا مالقاش [OK]، كيجيب السيرفرات العاديين باش ما يبقاش الملف خاوي
            print("⚠️ No [OK] servers found, fetching available ones...")
            matches_all = re.findall(r'C:\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+([^\s]+)', response.text, re.IGNORECASE)
            for i, (host, port, user, pwd) in enumerate(matches_all[:10]): # ناخدو أحسن 10
                final_content += config_template.format(index=i+1, host=host, port=port, user=user, pwd=pwd)

        with open("ncam.server", "w") as f:
            f.write(final_content)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scrape_to_ncam()
