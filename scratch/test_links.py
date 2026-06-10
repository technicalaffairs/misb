with open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_Index.htm', 'r', encoding='utf-8') as f:
    text = f.read()
import re
nav = re.search(r'<nav class="main-nav">(.*?)</nav>', text, re.DOTALL)
if nav:
    for a in re.findall(r'<a.*?</a>', nav.group(1), re.DOTALL):
        print(a.strip())
