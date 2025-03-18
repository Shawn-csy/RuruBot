import unittest
from unittest.mock import patch, MagicMock
import sys
import os


from services.command_handler import parse_command, handle_command


class TestCommandHandler(unittest.TestCase):
    
    def test_parse_command_radar(self):
        """測試解析雷達命令"""
        command, params = parse_command("雷達")
        self.assertEqual(command, "radar")
        self.assertEqual(params, {})
        
        command, params = parse_command("radar")
        self.assertEqual(command, "radar")
        self.assertEqual(params, {})
    
    def test_parse_command_astro_daily(self):
        """測試解析星座日報命令"""
        command, params = parse_command("雙子座")
        self.assertEqual(command, "astro")
        self.assertEqual(params, {"astro_name": "雙子座", "type": "daily"})
    
    def test_parse_command_astro_weekly(self):
        """測試解析星座週報命令"""
        command, params = parse_command("雙子座 -w")
        self.assertEqual(command, "astro")
        self.assertEqual(params, {"astro_name": "雙子座", "type": "weekly"})
    
    def test_parse_command_echo(self):
        """測試解析回聲命令"""
        command, params = parse_command("你好")
        self.assertEqual(command, "echo")
        self.assertEqual(params, {"text": "你好"})
    
    @patch('services.command_handler.radar')
    def test_handle_command_radar(self, mock_radar):
        """測試處理雷達命令"""
        # 模擬 radar 函數返回值
        mock_radar.return_value = ["http://example.com/radar.jpg"]
        
        result = handle_command("radar", {})
        self.assertEqual(result["type"], "mixed")
        self.assertEqual(result["data"][0]["type"], "image")
        self.assertEqual(result["data"][0]["url"], "http://example.com/radar.jpg")
    
    @patch('services.command_handler.get_astro_info')
    def test_handle_command_astro(self, mock_get_astro_info):
        """測試處理星座命令"""
        # 模擬 get_astro_info 函數返回值
        mock_get_astro_info.return_value = ["今日運勢：很好", "愛情運：普通"]
        
        result = handle_command("astro", {"astro_name": "雙子座", "type": "daily"})
        self.assertEqual(result["type"], "text")
        self.assertEqual(result["data"], "今日運勢：很好\n愛情運：普通")
    
    def test_handle_command_echo(self):
        """測試處理回聲命令"""
        result = handle_command("echo", {"text": "你好"})
        self.assertEqual(result["type"], "text")
        self.assertEqual(result["data"], "你好")
    
    def test_handle_command_unknown(self):
        """測試處理未知命令"""
        result = handle_command("unknown", {})
        self.assertEqual(result["type"], "text")
        self.assertEqual(result["data"], "抱歉，我不明白這個命令")


if __name__ == '__main__':
    unittest.main() 