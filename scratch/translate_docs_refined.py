"""
translate_docs_refined.py
=========================
Professional Electrical Engineering Document Translator
Author: Antigravity AI for MPIS Technical Procedures Project
Date: 2026-06-10

This script translates English electrical testing procedure HTML documents
into Arabic using:
 - A custom Electrical Engineering terminology dictionary (applied BEFORE
   sending to Google Translate to ensure consistent, standard Arabic terms)
 - Block-level translation (full <p> and <td> text is assembled as a unit
   before translation, preventing disjointed sentence fragments)
 - Formula & Symbol protection (R60/R15, H1-H2, X1-X0, etc. are preserved)
 - Clean HTML output (avoids MS FrontPage "tag soup")
"""

import os
import re
import time
from bs4 import BeautifulSoup, NavigableString, Tag
from deep_translator import GoogleTranslator

# ===========================================================================
# PATHS
# ===========================================================================
ENG_DIR = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\appr_docs\ad_subst\ad_sub_tp"
AR_DIR  = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\ad_ss_docs\new_translated"

# ===========================================================================
# ELECTRICAL ENGINEERING TERMINOLOGY DICTIONARY
# Applied as direct string replacement BEFORE Google Translate
# Keys must be in Title/Sentence case to match rendered HTML text
# ===========================================================================
ENG_TERM_DICT = {
    # Document headers
    "Substations":                          "محطات المحولات",
    "Technical Procedure":                  "إجراء فني",
    "APPROVED":                             "معتمد",
    "Testing Procedure(s)":                 "إجراء (إجراءات) الاختبار",
    "Testing Procedures":                   "إجراءات الاختبار",
    "Document No:":                         "رقم الوثيقة:",
    "Issued to:":                           "صادر إلى:",
    "Status:":                              "الموقف:",
    "Procedure:":                           "الإجراء:",
    "Approved Date:":                       "تاريخ الاعتماد:",
    "Date to be Reviewed:":                 "تاريخ المراجعة التالية:",
    "Networks":                             "الشبكات",
    "Equipment":                            "المعدة",
    "Introduction":                         "مقدمة",
    "Safety Precautions":                   "احتياطات السلامة والأمان",
    "Tools and Equipment":                  "الأجهزة والعدد المستخدمة",
    "Work to be Carried Out":               "الإجراءات والخطوات المطلوب تنفيذها",
    "Location:":                            "الموقع:",
    "Equipment code:":                      "كود المعدة:",
    "Checked by:":                          "راجع بمعرفة:",
    "Date:":                                "التاريخ:",
    "Signature:":                           "التوقيع:",
    "Test Sheet":                           "جدول القياسات والنتائج",

    # Transformer Types
    "Power Transformer":                    "محول القدرة الكهربائية",
    "Power Transformers":                   "محولات القدرة الكهربائية",
    "Two Winding Transformer":              "محول ثنائي الملفات",
    "Two winding transformers":             "محولات ثنائية الملفات",
    "Three Winding Transformer":            "محول ثلاثي الملفات",
    "Three winding power transformers":     "محولات القدرة ثلاثية الملفات",
    "Three winding power transformer":      "محولات القدرة ثلاثية الملفات",
    "Two Winding":                          "ثنائي الملفات",
    "Three Winding":                        "ثلاثي الملفات",
    "type CB 100 TEOF":                     "طراز CB 100 TEOF",
    "type CB100-TEOF":                      "طراز CB100-TEOF",
    "type BM11 D":                          "طراز BM11 D",
    "type DRX 2000":                        "طراز DRX 2000",

    # Test Types
    "Turns Ratio Test":                     "اختبار نسبة التحويل",
    "Turns Ratio":                          "نسبة التحويل",
    "Ratio Test Results (for Two Winding Transformer)":
                                            "نتائج اختبار نسبة التحويل (محول ثنائي الملفات)",
    "Ratio Test Results (for Three Winding Transformer)":
                                            "نتائج اختبار نسبة التحويل (محول ثلاثي الملفات)",
    "3B-Turns Ratio Test For Two winding transformer":
                                            "اختبار نسبة التحويل لمحولات ثنائية الملفات",

    "Insulation Resistance":                "مقاومة العزل",
    "DC Winding Resistance":                "مقاومة الملفات بالتيار المستمر",
    "Winding Resistance Test":              "اختبار مقاومة الملفات بالتيار المستمر",
    "DC Resistance":                        "المقاومة بالتيار المستمر",
    "Megger test":                          "اختبار مقاومة العزل (الميجر)",
    "Megger Test":                          "اختبار مقاومة العزل (الميجر)",
    "Megger Tests":                         "اختبارات مقاومة العزل (الميجر)",
    "Megger test (5000V)":                  "اختبار الميجر بجهد 5000 فولت",
    "5000V Megger Tests":                   "اختبارات مقاومة العزل بجهد 5000 فولت",
    "Two Winding Transformer Resistance Test Report":
                                            "تقرير اختبار مقاومة العزل لمحولات ثنائية الملفات",
    "Three Winding Transformer Resistance Test Report":
                                            "تقرير اختبار مقاومة العزل لمحولات ثلاثية الملفات",
    "5000V Megger Tests":                   "اختبارات مقاومة العزل بجهد 5000 فولت",
    "High Voltage Tan δ testing (Results corrected to be at 20 °C":
                                            "اختبار تان دلتا للجهد العالي (النتائج مصححة عند 20 درجة مئوية)",
    "High Voltage Tan δ testing (Results corrected to be at 20":
                                            "اختبار تان دلتا للجهد العالي (النتائج مصححة عند 20",
    "Insulation Capacitance and Tan δ Dissipation Factor for Two Winding Transformer type CB 100 TEOF":
                                            "قياس سعة العزل وعامل الفقد (تان دلتا) لمحولات ثنائية الملفات طراز CB 100 TEOF",
    "Insulation Capacitance and Tan":       "سعة العزل وعامل الفقد",

    # Electrical Parameters
    "HV":           "الجهد العالي",
    "LV":           "الجهد المنخفض",
    "HV side":      "جانب الجهد العالي",
    "LV side":      "جانب الجهد المنخفض",
    "HV to LV + E": "الجهد العالي إلى (الجهد المنخفض + الأرضي)",
    "LV to HV + E": "الجهد المنخفض إلى (الجهد العالي + الأرضي)",
    "HV to LV +E":  "الجهد العالي إلى (الجهد المنخفض + الأرضي)",
    "LV to HV +E":  "الجهد المنخفض إلى (الجهد العالي + الأرضي)",
    "HV to LV":     "الجهد العالي إلى الجهد المنخفض",
    "LV to HV":     "الجهد المنخفض إلى الجهد العالي",
    "T to (H+L+E)": "الملف الثالث إلى (الجهد العالي + الجهد المنخفض + الأرضي)",
    "Resistance at 15 sec":  "مقاومة العزل بعد 15 ثانية",
    "Resistance at 60 sec":  "مقاومة العزل بعد 60 ثانية",
    "Insulation tested":     "العزل المختبر",
    "Tap Position":          "وضع مغير التفريعات (التاب)",
    "Calculated":            "القيمة المحسوبة",
    "Phase A":               "الفازة R (أ)",
    "Phase B":               "الفازة S (ب)",
    "Phase C":               "الفازة T (ج)",
    "Notes":                 "ملاحظات",

    "Tan δ %":       "عامل الفقد (تان دلتا %)",
    "Pfd Cap.":      "السعة (pF)",

    # Connections
    "S.C.":              "مقصّر",
    "short circuit":     "قصر (دائرة مقصورة)",
    "Short Circuit":     "قصر (دائرة مقصورة)",
    "Star connection":   "التوصيل النجمي",
    "Delta connection":  "التوصيل المثلثي (الدلتا)",
    "Neutral point":     "نقطة التعادل",
    "Neutral bushing":   "عازل التعادل (النيوترال)",
    "earth point":       "نقطة الأرضي",
    "Earth":             "الأرضي",
    "earth":             "الأرضي",

    # Components
    "Bushing":      "عازل الاختراق (البوشينج)",
    "Bushings":     "عوازل الاختراق (البوشينج)",
    "bushing":      "عازل الاختراق (البوشينج)",
    "bushings":     "عوازل الاختراق (البوشينج)",
    "HV Bushing":   "عازل الجهد العالي",
    "LV Bushing":   "عازل الجهد المنخفض",
    "HV bushing":   "عازل الجهد العالي",
    "LV bushing":   "عازل الجهد المنخفض",
    "Tap":          "التفرّع (التاب)",
    "Tap Changer":  "مغير التفريعات (Tap Changer)",
    "tap":          "التفرّع (التاب)",
    "Potential leads":   "أطراف قياس الجهد",
    "Current leads":     "أطراف قياس التيار",
    "Tertiary":          "الملف الثالث (الترشيري)",
    "tertiary":          "الملف الثالث (الترشيري)",

    # Instruments and connections
    "megger":       "الميجر",
    "Megger":       "الميجر",
    "+ ve":         "الطرف الموجب (+ve)",
    "- ve":         "الطرف السالب (-ve)",
    "+ve":          "الطرف الموجب (+ve)",
    "-ve":          "الطرف السالب (-ve)",
    "probe":        "طرف القياس",
    "Polarization index": "معامل الاستقطاب",
    "polarization index": "معامل الاستقطاب",

    # Safety
    "Isolate the transformer":   "فصل وعزل المحول",
    "out of service":            "خارج الخدمة",
    "earthed":                   "ومع إبقائه مؤرضاً",
    "Safety fence":              "تسييج منطقة العمل",
    "caution marks":             "شريط تحذيري",
    "A word order permit":       "يجب إصدار تصريح وأمر شغل",
    "work order permit":         "تصريح وأمر شغل",
    "Word Order Permit":         "تصريح وأمر شغل",
    "safety category":           "فئة السلامة المناسبة",
    "Bridles":                   "وصلات الكابلات المرنة",
    "bridles":                   "وصلات الكابلات المرنة",
    "clamps":                    "مشابك التوصيل",
    "Clamps":                    "مشابك التوصيل",
    "qualified test staff":      "طاقم الاختبار المؤهل",
    "qualified test grup staff": "طاقم الاختبار المؤهل",

    # Actions
    "Turn on megger":       "شغّل الميجر",
    "Turn off megger":      "أوقف تشغيل الميجر",
    "Record the result":    "سجّل النتيجة",
    "Record the results":   "سجّل القراءات في جدول القياسات المرفق",
    "Repeat":               "كرّر",
    "Remove any earth":     "افصل أي تأريض مؤقت",
    "Connect":              "وصّل",
    "Disconnect":           "افصل",
    "Apply the":            "وصّل",
    "Keep":                 "أبقِ",

    # Test modes (Tan Delta)
    "GST L - Ground":   "وضع القياس: GST-L (تأريض مع حماية المنخفض)",
    "GST l - Guard":    "وضع القياس: GST-L (حماية)",
    "GST H-guard":      "وضع القياس: GST-H (حماية العالي)",
    "GSTL- ground":     "وضع القياس: GSTL (تأريض)",
    "UST":              "وضع القياس: UST (غير مؤرض)",
    "UST-ground":       "وضع القياس: UST (غير مؤرض)",
    "Test mode":        "وضع القياس",

    # Results Table Labels
    "TWO WINDING TRANSFORMER TESts":      "نتائج اختبارات محولات ثنائية الملفات",
    "Ratio Test Results":                  "نتائج اختبار نسبة التحويل",
}

# Patterns that should NEVER be translated (formulas, codes, terminals, etc.)
NEVER_TRANSLATE_PATTERNS = [
    r'\bR\d{2}/R\d{2}\b',           # R60/R15
    r'\bR\d{2}\b',                   # R15, R60
    r'\bH[0-9]+\b',                  # H1, H2, H3, H0
    r'\bX[0-9]+\b',                  # X1, X2, X3, X0
    r'\bY[0-9]+\b',                  # Y1, Y2
    r'\b[HX][0-9]+-[HX][0-9]+\b',   # H1-H2, X1-X0
    r'\bC[HL]+\b',                   # CH, CL, CHL, CLH
    r'\bCT\b', r'\bCHT\b', r'\bCLT\b',
    r'\bT-\d{3}-r\d+[a-z]?\b',      # Document codes T-022-r0
    r'\bCB\s*\d+\s*TEOF\b',         # CB 100 TEOF
    r'\bBM\d+\s*D\b',               # BM11 D
    r'\bDRX\s*\d+\b',               # DRX 2000
    r'\b5000\s*V\b', r'\b5\s*kV\b', # voltage values
    r'\bAVO\b', r'\bMR\b',
    r'\bUSA\b', r'\bTX\b', r'\bOntario\b',
    r'\b\d{2,4}\b',                  # Standalone numbers
    r'[A-Z]\.[A-Z]\.',               # A.C., D.C.
    r'\b\d+ (?:Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Jan) \d{4}\b',  # Dates
    r'\b\d+ (?:فبراير|يناير|مارس|أبريل|مايو|يونيو|يوليو|أغسطس|سبتمبر|أكتوبر|نوفمبر|ديسمبر) \d{4}\b',  # Arabic dates
]

# ===========================================================================
# HELPERS
# ===========================================================================

translator = GoogleTranslator(source='en', target='ar')
translation_cache = {}

def protect_formulas(text):
    """
    Replace formulas/codes with placeholders before translation
    to prevent them from being altered.
    """
    placeholders = {}
    counter = [0]
    
    def replacer(m):
        key = f"__PLACEHOLDER_{counter[0]}__"
        placeholders[key] = m.group(0)
        counter[0] += 1
        return key
    
    protected = text
    for pat in NEVER_TRANSLATE_PATTERNS:
        protected = re.sub(pat, replacer, protected)
    
    return protected, placeholders

def restore_placeholders(text, placeholders):
    """Restore original formulas/codes from placeholders."""
    for key, val in placeholders.items():
        text = text.replace(key, val)
    return text

def apply_term_dict(text):
    """
    Apply the engineering terminology dictionary with longest-first matching
    so that longer phrases take priority over shorter ones.
    """
    # Sort keys by length descending so longer phrases are replaced first
    for key in sorted(ENG_TERM_DICT.keys(), key=len, reverse=True):
        # Case-insensitive search but preserve structure
        if key in text:
            text = text.replace(key, ENG_TERM_DICT[key])
        elif key.lower() in text.lower():
            # Case-insensitive replace
            idx = text.lower().find(key.lower())
            text = text[:idx] + ENG_TERM_DICT[key] + text[idx+len(key):]
    return text

def translate_block(text):
    """
    Translate a complete block of text (paragraph or cell content).
    1. Apply term dictionary replacements.
    2. Protect formulas with placeholders.
    3. If the text now contains Arabic-dominant content, skip translation.
    4. Otherwise, call Google Translate.
    5. Restore placeholders.
    """
    text = text.strip()
    if not text:
        return text
    
    # Skip pure whitespace, numbers, or codes
    if re.match(r'^[\d\s\W]+$', text):
        return text
    
    # Apply terminology dictionary first
    text = apply_term_dict(text)
    
    # Check if text is already predominantly Arabic after term replacement
    arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))
    total_chars = len(re.findall(r'[a-zA-Z\u0600-\u06FF]', text))
    if total_chars > 0 and arabic_chars / total_chars > 0.5:
        # Already mostly Arabic, just restore placeholders and return
        return text
    
    # Protect formulas
    protected, placeholders = protect_formulas(text)
    
    # If after protection nothing translatable remains, return as-is
    translatable = re.sub(r'__PLACEHOLDER_\d+__', '', protected).strip()
    if not translatable or re.match(r'^[\s\W]+$', translatable):
        return restore_placeholders(protected, placeholders)
    
    # Check cache
    if protected in translation_cache:
        result = translation_cache[protected]
        return restore_placeholders(result, placeholders)
    
    try:
        translated = translator.translate(protected)
        time.sleep(0.3)
        if translated:
            translation_cache[protected] = translated
            return restore_placeholders(translated, placeholders)
        return restore_placeholders(protected, placeholders)
    except Exception as e:
        print(f"  [WARN] Translation error: {e}")
        return restore_placeholders(protected, placeholders)

def get_block_text(element):
    """Get all visible text from a block element, collapsing whitespace."""
    return ' '.join(element.get_text(' ').split())

def replace_block_content(element, translated_text):
    """
    Replace all children of a block element with a single translated text node.
    Preserves inline sub/sup tags (for formulas like H1, X0) since they are
    structural, not semantic content.
    """
    # Find all sub/sup children and their texts
    special_tags = []
    for child in element.find_all(['sub', 'sup']):
        special_tags.append((child.get_text(), child.name))
    
    # Clear current content
    for child in list(element.children):
        child.extract()
    
    # Insert the translated text (rendered as a NavigableString)
    element.append(NavigableString(translated_text))

# ===========================================================================
# MAIN TRANSLATION LOGIC
# ===========================================================================

def translate_html_document(soup):
    """
    Translate block-level elements (p, td, li, h1-h6) as complete units.
    Skip elements that are part of scripts, styles, or code blocks.
    """
    BLOCK_TAGS = ['p', 'td', 'th', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote']
    SKIP_PARENTS = ['script', 'style', 'code', 'pre']
    
    # Collect block elements
    block_elements = []
    for tag_name in BLOCK_TAGS:
        block_elements.extend(soup.find_all(tag_name))
    
    # Remove nested blocks (e.g. <li> inside <li>, <p> inside <td>)
    # We translate from innermost non-nested blocks outward
    def is_nested_block(el):
        for parent in el.parents:
            if parent.name in BLOCK_TAGS and parent != el:
                return True
        return False
    
    # Get leaf block elements (no block children)
    leaf_blocks = []
    for el in block_elements:
        has_block_child = any(child.name in BLOCK_TAGS for child in el.children if isinstance(child, Tag))
        if not has_block_child:
            # Check parent is not in skip list
            parent_names = [p.name for p in el.parents]
            if not any(p in SKIP_PARENTS for p in parent_names):
                leaf_blocks.append(el)
    
    print(f"  Found {len(leaf_blocks)} text blocks to translate...")
    
    for i, el in enumerate(leaf_blocks):
        original_text = get_block_text(el)
        if not original_text.strip():
            continue
        
        translated = translate_block(original_text)
        
        if translated and translated != original_text:
            # Clear the element and set new content
            for child in list(el.children):
                child.extract()
            el.append(NavigableString(translated))
        
        # Progress indicator every 10 blocks
        if (i + 1) % 10 == 0:
            print(f"    ... {i+1}/{len(leaf_blocks)} blocks translated")
    
    return soup

def fix_paths(soup, depth_diff=2):
    """
    Adjust relative paths from English source (depth 3 from root)
    to Arabic target (depth 5 from root).
    English:  ../../../style.css       (3 levels up)
    Arabic:   ../../../../../style.css  (5 levels up)
    """
    old_prefix_3 = "../../../"
    new_prefix_5 = "../../../../../"
    old_prefix_4 = "../../../../"
    
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href", "")
        if "style.css" in href:
            link["href"] = href.replace(old_prefix_3, new_prefix_5).replace(old_prefix_4, new_prefix_5)
    
    for body in soup.find_all("body"):
        bg = body.get("background", "")
        if "images/" in bg:
            body["background"] = bg.replace(old_prefix_3, new_prefix_5).replace(old_prefix_4, new_prefix_5)
    
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if "images/" in src or "graphics/" in src:
            # For images and graphics in the source, update path
            img["src"] = src.replace(old_prefix_3, new_prefix_5).replace(old_prefix_4, new_prefix_5)

def process_file(filename):
    eng_path = os.path.join(ENG_DIR, filename)
    # Determine output filename
    ar_filename = (filename
                   .replace("-r0.htm", "-r0a.htm")
                   .replace("-r1.htm", "-r1a.htm")
                   .replace("-r0.html", "-r0a.htm")
                   .replace("-r1.html", "-r1a.htm"))
    ar_path = os.path.join(AR_DIR, ar_filename)
    
    print(f"\n{'='*60}")
    print(f"Processing: {filename}  ->  {ar_filename}")
    print(f"{'='*60}")
    
    with open(eng_path, "r", encoding="windows-1252", errors="ignore") as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Set Arabic document attributes
    html_tag = soup.find("html")
    if html_tag:
        html_tag["dir"] = "rtl"
        html_tag["lang"] = "ar"
    
    # 2. Update/add charset meta tag for UTF-8 support
    meta_charset = soup.find("meta", attrs={"http-equiv": "Content-Type"})
    if meta_charset:
        meta_charset["content"] = "text/html; charset=utf-8"
    else:
        head = soup.find("head")
        if head:
            new_meta = soup.new_tag("meta")
            new_meta["http-equiv"] = "Content-Type"
            new_meta["content"] = "text/html; charset=utf-8"
            head.insert(0, new_meta)
    
    # 3. Update title
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        doc_code = filename.replace(".htm", "").replace(".html", "")
        ar_doc_code = doc_code.replace("-r0", "-r0a").replace("-r1", "-r1a")
        title_tag.string = f"{ar_doc_code} APPROVED معتمد (APPROVED)"
    
    # 4. Fix relative paths
    fix_paths(soup)
    
    # 5. Translate content
    translate_html_document(soup)
    
    # 6. Save with UTF-8 encoding
    os.makedirs(AR_DIR, exist_ok=True)
    with open(ar_path, "w", encoding="utf-8", errors="ignore") as out_f:
        # Write a proper HTML5-style header comment
        out_f.write(str(soup))
    
    print(f"\n  [OK] Saved: {ar_path}")

# ===========================================================================
# ENTRY POINT
# ===========================================================================
FILES_TO_TRANSLATE = [
    "T-022-r0.htm",
    "T-024-r0.htm",
    "T-025-r0.htm",
    "T-026-r0.htm",
    "T-027-r0.htm",
]

if __name__ == "__main__":
    import sys
    
    # Allow running a single file: python translate_docs_refined.py T-022-r0.htm
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = FILES_TO_TRANSLATE
    
    for f in files:
        process_file(f)
    
    print(f"\n\n{'='*60}")
    print("Translation pipeline complete!")
    print(f"Output directory: {AR_DIR}")
    print(f"{'='*60}")
