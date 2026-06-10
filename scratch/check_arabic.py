import os, re
with open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_gen_docs\Ar_Gas Turbines_docs Page.htm', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

hrefs = re.findall(r'href=[\'\"]([^\'\"]+-r0\.htm)[\'\"]', text, re.IGNORECASE)

base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_gen_docs'
exists_count = 0
for h in hrefs:
    a_link = h.replace('-r0.htm', '-r0a.htm')
    abs_path = os.path.normpath(os.path.join(base_dir, a_link))
    if os.path.exists(abs_path):
        exists_count += 1

print(f'Out of {len(hrefs)} links, {exists_count} have an Arabic version.')
