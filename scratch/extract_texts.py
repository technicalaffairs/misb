import os
import json
import re
from bs4 import BeautifulSoup

files = [
    r'arabic_web\Ar_gen_docs\Ar_Boilers_docs Page.htm',
    r'arabic_web\Ar_gen_docs\Ar_Turbines.htm',
    r'arabic_web\Ar_gen_docs\Ar_Pumps_docs Page.htm',
    r'arabic_web\Ar_gen_docs\Ar_Fans_docs Page.htm',
    r'arabic_web\Ar_gen_docs\Ar_Governers.htm',
    r'arabic_web\Ar_gen_docs\Ar_Air Heaters.htm',
    r'arabic_web\Ar_gen_docs\Ar_Thermal aux.htm',
    r'arabic_web\Ar_gen_docs\Ar_Generators Page.htm',
    r'arabic_web\Ar_appr_docs\ad_subst\Ar_ad_dsl.htm',
    r'arabic_web\Ar_gen_docs\Ar_Valves.htm',
    r'arabic_web\Ar_gen_docs\Ar_Motors Page.htm',
    r'arabic_web\Ar_gen_docs\Ar_Filters_docs Page.htm',
    r'arabic_web\Ar_gen_docs\Ar_Hydraulic aux.htm'
]

cwd = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
unique_strings = set()

for file in files:
    filepath = os.path.join(cwd, file)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='windows-1256', errors='ignore') as f:
        html = f.read()
    
    # Try utf-8 if windows-1256 fails or vice versa, actually 'ignore' might lose data.
    # Let's try utf-8 first, fallback to windows-1256
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='windows-1256', errors='ignore') as f:
            html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract text from tables
    tables = soup.find_all('table')
    for table in tables:
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if not cells:
                continue
            
            # The second and third cells usually have the text we need to translate
            # We will extract text from all cells to be safe
            for cell in cells:
                for text_node in cell.stripped_strings:
                    text_node = text_node.strip()
                    # If it contains English letters and is longer than 2 chars
                    if re.search(r'[A-Za-z]{3,}', text_node) and not re.search(r'[\u0600-\u06FF]', text_node):
                        unique_strings.add(text_node)

# Remove document IDs which look like Blr-001-r0, BG-001-r1 etc.
filtered_strings = []
for s in unique_strings:
    # Skip if it matches document ID pattern exactly e.g. Blr-001-r0 or VLV-123-r1
    if re.fullmatch(r'[A-Za-z0-9\-]+-r\w*', s, re.IGNORECASE):
        continue
    # Skip short words like "USA", "M3", "M6" unless part of larger string? Wait, USA could be translated.
    # Let's keep them and filter manually if needed.
    filtered_strings.append(s)

with open(os.path.join(cwd, 'scratch', 'extracted_english.json'), 'w', encoding='utf-8') as f:
    json.dump(filtered_strings, f, ensure_ascii=False, indent=4)

print(f"Extracted {len(filtered_strings)} unique English strings.")
