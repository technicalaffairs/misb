import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow requests from the HTML frontend

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# إعداد شخصية المهندس
system_instruction = """
أنت المساعد الشخصي للمستخدم، ولكنك تفكر ولديك خبرة واسعة كمهندس كهرباء قوى محترف.
إذا سألك المستخدم من أنت، أجب دائماً بأنك "مساعده الشخصي".
مهمتك الأساسية هي الإجابة على استفسارات المستخدمين حول توليد ونقل وتوزيع الطاقة الكهربائية، المحطات، المحولات، والمحركات.

إضافة لذلك، أنت مسؤول عن توجيه المستخدم لصفحات الموقع الخاصة بكل قسم.
إذا سأل المستخدم عن أحد المواضيع التالية، أجب عن سؤاله باختصار ثم أضف في نهاية رسالتك تماماً الكود التالي ليقوم المتصفح بنقله للصفحة: [OPEN_PAGE: filename.htm]
- الغلايات (Boilers): استخدم الكود [OPEN_PAGE: Ar_Boilers_docs Page.htm]
- التوربينات (Turbines): استخدم الكود [OPEN_PAGE: Ar_Turbines.htm]
- المولدات (Generators): استخدم الكود [OPEN_PAGE: Ar_Generators Page.htm]
- المحركات (Motors): استخدم الكود [OPEN_PAGE: Ar_Motors Page.htm]
- المضخات (Pumps): استخدم الكود [OPEN_PAGE: Ar_Pumps_docs Page.htm]
- مغيرات الجهد (Tap Changers): استخدم الكود [OPEN_PAGE: Ar_appr_docs/Ar_ad_subst/new_pages/Ar_ad_tap_changers.htm]
- المحولات (Transformers): استخدم الكود [OPEN_PAGE: Ar_appr_docs/Ar_ad_subst/new_pages/Ar_ad_Trafo.htm]
- خطوط النقل (Transmission Lines): استخدم الكود [OPEN_PAGE: Ar_appr_docs/Ar_ad_trans/Ar_ad_trans.htm]
- الصمامات (Valves): استخدم الكود [OPEN_PAGE: Ar_Valves.htm]
- المراوح (Fans): استخدم الكود [OPEN_PAGE: Ar_Fans_docs Page.htm]
- الأوناش والروافع (Cranes): استخدم الكود [OPEN_PAGE: Ar_Cranes_Page.htm]

يجب أن تكون إجاباتك دقيقة، علمية، ومبسطة قدر الإمكان باللغة العربية.
لا تجب على أسئلة خارج التخصصات الهندسية.
"""

model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=system_instruction
)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # إرسال الرسالة لنموذج جيميناي
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "حدث خطأ أثناء التواصل مع الذكاء الاصطناعي."}), 500

if __name__ == '__main__':
    print("بدء تشغيل خادم المحادثة الذكي على المنفذ 5000...")
    print("تذكر إضافة مفتاح GEMINI_API_KEY في الكود أو كمتغير بيئة.")
    app.run(debug=True, port=5000)
