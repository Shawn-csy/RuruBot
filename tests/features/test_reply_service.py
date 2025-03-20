# 將原本的 test_reply_service.py 移動到 tests/features/ 目錄 

import pytest
from unittest.mock import patch, MagicMock
from services.linebot_reply.reply_service import ReplyService
from linebot.v3.messaging import (
    Configuration,
    TextMessage,
    ImageMessage,
    FlexMessage,
    ReplyMessageRequest
)

class TestReplyService:
    """回覆服務測試"""
    
    @pytest.fixture
    def reply_service(self):
        """建立回覆服務實例"""
        config = Configuration(access_token="dummy_token")
        service = ReplyService(config)
        # 直接 mock line_bot_api
        service.line_bot_api = MagicMock()
        return service

    def test_reply_text(self, reply_service):
        """測試文字回覆"""
        reply_service.reply("reply-token", {
            "type": "text",
            "data": "測試訊息"
        })
        
        # 驗證呼叫
        reply_service.line_bot_api.reply_message.assert_called_once()
        args = reply_service.line_bot_api.reply_message.call_args[0][0]
        assert isinstance(args, ReplyMessageRequest)
        assert len(args.messages) == 1
        assert isinstance(args.messages[0], TextMessage)
        assert args.messages[0].text == "測試訊息"

    def test_reply_image(self, reply_service):
        """測試圖片回覆"""
        image_url = "https://example.com/image.jpg"
        reply_service.reply("reply-token", {
            "type": "image",
            "data": [image_url]
        })
        
        reply_service.line_bot_api.reply_message.assert_called_once()
        args = reply_service.line_bot_api.reply_message.call_args[0][0]
        assert isinstance(args.messages[0], ImageMessage)
        assert args.messages[0].original_content_url == image_url
        assert args.messages[0].preview_image_url == image_url

    def test_reply_mixed(self, reply_service):
        """測試混合回覆"""
        image_url = "https://example.com/image.jpg"
        reply_service.reply("reply-token", {
            "type": "mixed",
            "data": [
                {
                    "type": "text",
                    "text": "測試文字"
                },
                {
                    "type": "image",
                    "url": image_url,
                    "preview_url": image_url
                }
            ]
        })
        
        reply_service.line_bot_api.reply_message.assert_called_once()
        args = reply_service.line_bot_api.reply_message.call_args[0][0]
        assert len(args.messages) == 2
        assert isinstance(args.messages[0], TextMessage)
        assert isinstance(args.messages[1], ImageMessage)

    def test_reply_none(self, reply_service):
        """測試 None 回覆"""
        reply_service.reply("reply-token", None)
        reply_service.line_bot_api.reply_message.assert_not_called() 