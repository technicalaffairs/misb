import os
import re
import shutil
import urllib.parse

cwd = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
arabic_dir = os.path.join(cwd, 'arabic_web')
gen_docs_abs = os.path.normpath(os.path.join(cwd, 'gen_docs'))

def process_file(filepath):
    changed = False
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return False, []

    file_dir = os.path.dirname(filepath)
    new_files_to_process = []

    def update_link(match):
        nonlocal changed
        original_href = match.group(1)
        decoded_href = urllib.parse.unquote(original_href)
        
        src_abs = os.path.normpath(os.path.join(file_dir, decoded_href))
        
        if not src_abs.startswith(gen_docs_abs):
            return match.group(0)
            
        if 'file:' in src_abs or 'file://' in decoded_href:
            return match.group(0)
        
        rel_path_from_gen_docs = os.path.relpath(src_abs, gen_docs_abs).replace('\\', '/')
        
        path_parts = rel_path_from_gen_docs.split('/')
        if path_parts[0] == 'app_gen':
            path_parts[0] = 'Ar_app_gen'
            
        filename = path_parts[-1]
        if not filename.startswith('Ar_'):
            path_parts[-1] = 'Ar_' + filename
            
        new_rel_path = '/'.join(path_parts)
        dest_abs = os.path.normpath(os.path.join(arabic_dir, new_rel_path))
        
        os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
        
        if os.path.exists(src_abs) and not os.path.exists(dest_abs):
            try:
                shutil.copy2(src_abs, dest_abs)
                if dest_abs.lower().endswith('.htm') or dest_abs.lower().endswith('.html'):
                    new_files_to_process.append(dest_abs)
            except Exception as e:
                print(f"Failed to copy {src_abs}: {e}")
                
        new_href_rel = os.path.relpath(dest_abs, file_dir).replace('\\', '/')
        changed = True
        return 'href="' + urllib.parse.quote(new_href_rel) + '"'

    new_content = re.sub(r'href="([^"]*gen_docs/[^"]+)"', update_link, content, flags=re.IGNORECASE)
    # Also handle single quotes
    new_content = re.sub(r'href=\'([^\']*gen_docs/[^\']+)\'', lambda m: update_link(m).replace('href="', "href='").replace('"', "'"), new_content, flags=re.IGNORECASE)

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated links in {filepath}")
        
    return changed, new_files_to_process

# Queue all current htm files in arabic_web
queue = []
for root, _, files in os.walk(arabic_dir):
    for f in files:
        if f.endswith('.htm') or f.endswith('.html'):
            queue.append(os.path.join(root, f))

processed = set()
while queue:
    current_file = queue.pop(0)
    if current_file in processed:
        continue
    processed.add(current_file)
    
    changed, new_files = process_file(current_file)
    for nf in new_files:
        if nf not in processed and nf not in queue:
            queue.append(nf)

print(f"Finished. Processed {len(processed)} files.")
