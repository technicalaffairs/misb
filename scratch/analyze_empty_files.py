import re, os

files = [
    r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_Trafo.htm",
    r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_CBs.htm",
    r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_Batteries.htm",
    r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_tap_changers.htm",
    r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_CT_PT_LA.htm",
    r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_DS_ES.htm",
    r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_Busbars.htm",
    r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_compressors.htm",
    r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_condensers.htm",
    r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_Distrib_Board.htm",
]

OUT = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\scratch\trafo_analysis.txt"
out_lines = []

for fp in files:
    fname = os.path.basename(fp)
    with open(fp, encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    ar = len(re.findall(r'[\u0600-\u06FF]', content))
    total = len(content)
    lines = content.split('\n')
    
    out_lines.append(f"\n{'='*60}")
    out_lines.append(f"FILE: {fname} | Size: {total//1024} KB | AR chars: {ar}")
    out_lines.append(f"{'='*60}")
    
    # Find href links to understand what documents are referenced
    links = re.findall(r'href=["\']([^"\']+\.htm[^"\']*)["\']', content, re.IGNORECASE)
    if links:
        out_lines.append(f"LINKS ({len(links)}):")
        for lnk in links[:20]:
            out_lines.append(f"  -> {lnk}")
    
    # Show meaningful text lines
    out_lines.append("TEXT PREVIEW (non-empty lines):")
    count = 0
    for i, line in enumerate(lines, 1):
        stripped = re.sub(r'<[^>]+>', ' ', line).strip()
        stripped = re.sub(r'\s+', ' ', stripped).strip()
        if len(stripped) > 8 and count < 30:
            out_lines.append(f"  L{i}: {stripped[:200]}")
            count += 1

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print(f"Done. Output: {OUT}")
