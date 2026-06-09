import os
import re
from html.parser import HTMLParser

class DocMetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.in_title = False
        self.title_tag_text = ""

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.in_title = True

    def handle_data(self, data):
        if self.in_title:
            self.title_tag_text += data
        else:
            self.text_content.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

def clean_arabic_text(text):
    # Normalize spaces
    text = " ".join(text.split())
    # Keep arabic characters, numbers, slashes, dashes, parentheses
    return text

def parse_doc_file(filepath):
    filename = os.path.basename(filepath)
    doc_id = os.path.splitext(filename)[0]
    
    with open(filepath, "r", encoding="windows-1252", errors="ignore") as f:
        html = f.read()

    # Basic extraction using regex is often safer for these nested tables
    # Let's extract date
    date_match = re.search(r'&#1578;&#1575;&#1585;&#1610;&#1582;\s*(?:&#1575;&#1604;&#1575;&#1593;&#1578;&#1605;&#1575;&#1583;)?\s*:\s*([^<]+)', html)
    if not date_match:
        # Fallback date search
        date_match = re.search(r'(\d{1,2}\s*&#1610;&#1608;&#1604;&#1610;&#1608;|\d{1,2}\s*&#1605;&#1575;&#1585;&#1587;|\d{1,2}\s*&#1571;&#1576;&#1585;&#1610;&#1604;|\d{1,2}\s*&#1606;&#1608;&#1601;&#1605;&#1576;&#1585;|\d{1,2}\s*&#1605;&#1575;&#1610;&#1608;|\d{1,2}\s*&#1587;&#1576;&#1578;&#1605;&#1576;&#1585;|\d{1,2}\s*&#1571;&#1603;&#1578;&#1608;&#1576;&#1585;|\d{1,2}\s*&#1610;&#1608;&#1606;&#1610;&#1608;|\d{1,2}\s*&#1601;&#1576;&#1585;&#1575;&#1610;&#1585;|\d{1,2}\s*&#1571;&#1594;&#1587;&#1591;&#1587;|\d{1,2}\s*&#1610;&#1606;&#1575;&#1610;&#1585;|\d{1,2}\s*&#1583;&#1610;&#1587;&#1605;&#1576;&#1585;)\s*\d{4}', html)
    
    date_str = ""
    if date_match:
        date_str = date_match.group(0 if date_match.lastindex is None else 1).strip()
        # Clean tags if any
        date_str = re.sub('<[^<]+?>', '', date_str)
        date_str = clean_arabic_text(date_str)

    # Let's extract document title: usually under "المعدة:" cell
    # Looking for: &#1575;&#1604;&#1605;&#1593;&#1583;&#1577;:
    equipment_match = re.search(r'&#1575;&#1604;&#1605;&#1593;&#1583;&#1577;\s*:\s*<br>(.*?)</td>', html, re.DOTALL | re.IGNORECASE)
    if not equipment_match:
        equipment_match = re.search(r'&#1575;&#1604;&#1605;&#1593;&#1583;&#1577;\s*:\s*(.*?)</td>', html, re.DOTALL | re.IGNORECASE)
    
    title_str = ""
    if equipment_match:
        title_str = equipment_match.group(1).strip()
        title_str = re.sub('<[^<]+?>', ' ', title_str)
        title_str = clean_arabic_text(title_str)

    # Let's extract procedure: usually under "الإجراء:" cell
    # Looking for: &#1575;&#1604;&#1573;&#1580;&#1585;&#1575;&#1569;:
    proc_match = re.search(r'&#1575;&#1604;&#1573;&#1580;&#1585;&#1575;&#1569;\s*:\s*<br>(.*?)</td>', html, re.DOTALL | re.IGNORECASE)
    if not proc_match:
        proc_match = re.search(r'&#1575;&#1604;&#1573;&#1580;&#1585;&#1575;&#1569;\s*:\s*(.*?)</td>', html, re.DOTALL | re.IGNORECASE)
        
    proc_str = ""
    if proc_match:
        proc_str = proc_match.group(1).strip()
        proc_str = re.sub('<[^<]+?>', ' ', proc_str)
        proc_str = clean_arabic_text(proc_str)

    return {
        "doc_id": doc_id,
        "title": title_str,
        "procedure": proc_str,
        "date": date_str,
        "filename": filename
    }

ad_ss_docs_path = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\ad_ss_docs"
htm_files = [f for f in os.listdir(ad_ss_docs_path) if f.endswith(".htm") or f.endswith(".html")]

metadata_list = []
for f in htm_files:
    filepath = os.path.join(ad_ss_docs_path, f)
    try:
        meta = parse_doc_file(filepath)
        metadata_list.append(meta)
    except Exception as e:
        print(f"Error parsing {f}: {e}")

print(f"Successfully parsed {len(metadata_list)} files.")
for meta in sorted(metadata_list, key=lambda x: x["doc_id"]):
    print(f"ID: {meta['doc_id']:15s} | Date: {meta['date']:15s} | Title: {meta['title'][:40]:40s} | Proc: {meta['procedure'][:30]}")
