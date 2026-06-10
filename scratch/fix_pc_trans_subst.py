import os, re, urllib.parse

base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
arabic_web_dir = os.path.join(base_dir, 'arabic_web')
ar_index_path = os.path.join(arabic_web_dir, 'Ar_Index.htm')

with open(ar_index_path, 'r', encoding='utf-8') as f:
    index_html = f.read()

modern_header_base = re.search(r'<div class="top-bar">.*?</nav>', index_html, re.DOTALL).group(0)
style_match = re.search(r'<style>.*?</style>', index_html, re.DOTALL)
modern_style = style_match.group(0)

def adjust_links(html_chunk, current_file_path):
    def replacer(match):
        attr = match.group(1)
        url = match.group(2)
        if url.startswith('http') or url.startswith('mailto') or url.startswith('#') or url == '': return match.group(0)
        abs_target = os.path.normpath(os.path.join(arabic_web_dir, urllib.parse.unquote(url).replace('/', '\\')))
        rel_target = os.path.relpath(abs_target, os.path.dirname(current_file_path)).replace('\\', '/')
        return f'{attr}="{urllib.parse.quote(rel_target)}"'
    return re.sub(r'(href|src)=[\'\"]([^\'\"]+)[\'\"]', replacer, html_chunk, flags=re.IGNORECASE)

files_to_process = [
    r'Ar_appr_docs\Ar_ad_pc\Ar_ad_pc.htm',
    r'Ar_appr_docs\Ar_ad_trans\Ar_ad_trans.htm',
    r'Ar_appr_docs\Ar_ad_subst\Ar_ad_subst.htm',
]

for t in files_to_process:
    filepath = os.path.join(arabic_web_dir, t)
    with open(filepath, 'r', encoding='windows-1256', errors='ignore') as f:
        text = f.read()
        
    if 'app-container' in text:
        continue

    rows = re.findall(r'(<tr.*?>.*?</tr>)', text, re.IGNORECASE | re.DOTALL)
    header_idx = -1
    for i, r in enumerate(rows):
        if '&#1578;&#1575;&#1585;&#1610;&#1582;' in r or '&#1575;&#1587;&#1600;&#1605;' in r or '&#1585;&#1602;&#1605;' in r or 'تاريخ' in r or 'المستند' in r:
            header_idx = i
            break
            
    if header_idx == -1:
        print(f'{t}: No header row found!')
        continue
        
    header_row = rows[header_idx]
    
    body_split = re.split(r'(<body[^>]*>)', text, maxsplit=1, flags=re.IGNORECASE)
    pre_body = body_split[0]
    body_tag = '<body dir="rtl">'
    post_body = body_split[2]
    
    idx = post_body.find(header_row)
    old_header_part = post_body[:idx]
    
    table_tag_match = re.search(r'<table[^>]*>', old_header_part, re.IGNORECASE)
    table_tag = table_tag_match.group(0) if table_tag_match else '<table border="1" cellspacing="1" width="100%">'
    
    title = 'محطات المحولات'
    if 'Ar_ad_trans' in filepath: title = 'الخطوط الهوائية'
    elif 'Ar_ad_pc' in filepath: title = 'أجهزة الوقاية'
    
    title_html = f'''
    <div style="text-align: center; margin: 30px auto; max-width: 800px; padding: 0 20px;">
        <h1 style="color: #d9534f; font-weight: 700; margin-bottom: 10px; font-family: 'Cairo', sans-serif;">{title}</h1>
    </div>
    '''
    
    modern_header = adjust_links(modern_header_base, filepath)
    
    # post_body[idx:] starts exactly with the <tr> of the document header
    new_post_body = f'\n<div class="app-container">\n{modern_header}\n</div>\n{title_html}\n{table_tag}\n{post_body[idx:]}'
    
    content = pre_body + body_tag + new_post_body
    
    # Inject styles if missing
    fontawesome_link = r'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'
    if fontawesome_link not in content:
        content = re.sub(r'</head>', f'{fontawesome_link}\n{modern_style}\n</head>', content, flags=re.IGNORECASE)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f'Processed {t} successfully!')
