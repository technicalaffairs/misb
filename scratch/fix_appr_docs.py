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
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='windows-1256') as f:
            content = f.read()
            
    # Remove old EEHC header if it exists. 
    # The old EEHC header is the very first <table...> after <body>
    # Let's extract the part of content after <body>
    body_split = re.split(r'(<body[^>]*>)', content, maxsplit=1, flags=re.IGNORECASE)
    if len(body_split) < 3: continue
    
    pre_body = body_split[0]
    body_tag = body_split[1]
    post_body = body_split[2]
    
    # Check if the first thing is a table (EEHC header)
    table_match = re.search(r'^\s*<TABLE[^>]*>.*?</TABLE>\s*', post_body, re.IGNORECASE | re.DOTALL)
    if table_match:
        # EEHC header found! Remove it
        post_body = post_body[table_match.end():]
        
    # Check if it has the title paragraph (like in Ar_ad_Busbars)
    p_match = re.search(r'^\s*<p[^>]*>.*?</p>\s*<p[^>]*>.*?</p>\s*', post_body, re.IGNORECASE | re.DOTALL)
    if p_match and '&#1606;' in p_match.group(0): # system information encoded...
        # Wait, let's just remove the first few paragraphs if they contain the title
        pass # Not doing this to be safe, only doing for known EEHC headers
        
    # In some files, there is a title after EEHC header: <P class=MsoNormal dir=rtl align=right style="margin-top: 0; margin-bottom: 0"><u><b>التعليمات الفنية</b></u></P>
    # We want to insert the modern header here
    
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
    title = 'محطات المحولات'
    if 'Ar_ad_trans' in filepath: title = 'الخطوط الهوائية'
    elif 'Ar_ad_pc' in filepath: title = 'الحماية الكاثودية'
    
    title_html = f'''
    <div style="text-align: center; margin: 30px auto; max-width: 800px; padding: 0 20px;">
        <h1 style="color: #d9534f; font-weight: 700; margin-bottom: 10px; font-family: 'Cairo', sans-serif;">{title}</h1>
    </div>
    '''
    
    modern_header = adjust_links(modern_header_base, filepath)
    
    post_body = f'\n<div class="app-container">\n{modern_header}\n</div>\n{title_html}\n' + post_body
    
    content = pre_body + '<body dir="rtl">' + post_body
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Processed {t}')
