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

a_files = []
for base in [os.path.join(base_dir, 'gen_docs'), os.path.join(base_dir, 'arabic_web')]:
    for root, dirs, files in os.walk(base):
        if '_vti_cnf' in root: continue
        for f in files:
            if f.lower().endswith('a.htm') and '-' in f:
                a_files.append(os.path.join(root, f))

processed_count = 0
for filepath in a_files:
    try:
        with open(filepath, 'r', encoding='windows-1256', errors='ignore') as f:
            text = f.read()
            
        if 'app-container' in text:
            continue
            
        body_split = re.split(r'(<body[^>]*>)', text, maxsplit=1, flags=re.IGNORECASE)
        if len(body_split) < 3:
            continue
            
        pre_body = body_split[0]
        body_tag = body_split[1]
        post_body = body_split[2]
        
        # We need RTL direction on the body, so let's add dir="rtl" if not present
        if 'dir=' not in body_tag.lower():
            body_tag = body_tag.replace('>', ' dir="rtl">')
            
        modern_header = adjust_links(modern_header_base, filepath)
        new_post_body = f'\n<div class="app-container">\n{modern_header}\n</div>\n{post_body}'
        
        content = pre_body + body_tag + new_post_body
        
        fontawesome_link = r'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'
        if fontawesome_link not in content:
            content = re.sub(r'</head>', f'{fontawesome_link}\n{modern_style}\n</head>', content, flags=re.IGNORECASE)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        processed_count += 1
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print(f'Successfully injected modern header into {processed_count} individual Arabic documents.')
