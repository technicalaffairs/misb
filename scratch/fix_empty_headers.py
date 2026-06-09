import glob, os, re

# Find all files that might have the empty headers issue
base_dirs = [
    r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\ad_ss_docs",
    r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_pc\ad_pc_docs"
]

patterns_to_fix = [
    (r'(<span[^>]*font-size:\s*22\.0pt[^>]*>)\s*&nbsp;\s*(</span>)', r'\g<1>محطات المحولات\g<2>'),
    (r'(<span[^>]*font-size:\s*22\.0pt[^>]*>)\s*&nbsp;\s*(</span>)', r'\g<1>إجراءات الصيانة\g<2>'), # The second match
    (r'(<font size="?6"?>)\s*(</font>)', r'\g<1>نظام معلومات إجراءات الصيانة\g<2>'),
    (r'(<font size="?6"?>)&nbsp;\s*(</font>)', r'\g<1>نظام معلومات إجراءات الصيانة\g<2>'),
]

files_to_check = []
for d in base_dirs:
    files_to_check.extend(glob.glob(os.path.join(d, "*.htm")))

fixed_count = 0

for fp in files_to_check:
    try:
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
            
        original_content = content
        
        # Simple string replacements for the exact spaces found in these files
        content = re.sub(
            r'(<SPAN lang=AR-SA[^>]*>\s*<FONT size=6>)\s+(</FONT>\s*</SPAN>)', 
            r'\1نظام معلومات إجراءات الصيانة\2', 
            content, flags=re.IGNORECASE)
            
        content = re.sub(
            r'(<span lang="AR-SA"[^>]*>\s*<font size="6">)\s+(</font>\s*</span>)', 
            r'\1نظام معلومات إجراءات الصيانة\2', 
            content, flags=re.IGNORECASE)
            
        # For the empty &nbsp; spans
        # Find the first one (usually left side)
        content = re.sub(
            r'(width="58%"[^>]*>)\s*(?:<span|<SPAN)[^>]*font-size:\s*22\.?0?pt[^>]*>\s*(?:&nbsp;| )\s*(?:</span>|</SPAN>)',
            r'\1\n<span lang="AR-SA" style="font-weight: 700; font-size: 22pt; font-family: Traditional Arabic;">محطات المحولات</span>',
            content, count=1, flags=re.IGNORECASE)
            
        # Find the second one (usually right side)
        content = re.sub(
            r'(width="33%"[^>]*>)\s*(?:<p[^>]*>)?\s*(?:<span|<SPAN)[^>]*font-size:\s*22\.?0?pt[^>]*>\s*(?:&nbsp;| )\s*(?:</span>|</SPAN>)(?:(?:<span|<SPAN)[^>]*>\s*(?:&nbsp;| )\s*(?:</span>|</SPAN>))?\s*(?:</p>|</P>)?',
            r'\1\n<p align="center"><span lang="AR-SA" style="font-weight: 700; font-size: 22pt; font-family: Traditional Arabic;">إجراءات الصيانة</span></p>',
            content, count=1, flags=re.IGNORECASE)

        if content != original_content:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed headers in: {os.path.basename(fp)}")
            fixed_count += 1
    except Exception as e:
        pass

print(f"\nTotal files fixed: {fixed_count}")
