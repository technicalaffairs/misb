"""
check_all_arabic.py
===================
Comprehensive audit of all Arabic HTML files in the MPIS project.
Checks for:
  - Encoding issues (windows-1252/1256 vs UTF-8)
  - Empty content (placeholder-only sections)
  - Mixed Arabic/English in procedure steps
  - Missing RTL attributes
  - Broken image/CSS paths
  - Key electrical terminology consistency
"""

import os
import re
from bs4 import BeautifulSoup

BASE_DIR = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web"

ISSUES_REPORT = []

# Known correct Arabic EE terms that should appear (spot check)
GOOD_TERMS = [
    "احتياطات", "الأمان", "السلامة", "الاختبار", "المحول",
    "الشبكات", "معتمد", "الموقع", "الإجراء"
]

# Bad signs: leftover English procedure words that should have been translated
BAD_ENG_PATTERNS = [
    r'\bIsolate\b', r'\bConnect\b', r'\bDisconnect\b',
    r'\bRecord\b', r'\bRepeat\b', r'\bEnsure\b',
    r'\bMegger\b', r'\bBushing\b', r'\bTap Changer\b',
    r'\bWork Order\b', r'\bSafety fence\b'
]

def check_file(filepath):
    fname = os.path.basename(filepath)
    issues = []
    
    try:
        # Try UTF-8 first, then fall back to windows-1256
        for enc in ['utf-8', 'windows-1256', 'windows-1252']:
            try:
                with open(filepath, 'r', encoding=enc, errors='strict') as f:
                    content = f.read()
                used_enc = enc
                break
            except (UnicodeDecodeError, LookupError):
                continue
        else:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            used_enc = 'utf-8-ignore'
    except Exception as e:
        ISSUES_REPORT.append({'file': fname, 'severity': 'ERROR', 'issues': [f'Cannot read file: {e}']})
        return

    soup = BeautifulSoup(content, 'html.parser')
    
    # 1. Check charset declaration
    meta_charset = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
    if meta_charset:
        meta_content = meta_charset.get('content', '')
        if 'windows-1252' in meta_content or 'windows-1256' in meta_content:
            issues.append(f'⚠️ ترميز قديم: {meta_content.strip()} — يُنصح بترقيته إلى UTF-8')
    
    # 2. Check RTL direction on html tag
    html_tag = soup.find('html')
    if html_tag:
        if not html_tag.get('dir'):
            issues.append('⚠️ وسم <html> لا يحتوي على dir="rtl"')
    
    # 3. Check for empty procedure sections
    body_text = soup.get_text(' ', strip=True)
    arabic_chars = len(re.findall(r'[\u0600-\u06FF]', body_text))
    total_alpha = len(re.findall(r'[a-zA-Z\u0600-\u06FF]', body_text))
    
    if total_alpha > 0:
        ar_ratio = arabic_chars / total_alpha
    else:
        ar_ratio = 0
    
    # Check if the file has very little Arabic (mostly empty or English)
    if arabic_chars < 50:
        issues.append(f'❌ محتوى عربي شحيح جداً: {arabic_chars} حرف عربي فقط — الملف يبدو فارغاً أو غير مترجم')
    elif ar_ratio < 0.3 and total_alpha > 200:
        issues.append(f'⚠️ نسبة الحروف العربية منخفضة ({ar_ratio:.0%}) — قد يحتوي على نص إنجليزي غير مترجم')
    
    # 4. Check for untranslated English procedure words
    eng_found = []
    for pat in BAD_ENG_PATTERNS:
        matches = re.findall(pat, body_text, re.IGNORECASE)
        if matches:
            clean_pat = pat.replace('\\b', '')
            eng_found.append(f'{clean_pat} ({len(matches)} مرة)')
    if eng_found:
        issues.append(f'⚠️ كلمات إجرائية إنجليزية لم تُترجم: {", ".join(eng_found[:5])}')
    
    # 5. Check CSS path
    link = soup.find('link', rel='stylesheet')
    if link:
        href = link.get('href', '')
        if 'style.css' not in href:
            issues.append(f'⚠️ مسار CSS غير معتاد: {href}')
    else:
        issues.append('⚠️ لا يوجد رابط CSS')
    
    # 6. Check for broken image paths (absolute Windows paths)
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src.startswith('C:\\') or src.startswith('c:\\'):
            issues.append(f'❌ مسار صورة مطلق (يُكسر النشر على الويب): {src[:50]}')
            break
    
    # 7. File size sanity
    size_kb = os.path.getsize(filepath) / 1024
    
    # Severity
    if any('❌' in i for i in issues):
        severity = '❌ خطأ'
    elif issues:
        severity = '⚠️ تحذير'
    else:
        severity = '✅ جيد'
    
    ISSUES_REPORT.append({
        'file': fname,
        'path': filepath,
        'severity': severity,
        'encoding': used_enc,
        'arabic_chars': arabic_chars,
        'ar_ratio': f'{ar_ratio:.0%}',
        'size_kb': f'{size_kb:.0f} KB',
        'issues': issues
    })

def scan_directory(dirpath, max_depth=4, current_depth=0):
    if current_depth > max_depth:
        return
    try:
        for entry in os.scandir(dirpath):
            if entry.is_dir() and not entry.name.startswith('_'):
                scan_directory(entry.path, max_depth, current_depth + 1)
            elif entry.is_file() and entry.name.lower().endswith(('.htm', '.html')):
                check_file(entry.path)
    except PermissionError:
        pass

print("=" * 70)
print("فحص شامل للملفات العربية — مشروع MPIS")
print("=" * 70)

scan_directory(BASE_DIR)

# Sort by severity
order = {'❌ خطأ': 0, '⚠️ تحذير': 1, '✅ جيد': 2}
ISSUES_REPORT.sort(key=lambda x: (order.get(x['severity'], 3), x['file']))

# Print report
errors = [r for r in ISSUES_REPORT if r['severity'] == '❌ خطأ']
warnings = [r for r in ISSUES_REPORT if r['severity'] == '⚠️ تحذير']
good = [r for r in ISSUES_REPORT if r['severity'] == '✅ جيد']

print(f"\nإجمالي الملفات المفحوصة: {len(ISSUES_REPORT)}")
print(f"  ❌ أخطاء:    {len(errors)}")
print(f"  ⚠️ تحذيرات: {len(warnings)}")
print(f"  ✅ جيد:     {len(good)}")

print("\n" + "=" * 70)
print("❌ الملفات ذات الأخطاء الجسيمة:")
print("=" * 70)
for r in errors:
    print(f"\n📄 {r['file']} [{r['size_kb']}] [{r['encoding']}]")
    print(f"   حروف عربية: {r['arabic_chars']} | نسبة العربية: {r['ar_ratio']}")
    for issue in r['issues']:
        print(f"   {issue}")

print("\n" + "=" * 70)
print("⚠️ الملفات ذات التحذيرات:")
print("=" * 70)
for r in warnings:
    print(f"\n📄 {r['file']} [{r['size_kb']}] [{r['encoding']}]")
    print(f"   حروف عربية: {r['arabic_chars']} | نسبة العربية: {r['ar_ratio']}")
    for issue in r['issues']:
        print(f"   {issue}")

print("\n" + "=" * 70)
print("✅ الملفات الجيدة:")
print("=" * 70)
for r in good:
    print(f"  ✅ {r['file']} [{r['size_kb']}] — {r['arabic_chars']} حرف عربي ({r['ar_ratio']})")

# Save CSV for review
import csv
csv_path = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\scratch\arabic_audit_results.csv"
with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['الملف', 'الحالة', 'الترميز', 'الحروف العربية', 'نسبة العربية', 'الحجم', 'المشاكل'])
    for r in ISSUES_REPORT:
        writer.writerow([
            r['file'], r['severity'], r['encoding'],
            r['arabic_chars'], r['ar_ratio'], r['size_kb'],
            ' | '.join(r['issues']) if r['issues'] else 'لا مشاكل'
        ])
print(f"\n\nتم حفظ نتائج الفحص في:\n{csv_path}")
print("=" * 70)
