"""
解答之書 Use Case

回傳純資料，不 import LINE SDK。
"""
from services.features.answers_book import get_answer


def get_answers_book_result(question: str = "") -> dict:
    """
    從解答之書隨機抽一條答案。

    Returns:
        {
            "question": "使用者的問題",
            "answer": "解答之書的回答",
            "error": None | str
        }
    """
    try:
        answer = get_answer()
        return {
            "question": question,
            "answer": answer,
            "error": None,
        }
    except Exception as e:
        print(f"[get_answers_book_result] 發生錯誤: {e}")
        return {
            "question": question,
            "answer": "",
            "error": "解答之書暫時無法使用，請稍後再試",
        }
