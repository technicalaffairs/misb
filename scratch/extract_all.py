import os
import json
import re
from bs4 import BeautifulSoup

cwd = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
folder = os.path.join(cwd, r'gen_docs\app_gen\WDEPC\all_docs\Boilers')

unique_strings = set()

for file in os.listdir(folder):
    if not file.endswith('.htm') and not file.endswith('.html'):
        continue
    filepath = os.path.join(folder, file)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='windows-1252', errors='ignore') as f:
            html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract text from all text nodes
    for text_node in soup.find_all(string=True):
        parent = text_node.parent
        if parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            continue
            
        text = text_node.strip()
        # If it has at least one letter and isn't just whitespace/symbols
        if re.search(r'[A-Za-z]', text) and not re.search(r'[\u0600-\u06FF]', text):
            # Skip if it looks like a document ID like "Blr-007-r0"
            if re.fullmatch(r'[A-Za-z0-9\-]+-r\w*', text, re.IGNORECASE):
                continue
            # Skip if it is just a single character
            if len(text) <= 1:
                continue
            unique_strings.add(text)

with open(os.path.join(cwd, 'scratch', 'extracted_all.json'), 'w', encoding='utf-8') as f:
    json.dump(list(unique_strings), f, ensure_ascii=False, indent=4)

print(f"Extracted {len(unique_strings)} unique English strings.")
