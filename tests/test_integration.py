import unittest
from unittest.mock import patch, MagicMock
import sys
import os


from main import handle_message
from linebot.v3.webhooks import MessageEvent, TextMessageContent, Source


class TestIntegration(unittest.TestCase):
    
    @patch('main.ReplyService')
    @patch('services.command_handler.radar')
    def test_handle_message_radar(self, mock_radar, mock_reply_service_class):
        """測試處理雷達命令的完整流程"""
        # 模擬 radar 函數返回值
        mock_radar.return_value = ["http://example.com/radar.jpg"]
        
        # 模擬 ReplyService
        mock_reply_service = MagicMock()
        mock_reply_service_class.return_value = mock_reply_service
        
        # 創建模擬的 MessageEvent
        event = MessageEvent(
            reply_token="reply_token",
            type="message",
            mode="active",
            timestamp=1462629479859,
            source=Source(type="user", userId="U4af4980629..."),
            message=TextMessageContent(id="12345678901234", text="雷達")
        )
        
        # 調用函數
        handle_message(event)
        
        # 驗證 ReplyService.reply 被正確調用
        mock_reply_service.reply.assert_called_once()
        args = mock_reply_service.reply.call_args[0]
        self.assertEqual(args[0], "reply_token")
        self.assertEqual(args[1]["type"], "mixed")
        self.assertEqual(args[1]["data"][0]["type"], "image")
        self.assertEqual(args[1]["data"][0]["url"], "http://example.com/radar.jpg")
    
    @patch('main.ReplyService')
    @patch('services.astro.requests.get')
    def test_handle_message_astro(self, mock_get, mock_reply_service_class):
        """測試處理星座命令的完整流程"""
        # 創建模擬的 response
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <div class="TODAY_CONTENT">今日運勢：很好</div>
            <div class="TODAY_WORD">
                <p>愛情運：普通</p>
                <p>財運：不錯</p>
            </div>
        </html>
        """
        mock_get.return_value = mock_response
        
        # 模擬 ReplyService
        mock_reply_service = MagicMock()
        mock_reply_service_class.return_value = mock_reply_service
        
        # 創建模擬的 MessageEvent
        event = MessageEvent(
            reply_token="reply_token",
            type="message",
            mode="active",
            timestamp=1462629479859,
            source=Source(type="user", userId="U4af4980629..."),
            message=TextMessageContent(id="12345678901234", text="雙子座")
        )
        
        # 調用函數
        handle_message(event)
        
        # 驗證 ReplyService.reply 被正確調用
        mock_reply_service.reply.assert_called_once()
        args = mock_reply_service.reply.call_args[0]
        self.assertEqual(args[0], "reply_token")
        self.assertEqual(args[1]["type"], "text")
        self.assertIn("今日運勢：很好", args[1]["data"])


if __name__ == '__main__':
    unittest.main() 