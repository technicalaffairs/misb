import os, glob, re

search_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web'

files = list(glob.iglob(search_dir + '/**/*.htm', recursive=True))

logo_pattern = r'\s*<img[^>]*src="[^"]*eehc_logo\.gif"[^>]*>'
email_pattern = r'\s*<div class="contact-item">\s*<i class="fa-solid fa-envelope"></i>\s*<a href="mailto:mpisgd@hotmail\.com">mpisgd@hotmail\.com</a>\s*</div>'

for fp in files:
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig = content
        content = re.sub(logo_pattern, '', content, flags=re.IGNORECASE)
        content = re.sub(email_pattern, '', content, flags=re.IGNORECASE)
        
        if content != orig:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Updated:", fp)
    except:
        pass
