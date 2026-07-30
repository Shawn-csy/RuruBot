"""
淺草寺抽籤 Use Case

負責：抽籤、解構資料、呼叫 Gemini 解籤，回傳純資料，不 import LINE SDK。
"""
import random
from services.features.get_tickets import locat_ticket
from services.features.gemini_reply import get_gemini_reply


def get_ticket_result(question: str = "", with_ai: bool = True) -> dict:
    """
    抽一支淺草寺籤並取得解籤結果。

    Args:
        question: 使用者的問題（可為空）
        with_ai: 是否呼叫 Gemini 解籤。LINE 指令維持 True；REST API 可用 False 快速回籤詩。

    Returns:
        {
            "title": "第001籤",
            "ticket_type": "大吉",
            "poem": "...",
            "explain": "...",
            "result": "...",
            "img_url": "https://...",
            "ai_result": "Gemini 解籤文字 | 喵？",
            "error": None | str
        }
    """
    try:
        ticket_data, img_url = locat_ticket(random.randint(0, 99))
        title, ticket_type, poem, explain, result = ticket_data

        if question and with_ai:
            ai_result = get_gemini_reply(
                "問題 " + question + " 籤詩結果 " + title + poem + explain + result
            )
        elif question:
            ai_result = ""
        else:
            ai_result = "喵？"

        return {
            "title": title,
            "ticket_type": ticket_type,
            "poem": poem,
            "explain": explain,
            "result": result,
            "img_url": img_url,
            "ai_result": ai_result,
            "error": None,
        }
    except Exception as e:
        print(f"[get_ticket_result] 發生錯誤: {e}")
        return {
            "title": "",
            "ticket_type": "",
            "poem": "",
            "explain": "",
            "result": "",
            "img_url": "",
            "ai_result": "",
            "error": "抱歉，籤詩服務暫時無法使用，請稍後再試",
        }
