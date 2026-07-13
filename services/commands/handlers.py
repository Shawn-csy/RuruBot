"""
命令處理器集合

每個處理器負責執行具體的業務邏輯並返回結果
"""
from typing import Dict, Any, Optional
from services.constants import astro as astro_dict
from services.use_cases.astro import get_astro_result
from services.use_cases.radar import get_radar_result
from services.use_cases.ticket import get_ticket_result
from services.use_cases.podcast import get_podcast_result
from services.use_cases.answers_book import get_answers_book_result
from services.features.help import get_help_message
from services.features.dogdog_meme import dogdog_meme
from services.linebot_reply.process_reply_data import (
    process_astro_bubble_reply,
    process_ticket_reply,
    process_podcast_reply,
    process_help_reply,
    process_answers_book_reply,
)


def handle_radar(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理雷達命令"""
    result = get_radar_result()
    if result.get("error") or not result["urls"]:
        return None
    return {
        "type": "mixed",
        "data": [{"type": "image", "url": result["urls"][0]}]
    }


def handle_astro(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理星座命令"""
    astro_name = params.get("astro_name", "")
    astro_type = params.get("type", "daily")

    if astro_name not in astro_dict:
        return {"type": "text", "data": "抱歉，無法識別的星座名稱"}

    result = get_astro_result(astro_name, astro_type)
    reply = process_astro_bubble_reply(result)
    return {"type": "flex", "data": reply}


def handle_ticket(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理淺草寺籤命令"""
    question = params.get("text", "").replace("抽淺草寺", "").strip()
    result = get_ticket_result(question)
    if result.get("error"):
        return {"type": "text", "data": result["error"]}
    reply = process_ticket_reply(result)
    return {"type": "flex", "data": reply}


def handle_podcast(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理國師命令"""
    result = get_podcast_result()
    if result.get("error"):
        return {"type": "text", "data": result["error"]}
    reply = process_podcast_reply(result)
    return {"type": "flex", "data": reply}


def handle_help(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理幫助命令"""
    help_content = get_help_message()
    reply = process_help_reply(help_content)
    return {"type": "flex", "data": reply}


def handle_dogmeme(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理暈船迷因"""
    img_url = dogdog_meme()
    return {
        "type": "mixed",
        "data": [{"type": "image", "url": img_url}]
    }


def handle_answers_book(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理解答之書命令"""
    question = params.get("question", "")
    result = get_answers_book_result(question)
    if result.get("error"):
        return {"type": "text", "data": result["error"]}
    reply = process_answers_book_reply(result)
    return {"type": "flex", "data": reply}
