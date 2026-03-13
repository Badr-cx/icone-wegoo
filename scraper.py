import requests
import re
from datetime import datetime

# كيجيب التاريخ ديال اليوم أوتوماتيكياً
today = datetime.now().strftime('%Y-%m-%d')
URL = f"https://testious.com/old-free-cccam-servers/{today}/"

def scrape_to_star_c():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        
        # كيجلب السيرفرات اللي حداهم [OK] لضمان القوة
        matches = re.findall(r'C:\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+([^\s]+).*?\[OK\]', response.text, re.IGNORECASE)
        
        final_content = ""
        
        if matches:
            for host, port, user, pwd in matches:
                # التنسيق اللي طلبتي بضبط مع الكومنت فالاخير
                final_content += f"C: {host} {port} {user} {pwd} # v2.0.11-2892\n"
            
            print(f"✅ Done! {len(matches)} Servers generated in Star C format.")
        else:
            # إيلا مالقاش [OK] كيهز العاديين
            print("⚠️ No [OK] found, fetching available ones...")
            matches_all = re.findall(r'C:\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+([^\s]+)', response.text, re.IGNORECASE)
            for host, port, user, pwd in matches_all[:15]:
                final_content += f"C: {host} {port} {user} {pwd} # v2.0.11-2892\n"

        # حفظ النتيجة فـ ncam.server
        with open("ncam.server", "w") as f:
            f.write(final_content)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scrape_to_star_c()
