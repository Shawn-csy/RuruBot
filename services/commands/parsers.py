"""
命令參數解析器集合

每個解析器負責從用戶輸入中提取命令參數
"""
from typing import Dict, Any, Optional
from services.constants import astro as astro_dict


def parse_astro_params(text: str) -> Optional[Dict[str, Any]]:
    """
    解析星座命令參數

    Args:
        text: 用戶輸入文本

    Returns:
        {"astro_name": "星座名", "type": "daily/weekly"} 或 None
    """
    for astro_name in astro_dict.keys():
        if astro_name in text:
            astro_type = "weekly" if "-w" in text else "daily"
            return {"astro_name": astro_name, "type": astro_type}
    return None


def parse_astro_weekly_flag_params(text: str) -> Optional[Dict[str, Any]]:
    """
    解析 -w 星座名 格式（weekly flag 在前）

    Args:
        text: 用戶輸入文本，需以 -w 開頭

    Returns:
        {"astro_name": "星座名", "type": "weekly"} 或 None
    """
    for astro_name in astro_dict.keys():
        if astro_name in text:
            return {"astro_name": astro_name, "type": "weekly"}
    return None




def parse_ticket_params(text: str) -> Dict[str, Any]:
    """解析淺草寺籤參數"""
    return {"text": text}


def parse_answers_book_params(text: str) -> Dict[str, Any]:
    """解析解答之書參數，提取問題內容"""
    question = text.replace("解答之書", "").strip()
    return {"question": question}
