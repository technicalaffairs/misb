import os, re, urllib.parse

base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
arabic_web_dir = os.path.join(base_dir, 'arabic_web')
ar_index_path = os.path.join(arabic_web_dir, 'Ar_Index.htm')

with open(ar_index_path, 'r', encoding='utf-8') as f:
    index_html = f.read()

fontawesome_link = r'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'
style_match = re.search(r'<style>.*?</style>', index_html, re.DOTALL)
modern_style = style_match.group(0) if style_match else ''
header_match = re.search(r'<div class="top-bar">.*?</nav>', index_html, re.DOTALL)
modern_header_base = header_match.group(0) if header_match else ''

def adjust_links(html_chunk, current_file_path):
    def replacer(match):
        attr = match.group(1)
        url = match.group(2)
        if url.startswith('http') or url.startswith('mailto') or url.startswith('#') or url == '': return match.group(0)
        abs_target = os.path.normpath(os.path.join(arabic_web_dir, urllib.parse.unquote(url).replace('/', '\\')))
        rel_target = os.path.relpath(abs_target, os.path.dirname(current_file_path)).replace('\\', '/')
        return f'{attr}="{urllib.parse.quote(rel_target)}"'
    return re.sub(r'(href|src)=[\'\"]([^\'\"]+)[\'\"]', replacer, html_chunk, flags=re.IGNORECASE)

def process_file(filepath, category_name=""):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding='windows-1256') as file:
                content = file.read()
        except: return
        
    if 'app-container' in content:
        # Already modernized
        return
        
    extracted_title = category_name
    old_header_to_remove = ""
    
    # Check for EEHC table
    eehc_table_match = re.search(r'<table[^>]*>.*?الشركة القابضة.*?</table>', content, re.IGNORECASE | re.DOTALL)
    if eehc_table_match:
        old_header_to_remove = eehc_table_match.group(0)
        # Try to extract title from this table or just after
        # Usually it has <big><big><big> or something similar
        title_match = re.search(r'<font[^>]*color=[\'\"]#FF0000[\'\"][^>]*>(.*?)</font>', old_header_to_remove, re.IGNORECASE | re.DOTALL)
        if not title_match:
            title_match = re.search(r'<big>\s*<big>\s*<big>(.*?)</big>\s*</big>\s*</big>', old_header_to_remove, re.IGNORECASE | re.DOTALL)
        if title_match and not extracted_title:
            extracted_title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
    else:
        # Look for the <p> tags with title, like in new_pages
        # <p ...>نظام معلومات إجراءات الصيانة — محطات المحولات</p>
        # <p ...>قضبان التوصيل (العملة) — سجل الوثائق المعتمدة</p>
        p_matches = re.finditer(r'<p[^>]*>.*?</p>', content, re.IGNORECASE | re.DOTALL)
        for m in p_matches:
            text = re.sub(r'<[^>]+>', '', m.group(0)).strip()
            if 'نظام معلومات إجراءات الصيانة' in text:
                old_header_to_remove += m.group(0)
            elif 'سجل الوثائق' in text or (text and len(text) < 100):
                old_header_to_remove += "\n" + m.group(0)
                if not extracted_title:
                    extracted_title = text.replace('سجل الوثائق المعتمدة', '').replace('—', '').strip()
                break # stop at second p

    if not old_header_to_remove:
        # Just insert after <body>
        body_match = re.search(r'<body[^>]*>', content, re.IGNORECASE)
        if body_match:
            old_header_to_remove = body_match.group(0)
        else:
            return

    # Use default extracted title if none found
    if not extracted_title:
        extracted_title = category_name
        
    # Replace English titles with Arabic ones based on filename/category
    english_to_arabic = {
        'Cables': 'الكابلات الأرضية والبحرية',
        'Communications': 'أجهزة الاتصالات',
        'Overhead Lines': 'الخطوط الهوائية',
        'Protection Devices': 'أجهزة الوقاية',
        'Cathodic Protection': 'الحماية الكاثودية',
        'Fire control': 'أجهزة ونظم الإطفاء',
        'Instruments': 'أجهزة القياس والتحكم',
        'Substations': 'محطات المحولات'
    }
    for eng, ar in english_to_arabic.items():
        if eng.lower() in extracted_title.lower() or eng.lower() in filepath.lower():
            extracted_title = ar
            
    # Hardcode translation for specific files just in case
    if 'Ar_ad_cables.htm' in filepath: extracted_title = 'الكابلات الأرضية والبحرية'
    elif 'Ar_ad_com.htm' in filepath: extracted_title = 'أجهزة الاتصالات'
    elif 'Ar_ad_trans.htm' in filepath: extracted_title = 'الخطوط الهوائية'
    elif 'Ar_ad_pc.htm' in filepath: extracted_title = 'الحماية الكاثودية'
    elif 'Ar_ad_subst.htm' in filepath: extracted_title = 'محطات المحولات'

    title_html = f'''
    <div style="text-align: center; margin: 30px auto; max-width: 800px; padding: 0 20px;">
        <h1 style="color: #d9534f; font-weight: 700; margin-bottom: 10px; font-family: 'Cairo', sans-serif;">{extracted_title}</h1>
    </div>
    '''
    
    modern_header = adjust_links(modern_header_base, filepath)
    
    content = content.replace(old_header_to_remove, old_header_to_remove + '\n<div class="app-container">\n' + modern_header + '\n</div>\n' + title_html, 1)
    
    # We should also hide the old_header_to_remove since we appended to it!
    # Wait, if we append, the old EEHC table is still there!
    # Let's REPLACE old_header_to_remove instead!
    
    content = content.replace(old_header_to_remove + '\n<div class="app-container">\n' + modern_header + '\n</div>\n' + title_html, '<div class="app-container">\n' + modern_header + '\n</div>\n' + title_html)
    
    if fontawesome_link not in content:
        content = re.sub(r'</head>', f'{fontawesome_link}\n{modern_style}\n</head>', content, flags=re.IGNORECASE)
        
    # Ensure body dir="rtl"
    content = re.sub(r'<body[^>]*>', '<body dir="rtl">', content, flags=re.IGNORECASE)
        
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f'Updated {os.path.basename(filepath)} with title: {extracted_title}')

targets = [
    r'Ar_appr_docs\ad_cables\Ar_ad_cables.htm',
    r'Ar_appr_docs\ad_com\Ar_ad_com.htm',
    r'Ar_appr_docs\Ar_ad_pc\Ar_ad_pc.htm',
    r'Ar_appr_docs\Ar_ad_trans\Ar_ad_trans.htm',
    r'Ar_appr_docs\Ar_ad_subst\Ar_ad_subst.htm'
]

# Add new_pages
for root, dirs, files in os.walk(os.path.join(arabic_web_dir, 'Ar_appr_docs', 'Ar_ad_subst', 'new_pages')):
    for f in files:
        if f.endswith('.htm'):
            targets.append(os.path.relpath(os.path.join(root, f), arabic_web_dir))
for root, dirs, files in os.walk(os.path.join(arabic_web_dir, 'Ar_appr_docs', 'Ar_ad_subst')):
    for f in files:
        if f.endswith('.htm') and 'new_pages' not in root and 'ad_ss_docs' not in root:
            targets.append(os.path.relpath(os.path.join(root, f), arabic_web_dir))

for t in set(targets):
    process_file(os.path.join(arabic_web_dir, t))
