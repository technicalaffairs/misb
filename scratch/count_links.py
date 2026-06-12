import re

content = open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_gen_docs\Ar_Boilers_docs Page.htm', encoding='utf-8', errors='ignore').read()
links = re.findall(r'href="(../../gen_docs/[^"]+)"', content)
print(f"Total English links in Boilers index: {len(set(links))}")
