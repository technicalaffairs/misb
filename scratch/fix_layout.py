import os, glob, re

search_dir_en = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'

files = list(glob.iglob(search_dir_en + '/**/*.htm', recursive=True)) + list(glob.iglob(search_dir_en + '/**/*.html', recursive=True))

for fp in files:
    if 'scratch' in fp or '_vti_cnf' in fp: continue
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig = content
        
        # Remove the rogue </div> before lang-switch
        content = re.sub(r'<div class="top-bar">\s*</div>\s*<a href', r'<div class="top-bar">\n      <a href', content, flags=re.IGNORECASE|re.DOTALL)
        
        if content != orig:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)
            print('Fixed layout in:', fp)
    except Exception as e:
        pass
