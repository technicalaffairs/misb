import os, glob, re
base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
arabic_web_dir = os.path.join(base_dir, 'arabic_web')

for fp in glob.iglob(arabic_web_dir + r'\Ar_appr_docs\**\*.htm*', recursive=True):
    if 'scratch' in fp or '_vti' in fp: continue
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        continue
    
    m = re.search(r'<h1 style="color: #d9534f[^"]*">(.*?)</h1>', content)
    if m:
        title = m.group(1).strip()
        if re.search(r'[a-zA-Z]', title):
            print(os.path.relpath(fp, arabic_web_dir), '->', title)
