import os
import re
import time
from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator

# Folders definition
eng_dir = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\appr_docs\ad_subst\ad_sub_tp"
ar_dir = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\ad_ss_docs"

translator = GoogleTranslator(source='en', target='ar')

# Regex to detect text that shouldn't be translated (like terminal names, numbers, or document codes)
CODE_PATTERNS = [
    r'^[H|X|Y]\d+-[H|X|Y]\d+$',
    r'^[H|X|Y]\d+$',
    r'^[T|CB|BB|B|Ch|FS|PT|CT|TC|TD|TB]-\d+-[r|R]\d+[a-z]?$',
    r'^\d+$',
    r'^[A-Z]$',
    r'^[R|S|T]$',
    r'^[H|L]V$',
    r'^D\.?C\.?$',
    r'^A\.?C\.?$',
    r'^Vacuum$',
    r'^MR$',
    r'^WRT100$',
    r'^Programa$',
    r'^TM\s*\d+$'
]

def should_skip(text):
    text = text.strip()
    if not text:
        return True
    # If it is just punctuation or spaces
    if re.match(r'^[^\w\s]+$', text):
        return True
    # Check if it matches any code patterns
    for p in CODE_PATTERNS:
        if re.match(p, text, re.IGNORECASE):
            return True
    return False

# Translation cache to avoid redundant network calls and preserve consistency
translation_cache = {}

def translate_text(text):
    text_stripped = text.strip()
    if should_skip(text_stripped):
        return text
        
    if text_stripped in translation_cache:
        return text.replace(text_stripped, translation_cache[text_stripped])
        
    try:
        translated = translator.translate(text_stripped)
        # Add to cache
        translation_cache[text_stripped] = translated
        # Introduce a tiny delay to respect rate limits
        time.sleep(0.3)
        # Preserve original spacing if any
        return text.replace(text_stripped, translated)
    except Exception as e:
        print(f"Error translating '{text_stripped}': {e}")
        return text

def translate_html_tree(node):
    # If it is a string element, translate it
    if isinstance(node, NavigableString):
        if node.parent.name not in ['script', 'style', 'title']:
            translated = translate_text(str(node))
            node.replace_with(translated)
        return
        
    # Recurse through children
    for child in list(node.children):
        translate_html_tree(child)

def process_file(filename):
    eng_path = os.path.join(eng_dir, filename)
    ar_filename = filename.replace("-r0.htm", "-r0a.htm").replace("-r1.htm", "-r1a.htm").replace("-r0.html", "-r0a.htm").replace("-r1.html", "-r1a.htm")
    ar_path = os.path.join(ar_dir, ar_filename)
    
    print(f"\nProcessing: {filename} -> {ar_filename}")
    
    with open(eng_path, "r", encoding="windows-1252", errors="ignore") as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Update document attributes for Arabic RTL rendering
    html_tag = soup.find("html")
    if html_tag:
        html_tag["dir"] = "rtl"
        html_tag["lang"] = "ar"
        
    # Set proper encoding meta tag (windows-1252 to match the repository encoding)
    meta_charset = soup.find("meta", attrs={"http-equiv": "Content-Type"})
    if meta_charset:
        meta_charset["content"] = "text/html; charset=windows-1252"
        
    # 2. Update relative paths from depth 3 to depth 4
    # E.g. style.css: ../../../style.css -> ../../../../style.css
    # E.g. images: ../../../images/... -> ../../../../images/...
    for link in soup.find_all("link", rel="stylesheet"):
        if "style.css" in link.get("href", ""):
            link["href"] = link["href"].replace("../../../style.css", "../../../../style.css")
            
    for body in soup.find_all("body"):
        if body.get("background"):
            body["background"] = body["background"].replace("../../../images/", "../../../../images/")
            
    for img in soup.find_all("img"):
        if img.get("src"):
            img["src"] = img["src"].replace("../../../images/", "../../../../images/")
            
    # Update title element
    title_tag = soup.find("title")
    if title_tag:
        title_tag.string = title_tag.string.replace("-r0", "-r0a").replace("-r1", "-r1a") + " APPROVED (AR)"

    # 3. Translate all HTML text nodes recursively
    translate_html_tree(soup)
    
    # 4. Save the translated HTML
    # We write it in windows-1252 to keep charset compatibility
    with open(ar_path, "w", encoding="windows-1252", errors="ignore") as out_f:
        out_f.write(str(soup))
        
    print(f"Generated Arabic page: {ar_filename}")

# List of files to translate
files_to_translate = [
    "T-022-r0.htm",
    "T-024-r0.htm",
    "T-025-r0.htm",
    "T-026-r0.htm",
    "T-027-r0.htm"
]

for f in files_to_translate:
    process_file(f)
    
print("\nPDF translation/HTML generation pipeline complete!")
