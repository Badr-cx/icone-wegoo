import requests
import re

# هادو هما الروابط اللي صيفطتي + روابط عالمية إضافية
URLS = [
    "https://cccam.premium.pro/free-cccam/",
    "https://cccam.net/free",
    "https://cccamia.com/free-cccam/",
    "https://www.cccambird.com/freecccam.php",
    "https://www.cccambird2.com/freecccam.php",
    "https://cccamprime.com/cccam48h.php",
    "https://skyhd.xyz/freetest/osm.php",
    "https://www.tvlivepro.com/free_cccam_48h/",
    "https://dhoom.org/test/",
    "https://raw.githubusercontent.com/yebekhe/TV-Logo/main/cccam.txt",
    "https://thecccam.com/cccam-free.php"
]

def run_scraper():
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for url in URLS:
        try:
            print(f"Searching in: {url}")
            r = requests.get(url, headers=headers, timeout=20)
            
            # رادار البحث عن أسطر CCcam
            cccam_pattern = r'C:\s*([^\s<|]+)\s+(\d+)\s+([^\s<|]+)\s+([^\s<|]+)'
            # رادار البحث عن أسطر Newcamd
            new_pattern = r'N:\s*([^\s<|]+)\s+(\d+)\s+([^\s<|]+)\s+([^\s<|]+)\s+(01\s*02.*?14)'

            # جمع أسطر C:
            for m in re.findall(cccam_pattern, r.text):
                results.append(f"C: {m[0]} {m[1]} {m[2]} {m[3]}")

            # جمع أسطر N:
            for m in re.findall(new_pattern, r.text):
                des = re.sub(r'\s+', ' ', m[4]).strip()
                results.append(f"N: {m[0]} {m[1]} {m[2]} {m[3]} {des}")

        except Exception as e:
            print(f"Error in {url}: {e}")
            continue
    
    # مسح المكرر وتصفية الأسطر
    unique_results = sorted(list(set(results)))
    
    with open("CCcam.cfg", "w") as f:
        f.write(f"# Updated by Badr-cx System | Total: {len(unique_results)}\n")
        f.write("# Includes CCcam and Newcamd from Global Sources\n\n")
        if unique_results:
            f.write("\n".join(unique_results))
        else:
            f.write("# No servers found, checking again in 6 hours.")
            
    print(f"Done! Found {len(unique_results)} servers.")

if __name__ == "__main__":
    run_scraper()
