"""
命令處理器集合

每個處理器負責執行具體的業務邏輯並返回結果
"""
import random
from typing import Dict, Any, Optional
from services.constants import astro as astro_dict, lulu_chat_system_prompt
from services.features.radar import radar
from services.features.astro import get_astro_info
from services.features.spotify_service import spotify_service
from services.features.get_tickets import locat_ticket, get_sixty_poem
from services.features.get_podcast import get_podcast
from services.features.help import get_help_message
from services.features.gemini_reply import get_gemini_reply
from services.features.tarot import tarot_with_fallback
from services.features.dogdog_meme import dogdog_meme
from services.linebot_reply.process_reply_data import (
    process_astro_bubble_reply,
    process_ticket_reply,
    process_podcast_reply,
    process_sixty_poem_reply,
    process_music_reply,
    process_help_reply,
    process_tarot_daily_reply
)


def handle_radar(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理雷達命令"""
    radar_urls = radar()
    if radar_urls and len(radar_urls) > 0:
        return {
            "type": "mixed",
            "data": [{"type": "image", "url": radar_urls[0]}]
        }
    return None


def handle_astro(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理星座命令"""
    astro_name = params.get("astro_name", "")
    astro_type = params.get("type", "daily")

    if astro_name not in astro_dict:
        return {"type": "text", "data": "抱歉，無法識別的星座名稱"}

    astro_info = get_astro_info(astro_name, astro_type)
    reply = process_astro_bubble_reply(astro_info)
    return {"type": "flex", "data": reply}


def handle_ticket(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理淺草寺籤命令"""
    ticket = locat_ticket(random.randint(0, 100))
    reply = process_ticket_reply(ticket, params.get("text", ""))
    return {"type": "flex", "data": reply}


def handle_sixty_poem(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理六十甲子籤命令"""
    data, url = get_sixty_poem()
    if data and url:
        reply = process_sixty_poem_reply(data, url, params.get("text", ""))
        return {"type": "flex", "data": reply}
    return {"type": "text", "data": "抱歉，無法獲取籤詩資料"}


def handle_podcast(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理國師命令"""
    podcast = get_podcast()
    reply = process_podcast_reply(podcast)
    return {"type": "flex", "data": reply}


def handle_music(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理音樂推薦命令"""
    user_name = params.get("user_name")
    music_info = spotify_service.get_random_recommendation(user_name if user_name else None)

    if "error" in music_info:
        return {"type": "text", "data": music_info["error"]}

    reply = process_music_reply(music_info)
    return {"type": "flex", "data": reply}


def handle_help(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理幫助命令"""
    help_content = get_help_message()
    reply = process_help_reply(help_content)
    return {"type": "flex", "data": reply}


def handle_lulu_chat(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理露露對話命令"""
    content = params.get("text", "")
    if content:
        ai_response = get_gemini_reply(content, lulu_chat_system_prompt)
        return {"type": "text", "data": ai_response}
    return {"type": "text", "data": "請告訴露露你想聊什麼～ 🐱"}


def handle_dogmeme(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理暈船迷因"""
    img_url = dogdog_meme()
    return {
        "type": "mixed",
        "data": [{"type": "image", "url": img_url}]
    }


def handle_tarot(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理塔羅命令"""
    method = params.get("method", "daily")
    question = params.get("question")
    spread_name = params.get("spread_name", "時間之流占卜法")

    result = tarot_with_fallback(
        method=method,
        question=question,
        spread_name=spread_name
    )

    if result and result.get("success"):
        try:
            reply = process_tarot_daily_reply(result["data"])
            return {"type": "flex", "data": reply}
        except Exception as e:
            print(f"Flex Message 處理失敗: {e}")
            source_label = "🌐 API" if result["source"] == "api" else "💻 本地"
            return {"type": "text", "data": f"{source_label} 塔羅解讀\n\n{result['data']}"}

    return {"type": "text", "data": "塔羅占卜發生錯誤，請稍後再試"}
