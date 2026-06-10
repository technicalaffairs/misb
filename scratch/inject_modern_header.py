import os
import re
import urllib.parse

base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
arabic_web_dir = os.path.join(base_dir, 'arabic_web')
ar_index_path = os.path.join(arabic_web_dir, 'Ar_Index.htm')

# 1. Extract modern header components from Ar_Index.htm
with open(ar_index_path, 'r', encoding='utf-8') as f:
    index_html = f.read()

fontawesome_link = r'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'
style_match = re.search(r'<style>.*?</style>', index_html, re.DOTALL)
modern_style = style_match.group(0) if style_match else ''

header_match = re.search(r'<div class="top-bar">.*?</nav>', index_html, re.DOTALL)
modern_header_base = header_match.group(0) if header_match else ''

def adjust_links(html_chunk, current_file_path):
    # Adjust href="..." and src="..."
    def replacer(match):
        attr = match.group(1) # href or src
        url = match.group(2)
        if url.startswith('http') or url.startswith('mailto') or url.startswith('#') or url == '':
            return match.group(0)
            
        # url is relative to arabic_web_dir
        # resolve absolute path
        abs_target = os.path.normpath(os.path.join(arabic_web_dir, urllib.parse.unquote(url).replace('/', '\\')))
        # relative path from current file
        rel_target = os.path.relpath(abs_target, os.path.dirname(current_file_path)).replace('\\', '/')
        return f'{attr}="{urllib.parse.quote(rel_target)}"'
        
    return re.sub(r'(href|src)=[\'\"]([^\'\"]+)[\'\"]', replacer, html_chunk, flags=re.IGNORECASE)

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

            # 2. Locate the old header table
            table_match = re.search(r'<table[^>]*>.*?</table>', content, re.IGNORECASE | re.DOTALL)
            if not table_match:
                continue
                
            old_header = table_match.group(0)
            if 'mpis-22.gif' not in old_header and 'الرئيسية' not in old_header:
                continue
                
            # 3. Extract the red title
            title_match = re.search(r'<font[^>]*color=[\'\"]#FF0000[\'\"][^>]*>(.*?)</font>', old_header, re.IGNORECASE | re.DOTALL)
            if not title_match:
                title_match = re.search(r'<big>\s*<big>\s*<big>(.*?)</big>\s*</big>\s*</big>', old_header, re.IGNORECASE | re.DOTALL)
                
            extracted_title = ""
            if title_match:
                extracted_title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
                
            # 4. Extract banner
            has_banner = 'مستندات معتمدة' in old_header or 'APPROVED DOCUMENTS' in old_header
            
            banner_html = ""
            if has_banner:
                banner_html = '<h2 style="color: #d9534f; border-bottom: 2px solid #d9534f; padding-bottom: 10px; display: inline-block; font-family: \'Cairo\', sans-serif;">مستندات معتمدة</h2>'

            # 5. Build new title HTML
            title_html = f'''
            <div style="text-align: center; margin: 30px auto; max-width: 800px; padding: 0 20px;">
                <h1 style="color: #d9534f; font-weight: 700; margin-bottom: 10px; font-family: 'Cairo', sans-serif;">{extracted_title}</h1>
                {banner_html}
            </div>
            '''
            
            # 6. Adjust links in modern header
            modern_header = adjust_links(modern_header_base, filepath)
            
            # 7. Inject into content
            content = content.replace(old_header, modern_header + '\n' + title_html)
            
            if fontawesome_link not in content:
                content = re.sub(r'</head>', f'{fontawesome_link}\n{modern_style}\n</head>', content, flags=re.IGNORECASE)
                
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
                
            updated_files += 1
            print(f'Updated {os.path.relpath(filepath, arabic_web_dir)}')

print(f'Total files updated: {updated_files}')
