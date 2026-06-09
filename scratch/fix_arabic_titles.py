import os
import glob
import re
import urllib.parse

base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
arabic_web_dir = os.path.join(base_dir, 'arabic_web')
ar_index_path = os.path.join(arabic_web_dir, 'Ar_Index.htm')

with open(ar_index_path, 'r', encoding='utf-8') as f:
    text = f.read()

mapping = {}
matches = re.findall(r'<a href=\"(Ar_[^\"]+)\"[^>]*>(.*?)</a>', text, re.DOTALL)
for url, content in matches:
    clean = re.sub(r'<[^>]+>', '', content).strip()
    arabic_only = re.sub(r'\(.*?\)', '', clean).strip()
    # Decode the URL so spaces match
    decoded_url = urllib.parse.unquote(url)
    mapping[decoded_url] = arabic_only

for fp in glob.iglob(arabic_web_dir + '/**/*.htm*', recursive=True):
    if 'Ar_Index' in fp: continue
    
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
            
        rel_path = os.path.relpath(fp, arabic_web_dir).replace('\\', '/')
        
        ar_title = mapping.get(rel_path, '')
        updated = False
        
        if ar_title:
            eng_word = os.path.basename(fp).replace('Ar_', '').replace('.htm', '').replace('.html', '').replace('_docs Page', '')
            eng_word = urllib.parse.unquote(eng_word)
            
            # More generic matching for titles
            title_regex = re.compile(r'(<big>|<span[^>]*>|<font[^>]*>)\s*(' + re.escape(eng_word) + r'.*?)\s*(</big>|</span>|</font>)', re.IGNORECASE)
            
            def replace_title(m):
                return m.group(1) + ar_title + m.group(3)
                
            new_content = title_regex.sub(replace_title, content)
            
            # If it still didn't match, maybe the english word wasn't quite right.
            # E.g. "Safety Health Page" vs "Safety Health"
            if new_content == content and ' ' in eng_word:
                first_word = eng_word.split()[0]
                fallback_regex = re.compile(r'(<big>|<span[^>]*>|<font[^>]*>)\s*(' + re.escape(first_word) + r'.*?)\s*(</big>|</span>|</font>)', re.IGNORECASE)
                new_content = fallback_regex.sub(replace_title, content)
            
            if new_content != content:
                content = new_content
                updated = True
            else:
                # Try one more aggressive fallback just replacing the text inside any <big> or <span> that contains the English word
                def aggressive_replace(match):
                    return match.group(1) + ar_title + match.group(3)
                aggressive_regex = re.compile(r'(<[^>]*>)\s*([a-zA-Z\s\-]+)\s*(</[^>]*>)', re.IGNORECASE)
                # Not safe to do this globally, only if we find the exact english word
                content_mod = content.replace(f'<span lang="en-us">{eng_word}</span>', f'<span lang="en-us">{ar_title}</span>')
                content_mod = content_mod.replace(f'<big>{eng_word}</big>', f'<big>{ar_title}</big>')
                if content_mod != content:
                    content = content_mod
                    updated = True

        if updated:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated title in {rel_path} to {ar_title}')
            
    except Exception as e:
        pass
