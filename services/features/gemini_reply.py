from google import genai
import os
from dotenv import load_dotenv
from services.constants import gemini_system_prompt

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_reply(prompt, system_prompt=None, timeout=15):
    """
    獲取 Gemini AI 回覆

    Args:
        prompt: 用戶輸入的內容
        system_prompt: 自定義的系統提示，如果不提供則使用預設的
        timeout: API 請求超時時間 (秒)，預設 15 秒 (目前未使用,保留參數以便未來擴展)
    """
    try:
        if system_prompt is None:
            system_prompt = gemini_system_prompt

        # Gemini API 調用 (Google genai SDK 會自動處理超時)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=system_prompt + prompt
        )
        return response.text
    except Exception as e:
        print(f"[Gemini API] 發生錯誤: {e}")
        return "沒請到神無法解籤"
