import os
import re

cwd = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
index_file = os.path.join(cwd, r'arabic_web\Ar_gen_docs\Ar_Boilers_docs Page.htm')

with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# The old links are like: ../../gen_docs/app_gen/WDEPC/all_docs/Boilers/BLR-007-r0.htm
# We want to change them to point to: ../Ar_app_gen/WDEPC/all_docs/Boilers/Ar_BLR-007-r0.htm
# Wait, the index file is in arabic_web/Ar_gen_docs.
# The relative path from arabic_web/Ar_gen_docs to arabic_web/Ar_app_gen is: ../Ar_app_gen
# The old relative path was: ../../gen_docs/app_gen

def link_replacer(match):
    prefix = match.group(1) # something like: ../../gen_docs/app_gen/WDEPC/all_docs/Boilers/
    filename = match.group(2) # BLR-007-r0.htm
    
    # Check if this is the target WDEPC boilers folder
    if "WDEPC" in prefix and "Boilers" in prefix:
        # new path: ../Ar_app_gen/WDEPC/all_docs/Boilers/Ar_filename
        new_prefix = prefix.replace("../../gen_docs/app_gen", "../Ar_app_gen")
        # Ensure Ar_ prefix on filename
        new_filename = filename if filename.startswith("Ar_") else "Ar_" + filename
        return new_prefix + new_filename
    return match.group(0)

# Replace href values
new_content = re.sub(r'href="([^"]*/)([^"/]+\.html?)"', link_replacer, content, flags=re.IGNORECASE)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated links in Ar_Boilers_docs Page.htm")
