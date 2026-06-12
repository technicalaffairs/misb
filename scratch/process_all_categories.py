import os
import re
import shutil
import urllib.parse

cwd = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'

index_files = [
    r'arabic_web\Ar_gen_docs\Ar_Turbines.htm',
    r'arabic_web\Ar_gen_docs\Ar_Pumps_docs Page.htm',
    r'arabic_web\Ar_gen_docs\Ar_Fans_docs Page.htm',
    r'arabic_web\Ar_gen_docs\Ar_Governers.htm',
    r'arabic_web\Ar_gen_docs\Ar_Air Heaters.htm',
    r'arabic_web\Ar_gen_docs\Ar_Thermal aux.htm',
    r'arabic_web\Ar_gen_docs\Ar_Generators Page.htm',
    r'arabic_web\Ar_gen_docs\Ar_Valves.htm',
    r'arabic_web\Ar_gen_docs\Ar_Motors Page.htm',
    r'arabic_web\Ar_appr_docs\ad_subst\Ar_ad_dsl.htm'
]

# We need a function to process an index file
def process_index(index_rel_path):
    index_abs = os.path.join(cwd, index_rel_path)
    if not os.path.exists(index_abs):
        print(f"Skipping missing file: {index_abs}")
        return
        
    print(f"Processing: {index_rel_path}")
    
    with open(index_abs, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    index_dir_abs = os.path.dirname(index_abs)

    def update_link(match):
        original_href = match.group(1)
        decoded_href = urllib.parse.unquote(original_href)
        
        # Determine source absolute path
        # It's relative to index_dir_abs
        src_abs = os.path.normpath(os.path.join(index_dir_abs, decoded_href))
        
        # Check if src_abs is within gen_docs
        gen_docs_abs = os.path.normpath(os.path.join(cwd, 'gen_docs'))
        
        # If the file is not in gen_docs or doesn't exist, we skip
        if not src_abs.startswith(gen_docs_abs):
            return match.group(0) # Keep original
            
        # If it doesn't exist, we still want to map it?
        # Let's map it anyway to preserve structure
        
        if 'file:' in src_abs or 'file://' in decoded_href:
            return match.group(0)
        
        # Get relative path from gen_docs
        rel_path_from_gen_docs = os.path.relpath(src_abs, gen_docs_abs).replace('\\', '/')
        
        # Determine destination
        path_parts = rel_path_from_gen_docs.split('/')
        if path_parts[0] == 'app_gen':
            path_parts[0] = 'Ar_app_gen'
            
        filename = path_parts[-1]
        if not filename.startswith('Ar_'):
            path_parts[-1] = 'Ar_' + filename
            
        new_rel_path = '/'.join(path_parts)
        
        # dest is arabic_web/new_rel_path
        dest_abs = os.path.normpath(os.path.join(cwd, 'arabic_web', new_rel_path))
        
        # Create dir
        os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
        
        # Copy
        if os.path.exists(src_abs) and not os.path.exists(dest_abs):
            try:
                shutil.copy2(src_abs, dest_abs)
                #print(f"Copied {src_abs} -> {dest_abs}")
            except Exception as e:
                print(f"Failed to copy {src_abs}: {e}")
                
        # Calculate new relative link from index to dest
        new_href_rel = os.path.relpath(dest_abs, index_dir_abs).replace('\\', '/')
        return 'href="' + urllib.parse.quote(new_href_rel) + '"'

    # Match anything like href="../../gen_docs/..." or href="../../../gen_docs/..."
    # We can match href="([^"]*gen_docs/[^"]+)"
    new_content = re.sub(r'href="([^"]*gen_docs/[^"]+)"', update_link, content, flags=re.IGNORECASE)

    if new_content != content:
        with open(index_abs, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated links in {index_rel_path}")

for file in index_files:
    process_index(file)

print("Done processing all index files.")
