import os
import re
import shutil
import urllib.parse

cwd = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
index_file = os.path.join(cwd, r'arabic_web\Ar_gen_docs\Ar_Boilers_docs Page.htm')

with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find all hrefs pointing to English docs
# e.g. ../../gen_docs/Boilers/BG-001-r1.htm
# e.g. ../../gen_docs/app_gen/EDEPC/Boilers/drum-010-r0.htm
# We want to map:
# ../../gen_docs/Boilers/... -> ../Boilers/Ar_...
# ../../gen_docs/app_gen/... -> ../Ar_app_gen/.../Ar_...

def update_link(match):
    original_href = match.group(1)
    
    # decode URL encoding for local path resolution (e.g. %20 -> space)
    decoded_href = urllib.parse.unquote(original_href)
    
    # Base English dir is cwd\gen_docs
    # decoded_href starts with ../../gen_docs/
    rel_path_from_gen_docs = decoded_href[15:] # remove "../../gen_docs/"
    
    # Construct source absolute path
    src_abs = os.path.normpath(os.path.join(cwd, 'gen_docs', rel_path_from_gen_docs))
    
    # We only process .htm or .html files, and NOT index pages.
    # Actually, we should process all of them to Arabic paths.
    
    # Construct destination Arabic relative path from gen_docs root equivalent
    # If it's in app_gen -> Ar_app_gen
    # If it's in Boilers -> Boilers
    # The new path should be inside arabic_web.
    
    path_parts = rel_path_from_gen_docs.split('/')
    if path_parts[0] == 'app_gen':
        path_parts[0] = 'Ar_app_gen'
        
    filename = path_parts[-1]
    if not filename.startswith('Ar_'):
        path_parts[-1] = 'Ar_' + filename
        
    new_rel_path = '/'.join(path_parts)
    
    # Absolute destination
    dest_abs = os.path.normpath(os.path.join(cwd, 'arabic_web', new_rel_path))
    
    # Ensure dir exists
    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    
    # Copy file if source exists and destination doesn't
    if os.path.exists(src_abs) and not os.path.exists(dest_abs):
        try:
            shutil.copy2(src_abs, dest_abs)
            print(f"Copied {src_abs} -> {dest_abs}")
        except Exception as e:
            print(f"Failed to copy {src_abs}: {e}")
            
    # Return new href.
    # Since index is at arabic_web/Ar_gen_docs/Ar_Boilers_docs Page.htm
    # To get to arabic_web/Ar_app_gen/... we use ../Ar_app_gen/...
    # To get to arabic_web/Boilers/... we use ../Boilers/...
    return 'href="../' + urllib.parse.quote(new_rel_path) + '"'

new_content = re.sub(r'href="(../../gen_docs/[^"]+)"', update_link, content, flags=re.IGNORECASE)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated links and copied files.")
