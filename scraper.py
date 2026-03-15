import scrapy
from scrapy.crawler import CrawlerProcess
import re
import os

class CccamSpider(scrapy.Spider):
    name = 'cccam_spider'
    
    # الرابط ديال الموقع
    start_urls = ['https://cccamia.com/cccamfree1/']

    custom_settings = {
        # إعدادات البروكسي (Privoxy اللي مربوط بـ Tor)
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        },
        # هاد البورت 8118 هو ديال Privoxy اللي غديرو ف الـ YAML
        'HTTP_PROXY': 'http://127.0.0.1:8118',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'LOG_LEVEL': 'INFO',
    }

    def parse(self, response):
        self.logger.info(f"Connecting to site via Tor... Status: {response.status}")
        
        # كنقلبو فـ السورس ديال الصفحة على السطر (Format: C: host port user pass)
        page_text = response.text
        # Regex محكم باش يجيب البيانات كاملة
        match = re.search(r'C:\s+([^\s]+)\s+(\d+)\s+([^\s]+)\s+([^\s]+)', page_text)

        if match:
            host, port, user, password = match.groups()
            self.logger.info(f"✅ Found Line: {host}:{port}")
            self.generate_ncam_file(host, port, user, password)
        else:
            self.logger.error("❌ Line not found! Site might be using JavaScript to hide the line.")
            # كنحفظو الصفحة للتأكد (Debug)
            with open("debug_page.html", "w", encoding='utf-8') as f:
                f.write(page_text)

    def generate_ncam_file(self, host, port, user, password):
        # إعداد محتوى ملف ncam.server
        config_content = f"""[reader]
label                         = CCCam_Scrapy_Tor
protocol                      = cccam
device                        = {host},{port}
user                          = {user}
password                      = {password}
group                         = 1
cccversion                    = 2.3.2
ccckeepalive                  = 1
"""
        # حفظ الملف
        with open("ncam.server", "w") as f:
            f.write(config_content)
        self.logger.info("📂 ncam.server has been updated successfully!")

# تشغيل الـ Spider
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(CccamSpider)
    process.start()
