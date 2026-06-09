"""
هذا السكريبت يقرأ ملفات الفهرس المرجعية المشفرة بـ windows-1256
ويستخرج النص العربي ليعرض محتوى الملف بشكل صحيح
"""
import re, os

files = {
    "Ar_ad_Trafo.htm": r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_Trafo.htm",
    "Ar_ad_CBs.htm": r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_CBs.htm",
    "Ar_ad_Batteries.htm": r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_Batteries.htm",
    "Ar_ad_tap_changers.htm": r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_tap_changers.htm",
    "Ar_ad_CT_PT_LA.htm": r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_CT_PT_LA.htm",
    "Ar_ad_DS_ES.htm": r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_DS_ES.htm",
    "Ar_ad_Busbars.htm": r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_Busbars.htm",
    "Ar_ad_compressors.htm": r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_compressors.htm",
    "Ar_ad_condensers.htm": r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_condensers.htm",
    "Ar_Distrib_Board.htm": r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_Distrib_Board.htm",
}

OUT = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\scratch\trafo_content.txt"
out_lines = []

for fname, fp in files.items():
    # Try both encodings
    for enc in ['windows-1256', 'utf-8']:
        try:
            with open(fp, encoding=enc) as f:
                raw = f.read()
            ar_count = len(re.findall(r'[\u0600-\u06FF]', raw))
            if ar_count > 10:
                break
        except:
            continue

    # Strip HTML tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&[a-zA-Z]+;', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    out_lines.append(f"\n{'='*60}")
    out_lines.append(f"FILE: {fname} (enc={enc}, AR={ar_count})")
    out_lines.append(f"{'='*60}")
    
    # Show non-trivial chunks
    parts = [p.strip() for p in re.split(r'  +', text) if p.strip() and len(p.strip()) > 3]
    count = 0
    for p in parts:
        if count > 60:
            break
        if len(p) > 3:
            out_lines.append(p[:300])
            count += 1

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print(f"Done -> {OUT}")
