import re
with open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_Index.htm', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'<a href=\"([^\"]+)\"[^>]*>(.*?)</a>', text, re.DOTALL)
for u, c in matches:
    if 'التوربينات' in c or 'المراوح' in c or 'الوقاية' in c:
        print(re.sub(r'<[^>]+>', '', c).strip())
