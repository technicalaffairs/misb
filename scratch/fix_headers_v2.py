import os, glob, re

search_dir_en = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'

def process_files(directory):
    files = list(glob.iglob(directory + '/**/*.htm', recursive=True)) + list(glob.iglob(directory + '/**/*.html', recursive=True))
    count = 0
    for fp in files:
        if 'scratch' in fp or '_vti_cnf' in fp: continue
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            orig = content
            
            # Remove ONLY the contacts-info div
            content = re.sub(r'<div class="contacts-info">.*?</div>\s*</div>', r'</div>', content, flags=re.IGNORECASE|re.DOTALL)
            # Or if it doesn't match perfectly, just remove contacts-info
            content = re.sub(r'<div class="contacts-info">.*?</div>(?=\s*<a href="[^"]+" class="lang-switch")', '', content, flags=re.IGNORECASE|re.DOTALL)
            
            # Remove secondary logos (including eehc_logo and flag)
            content = re.sub(r'<div class="secondary-logos">.*?</div>', '', content, flags=re.IGNORECASE|re.DOTALL)

            # Replace English Organization Subname
            old_en = 'Middle Egypt Electricity Zone - Technical Affairs Administration'
            new_en = 'Southern Region - Middle Egypt Electricity Zone - Technical Affairs Administration'
            if old_en in content:
                content = content.replace(old_en, new_en)
                
            old_footer_en = 'Developed by: Technical Affairs Administration, Middle Egypt Electricity Zone'
            new_footer_en = 'Developed by: Technical Affairs Administration, Middle Egypt Electricity Zone, Southern Region'
            if old_footer_en in content:
                content = content.replace(old_footer_en, new_footer_en)
                
            if content != orig:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                print('Updated:', fp)
        except:
            pass
    return count

c1 = process_files(search_dir_en)
print('Total files updated:', c1)
