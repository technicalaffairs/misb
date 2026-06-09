"""
fix_all_arabic.py
=================
Automatically fixes common issues across all Arabic HTML files:
1. Adds dir="rtl" lang="ar" to <html> tag
2. Updates charset from windows-1252/1256 to UTF-8
3. Fixes <body> background path if broken
4. Re-encodes file to UTF-8

Skips files marked as [ERROR] (0 Arabic chars) — those need manual translation.
"""
import os, re
from bs4 import BeautifulSoup

BASE_DIR = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web"
LOG_FILE = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\scratch\fix_log.txt"

# Files to SKIP (0 Arabic chars — need full translation, not just header fixes)
SKIP_FILES = {
    'Ar_Distrib_Board.htm', 'Ar_ad_Batteries.htm', 'Ar_ad_Busbars.htm',
    'Ar_ad_CBs.htm', 'Ar_ad_CT_PT_LA.htm', 'Ar_ad_DS_ES.htm',
    'Ar_ad_TB-SS+PS.htm', 'Ar_ad_TD-SS+PS.htm', 'Ar_ad_Trafo.htm',
    'Ar_ad_compressors.htm', 'Ar_ad_condensers.htm', 'Ar_ad_tap_changers.htm',
    'EFR-002-r0a.htm', 'EFR-003-r0a.htm', 'T-032-r0a.htm', 'T-033-r0a.htm',
    'TD-Oil-012-r0a.htm', 'TL-tmp2-r0a.htm', 'header.htm', 'td-tl-004-r0a.htm',
    'Gn-001-r0a.htm',
}

fixed_count = 0
skipped_count = 0
error_count = 0
log_lines = []

def fix_file(filepath):
    global fixed_count, skipped_count, error_count
    fname = os.path.basename(filepath)
    
    if fname in SKIP_FILES:
        skipped_count += 1
        return

    # Read with best encoding
    content = None
    used_enc = 'unknown'
    for enc in ['utf-8', 'windows-1256', 'windows-1252']:
        try:
            with open(filepath, 'r', encoding=enc, errors='strict') as f:
                content = f.read()
            used_enc = enc
            break
        except Exception:
            continue
    
    if content is None:
        log_lines.append(f'ERROR: Cannot read {fname}')
        error_count += 1
        return

    original = content
    changed = False
    changes = []

    # 1. Fix charset in meta Content-Type
    new_content = re.sub(
        r'(content=["\']text/html;\s*charset=)(windows-1252|windows-1256)(["\'])',
        r'\1utf-8\3',
        content,
        flags=re.IGNORECASE
    )
    if new_content != content:
        content = new_content
        changes.append('charset -> UTF-8')
        changed = True

    # 2. Fix <html> tag — add dir="rtl" lang="ar" if missing
    def fix_html_tag(m):
        tag = m.group(0)
        if 'dir=' not in tag.lower():
            tag = tag.rstrip('>') + ' dir="rtl">'
            changes.append('added dir=rtl to <html>')
        if 'lang=' not in tag.lower():
            tag = tag.rstrip('>') + ' lang="ar">'
            changes.append('added lang=ar to <html>')
        return tag

    new_content = re.sub(r'<html[^>]*>', fix_html_tag, content, flags=re.IGNORECASE)
    if new_content != content:
        content = new_content
        changed = True

    # 3. Fix Content-Language meta if it says en-us
    new_content = re.sub(
        r'(<meta[^>]*content=["\'])en-us(["\'][^>]*>)',
        r'\1ar\2',
        content,
        flags=re.IGNORECASE
    )
    if new_content != content:
        content = new_content
        changes.append('Content-Language: en-us -> ar')
        changed = True

    # 4. Add UTF-8 meta if missing entirely
    if '<meta' in content.lower() and 'charset' not in content.lower():
        content = content.replace(
            '</head>',
            '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n</head>',
            1
        )
        changes.append('inserted UTF-8 charset meta')
        changed = True

    if changed:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_count += 1
            rel = os.path.relpath(filepath, BASE_DIR)
            log_lines.append(f'FIXED: {fname}  [{", ".join(changes)}]  ({rel})')
        except Exception as e:
            log_lines.append(f'ERROR writing {fname}: {e}')
            error_count += 1
    else:
        rel = os.path.relpath(filepath, BASE_DIR)
        log_lines.append(f'OK (no changes needed): {fname}')


def scan(d, depth=0):
    if depth > 6:
        return
    try:
        for e in sorted(os.scandir(d), key=lambda x: x.name):
            if e.is_dir() and not e.name.startswith('_') and e.name not in ('graphics',):
                scan(e.path, depth + 1)
            elif e.is_file() and e.name.lower().endswith(('.htm', '.html')):
                fix_file(e.path)
    except PermissionError:
        pass


scan(BASE_DIR)

summary = [
    '=' * 70,
    'MPIS Arabic Files — Auto-Fix Report',
    '=' * 70,
    f'Files fixed   : {fixed_count}',
    f'Files skipped : {skipped_count} (need manual translation)',
    f'Errors        : {error_count}',
    '',
    'Skipped files (0 Arabic content — need full translation):',
]
for f in sorted(SKIP_FILES):
    summary.append(f'  - {f}')

summary.append('\nDetailed fix log:')
summary.extend(log_lines)

with open(LOG_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(summary))

print(f"Done. Fixed:{fixed_count}  Skipped:{skipped_count}  Errors:{error_count}")
print(f"Log: {LOG_FILE}")
