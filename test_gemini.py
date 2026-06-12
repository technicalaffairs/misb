import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

def search_site(query: str)->str:
    return 'test'

model = genai.GenerativeModel('gemini-flash-latest', tools=[search_site])
chat = model.start_chat(enable_automatic_function_calling=True)
try:
    print(chat.send_message('كيف يعمل مغير الجهد؟').text)
except Exception as e:
    print(e)
