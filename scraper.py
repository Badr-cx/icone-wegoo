import requests, re

def hunt_from_checker():
    # هاد الرابط هو اللي كيكونوا فيه النتائج المباشرة
    url = "https://clinetest.net/free_cccam.php"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://clinetest.net/'
    }

    try:
        # كانديرو Session باش نحافظوا على الـ Cookies
        with requests.Session() as s:
            response = s.get(url, headers=headers, timeout=15, verify=False)
            
            # هنا كنقلبو على السطور اللي وسط الـ HTML
            # بزاف د المرات كيكونوا مخبين وسط <td> أو <textarea>
            found = re.findall(r'C:\s*[a-zA-Z0-9\-\.]+\s+\d+\s+\S+\s+\S+', response.text, re.I)
            
            if found:
                print(f"✅ Found {len(found)} servers from Clinetest!")
                return list(set(found))
            else:
                print("⚠️ No servers visible on the page (maybe protected).")
                return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

# جرب هاد الفونكسيون وشوف واش غتجبد ليك شي حاجة
servers = hunt_from_checker()
