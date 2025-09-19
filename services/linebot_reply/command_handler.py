from typing import Dict, Any, Union
import random
import re
from services.features.radar import radar
from services.features.astro import get_astro_info
from services.features.spotify_service import spotify_service
from services.constants import astro as astro_dict, lulu_chat_system_prompt
from services.linebot_reply.process_reply_data import (
    process_astro_bubble_reply, 
    process_ticket_reply, 
    process_podcast_reply,
    process_sixty_poem_reply,
    process_music_reply
)

from services.features.get_tickets import locat_ticket, get_sixty_poem
from services.features.get_podcast import get_podcast
from services.features.help import get_help_message
from services.linebot_reply.process_reply_data import process_help_reply
from services.features.gemini_reply import get_gemini_reply

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
            
        elif command == "music":
            # 檢查是否有指定用戶
            user_name = params.get("user_name", "")
            music_info = spotify_service.get_random_recommendation(user_name if user_name else None)

            if "error" in music_info:
                return {
                    "type": "text",
                    "data": music_info["error"]
                }
            reply = process_music_reply(music_info)
            return {
                "type": "flex",
                "data": reply
            }

        elif command == "music_playlist":
            music_info = spotify_service.get_user_playlist_track()
            if "error" in music_info:
                return {
                    "type": "text",
                    "data": music_info["error"]
                }
            reply = process_music_reply(music_info)
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

        elif command == "lulu_chat":
            content = params.get("text", "")
            if content:
                # 使用專用的對話人設回覆用戶
                ai_response = get_gemini_reply(content, lulu_chat_system_prompt)
                return {
                    "type": "text",
                    "data": ai_response
                }
            else:
                return {
                    "type": "text",
                    "data": "請告訴露露你想聊什麼～ 🐱"
                }

    except Exception as e:
        print(f"處理命令時發生錯誤: {str(e)}")
        return {
            "type": "text",
            "data": "處理命令時發生錯誤，請稍後再試"
        }
    
    