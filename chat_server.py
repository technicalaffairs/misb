import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Allow requests from the HTML frontend

# قم بوضع مفتاح API الخاص بك هنا
# احصل عليه مجاناً من: https://aistudio.google.com/
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "ضع_مفتاح_API_هنا")

genai.configure(api_key=GEMINI_API_KEY)

# إعداد شخصية المهندس
system_instruction = """
أنت مهندس كهرباء قوى محترف وخبير. 
مهمتك هي الإجابة على استفسارات المستخدمين حول توليد ونقل وتوزيع الطاقة الكهربائية، المحطات، المحولات، والمحركات.
يجب أن تكون إجاباتك دقيقة، علمية، ومبسطة قدر الإمكان باللغة العربية.
لا تجب على أسئلة خارج هذا التخصص، وإذا سُئلت عن شيء آخر، اعتذر بلطف وأخبر المستخدم أن تخصصك هو هندسة القوى الكهربائية فقط.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
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
    print("🚀 بدء تشغيل خادم المحادثة الذكي على المنفذ 5000...")
    print("⚠️ تذكر إضافة مفتاح GEMINI_API_KEY في الكود أو كمتغير بيئة.")
    app.run(debug=True, port=5000)
