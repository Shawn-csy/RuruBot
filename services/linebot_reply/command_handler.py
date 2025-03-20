from typing import Dict, Any, Union
import random
import re
from services.features.radar import radar
from services.features.astro import get_astro_info
from services.constants import astro as astro_dict
from services.linebot_reply.process_reply_data import (
    process_astro_bubble_reply, 
    process_ticket_reply, 
    process_podcast_reply,
    process_sixty_poem_reply
)

from services.features.get_tickets import locat_ticket, get_sixty_poem
from services.features.get_podcast import get_podcast
from services.features.help import get_help_message
from services.linebot_reply.process_reply_data import process_help_reply

dice_pattern = re.compile(r'^(\d+)d(\d+)$', re.IGNORECASE)

def handle_command(command: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """根據命令執行相應的功能並返回結果"""
    
    try:
        # 如果沒有匹配的命令或命令為 None，直接返回 None
        if not command:
            return None
            
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
            astro_name = params.get("astro_name", "")
            astro_type = params.get("type", "daily")  
            if astro_name in astro_dict:
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
            reply = process_ticket_reply(ticket, params.get("text", ""))
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
            
        elif command == "sixty_poem":
            data, url = get_sixty_poem()
            if data and url:
                reply = process_sixty_poem_reply(data, url, params.get("text", ""))
                return {
                    "type": "flex",
                    "data": reply
                }
            else:
                return {
                    "type": "text",
                    "data": "抱歉，無法獲取籤詩資料"
                }
        
        elif command == "help":
            help_content = get_help_message()
            reply = process_help_reply(help_content)
            
            return {
                "type": "flex",
                "data": reply
            }
        
    except Exception as e:
        print(f"Error in handle_command: {str(e)}")
        return None
    
    