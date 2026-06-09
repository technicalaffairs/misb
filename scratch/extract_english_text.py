import os
import re
from bs4 import BeautifulSoup

eng_dir = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\appr_docs\ad_subst\ad_sub_tp"
files = ["T-022-r0.htm", "T-024-r0.htm", "T-025-r0.htm", "T-026-r0.htm", "T-027-r0.htm"]

sentences = set()

for f in files:
    filepath = os.path.join(eng_dir, f)
    if not os.path.exists(filepath):
        continue
    with open(filepath, "r", encoding="windows-1252", errors="ignore") as file_obj:
        html = file_obj.read()
    
    soup = BeautifulSoup(html, "html.parser")
    # Get all text from body
    for node in soup.find_all(text=True):
        if node.parent.name not in ['script', 'style', 'title']:
            txt = node.strip()
            if txt and len(txt) > 2:
                # Clean up spacing
                txt_clean = " ".join(txt.split())
                sentences.add(txt_clean)

# Print sorted unique sentences
print(f"Found {len(sentences)} unique text blocks.")
output_file = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\scratch\extracted_sentences.txt"
with open(output_file, "w", encoding="utf-8") as out:
    for s in sorted(list(sentences)):
        out.write(s + "\n")
        
print(f"Saved sentences to {output_file}")
