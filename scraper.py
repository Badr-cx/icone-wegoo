import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_line():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # الربط مع تور
    chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Dakhlin l-site via Tor...")
        driver.get("https://cccamia.com/cccamfree1/")
        
        wait = WebDriverWait(driver, 30)
        
        # كليك على الزر الأزرق
        print("Searching for the blue button...")
        # جربنا نلقاو الزر بـ النص اللي فيه
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'GET MY FREE')]")))
        driver.execute_script("arguments[0].click();", button)
        
        print("Waiting for line generation...")
        time.sleep(15) # ضروري حيت الموقع ثقيل مع تور
        
        # البحث عن السطر
        source = driver.page_source
        match = re.search(r'C:\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+([^\s]+)', source)
        
        if match:
            h, p, u, ps = match.groups()
            ncam = f"[reader]\nlabel=CCCam_Tor\nprotocol=cccam\ndevice={h},{p}\nuser={u}\npassword={ps}\ngroup=1\ncccversion=2.3.2\nccckeepalive=1\n"
            with open("ncam.server", "w") as f:
                f.write(ncam)
            print("✅ ncam.server updated!")
        else:
            print("❌ Line not found in source.")
            driver.save_screenshot("debug.png") # كيسجل صورة يلا ما لقاش السطر

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    get_line()
