import os
import re

base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
arabic_web_dir = os.path.join(base_dir, 'arabic_web')
ar_index_path = os.path.join(arabic_web_dir, 'Ar_Index.htm')

updated_files = 0

for root, dirs, files in os.walk(arabic_web_dir):
    for f in files:
        if f.endswith('.htm') or f.endswith('.html'):
            filepath = os.path.join(root, f)
            if filepath == ar_index_path or 'scratch' in filepath or 'Ar_index_old' in filepath:
                continue
                
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
            except UnicodeDecodeError:
                try:
                    with open(filepath, 'r', encoding='windows-1256') as file:
                        content = file.read()
                except: continue

            # Determine level
            rel_path = os.path.relpath(filepath, arabic_web_dir)
            level = rel_path.count(os.sep)
            prefix = '../' * level if level > 0 else ''

            # Construct the exact nav the user wants
            new_nav = f'''<nav class="main-nav">
      <a href="{prefix}Ar_whatsnew/Ar_whatsnew.htm" class="nav-btn">
        <i class="fa-solid fa-bullhorn"></i>
        <span>ما هو الجديد</span>
      </a>
      <a href="{prefix}Ar_about/docs%20status/Ar_status.htm" class="nav-btn">
        <i class="fa-solid fa-chart-line"></i>
        <span>موقف المستندات</span>
      </a>
      <a href="{prefix}Ar_forms/A_form.htm" class="nav-btn">
        <i class="fa-solid fa-file-invoice"></i>
        <span>النماذج</span>
      </a>
      <a href="{prefix}Ar_Index.htm" class="nav-btn">
        <i class="fa-solid fa-house"></i>
        <span>الصفحة الرئيسية</span>
      </a>
      <a href="{prefix}Ar_about/Ar_about.htm" class="nav-btn">
        <i class="fa-solid fa-circle-info"></i>
        <span>ما هو الـ MPIS</span>
      </a>
      <a href="{prefix}Ar_admin_inst/Ar_admin_inst.htm" class="nav-btn">
        <i class="fa-solid fa-sliders"></i>
        <span>التعليمات الإدارية</span>
      </a>
      <a href="{prefix}Ar_draf_docs/Ar_draf_doc.htm" class="nav-btn">
        <i class="fa-solid fa-file-signature"></i>
        <span>مسودة المستندات</span>
      </a>
      <a href="{prefix}Ar_Coordinators/Ar_MPIS_Coord_main%20Page.htm" class="nav-btn">
        <i class="fa-solid fa-users-gear"></i>
        <span>المنسقون</span>
      </a>
    </nav>'''

            if '<nav class="main-nav">' in content:
                content = re.sub(r'<nav class="main-nav">.*?</nav>', new_nav, content, flags=re.IGNORECASE | re.DOTALL)
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                updated_files += 1
                print(f'Updated nav in {os.path.relpath(filepath, arabic_web_dir)}')

print(f'Total files fixed: {updated_files}')
