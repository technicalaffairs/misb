import re

with open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_Index.htm', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract all links that go up a directory (outside arabic_web)
matches = re.findall(r'<a href=\"\.\./([^\"]+)\"[^>]*>(.*?)</a>', text, re.DOTALL)

outside_links = []
for url, content in matches:
    if url == 'index.htm': continue # Language toggle
    content_clean = re.sub(r'<[^>]+>', '', content).strip()
    outside_links.append((url, content_clean))

for u, c in outside_links:
    print(f'{u} -> {c}')
print('Total outside links:', len(outside_links))
