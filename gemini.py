import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY=os.getenv('API_KEY')

# configure
genai.configure(api_key=API_KEY)

model=genai.GenerativeModel('gemini-1.5-flash')

def ask_gemini(queries):
    response=model.generate_content(queries)
    return response.text