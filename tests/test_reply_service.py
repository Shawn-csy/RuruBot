import unittest
from unittest.mock import patch, MagicMock
from services.linebot_reply.reply_service import ReplyService
from linebot.v3.messaging import Configuration, TextMessage, ImageMessage, FlexMessage


class TestReplyService(unittest.TestCase):
    
    def setUp(self):
        """設置測試環境"""
        self.configuration = Configuration(access_token="dummy_token")
        self.reply_service = ReplyService(self.configuration)
        # 模擬 line_bot_api
        self.reply_service.line_bot_api = MagicMock()
    
    def test_reply_text(self):
        """測試文字回覆"""
        # 調用函數
        self.reply_service.reply("reply_token", {
            "type": "text",
            "data": "你好"
        })
        
        # 驗證 line_bot_api.reply_message 被正確調用
        self.reply_service.line_bot_api.reply_message.assert_called_once()
        args = self.reply_service.line_bot_api.reply_message.call_args[0][0]
        self.assertEqual(args.reply_token, "reply_token")
        self.assertEqual(len(args.messages), 1)
        self.assertIsInstance(args.messages[0], TextMessage)
        self.assertEqual(args.messages[0].text, "你好")
    
    def test_reply_text_empty(self):
        """測試空文字回覆"""
        # 調用函數
        self.reply_service.reply("reply_token", {
            "type": "text",
            "data": ""
        })
        
        # 驗證 line_bot_api.reply_message 被正確調用，且使用了預設文字
        args = self.reply_service.line_bot_api.reply_message.call_args[0][0]
        self.assertEqual(args.messages[0].text, "抱歉，沒有獲取到資訊")
    
    def test_reply_text_list(self):
        """測試列表文字回覆"""
        # 調用函數
        self.reply_service.reply("reply_token", {
            "type": "text",
            "data": ["你好", "世界"]
        })
        
        # 驗證 line_bot_api.reply_message 被正確調用，且列表被正確轉換為字符串
        args = self.reply_service.line_bot_api.reply_message.call_args[0][0]
        self.assertEqual(args.messages[0].text, "你好\n\n世界")
    
    def test_reply_image(self):
        """測試圖片回覆"""
        # 調用函數
        self.reply_service.reply("reply_token", {
            "type": "image",
            "data": ["http://example.com/image.jpg"]
        })
        
        # 驗證 line_bot_api.reply_message 被正確調用
        args = self.reply_service.line_bot_api.reply_message.call_args[0][0]
        self.assertEqual(args.reply_token, "reply_token")
        self.assertEqual(len(args.messages), 1)
        self.assertIsInstance(args.messages[0], ImageMessage)
        self.assertEqual(args.messages[0].originalContentUrl, "http://example.com/image.jpg")
    
    def test_reply_mixed(self):
        """測試混合回覆"""
        # 調用函數
        self.reply_service.reply("reply_token", {
            "type": "mixed",
            "data": [
                {"type": "text", "text": "你好"},
                {"type": "image", "url": "http://example.com/image.jpg"}
            ]
        })
        
        # 驗證 line_bot_api.reply_message 被正確調用
        args = self.reply_service.line_bot_api.reply_message.call_args[0][0]
        self.assertEqual(args.reply_token, "reply_token")
        self.assertEqual(len(args.messages), 2)
        self.assertIsInstance(args.messages[0], TextMessage)
        self.assertEqual(args.messages[0].text, "你好")
        self.assertIsInstance(args.messages[1], ImageMessage)
        self.assertEqual(args.messages[1].originalContentUrl, "http://example.com/image.jpg")
    
    def test_reply_unsupported(self):
        """測試不支援的回覆類型"""
        # 調用函數
        self.reply_service.reply("reply_token", {
            "type": "unsupported",
            "data": "data"
        })
        
        # 驗證 line_bot_api.reply_message 被正確調用，且使用了預設文字
        args = self.reply_service.line_bot_api.reply_message.call_args[0][0]
        self.assertEqual(args.messages[0].text, "不支援的回覆類型")


if __name__ == '__main__':
    unittest.main() 