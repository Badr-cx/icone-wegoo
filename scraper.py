import requests
import re

URLS = [
    "https://thecccam.com/cccam-free.php",
    "https://bosscccam.co/Test.php",
    "https://cccamsiptv.com/cccamfree/get.php",
    "https://mycccam.shop/free-cccam.php",
    "https://cccam.zone/FREEN12/new0.php",
    "https://www.cccambird.com/freecccam.php"
]

def run_scraper():
    results = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for url in URLS:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            found = re.findall(r'C:\s*[^\s<]+ [^\s<]+ [^\s<]+ [^\s<]+', r.text)
            for line in found:
                clean = re.sub('<[^<]+?>', '', line).strip()
                if len(clean) > 10: results.append(clean)
        except: continue
    
    with open("CCcam.cfg", "w") as f:
        f.write("# Updated by Badr-cx\n")
        f.write("\n".join(sorted(list(set(results)))))

if __name__ == "__main__":
    run_scraper()
