import os
import json
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
mapping_file = os.path.join(cwd, 'scratch', 'translated_mapping.json')

with open(mapping_file, 'r', encoding='utf-8') as f:
    mapping = json.load(f)

# Optional: Add manual overrides for specific power stations and terms, as deep-translator might get them slightly wrong for this domain.
overrides = {
    "Nubaria CCPS": "محطة النوبارية (دورة مركبة)",
    "Port Said GT": "محطة بورسعيد الغازية",
    "El-Shabab GT": "محطة الشباب الغازية",
    "Talkha GT": "محطة طلخا الغازية",
    "Nubaria PS": "محطة النوبارية",
    "Mahmoudia PS": "محطة المحمودية",
    "Demiatta GT": "محطة دمياط الغازية",
    "Wady Hof": "محطة وادي حوف",
    "Talkha 750": "محطة طلخا 750",
    "Kafr El Dawar": "محطة كفر الدوار",
    "Mahmudia PS": "محطة المحمودية",
    "Shubra El-Khima": "محطة شبرا الخيمة",
    "Talkha 2x210": "محطة طلخا 2x210",
    "Talkha CC": "محطة طلخا (دورة مركبة)",
    "Damietta CC": "محطة دمياط (دورة مركبة)",
    "Abu Sultan": "محطة أبو سلطان",
    "Ayon Mousa": "محطة عيون موسى",
    "Ataka PS": "محطة عتاقة",
    "Damanhour PS": "محطة دمنهور",
    "Asuit 3x30": "محطة أسيوط 3x30",
}
mapping.update(overrides)

for file in files:
    filepath = os.path.join(cwd, file)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    changed = False
    tables = soup.find_all('table')
    for table in tables:
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if not cells:
                continue
            
            for cell in cells:
                # To modify in-place while iterating, find all text nodes
                # Beautiful Soup's find_all(text=True) is deprecated, use string=True
                for text_node in cell.find_all(string=True):
                    original_text = text_node.string
                    if original_text is None:
                        continue
                    
                    stripped_text = original_text.strip()
                    if stripped_text in mapping:
                        translated_text = mapping[stripped_text]
                        # Replace the stripped portion, keeping surrounding whitespace
                        new_text = original_text.replace(stripped_text, translated_text)
                        text_node.replace_with(new_text)
                        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated: {filepath}")
    else:
        print(f"No changes for: {filepath}")

print("Applied translations successfully.")
