import requests
import re

URLS = [
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "http://cccam24h.com/lik1.php",
    "https://bosscccam.co/Test.php",
    "https://thecccam.com/cccam-free.php",
    "https://cccamprime.com/cccam48h.php",
    "https://www.tvlivepro.com/free_cccam_48h/"
]

def run_scraper():
    results = []
    # هاد الـ User-Agent كيخليك تبان بحال إنسان حقيقي في 2026
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
    }

    for url in URLS:
        try:
            print(f"Fetching: {url}")
            r = requests.get(url, headers=headers, timeout=15)
            # Regex مطور كايجيب حتى السطور اللي فيها رموز خاصة
            pattern = r'[CN]:\s*([^\s<|]+)\s+(\d+)\s+([^\s<|]+)\s+([^\s<|]+)'
            matches = re.findall(pattern, r.text)
            
            for m in matches:
                # كايعرف واش السطر C أو N من أول حرف في البحث
                prefix = "C" if "C:" in r.text[:100] else "C" # افتراضياً C
                results.append(f"C: {m[0]} {m[1]} {m[2]} {m[3]}")
        except:
            continue

    unique_lines = sorted(list(set(results)))
    with open("CCcam.cfg", "w") as f:
        f.write(f"# Badr-cx 2026 Global Scraper\n# Found: {len(unique_lines)}\n\n")
        f.write("\n".join(unique_lines))
    print(f"Done! {len(unique_lines)} servers found.")

if __name__ == "__main__":
    run_scraper()
