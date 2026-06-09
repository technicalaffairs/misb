import os
import re
from bs4 import BeautifulSoup

# Define paths
arabic_web_dir = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web"

# Define the HTML template for modern sub-pages
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

    <!-- Main Content -->
    {content_html}

    <!-- Footer -->
    <footer class="footer-section">
      <p class="footer-copy">حقوق الطبع محفوظة &copy; الشركة القابضة لكهرباء مصر، قطاع تطوير نظم الصيانة ومراقبة الجودة 2026.</p>
      <p class="footer-note">تم تطوير الصفحات وتحديثها بمعرفة إدارة الشئون الفنية بمنطقة كهرباء مصر الوسطى</p>
    </footer>
  </div>
</body>
</html>"""

def clean_legacy_html(html):
    # Strip FrontPage conditional comments
    html = re.sub(r'<!\[if[^\]]*\]>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<!\[endif\]>', '', html, flags=re.IGNORECASE)
    
    # Strip premature body/html closing tags
    html = re.sub(r'</body[^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'</html[^>]*>', '', html, flags=re.IGNORECASE)
    
    return html

def adjust_content_links(soup, root_prefix):
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if href and not href.startswith("http") and not href.startswith("#"):
            if href.startswith("../../../../"):
                a["href"] = href.replace("../../../../", root_prefix)
            elif href.startswith("../../../"):
                a["href"] = href.replace("../../../", root_prefix)
            elif href.startswith("../../"):
                a["href"] = href.replace("../../", root_prefix)
            elif href.startswith("../"):
                a["href"] = href.replace("../", root_prefix + "arabic_web/")

def update_whatsnew():
    filepath = os.path.join(arabic_web_dir, "Ar_whatsnew", "Ar_whatsnew.htm")
    print("Modernizing What's New page...")
    with open(filepath, "r", encoding="windows-1256", errors="ignore") as f:
        html = f.read()
    
    html = clean_legacy_html(html)
    soup = BeautifulSoup(html, "html.parser")
    content_table = soup.find("table", id="AutoNumber1")
    
    adjust_content_links(content_table, "../../")
    
    content_html = str(content_table)
    final_html = modern_page_template.format(
        title="ما هو الجديد",
        root_prefix="../../",
        content_html=content_html
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_html)

def update_about():
    filepath = os.path.join(arabic_web_dir, "Ar_about", "Ar_about.htm")
    print("Modernizing About page...")
    with open(filepath, "r", encoding="windows-1256", errors="ignore") as f:
        html = f.read()
    
    html = clean_legacy_html(html)
    soup = BeautifulSoup(html, "html.parser")
    
    # Decompose all tables since the content is outside the tables
    tables = soup.find_all("table")
    for t in tables:
        t.decompose()
        
    adjust_content_links(soup.body, "../../")
    
    content_html = "".join([str(child) for child in soup.body.contents])
    final_html = modern_page_template.format(
        title="ما هو الـ MPIS",
        root_prefix="../../",
        content_html=content_html
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_html)

def update_forms():
    filepath = os.path.join(arabic_web_dir, "Ar_forms", "A_form.htm")
    print("Modernizing Forms page...")
    with open(filepath, "r", encoding="windows-1256", errors="ignore") as f:
        html = f.read()
    
    html = clean_legacy_html(html)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    
    rows = table.find_all("tr")
    content_rows = rows[8:] # content starts from row index 8
    
    new_table_soup = BeautifulSoup('<table border="1" width="100%"></table>', "html.parser")
    new_table = new_table_soup.table
    for r in content_rows:
        new_table.append(r)
        
    adjust_content_links(new_table, "../../")
    
    content_html = str(new_table)
    final_html = modern_page_template.format(
        title="النماذج والوثائق",
        root_prefix="../../",
        content_html=content_html
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_html)

def update_appr_doc():
    filepath = os.path.join(arabic_web_dir, "Ar_appr_docs", "Ar_appr_doc.htm")
    print("Modernizing Approved Documents main category page...")
    with open(filepath, "r", encoding="windows-1256", errors="ignore") as f:
        html = f.read()
    
    html = clean_legacy_html(html)
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    content_table = tables[1] # the second table contains the category cards grid
    
    adjust_content_links(content_table, "../../")
    
    content_html = str(content_table)
    final_html = modern_page_template.format(
        title="المستندات المعتمدة",
        root_prefix="../../",
        content_html=content_html
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_html)

def update_admin_draf():
    filepath = os.path.join(arabic_web_dir, "Ar_admin_inst", "Ar_draf_doc.htm")
    print("Modernizing Administrative Instructions page...")
    with open(filepath, "r", encoding="windows-1256", errors="ignore") as f:
        html = f.read()
    
    html = clean_legacy_html(html)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    
    rows = table.find_all("tr")
    content_rows = rows[7:] # content starts from row index 7
    
    new_table_soup = BeautifulSoup('<table border="1" width="100%"></table>', "html.parser")
    new_table = new_table_soup.table
    for r in content_rows:
        new_table.append(r)
        
    adjust_content_links(new_table, "../../")
    
    content_html = str(new_table)
    final_html = modern_page_template.format(
        title="التعليمات والمنشورات الإدارية",
        root_prefix="../../",
        content_html=content_html
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_html)

# Execute modernization
update_whatsnew()
update_about()
update_forms()
update_appr_doc()
update_admin_draf()

print("All 5 main portal pages modernized successfully!")
