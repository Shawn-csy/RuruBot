import pytest
from services.features.command_ai import (
    parse_command_with_ai,
    _validate_and_clean_response,
    _validate_astro_command,
    _validate_ticket_command,
    _validate_sixty_poem_command,
    _validate_command_keywords
)
from services.linebot_reply.parse_command import parse_command, parse_command_traditional

class TestCommandParser:
    """命令解析器測試"""

    def test_traditional_parser(self):
        """測試傳統解析方法"""
        test_cases = [
            # 雷達相關
            ("雷達", ("radar", {})),
            ("查看雷達", ("radar", {})),
            ("radar", ("radar", {})),
            
            # 星座相關
            ("金牛座", ("astro", {"astro_name": "金牛座", "type": "daily"})),
            ("金牛座 -w", ("astro", {"astro_name": "金牛座", "type": "weekly"})),
            
            # 籤詩相關
            ("抽淺草寺", ("ticket", {"text": "抽淺草寺"})),
            ("抽六十甲子籤", ("sixty_poem", {"text": ""})),
            
            # 國師相關
            ("本週國師", ("podcast", {})),
            
            # 無效輸入
            ("隨便說話", (None, {})),
        ]
        
        for input_text, expected in test_cases:
            command, params = parse_command_traditional(input_text)
            assert (command, params) == expected

    def test_ai_parser_validation(self):
        """測試 AI 解析器的驗證功能"""
        # 測試星座驗證
        assert _validate_astro_command({
            "astro_name": "金牛座",
            "type": "daily"
        }) == True
        
        assert _validate_astro_command({
            "astro_name": "不存在座",
            "type": "daily"
        }) == False
        
        # 測試淺草寺籤驗證
        assert _validate_ticket_command(
            {"text": "工作運"}, 
            "幫我抽一張淺草寺籤"
        ) == True
        
        assert _validate_ticket_command(
            {"text": "工作運"}, 
            "抽個籤看看"
        ) == True
        
        # 測試六十甲子籤驗證
        assert _validate_sixty_poem_command(
            {"text": "感情運"}, 
            "抽六十甲子籤"
        ) == True

    def test_command_keywords_validation(self):
        """測試命令關鍵字驗證"""
        test_cases = [
            ("radar", "查看雷達圖", True),
            ("ticket", "幫我抽個淺草寺籤", True),
            ("ticket", "運勢如何", False),
            ("astro", "金牛座今天運勢", True),
            ("podcast", "看看本週國師", True),
        ]
        
        for command, text, expected in test_cases:
            assert _validate_command_keywords(command, text) == expected

    def test_integrated_parser(self):
        """測試整合後的解析器"""
        test_cases = [
            # 傳統解析的案例 - 完整比對
            ("雷達", ("radar", {})),
            ("金牛座", ("astro", {"astro_name": "金牛座", "type": "daily"})),
            ("抽淺草寺", ("ticket", {"text": "抽淺草寺"})),
            
            # AI 解析的案例 - 只檢查命令類型
            ("幫我看看今天運勢", "astro"),
            ("我想抽個籤問問", "ticket"),
            ("請問可以幫我抽籤嗎", "ticket"),
            ("想知道這週運勢", "astro"),
            
            # 無效輸入
            ("", (None, {})),
        ]
        
        for input_text, expected in test_cases:
            command, params = parse_command(input_text)
            if isinstance(expected, str):
                assert command == expected, f"Failed for input: {input_text}"
                if command == "ticket":
                    assert "text" in params
                elif command == "astro":
                    assert "astro_name" in params
                    assert "type" in params
            else:
                assert (command, params) == expected, f"Failed for input: {input_text}" 