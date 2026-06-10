import os, re
with open(r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_gen_docs\Ar_Gas Turbines_docs Page.htm', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

hrefs = re.findall(r'href=[\'\"]([^\'\"]+-r0\.htm)[\'\"]', text, re.IGNORECASE)

filenames = [os.path.basename(h) for h in hrefs]
filenames = list(set(filenames)) # unique

base = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
all_a_files = {}
for root, dirs, files in os.walk(base):
    if '_vti_cnf' in root: continue
    for f in files:
        if f.lower().endswith('a.htm'):
            all_a_files[f.lower()] = os.path.join(root, f)

found = 0
for fn in filenames:
    a_fn = fn.lower().replace('-r0.htm', '-r0a.htm')
    if a_fn in all_a_files:
        found += 1
        print('Found:', a_fn, 'at', all_a_files[a_fn])

print(f'Total existing: {found} out of {len(filenames)} unique links')
