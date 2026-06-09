import os
import re
import json
from bs4 import BeautifulSoup

def clean_txt(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_with_bs4(filepath):
    filename = os.path.basename(filepath)
    doc_id_fallback = os.path.splitext(filename)[0]
    
    with open(filepath, "r", encoding="windows-1252", errors="ignore") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    # Let's collect all text from cells
    tds = soup.find_all("td")
    
    doc_id = doc_id_fallback
    equipment = ""
    procedure = ""
    date_str = ""
    
    # We will search for keywords in cells
    for td in tds:
        text = td.get_text()
        clean = clean_txt(text)
        
        # Check for Document Number
        # "رقم المستند" is "&#1585;&#1602;&#1605; &#1575;&#1604;&#1605;&#1587;&#1578;&#1606;&#1583;"
        if "رقم المستند" in clean:
            # Try to extract the document code from this cell's text
            # E.g. "رقم المستند: CT-014-r0a"
            match = re.search(r'([a-zA-Z]+-\d+-\w+|[a-zA-Z]+-\d+)', clean)
            if match:
                doc_id = match.group(1)
        
        # Check for Equipment (Title)
        # "المعدة" is "&#1575;&#1604;&#1605;&#1593;&#1583;&#1577;"
        if "المعدة" in clean:
            # The equipment name is often the rest of the text in the cell after "المعدة:"
            parts = clean.split("المعدة:")
            if len(parts) > 1 and len(parts[1].strip()) > 3:
                equipment = parts[1].strip()
            else:
                # Sometimes it is just the cell content minus "المعدة" and ":"
                val = clean.replace("المعدة", "").replace(":", "").strip()
                if len(val) > 3:
                    equipment = val
                    
        # Check for Procedure
        # "الإجراء" is "&#1575;&#1604;&#1573;&#1580;&#1585;&#1575;&#1569;"
        if "الإجراء" in clean:
            parts = clean.split("الإجراء:")
            if len(parts) > 1 and len(parts[1].strip()) > 3:
                procedure = parts[1].strip()
            else:
                val = clean.replace("الإجراء", "").replace(":", "").strip()
                if len(val) > 3:
                    procedure = val
                    
        # Check for Date
        # "تاريخ الاعتماد" is "&#1578;&#1575;&#1585;&#1610;&#1582; &#1575;&#1604;&#1575;&#1593;&#1578;&#1605;&#1575;&#1583;"
        if "تاريخ الاعتماد" in clean or "تاريخ اعتماد" in clean or "تاريخالاعتماد" in clean:
            parts = re.split(r'تاريخ\s*(?:الاعتماد|اعتماد|الاعتما|الاعتـماد)\s*:', clean)
            if len(parts) > 1 and len(parts[1].strip()) > 3:
                date_str = parts[1].strip()
            else:
                val = clean.replace("تاريخ الاعتماد", "").replace("تاريخ اعتماد", "").replace(":", "").strip()
                if len(val) > 3:
                    date_str = val
                    
    # Double check if we still missed title or date from structured tables
    if not date_str:
        # Fallback date search
        date_match = re.search(r'(\d{1,2}\s+(?:يناير|فبراير|مارس|أبريل|ابريل|مايو|يونيو|يوليو|أغسطس|اغسطس|سبتمبر|أكتوبر|اكتوبر|نوفمبر|ديسمبر)\s+\d{4})', clean_txt(soup.get_text()))
        if date_match:
            date_str = date_match.group(1)
            
    # Clean up standard artifacts or prefixes in equipment/procedure
    if equipment:
        # If equipment has extra text or trailing/leading noise, clean it
        pass
        
    return {
        "doc_id": doc_id,
        "title": equipment,
        "procedure": procedure,
        "date": date_str,
        "filename": filename
    }

ad_ss_docs_path = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\ad_ss_docs"
htm_files = [f for f in os.listdir(ad_ss_docs_path) if f.endswith(".htm") or f.endswith(".html")]

metadata_list = []
for f in htm_files:
    filepath = os.path.join(ad_ss_docs_path, f)
    try:
        meta = parse_with_bs4(filepath)
        metadata_list.append(meta)
    except Exception as e:
        print(f"Error parsing {f}: {e}")

print(f"Parsed {len(metadata_list)} files.")

# Save to json file for reference
output_json = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\scratch\ad_ss_docs_metadata.json"
with open(output_json, "w", encoding="utf-8") as out:
    json.dump(metadata_list, out, indent=2, ensure_ascii=False)

print(f"Metadata saved to {output_json}")

# Print first 20 parsed items
for m in sorted(metadata_list, key=lambda x: x["doc_id"])[:20]:
    print(f"ID: {m['doc_id']:12s} | Date: {m['date']:15s} | Title: {m['title'][:30]:30s} | Proc: {m['procedure'][:30]}")
