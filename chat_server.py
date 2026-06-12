import os
import json
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow requests from the HTML frontend

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Load search index
print("Loading search index...")
try:
    with open('search_index.json', 'r', encoding='utf-8') as f:
        SEARCH_INDEX = json.load(f)
    print(f"Loaded {len(SEARCH_INDEX)} documents into memory.")
except Exception as e:
    print(f"Error loading index: {e}")
    SEARCH_INDEX = []

def search_site(query: str) -> str:
    """
    يبحث في مستندات وصفحات موقع محطة المحولات عن الكلمات المفتاحية المتعلقة بسؤال المستخدم.
    استخدم هذه الأداة دائماً للبحث عن المعلومات للإجابة على الأسئلة التقنية.
    ترجع الدالة أفضل 3 صفحات مطابقة تحتوي على المعلومات مع روابطها.
    """
    if not SEARCH_INDEX:
        return "عذراً، الفهرس غير متاح حالياً."
        
    keywords = set(re.findall(r'\w+', query.lower()))
    if not keywords:
        return "لا توجد كلمات مفتاحية في البحث."
        
    scored_results = []
    
    for doc in SEARCH_INDEX:
        content_lower = doc['content'].lower()
        title_lower = doc['title'].lower()
        
        score = 0
        for kw in keywords:
            if len(kw) < 3: continue
            score += title_lower.count(kw) * 5
            score += content_lower.count(kw)
            
        if score > 0:
            scored_results.append((score, doc))
            
    scored_results.sort(key=lambda x: x[0], reverse=True)
    top_results = scored_results[:3]
    
    if not top_results:
        return "لم يتم العثور على أي معلومات حول هذا الموضوع في مستندات الموقع."
        
    result_text = "نتائج البحث في مستندات الموقع:\n\n"
    for idx, (score, doc) in enumerate(top_results):
        snippet = doc['content'][:1000]
        for kw in keywords:
            if len(kw) > 2 and kw in doc['content'].lower():
                pos = doc['content'].lower().find(kw)
                start = max(0, pos - 200)
                end = min(len(doc['content']), pos + 800)
                snippet = doc['content'][start:end]
                break
                
        result_text += f"العنوان: {doc['title']}\n"
        result_text += f"مسار الملف: {doc['path']}\n"
        result_text += f"المحتوى المقتبس: ...{snippet}...\n\n"
        
    return result_text


# إعداد شخصية المهندس
system_instruction = """
أنت مهندس كهرباء قوى محترف وخبير تعمل في موقع محطة محولات، وهندسة الخطوط، والوقاية، والصيانة.
إذا سألك المستخدم من أنت، أجب بأنك "مساعده الشخصي وتفكر كمهندس كهرباء محترف".
أنت دائم التعلم من مستندات الموقع الموجودة لديك.

تعليمات هامة جداً:
1. عند طرح أي سؤال فني، يجب عليك **دائماً** استخدام أداة البحث `search_site` للبحث في مستندات الموقع قبل الإجابة.
2. اقرأ نتائج البحث وصغ منها إجابة علمية، دقيقة، ومبسطة باللغة العربية.
3. **يجب** أن ترفق في نهاية إجابتك كود فتح الصفحة التي اقتبست منها المعلومة بالضبط بالصيغة التالية:
[OPEN_PAGE: مسار_الملف]
(حيث مسار_الملف هو المسار الموجود في نتائج أداة البحث مثل arabic_web/Ar_appr_docs/...).
4. لا تجب على أسئلة خارج التخصصات الهندسية.
5. إذا لم تجد الإجابة في البحث، يمكنك الإجابة من خبرتك الهندسية، ولكن وضح للمستخدم أن المعلومة ليست من مستندات الموقع المباشرة.
"""

model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=system_instruction,
    tools=[search_site]
)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # إرسال الرسالة لنموذج جيميناي
        # Initialize a new chat session for function calling to work nicely
        chat_session = model.start_chat(enable_automatic_function_calling=True)
        response = chat_session.send_message(user_message)
        
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "حدث خطأ أثناء التواصل مع الذكاء الاصطناعي."}), 500

if __name__ == '__main__':
    print("بدء تشغيل خادم المحادثة الذكي على المنفذ 5000...")
    print("تذكر إضافة مفتاح GEMINI_API_KEY في الكود أو كمتغير بيئة.")
    app.run(debug=True, port=5000)
