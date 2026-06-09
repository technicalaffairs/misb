import os
import re
import json
from bs4 import BeautifulSoup

subst_file = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_subst.htm"
output_dir = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\new_pages"
ad_ss_docs_path = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\ad_ss_docs"
new_translated_path = os.path.join(ad_ss_docs_path, "new_translated")
metadata_json_path = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\scratch\ad_ss_docs_metadata.json"

# Create output folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Helper to translate English months in date strings
months_dict = {
    "Jan": "يناير", "Feb": "فبراير", "Mar": "مارس", "Apr": "أبريل",
    "May": "مايو", "Jun": "يونيو", "Jul": "يوليو", "Aug": "أغسطس",
    "Sep": "سبتمبر", "Oct": "أكتوبر", "Nov": "نوفمبر", "Dec": "ديسمبر"
}

def clean_date_arabic(date_str):
    for eng, ar in months_dict.items():
        date_str = date_str.replace(eng, ar)
    return date_str

# Load unlisted legacy documents metadata
with open(metadata_json_path, "r", encoding="utf-8") as f:
    unlisted_docs = json.load(f)

# Read the original Ar_ad_subst.htm content
with open(subst_file, "r", encoding="windows-1252", errors="ignore") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")
table = soup.find("table")
if not table:
    print("Error: Outer table not found in Ar_ad_subst.htm")
    exit()

all_rows = table.find_all("tr")
print(f"Total rows in outer table: {len(all_rows)}")

# The first 12 rows (indices 0 to 11) are the header rows of the page
header_rows = all_rows[:12]
doc_rows = all_rows[12:]

# Let's extract the header template HTML
header_soup = BeautifulSoup(html_content, "html.parser")
h_table = header_soup.find("table")
h_table.clear() # Clear all contents

for r in header_rows:
    h_table.append(BeautifulSoup(str(r), "html.parser").tr)

# Categories definition
categories = {
    "CBs": {
        "title": "القواطع الكهربائية",
        "filename": "Ar_ad_CBs.htm",
        "docs": []
    },
    "Trafo": {
        "title": "محولات القدرة",
        "filename": "Ar_ad_Trafo.htm",
        "docs": []
    },
    "Busbars": {
        "title": "قضبان التوصيل",
        "filename": "Ar_ad_Busbars.htm",
        "docs": []
    },
    "DS_ES": {
        "title": "سكاكين الفصل والتأريض",
        "filename": "Ar_ad_DS_ES.htm",
        "docs": []
    },
    "Batteries": {
        "title": "البطاريات والشواحن وموانع الانقطاع",
        "filename": "Ar_ad_Batteries.htm",
        "docs": []
    },
    "CT_PT_LA": {
        "title": "محولات التيار والجهد ومانعات الصواعق",
        "filename": "Ar_ad_CT_PT_LA.htm",
        "docs": []
    },
    "tap_changers": {
        "title": "مغيرات الجهد",
        "filename": "Ar_ad_tap_changers.htm",
        "docs": []
    },
    "condensers": {
        "title": "المكثفات الكهربائية",
        "filename": "Ar_ad_condensers.htm",
        "docs": []
    },
    "compressors": {
        "title": "الضواغط",
        "filename": "Ar_ad_compressors.htm",
        "docs": []
    },
    "Distrib_Board": {
        "title": "لوحات التوزيع",
        "filename": "Ar_Distrib_Board.htm",
        "docs": []
    },
    "TD_SS_PS": {
        "title": "التعليمات الفنية والتوجيهات",
        "filename": "Ar_ad_TD-SS+PS.htm",
        "docs": []
    },
    "TB_SS_PS": {
        "title": "النشرات الفنية",
        "filename": "Ar_ad_TB-SS+PS.htm",
        "docs": []
    }
}

# Function to match a document ID to a category
def get_category_key(doc_id):
    doc_id = doc_id.upper()
    if doc_id.startswith("CB-"): return "CBs"
    if doc_id.startswith("BB-"): return "Busbars"
    if doc_id.startswith("DS-") or doc_id.startswith("ES-"): return "DS_ES"
    if doc_id.startswith("CT-") or doc_id.startswith("PT-") or doc_id.startswith("LA-"): return "CT_PT_LA"
    if doc_id.startswith("TC-"): return "tap_changers"
    if doc_id.startswith("TD-"): return "TD_SS_PS"
    if doc_id.startswith("TB-"): return "TB_SS_PS"
    if doc_id.startswith("DES-"): return "Distrib_Board"
    if doc_id.startswith("CP-"): return "compressors"
    
    if doc_id.startswith("B-") or doc_id.startswith("CH-"):
        return "Batteries"
    if doc_id.startswith("C-"):
        return "condensers"
    if doc_id.startswith("T-") or doc_id == "FS-007-R0A":
        return "Trafo"
    if doc_id.startswith("FS-"):
        if doc_id == "FS-007-R0A":
            return "Trafo"
        else:
            return "TD_SS_PS"
            
    return "Other"

handled_ids = set()

# Process original rows in Ar_ad_subst.htm
for r in doc_rows:
    row_text = r.get_text()
    match = re.search(r'([a-zA-Z]+-\d+-\w+|[a-zA-Z]+-\d+)', row_text)
    if match:
        doc_id = match.group(1)
        cat_key = get_category_key(doc_id)
        if cat_key != "Other":
            categories[cat_key]["docs"].append({
                "type": "row",
                "doc_id": doc_id,
                "row_soup": r
            })
            handled_ids.add(doc_id.upper())

# Now add unlisted legacy documents from ad_ss_docs/
for doc in unlisted_docs:
    doc_id = doc["doc_id"]
    doc_id_upper = doc_id.upper()
    
    if "_OLD" in doc_id_upper:
        continue
        
    if doc_id_upper not in handled_ids:
        title = doc["title"].strip()
        proc = doc["procedure"].strip()
        date = clean_date_arabic(doc["date"].strip())
        
        pdf_name = f"{doc_id}.pdf"
        pdf_path = os.path.join(ad_ss_docs_path, pdf_name)
        if os.path.exists(pdf_path):
            href = f"../ad_ss_docs/{pdf_name}"
        else:
            href = f"../ad_ss_docs/{doc['filename']}"
            
        cat_key = get_category_key(doc_id)
        if cat_key != "Other":
            if not title:
                title = f"مستند فني رقم {doc_id}"
            categories[cat_key]["docs"].append({
                "type": "meta",
                "doc_id": doc_id,
                "title": title,
                "procedure": proc,
                "date": date,
                "href": href
            })
            handled_ids.add(doc_id_upper)

# Now scan and load the new translated documents from ad_ss_docs/new_translated/
if os.path.exists(new_translated_path):
    trans_files = [f for f in os.listdir(new_translated_path) if f.endswith(".htm") or f.endswith(".html")]
    print(f"Found {len(trans_files)} translated files in new_translated/ folder.")
    
    for f in trans_files:
        filepath = os.path.join(new_translated_path, f)
        doc_id = os.path.splitext(f)[0].replace("a", "") # E.g. T-022-r0a -> T-022-r0
        doc_id_upper = doc_id.upper()
        
        # Parse metadata from the translated file
        with open(filepath, "r", encoding="utf-8") as file_obj:
            t_html = file_obj.read()
        
        t_soup = BeautifulSoup(t_html, "html.parser")
        tds = t_soup.find_all("td")
        
        equipment = ""
        procedure = ""
        date_str = ""
        
        for td in tds:
            text = td.get_text().strip()
            text_clean = " ".join(text.split())
            if "المعدة" in text_clean:
                val = text_clean.replace("المعدة", "").replace(":", "").strip()
                if len(val) > 2:
                    equipment = val
            elif "الإجراء" in text_clean or "الاجراء" in text_clean:
                val = text_clean.replace("الإجراء", "").replace("الاجراء", "").replace(":", "").strip()
                if len(val) > 2:
                    procedure = val
            elif "تاريخ الاعتماد" in text_clean or "تاريخالاعتماد" in text_clean or "تاريخ اعتماد" in text_clean:
                val = text_clean.replace("تاريخ الاعتماد", "").replace("تاريخالاعتماد", "").replace("تاريخ اعتماد", "").replace(":", "").strip()
                if len(val) > 2:
                    date_str = val
        
        date_str = clean_date_arabic(date_str)
        
        # Use PDF version if exists in new/ directory or as fallback
        pdf_name = f"{doc_id}.pdf" # e.g. T-022-r0.pdf
        href = f"../ad_ss_docs/new_translated/{f}" # Link to translated HTML
        
        cat_key = get_category_key(doc_id)
        if cat_key != "Other":
            # Avoid duplicate if already in lists
            categories[cat_key]["docs"].append({
                "type": "meta",
                "doc_id": doc_id_upper + "a", # Add 'a' to indicate Arabic version
                "title": equipment,
                "procedure": procedure,
                "date": date_str,
                "href": href
            })
            try:
                print(f"Translated file merged: ID {doc_id_upper}a -> {cat_key} | Title: {equipment}")
            except Exception:
                safe_eq = equipment.encode('ascii', errors='replace').decode('ascii')
                print(f"Translated file merged: ID {doc_id_upper}a -> {cat_key} | Title (safe): {safe_eq}")

# Function to adjust relative links in BeautifulSoup elements to account for being 1 level deeper
def adjust_soup_paths(soup):
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if href:
            # Check if it's already updated
            if not href.startswith("http") and not href.startswith("#"):
                if href.startswith("ad_ss_docs/"):
                    a["href"] = "../" + href
                elif href.startswith("../../"):
                    a["href"] = "../" + href
                elif href.startswith("../"):
                    # Double it
                    a["href"] = "../" + href
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and not src.startswith("http"):
            if src.startswith("../../"):
                img["src"] = "../" + src

# Function to generate an HTML row block for extra/metadata items
def make_html_row(date, title, href, doc_id):
    row_html = f"""  <tr>
    <TD style="BORDER-RIGHT: medium none; BORDER-TOP: medium none; BORDER-LEFT: medium none; BORDER-BOTTOM: medium none" align=center width=194 height=25 dir="rtl">
      <p dir="rtl"><b><font face="Traditional Arabic"><span lang="ar-sa">{date}</span></font></b></TD>
    <TD style="BORDER-RIGHT: medium none; BORDER-TOP: medium none; BORDER-LEFT: medium none; BORDER-BOTTOM: medium none" align=right width=1010 height=1 dir="rtl">
      <p align="right"><b><span dir="rtl"><font face="Traditional Arabic">&nbsp;<a href="{href}"><font color="#000000">{title}</font></a></font></span></b></TD>
    <td valign="top" width="98" height="7" style="border-style: none; border-width: medium" align="center">
      <b><font size="2" face="Arial"><span dir="ltr"><a href="{href}"><font color="#000000">{doc_id}</font></a></span></font></b></td>
  </tr>"""
    return BeautifulSoup(row_html, "html.parser").tr

# Function to generate an empty placeholder row
def make_empty_row():
    row_html = """  <tr>
    <TD style="BORDER-RIGHT: medium none; BORDER-TOP: medium none; BORDER-LEFT: medium none; BORDER-BOTTOM: medium none" align=center width=194 height=25 dir="rtl">
      <b><font face="Traditional Arabic">-</font></b></TD>
    <TD style="BORDER-RIGHT: medium none; BORDER-TOP: medium none; BORDER-LEFT: medium none; BORDER-BOTTOM: medium none" align=center width=1010 height=1 dir="rtl">
      <p align="center"><b><font face="Traditional Arabic" color="#FF0000">لا توجد مستندات معتمدة باللغة العربية حالياً لهذه الفئة، يرجى مراجعة النسخة الإنجليزية</font></b></TD>
    <td valign="top" width="98" height="7" style="border-style: none; border-width: medium" align="center">
      <b><font size="2" face="Arial">-</font></b></td>
  </tr>"""
    return BeautifulSoup(row_html, "html.parser").tr

# Generate category HTML files
for cat_key, cat_data in categories.items():
    title_ar = cat_data["title"]
    filename = cat_data["filename"]
    docs = cat_data["docs"]
    
    # 1. Start with the header template
    cat_soup = BeautifulSoup(str(header_soup), "html.parser")
    cat_table = cat_soup.find("table")
    
    # Set proper encoding meta tag to UTF-8
    meta_charset = cat_soup.find("meta", attrs={"http-equiv": "Content-Type"})
    if meta_charset:
        meta_charset["content"] = "text/html; charset=utf-8"
    else:
        meta_c = cat_soup.find("meta", charset=True)
        if meta_c:
            meta_c["charset"] = "utf-8"
        else:
            new_meta = cat_soup.new_tag("meta", attrs={"http-equiv": "Content-Type", "content": "text/html; charset=utf-8"})
            if cat_soup.head:
                cat_soup.head.insert(0, new_meta)
    
    # Update <title> element
    title_el = cat_soup.find("title")
    if title_el:
        title_el.string = f"MPIS - {title_ar}"
        
    # Update category header cell text "محطات المحولات" to the specific category name
    header_td = cat_soup.find("td", width="553", valign="middle")
    if header_td:
        font_el = header_td.find("font", face="Traditional Arabic")
        if font_el and font_el.find("span"):
            font_el.find("span").string = title_ar
        else:
            header_td.string = title_ar
            
    # Adjust relative paths in the header navigation
    adjust_soup_paths(cat_soup)
    
    # Update style, body background, and images in the header soup to depth 4
    for link in cat_soup.find_all("link", rel="stylesheet"):
        href = link.get("href", "")
        if "style.css" in href:
            link["href"] = "../../../../style.css"
            
    body = cat_soup.find("body")
    if body and body.get("background"):
        body["background"] = body["background"].replace("../../../images/", "../../../../images/")
        
    for img in cat_soup.find_all("img"):
        src = img.get("src", "")
        if "../../../images/" in src:
            img["src"] = src.replace("../../../images/", "../../../../images/")

    # 2. Add document rows
    if len(docs) > 0:
        sorted_docs = sorted(docs, key=lambda x: x["doc_id"].upper())
        for doc in sorted_docs:
            if doc["type"] == "row":
                # Original row (make a clean copy and adjust links inside it)
                r_soup = BeautifulSoup(str(doc["row_soup"]), "html.parser").tr
                adjust_soup_paths(r_soup)
                cat_table.append(r_soup)
            else:
                # Extra metadata row
                title_full = doc["title"]
                if doc["procedure"]:
                    title_full = f"{title_full} - {doc['procedure']}"
                r_soup = make_html_row(doc["date"], title_full, doc["href"], doc["doc_id"])
                cat_table.append(r_soup)
    else:
        # Empty placeholder row
        cat_table.append(make_empty_row())
        
    # 3. Add closing tags
    output_file = os.path.join(output_dir, filename)
    final_html = str(cat_soup)
    final_html += "\n<![if !supportEmptyParas]>\n\n</BODY></HTML>"
    
    with open(output_file, "w", encoding="utf-8") as out_f:
        out_f.write(final_html)
        
    print(f"Generated page in isolated folder: {filename} ({len(docs)} documents)")

print("\nAll isolated category sub-pages generated successfully in new_pages/ directory!")
