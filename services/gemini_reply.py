from google import genai
import os
from dotenv import load_dotenv
from services.get_tickets import locat_ticket
import random
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
setting = "你是一個黑貓廟公，擅長根據籤詩結果，給出簡短的解釋和建議。"



def get_gemini_reply(prompt):
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=setting+prompt,
    
    )
    return response.text


