import os, re, shutil

filepath = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_gen_docs\Ar_Gas Turbines_docs Page.htm'
base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_gen_docs'

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

hrefs = re.findall(r'href=[\'\"]([^\'\"]+-r0a\.htm)[\'\"]', text, re.IGNORECASE)

copied = 0
for h in hrefs:
    abs_a_path = os.path.normpath(os.path.join(base_dir, h))
    if not os.path.exists(abs_a_path):
        # The english file should exist
        abs_eng_path = abs_a_path.replace('-r0a.htm', '-r0.htm').replace('-R0a.htm', '-R0.htm').replace('-r0a.HTM', '-r0.HTM')
        if os.path.exists(abs_eng_path):
            shutil.copy2(abs_eng_path, abs_a_path)
            copied += 1
            print(f'Copied {os.path.basename(abs_eng_path)} to {os.path.basename(abs_a_path)}')

print(f'Total copied: {copied}')
