"""
check_all_arabic_v2.py
======================
Saves all results directly to file — avoids PowerShell encoding issues.
"""
import os, re, sys
from bs4 import BeautifulSoup
import csv

BASE_DIR = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web"
OUT_TXT  = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\scratch\audit_results.txt"
OUT_CSV  = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\scratch\audit_results.csv"

BAD_ENG_PATTERNS = [
    r'\bIsolate\b', r'\bConnect\b', r'\bDisconnect\b',
    r'\bRecord\b', r'\bRepeat\b', r'\bEnsure\b',
    r'\bMegger\b', r'\bBushing\b', r'\bWork Order\b',
    r'\bSafety fence\b', r'\bDepress\b', r'\bSwitch ON\b',
]

ISSUES_REPORT = []

def check_file(filepath):
    fname  = os.path.basename(filepath)
    relpath = os.path.relpath(filepath, BASE_DIR)
    issues = []

    # Read file
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
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            used_enc = 'utf-8-replace'
        except Exception as e:
            ISSUES_REPORT.append({'file': fname, 'relpath': relpath,
                                   'severity': 'ERROR', 'encoding': '?',
                                   'arabic_chars': 0, 'ar_ratio': '0%',
                                   'size_kb': '?', 'issues': [f'Cannot read: {e}']})
            return

    soup = BeautifulSoup(content, 'html.parser')

    # 1. Charset check
    meta = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
    if meta:
        mc = meta.get('content', '')
        if 'windows-1252' in mc or 'windows-1256' in mc:
            issues.append(f'[WARN] Old charset: {mc.strip()} — upgrade to UTF-8')

    # 2. RTL on <html>
    html_tag = soup.find('html')
    if html_tag and not html_tag.get('dir'):
        issues.append('[WARN] <html> tag missing dir="rtl"')

    # 3. Arabic content ratio
    body_text = soup.get_text(' ', strip=True)
    ar_chars = len(re.findall(r'[\u0600-\u06FF]', body_text))
    alpha    = len(re.findall(r'[a-zA-Z\u0600-\u06FF]', body_text))
    ar_ratio = (ar_chars / alpha) if alpha > 0 else 0

    if ar_chars < 50:
        issues.append(f'[ERROR] Very little Arabic content: {ar_chars} chars — file may be empty/untranslated')
    elif ar_ratio < 0.30 and alpha > 200:
        issues.append(f'[WARN] Low Arabic ratio {ar_ratio:.0%} — may have untranslated English procedures')

    # 4. Untranslated English procedure keywords
    eng_found = []
    for pat in BAD_ENG_PATTERNS:
        matches = re.findall(pat, body_text, re.IGNORECASE)
        if matches:
            label = pat.replace('\\b','')
            eng_found.append(f'{label}({len(matches)}x)')
    if eng_found:
        issues.append('[WARN] Untranslated English procedure words: ' + ', '.join(eng_found[:8]))

    # 5. Broken absolute Windows image paths
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src.lower().startswith('c:\\') or src.lower().startswith('c:/'):
            issues.append(f'[ERROR] Absolute Windows image path: {src[:60]}')
            break

    # 6. Missing CSS link
    links = soup.find_all('link', rel='stylesheet')
    if not links:
        issues.append('[WARN] No CSS stylesheet link found')

    size_kb = os.path.getsize(filepath) / 1024

    if any('[ERROR]' in i for i in issues):
        severity = 'ERROR'
    elif issues:
        severity = 'WARN'
    else:
        severity = 'OK'

    ISSUES_REPORT.append({
        'file': fname,
        'relpath': relpath,
        'severity': severity,
        'encoding': used_enc,
        'arabic_chars': ar_chars,
        'ar_ratio': f'{ar_ratio:.0%}',
        'size_kb': f'{size_kb:.0f}',
        'issues': issues,
    })


def scan_dir(d, depth=0, max_depth=6):
    if depth > max_depth:
        return
    try:
        for e in sorted(os.scandir(d), key=lambda x: x.name):
            if e.is_dir() and not e.name.startswith('_') and e.name != 'graphics':
                scan_dir(e.path, depth + 1, max_depth)
            elif e.is_file() and e.name.lower().endswith(('.htm', '.html')):
                check_file(e.path)
    except PermissionError:
        pass


scan_dir(BASE_DIR)

# Sort
order = {'ERROR': 0, 'WARN': 1, 'OK': 2}
ISSUES_REPORT.sort(key=lambda x: (order.get(x['severity'], 3), x['file']))

errors   = [r for r in ISSUES_REPORT if r['severity'] == 'ERROR']
warnings = [r for r in ISSUES_REPORT if r['severity'] == 'WARN']
good     = [r for r in ISSUES_REPORT if r['severity'] == 'OK']

lines = []
lines.append('=' * 80)
lines.append('MPIS Arabic Files Audit Report')
lines.append('=' * 80)
lines.append(f'Total files scanned : {len(ISSUES_REPORT)}')
lines.append(f'  ERRORS  : {len(errors)}')
lines.append(f'  WARNINGS: {len(warnings)}')
lines.append(f'  OK      : {len(good)}')

lines.append('\n' + '=' * 80)
lines.append('[ERROR] Files with critical issues:')
lines.append('=' * 80)
for r in errors:
    lines.append(f"\n  FILE: {r['file']}  [{r['size_kb']} KB] [{r['encoding']}]")
    lines.append(f"  PATH: {r['relpath']}")
    lines.append(f"  Arabic chars: {r['arabic_chars']}  |  Arabic ratio: {r['ar_ratio']}")
    for iss in r['issues']:
        lines.append(f"    >> {iss}")

lines.append('\n' + '=' * 80)
lines.append('[WARN] Files with warnings:')
lines.append('=' * 80)
for r in warnings:
    lines.append(f"\n  FILE: {r['file']}  [{r['size_kb']} KB] [{r['encoding']}]")
    lines.append(f"  PATH: {r['relpath']}")
    lines.append(f"  Arabic chars: {r['arabic_chars']}  |  Arabic ratio: {r['ar_ratio']}")
    for iss in r['issues']:
        lines.append(f"    >> {iss}")

lines.append('\n' + '=' * 80)
lines.append('[OK] Clean files:')
lines.append('=' * 80)
for r in good:
    lines.append(f"  OK  {r['file']}  [{r['size_kb']} KB]  AR:{r['ar_ratio']}  ({r['arabic_chars']} chars)")

report_text = '\n'.join(lines)

with open(OUT_TXT, 'w', encoding='utf-8') as f:
    f.write(report_text)

with open(OUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['File','RelPath','Severity','Encoding','Arabic Chars','AR Ratio','Size KB','Issues'])
    for r in ISSUES_REPORT:
        writer.writerow([r['file'], r['relpath'], r['severity'], r['encoding'],
                         r['arabic_chars'], r['ar_ratio'], r['size_kb'],
                         ' | '.join(r['issues'])])

print(f"Done. Results saved to:\n  {OUT_TXT}\n  {OUT_CSV}")
print(f"Totals: {len(ISSUES_REPORT)} files | {len(errors)} errors | {len(warnings)} warnings | {len(good)} OK")
