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


def parse_ticket_params(text: str) -> Dict[str, Any]:
    """解析淺草寺籤參數"""
    return {"text": text}


def parse_sixty_poem_params(text: str) -> Dict[str, Any]:
    """解析六十甲子籤參數"""
    return {"text": text.replace("抽六十甲子籤", "").strip()}


def parse_music_params(text: str) -> Dict[str, Any]:
    """
    解析音樂命令參數

    支持:
    - --m: 隨機推薦
    - --ping 用戶名: 指定用戶推薦
    """
    if "--ping" in text:
        user_name = text.replace("--ping", "").strip()
        return {"user_name": user_name} if user_name else {}
    return {}


def parse_lulu_chat_params(text: str) -> Optional[Dict[str, Any]]:
    """
    解析露露對話參數

    格式: 露露 [對話內容]
    """
    if text.startswith("露露"):
        content = text[2:].strip()
        if content:
            return {"text": content}
    return None


def parse_tarot_params(text: str) -> Dict[str, Any]:
    """
    解析塔羅命令參數

    支持:
    - 每日塔羅/本日塔羅
    - -塔羅 [問題]
    """
    # 每日塔羅
    if text in ["每日塔羅", "本日塔羅"]:
        return {"method": "daily", "question": None}

    # 問題塔羅
    if text.startswith("-塔羅"):
        question = text[3:].strip()
        return {
            "method": "question" if question else "daily",
            "question": question if question else None
        }

    return {"method": "daily", "question": None}
