from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest,
    TextMessage, ImageMessage, FlexMessage, FlexContainer
)
from typing import Dict, Any, List, Union
import json

class ReplyService:
    """統一的回覆服務"""
    
    def __init__(self, configuration: Configuration):
        self.api_client = ApiClient(configuration)
        self.line_bot_api = MessagingApi(self.api_client)
    
    def reply(self, reply_token: str, result: Dict[str, Any]) -> None:
        """統一的回覆服務"""
        # 如果結果為 None，不進行任何回覆
        if result is None:
            return
        
        result_type = result.get("type", "text")
        data = result.get("data", "")
        
        if result_type == "text":
            self._reply_text(reply_token, data)
        elif result_type == "image":
            self._reply_images(reply_token, data)
        elif result_type == "carousel":
            self._reply_carousel(reply_token, data)
        elif result_type == "flex":
            self._reply_flex(reply_token, data)
        elif result_type == "mixed":
            self._reply_mixed(reply_token, data)
    
    def _reply_text(self, reply_token: str, text: str) -> None:
        """發送文字回覆"""
        # 確保 text 是字符串
        if not isinstance(text, str):
            if isinstance(text, list):
                text = "\n\n".join(text)
            else:
                text = str(text)
        
        # 確保文字不為空
        if not text.strip():
            text = "抱歉，沒有獲取到資訊"
        
        self.line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=text)]
            )
        )
    
    def _reply_images(self, reply_token: str, image_urls: List[str]) -> None:
        """發送圖片回覆"""
        image_messages = [
            ImageMessage(
                originalContentUrl=url,
                previewImageUrl=url
            ) for url in image_urls
        ]
        
        self.line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=image_messages
            )
        )
    
    def _reply_carousel(self, reply_token: str, carousel_data: Dict[str, Any]) -> None:
        """發送輪播回覆"""
        # 實現輪播訊息的邏輯
        pass 
    
    def _reply_flex(self, reply_token: str, flex_data: Union[Dict[str, Any], FlexMessage]) -> None:
        """發送 Flex 訊息"""
        # 檢查 flex_data 的類型
        if isinstance(flex_data, dict):
            # 如果是字典，按原來的方式處理
            flex_json = flex_data.get("content", {})
            alt_text = flex_data.get("alt_text", "Flex Message")
            
            flex_container = FlexContainer.from_dict(flex_json)
            flex_message = FlexMessage(alt_text=alt_text, contents=flex_container)
        else:
            # 如果已經是 FlexMessage 對象，直接使用
            flex_message = flex_data
        
        self.line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[flex_message]
            )
        ) 
    
    def _reply_mixed(self, reply_token: str, messages_data: List[Dict[str, Any]]) -> None:
        """發送混合多種類型的訊息"""
        messages = []
        
        for msg_data in messages_data:
            msg_type = msg_data.get("type")
            
            if msg_type == "text":
                messages.append(TextMessage(text=msg_data.get("text", "")))
            elif msg_type == "image":
                messages.append(ImageMessage(
                    originalContentUrl=msg_data.get("url", ""),
                    previewImageUrl=msg_data.get("preview_url", msg_data.get("url", ""))
                ))
            elif msg_type == "flex":
                flex_container = FlexContainer.from_dict(msg_data.get("content", {}))
                messages.append(FlexMessage(
                    alt_text=msg_data.get("alt_text", "Flex Message"),
                    contents=flex_container
                ))
        
        if messages:
            self.line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=messages
                )
            ) 