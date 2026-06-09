import os

path = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\ad_ss_docs"
files = os.listdir(path)
print(f"Total files in ad_ss_docs: {len(files)}")
for f in sorted(files):
    size = os.path.getsize(os.path.join(path, f))
    print(f" - {f} ({size} bytes)")
