import re

content = open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_gen_docs\Ar_Boilers_docs Page.htm', encoding='utf-8', errors='ignore').read()
links = set(re.findall(r'href="(../../gen_docs/[^"]+)"', content))

print(f"Total English links in Boilers index: {len(links)}")
for link in sorted(links):
    print(link)
