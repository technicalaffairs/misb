import os
import re

cwd = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
arabic_web_dir = os.path.join(cwd, 'arabic_web')

def fix_rtl(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original = content
    # Replace dir="ltr" -> dir="rtl"
    content = re.sub(r'dir="ltr"', 'dir="rtl"', content, flags=re.IGNORECASE)
    # Replace align="left" -> align="right"
    content = re.sub(r'align="left"', 'align="right"', content, flags=re.IGNORECASE)
    # Replace direction: ltr -> direction: rtl
    content = re.sub(r'direction:\s*ltr', 'direction: rtl', content, flags=re.IGNORECASE)
    # Replace text-align: left -> text-align: right
    content = re.sub(r'text-align:\s*left', 'text-align: right', content, flags=re.IGNORECASE)
    # Add dir="rtl" to body if not present
    if '<body' in content and 'dir="rtl"' not in content.lower():
        content = re.sub(r'(<body\b[^>]*)>', r'\1 dir="rtl">', content, flags=re.IGNORECASE)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

updated_count = 0
for root, _, files in os.walk(arabic_web_dir):
    for f in files:
        if f.lower().endswith(('.htm', '.html')):
            path = os.path.join(root, f)
            if fix_rtl(path):
                updated_count += 1

print(f"Updated RTL settings in {updated_count} files.")
