import os
import re

base_dir = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb"
css_abs_path = os.path.join(base_dir, "arabic_web", "chatbot.css")
js_abs_path = os.path.join(base_dir, "arabic_web", "chatbot.js")

def inject():
    print("جاري البحث عن ملفات HTML...")
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        # تجنب مجلدات معينة إذا لزم الأمر (مثل scratch, .git)
        if '.git' in root or 'scratch' in root:
            continue
        for file in files:
            if file.lower().endswith(('.htm', '.html')):
                html_files.append(os.path.join(root, file))
    
    print(f"تم العثور على {len(html_files)} ملف HTML. جاري التعديل...")
    success = 0
    skipped = 0
    errors = 0

    for file_path in html_files:
        try:
            # محاولة قراءة الملف بترميز مختلف
            encoding_used = 'utf-8'
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                encoding_used = 'cp1256'
                with open(file_path, 'r', encoding='cp1256') as f:
                    content = f.read()

            # التخطي إذا كان يحتوي مسبقاً على كود المساعد
            if "chatbot.js" in content or "chatbot.css" in content:
                skipped += 1
                continue

            # حساب المسار النسبي
            rel_css = os.path.relpath(css_abs_path, os.path.dirname(file_path)).replace('\\', '/')
            rel_js = os.path.relpath(js_abs_path, os.path.dirname(file_path)).replace('\\', '/')

            css_tag = f'\n<!-- Chatbot CSS -->\n<link href="{rel_css}" rel="stylesheet"/>\n</head>'
            content, count_css = re.subn(r'</head>', css_tag, content, count=1, flags=re.IGNORECASE)

            js_tag = f'\n<!-- Chatbot JS -->\n<script src="{rel_js}"></script>\n</body>'
            content, count_js = re.subn(r'</body>', js_tag, content, count=1, flags=re.IGNORECASE)

            if count_css > 0 or count_js > 0:
                with open(file_path, 'w', encoding=encoding_used) as f:
                    f.write(content)
                success += 1
            else:
                skipped += 1

        except Exception as e:
            errors += 1

    print(f"✅ تم الانتهاء بنجاح!")
    print(f"تم تعديل: {success} صفحة.")
    print(f"تم التخطي: {skipped} صفحة.")
    print(f"أخطاء: {errors} صفحة.")

if __name__ == "__main__":
    inject()
