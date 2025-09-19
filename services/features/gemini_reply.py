from google import genai
import os
from dotenv import load_dotenv
from services.constants import gemini_system_prompt

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_reply(prompt, system_prompt=None):
    """
    獲取 Gemini AI 回覆

    Args:
        prompt: 用戶輸入的內容
        system_prompt: 自定義的系統提示，如果不提供則使用預設的
    """
    if system_prompt is None:
        system_prompt = gemini_system_prompt

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=system_prompt + prompt,
    )
    return response.text
