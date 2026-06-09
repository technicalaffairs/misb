import json
import sys

# Reconfigure stdout to print UTF-8 characters safely in terminal logs
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

json_path = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\scratch\ad_ss_docs_metadata.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total documents loaded: {len(data)}")
for idx, m in enumerate(sorted(data, key=lambda x: x["doc_id"])):
    print(f"{idx:2d} | ID: {m['doc_id']:12s} | Date: {m['date']:15s} | Title: {m['title'][:35]:35s} | Proc: {m['procedure'][:30]}")
