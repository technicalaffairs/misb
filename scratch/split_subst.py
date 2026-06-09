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
      <p align="right"><b><span dir="rtl"><font face="Traditional Arabic">&nbsp;<a href="{href}">{title}</a></font></span></b></TD>
    <td valign="top" width="98" height="7" style="border-style: none; border-width: medium" align="center">
      <b><font size="2" face="Arial"><span dir="ltr"><a href="{href}">{doc_id}</a></span></font></b></td>
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

# Modern sub-page HTML template
modern_page_template = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MPIS - {title}</title>
  <link rel="stylesheet" href="{root_prefix}style.css?v=2">
  <!-- FontAwesome for modern icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700&display=swap');
    body {{
      font-family: 'Cairo', 'Outfit', sans-serif;
      direction: rtl;
    }}
    .header-text-left {{
      text-align: right;
    }}
    .header-text-right {{
      text-align: left;
    }}
    .page-title-banner {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 15px 30px;
      text-align: center;
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--accent-teal);
      margin-top: 10px;
      box-shadow: var(--shadow-glow);
    }}
    /* Hide header when printing */
    @media print {{
      .top-bar, .header-section, .main-nav, .page-title-banner {{
        display: none !important;
      }}
      body {{
        background: white !important;
        color: black !important;
        padding: 0 !important;
      }}
    }}
  </style>
</head>
<body class="subpage-body">
  <div class="app-container">
    <!-- Top Bar with Contact Info and Language Toggle -->
    <div class="top-bar">
      <div class="contacts-info">
        <div class="contact-item">
          <i class="fa-solid fa-phone"></i>
          <span>الهاتف/الفاكس: 02 22601911</span>
        </div>
        <div class="contact-item">
          <i class="fa-solid fa-envelope"></i>
          <a href="mailto:mpisgd@hotmail.com">mpisgd@hotmail.com</a>
        </div>
        <div class="contact-item">
          <i class="fa-solid fa-server"></i>
          <span>رقم الخادم: 02 24010301</span>
        </div>
      </div>
      <a href="{root_prefix}index.htm" class="lang-switch">
        <i class="fa-solid fa-globe"></i>
        <span>English Version</span>
      </a>
    </div>

    <!-- Header Section -->
    <header class="header-section">
      <div class="header-text-left">
        <span class="org-hierarchy">وزارة الكهرباء والطاقة المتجددة</span>
        <h1 class="org-name">الشركة القابضة لكهرباء مصر</h1>
        <span class="org-subname">منطقة كهرباء مصر الوسطى - إدارة الشئون الفنية</span>
      </div>

      <div class="logo-container">
        <div class="logo-glow-wrapper">
          <img src="{root_prefix}images/eetc_logo.jpg" alt="EETC Logo" class="main-logo">
        </div>
        <div class="secondary-logos">
          <img src="{root_prefix}images/eehc_logo.gif" alt="EEHC Logo" class="sec-logo">
          <img src="{root_prefix}images/Flag5555.gif" alt="Egyptian Flag" class="sec-logo flag">
        </div>
      </div>

      <div class="header-text-right">
        <span class="org-hierarchy">قطاع تطوير نظم إجراءات الصيانة ومراقبة الجودة</span>
        <h2 class="org-name">نظام معلومات إجراءات الصيانة (MPIS)</h2>
        <span class="org-subname">الإدارة العامة لتطوير نظم إجراءات الصيانة</span>
      </div>
    </header>

    <!-- Navigation Menu Buttons -->
    <nav class="main-nav">
      <a href="{root_prefix}arabic_web/Ar_whatsnew/Ar_whatsnew.htm" class="nav-btn">
        <i class="fa-solid fa-bullhorn"></i>
        <span>ما هو الجديد</span>
      </a>
      <a href="{root_prefix}about/docs%20status/status.htm" class="nav-btn">
        <i class="fa-solid fa-chart-line"></i>
        <span>موقف المستندات</span>
      </a>
      <a href="{root_prefix}arabic_web/Ar_forms/A_form.htm" class="nav-btn">
        <i class="fa-solid fa-file-invoice"></i>
        <span>النماذج</span>
      </a>
      <a href="{root_prefix}arabic_web/Ar_Index.htm" class="nav-btn">
        <i class="fa-solid fa-house"></i>
        <span>الصفحة الرئيسية</span>
      </a>
      <a href="{root_prefix}arabic_web/Ar_about/Ar_about.htm" class="nav-btn">
        <i class="fa-solid fa-circle-info"></i>
        <span>ما هو الـ MPIS</span>
      </a>
      <a href="{root_prefix}arabic_web/Ar_admin_inst/Ar_draf_doc.htm" class="nav-btn">
        <i class="fa-solid fa-sliders"></i>
        <span>التعليمات الإدارية</span>
      </a>
      <a href="{root_prefix}draf_docs/draf_doc.htm" class="nav-btn">
        <i class="fa-solid fa-file-signature"></i>
        <span>مسودة المستندات</span>
      </a>
      <a href="{root_prefix}Coordinators/MPIS_Coord_main%20Page.htm" class="nav-btn">
        <i class="fa-solid fa-users-gear"></i>
        <span>المنسقون</span>
      </a>
    </nav>

    <!-- Category Title Banner -->
    <div class="page-title-banner">
      {title}
    </div>

    <!-- Document Table -->
    {content_html}

    <!-- Footer -->
    <footer class="footer-section">
      <p class="footer-copy">حقوق الطبع محفوظة &copy; الشركة القابضة لكهرباء مصر، قطاع تطوير نظم الصيانة ومراقبة الجودة 2026.</p>
      <p class="footer-note">تم تطوير الصفحات وتحديثها بمعرفة إدارة الشئون الفنية بمنطقة كهرباء مصر الوسطى</p>
    </footer>
  </div>
</body>
</html>"""

# Generate category HTML files
for cat_key, cat_data in categories.items():
    title_ar = cat_data["title"]
    filename = cat_data["filename"]
    docs = cat_data["docs"]
    
    table_rows_html = ""
    if len(docs) > 0:
        sorted_docs = sorted(docs, key=lambda x: x["doc_id"].upper())
        for doc in sorted_docs:
            if doc["type"] == "row":
                r_soup = BeautifulSoup(str(doc["row_soup"]), "html.parser").tr
                adjust_soup_paths(r_soup)
                table_rows_html += str(r_soup) + "\n"
            else:
                title_full = doc["title"]
                if doc["procedure"]:
                    title_full = f"{title_full} - {doc['procedure']}"
                r_soup = make_html_row(doc["date"], title_full, doc["href"], doc["doc_id"])
                table_rows_html += str(r_soup) + "\n"
    else:
        r_soup = make_empty_row()
        table_rows_html += str(r_soup) + "\n"
        
    content_html = f"""<table border="1" width="100%">
      <thead>
        <tr>
          <th width="15%" align="center">تاريخ الاعتماد</th>
          <th width="70%" align="center">اسم المستند</th>
          <th width="15%" align="center">رقم المستند</th>
        </tr>
      </thead>
      <tbody>
{table_rows_html}      </tbody>
    </table>"""
    
    final_html = modern_page_template.format(
        title=title_ar,
        root_prefix="../../../../",
        content_html=content_html
    )
    
    output_file = os.path.join(output_dir, filename)
    with open(output_file, "w", encoding="utf-8") as out_f:
        out_f.write(final_html)
        
    print(f"Generated page in isolated folder: {filename} ({len(docs)} documents)")

print("\nAll isolated category sub-pages generated successfully in new_pages/ directory!")
