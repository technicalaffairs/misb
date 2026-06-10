with open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\new_pages\Ar_ad_Batteries.htm', 'r', encoding='windows-1256') as f:
    text = f.read()
import re
p = re.search(r'<p dir="ltr">.*?<span[^>]*>(.*?)</span>', text, re.IGNORECASE | re.DOTALL)
if p: print(p.group(1))
