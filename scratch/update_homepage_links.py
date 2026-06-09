import re

index_file = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_index.HTM"

with open(index_file, "r", encoding="utf-8") as f:
    content = f.read()

# Define the replacements mapping
replacements = {
    r'../appr_docs/ad_subst/ad_CBs.htm': 'Ar_appr_docs/Ar_ad_subst/Ar_ad_CBs.htm',
    r'../appr_docs/ad_subst/ad_Trafo.htm': 'Ar_appr_docs/Ar_ad_subst/Ar_ad_Trafo.htm',
    r'../appr_docs/ad_subst/ad_tap%20changers.htm': 'Ar_appr_docs/Ar_ad_subst/Ar_ad_tap_changers.htm',
    r'../appr_docs/ad_subst/ad_DS,%20ES.htm': 'Ar_appr_docs/Ar_ad_subst/Ar_ad_DS_ES.htm',
    r'../appr_docs/ad_subst/ad_CT+PT+LA.htm': 'Ar_appr_docs/Ar_ad_subst/Ar_ad_CT_PT_LA.htm',
    r'../appr_docs/ad_subst/ad_Batteries.htm': 'Ar_appr_docs/Ar_ad_subst/Ar_ad_Batteries.htm',
    r'../appr_docs/ad_subst/Distrib_Board.htm': 'Ar_appr_docs/Ar_ad_subst/Ar_Distrib_Board.htm',
    r'../appr_docs/ad_subst/ad_condensers.htm': 'Ar_appr_docs/Ar_ad_subst/Ar_ad_condensers.htm',
    r'../appr_docs/ad_subst/ad_Busbars.htm': 'Ar_appr_docs/Ar_ad_subst/Ar_ad_Busbars.htm',
    r'../appr_docs/ad_subst/ad_compressors.htm': 'Ar_appr_docs/Ar_ad_subst/Ar_ad_compressors.htm',
    r'../appr_docs/ad_subst/ad_TB-SS+PS.htm': 'Ar_appr_docs/Ar_ad_subst/Ar_ad_TB-SS+PS.htm',
    r'../appr_docs/ad_subst/ad_TD-SS+PS.htm': 'Ar_appr_docs/Ar_ad_subst/Ar_ad_TD-SS+PS.htm'
}

count = 0
for search, replace in replacements.items():
    if search in content:
        content = content.replace(search, replace)
        print(f"Replaced: {search} -> {replace}")
        count += 1
    else:
        # Also check for urlencoded versions if any
        search_escaped = search.replace(" ", "%20")
        if search_escaped in content:
            content = content.replace(search_escaped, replace)
            print(f"Replaced url-encoded: {search_escaped} -> {replace}")
            count += 1
        else:
            print(f"Not found: {search}")

with open(index_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated index page with {count} replaced links.")
