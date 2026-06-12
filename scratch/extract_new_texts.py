import os
import json
import re
from bs4 import BeautifulSoup

cwd = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
dirs_to_scan = [
    os.path.join(cwd, r'arabic_web')
]

unique_strings = set()

for d in dirs_to_scan:
    for root, _, files in os.walk(d):
        for file in files:
            if (file.endswith('.htm') or file.endswith('.html')) and file.startswith('Ar_'):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        html = f.read()
                except UnicodeDecodeError:
                    with open(filepath, 'r', encoding='windows-1252', errors='ignore') as f:
                        html = f.read()

                soup = BeautifulSoup(html, 'html.parser')
                
                for text_node in soup.find_all(string=True):
                    parent = text_node.parent
                    if parent and parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                        continue
                        
                    text = text_node.strip()
                    if re.search(r'[A-Za-z]', text) and not re.search(r'[\u0600-\u06FF]', text):
                        if re.fullmatch(r'[A-Za-z0-9\-]+-r\w*', text, re.IGNORECASE):
                            continue
                        if len(text) <= 1:
                            continue
                        unique_strings.add(text)

with open(os.path.join(cwd, 'scratch', 'extracted_all.json'), 'w', encoding='utf-8') as f:
    json.dump(list(unique_strings), f, ensure_ascii=False, indent=4)

print(f"Extracted {len(unique_strings)} unique English strings.")
