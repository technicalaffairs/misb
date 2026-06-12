import os
import shutil

cwd = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
src_dir = os.path.join(cwd, r'gen_docs\app_gen\WDEPC\all_docs\Boilers')
dest_dir = os.path.join(cwd, r'arabic_web\Ar_app_gen\WDEPC\all_docs\Boilers')

for file in os.listdir(src_dir):
    if file.endswith('.htm') or file.endswith('.html'):
        src_path = os.path.join(src_dir, file)
        # Prefix with Ar_ if it doesn't already have it
        if file.startswith('Ar_'):
            dest_file = file
        else:
            dest_file = 'Ar_' + file
        dest_path = os.path.join(dest_dir, dest_file)
        shutil.copy2(src_path, dest_path)
        print(f"Copied to {dest_file}")
