from google import genai
import os
from services.constants import gemini_system_prompt

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


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

        response = _get_client().models.generate_content(
            model="gemini-3-flash-preview",
            contents=system_prompt + prompt
        )
        return response.text
    except Exception as e:
        print(f"[Gemini API] 發生錯誤: {e}")
        return "沒請到神無法解籤"
