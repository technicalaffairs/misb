import os
import re

base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
arabic_web_dir = os.path.join(base_dir, 'arabic_web')
ar_index_path = os.path.join(arabic_web_dir, 'Ar_Index.htm')

updated_files = 0

for root, dirs, files in os.walk(arabic_web_dir):
    for f in files:
        if f.endswith('.htm') or f.endswith('.html'):
            filepath = os.path.join(root, f)
            if filepath == ar_index_path or 'scratch' in filepath or 'Ar_index_old' in filepath:
                continue
                
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
            except UnicodeDecodeError:
                try:
                    with open(filepath, 'r', encoding='windows-1256') as file:
                        content = file.read()
                except: continue

            if '<div class="top-bar">' not in content:
                continue

            updated = False

            # 1. Strip body attributes
            new_content = re.sub(r'<body[^>]*>', '<body>', content, flags=re.IGNORECASE)
            if new_content != content:
                content = new_content
                updated = True

            # 2. Wrap header in app-container if not already wrapped
            # Check if it's already wrapped
            if '<div class="app-container">\n<div class="top-bar">' not in content:
                def wrap_header(match):
                    return '<div class="app-container">\n' + match.group(0) + '\n</div>'
                    
                new_content = re.sub(r'(<div class="top-bar">.*?</nav>)', wrap_header, content, flags=re.IGNORECASE | re.DOTALL)
                if new_content != content:
                    content = new_content
                    updated = True
                    
            if updated:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                updated_files += 1
                print(f'Fixed layout in {os.path.relpath(filepath, arabic_web_dir)}')

print(f'Total files fixed: {updated_files}')
