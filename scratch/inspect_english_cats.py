import os
import re

eng_dir = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\appr_docs\ad_subst"
files = [f for f in os.listdir(eng_dir) if f.endswith(".htm") or f.endswith(".html")]

print("English files and the document codes they contain:")
for f in sorted(files):
    filepath = os.path.join(eng_dir, f)
    with open(filepath, "r", encoding="windows-1252", errors="ignore") as file_obj:
        content = file_obj.read()
    
    # find all patterns of document codes (e.g. T-xxx, CB-xxx, etc.)
    codes = re.findall(r'[a-zA-Z]+-\d+-\w+', content)
    if not codes:
        codes = re.findall(r'[a-zA-Z]+-\d+', content)
        
    unique_prefixes = sorted(list(set(c.split("-")[0].upper() for c in codes)))
    print(f" - {f}: total codes {len(codes)}, unique prefixes: {unique_prefixes}, snippet codes: {list(set(codes))[:10]}")
