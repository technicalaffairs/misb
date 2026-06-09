import re

with open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_index_old.htm', 'r', encoding='windows-1256') as f:
    text = f.read()

matches = re.findall(r'<a href=\"([^\"]+)\"[^>]*>(.*?)</a>', text, re.DOTALL)
for url, content in matches:
    if 'gen_docs' in url:
        print('gen_docs url:', url)
