import requests
import re

def scrape_servers():
    # المصادر اللي كنجبدو منها
    sources = [
        "https://cccamcard.com/free-cccam-server.php",
        "https://clinetest.net/free_cccam.php",
        "https://raw.githubusercontent.com/yebekhe/TVHub/main/pannels/channels.txt"
    ]
    
    all_found = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in sources:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            # هاد الكود السحري كيجلب أي سطر كيبدأ بـ C: أو N: متبوع بـ host port user pass
            matches = re.findall(r'([CN]:\s?\S+\s\d+\s\S+\s\S+)', r.text)
            all_found.extend(matches)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            continue

    # تنقية الأسطر من أي فراغات زائدة وتجنب التكرار
    clean_all = list(set([s.strip() for s in all_found if len(s) > 10]))

    # حفظ الملف
    with open("CCcam.cfg", "w") as f:
        for s in clean_all:
            f.write(s + "\n")
        # إذا بغيتي تزيد السيرفر ديالك الخاص ديما في الأخير
        f.write("C: 151.115.73.226 12001 west bestpsw\n")

    print(f"Success! {len(clean_all)} servers saved to CCcam.cfg")

if __name__ == "__main__":
    scrape_servers()
