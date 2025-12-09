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
from services.features.daily_meme import get_daily_meme
from datetime import datetime
import pytz
from services.linebot_reply.process_reply_data import (
    process_astro_bubble_reply,
    process_ticket_reply,
    process_podcast_reply,
    process_sixty_poem_reply,
    process_music_reply,
    process_help_reply,
    process_tarot_daily_reply
)
from services.linebot_reply.process_daily_meme import process_daily_meme_carousel


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
    try:
        ticket = locat_ticket(random.randint(0, 100))
        reply = process_ticket_reply(ticket, params.get("text", ""))
        return {"type": "flex", "data": reply}
    except Exception as e:
        print(f"[handle_ticket] 發生錯誤: {e}")
        return {"type": "text", "data": "抱歉，籤詩服務暫時無法使用，請稍後再試"}


def handle_sixty_poem(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理六十甲子籤命令"""
    try:
        data, url = get_sixty_poem()
        if data and url:
            reply = process_sixty_poem_reply(data, url, params.get("text", ""))
            return {"type": "flex", "data": reply}
        return {"type": "text", "data": "抱歉，無法獲取籤詩資料，請稍後再試"}
    except Exception as e:
        print(f"[handle_sixty_poem] 發生錯誤: {e}")
        return {"type": "text", "data": "抱歉，籤詩服務暫時無法使用，請稍後再試"}


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


def handle_daily_meme(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """處理每日梗圖命令"""
    image_urls = get_daily_meme()
    if image_urls and len(image_urls) > 0:
        # 獲取今天的日期字串
        taipei_tz = pytz.timezone('Asia/Taipei')
        today = datetime.now(taipei_tz)
        date_str = today.strftime("%Y/%m/%d")

        # 第一則訊息顯示日期,後面是圖片
        messages = [{"type": "text", "text": f"📅 {date_str} 每日梗圖"}]
        messages.extend([{"type": "image", "url": url} for url in image_urls])

        return {
            "type": "mixed",
            "data": messages
        }
    return {"type": "text", "data": "抱歉,今天還沒有梗圖或無法取得"}
