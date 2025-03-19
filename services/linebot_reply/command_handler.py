from services.radar import radar
from services.astro import get_astro_info
from typing import Dict, Any, Union
from services.constants import astro as astro_dict
from services.linebot_reply.process_reply_data import process_astro_bubble_reply, process_ticket_reply, process_podcast_reply
from services.get_tickets import locat_ticket
from services.get_podcast import get_podcast
import random
from services.linebot_reply.parse_command import parse_command
import re

dice_pattern = re.compile(r'^(\d+)d(\d+)$', re.IGNORECASE)


def handle_command(command: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    處理各種命令並返回結果
    
    Args:
        command: 命令名稱
        params: 命令參數
        
    Returns:
        包含回覆資訊的字典
    """
    if command == "radar":
        radar_urls = radar()
        if radar_urls and len(radar_urls) > 0:
            return {
                "type": "mixed",
                "data": [
                    {
                        "type": "image",
                        "url": radar_urls[0]
                    }
                ]
            }
    
    elif command == "astro":
        # 從參數中獲取星座名稱
        astro_name = params.get("astro_name", "")
        astro_type = params.get("type", "daily")  
        if astro_name in astro_dict:
            # 獲取星座資訊
            astro_info = get_astro_info(astro_name, astro_type)
            reply = process_astro_bubble_reply(astro_info)
            
            return {
                "type": "flex",
                "data": reply
            }
        else:
            return {
                "type": "text",
                "data": "抱歉，無法識別的星座名稱"
            }
    elif command == "ticket":
        ticket = locat_ticket(random.randint(0, 100))
        reply = process_ticket_reply(ticket,params.get("text", ""))
        return {
            "type": "flex",
            "data": reply
        }
    elif command == "podcast":
        podcast = get_podcast()
        reply = process_podcast_reply(podcast)
        return {
            "type": "flex",
            "data": reply
        }
    
    