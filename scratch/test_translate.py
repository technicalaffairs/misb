import sys
from deep_translator import GoogleTranslator

print("Testing deep-translator...")
try:
    translator = GoogleTranslator(source='en', target='ar')
    res = translator.translate("A work order must be issued")
    print("Result:", res)
except Exception as e:
    print("Error:", e, file=sys.stderr)
