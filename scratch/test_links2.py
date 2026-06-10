with open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_Index.htm', 'r', encoding='utf-8') as f:
    text = f.read()
import re
m = re.search(r'نقل الطاقة، التحكم والوقاية', text)
print('Found:', m is not None)
if m:
    idx = m.end()
    snippet = text[idx:idx+2000]
    links = re.findall(r'<a href="([^"]+)".*?>\s*(?:<i.*?></i>)?\s*(.*?)</a>', snippet, re.IGNORECASE | re.DOTALL)
    for href, name in links:
        print(f'{name.strip()} -> {href}')
