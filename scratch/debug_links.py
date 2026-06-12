import os
import re
import urllib.parse

cwd = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
index_abs = os.path.join(cwd, r'arabic_web\Ar_gen_docs\Ar_Pumps_docs Page.htm')
with open(index_abs, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

index_dir_abs = os.path.dirname(index_abs)
matches = re.findall(r'href="([^"]*gen_docs/[^"]+)"', content, flags=re.IGNORECASE)
for m in matches:
    decoded_href = urllib.parse.unquote(m)
    src_abs = os.path.normpath(os.path.join(index_dir_abs, decoded_href))
    gen_docs_abs = os.path.normpath(os.path.join(cwd, 'gen_docs'))
    if src_abs.startswith(gen_docs_abs):
        rel_path_from_gen_docs = os.path.relpath(src_abs, gen_docs_abs).replace('\\', '/')
        path_parts = rel_path_from_gen_docs.split('/')
        if 'file:' in path_parts[0]:
            print("Found it:", m)
        new_rel_path = '/'.join(path_parts)
        if 'file:' in new_rel_path:
            print("In dest:", m)
