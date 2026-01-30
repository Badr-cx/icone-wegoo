import requests
import re

URLS = [
    "ضع_هنا_روابط_المواقع"
]

def run_scraper():
    results = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in URLS:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            
            # 1. استخراج أسطر CCcam (C: Host Port User Pass)
            # يتعامل مع النقط، العوارض، والآي بي
            cccam_pattern = r'C:\s*([^\s<]+)\s+(\d+)\s+([^\s<]+)\s+([^\s<]+)'
            cccam_found = re.findall(cccam_pattern, r.text)
            for m in cccam_found:
                results.append(f"C: {m[0]} {m[1]} {m[2]} {m[3]}")

            # 2. استخراج أسطر Newcamd (N: Host Port User Pass DESKey)
            # DESKey غالباً ما يكون من 01 إلى 14
            newcamd_pattern = r'N:\s*([^\s<]+)\s+(\d+)\s+([^\s<]+)\s+([^\s<]+)\s+(01\s*02.*?14)'
            newcamd_found = re.findall(newcamd_pattern, r.text)
            for m in newcamd_found:
                des_key = m[4].replace(" ", "") # تنظيف المسافات في DES Key
                formatted_des = " ".join([des_key[i:i+2] for i in range(0, len(des_key), 2)])
                results.append(f"N: {m[0]} {m[1]} {m[2]} {m[3]} {formatted_des}")

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            continue
    
    # تنقية وحفظ الملف
    with open("CCcam.cfg", "w") as f:
        f.write("# Updated by Badr-cx System\n# Includes CCcam and Newcamd\n\n")
        f.write("\n".join(sorted(list(set(results)))))

if __name__ == "__main__":
    run_scraper()
