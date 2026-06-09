import re

with open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_Index.htm', 'r', encoding='utf-8') as f:
    text = f.read()

subname = re.search(r'<span class="org-subname">.*?</span>', text)
if subname:
    print('Arabic Subname:', subname.group(0))

footer = re.search(r'<p class="footer-note">.*?</p>', text)
if footer:
    print('Arabic Footer:', footer.group(0))
    
with open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\index.htm', 'r', encoding='utf-8') as f:
    text_en = f.read()

subname_en = re.search(r'<span class="org-subname">.*?</span>', text_en)
if subname_en:
    print('English Subname:', subname_en.group(0))

footer_en = re.findall(r'<p class="footer-note".*?>.*?</p>', text_en)
for f in footer_en:
    print('English Footer:', f)

