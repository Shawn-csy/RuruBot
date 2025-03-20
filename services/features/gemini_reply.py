from google import genai
import os
from dotenv import load_dotenv
from services.constants import gemini_system_prompt

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
setting = gemini_system_prompt



def get_gemini_reply(prompt):
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=setting+prompt,
    
    )
    return response.text
