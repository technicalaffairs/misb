import re

with open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_Index.htm', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'<a href=\"([^\"]+)\"[^>]*>(.*?)</a>', text, re.DOTALL)
for u, c in matches:
    if 'Protection' in c or 'Transmission' in c or 'Communications' in c or 'Cathode' in c or 'الإطفاء' in c or 'الوقاية' in c or 'التحكم' in c or 'الاتصالات' in c:
        print(u, '->', re.sub(r'<[^>]+>', '', c).strip())
