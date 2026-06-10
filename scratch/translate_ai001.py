import os, re, urllib.parse

src_path = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\gen_docs\app_gen\MDEPC\Mechanical\AI-001-r0.htm'
dest_path = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\gen_docs\app_gen\MDEPC\Mechanical\AI-001-r0a.htm'
index_path = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_gen_docs\Ar_Gas Turbines_docs Page.htm'
base_dir = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb'
arabic_web_dir = os.path.join(base_dir, 'arabic_web')
ar_index_path = os.path.join(arabic_web_dir, 'Ar_Index.htm')

with open(ar_index_path, 'r', encoding='utf-8') as f:
    index_html = f.read()

modern_header_base = re.search(r'<div class="top-bar">.*?</nav>', index_html, re.DOTALL).group(0)
style_match = re.search(r'<style>.*?</style>', index_html, re.DOTALL)
modern_style = style_match.group(0)

def adjust_links(html_chunk, current_file_path):
    def replacer(match):
        attr = match.group(1)
        url = match.group(2)
        if url.startswith('http') or url.startswith('mailto') or url.startswith('#') or url == '': return match.group(0)
        abs_target = os.path.normpath(os.path.join(arabic_web_dir, urllib.parse.unquote(url).replace('/', '\\')))
        rel_target = os.path.relpath(abs_target, os.path.dirname(current_file_path)).replace('\\', '/')
        return f'{attr}="{urllib.parse.quote(rel_target)}"'
    return re.sub(r'(href|src)=[\'\"]([^\'\"]+)[\'\"]', replacer, html_chunk, flags=re.IGNORECASE)

with open(src_path, 'r', encoding='windows-1252', errors='ignore') as f:
    text = f.read()

# Replace texts
replacements = {
    "Power Stations": "محطات الإنتاج",
    "Technical Procedure": "إجراء فني",
    "Equipment:": "المعدة:",
    "Air Intake<br>\n      Kafeer Raco -\n      England": "مأخذ الهواء<br>كافير راكو - إنجلترا",
    "Air Intake Kafeer Raco - England": "مأخذ الهواء كافير راكو - إنجلترا",
    "Document No:": "رقم المستند:",
    "Issued to:": "إصدار إلى:",
    "Nubaria PS": "محطة النوبارية",
    "Status:": "الحالة:",
    "APPROVED": "معتمد",
    "Procedure:": "الإجراء:",
    "Equipment Inspection (I1-W1)\n    depend on &#916;P": "فحص المعدة (I1-W1)\n    بناءً على فرق الضغط &#916;P",
    "Approved Date:": "تاريخ الاعتماد:",
    "19 Nov 2007": "19 نوفمبر 2007",
    "Date to be Reviewed:": "تاريخ المراجعة:",
    "Nov 2012": "نوفمبر 2012",
    "Introduction": "مقدمة",
    "This document outlines the equipment inspection I1, which must be performed on \na weekly bases bases as indicated by W1 in the title block. For air intake, cleaning air \nadded to fuel and burnt in combustion chamber and hot gases are expanded in \nturbine.": "يوضح هذا المستند فحص المعدة I1، والذي يجب إجراؤه بشكل أسبوعي كما هو موضح بـ W1 في صندوق العنوان. بالنسبة لمأخذ الهواء، يتم تنظيف الهواء المضاف للوقود والمحترق في غرفة الاحتراق وتتمدد الغازات الساخنة في التوربينة.",
    "Technical\nSpecification": "المواصفات الفنية",
    "Quantity": "الكمية",
    "Type": "النوع",
    "1<sup><u>st</u></sup>\n    <span style=\"text-transform: capitalize\">Stage</span> coaleser\n    <span style=\"text-transform: capitalize\">filter</span> (A1 Mg3_384 pcs 610X610X50 &amp; 224 pcs 610X305X50)": "مرشح تجميع المرحلة الأولى (A1 Mg3_384 قطعة 610X610X50 و 224 قطعة 610X305X50)",
    "2<sup><u>nd</u></sup>\n    <span style=\"text-transform: capitalize\">stage</span> \n    768 pcs <span style=\"text-transform: capitalize\">pulse</span>\n    <span style=\"text-transform: capitalize\">filter</span> ( \n    <span style=\"text-transform: capitalize\">conical</span> CO-2612 &amp; cylindrical CY-2612)": "المرحلة الثانية 768 قطعة مرشح نبضي (مخروطي CO-2612 وأسطواني CY-2612)",
    "3<sup><u>rd</u></sup>\n    <span style=\"text-transform: capitalize\">stage</span> \n    473 pcs <span style=\"text-transform: capitalize\">fine filte</span>r (CAM GT - 242412-85_592X592X290)": "المرحلة الثالثة 473 قطعة مرشح دقيق (CAM GT - 242412-85_592X592X290)",
    "Auxiliaries": "المساعدات",
    "Two \n    <span style=\"text-transform: capitalize\">pulse \n    air compressors</span> (<span style=\"text-transform: capitalize\">atlas</span> copco GA30)": "ضاغطا هواء نبضي (أطلس كوبكو GA30)",
    "192 \n    double<span style=\"text-transform: capitalize\"> </span>diaphragm<span style=\"text-transform: capitalize\">\n    </span>valves VEP 416 - 24DC 2'": "192 صمام غشاء مزدوج VEP 416 - 24DC 2'",
    "Alarm": "إنذار",
    "12 mm bar": "12 مم بار",
    "Trip": "فصل",
    "16 mm bar": "16 مم بار",
    "The first draft initiated and tested by eng. Richard Kromer, revised by \neng. Fawzi Kamar, reviewed by eng. Fawzy Qamar, accepted by eng. Omran Abd El-Hamed Shoaib general director, approved by eng. Mohamed Naguib: \nMDEPC quality \ncontrol head sector &amp; eng. Ahmed Abd El-Maged Sawan: Head sector of Nubaria CCPS \n750MW, and certified by eng. Samir Abd El-Gelil: MDEPC inspection and quality control general \ndirector &amp; MPIS coordinator.": "تم إعداد المسودة الأولى واختبارها بواسطة م. ريتشارد كرومر، وروجعت بواسطة م. فوزي قمر، واعتمدت من م. عمران عبد الحميد شعيب المدير العام، وتم التصديق عليها من م. محمد نجيب رئيس قطاع مراقبة الجودة وم. أحمد عبد المجيد صوان رئيس قطاع محطة النوبارية للدورة المركبة 750 ميجاوات، ومعتمدة من م. سمير عبد الجليل مدير عام التفتيش ومراقبة الجودة.",
    "Safety Precautions": "احتياطات السلامة",
    "A work permit ": "يجب إصدار تصريح عمل.",
    "must be issued.": "",
    "The qualified maintenance staff should carry the \n  suitable ID safety category.": "يجب أن يحمل طاقم الصيانة المؤهل فئة السلامة المناسبة.",
    "Safety fence with \n  caution marks surrounding the work area is required.": "مطلوب سياج أمان مع علامات تحذير تحيط بمنطقة العمل.",
    "Wear safety and healthy equipment as safety \n  helmet, shoes, breathing-mask, safety glasses ... etc.": "ارتداء معدات السلامة والصحة المهنية مثل خوذة السلامة، والأحذية، وقناع التنفس، ونظارات السلامة ... إلخ.",
    "Close the main pulsing valve.": "أغلق الصمام النبضي الرئيسي.",
    "Tools and Equipment ": "العدد والأدوات",
    "Suitable tool set.": "طقم عِدد مناسب.",
    "Safety and healthy tools": "أدوات السلامة والصحة المهنية",
    "Vacuum cleaner or air blower.": "مكنسة كهربائية أو منفاخ هواء.",
    "Work to be Carried Out": "الأعمال المطلوب تنفيذها",
    "Monitoring of DP across each filter stage.": "مراقبة فرق الضغط (DP) عبر كل مرحلة من مراحل المرشح.",
    "Check leakage of double diaphragm valves.": "فحص تسرب صمامات الغشاء المزدوج.",
    "Inspect the weather entry screen for blockage of \n      debris.": "فحص شبكة دخول الهواء بحثًا عن أي انسداد بالشوائب.",
    "Visible check of clean compressor inlet via MBL \n      inspection windows.": "فحص بصري لنظافة مدخل الضاغط عبر نوافذ فحص MBL.",
    "Check cleanness": "فحص النظافة.",
    "Test auto drain function for compressor and dryers.": "اختبار وظيفة التصفية الآلية للضاغط والمجففات.",
    "Check oil level in oil collector": "فحص مستوى الزيت في مجمع الزيت.",
    "Filter check and connections check for air dryer.": "فحص المرشح والوصلات الخاصة بمجفف الهواء.",
    "Leakage check on hoses, hose connection and container \n      for oil water separator": "فحص التسرب في الخراطيم ووصلات الخراطيم ووعاء فاصل الزيت عن الماء.",
    "Check condensate level at sight glass for DD/PD filters.": "فحص مستوى المتكثف عند زجاجة الرؤية لمرشحات DD/PD.",
    "Test auto drain function for DD/PD filters.": "اختبار وظيفة التصفية الآلية لمرشحات DD/PD.",
    "Test auto drain function for air receiver.": "اختبار وظيفة التصفية الآلية لمستقبل الهواء.",
    "Location:": "الموقع:",
    "Air \n      Intake": "مأخذ الهواء",
    "Designation:": "التعيين:",
    "Tested by:": "تم الاختبار بواسطة:",
    "Signature:": "التوقيع:",
    "Test Date:": "تاريخ الاختبار:",
}

for eng, ar in replacements.items():
    text = text.replace(eng, ar)
    
text = text.replace('AI-001-r0', 'AI-001-r0a')

# Add Modern Header
body_split = re.split(r'(<body[^>]*>)', text, maxsplit=1, flags=re.IGNORECASE)
pre_body = body_split[0]
body_tag = body_split[1]
post_body = body_split[2]

if 'dir=' not in body_tag.lower():
    body_tag = body_tag.replace('>', ' dir="rtl">')

modern_header = adjust_links(modern_header_base, dest_path)
new_post_body = f'\n<div class="app-container">\n{modern_header}\n</div>\n{post_body}'

content = pre_body + body_tag + new_post_body

fontawesome_link = r'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'
content = re.sub(r'</head>', f'{fontawesome_link}\n{modern_style}\n</head>', content, flags=re.IGNORECASE)

with open(dest_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Update Index
with open(index_path, 'r', encoding='utf-8') as f:
    idx_text = f.read()

idx_text = idx_text.replace('AI-001-r0.htm', 'AI-001-r0a.htm')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(idx_text)

print("Translation and injection completed.")
