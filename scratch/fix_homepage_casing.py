import os

search_bytes = [b"Ar_index.HTM", b"Ar_index.htm", b"Ar_Index.HTM"]
target_bytes = b"Ar_Index.htm"

count = 0
for root, _, files in os.walk("."):
    if ".git" in root or "node_modules" in root:
        continue
    for f in files:
        if f.lower().endswith(('.htm', '.html')):
            path = os.path.join(root, f)
            try:
                with open(path, "rb") as file_obj:
                    data = file_obj.read()
                
                updated = False
                for s in search_bytes:
                    if s in data:
                        data = data.replace(s, target_bytes)
                        updated = True
                
                if updated:
                    with open(path, "wb") as file_obj:
                        file_obj.write(data)
                    print(f"Fixed homepage casing in: {path}")
                    count += 1
            except Exception as e:
                print(f"Error processing {path}: {e}")

print(f"Completed! Casing fixed in {count} files.")
