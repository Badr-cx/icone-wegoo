import cloudscraper
import re

# الروابط القوية التي اخترتها
URLS = [
    "https://cccam.net/freecccam",
    "https://cccamia.com/cccamfree1/",
    "https://www.cccampri.me/cccam24h.php",
    "https://cccam-premium.pro/free-cccam/",
    "http://cccam24h.com/lik1.php"
]

def run_scraper():
    results = []
    # محاكاة متصفح حقيقي لتخطي Cloudflare
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )

    for url in URLS:
        try:
            print(f"جاري استخراج السيرفرات من: {url}")
            r = scraper.get(url, timeout=30)
            
            # رادار ذكي لاستخراج أسطر C: و N:
            pattern = r'([CN]:\s*[^\s<|]+(?:\s+[^\s<|]+){3})'
            matches = re.findall(pattern, r.text, re.IGNORECASE)
            
            for line in matches:
                # تنظيف السطر من أي وسم HTML
                clean = re.sub('<[^<]+?>', '', line).strip()
                if len(clean) > 15:
                    results.append(clean)
        except Exception as e:
            print(f"فشل الموقع {url}: {e}")
            continue

    # إزالة التكرار
    unique_results = sorted(list(set(results)))
    
    with open("CCcam.cfg", "w") as f:
        f.write(f"# Updated by Badr-cx System | 2026-01-30\n")
        f.write(f"# Total Servers Found: {len(unique_results)}\n\n")
        if unique_results:
            f.write("\n".join(unique_results))
        else:
            f.write("# No servers found. Check site availability.")
            
    print(f"تم العثور على {len(unique_results)} سيرفر بنجاح!")

if __name__ == "__main__":
    run_scraper()
