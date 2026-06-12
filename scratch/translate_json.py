import json
import os
import time
from deep_translator import GoogleTranslator

cwd = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\scratch'
input_file = os.path.join(cwd, 'extracted_all.json')
output_file = os.path.join(cwd, 'translated_all_mapping.json')

with open(input_file, 'r', encoding='utf-8') as f:
    strings = json.load(f)

mapping = {}
if os.path.exists(output_file):
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
    except:
        pass

translator = GoogleTranslator(source='en', target='ar')

to_translate = [s for s in strings if s not in mapping]
print(f"Remaining to translate: {len(to_translate)}")

batch_size = 20
for i in range(0, len(to_translate), batch_size):
    batch = to_translate[i:i+batch_size]
    try:
        translated_batch = translator.translate_batch(batch)
        for original, translated in zip(batch, translated_batch):
            mapping[original] = translated
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=4)
        print(f"Translated batch {i//batch_size + 1}")
    except Exception as e:
        print(f"Batch failed: {e}. Translating individually...")
        for s in batch:
            try:
                mapping[s] = translator.translate(s)
            except Exception as ex:
                mapping[s] = s
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=4)
            
    time.sleep(2)

print("Translation completed.")
