import os, re

filepath = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_gen_docs\Ar_Gas Turbines_docs Page.htm'

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Replace all occurrences of -r0.htm to -r0a.htm inside href attributes
def replacer(match):
    return match.group(0).replace('-r0.htm', '-r0a.htm').replace('-R0.htm', '-R0a.htm').replace('-r0.HTM', '-r0a.HTM')

new_text = re.sub(r'href=[\'\"][^\'\"]+-r0\.htm[\'\"]', replacer, text, flags=re.IGNORECASE)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated links to point to -r0a.htm.")
