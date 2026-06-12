import os
import re

arabic_dir = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web"
files_with_links = set()

for root, _, files in os.walk(arabic_dir):
    for f in files:
        if f.endswith(".htm") or f.endswith(".html"):
            filepath = os.path.join(root, f)
            try:
                with open(filepath, "r", encoding="utf-8") as f_in:
                    content = f_in.read()
                matches = re.findall(r"href=[\"\'\s]*([^\"\'\s>]*gen_docs[^\"\'\s>]*)[\"\'\s]*", content, re.IGNORECASE)
                if matches:
                    files_with_links.add(filepath)
            except Exception as e:
                pass

for f in sorted(files_with_links):
    print(f)
