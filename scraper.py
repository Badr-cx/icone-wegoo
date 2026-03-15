import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def get_line():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # الخدمة فـ الخلفية
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://cccamia.com/cccamfree1/")
        
        # التورك على الزر الأزرق "GET MY FREE C-LINE NOW"
        wait = WebDriverWait(driver, 20)
        button = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "GET MY FREE")))
        button.click()
        
        # الانتظار حتى يظهر السطر (غالباً كيكون فيه C: host port user pass)
        page_source = driver.page_source
        match = re.search(r'C:\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+([^\s]+)', page_source)
        
        if match:
            host, port, user, password = match.groups()
            ncam_config = f"""
[reader]
label                         = CCCam_Free_Auto
protocol                      = cccam
device                        = {host},{port}
user                          = {user}
password                      = {password}
group                         = 1
cccversion                    = 2.3.2
ccckeepalive                  = 1
"""
            with open("ncam.server", "w") as f:
                f.write(ncam_config)
            print("Done: ncam.server updated!")
        else:
            print("Error: Could not find the C-line pattern.")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    get_line()
