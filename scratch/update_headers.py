import os
import re

# List of target files and their relative path to the EETC logo image
targets = [
    {
        "filepath": "arabic_web/Ar_about/Ar_about.htm",
        "logo_path": "../../images/eetc_logo.jpg"
    },
    {
        "filepath": "arabic_web/Ar_admin_inst/Ar_draf_doc.htm",
        "logo_path": "../../images/eetc_logo.jpg"
    },
    {
        "filepath": "arabic_web/Ar_appr_docs/Ar_ad_trans/Ar_ad_trans.htm",
        "logo_path": "../../../images/eetc_logo.jpg"
    },
    {
        "filepath": "arabic_web/Ar_draf_docs/Ar_draf_trans/Ar_draf_tl.htm",
        "logo_path": "../../../images/eetc_logo.jpg"
    },
    {
        "filepath": "arabic_web/Ar_index_old.htm",
        "logo_path": "../images/eetc_logo.jpg"
    }
]

def update_file(filepath, relative_logo_path):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='latin1') as f:
        content = f.read()

    # 1. Update logo if it exists
    # Find eehc_logo.gif with any relative path and replace with correct relative_logo_path
    logo_pattern = re.compile(r'src=["\'][^"\']*eehc_logo\.gif["\']', re.IGNORECASE)
    if logo_pattern.search(content):
        content = logo_pattern.sub(f'src="{relative_logo_path}"', content)
        print("  Updated logo image src successfully.")

    # 2. Add the Arabic text "منطقة كهرباء مصر الوسطى - مكتب الشئون الفنية"
    # HTML Entity Representation:
    # &#1605;&#1606;&#1591;&#1602;&#1577; &#1603;&#1607;&#1585;&#1576;&#1575;&#1569; &#1605;&#1589;&#1585; &#1575;&#1604;&#1608;&#1587;&#1591;&#1609; - &#1605;&#1603;&#1578;&#1576; &#1575;&#1604;&#1588;&#1574;&#1608;&#1606; &#1575;&#1604;&#1601;&#1606;&#1610;&#1577;
    new_text_entity = '&#1605;&#1606;&#1591;&#1602;&#1577; &#1603;&#1607;&#1585;&#1576;&#1575;&#1569; &#1605;&#1589;&#1585; &#1575;&#1604;&#1608;&#1587;&#1591;&#1609; - &#1605;&#1603;&#1578;&#1576; &#1575;&#1604;&#1588;&#1574;&#1608;&#1606; &#1575;&#1604;&#1601;&#1606;&#1610;&#1577;'
    
    # We find table cells (<td ...>...</td>) that contain the hierarchy marker entity '&#1575;&#1604;&#1593;&#1590;&#1608;' (العضو)
    td_pattern = re.compile(r'(<td\b[^>]*>)(.*?)(</td>)', re.IGNORECASE | re.DOTALL)
    
    def replace_td(match):
        start_tag = match.group(1)
        body = match.group(2)
        end_tag = match.group(3)
        
        if '&#1575;&#1604;&#1593;&#1590;&#1608;' in body:
            # Check if already added
            if new_text_entity in body:
                print("  Text already present in cell. Skipping text injection.")
                return match.group(0)
            
            # Find the closing </b> tag inside the cell and inject text before it
            bold_pattern = re.compile(r'(</b>|</B>)')
            injected = f'<br><font face="Tahoma" size="3">{new_text_entity}</font>'
            
            new_body, count = bold_pattern.subn(rf'{injected}\1', body)
            if count > 0:
                print(f"  Successfully injected text into header cell.")
                return f"{start_tag}{new_body}{end_tag}"
            
        return match.group(0)

    new_content = td_pattern.sub(replace_td, content)
    
    with open(filepath, 'w', encoding='latin1') as f:
        f.write(new_content)
    print("  Saved updates.")

if __name__ == "__main__":
    for target in targets:
        update_file(target["filepath"], target["logo_path"])
    print("Done!")
