import os
import re
from bs4 import BeautifulSoup

eng_dir = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\appr_docs\ad_subst"
files = [f for f in os.listdir(eng_dir) if f.endswith(".htm") or f.endswith(".html")]

print("Hyperlink targets inside English files:")
for f in sorted(files):
    filepath = os.path.join(eng_dir, f)
    with open(filepath, "r", encoding="windows-1252", errors="ignore") as file_obj:
        content = file_obj.read()
    
    soup = BeautifulSoup(content, "html.parser")
    links = soup.find_all("a")
    hrefs = [a.get("href") for a in links if a.get("href")]
    
    # Let's see what kinds of files are linked (extensions like .pdf, .htm) and their directories
    pdf_links = [h for h in hrefs if h.lower().endswith(".pdf")]
    htm_links = [h for h in hrefs if h.lower().endswith(".htm") or h.lower().endswith(".html")]
    
    # Group by directory prefix
    pdf_prefixes = set(os.path.dirname(p) for p in pdf_links)
    htm_prefixes = set(os.path.dirname(h) for h in htm_links)
    
    print(f" - {f}:")
    print(f"   * Linked PDFs: {len(pdf_links)} (directories: {pdf_prefixes})")
    print(f"   * Linked HTMs: {len(htm_links)} (directories: {htm_prefixes})")
