with open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_Index.htm', 'r', encoding='utf-8') as f:
    text = f.read()
import re
cats = re.findall(r'<a href="([^"]+)"[^>]*>\s*<span[^>]*>(.*?)</span>', text)
for href, title in cats:
    print(f'{title} -> {href}')
