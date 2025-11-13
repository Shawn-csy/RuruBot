import pytest
from unittest.mock import patch, MagicMock
from services.commands import handle_command
from linebot.v3.messaging import FlexMessage

class TestCommandHandler:
    """命令處理器測試"""
    
    def test_handle_astro(self):
        """測試星座命令處理"""
        with patch('services.features.astro.get_astro_info') as mock_astro:
            mock_astro.return_value = {"星座": "金牛座", "運勢": "很好"}
            result = handle_command("astro", {
                "astro_name": "金牛座",
                "type": "daily"
            })
            
            assert result["type"] == "flex"
            assert isinstance(result["data"], (dict, FlexMessage))
            if isinstance(result["data"], FlexMessage):
                assert result["data"].alt_text == "今日運勢"
                assert result["data"].contents is not None
    
    def test_handle_ticket(self):
        """測試抽籤命令處理"""
        result = handle_command("ticket", {"text": "工作運"})
        assert result["type"] == "flex"
        assert isinstance(result["data"], (dict, FlexMessage))
        if isinstance(result["data"], FlexMessage):
            assert result["data"].alt_text == "籤詩結果"
            assert result["data"].contents is not None
    
    def test_handle_radar(self):
        """測試雷達命令處理"""
        with patch('services.features.radar.radar') as mock_radar:
            mock_radar.return_value = ["https://example.com/radar.jpg"]
            result = handle_command("radar", {})
            
            assert result["type"] == "mixed"
            assert isinstance(result["data"], list)
            assert len(result["data"]) > 0
    
    def test_handle_invalid(self):
        """測試無效命令處理"""
        result = handle_command(None, {})
        assert result is None 