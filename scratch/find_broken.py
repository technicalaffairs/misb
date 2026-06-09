import os
import re

base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
for root, dirs, files in os.walk(base_dir):
    if 'scratch' in root or '.git' in root:
        continue
    for f in files:
        if f.endswith('.htm') or f.endswith('.html'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if 'OFR-002-r0a' in content:
                        print(f'Found OFR-002-r0a in: {path}')
                        matches = re.findall(r'<a[^>]+href=[\'\"]([^\'\"]+)[\'\"][^>]*>[^<]*OFR-002-r0a[^<]*</a>', content, re.IGNORECASE)
                        for m in matches:
                            print(f'  Link points to: {m}')
            except Exception as e:
                try:
                    with open(path, 'r', encoding='windows-1256') as file:
                        content = file.read()
                        if 'OFR-002-r0a' in content:
                            print(f'Found OFR-002-r0a in: {path}')
                            matches = re.findall(r'<a[^>]+href=[\'\"]([^\'\"]+)[\'\"][^>]*>[^<]*OFR-002-r0a[^<]*</a>', content, re.IGNORECASE)
                            for m in matches:
                                print(f'  Link points to: {m}')
                except: pass
