import re
import os

def decoder_machine():
    # هاد الجزء كيقرا النص اللي غاتحطو نتا فملف سميتو source.txt
    # (تقدر تحط فيه الرموز، السطور، أي حاجة)
    source_file = "source.txt"
    
    if not os.path.exists(source_file):
        with open(source_file, "w") as f:
            f.write("# حط الرموز أو السطور هنا")
        print(f"⚠️ حط الرموز فـ ملف {source_file} أولا!")
        return

    with open(source_file, "r", encoding="utf-8", errors="ignore") as f:
        raw_data = f.read()

    # هادي هي "الفكاكة": كتقلب على أي حاجة كتشبه لسطر CCcam وسط الرموز
    # كتجبد: الهوست، البورت، اليوزر، الباص
    pattern = r'([a-zA-Z0-9\.-]+\.[a-z]{2,})\s*[\s,:]\s*(\d{4,5})\s+([a-zA-Z0-9\._-]+)\s+([a-zA-Z0-9\._-]+)'
    matches = re.findall(pattern, raw_data)

    config_template = """[reader]
label                         = Extracted_Server_{index}
protocol                      = cccam
device                        = {host},{port}
user                          = {user}
password                      = {pwd}
group                         = 1
root                          = 1
inactivitytimeout             = 30
reconnecttimeout              = 2
disablecrccws                 = 1
cccversion                    = 2.3.2
ccckeepalive                  = 1
audisabled                    = 1

"""

    final_content = ""
    for i, (host, port, user, pwd) in enumerate(matches):
        final_content += config_template.format(index=i+1, host=host, port=port, user=user, pwd=pwd)

    if final_content:
        with open("ncam.server", "w") as f:
            f.write(final_content)
        print(f"✅ ناضي! جبدت {len(matches)} سيرفر من وسط الرموز وحولتهم.")
    else:
        print("❌ مالقيت حتى سيرفر، تأكد بلي السطور واضحة وسط الرموز.")

if __name__ == "__main__":
    decoder_machine()
