import re

def decrypt_and_format():
    # هاد المتغير فيه الرموز اللي صيفطتي (raw data)
    raw_symbols = """
    §éõ<¶NÒzœ[>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
    """

    # الفلتر: كينبش ف وسط الرموز ويجبد غير الهوست والبورت والباص
    pattern = r'([a-zA-Z0-9.-]+\.[a-z]{2,})\s*,?\s*(\d{4,5})\s+([a-zA-Z0-9._-]+)\s+([a-zA-Z0-9._-]+)'
    matches = re.findall(pattern, raw_symbols)

    reader_template = """[reader]
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

    final_output = ""
    for i, (host, port, user, pwd) in enumerate(matches):
        final_output += reader_template.format(index=i+1, host=host, port=port, user=user, pwd=pwd)

    # حفظ النتيجة فـ الملف
    with open("ncam.server", "w") as f:
        f.write(final_output)
    
    print(f"✅ تم فك الرموز واستخراج {len(matches)} سيرفرات بنجاح!")

if __name__ == "__main__":
    decrypt_and_format()
