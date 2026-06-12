import os
import json
from bs4 import BeautifulSoup

cwd = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
folder = os.path.join(cwd, r'gen_docs\app_gen\WDEPC\all_docs\Boilers')
mapping_file = os.path.join(cwd, 'scratch', 'translated_all_mapping.json')

with open(mapping_file, 'r', encoding='utf-8') as f:
    mapping = json.load(f)

# Sort mapping by length descending to replace longer strings first, just in case
sorted_mapping = dict(sorted(mapping.items(), key=lambda item: len(item[0]), reverse=True))

for file in os.listdir(folder):
    if not file.endswith('.htm') and not file.endswith('.html'):
        continue
    filepath = os.path.join(folder, file)
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
    except Exception:
        continue

    soup = BeautifulSoup(html, 'html.parser')
    
    changed = False
    
    for text_node in soup.find_all(string=True):
        parent = text_node.parent
        if parent and parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            continue
            
        original_text = text_node.string
        if original_text is None:
            continue
            
        stripped_text = original_text.strip()
        if stripped_text in sorted_mapping and sorted_mapping[stripped_text] != stripped_text:
            translated_text = sorted_mapping[stripped_text]
            new_text = original_text.replace(stripped_text, translated_text)
            text_node.replace_with(new_text)
            changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated: {filepath}")

print("Applied translations successfully.")
