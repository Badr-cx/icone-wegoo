import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_line():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # إضافة User-Agent حقيقي باش نتفاداو الحجب
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print("جاري الدخول للموقع...")
        driver.get("https://cccamia.com/cccamfree1/")
        
        # الانتظار حتى تحمل الصفحة تماماً
        time.sleep(5) 

        wait = WebDriverWait(driver, 30)
        
        # محاولة الضغط على الزر باستخدام CSS Selector لأنه أدق
        print("البحث عن الزر الأزرق...")
        try:
            # كنقلبو على الزر اللي فيه النص GET MY FREE
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn-primary, .button, [href*='free']")))
            driver.execute_script("arguments[0].click();", button) # الضغط عن طريق JS أضمن
            print("تم الضغط على الزر بنجاح.")
        except:
            print("فشل العثور على الزر، كنحاول نطبع السورس للتأكد...")
        
        # تسنى شوية باش الصفحة الجديدة تحمل
        time.sleep(10)
        
        page_source = driver.page_source
        
        # البحث عن السطر (C-line) باستعمال Regex
        # هاد النمط كيقلب على C: host port user pass
        match = re.search(r'C:\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+([^\s]+)', page_source)
        
        if match:
            host, port, user, password = match.groups()
            print(f"تم إيجاد السطر: {host}")
            
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
            print("تم تحديث ملف ncam.server بنجاح!")
        else:
            print("لم يتم العثور على السطر في الصفحة. قد يكون الموقع يتطلب تخطي كابتشا يدوي.")
            # اختياري: حفظ صورة للصفحة للتأكد من المشكل (كتلقاها ف الـ artifacts)
            driver.save_screenshot("debug_screen.png")
            
    except Exception as e:
        print(f"حدث خطأ: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    get_line()
