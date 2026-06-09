import os
import re
import urllib.parse

base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
ar_index_path = os.path.join(base_dir, 'arabic_web', 'Ar_Index.htm')

with open(ar_index_path, 'r', encoding='utf-8') as f:
    ar_index_text = f.read()

static_translations = {
    'Home': 'الرئيسية',
    'About us': 'من نحن',
    "What's New": 'ما هو الجديد',
    'Forms': 'النماذج',
    'Admin': 'تعليمات الإدارة',
    'Status': 'موقف المستندات',
    'Draf docs': 'مستندات تحت المراجعة',
    'Prod': 'إنتاج',
    'Trans': 'نقل',
    'Dist': 'توزيع',
    'Ad docs': 'مستندات معتمدة',
    'Click links below to access desired document.': 'اضغط على الروابط أدناه للوصول للمستند المطلوب.',
    'Click links below to access desired document': 'اضغط على الروابط أدناه للوصول للمستند المطلوب'
}

matches = re.findall(r'<a href=\"\.\./([^\"]+)\"[^>]*>(.*?)</a>', ar_index_text, re.DOTALL)

updated_ar_index = ar_index_text
processed_urls = set()

for eng_url, arabic_content in matches:
    if eng_url == 'index.htm' or eng_url.startswith('images/'):
        continue
    if eng_url in processed_urls:
        continue
    processed_urls.add(eng_url)

    # Decode URL (e.g. Air%20Heaters.htm -> Air Heaters.htm)
    decoded_url = urllib.parse.unquote(eng_url)
    
    eng_full_path = os.path.join(base_dir, decoded_url.replace('/', '\\'))
    
    parts = eng_url.split('/')
    if len(parts) == 1:
        new_dir_name = 'Ar_' + parts[0].split('.')[0]
        new_file_name = 'Ar_' + parts[0]
        rel_ar_url = f'{new_dir_name}/{new_file_name}'
    else:
        new_dir_name = 'Ar_' + parts[0]
        new_file_name = 'Ar_' + parts[-1]
        rel_ar_url = f'{new_dir_name}/' + '/'.join(parts[1:-1] + [new_file_name]) if len(parts) > 2 else f'{new_dir_name}/{new_file_name}'
        
    ar_full_path = os.path.join(base_dir, 'arabic_web', urllib.parse.unquote(rel_ar_url).replace('/', '\\'))
    
    updated_ar_index = updated_ar_index.replace(f'../{eng_url}', rel_ar_url)

    if not os.path.exists(eng_full_path):
        print(f"Warning: {eng_full_path} not found.")
        continue

    os.makedirs(os.path.dirname(ar_full_path), exist_ok=True)
    
    try:
        with open(eng_full_path, 'r', encoding='utf-8') as f:
            eng_content = f.read()
    except UnicodeDecodeError:
        try:
            with open(eng_full_path, 'r', encoding='windows-1256') as f:
                eng_content = f.read()
        except:
            print(f"Failed to read {eng_full_path}")
            continue

    ar_content = eng_content
    for en_word, ar_word in static_translations.items():
        ar_content = re.sub(rf'\b{en_word}\b', ar_word, ar_content, flags=re.IGNORECASE)
    
    ar_content = ar_content.replace('About us', 'من نحن')
    ar_content = ar_content.replace("What's New", 'ما هو الجديد')
    ar_content = ar_content.replace('Draf docs', 'مستندات تحت المراجعة')
    ar_content = ar_content.replace('Ad docs', 'مستندات معتمدة')
    ar_content = ar_content.replace('Click links below to access desired document.', 'اضغط على الروابط أدناه للوصول للمستند المطلوب.')
    ar_content = ar_content.replace('Click links below to access desired document', 'اضغط على الروابط أدناه للوصول للمستند المطلوب')

    ar_content = ar_content.replace('href="../', 'href="../../')
    ar_content = ar_content.replace('src="../', 'src="../../')
    ar_content = ar_content.replace('background="../', 'background="../../')
    
    def fix_internal_link(match):
        href = match.group(1)
        if href.startswith('http') or href.startswith('mailto') or href.startswith('javascript') or href.startswith('#') or href.startswith('../'):
            return f'href="{href}"'
        depth_in_eng = len(parts) - 1
        up_to_root = '../' * (depth_in_eng + 1)
        original_dir = '/'.join(parts[:-1])
        if original_dir:
            return f'href="{up_to_root}{original_dir}/{href}"'
        else:
            return f'href="{up_to_root}{href}"'

    ar_content = re.sub(r'href=\"([^\"]+)\"', fix_internal_link, ar_content)

    with open(ar_full_path, 'w', encoding='utf-8') as f:
        f.write(ar_content)
    print(f"Created {ar_full_path}")

with open(ar_index_path, 'w', encoding='utf-8') as f:
    f.write(updated_ar_index)
print("Updated Ar_Index.htm")
